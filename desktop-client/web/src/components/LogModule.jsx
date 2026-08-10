import { formatToTime } from '../utils/date';
import { partitionLogsForDisplay } from '../utils/downloadLog';
import { useEffect, useRef } from 'react';

function LogItem({ log, index, logIconMap }) {
  return (
    <li className={`log-item ${log.level}`}>
      <span className="log-time">[{formatToTime(log.time)}]</span>
      <i className={`log-icon show ${logIconMap[log.level] || 'hide'}`}></i>
      <span className="log-message">{log.message}</span>
    </li>
  );
}

function LogModule({ logs, onClear }) {
  const logIconMap = {
      error: "fas fa-times-circle",
      loading: "fas fa-spinner fa-spin",
      success: "fas fa-check-circle",
      all: "fas fa-check-circle",
  };
  const logListRef = useRef(null);
  const { settled, active } = partitionLogsForDisplay(logs);

  // 当日志列表变化时，自动滚动到底部，便于查看正在下载的配置/资源
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
          {settled.map((log, index) => (
            <LogItem key={log.id || `${log.time}-${index}`} log={log} index={index} logIconMap={logIconMap} />
          ))}
          {active.length > 0 && (
            <li className="log-active-divider" aria-label="正在下载">
              <span className="log-active-divider-label">
                <i className="fas fa-spinner fa-spin"></i>
                正在下载 ({active.length})
              </span>
            </li>
          )}
          {active.map((log, index) => (
            <LogItem
              key={log.id || `${log.time}-active-${index}`}
              log={log}
              index={index}
              logIconMap={logIconMap}
            />
          ))}
        </ul>
      )}
    </section>
  );
}

export default LogModule;
