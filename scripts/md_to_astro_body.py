#!/usr/bin/env python3
"""Convert markdown draft to Astro-ready HTML body string for apirank.vip.
Pattern: matches the lepton-ai.astro / runway-api-review.astro inline HTML body.
"""
import re
import sys
import html as html_module


def md_to_astro_body(md_text: str) -> str:
    """Convert markdown to HTML body string suitable for `set:html={...}` in Astro."""
    out = []

    lines = md_text.split('\n')
    i = 0
    n = len(lines)
    in_code_block = False
    code_buffer = []
    code_lang = ''
    list_type = None  # 'ul' or 'ol' or None
    in_table = False
    table_buffer = []
    para_buffer = []

    def flush_para():
        nonlocal para_buffer
        if not para_buffer:
            return
        text = ' '.join(para_buffer).strip()
        if text:
            out.append(f'<p class="text-gray-700 leading-relaxed my-4">{inline_md(text)}</p>')
        para_buffer = []

    def flush_list():
        nonlocal list_type
        if list_type:
            out.append(f'</{list_type}>')
            list_type = None

    def flush_table():
        nonlocal in_table, table_buffer
        if not in_table:
            return
        # parse table: header, separator, rows
        rows = [r for r in table_buffer if r.strip()]
        if len(rows) >= 2:
            headers = [c.strip() for c in rows[0].strip('|').split('|')]
            data_rows = []
            for r in rows[2:]:
                cells = [c.strip() for c in r.strip('|').split('|')]
                data_rows.append(cells)
            out.append('<div class="overflow-x-auto my-6"><table class="min-w-full divide-y divide-gray-200 border border-gray-200 rounded-lg">')
            out.append('<thead class="bg-gray-50"><tr>')
            for h in headers:
                out.append(f'<th class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">{inline_md(h)}</th>')
            out.append('</tr></thead>')
            out.append('<tbody class="divide-y divide-gray-200 bg-white">')
            for dr in data_rows:
                out.append('<tr>')
                for c in dr:
                    out.append(f'<td class="px-4 py-3 text-sm text-gray-700">{inline_md(c)}</td>')
                out.append('</tr>')
            out.append('</tbody></table></div>')
        in_table = False
        table_buffer = []

    def inline_md(text: str) -> str:
        """Apply inline markdown: bold, italic, code, links."""
        # Escape HTML chars in text first? Astro renders via set:html so this is plain HTML output
        # We trust the input — bold/italic/emphasis patterns
        # bold **text**
        text = re.sub(r'\*\*([^*\n]+?)\*\*', r'<strong>\1</strong>', text)
        # italic *text* (avoid matching **)
        text = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', text)
        # inline code `text`
        text = re.sub(r'`([^`\n]+?)`', r'<code>\1</code>', text)
        # links [text](url) — external links get rel="sponsored noopener" + target="_blank"
        def _link_sub(m):
            label, url = m.group(1), m.group(2)
            if re.match(r'^https?://', url):
                host_m = re.search(r'^https?://([^/]+)', url)
                host = host_m.group(1) if host_m else ''
                # Internal + personal-about links: no rel/target
                if host in ('apirank.vip', 'www.apirank.vip', 'about.me', 'www.about.me'):
                    return f'<a href="{url}" class="text-blue-600 hover:underline">{label}</a>'
                # External links: sponsored disclosure
                return (
                    f'<a href="{url}" class="text-blue-600 hover:underline" '
                    f'rel="sponsored noopener" target="_blank">{label}</a>'
                )
            # Relative/internal link (no scheme)
            return f'<a href="{url}" class="text-blue-600 hover:underline">{label}</a>'
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', _link_sub, text)
        # inline HTML links <a href="URL" ...>text</a> — patch external href to add rel="sponsored noopener" target="_blank"
        def _html_link_sub(m):
            open_tag = m.group(1)
            label = m.group(2)
            close_tag = m.group(3)
            href_m = re.search(r'href="([^"]+)"', open_tag)
            if not href_m:
                return m.group(0)
            url = href_m.group(1)
            if not re.match(r'^https?://', url):
                return m.group(0)
            host_m = re.search(r'^https?://([^/]+)', url)
            host = host_m.group(1) if host_m else ''
            if host in ('apirank.vip', 'www.apirank.vip', 'about.me', 'www.about.me'):
                return m.group(0)
            # Check if rel already has "sponsored" or "noopener" — avoid double-adding
            if re.search(r'rel="[^"]*sponsored', open_tag) and re.search(r'rel="[^"]*noopener', open_tag) and 'target="_blank"' in open_tag:
                return m.group(0)
            # Build new attrs
            new_tag = open_tag
            if re.search(r'rel="', new_tag):
                # Replace existing rel with our full set
                new_tag = re.sub(r'rel="[^"]*"', 'rel="sponsored noopener"', new_tag)
            else:
                new_tag = new_tag.rstrip('>') + ' rel="sponsored noopener">'
            if 'target="_blank"' not in new_tag:
                new_tag = new_tag.rstrip('>') + ' target="_blank">'
            return f'{new_tag}{label}{close_tag}'
        text = re.sub(r'(<a\s+[^>]*>)([^<]*)(</a>)', _html_link_sub, text)
        # Bare URLs (not already in markdown link or <a> tag) — wrap as proper affiliate link
        # Only target the specific invite URL pattern; the base api.freemodel.dev URL is NOT affiliate
        # Negative lookbehind: not preceded by "](" (markdown link) or href=" (HTML link) or ">" (attribute)
        def _bare_url_sub(m):
            url = m.group(0)
            return f'<a href="{url}" rel="sponsored noopener" target="_blank">{url}</a>'
        # Only target the actual invite link — not other freemodel URLs
        invite_pat = r'(?<!\])(?<!href=")(?<!href=\')(?<!>)https://freemodel\.dev/invite/FRE-7a3b6220(?![\w])'
        text = re.sub(invite_pat, _bare_url_sub, text)
        return text

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Code block toggle
        if stripped.startswith('```'):
            if not in_code_block:
                # Flush pending blocks
                flush_para()
                flush_list()
                flush_table()
                in_code_block = True
                code_lang = stripped[3:].strip()
                code_buffer = []
            else:
                # End code block
                code_text = '\n'.join(code_buffer)
                # HTML-escape { } for Astro JSX safety
                code_text_escaped = code_text.replace('{', '&#123;').replace('}', '&#125;')
                lang_class = f' class="language-{code_lang}"' if code_lang else ''
                out.append(f'<pre><code{lang_class}>{code_text_escaped}</code></pre>')
                in_code_block = False
            i += 1
            continue

        if in_code_block:
            code_buffer.append(line)
            i += 1
            continue

        # Table handling
        if stripped.startswith('|') and '|' in stripped[1:]:
            if not in_table:
                flush_para()
                flush_list()
                in_table = True
                table_buffer = []
            table_buffer.append(stripped)
            i += 1
            continue
        else:
            if in_table:
                flush_table()

        # Headings
        m = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if m:
            flush_para()
            flush_list()
            level = len(m.group(1))
            text = m.group(2).strip()
            cls = {
                1: 'text-3xl font-bold text-gray-900 mt-8 mb-4',
                2: 'text-2xl font-bold text-gray-900 mt-8 mb-4',
                3: 'text-xl font-bold text-gray-900 mt-6 mb-3',
                4: 'text-lg font-bold text-gray-900 mt-4 mb-2',
            }.get(level, 'text-base font-bold text-gray-900 mt-2 mb-1')
            out.append(f'<h{level} class="{cls}">{inline_md(text)}</h{level}>')
            i += 1
            continue

        # Horizontal rule
        if stripped == '---':
            flush_para()
            flush_list()
            out.append('<hr class="my-8 border-gray-200" />')
            i += 1
            continue

        # Unordered list
        if re.match(r'^[-*]\s+', stripped):
            flush_para()
            if list_type != 'ul':
                flush_list()
                out.append('<ul class="list-disc list-inside text-gray-700 my-4 space-y-1">')
                list_type = 'ul'
            item = re.sub(r'^[-*]\s+', '', stripped)
            out.append(f'<li>{inline_md(item)}</li>')
            i += 1
            continue

        # Ordered list
        if re.match(r'^\d+\.\s+', stripped):
            flush_para()
            if list_type != 'ol':
                flush_list()
                out.append('<ol class="list-decimal list-inside text-gray-700 my-4 space-y-1">')
                list_type = 'ol'
            item = re.sub(r'^\d+\.\s+', '', stripped)
            out.append(f'<li>{inline_md(item)}</li>')
            i += 1
            continue

        # Empty line = paragraph break
        if not stripped:
            flush_para()
            flush_list()
            i += 1
            continue

        # Regular paragraph
        para_buffer.append(stripped)
        i += 1

    flush_para()
    flush_list()
    flush_table()
    if in_code_block:
        # unclosed
        code_text = '\n'.join(code_buffer)
        code_text_escaped = code_text.replace('{', '&#123;').replace('}', '&#125;')
        out.append(f'<pre><code>{code_text_escaped}</code></pre>')

    return '\n\n'.join(out)


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        md = f.read()
    # strip frontmatter
    md = re.sub(r'^---\s*\n.*?\n---\s*\n', '', md, count=1, flags=re.DOTALL)
    result = md_to_astro_body(md)
    print(result)
