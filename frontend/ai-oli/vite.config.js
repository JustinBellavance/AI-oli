import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
  base: 'https://storage.googleapis.com/ai-oli/', // Set this to '/' or your GCS bucket path
  css: {
    preprocessorOptions: {
      css: {
        additionalData: `@import "./src/App.css";`,
      },
    },
  },
});