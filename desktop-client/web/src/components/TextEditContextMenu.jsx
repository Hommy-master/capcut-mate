import { useEffect } from 'react';
import { Scissors, Copy, Clipboard, Trash, CheckAll } from 'react-bootstrap-icons';
import { shortcutModifierLabel } from '../utils/draftUrlInput';

const MENU_WIDTH = 240;
const MENU_ESTIMATED_HEIGHT = 240;

function clampPosition(x, y) {
  const maxX = Math.max(8, window.innerWidth - MENU_WIDTH - 8);
  const maxY = Math.max(8, window.innerHeight - MENU_ESTIMATED_HEIGHT - 8);
  return {
    left: Math.min(Math.max(8, x), maxX),
    top: Math.min(Math.max(8, y), maxY),
  };
}

function TextEditContextMenu({
  x,
  y,
  canCut,
  canCopy,
  canPaste,
  canDelete,
  canSelectAll,
  onCut,
  onCopy,
  onPaste,
  onDelete,
  onSelectAll,
  onClose,
}) {
  const mod = shortcutModifierLabel();
  const position = clampPosition(x, y);

  useEffect(() => {
    const handleKey = (event) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };
    const handleDismiss = () => onClose();
    window.addEventListener('keydown', handleKey);
    window.addEventListener('resize', handleDismiss);
    window.addEventListener('scroll', handleDismiss, true);
    return () => {
      window.removeEventListener('keydown', handleKey);
      window.removeEventListener('resize', handleDismiss);
      window.removeEventListener('scroll', handleDismiss, true);
    };
  }, [onClose]);

  const items = [
    { key: 'cut', label: '剪切', shortcut: `${mod}+X`, enabled: canCut, action: onCut, Icon: Scissors },
    { key: 'copy', label: '复制', shortcut: `${mod}+C`, enabled: canCopy, action: onCopy, Icon: Copy },
    { key: 'paste', label: '粘贴', shortcut: `${mod}+V`, enabled: canPaste, action: onPaste, Icon: Clipboard },
    { key: 'delete', label: '删除', enabled: canDelete, action: onDelete, Icon: Trash },
    { key: 'sep-1', separator: true },
    { key: 'selectAll', label: '全选', shortcut: `${mod}+A`, enabled: canSelectAll, action: onSelectAll, Icon: CheckAll },
  ];

  return (
    <>
      <div className="text-edit-context-backdrop" onMouseDown={onClose} />
      <ul
        className="text-edit-context-menu"
        style={{ left: position.left, top: position.top }}
        role="menu"
        onMouseDown={(event) => event.preventDefault()}
      >
        {items.map((item) =>
          item.separator ? (
            <li key={item.key} className="text-edit-context-separator" role="separator" />
          ) : (
            <li key={item.key} role="none">
              <button
                type="button"
                role="menuitem"
                className="text-edit-context-item"
                disabled={!item.enabled}
                onClick={() => {
                  if (!item.enabled) {
                    return;
                  }
                  item.action();
                  onClose();
                }}
              >
                <span className="text-edit-context-icon" aria-hidden="true">
                  <item.Icon size={15} />
                </span>
                <span className="text-edit-context-label">{item.label}</span>
                {item.shortcut ? <span className="text-edit-context-shortcut">{item.shortcut}</span> : null}
              </button>
            </li>
          )
        )}
      </ul>
    </>
  );
}

export default TextEditContextMenu;
