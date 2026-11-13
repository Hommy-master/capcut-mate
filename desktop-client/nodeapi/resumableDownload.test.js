const { test } = require('node:test');
const assert = require('node:assert/strict');

const { createDegradeDetector } = require('./downloadSpeedGuard');

const KB = 1024;

test('fast link needs two consecutive slow windows to degrade', () => {
  const detect = createDegradeDetector();

  assert.equal(detect(300 * KB).degraded, false); // 窗口 1：建立基线
  assert.equal(detect(300 * KB).degraded, false); // 窗口 2：维持
  assert.equal(detect(10 * KB).degraded, false); // 窗口 3：劣化 1/2
  assert.equal(detect(10 * KB).degraded, true); // 窗口 4：劣化 2/2
});

test('slow link below baseline floor never degrades', () => {
  const detect = createDegradeDetector();

  for (let i = 0; i < 10; i += 1) {
    assert.equal(detect(200 * KB).degraded, false);
  }
});

test('link below 256KiB/s floor does not rotate even after a drop', () => {
  const detect = createDegradeDetector();

  assert.equal(detect(200 * KB).degraded, false); // 基线 200KiB/s（低于门槛）
  assert.equal(detect(200 * KB).degraded, false);
  assert.equal(detect(10 * KB).degraded, false); // 掉速也不判定劣化
  assert.equal(detect(10 * KB).degraded, false);
});

test('baseline is frozen while degradation is suspected', () => {
  const detect = createDegradeDetector();

  detect(300 * KB); // 基线 300KiB/s（略高于 256KiB/s 门槛）
  assert.equal(detect(10 * KB).degraded, false); // 劣化 1/2，基线冻结
  // 若基线被劣化样本拉低到 256KiB/s 以下，这里会漏报；冻结后必须触发。
  assert.equal(detect(10 * KB).degraded, true);
});

test('recovery resets the slow window counter', () => {
  const detect = createDegradeDetector();

  detect(300 * KB);
  detect(300 * KB);
  assert.equal(detect(10 * KB).degraded, false); // 劣化 1/2
  assert.equal(detect(300 * KB).degraded, false); // 恢复，计数清零
  assert.equal(detect(10 * KB).degraded, false); // 重新劣化 1/2
  assert.equal(detect(10 * KB).degraded, true); // 劣化 2/2
});

test('gradual decay still degrades before baseline sinks below the floor', () => {
  const detect = createDegradeDetector();

  detect(588 * KB); // 窗口 1：峰值基线
  detect(392 * KB);
  detect(196 * KB);
  assert.equal(detect(98 * KB).degraded, false); // 劣化 1/2
  // 旧 EWMA 基线已沉到 256KiB/s 以下；快升慢降基线仍保持高位 → 必须触发。
  assert.equal(detect(38 * KB).degraded, true); // 劣化 2/2
});

test('drop from peak to a still-usable speed does not rotate', () => {
  const detect = createDegradeDetector();

  detect(2 * 1024 * KB); // 峰值约 2MiB/s
  for (let i = 0; i < 4; i += 1) {
    // 不足峰值 20%，但仍高于 256KiB/s，重连只会打断传输。
    assert.equal(detect(294 * KB).degraded, false);
  }
});
