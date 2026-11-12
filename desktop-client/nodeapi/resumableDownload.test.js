const { test } = require('node:test');
const assert = require('node:assert/strict');

const { createDegradeDetector } = require('./downloadSpeedGuard');

const KB = 1024;

test('fast link needs two consecutive slow windows to degrade', () => {
  const detect = createDegradeDetector();

  assert.equal(detect(100 * KB).degraded, false); // 窗口 1：建立基线
  assert.equal(detect(100 * KB).degraded, false); // 窗口 2：维持
  assert.equal(detect(10 * KB).degraded, false); // 窗口 3：劣化 1/2
  assert.equal(detect(10 * KB).degraded, true); // 窗口 4：劣化 2/2
});

test('slow link below baseline floor never degrades', () => {
  const detect = createDegradeDetector();

  for (let i = 0; i < 10; i += 1) {
    assert.equal(detect(2 * KB).degraded, false);
  }
});

test('baseline is frozen while degradation is suspected', () => {
  const detect = createDegradeDetector();

  detect(70 * KB); // 基线 70KiB/s（略高于门槛）
  assert.equal(detect(10 * KB).degraded, false); // 劣化 1/2，基线冻结
  // 若基线被劣化样本拉低到 64KiB/s 以下，这里会漏报；冻结后必须触发。
  assert.equal(detect(10 * KB).degraded, true);
});

test('recovery resets the slow window counter', () => {
  const detect = createDegradeDetector();

  detect(100 * KB);
  detect(100 * KB);
  assert.equal(detect(10 * KB).degraded, false); // 劣化 1/2
  assert.equal(detect(100 * KB).degraded, false); // 恢复，计数清零
  assert.equal(detect(10 * KB).degraded, false); // 重新劣化 1/2
  assert.equal(detect(10 * KB).degraded, true); // 劣化 2/2
});
