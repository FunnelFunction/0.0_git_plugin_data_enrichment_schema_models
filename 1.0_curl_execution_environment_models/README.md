# 1.0_curl_execution_environment_models

## Execution Environment Library | The "How to Fetch"

This section defines configuration templates for different execution environments based on target website complexity.

---

## Environment Selection Guide

| Target Complexity | Folder | Use Case |
|-------------------|--------|----------|
| Static HTML | `1.1_simple_curl_static_html_request_model/` | Basic sites, no JS rendering needed |
| Dynamic/JS Content | `1.2_dynamic_browser_javascript_render_model/` | React/Vue/Angular sites, content loads via JS |
| Heavy Anti-Bot | `1.3_stealth_managed_antibot_bypass_model/` | Cloudflare, Akamai, PerimeterX protected sites |

---

## 1.1 Simple Curl Model

**When to use:** Static HTML pages with content in initial response

**Key characteristics:**
- HTTP request client (no browser needed)
- Fast, high-volume capable
- Focus on headers (User-Agent rotation)

**Typical implementation:**
```python
# Python requests or raw curl
headers = {"User-Agent": "Mozilla/5.0..."}
response = requests.get(url, headers=headers)
```

**Anti-bot handling:** Basic rate limiting, gentle pacing (1-2s delays)

---

## 1.2 Dynamic Browser Model

**When to use:** JavaScript-rendered content (SPA frameworks)

**Key characteristics:**
- Headless browser required (Selenium, Playwright, Puppeteer)
- Must wait for elements to load (`explicit waits`)
- Full DOM rendering before extraction

**Typical implementation:**
```python
# Selenium/Playwright
browser.get(url)
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".content"))
)
```

**Anti-bot handling:** JS enablement checks, basic fingerprinting, behavioral pacing

---

## 1.3 Stealth Managed Model

**When to use:** Sites with sophisticated bot protection

**Key characteristics:**
- IP rotation (residential proxies)
- Automated CAPTCHA solving
- Realistic TLS/HTTP2 fingerprinting
- Human-like mouse movements and delays

**Typical implementation:**
```python
# Integration with proxy services / scraping APIs
# ScraperAPI, ZenRows, Bright Data, Smartproxy
api_url = f"http://api.scraperapi.com?api_key={KEY}&url={target_url}"
```

**Anti-bot handling:** IP blacklisting, advanced fingerprinting, CAPTCHAs, honeypots, WAFs

---

## Execution Model Reference

The actual execution environment is managed by:
[0.0_git_universal_protocol_os_handshake](https://github.com/intent-tensor-theory/0.0_git_universal_protocol_os_handshake)

This folder contains **configuration templates** that reference which model to use for each platform schema.
