import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://apirank.vip',
  integrations: [
    tailwind(),
    sitemap({
      i18n: {
        defaultLocale: 'zh',
        locales: {
          en: 'en-US',
          zh: 'zh-CN',
        },
      },
    }),
  ],
  i18n: {
    defaultLocale: 'zh',
    locales: ['zh', 'en'],
    routing: {
      prefixDefaultLocale: false,
    },
  },
  redirects: {
    '/en': '/',
  },
});
