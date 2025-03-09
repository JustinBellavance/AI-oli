import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
  base: '/www.aioli.tech/', // Update this to match your bucket path
  css: {
    preprocessorOptions: {
      css: {
        additionalData: `@import "./src/App.css";`,
      },
    },
  },
});