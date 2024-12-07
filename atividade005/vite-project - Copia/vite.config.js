import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  base: '/Our-game/',
  plugins: [react()],
  base: "/vite-react-deploy/",
})
