import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath } from 'node:url'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: [
      {find: '@', replacement: fileURLToPath(new URL('./src', import.meta.url))},
      {find: '@assets', replacement: fileURLToPath(new URL('./src/assets', import.meta.url))},
      {find: '@fonts', replacement: fileURLToPath(new URL('./src/assets/fonts', import.meta.url))},
      {find: '@icons', replacement: fileURLToPath(new URL('./src/icons', import.meta.url))},
      {find: '@components', replacement: fileURLToPath(new URL('./src/components', import.meta.url))},
      {find: '@pages', replacement: fileURLToPath(new URL('./src/pages', import.meta.url))},
      {find: '@store', replacement: fileURLToPath(new URL('./src/store', import.meta.url))},
      {find: '@services', replacement: fileURLToPath(new URL('./src/services', import.meta.url))},
    ]
  }
})