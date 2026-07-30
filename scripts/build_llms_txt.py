#!/usr/bin/env python3
"""
Build llms.txt + zh/llms.txt for APIRank following llmstxt.org spec.

Spec (https://llmstxt.org/):
- H1 project title (required, only required field)
- Optional BOM
- Optional blockquote summary (with optional short paragraph)
- Zero or more markdown sections (anything not H2)
- Zero or more H2-delimited sections, each containing "file lists"
- File list item format: `- [name](url) : notes`  (notes optional)

Inputs:
- dist/sitemap-0.xml (built by @astrojs/sitemap)
- Slug-to-description mapping derived from URL patterns

Outputs:
- dist/llms.txt (English / global file list)
- dist/zh/llms.txt (Chinese localized file list)
"""

import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

# ─── Paths ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
SITEMAP = ROOT / "dist" / "sitemap-0.xml"
OUT_EN = ROOT / "dist" / "llms.txt"
OUT_ZH = ROOT / "dist" / "zh" / "llms.txt"
OUT_EN.parent.mkdir(parents=True, exist_ok=True)

SITE = "https://apirank.vip"

# ─── XML parsing ──────────────────────────────────────────────────────────────
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def parse_sitemap(path: Path) -> list[str]:
    """Return list of all <loc> URLs from sitemap, in source order."""
    tree = ET.parse(path)
    root = tree.getroot()
    return [loc.text or "" for loc in root.findall(".//sm:url/sm:loc", NS)]


# ─── URL classification ────────────────────────────────────────────────────────
def normalize(url: str) -> tuple[str, str]:
    """Strip trailing slash + drop /zh/ prefix → (lang, path).

    >>> normalize("https://apirank.vip/zh/tutorials/foo/")
    ('zh', '/tutorials/foo')
    >>> normalize("https://apirank.vip/tutorials/foo/")
    ('en', '/tutorials/foo')
    """
    path = url.replace(SITE, "", 1)
    if path.startswith("/zh/"):
        return "zh", "/zh/" + path[4:]
    return "en", path


def categorize(path: str) -> str:
    """Map path to a bucket name. Path is /foo/bar[/...], no lang prefix here
    for EN, but for ZH it keeps /zh/ prefix. We strip /zh/ for bucketing."""
    bare = path.replace("/zh/", "/", 1)
    bare = bare.rstrip("/")
    for prefix, label in [
        ("/tutorials/", "Tutorials"),
        ("/providers/", "Providers"),
        ("/compare/", "Comparisons"),
        ("/use-case/", "Use Cases"),
    ]:
        if bare.startswith(prefix):
            return label
    if bare in ("", "/"):
        return "Core"
    if bare in ("/about", "/contact", "/privacy"):
        return "Core"
    if bare in ("/calculator",):
        return "Core"
    if bare in ("/tutorials", "/providers", "/compare", "/use-case"):
        return "Core"
    return "Other"


def is_index(path: str) -> bool:
    """Index pages (list pages, not individual content)."""
    bare = path.replace("/zh/", "/", 1).rstrip("/")
    return bare in (
        "",
        "/tutorials",
        "/providers",
        "/compare",
        "/use-case",
        "/about",
        "/contact",
        "/privacy",
        "/calculator",
    )


def humanize(path: str) -> str:
    """Turn /tutorials/foo-bar-2026 → 'Foo Bar 2026'."""
    bare = path.replace("/zh/", "/", 1).rstrip("/")
    slug = bare.rsplit("/", 1)[-1]
    if not slug or slug == "zh":
        slug = "home"
    # Replace hyphens with spaces, title-case
    return slug.replace("-", " ").title()


# ─── Section descriptions (per category, per language) ───────────────────────
DESCRIPTIONS = {
    "en": {
        "Core": "Core site pages and index listings",
        "Tutorials": "API reviews, pricing analysis, and integration tutorials",
        "Providers": "Provider profile pages with pricing, models, and availability",
        "Comparisons": "Side-by-side API provider comparisons",
        "Use Cases": "Recommendation pages for specific use cases",
        "Other": "Additional pages",
    },
    "zh": {
        "Core": "网站核心页面与索引列表",
        "Tutorials": "API 测评、价格分析与集成教程",
        "Providers": "厂商主页，含价格、模型与可用性",
        "Comparisons": "厂商横向对比",
        "Use Cases": "针对具体场景的推荐",
        "Other": "其他页面",
    },
}

SUMMARY = {
    "en": "APIRank indexes AI API token pricing, free tiers, and reviews for OpenAI, Anthropic Claude, Google Gemini, DeepSeek, Alibaba Qwen, Baidu Ernie, Tencent Hunyuan, ByteDance Doubao, Zhipu GLM, Moonshot Kimi and more — helping developers find the cheapest AI token plan. Updated weekly.",
    "zh": "APIRank 收录 OpenAI、Anthropic Claude、Google Gemini、DeepSeek、阿里云通义、百度文心、腾讯混元、字节豆包、智谱 GLM、月之暗面 Kimi 等主流 AI 厂商的 API 价格、免费额度与深度测评，帮助开发者找到最划算的 AI Token 方案。每周更新。",
}


# ─── Build per-language content ───────────────────────────────────────────────
def build(lang: str, all_urls: list[str]) -> str:
    # Filter URLs for this language
    if lang == "en":
        # English or language-neutral (i.e., /about/, /contact/, etc.)
        urls = [u for u in all_urls if not u.replace(SITE, "", 1).startswith("/zh/")]
    else:
        # Chinese only
        urls = [u for u in all_urls if u.replace(SITE, "", 1).startswith("/zh/")]

    # Group by category
    buckets: dict[str, list[tuple[str, str]]] = {}
    for url in urls:
        _, path = normalize(url)
        cat = categorize(path)
        buckets.setdefault(cat, []).append((path, url))

    # Sort each bucket: index pages first, then alphabetical
    def sort_key(item: tuple[str, str]) -> tuple[int, str]:
        path, _ = item
        return (1 if is_index(path) else 0, path)

    for cat in buckets:
        buckets[cat].sort(key=sort_key)

    # Order of sections: Core first, then content categories
    section_order = ["Core", "Tutorials", "Providers", "Comparisons", "Use Cases", "Other"]
    present_sections = [s for s in section_order if buckets.get(s)]

    lines: list[str] = []
    # H1 (required)
    title = "API Rank" if lang == "en" else "APIRank - AI API 价格对比与深度测评"
    lines.append(f"# {title}")
    lines.append("")

    # URL line (common convention; llmstxt spec allows extra prose here)
    lines.append(f"<{SITE}>")
    lines.append("")

    # Blockquote summary (recommended)
    lines.append(f"> {SUMMARY[lang]}")
    lines.append("")

    # Optional intro paragraph (not an H2, so it's a detail section)
    if lang == "en":
        lines.append(
            "APIRank is a navigation site focused on AI API token pricing. "
            "It catalogs OpenAI, Anthropic Claude, Google Gemini, DeepSeek, "
            "Alibaba Qwen, Baidu Ernie, Tencent Hunyuan, ByteDance Doubao, "
            "Zhipu GLM, Moonshot Kimi and 40+ other providers with real-time "
            "token pricing (input/output/cached), free tiers, model comparisons, "
            "and beginner tutorials. Pricing data is updated weekly from official "
            "provider documentation."
        )
    else:
        lines.append(
            "APIRank 是一个专注于 AI API Token 价格对比的导航网站。"
            "收录 OpenAI、Anthropic Claude、Google Gemini、DeepSeek、阿里云通义、"
            "百度文心、腾讯混元、字节豆包、智谱 GLM、月之暗面 Kimi 等 40+ 主流厂商的"
            "API 价格、免费额度、模型对比与新手教程。价格数据每周从官方文档更新。"
        )
    lines.append("")

    # H2 sections (each MUST be a file list per spec)
    for sec in present_sections:
        lines.append(f"## {sec}")
        lines.append("")
        for path, url in buckets[sec]:
            slug = humanize(path)
            # Mark index pages with a note so LLMs understand context
            note = DESCRIPTIONS[lang].get(sec, "")
            if is_index(path):
                slug = slug + " (index)"
            lines.append(f"- [{slug}]({url})")
        lines.append("")

    # Optional section (per spec, an H2 named "Optional" is the conventional
    # place for non-essential content)
    lines.append("## Optional")
    lines.append("")
    if lang == "en":
        lines.append(f"- [API cost calculator]({SITE}/calculator/)")
        lines.append(f"- [About APIRank]({SITE}/about/)")
        lines.append(f"- [Contact]({SITE}/contact/)")
        lines.append(f"- [Privacy policy]({SITE}/privacy/)")
    else:
        lines.append(f"- [API 成本计算器]({SITE}/zh/calculator/)")
        lines.append(f"- [关于 APIRank]({SITE}/zh/about/)")
        lines.append(f"- [联系我们]({SITE}/zh/contact/)")
        lines.append(f"- [隐私政策]({SITE}/zh/privacy/)")
    lines.append("")

    # Provenance footer
    today = __import__("datetime").date.today().isoformat()
    lines.append(f"<!-- Generated {today} from {SITE}/sitemap-0.xml -->")
    lines.append("")

    return "\n".join(lines)


# ─── Main ─────────────────────────────────────────────────────────────────────
def main() -> int:
    if not SITEMAP.exists():
        print(f"ERROR: {SITEMAP} not found. Run `npm run build` first.", file=sys.stderr)
        return 1

    urls = parse_sitemap(SITEMAP)
    print(f"Parsed {len(urls)} URLs from {SITEMAP.name}")

    en_content = build("en", urls)
    OUT_EN.write_text(en_content, encoding="utf-8")
    print(f"Wrote {OUT_EN} ({len(en_content):,} bytes)")

    zh_content = build("zh", urls)
    OUT_ZH.write_text(zh_content, encoding="utf-8")
    print(f"Wrote {OUT_ZH} ({len(zh_content):,} bytes)")

    # Sanity check: count file-list items (lines starting with "- [")
    for label, content in [("EN", en_content), ("ZH", zh_content)]:
        items = [ln for ln in content.splitlines() if ln.startswith("- [")]
        h2s = [ln for ln in content.splitlines() if ln.startswith("## ")]
        h1s = [ln for ln in content.splitlines() if ln.startswith("# ")]
        print(f"  {label}: {len(h1s)} H1, {len(h2s)} H2 sections, {len(items)} file-list items")

    return 0


if __name__ == "__main__":
    sys.exit(main())