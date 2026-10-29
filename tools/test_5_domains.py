#!/usr/bin/env python3
"""单日 5 个域名批量检测工具 - APIRank"""
import urllib.request
import urllib.error
import re
import json
import ssl
from datetime import datetime, timezone
import time

DOMAINS = ["529961.com", "91code.pro", "api.wpgzs.top", "applyj.hiapi.top", "augmunt.com"]
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
TIMEOUT = 10

def probe_domain(domain):
    result = {
        'domain': domain,
        'ts': datetime.now(timezone.utc).isoformat(),
        'homepage_status': 'fail',
        'homepage_url': '',
        'title': '',
        'meta_description': '',
        'score': 0,
        'verdict': '',
        'path_pricing_status': None, 'path_price_status': None,
        'path_docs_status': None, 'path_api_status': None,
        'path_models_status': None, 'path_about_status': None,
        'path_register_status': None, 'path_login_status': None,
        'path_dashboard_status': None, 'error': '',
    }
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        url = f'https://{domain}/'
        req = urllib.request.Request(url, headers=HEADERS)
        start_time = time.time()
        
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
            result['homepage_status'] = resp.status
            result['homepage_url'] = resp.geturl()
            body = resp.read(80000).decode('utf-8', errors='ignore')
            result['response_time'] = round((time.time() - start_time) * 1000, 2)
            
            m = re.search(r'<title[^>]*>([^<]+)</title>', body, re.I)
            if m:
                result['title'] = m.group(1).strip()[:300]
            
            m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)', body, re.I)
            if m:
                result['meta_description'] = m.group(1).strip()[:300]
    
    except urllib.error.HTTPError as e:
        result['homepage_status'] = e.code
        result['error'] = f'HTTP {e.code}'
    except urllib.error.URLError as e:
        result['error'] = f'URLError: {str(e.reason)[:200]}'
    except Exception as e:
        result['error'] = f'Exception: {str(e)[:200]}'
    
    subpaths = ['/pricing', '/price', '/docs', '/api', '/models', '/about', '/register', '/login', '/dashboard']
    for path in subpaths:
        try:
            req = urllib.request.Request(f'https://{domain}{path}', headers=HEADERS)
            with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
                result[f'path_{path[1:]}_status'] = resp.status
        except urllib.error.HTTPError as e:
            result[f'path_{path[1:]}_status'] = e.code
        except:
            pass
    
    score = 0
    if result['homepage_status'] in [200, 301, 302]:
        score += 5
    if result.get('title') and result['title'].strip() not in ['Loading...', 'New API', 'Domain for Sale']:
        score += 2
    if result.get('meta_description') and result['meta_description'].strip():
        score += 1
    if result.get('path_pricing_status') in [200, 301, 302]:
        score += 1
    if result.get('path_docs_status') in [200, 301, 302]:
        score += 1
    
    result['score'] = min(10, score)
    
    if result['homepage_status'] == 'fail':
        result['verdict'] = '已不可达'
    elif result['score'] >= 6:
        result['verdict'] = '值得收录'
    elif result['score'] >= 3:
        result['verdict'] = '备选'
    else:
        result['verdict'] = '维护差跳过'
    
    return result

def main():
    print(f"Starting probing: {DOMAINS}")
    all_results = []
    for d in DOMAINS:
        print(f"  Testing: {d}")
        r = probe_domain(d)
        all_results.append(r)
        print(f"    -> {r['homepage_status']} | score={r['score']} | {r['verdict']}")
        if r['error']:
            print(f"    -> Error: {r['error']}")
    
    with open('/root/apirank/tools/test_5_result.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\nResults saved to /root/apirank/tools/test_5_result.json")
    return json.dumps(all_results, ensure_ascii=False)

if __name__ == '__main__':
    print(main())