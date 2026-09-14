#!/usr/bin/env bash
# macOS CI：安装包构建（含签名/公证/DMG），对 DMG Resource busy 等偶发错误自动重试
set -euo pipefail

INSTALLER_COMMAND="${1:?installer npm script required}"
MAX_ATTEMPTS="${MAC_BUILD_MAX_ATTEMPTS:-3}"

cleanup_dmg_devices() {
  echo "Cleaning up attached DMG devices (best effort)..."
  # 卸下可能残留的临时磁盘，减轻 hdiutil Resource busy
  hdiutil info 2>/dev/null | awk '/\/dev\/disk[0-9]+/ {print $1}' | sort -u | while read -r disk; do
    hdiutil detach -force "$disk" >/dev/null 2>&1 || true
  done || true
  sleep 2
}

unlock_signing_keychain() {
  if [ -n "${KEYCHAIN_PATH:-}" ] && [ -n "${KEYCHAIN_PASSWORD:-}" ]; then
    security unlock-keychain -p "$KEYCHAIN_PASSWORD" "$KEYCHAIN_PATH" || true
    security set-key-partition-list \
      -S apple-tool:,apple:,codesign: \
      -s -k "$KEYCHAIN_PASSWORD" \
      "$KEYCHAIN_PATH" || true
  fi
}

is_retryable_build_error() {
  local log_file="$1"
  grep -Eiq \
    'Resource busy|Unable to detach device|couldn.?t eject|hdiutil|DMGError|ECONNRESET|ETIMEDOUT|timed out|offline|No network route' \
    "$log_file"
}

LOG_FILE="$(mktemp)"
trap 'rm -f "$LOG_FILE"' EXIT

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  echo "==> mac installer attempt ${attempt}/${MAX_ATTEMPTS}: npm run ${INSTALLER_COMMAND}"
  unlock_signing_keychain
  cleanup_dmg_devices

  set +e
  npm run "$INSTALLER_COMMAND" 2>&1 | tee "$LOG_FILE"
  status=${PIPESTATUS[0]}
  set -e

  if [ "$status" -eq 0 ]; then
    echo "==> mac installer succeeded on attempt ${attempt}"
    exit 0
  fi

  echo "==> mac installer failed on attempt ${attempt} (exit ${status})"
  if [ "$attempt" -ge "$MAX_ATTEMPTS" ]; then
    exit "$status"
  fi
  if ! is_retryable_build_error "$LOG_FILE"; then
    echo "==> error does not look retryable; stopping"
    exit "$status"
  fi

  sleep $((attempt * 20))
done

exit 1
