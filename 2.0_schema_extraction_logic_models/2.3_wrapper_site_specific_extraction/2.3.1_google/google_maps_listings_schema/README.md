# Google Maps Listings Schema

## Schema Overview

Extraction schema for Google Maps business listings from search results.

---

## Execution Model

| Requirement | Value |
|-------------|-------|
| **Model** | `1.2_dynamic_browser_javascript_render_model` |
| **Browser** | Selenium / Playwright required |
| **Anti-Bot** | Medium - Rate limiting, JS rendering |
| **Delay** | 2-3 seconds between requests |

---

## Endpoint Pattern

```
https://www.google.com/maps/search/{query}+{location}
```

**Examples:**
```
https://www.google.com/maps/search/plumbers+miami+fl
https://www.google.com/maps/search/restaurants+near+me
https://www.google.com/maps/search/dentists+90210
```

---

## Data Fields Extracted

| Field | Type | Description |
|-------|------|-------------|
| `business_name` | string | Business name |
| `address_full` | string | Complete street address |
| `city` | string | City name |
| `state` | string | State abbreviation |
| `zip_code` | string | ZIP/Postal code |
| `phone_number` | string | Phone number |
| `website_url` | string | Business website |
| `rating_stars` | float | Star rating (1.0-5.0) |
| `review_count` | int | Number of reviews |
| `category` | string | Business category |
| `hours_json` | object | Operating hours |
| `latitude` | float | GPS latitude |
| `longitude` | float | GPS longitude |
| `place_id` | string | Google Place ID |
| `maps_url` | string | Direct Google Maps URL |

---

## Files in This Schema

| File | Purpose |
|------|---------|
| `selectors.json` | XPath and CSS selector definitions |
| `google_maps_listings_schema.py` | Main extraction logic |
| `sample_output.json` | Expected output structure |

---

## Usage

```python
from google_maps_listings_schema import GoogleMapsListingsExtractor

extractor = GoogleMapsListingsExtractor()
writables = extractor.extract_listings_by_query("plumbers", "miami fl")
```

---

## Yield Rates

| Data Point | Yield |
|------------|-------|
| Business Name | 100% |
| Address | 95% |
| Phone | 85% |
| Website | 70% |
| Rating | 90% |
| Hours | 75% |

---

## Notes

- Pagination: Scroll to load more results (infinite scroll)
- Results cap: ~120 listings per search typically
- Rate limit: 20 searches per session recommended before rotating
