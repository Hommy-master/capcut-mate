#!/usr/bin/env python3
"""草稿下载稳定性测试：重复下载同一草稿，统计每次完整下载耗时。

用法（项目根目录）：
    .venv/bin/python -I scripts/stability_test_draft_download.py \
        --url "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025120421372636a27729" \
        --iterations 100

每次迭代都会删除本地草稿目录后重新下载，确保统计的是完整下载耗时，
而不是断点续传/已有文件跳过的耗时。
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


def _percentile(sorted_values: List[float], ratio: float) -> float:
    if not sorted_values:
        return 0.0
    index = min(len(sorted_values) - 1, int(round((len(sorted_values) - 1) * ratio)))
    return sorted_values[index]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--save-root", default=os.path.join(PROJECT_ROOT, "temp", "stability"))
    parser.add_argument("--keep", action="store_true", help="保留最后一次下载的草稿目录")
    args = parser.parse_args()

    draft_id = dd.extract_draft_id_from_url(args.url)
    if not draft_id:
        print(f"无法从 URL 解析 draft_id: {args.url}", file=sys.stderr)
        return 2

    os.makedirs(args.save_root, exist_ok=True)
    target_dir = os.path.join(args.save_root, draft_id)

    durations: List[float] = []
    failures: List[dict] = []

    for i in range(1, args.iterations + 1):
        if os.path.isdir(target_dir):
            shutil.rmtree(target_dir, ignore_errors=True)

        started = time.monotonic()
        result = dd.download_draft_with_result(args.url, save_path=args.save_root)
        elapsed = time.monotonic() - started
        durations.append(elapsed)

        if result.ok:
            print(
                f"[{i}/{args.iterations}] ok  {elapsed:.3f}s",
                flush=True,
            )
        else:
            failures.append(
                {
                    "iteration": i,
                    "elapsed": elapsed,
                    "kind": result.kind.value if result.kind else None,
                    "detail": result.detail,
                    "http_status": result.http_status,
                }
            )
            print(
                f"[{i}/{args.iterations}] FAIL {elapsed:.3f}s kind={result.kind} "
                f"detail={result.detail}",
                flush=True,
            )

    if not args.keep and os.path.isdir(target_dir):
        shutil.rmtree(target_dir, ignore_errors=True)

    sorted_durations = sorted(durations)
    summary = {
        "url": args.url,
        "draft_id": draft_id,
        "iterations": args.iterations,
        "success": len(durations) - len(failures),
        "failure": len(failures),
        "avg_seconds": round(statistics.fmean(durations), 3) if durations else 0.0,
        "min_seconds": round(min(durations), 3) if durations else 0.0,
        "max_seconds": round(max(durations), 3) if durations else 0.0,
        "p50_seconds": round(_percentile(sorted_durations, 0.50), 3),
        "p90_seconds": round(_percentile(sorted_durations, 0.90), 3),
        "p95_seconds": round(_percentile(sorted_durations, 0.95), 3),
        "stdev_seconds": round(statistics.pstdev(durations), 3) if len(durations) > 1 else 0.0,
        "failures": failures,
    }

    report_path = os.path.join(args.save_root, f"stability-report-{draft_id}.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\n===== 稳定性统计 =====")
    print(f"总次数: {summary['iterations']}  成功: {summary['success']}  失败: {summary['failure']}")
    print(f"平均耗时: {summary['avg_seconds']:.3f}s")
    print(f"最短耗时: {summary['min_seconds']:.3f}s")
    print(f"最长耗时: {summary['max_seconds']:.3f}s")
    print(f"P50: {summary['p50_seconds']:.3f}s  P90: {summary['p90_seconds']:.3f}s  "
          f"P95: {summary['p95_seconds']:.3f}s  标准差: {summary['stdev_seconds']:.3f}s")
    print(f"报告: {report_path}")

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
