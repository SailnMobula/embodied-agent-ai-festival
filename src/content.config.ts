import { defineCollection, z } from 'astro:content'
import { glob } from 'astro/loaders'

const stations = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/stations' }),
  schema: z.object({
    order: z.number().int().positive(),
    title: z.string(),
    tagline: z.string(),
    durationMinutes: z.number().int().positive(),
    takeaway: z.string(),
  }),
})

export const collections = { stations }
