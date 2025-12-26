import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 80,
    allowedHosts: ['nsai.morningmonkey.net'],
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      '/__/auth': {
        target: 'https://ns-ai-project.firebaseapp.com',
        changeOrigin: true,
      },
    }
  },
})
