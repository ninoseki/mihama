import vue from '@vitejs/plugin-vue'
import { URL, fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'
import VueDevTools from 'vite-plugin-vue-devtools'

const env = process.env
const target = env.BACKEND_URL || 'http://localhost:8000/'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), VueDevTools()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      '/v1': target
    }
  }
})
