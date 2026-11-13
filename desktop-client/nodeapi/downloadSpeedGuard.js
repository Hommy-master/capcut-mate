/**
 * 断点续传的相对劣化判定器：以连接自身峰值吞吐（快升慢降）为基线。
 *
 * - 基线低于 256KiB/s 的慢链路不轮换：本来就慢，换连接通常没有意义；
 * - 快链路连续两个 5s 采样窗口低于基线 20%、且当前速度也低于 256KiB/s 才判定劣化；
 * - 疑似劣化期间冻结基线，避免基线被劣化样本拉低后漏报；
 * - 基线快升慢降：高于基线的窗口立即抬升，低于基线时每窗口只衰减 2%。
 *   旧的 EWMA 基线会跟随逐窗口劣化一起下降，跌破门槛后看门狗永久失效。
 *
 * 与 capcut-mate Python 端 src/utils/draft_downloader.py 的策略保持一致。
 */
const DEGRADE_RATIO = 0.2;
const DEGRADE_CONSECUTIVE_WINDOWS = 2;
const DEGRADE_MIN_BASELINE_BYTES_PER_SEC = 256 * 1024;
const DEGRADE_MAX_CURRENT_BYTES_PER_SEC = 256 * 1024;
const BASELINE_DECAY_PER_WINDOW = 0.98;

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
      if (
        speed < baselineSpeed * DEGRADE_RATIO &&
        speed < DEGRADE_MAX_CURRENT_BYTES_PER_SEC
      ) {
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
        speed > baselineSpeed
          ? speed
          : Math.max(speed, baselineSpeed * BASELINE_DECAY_PER_WINDOW);
    }

    return { degraded, baseline: baselineSpeed };
  };
}

module.exports = {
  createDegradeDetector,
};
