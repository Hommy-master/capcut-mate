const TERMINAL_LEVELS = new Set(["success", "error", "all"]);

function mergeLogEntry(existing, incoming) {
  if (TERMINAL_LEVELS.has(existing.level) && incoming.level === "loading") {
    return existing;
  }
  return {
    ...existing,
    ...incoming,
    time: incoming.time ?? existing.time,
  };
}

/**
 * 按顺序合并单条 IPC 日志，避免 update 先于 append 到达时残留「下载中」。
 */
export function applyLogEntry(prevLogs, logEntry) {
  const { action, ...entry } = logEntry;

  if (entry.id) {
    const index = prevLogs.findIndex((log) => log.id === entry.id);
    if (index >= 0) {
      const next = [...prevLogs];
      next[index] = mergeLogEntry(next[index], entry);
      return next;
    }
  }

  if (action === "update" && entry.id) {
    return [...prevLogs, entry];
  }

  return [...prevLogs, entry];
}

export function applyLogBatch(prevLogs, batch) {
  return batch.reduce((acc, entry) => applyLogEntry(acc, entry), prevLogs);
}
