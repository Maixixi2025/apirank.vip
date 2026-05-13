import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://apirank.vip',
  integrations: [
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
    defaultLocale: 'en',
    locales: ['en', 'zh'],
    routing: {
      prefixDefaultLocale: true,
    },
  },
});
