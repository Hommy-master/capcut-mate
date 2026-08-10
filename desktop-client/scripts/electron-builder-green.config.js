module.exports = {
  appId: "com.gogoshine.capcutmate",
  productName: "CapCut-Mate",
  directories: {
    output: "dist"
  },
  win: {
    icon: "assets/icons/logo.ico",
    artifactName: "capcut-mate-windows-x64-green.zip",
  },
  mac: {
    icon: "assets/icons/logo.icns",
    artifactName: "capcut-mate-macos-\${arch}-green.zip",
    hardenedRuntime: true,
    gatekeeperAssess: false,
    entitlements: "assets/entitlements.mac.plist",
    entitlementsInherit: "assets/entitlements.mac.plist"
  },
  files: [
    "!node_modules/**/*",
    "!web/node_modules/**/*",
    "!web/src/**/*",
    "!web/public/**/*",
    "!scripts/**/*",
    "!*.yml",
    "!*.yaml",
    "!*.lock",
    "!README.md",
    "!Dockerfile",
    "!docker-compose.yaml",
    "node_modules/**/*",
    "ui/**/*",
    "nodeapi/**/*",
    "*.js",
    "*.json",
    "assets/**/*"
  ],
  extraResources: [
    {
      from: "assets/",
      to: "assets/"
    }
  ]
};