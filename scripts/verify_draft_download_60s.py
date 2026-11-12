#!/usr/bin/env python3
"""验证草稿下载稳定性：连续 N 次完整下载，每次必须 <= LIMIT 秒。

任一次超时/失败会立即停止，保留现场供分析。
用法（项目根目录）：
    .venv/bin/python -I scripts/verify_draft_download_60s.py \
        --url "http://jc2.hzhuantin.com/openapi/capcut-mate/v1/get_draft?draft_id=20261111155406a6aad615" \
        --iterations 20 --limit 60
"""
import argparse
import json
import os
import shutil
import statistics
import sys
import time
from typing import List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.utils import draft_downloader as dd  # noqa: E402


def _directory_size(path: str) -> int:
    """统计草稿目录实际落盘字节数（含素材），用于计算吞吐。"""
    total = 0
    for root, _dirs, files in os.walk(path):
        for name in files:
            try:
                total += os.path.getsize(os.path.join(root, name))
            except OSError:
                continue
    return total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--limit", type=float, default=60.0)
    parser.add_argument(
        "--save-root", default=os.path.join(PROJECT_ROOT, "temp", "verify60")
    )
    args = parser.parse_args()

    draft_id = dd.extract_draft_id_from_url(args.url)
    if not draft_id:
        print(f"无法解析 draft_id: {args.url}", file=sys.stderr)
        return 2

    # 用与要求一致的硬上限：超过 limit 直接判失败，不再等 600s 总预算。
    dd._DOWNLOAD_PHASE_BUDGET_SECONDS = args.limit

    os.makedirs(args.save_root, exist_ok=True)
    target_dir = os.path.join(args.save_root, draft_id)
    durations: List[float] = []
    sizes: List[int] = []
    speeds: List[float] = []
    failures: List[dict] = []

    for i in range(1, args.iterations + 1):
        shutil.rmtree(target_dir, ignore_errors=True)
        started = time.monotonic()
        result = dd.download_draft_with_result(args.url, save_path=args.save_root)
        elapsed = time.monotonic() - started
        size_bytes = _directory_size(target_dir)
        mbps = size_bytes / elapsed / 1024 / 1024 if elapsed > 0 else 0.0
        durations.append(elapsed)
        sizes.append(size_bytes)
        speeds.append(mbps)

        ok = result.ok and elapsed <= args.limit
        print(
            f"[{i}/{args.iterations}] {'ok' if ok else 'FAIL'} {elapsed:.2f}s "
            f"{size_bytes / 1024 / 1024:.2f}MB {mbps:.2f}MB/s",
            flush=True,
        )

        if not ok:
            failures.append(
                {
                    "iteration": i,
                    "elapsed": round(elapsed, 3),
                    "bytes": size_bytes,
                    "ok": result.ok,
                    "kind": result.kind.value if result.kind else None,
                    "detail": result.detail,
                    "target_dir": target_dir,
                }
            )
            break

        shutil.rmtree(target_dir, ignore_errors=True)

    summary = {
        "url": args.url,
        "draft_id": draft_id,
        "iterations_requested": args.iterations,
        "iterations_done": len(durations),
        "limit_seconds": args.limit,
        "passed": not failures,
        "avg_seconds": round(sum(durations) / len(durations), 3) if durations else 0.0,
        "min_seconds": round(min(durations), 3) if durations else 0.0,
        "max_seconds": round(max(durations), 3) if durations else 0.0,
        "median_seconds": round(statistics.median(durations), 3) if durations else 0.0,
        "durations": [round(x, 3) for x in durations],
        "bytes_per_iteration": sizes,
        "avg_bytes": round(sum(sizes) / len(sizes)) if sizes else 0,
        "avg_mbps": round(sum(speeds) / len(speeds), 3) if speeds else 0.0,
        "failures": failures,
    }
    report_path = os.path.join(args.save_root, f"verify60-report-{draft_id}.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\n===== 60s 验证 =====", flush=True)
    print(
        f"完成 {len(durations)}/{args.iterations} 次，"
        f"平均 {summary['avg_seconds']}s，中位 {summary['median_seconds']}s，"
        f"最快 {summary['min_seconds']}s，最慢 {summary['max_seconds']}s，"
        f"平均 {summary['avg_mbps']}MB/s，限时 {args.limit}s，"
        f"{'通过' if summary['passed'] else '未通过'}",
        flush=True,
    )
    print(f"报告: {report_path}", flush=True)
    if failures:
        print(f"失败详情: {failures}", flush=True)
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
