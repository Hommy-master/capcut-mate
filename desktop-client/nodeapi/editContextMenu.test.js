const { test } = require('node:test');
const assert = require('node:assert/strict');
const { buildEditMenuTemplate } = require('./editContextMenu');

test('editable field is left to the renderer menu', () => {
  const template = buildEditMenuTemplate({
    isEditable: true,
    editFlags: {
      canCut: true,
      canCopy: true,
      canPaste: true,
      canDelete: true,
      canSelectAll: true,
    },
    selectionText: 'https://example.com',
  });
  assert.deepEqual(template, []);
});

test('non-editable selection only offers copy', () => {
  const template = buildEditMenuTemplate({
    isEditable: false,
    selectionText: 'selected',
  });
  assert.deepEqual(template, [{ role: 'copy', label: '复制' }]);
});

test('empty non-editable area has no menu', () => {
  const template = buildEditMenuTemplate({
    isEditable: false,
    selectionText: '',
    editFlags: {},
  });
  assert.deepEqual(template, []);
});
