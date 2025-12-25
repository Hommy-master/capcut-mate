/**
 * 更新 package.json 中的 version 字段为 GitHub tag 版本号
 */
const fs = require('fs');
const path = require('path');

// 获取 GitHub tag 版本号
const githubRef = process.env.GITHUB_REF;
console.log(`GITHUB_REF: ${githubRef}`);

if (!githubRef || !githubRef.startsWith('refs/tags/')) {
  console.log('不是 tag 触发的构建，跳过版本更新');
  process.exit(0);
}

// 提取 tag 名称（去除 refs/tags/ 前缀）
const tagName = githubRef.replace('refs/tags/', '');
console.log(`Tag 名称: ${tagName}`);

// 检查 tag 是否符合语义化版本规范 (v1.2.3 或 1.2.3)
const versionMatch = tagName.match(/v?(\d+\.\d+\.\d+)/);
if (!versionMatch) {
  console.error(`Tag 名称 "${tagName}" 不符合语义化版本规范 (例: v1.2.3 或 1.2.3)`);
  process.exit(1);
}

const version = versionMatch[1];
console.log(`提取的版本号: ${version}`);

// 读取 package.json 文件
const packageJsonPath = path.join(__dirname, '..', 'package.json');
const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));

// 更新版本号
const oldVersion = packageJson.version;
packageJson.version = version;

// 写回 package.json 文件
fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2) + '\n');

console.log(`成功更新版本号: ${oldVersion} -> ${version}`);