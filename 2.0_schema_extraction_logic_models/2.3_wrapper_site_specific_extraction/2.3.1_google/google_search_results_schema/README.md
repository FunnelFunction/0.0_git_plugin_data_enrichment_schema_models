# Google Search Results Schema

## Schema Overview

Extraction schema for Google Search Results Pages (SERPs). Extracts organic results, ads, featured snippets, and other SERP features.

---

## Execution Model

| Requirement | Value |
|-------------|-------|
| **Model** | `1.2_dynamic_browser_javascript_render_model` |
| **Browser** | Selenium / Playwright required |
| **Anti-Bot** | Medium-High - CAPTCHA possible on volume |
| **Delay** | 3-5 seconds between searches |

---

## Endpoint Pattern

```
https://www.google.com/search?q={query}&num={results_per_page}
```

**Examples:**
```
https://www.google.com/search?q=plumbers+miami
https://www.google.com/search?q=best+restaurants+near+me&num=50
https://www.google.com/search?q=site:example.com
```

---

## Data Fields Extracted

### Organic Results
| Field | Type | Description |
|-------|------|-------------|
| `position` | int | Ranking position (1-indexed) |
| `title` | string | Result title/headline |
| `url` | string | Destination URL |
| `displayed_url` | string | URL shown in result |
| `description` | string | Meta description snippet |
| `date_published` | string | Publication date (if shown) |
| `rich_snippet` | dict | Structured data (ratings, prices, etc.) |

### Ads (Sponsored Results)
| Field | Type | Description |
|-------|------|-------------|
| `position` | int | Ad position |
| `title` | string | Ad headline |
| `url` | string | Landing page URL |
| `displayed_url` | string | Displayed URL |
| `description` | string | Ad copy |
| `ad_extensions` | list | Sitelinks, callouts, etc. |

### SERP Features
| Field | Type | Description |
|-------|------|-------------|
| `featured_snippet` | dict | Featured snippet content |
| `people_also_ask` | list | PAA questions |
| `related_searches` | list | Related search suggestions |
| `knowledge_panel` | dict | Knowledge panel data |
| `local_pack` | list | Local 3-pack results |

---

## Files in This Schema

| File | Purpose |
|------|---------|
| `selectors.json` | XPath and CSS selector definitions |
| `google_search_results_schema.py` | Main extraction logic |
| `sample_output.json` | Expected output structure |

---

## Usage

```python
from google_search_results_schema import GoogleSearchResultsExtractor

extractor = GoogleSearchResultsExtractor(driver)
writables = extractor.extract_results_by_query("plumbers miami", max_pages=1)
```

---

## Anti-Bot Considerations

- **CAPTCHA Risk**: High volume triggers CAPTCHA
- **Rate Limiting**: 3-5 second delays recommended
- **User-Agent**: Rotate realistic browser user-agents
- **Cookies**: Accept cookies to appear more legitimate
- **Proxy**: Consider residential proxies for volume
