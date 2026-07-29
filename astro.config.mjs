import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://apirank.vip',
  integrations: [
    sitemap({
      i18n: {
        defaultLocale: 'en',
        locales: {
          en: 'en-US',
          zh: 'zh-CN',
        },
      },
    }),
  ],
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'zh'],
    routing: {
      prefixDefaultLocale: false,
    },
  },
  redirects: {
    // Consolidate /blog/ into /tutorials/ (2026-07-01) — avoids duplicate-content SEO signal.
    // Source pages src/pages/blog.astro + src/pages/zh/blog.astro must be deleted
    // so Astro build doesn't also emit real HTML for these paths.
    '/blog': '/tutorials',
    '/blog/': '/tutorials/',
    '/zh/blog': '/zh/tutorials',
    '/zh/blog/': '/zh/tutorials/',
  },
  build: {
    // Constrain build parallelism. The default is os.cpus().length, but on the
    // 1.9 GB / 2-CPU VPS used for cron builds, 2 concurrent esbuild workers
    // OOM-kill during "Building static entrypoints..." when compiling 270+
    // .astro pages. Set to 1 to serialize and stay within memory budget.
    // See references/apirank/apirank-cron-daily-article-2026-07-27-gpt-5-6-sol-huggingface-attack.md
    // (lesson: "Build runs with NODE_OPTIONS=--max-old-space-size=350 only
    // complete because esbuild workers serialize through one CPU; doubling
    // parallelism would crash on the same VM.")
    concurrency: 1,
  },
});