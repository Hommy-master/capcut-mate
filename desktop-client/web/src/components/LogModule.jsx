import { formatToTime } from '../utils/date';
import { useEffect, useRef } from 'react';

function LogModule({ logs, onClear }) {
  const logIconMap = {
      error: "fas fa-times-circle",
      loading: "fas fa-spinner fa-spin",
      success: "fas fa-check-circle",
      all: "fas fa-check-circle",
  };
  const logListRef = useRef(null);
  // 当日志列表变化时，自动滚动到底部
  useEffect(() => {
    if (logListRef.current) {
      logListRef.current.scrollTop = logListRef.current.scrollHeight;
    }
  }, [logs]);
  
  return (
    <section className="module log-module">
      <h2 className="module-title">
        <span><i className="fas fa-list-alt"></i> 下载日志</span>
        <button className="btn btn-clear" onClick={onClear}>
          <i className="fas fa-trash"></i> 清空日志
        </button>
      </h2>
      {logs.length === 0 ? (
        <div className="log-empty">暂无日志记录</div>
      ) : (
        <ul className="log-list" ref={logListRef}>
          {logs.map((log, index) => (
            <li key={log.id || `${log.time}-${index}`} className={`log-item ${log.level}`}>
              <span className="log-time">[{formatToTime(log.time)}]</span>
              <i className={`log-icon show ${logIconMap[log.level] || 'hide'}`}></i>
              <span className={`log-message`}>
                {log.message}
              </span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default LogModule;
