// scripts/lib/html.js
// Minimal HTML → text + table extraction. No cheerio dep.
// Good enough to feed an LLM extractor.

function stripHtml(html) {
  return html
    // remove script/style
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<noscript[\s\S]*?<\/noscript>/gi, ' ')
    // normalize tags that introduce line breaks
    .replace(/<\/(p|div|li|tr|h[1-6]|br|section|article)>/gi, '\n')
    .replace(/<br\s*\/?>/gi, '\n')
    // strip remaining tags
    .replace(/<[^>]+>/g, ' ')
    // decode common entities
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    // collapse whitespace
    .replace(/[ \t]+/g, ' ')
    .replace(/\n\s*\n+/g, '\n\n')
    .trim();
}

function extractTables(html) {
  // Returns array of { headers: [..], rows: [[..]] }
  const tables = [];
  const tableRe = /<table[\s\S]*?<\/table>/gi;
  let m;
  while ((m = tableRe.exec(html))) {
    const t = m[0];
    const headers = [];
    const thRe = /<th[\s\S]*?>([\s\S]*?)<\/th>/gi;
    let th;
    while ((th = thRe.exec(t))) {
      headers.push(stripHtml(th[1]).trim());
    }
    const rows = [];
    const trRe = /<tr[\s\S]*?<\/tr>/gi;
    let tr;
    while ((tr = trRe.exec(t))) {
      const cells = [];
      const tdRe = /<t[dh][\s\S]*?>([\s\S]*?)<\/t[dh]>/gi;
      let td;
      while ((td = tdRe.exec(tr[0]))) {
        cells.push(stripHtml(td[1]).trim());
      }
      if (cells.length) rows.push(cells);
    }
    tables.push({ headers, rows });
  }
  return tables;
}

function tablesToText(tables) {
  return tables
    .map((t, i) => {
      const head = t.headers.length ? `Headers: ${t.headers.join(' | ')}` : '';
      const body = t.rows.map(r => r.join(' | ')).join('\n');
      return `[Table ${i + 1}]\n${head}\n${body}`;
    })
    .join('\n\n');
}

module.exports = { stripHtml, extractTables, tablesToText };