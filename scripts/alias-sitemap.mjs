#!/usr/bin/env node
// Post-build: alias Astro's @astrojs/sitemap output as /sitemap.xml.
// See skill: astro-sitemap-alias

import { readFile, writeFile, readdir } from 'node:fs/promises';
import { join } from 'node:path';

const DIST = new URL('../dist/', import.meta.url).pathname;

async function main() {
  const files = await readdir(DIST);
  const chunks = files.filter(f => /^sitemap-\d+\.xml$/.test(f)).sort();
  if (chunks.length === 0) {
    console.error('[alias-sitemap] No sitemap-N.xml chunks found, skipping');
    process.exit(0);
  }

  const allLocs = [];
  for (const f of chunks) {
    const xml = await readFile(join(DIST, f), 'utf8');
    const urlBlocks = xml.match(/<url>[\s\S]*?<\/url>/g) || [];
    for (const block of urlBlocks) {
      const locMatch = block.match(/<loc>([^<]+)<\/loc>/);
      const lastmodMatch = block.match(/<lastmod>([^<]+)<\/lastmod>/);
      if (locMatch) {
        const lastmod = lastmodMatch ? `<lastmod>${lastmodMatch[1]}</lastmod>` : '';
        allLocs.push(`<url><loc>${locMatch[1]}</loc>${lastmod}</url>`);
      }
    }
  }

  const out = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allLocs.join('\n')}
</urlset>\n`;

  await writeFile(join(DIST, 'sitemap.xml'), out, 'utf8');
  console.log(`[alias-sitemap] Wrote dist/sitemap.xml with ${allLocs.length} URLs (from ${chunks.length} chunks)`);
}

main().catch(err => { console.error('[alias-sitemap] Failed:', err); process.exit(1); });
