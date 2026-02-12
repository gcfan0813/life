import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      '@shared': resolve(__dirname, './shared'),
      '@core': resolve(__dirname, './core'),
    },
  },
  server: {
    port: 3000,
    host: true,
  },
  build: {
    target: 'es2020',
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ai: ['@core/ai', '@shared/ai'],
          rules: ['@core/engine', '@shared/rules'],
        },
      },
    },
  },
  optimizeDeps: {
    include: ['react', 'react-dom', '@core/ai', '@shared/ai'],
  },
})