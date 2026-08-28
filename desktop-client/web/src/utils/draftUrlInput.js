/**
 * 草稿地址输入：识别 macOS / Windows，规范化粘贴内容。
 */

export function isMacPlatform() {
  if (typeof navigator === 'undefined') {
    return false;
  }
  const platform = navigator.platform || '';
  const ua = navigator.userAgent || '';
  return /Mac|iPhone|iPad|iPod/i.test(platform) || /Mac OS X/i.test(ua);
}

export function isElectronRenderer() {
  return Boolean(typeof window !== 'undefined' && window.electronAPI);
}

export function shortcutModifierLabel() {
  return isMacPlatform() ? '⌘' : 'Ctrl';
}

/**
 * 粘贴多个草稿 URL 时，拆成一行一个；普通文本保持原样（仅统一换行）。
 */
export function normalizeDraftUrlPaste(text) {
  const raw = String(text || '')
    .replace(/\r\n/g, '\n')
    .replace(/\r/g, '\n');
  const urlTokens = raw
    .split(/\s+/)
    .map((token) => token.trim())
    .filter((token) => /^https?:\/\//i.test(token));
  if (urlTokens.length >= 2) {
    return urlTokens.join('\n');
  }
  return raw;
}

export function replaceSelection(value, start, end, insert) {
  const from = Math.max(0, start ?? 0);
  const to = Math.max(from, end ?? from);
  const next = `${value.slice(0, from)}${insert}${value.slice(to)}`;
  return {
    next,
    caret: from + String(insert).length,
  };
}
