# Google Business Profile Schema

## Schema Overview

Extraction schema for individual Google Business Profile detail pages. This extracts comprehensive data from a single business listing page.

---

## Execution Model

| Requirement | Value |
|-------------|-------|
| **Model** | `1.2_dynamic_browser_javascript_render_model` |
| **Browser** | Selenium / Playwright required |
| **Anti-Bot** | Medium - Rate limiting, JS rendering |
| **Delay** | 2-3 seconds between page loads |

---

## Endpoint Pattern

```
https://www.google.com/maps/place/{business_name}/{place_id}
```

**Examples:**
```
https://www.google.com/maps/place/Starbucks/@25.7617,-80.1918,17z/data=!3m1!4b1
https://www.google.com/maps/place/data=!4m5!3m4!1s0x88d9b0a20ec8c111:0x4d7e7!8m2!3d25.76!4d-80.19
```

---

## Data Fields Extracted

| Field | Type | Description |
|-------|------|-------------|
| `business_name` | string | Official business name |
| `address_full` | string | Complete formatted address |
| `address_street` | string | Street address |
| `address_city` | string | City |
| `address_state` | string | State |
| `address_zip` | string | ZIP code |
| `address_country` | string | Country |
| `phone_number` | string | Primary phone |
| `website_url` | string | Business website |
| `rating_stars` | float | Overall rating (1.0-5.0) |
| `review_count` | int | Total review count |
| `price_level` | string | Price indicator ($, $$, $$$) |
| `category_primary` | string | Main business category |
| `categories_all` | list | All listed categories |
| `hours_structured` | dict | Hours by day |
| `hours_special` | list | Holiday/special hours |
| `attributes` | dict | Business attributes (wheelchair, wifi, etc.) |
| `popular_times` | dict | Popular times by day/hour |
| `photos_count` | int | Number of photos |
| `menu_url` | string | Menu link (if restaurant) |
| `reservation_url` | string | Reservation link |
| `order_url` | string | Online order link |
| `owner_verified` | bool | Owner verified status |
| `place_id` | string | Google Place ID |
| `plus_code` | string | Plus code location |
| `latitude` | float | GPS latitude |
| `longitude` | float | GPS longitude |

---

## Files in This Schema

| File | Purpose |
|------|---------|
| `selectors.json` | XPath and CSS selector definitions |
| `google_business_profile_schema.py` | Main extraction logic |
| `sample_output.json` | Expected output structure |

---

## Usage

```python
from google_business_profile_schema import GoogleBusinessProfileExtractor

extractor = GoogleBusinessProfileExtractor(driver)
writables = extractor.extract_profile_from_url(maps_url)
```

---

## Yield Rates

| Data Point | Yield |
|------------|-------|
| Business Name | 100% |
| Address | 98% |
| Phone | 90% |
| Website | 75% |
| Rating | 95% |
| Hours | 85% |
| Attributes | 70% |
| Popular Times | 60% |
