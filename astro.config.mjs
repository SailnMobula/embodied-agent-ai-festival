import { defineConfig } from 'astro/config'
import react from '@astrojs/react'
import mdx from '@astrojs/mdx'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  site: 'https://sailnmobula.github.io',
  base: '/embodied-agent-ai-festival',
  integrations: [react(), mdx()],
  markdown: {
    shikiConfig: { theme: 'catppuccin-latte' },
  },
  vite: { plugins: [tailwindcss()] },
})
