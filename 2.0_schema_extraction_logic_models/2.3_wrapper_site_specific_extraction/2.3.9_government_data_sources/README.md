# 2.3.9_government_data_sources

## Government Data Source Schemas

Extraction schemas for federal, state, and local government data sources.

---

## Structure Overview

```
2.3.9_government_data_sources/
├── federal/                    ← Federal agency data
└── state/                      ← All 50 states + DC
    ├── [state_name]/
    │   ├── county/            ← County-level data
    │   ├── city/              ← City/municipal data
    │   └── zip/               ← ZIP code specific data
```

---

## Coverage

| Level | Folders | Examples |
|-------|---------|----------|
| **Federal** | 1 | SEC, FCC, USPTO, Census, FOIA |
| **State** | 51 | Secretary of State, licensing boards, courts |
| **County** | Expandable | Property records, courts, assessors |
| **City** | Expandable | Permits, licenses, inspections |
| **ZIP** | Expandable | Demographic, postal data |

---

## States Included

All 50 states plus District of Columbia:
- Alabama through Wyoming
- District of Columbia

Each state folder contains `county/`, `city/`, and `zip/` subfolders for granular data organization.

---

## Common Government Data Types

### Federal Level
- Business registrations (SEC)
- FCC licenses
- Patent/trademark data (USPTO)
- Census data
- Court records (PACER)

### State Level
- Business entity filings
- Professional licenses
- Court records
- Property records
- Vital records

### Local Level
- Property tax records
- Building permits
- Business licenses
- Code violations
- Zoning data

---

## Execution Model

Most government sites: **1.1 Simple Curl** or **1.2 Dynamic Browser**

Government sites rarely have aggressive anti-bot measures, but may have:
- Rate limiting
- CAPTCHA on bulk downloads
- Session timeouts
- Outdated/inconsistent HTML structures

---

## Usage Notes

Government data is generally public record, but:
- Respect rate limits
- Check terms of service
- Some data may require FOIA requests
- Data freshness varies widely
