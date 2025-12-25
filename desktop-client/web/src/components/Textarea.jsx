import React, { useState, useEffect } from 'react';

function Textarea({ value, onChange }) {
  const [textareaHeight, setTextareaHeight] = useState('auto');

  const handleInput = (e) => {
    onChange(e.target.value);
    adjustTextareaHeight(e.target);
  };

  const adjustTextareaHeight = (textarea) => {
    textarea.style.height = 'auto';
    const newHeight = Math.min(textarea.scrollHeight, 300); // 设置最大高度
    setTextareaHeight(`${newHeight}px`);
  };

  useEffect(() => {
    const textarea = document.querySelector('.auto-resize-textarea');
    if (textarea) {
      adjustTextareaHeight(textarea);
    }
  }, [value]);

  return (
    <section className="module">
      <div className="textarea-container">
        <textarea
          className="auto-resize-textarea"
          placeholder={`请输入草稿地址，多个使用回车换行分隔例如：
草稿地址1 
草稿地址2 
草稿地址3`}
          value={value}
          onChange={handleInput}
          style={{ height: textareaHeight }}
        ></textarea>
      </div>
    </section>
  );
}

export default Textarea;
