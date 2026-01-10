module.exports = {
  appId: "com.gogoshine.capcutmate",
  productName: "CapCut-Mate",
  directories: {
    output: "dist"
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
    "web/dist/**/*",
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