#!/usr/bin/env python3
import urllib.request, urllib.error, re
from concurrent.futures import ThreadPoolExecutor, as_completed

def deep_probe(d):
    out = {'domain': d}
    # 1) 首页
    homepage_found = False
    for scheme in ['https', 'http']:
        try:
            req = urllib.request.Request(f'{scheme}://{d}/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
            with urllib.request.urlopen(req, timeout=10) as r:
                out['homepage_status'] = r.status
                out['homepage_url'] = r.geturl()
                body = r.read(80000).decode('utf-8', errors='ignore')
                homepage_found = True
                break
        except urllib.error.HTTPError as e:
            if e.code in [301, 302]:  # 重定向也算找到
                out['homepage_status'] = e.code
                out['homepage_url'] = e.headers.get('Location', '')
                break
            out['homepage_error'] = f"{scheme}: HTTP {e.code}"
        except Exception as e:
            out['homepage_error'] = f"{scheme}: {str(e)[:150]}"
    if not homepage_found:
        if 'homepage_status' not in out:
            out['homepage_status'] = 'fail'
        return out
    
    # 2) 标题/描述
    m = re.search(r'<title[^>]*>([^<]+)</title>', body, re.I)
    out['title'] = m.group(1).strip()[:120] if m else ''
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)', body, re.I)
    out['description'] = m.group(1).strip()[:200] if m else ''
    m = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)', body, re.I)
    if not out['title'] and m:
        out['title'] = m.group(1).strip()[:120]
    
    # 3) 关键页面探测
    for path in ['/pricing', '/price', '/docs', '/api', '/models', '/about', '/register', '/login', '/dashboard']:
        try:
            req = urllib.request.Request(f'https://{d}{path}', method='GET', headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=8) as r:
                out[f'path_{path.strip("/")}_status'] = r.status
        except urllib.error.HTTPError as e:
            out[f'path_{path.strip("/")}_status'] = e.code
        except Exception:
            out[f'path_{path.strip("/")}_status'] = 'fail'
    
    # 4) 关键词检测
    body_low = body.lower()
    keywords = {
        'relay_words': ['中转', '转发', '聚合', '分销', '分发'],
        'brands': ['claude', 'gpt-4', 'chatgpt', 'gemini', 'deepseek', 'kimi',
                   'moonshot', 'qwen', '通义', '豆包', 'doubao', 'mistral',
                   'hunyuan', 'zhipu', '智谱', 'minimax', 'grok'],
        'pricing_words': ['价格', '计费', 'pricing', 'price', '¥', '$', 'tokens',
                          '元/百万', 'per million', 'per 1k', 'rate'],
        'contact': ['微信', 'wechat', 'telegram', 'tg', '客服', 'support',
                    'contact@', 'mailto:', 'qq 群', 'qq 群'],
    }
    for cat, words in keywords.items():
        hits = [w for w in words if w in body_low]
        out[f'has_{cat}'] = bool(hits)
        out[f'{cat}_hits'] = hits[:10]
    
    # 5) 套壳 New API 信号
    title_check = (out.get('title','') or '').lower().strip()
    if title_check in ['new api', 'new api', 'new api']:
        out['is_cloneshell'] = True
    else:
        out['is_cloneshell'] = False
    
    return out

if __name__ == '__main__':
    import json
    import time
    
    domains = ['foxcode.rjj.cc', 'fuli.hxi.me', 'yunwu.zeabur.app', 'api.xty.app', 'clauddy.com']
    
    print(f"🚀 Starting deep probe for {len(domains)} domains...")
    start_time = time.time()
    
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_domain = {executor.submit(deep_probe, d): d for d in domains}
        for future in as_completed(future_to_domain):
            d = future_to_domain[future]
            try:
                result = future.result()
                results.append(result)
                print(f"✅ {d} done")
            except Exception as e:
                print(f"❌ {d} error: {e}")
    
    elapsed = time.time() - start_time
    print(f"\n⏱ Probe took {elapsed:.1f}s")
    
    # Output as JSON
    print("\n=== RESULTS JSON ===")
    print(json.dumps(results, ensure_ascii=False, indent=2))