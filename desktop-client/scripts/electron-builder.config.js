/**
 * Electron Builder Configuration
 */
function macNotarize() {
  const teamId = process.env.APPLE_TEAM_ID;
  // 本地无 Team ID 时跳过公证；CI 注入 APPLE_TEAM_ID + Apple ID 凭据后启用
  if (!teamId) return false;
  return { teamId };
}

module.exports = {
  appId: "com.gogoshine.capcutmate",
  productName: "剪映小助手",
  directories: {
    output: "dist"
  },
  afterPack: require("./afterPackWinIcon"),
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
    // 跳过 winCodeSign（本机解压会因符号链接权限失败）；exe 图标由 afterPack 写入
    signingHashAlgorithms: [],
    signAndEditExecutable: false,
    signDlls: false
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
    target: [
      {
        target: "dmg",
        arch: "arm64"
      },
      {
        target: "dmg",
        arch: "x64"
      }
    ],
    artifactName: "capcut-mate-macos-${arch}-installer.dmg",
    category: "public.app-category.productivity",
    hardenedRuntime: true,
    gatekeeperAssess: false,
    entitlements: "assets/entitlements.mac.plist",
    entitlementsInherit: "assets/entitlements.mac.plist",
    notarize: macNotarize()
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