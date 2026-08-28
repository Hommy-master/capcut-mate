import React, { useCallback, useEffect, useRef, useState } from 'react';
import TextEditContextMenu from './TextEditContextMenu';
import electronService from '../services/electronService';
import {
  isMacPlatform,
  normalizeDraftUrlPaste,
  replaceSelection,
  shortcutModifierLabel,
} from '../utils/draftUrlInput';

const MIN_HEIGHT = 140;
const MAX_HEIGHT = 320;

function Textarea({ value, onChange }) {
  const textareaRef = useRef(null);
  const [textareaHeight, setTextareaHeight] = useState(`${MIN_HEIGHT}px`);
  const [menu, setMenu] = useState(null);
  const mod = shortcutModifierLabel();

  const closeMenu = useCallback(() => setMenu(null), []);

  const adjustTextareaHeight = useCallback((textarea) => {
    if (!textarea) {
      return;
    }
    textarea.style.height = 'auto';
    const next = Math.min(Math.max(textarea.scrollHeight, MIN_HEIGHT), MAX_HEIGHT);
    setTextareaHeight(`${next}px`);
  }, []);

  const focusAndSetCaret = (caret) => {
    const el = textareaRef.current;
    if (!el) {
      return;
    }
    el.focus();
    const pos = Math.max(0, Math.min(caret, el.value.length));
    el.setSelectionRange(pos, pos);
    adjustTextareaHeight(el);
  };

  const applyInsert = (insert) => {
    const el = textareaRef.current;
    const start = el ? el.selectionStart : value.length;
    const end = el ? el.selectionEnd : value.length;
    const { next, caret } = replaceSelection(value, start, end, insert);
    onChange(next);
    requestAnimationFrame(() => focusAndSetCaret(caret));
  };

  const selectedText = () => {
    const el = textareaRef.current;
    if (!el) {
      return '';
    }
    return value.slice(el.selectionStart, el.selectionEnd);
  };

  const handleInput = (event) => {
    onChange(event.target.value);
    adjustTextareaHeight(event.target);
  };

  const handlePaste = (event) => {
    const clipboard = event.clipboardData?.getData('text');
    if (clipboard == null) {
      return;
    }
    const normalized = normalizeDraftUrlPaste(clipboard);
    if (normalized === clipboard) {
      return;
    }
    event.preventDefault();
    applyInsert(normalized);
  };

  const handleKeyDown = (event) => {
    const withMod = isMacPlatform() ? event.metaKey : event.ctrlKey;
    if (withMod && event.key.toLowerCase() === 'a') {
      event.preventDefault();
      textareaRef.current?.select();
    }
  };

  const handleContextMenu = (event) => {
    event.preventDefault();
    const el = textareaRef.current;
    if (el && document.activeElement !== el) {
      el.focus();
    }
    setMenu({
      x: event.clientX,
      y: event.clientY,
      hasSelection: Boolean(selectedText()),
      hasValue: Boolean(value),
    });
  };

  const handleCut = async () => {
    const text = selectedText();
    if (!text) {
      return;
    }
    await electronService.clipboardWriteText(text);
    applyInsert('');
  };

  const handleCopy = async () => {
    const text = selectedText();
    if (!text) {
      return;
    }
    await electronService.clipboardWriteText(text);
  };

  const handleMenuPaste = async () => {
    try {
      const clip = await electronService.clipboardReadText();
      applyInsert(normalizeDraftUrlPaste(clip));
    } catch (error) {
      console.error('Paste failed:', error);
    }
  };

  const handleDelete = () => {
    if (!selectedText()) {
      return;
    }
    applyInsert('');
  };

  const handleSelectAll = () => {
    textareaRef.current?.select();
  };

  useEffect(() => {
    adjustTextareaHeight(textareaRef.current);
  }, [value, adjustTextareaHeight]);

  return (
    <section className="module">
      <div className="textarea-container">
        <textarea
          ref={textareaRef}
          className="auto-resize-textarea"
          placeholder={`请输入草稿地址，每行一个。支持右键菜单与 ${mod}+C / ${mod}+V。
例如：
https://example.com/get_draft?draft_id=草稿1
https://example.com/get_draft?draft_id=草稿2`}
          value={value}
          onChange={handleInput}
          onPaste={handlePaste}
          onKeyDown={handleKeyDown}
          onContextMenu={handleContextMenu}
          style={{ height: textareaHeight }}
          spellCheck={false}
          autoComplete="off"
          autoCorrect="off"
          autoCapitalize="off"
          wrap="soft"
          inputMode="url"
        />
        <p className="textarea-hint">
          每行一个地址。右键可复制、粘贴、删除、全选
          {isMacPlatform() ? '；macOS 使用 ⌘，Ctrl+点击也可打开菜单' : '；Windows 使用 Ctrl'}。
        </p>
      </div>
      {menu ? (
        <TextEditContextMenu
          x={menu.x}
          y={menu.y}
          canCut={menu.hasSelection}
          canCopy={menu.hasSelection}
          canPaste
          canDelete={menu.hasSelection}
          canSelectAll={menu.hasValue}
          onCut={handleCut}
          onCopy={handleCopy}
          onPaste={handleMenuPaste}
          onDelete={handleDelete}
          onSelectAll={handleSelectAll}
          onClose={closeMenu}
        />
      ) : null}
    </section>
  );
}

export default Textarea;
