const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

function loadModule() {
  const source = fs.readFileSync(path.join(__dirname, 'draftUrlInput.js'), 'utf8');
  const wrapped = source
    .replace(/export function /g, 'function ')
    .concat('\nmodule.exports = { isMacPlatform, isElectronRenderer, shortcutModifierLabel, normalizeDraftUrlPaste, replaceSelection };\n');
  const context = { module: { exports: {} }, exports: {}, navigator: { platform: 'Win32', userAgent: 'Windows' } };
  context.module.exports = context.exports;
  vm.runInNewContext(wrapped, context);
  return context.module.exports;
}

const {
  normalizeDraftUrlPaste,
  replaceSelection,
  shortcutModifierLabel,
} = loadModule();

test('keeps a single url unchanged', () => {
  const url = 'https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=1';
  assert.equal(normalizeDraftUrlPaste(url), url);
});

test('splits multiple urls onto their own lines', () => {
  const pasted = 'https://a.example/x?draft_id=1 https://b.example/y?draft_id=2';
  assert.equal(
    normalizeDraftUrlPaste(pasted),
    'https://a.example/x?draft_id=1\nhttps://b.example/y?draft_id=2'
  );
});

test('normalizes windows newlines for ordinary text', () => {
  assert.equal(normalizeDraftUrlPaste('a\r\nb\rc'), 'a\nb\nc');
});

test('replaceSelection inserts at the caret', () => {
  const inserted = replaceSelection('ab', 1, 1, 'X');
  assert.equal(inserted.next, 'aXb');
  assert.equal(inserted.caret, 2);
  const replaced = replaceSelection('abcd', 1, 3, 'Z');
  assert.equal(replaced.next, 'aZd');
  assert.equal(replaced.caret, 2);
});

test('windows shortcut label is Ctrl', () => {
  assert.equal(shortcutModifierLabel(), 'Ctrl');
});
