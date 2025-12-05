# 2.3.1_google

## Google Platform Schemas

Extraction schemas for Google properties.

---

## Platform Overview

| Property | Data Yield | Coverage | Execution Model |
|----------|------------|----------|-----------------|
| Google Search Results | Organic listings, ads, snippets | Global | 1.2 Dynamic Browser |
| Google Maps | 90%+ fresh locations, reviews, hours | 50M+ US businesses | 1.2 Dynamic Browser |
| Google Business Profile | Name, address, phone, website, rating, category | Tied to Maps | 1.2 Dynamic Browser |

---

## Schemas in This Folder

```
2.3.1_google/
├── google_search_results_schema/
├── google_maps_listings_schema/
└── google_business_profile_schema/
```

---

## Google Maps Notes

**Base endpoint pattern:**
```
/search?q=plumbers+MIAMI
```

**Pagination:** Rotate every 20 results

**Data fields:**
- Name
- Address
- Phone
- Website
- Rating
- Category
- Reviews
- Hours

**Anti-bot:** Requires browser rendering (1.2 model), rate limiting
