import { defineConfig } from 'astro/config'
import react from '@astrojs/react'
import mdx from '@astrojs/mdx'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  site: 'https://exxeta.github.io',
  base: '/embodied-agent-ai-festival',
  integrations: [react(), mdx()],
  vite: { plugins: [tailwindcss()] },
})
