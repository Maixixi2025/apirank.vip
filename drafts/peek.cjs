const s = require('./state.json');
for (const d of s.drafts || []) {
  const price = d.price ? '[$' + (d.price.monthly || '?') + '/mo]' : '';
  const prov = d.provider && d.provider.name ? '[' + d.provider.name + ']' : '';
  console.log(
    (d.status || '').padEnd(16),
    '|', (d.site || '').padEnd(8),
    '|', (d.lang || '').padEnd(3),
    '|', d.slug || '',
    price, prov,
    '|', d.updatedAt || ''
  );
}
