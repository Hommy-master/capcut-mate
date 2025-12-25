/**
 * Electron Builder Configuration
 */
module.exports = {
  appId: "com.gogoshine.capcut-mate",
  productName: "剪映小助手",
  directories: {
    output: "dist"
  },
  files: [
    "**/*",
    // "!node_modules",
    "!web",
    "!dist",
    "!electron-builder.config.js",
    "!.gitignore",
    "!.github",
    "!README.md",
    "!.vscode",
    "!DS_Store",
  ],
  win: {
    icon: "assets/icons/logo.ico",
    target: "nsis",
    artifactName: "capcut-mate-windows-x64-installer.exe",
    // 禁用代码签名
    signingHashAlgorithms: []
  },
  nsis: {
    oneClick: false,
    allowToChangeInstallationDirectory: true,
  },
  mac: {
    icon: "assets/icons/logo.icns",
    target: "dmg",
    artifactName: "capcut-mate-macos-arm64-installer.dmg",
    category: "public.app-category.productivity"
  },
  dmg: {
    background: null,
    window: {
      width: 540,
      height: 380
    },
    contents: [
      {
        x: 130,
        y: 150,
        type: "file"
      },
      {
        x: 410,
        y: 150,
        type: "link",
        path: "/Applications"
      }
    ]
  }
};