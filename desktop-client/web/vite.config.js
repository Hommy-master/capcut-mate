import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import electron from 'vite-plugin-electron'

// https://vitejs.dev/config/
export default defineConfig({
  base: './',
  plugins: [
    react(),
    // Electron插件仅在生产构建时启用
    // ...(process.env.NODE_ENV === 'production' ? [electron({
    //   entry: 'electron/main.js',
    // })] : [])
  ],
  resolve: {
    alias: {
      '@': '/src'
    }
  },
  server: {
    port: 9000,
    open: true
  },
  build: {
    outDir: '../ui',
    emptyOutDir: true
  }
})
