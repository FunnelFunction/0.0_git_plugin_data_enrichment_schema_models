# 2.3.6_real_estate_platforms

## Real Estate Platform Schemas

Extraction schemas for property listing and real estate data sites.

---

## Platform Overview

| Platform | Execution Model | Coverage | Data Type |
|----------|-----------------|----------|-----------|
| **Zillow** | 1.2-1.3 | US nationwide | Listings, Zestimates, history |
| **Realtor.com** | 1.2 Dynamic | US nationwide | MLS listings, agents |
| **Redfin** | 1.2 Dynamic | US major markets | Listings, market data |

---

## Schemas in This Folder

```
2.3.6_real_estate_platforms/
├── zillow_property_listing_schema/
├── realtor_listing_schema/
└── redfin_listing_schema/
```

---

## Common Data Fields

- Property address
- Price (list, sold, Zestimate)
- Bedrooms / Bathrooms
- Square footage
- Lot size
- Year built
- Property type
- Listing status
- Agent/broker info
- Photos
- Description
- Price history
- Tax history

---

## Zillow-Specific Fields

- Zestimate (automated valuation)
- Rent Zestimate
- Neighborhood data
- School ratings
- Walk score
- Transit score

---

## Anti-Bot Notes

| Platform | Notes |
|----------|-------|
| Zillow | Aggressive anti-bot, may need stealth model |
| Realtor.com | JS rendering required |
| Redfin | Moderate protection, browser rendering |

**Note:** Real estate data often protected by terms of service. Use responsibly.
