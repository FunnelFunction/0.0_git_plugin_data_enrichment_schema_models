# 2.0_schema_extraction_logic_models

## Schema Extraction Library | The "What to Pull"

This section contains the actual extraction schemas - the code that defines WHAT data to extract from HTML.

---

## Structure Overview

```
2.0_schema_extraction_logic_models/
├── 2.1_selector_xpath_css_definitions/    ← Reusable selector patterns
├── 2.2_parser_transformation_logic/       ← Data transformation utilities
└── 2.3_wrapper_site_specific_extraction/  ← Platform-specific schemas
```

---

## 2.1 Selector Definitions

Common XPath and CSS selector patterns used across multiple schemas.

**Purpose:** DRY principle - define once, reuse everywhere

---

## 2.2 Parser Transformation Logic

Data transformation functions:
- Phone number normalization
- Email extraction and validation
- Address parsing
- Rating/review aggregation

---

## 2.3 Site-Specific Wrappers

**The main event.** Platform-specific extraction schemas organized by category:

| Category | Folder | Platforms |
|----------|--------|-----------|
| Search/Maps | `2.3.1_google/` | Google Search, Maps, Business Profile |
| Business Directories | `2.3.2_business_directories/` | Yelp, YellowPages, WhitePages, Manta, BBB, etc. |
| Social Media | `2.3.3_social_media_platforms/` | LinkedIn, Facebook, Instagram, Twitter/X, TikTok, YouTube, Reddit |
| E-commerce | `2.3.4_ecommerce_platforms/` | Amazon, eBay, Craigslist |
| Reviews | `2.3.5_review_platforms/` | TripAdvisor, Trustpilot, Glassdoor |
| Real Estate | `2.3.6_real_estate_platforms/` | Zillow, Realtor, Redfin |
| Jobs | `2.3.7_job_platforms/` | Indeed, Glassdoor Jobs |
| Domain Tools | `2.3.8_domain_tools/` | WHOIS lookups |
| Government | `2.3.9_government_data_sources/` | Federal, State (all 50 + DC), County, City, Zip |

---

## Schema Structure (Ghostless Standard)

Each schema folder contains:
```
platform_schema/
├── README.md           ← Platform notes, endpoints, yield rates
├── selectors.json      ← XPath/CSS definitions
├── schema.py           ← Extraction logic
└── sample_output.json  ← Expected output structure
```

---

## Platform README Index

| Platform Category | README |
|-------------------|--------|
| Google | [2.3.1_google/README.md](./2.3_wrapper_site_specific_extraction/2.3.1_google/README.md) |
| Business Directories | [2.3.2_business_directories/README.md](./2.3_wrapper_site_specific_extraction/2.3.2_business_directories/README.md) |
| Social Media | [2.3.3_social_media_platforms/README.md](./2.3_wrapper_site_specific_extraction/2.3.3_social_media_platforms/README.md) |
| E-commerce | [2.3.4_ecommerce_platforms/README.md](./2.3_wrapper_site_specific_extraction/2.3.4_ecommerce_platforms/README.md) |
| Reviews | [2.3.5_review_platforms/README.md](./2.3_wrapper_site_specific_extraction/2.3.5_review_platforms/README.md) |
| Real Estate | [2.3.6_real_estate_platforms/README.md](./2.3_wrapper_site_specific_extraction/2.3.6_real_estate_platforms/README.md) |
| Jobs | [2.3.7_job_platforms/README.md](./2.3_wrapper_site_specific_extraction/2.3.7_job_platforms/README.md) |
| Domain Tools | [2.3.8_domain_tools/README.md](./2.3_wrapper_site_specific_extraction/2.3.8_domain_tools/README.md) |
| Government | [2.3.9_government_data_sources/README.md](./2.3_wrapper_site_specific_extraction/2.3.9_government_data_sources/README.md) |
