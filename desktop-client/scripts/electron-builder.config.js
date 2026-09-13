/**
 * Electron Builder Configuration
 */
module.exports = {
  appId: "com.gogoshine.capcutmate",
  productName: "剪映小助手",
  directories: {
    output: "dist"
  },
  afterPack: require("./afterPackWinIcon"),
  afterSign: require("./notarize"),
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
    // electron-builder 26：仅跳过代码签名，仍写入 exe 图标/元数据
    // （signAndEditExecutable:false 会连图标一起跳过）
    signExecutable: false
  },
  nsis: {
    oneClick: false,
    allowToChangeInstallationDirectory: true,
    installerIcon: "assets/icons/logo.ico",
    uninstallerIcon: "assets/icons/logo.ico",
    shortcutName: "剪映小助手",
  },
  mac: {
    icon: "assets/icons/logo.icns",
    // 架构由 CLI --arm64 / --x64 决定，避免单个 job 打双架构导致超时
    target: ["dmg"],
    artifactName: "capcut-mate-macos-${arch}-installer.dmg",
    category: "public.app-category.productivity",
    hardenedRuntime: true,
    gatekeeperAssess: false,
    entitlements: "assets/entitlements.mac.plist",
    entitlementsInherit: "assets/entitlements.mac.plist",
    // 公证改由 afterSign（scripts/notarize.js）处理，便于重试
    notarize: false
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