const { test, after } = require("node:test");
const assert = require("node:assert/strict");
const http = require("http");
const os = require("os");
const path = require("path");
const fs = require("fs").promises;
const fsSync = require("fs");
const Module = require("module");

// resumableDownload -> logger -> electron；单测里用最小 stub 替代。
const USER_DATA_DIR = path.join(os.tmpdir(), "capcut-mate-resumable-test");
fsSync.mkdirSync(path.join(USER_DATA_DIR, "logs"), { recursive: true });

const originalLoad = Module._load;
Module._load = function (request, parent, isMain) {
  if (request === "electron") {
    return { app: { getPath: () => USER_DATA_DIR } };
  }
  return originalLoad.call(this, request, parent, isMain);
};

const { downloadBinaryToFile } = require("./resumableDownload");
const log4js = require("log4js");

after(() => {
  log4js.shutdown(() => {});
});

const BODY = Buffer.alloc(256 * 1024);
for (let i = 0; i < BODY.length; i += 1) {
  BODY[i] = i % 251;
}

/**
 * 模拟素材 CDN：
 * - HEAD 可配置返回 200 / 405 / 500（failFirstHead 时第一次 500）；
 * - Range 从 EOF 开始时可配置返回 500 或标准 416；
 * - Range: bytes=0-0 可配置成失败，用于覆盖探测失败后的 416 路径。
 */
function createFileServer(options = {}) {
  const {
    headStatus = 200,
    eofRangeStatus = 500,
    zeroRangeStatus = null,
    failFirstHead = false,
  } = options;
  const requests = [];
  let headCount = 0;

  const server = http.createServer((req, res) => {
    requests.push({ method: req.method, range: req.headers.range || null });

    if (req.method === "HEAD") {
      headCount += 1;
      if (failFirstHead && headCount === 1) {
        res.writeHead(500);
        res.end();
        return;
      }
      if (headStatus !== 200) {
        res.writeHead(headStatus);
        res.end();
        return;
      }
      res.writeHead(200, {
        "content-length": String(BODY.length),
        "content-type": "application/octet-stream",
        "accept-ranges": "bytes",
      });
      res.end();
      return;
    }

    const range = req.headers.range;
    if (range) {
      const match = /^bytes=(\d+)-(\d*)$/.exec(range);
      if (match) {
        const start = Number(match[1]);
        const end = match[2] ? Number(match[2]) : BODY.length - 1;

        if (start === 0 && end === 0 && zeroRangeStatus != null) {
          res.writeHead(zeroRangeStatus);
          res.end();
          return;
        }

        if (start >= BODY.length) {
          if (eofRangeStatus === 416) {
            res.writeHead(416, {
              "content-range": `bytes */${BODY.length}`,
            });
            res.end();
          } else {
            res.writeHead(eofRangeStatus, { "content-type": "text/plain" });
            res.end("range error");
          }
          return;
        }

        const last = Math.min(end, BODY.length - 1);
        res.writeHead(206, {
          "content-length": String(last - start + 1),
          "content-range": `bytes ${start}-${last}/${BODY.length}`,
          "content-type": "application/octet-stream",
          "accept-ranges": "bytes",
        });
        res.end(BODY.subarray(start, last + 1));
        return;
      }
    }

    res.writeHead(200, {
      "content-length": String(BODY.length),
      "content-type": "application/octet-stream",
      "accept-ranges": "bytes",
    });
    res.end(BODY);
  });

  return { server, requests };
}

async function startServer(target) {
  await new Promise((resolve) => target.server.listen(0, "127.0.0.1", resolve));
  return `http://127.0.0.1:${target.server.address().port}/video.mp4`;
}

async function stopServer(target) {
  await new Promise((resolve) => target.server.close(resolve));
}

async function makeDestDir() {
  return fs.mkdtemp(path.join(os.tmpdir(), "capcut-resume-"));
}

function getRequests(target, method, range) {
  return target.requests.filter(
    (r) =>
      r.method === method &&
      (range === undefined || r.range === range)
  );
}

test("complete local file: HEAD detects it and no GET is sent", async (t) => {
  const target = createFileServer({ eofRangeStatus: 500 });
  const url = await startServer(target);
  t.after(() => stopServer(target));

  const dir = await makeDestDir();
  t.after(() => fs.rm(dir, { recursive: true, force: true }));
  const dest = path.join(dir, "video.mp4");
  await fs.writeFile(dest, BODY);

  const result = await downloadBinaryToFile(url, { destPath: dest });

  assert.equal(result, dest);
  assert.deepEqual(await fs.readFile(dest), BODY);
  assert.equal(getRequests(target, "HEAD").length, 1);
  // 关键回归：本地已完整时不能发 GET，尤其是 bytes=<total>- 的 EOF Range。
  assert.equal(getRequests(target, "GET").length, 0);
});

test("partial local file: resumes with Range and completes", async (t) => {
  const target = createFileServer({ eofRangeStatus: 500 });
  const url = await startServer(target);
  t.after(() => stopServer(target));

  const dir = await makeDestDir();
  t.after(() => fs.rm(dir, { recursive: true, force: true }));
  const dest = path.join(dir, "video.mp4");
  const half = Math.floor(BODY.length / 2);
  await fs.writeFile(dest, BODY.subarray(0, half));

  const result = await downloadBinaryToFile(url, { destPath: dest });

  assert.equal(result, dest);
  assert.deepEqual(await fs.readFile(dest), BODY);
  const gets = getRequests(target, "GET");
  assert.equal(gets.length, 1);
  assert.equal(gets[0].range, `bytes=${half}-`);
});

test("local file larger than remote: restarts from byte 0", async (t) => {
  const target = createFileServer({ eofRangeStatus: 500 });
  const url = await startServer(target);
  t.after(() => stopServer(target));

  const dir = await makeDestDir();
  t.after(() => fs.rm(dir, { recursive: true, force: true }));
  const dest = path.join(dir, "video.mp4");
  await fs.writeFile(dest, Buffer.concat([BODY, Buffer.from("stale")]));

  const result = await downloadBinaryToFile(url, { destPath: dest });

  assert.equal(result, dest);
  assert.deepEqual(await fs.readFile(dest), BODY);
  const gets = getRequests(target, "GET");
  assert.equal(gets.length, 1);
  assert.equal(gets[0].range, null);
});

test("HEAD unsupported: 1-byte Range probe detects complete file", async (t) => {
  const target = createFileServer({
    headStatus: 405,
    eofRangeStatus: 500,
  });
  const url = await startServer(target);
  t.after(() => stopServer(target));

  const dir = await makeDestDir();
  t.after(() => fs.rm(dir, { recursive: true, force: true }));
  const dest = path.join(dir, "video.mp4");
  await fs.writeFile(dest, BODY);

  const result = await downloadBinaryToFile(url, { destPath: dest });

  assert.equal(result, dest);
  assert.deepEqual(await fs.readFile(dest), BODY);
  assert.equal(getRequests(target, "HEAD").length, 1);
  const gets = getRequests(target, "GET");
  assert.equal(gets.length, 1);
  assert.equal(gets[0].range, "bytes=0-0");
});

test("range request error: second HEAD confirms complete file", async (t) => {
  const target = createFileServer({
    failFirstHead: true,
    zeroRangeStatus: 405,
    eofRangeStatus: 500,
  });
  const url = await startServer(target);
  t.after(() => stopServer(target));

  const dir = await makeDestDir();
  t.after(() => fs.rm(dir, { recursive: true, force: true }));
  const dest = path.join(dir, "video.mp4");
  await fs.writeFile(dest, BODY);

  const result = await downloadBinaryToFile(url, { destPath: dest });

  assert.equal(result, dest);
  assert.deepEqual(await fs.readFile(dest), BODY);
  assert.equal(getRequests(target, "HEAD").length, 2);
  const gets = getRequests(target, "GET");
  assert.equal(gets.length, 2);
  assert.equal(gets[0].range, "bytes=0-0");
  assert.equal(gets[1].range, `bytes=${BODY.length}-`);
});

test("standard 416 is still handled when probes are unavailable", async (t) => {
  const target = createFileServer({
    headStatus: 405,
    zeroRangeStatus: 405,
    eofRangeStatus: 416,
  });
  const url = await startServer(target);
  t.after(() => stopServer(target));

  const dir = await makeDestDir();
  t.after(() => fs.rm(dir, { recursive: true, force: true }));
  const dest = path.join(dir, "video.mp4");
  await fs.writeFile(dest, BODY);

  const result = await downloadBinaryToFile(url, { destPath: dest });

  assert.equal(result, dest);
  assert.deepEqual(await fs.readFile(dest), BODY);
  const gets = getRequests(target, "GET");
  assert.equal(gets.length, 2);
  assert.equal(gets[0].range, "bytes=0-0");
  assert.equal(gets[1].range, `bytes=${BODY.length}-`);
});

test("fresh download: no HEAD probe, plain GET", async (t) => {
  const target = createFileServer();
  const url = await startServer(target);
  t.after(() => stopServer(target));

  const dir = await makeDestDir();
  t.after(() => fs.rm(dir, { recursive: true, force: true }));
  const dest = path.join(dir, "video.mp4");

  const result = await downloadBinaryToFile(url, { destPath: dest });

  assert.equal(result, dest);
  assert.deepEqual(await fs.readFile(dest), BODY);
  assert.equal(getRequests(target, "HEAD").length, 0);
  const gets = getRequests(target, "GET");
  assert.equal(gets.length, 1);
  assert.equal(gets[0].range, null);
});
