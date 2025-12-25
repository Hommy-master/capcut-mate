function DownloadControls({ isOpen, onToggle, isLoading }) {
  return (
    <section className="module flex justify-between">
      <div className="switch-container">
        <label className="switch">
          <input 
            type="checkbox"
            checked={isOpen} 
            disabled={isLoading}
            onChange={(e) => onToggle(e.target.checked)}
          />
          <span className="slider"></span>
        </label>
        <span>下载后打开草稿路径文件</span>
      </div>
    </section>
  );
}

export default DownloadControls;
