/**
 * 断点续传的相对劣化判定器：以连接自身近期吞吐（EWMA）为基线。
 *
 * - 基线低于 64KiB/s 的慢链路不轮换：本来就慢，换连接通常没有意义；
 * - 快链路连续两个 5s 采样窗口低于基线 20% 才判定劣化；
 * - 疑似劣化期间冻结基线，避免基线被劣化样本拉低后漏报。
 *
 * 与 capcut-mate Python 端 src/utils/draft_downloader.py 的策略保持一致。
 */
const DEGRADE_RATIO = 0.2;
const DEGRADE_CONSECUTIVE_WINDOWS = 2;
const DEGRADE_MIN_BASELINE_BYTES_PER_SEC = 64 * 1024;
const BASELINE_EWMA_ALPHA = 0.3;

function createDegradeDetector() {
  let speedWindowIndex = 0;
  let baselineSpeed = 0;
  let slowWindows = 0;

  return function observe(speed) {
    speedWindowIndex += 1;
    let degraded = false;
    let updateBaseline = true;

    if (
      speedWindowIndex > 1 &&
      baselineSpeed >= DEGRADE_MIN_BASELINE_BYTES_PER_SEC
    ) {
      if (speed < baselineSpeed * DEGRADE_RATIO) {
        slowWindows += 1;
        updateBaseline = false;
        degraded = slowWindows >= DEGRADE_CONSECUTIVE_WINDOWS;
      } else {
        slowWindows = 0;
      }
    } else {
      slowWindows = 0;
    }

    if (updateBaseline) {
      baselineSpeed =
        baselineSpeed === 0
          ? speed
          : BASELINE_EWMA_ALPHA * speed +
            (1 - BASELINE_EWMA_ALPHA) * baselineSpeed;
    }

    return { degraded, baseline: baselineSpeed };
  };
}

module.exports = {
  createDegradeDetector,
};
