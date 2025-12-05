# 2.3.5_review_platforms

## Review Platform Schemas

Extraction schemas for review and rating aggregation sites.

---

## Platform Overview

| Platform | Focus | Execution Model | Data Type |
|----------|-------|-----------------|-----------|
| **TripAdvisor** | Travel, hospitality | 1.2 Dynamic | Hotels, restaurants, attractions |
| **Trustpilot** | Business reviews | 1.1-1.2 | Company reviews, ratings |
| **Glassdoor** | Employment | 1.2-1.3 | Company reviews, salaries |

---

## Schemas in This Folder

```
2.3.5_review_platforms/
├── tripadvisor_review_schema/
├── trustpilot_review_schema/
└── glassdoor_company_review_schema/
```

---

## TripAdvisor Data Fields

- Business name
- Location
- Overall rating
- Review count
- Individual reviews (text, rating, date, reviewer)
- Category ranking
- Price range
- Amenities

---

## Trustpilot Data Fields

- Company name
- Trust score
- Total reviews
- Star breakdown
- Individual reviews
- Response rate
- Company details

---

## Glassdoor Data Fields

- Company name
- Overall rating
- CEO approval
- Recommend to friend %
- Reviews (pros, cons, advice)
- Salary data
- Interview experiences

---

## Anti-Bot Notes

| Platform | Notes |
|----------|-------|
| TripAdvisor | JS rendering, pagination handling |
| Trustpilot | Generally accessible, rate limiting |
| Glassdoor | Login walls for some data, stealth may be needed |
