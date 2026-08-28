/**
 * 可编辑区域由渲染进程自定义菜单处理（含图标）。
 * 这里只给只读选区提供复制；不再包含撤销 / 重做。
 */
function buildEditMenuTemplate(params = {}) {
  const { isEditable, editFlags = {}, selectionText = '' } = params;
  if (isEditable) {
    return [];
  }
  const canCopy = Boolean(editFlags.canCopy || selectionText);
  if (canCopy) {
    return [{ role: 'copy', label: '复制' }];
  }
  return [];
}

function attachEditContextMenu(contents) {
  if (!contents || contents.isDestroyed()) {
    return;
  }
  if (typeof contents.getType === 'function' && contents.getType() === 'devtools') {
    return;
  }
  contents.on('context-menu', (event, params) => {
    if (params.isEditable) {
      return;
    }
    const template = buildEditMenuTemplate(params);
    if (!template.length) {
      return;
    }
    const { Menu, BrowserWindow } = require('electron');
    const menu = Menu.buildFromTemplate(template);
    const window = BrowserWindow.fromWebContents(contents);
    menu.popup({ window });
  });
}

module.exports = {
  attachEditContextMenu,
  buildEditMenuTemplate,
};
