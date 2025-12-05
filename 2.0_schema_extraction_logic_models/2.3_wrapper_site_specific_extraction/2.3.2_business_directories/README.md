# 2.3.2_business_directories

## Business Directory Platform Schemas

Extraction schemas for business listing and directory sites.

---

## Platform Overview

| Platform | Listings | Email Yield | Coverage | Endpoint Pattern | Execution Model |
|----------|----------|-------------|----------|------------------|-----------------|
| **Yelp** | 70M+ | 40% | 80% US | `?q=plumbers&miami` | 1.2 Dynamic |
| **YellowPages** | 20M+ | 60% | 90% US | `/search?search_terms=plumbers&geo_location_terms=Miami` | 1.1 Simple Curl |
| **WhitePages** | 200M+ | 50% | 95% US | `/search?term=plumbers+miami` | 1.1 Simple Curl |
| **Manta** | 50M+ SMBs | 30% | 85% US | `/search?q=plumbers&location=miami` | 1.1 Simple Curl |
| **Superpages** | 10M+ | 40% | 80% US | `/search?ST=plumbers&city=Miami` | 1.1 Simple Curl |
| **411.com** | 15M+ | Phone-heavy | 90% US | `/search/plumbers/Miami` | 1.1 Simple Curl |
| **BBB** | Verified | High quality | 70% US | Varies by region | 1.1 Simple Curl |
| **Chamber of Commerce** | 4M+ verified | High quality | 70% US (local) | `/directory?location=miami&category=plumbers` | 1.1 Simple Curl |

---

## Schemas in This Folder

```
2.3.2_business_directories/
├── yelp_business_listing_schema/
├── yellowpages_business_schema/
├── whitepages_contact_schema/
├── manta_smb_schema/
├── superpages_local_schema/
├── 411_directory_schema/
├── better_business_bureau_schema/
└── chamber_of_commerce_schema/
```

---

## Common Data Fields

- Business Name
- Address (street, city, state, zip)
- Phone
- Email (yield varies by platform)
- Website
- Category/Industry
- Reviews/Ratings (where available)

---

## Anti-Bot Notes

| Platform | Difficulty | Notes |
|----------|------------|-------|
| Yelp | Medium | User-agent rotation + 2s delay required |
| YellowPages | Easy | Basic headers sufficient |
| WhitePages | Easy | Best for phone/email extraction |
| Manta | Easy | Good for B2B data |
| BBB | Easy | High quality, lower volume |
