// logger.js
const log4js = require('log4js');
const path = require('path');
const { app } = require('electron');

log4js.configure({
    appenders: {
        // 定义一个按日期分割的日志文件追加器
        dateFile: {
            type: 'dateFile',
            filename: path.join(app.getPath('userData'), 'logs', 'app.log'), // 日志文件路径
            pattern: 'yyyy-MM-dd', // 按天分割
            compress: false, // 是否压缩备份文件
            keepFileExt: true, // 保持.log扩展名
            numBackups: 7 // 保留最近7天的备份
        },
        // 同时输出到控制台
        console: { type: 'console' }
    },
    categories: {
        default: {
            appenders: ['dateFile', 'console'],
            level: 'info' // 默认日志级别
        }
    }
});

const logger = log4js.getLogger();
module.exports = logger;