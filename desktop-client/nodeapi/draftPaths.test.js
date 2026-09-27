const { test } = require('node:test');
const assert = require('node:assert/strict');
const path = require('path');
const draftPaths = require('./draftPaths');

const DRAFT_DIR = path.join('C:', 'Users', 'me', 'drafts', '20260927202001abcd');
const PREFIX = draftPaths.placeholderPrefix();

test('placeholder prefix matches the jianying native form', () => {
  assert.equal(
    PREFIX,
    '##_draftpath_placeholder_0E685133-18CE-45ED-8CB8-2904A212EC80_##'
  );
});

test('absolute path inside the draft dir becomes placeholder-relative', () => {
  const inside = path.join(DRAFT_DIR, 'assets', 'videos', 'a.mp4');
  assert.equal(
    draftPaths.toDraftRelative(inside, DRAFT_DIR),
    `${PREFIX}/assets/videos/a.mp4`
  );
});

test('posix-separated absolute path inside the draft dir is handled too', () => {
  const inside = 'C:/Users/me/drafts/20260927202001abcd/assets/videos/a.mp4';
  assert.equal(
    draftPaths.toDraftRelative(inside, 'C:/Users/me/drafts/20260927202001abcd'),
    `${PREFIX}/assets/videos/a.mp4`
  );
});

test('http urls, existing placeholders and relative paths are left alone', () => {
  const url = 'https://cdn.example.com/a.mp4';
  assert.equal(draftPaths.toDraftRelative(url, DRAFT_DIR), url);
  const already = `${PREFIX}/assets/videos/a.mp4`;
  assert.equal(draftPaths.toDraftRelative(already, DRAFT_DIR), already);
  assert.equal(draftPaths.toDraftRelative('assets/videos/a.mp4', DRAFT_DIR), 'assets/videos/a.mp4');
});

test('absolute paths outside the draft dir are left alone', () => {
  const outside = path.join('C:', 'other', 'a.mp4');
  assert.equal(draftPaths.toDraftRelative(outside, DRAFT_DIR), outside);
});

test('font sentinels are not mistaken for absolute paths', () => {
  assert.equal(draftPaths.isAbsLike('D:'), false);
  assert.equal(draftPaths.isAbsLike('C:'), false);
  assert.equal(draftPaths.toDraftRelative('D:', DRAFT_DIR), 'D:');
  assert.equal(draftPaths.toDraftFilePath('D:'), 'D:');
});

test('toDraftFilePath prefixes ./ and strips any placeholder', () => {
  assert.equal(
    draftPaths.toDraftFilePath(`${PREFIX}/assets/videos/a.mp4`),
    './assets/videos/a.mp4'
  );
  assert.equal(draftPaths.toDraftFilePath('assets/videos/a.mp4'), './assets/videos/a.mp4');
});

test('rewrite is idempotent and skips non-path keys', () => {
  const materials = {
    videos: [{ path: path.join(DRAFT_DIR, 'assets', 'videos', 'a.mp4'), type: 'video' }],
    audios: [],
    texts: [{ font_path: 'D:', styles: [{ font: { path: 'D:' } }] }],
  };
  assert.equal(draftPaths.normalizeMaterialPaths(materials, DRAFT_DIR), true);
  assert.equal(materials.videos[0].path, `${PREFIX}/assets/videos/a.mp4`);
  assert.equal(materials.texts[0].font_path, 'D:');
  assert.equal(materials.texts[0].styles[0].font.path, 'D:');
  assert.equal(draftPaths.normalizeMaterialPaths(materials, DRAFT_DIR), false);
});

test('material_save_mode follows the actual paths', () => {
  const local = { videos: [{ path: `${PREFIX}/assets/videos/a.mp4` }], audios: [] };
  assert.equal(draftPaths.computeMaterialSaveMode(local, DRAFT_DIR), 1);

  const remote = { videos: [{ path: 'https://cdn/a.mp4' }], audios: [] };
  assert.equal(draftPaths.computeMaterialSaveMode(remote, DRAFT_DIR), 0);

  const external = { videos: [{ path: path.join('E:', 'external', 'a.mp4') }], audios: [] };
  assert.equal(draftPaths.computeMaterialSaveMode(external, DRAFT_DIR), 0);
});

test('normalizeDraftContent localizes then recomputes the mode', () => {
  const jsonData = {
    config: { material_save_mode: 0 },
    materials: {
      videos: [{ path: path.join(DRAFT_DIR, 'assets', 'videos', 'a.mp4') }],
      audios: [],
    },
  };
  assert.equal(draftPaths.normalizeDraftContent(jsonData, DRAFT_DIR), 1);
  assert.equal(jsonData.materials.videos[0].path, `${PREFIX}/assets/videos/a.mp4`);
  assert.equal(jsonData.config.material_save_mode, 1);
});

test('url mode keeps mode 0 so jianying knows the media is not in the draft', () => {
  const jsonData = {
    config: {},
    materials: { videos: [{ path: 'https://cdn.example.com/a.mp4' }], audios: [] },
  };
  assert.equal(draftPaths.normalizeDraftContent(jsonData, DRAFT_DIR), 0);
  assert.equal(jsonData.config.material_save_mode, 0);
});

test('localizeDraftMeta rewrites server paths to the local draft dir', () => {
  const meta = {
    draft_name: 'server-side-name',
    draft_fold_path: 'C:/server/drafts/20260927202001abcd',
    draft_root_path: 'C:/server/drafts',
    draft_materials: [
      { type: 0, value: [{ file_Path: `${PREFIX}/assets/videos/a.mp4` }] },
      { type: 1, value: [] },
    ],
  };
  draftPaths.localizeDraftMeta(meta, DRAFT_DIR, '20260927202001abcd');

  assert.equal(meta.draft_name, '20260927202001abcd');
  assert.equal(meta.draft_fold_path, DRAFT_DIR.replace(/\\/g, '/'));
  assert.equal(meta.draft_root_path, path.dirname(DRAFT_DIR).replace(/\\/g, '/'));
  assert.equal(meta.draft_materials[0].value[0].file_Path, './assets/videos/a.mp4');
  // 未被识别的分组保持原样
  assert.deepEqual(meta.draft_materials[1], { type: 1, value: [] });
  // 服务端路径不应残留
  assert.equal(JSON.stringify(meta).includes('C:/server'), false);
});

test('materialLocalDir routes through the shared media-root constant', () => {
  assert.equal(
    draftPaths.materialLocalDir(DRAFT_DIR, 'videos'),
    path.join(DRAFT_DIR, draftPaths.DRAFT_MEDIA_ROOT, 'videos')
  );
  // 与 Python 侧 draft_paths.DRAFT_MEDIA_ROOT 必须一致
  assert.equal(draftPaths.DRAFT_MEDIA_ROOT, 'assets');
});

test('env var can override the placeholder id', () => {
  const original = process.env.DRAFT_PATH_PLACEHOLDER_ID;
  process.env.DRAFT_PATH_PLACEHOLDER_ID = 'TEST-UUID';
  try {
    assert.equal(
      draftPaths.placeholderPrefix(),
      '##_draftpath_placeholder_TEST-UUID_##'
    );
  } finally {
    if (original === undefined) delete process.env.DRAFT_PATH_PLACEHOLDER_ID;
    else process.env.DRAFT_PATH_PLACEHOLDER_ID = original;
  }
});
