# 2.3.4_ecommerce_platforms

## E-commerce Platform Schemas

Extraction schemas for e-commerce and marketplace sites.

---

## Platform Overview

| Platform | Execution Model | Data Type | Anti-Bot Level |
|----------|-----------------|-----------|----------------|
| **Amazon** | 1.2-1.3 | Products, prices, reviews | Medium-Heavy |
| **eBay** | 1.2 Dynamic | Auctions, products, sellers | Medium |
| **Craigslist** | 1.1 Simple Curl | Classifieds, local listings | Low |

---

## Schemas in This Folder

```
2.3.4_ecommerce_platforms/
├── amazon_product_listing_schema/
├── ebay_product_listing_schema/
└── craigslist_posting_schema/
```

---

## Amazon Data Fields

- Product title
- Price (current, list, sale)
- Rating (stars, count)
- Reviews
- Seller info
- Category/ASIN
- Availability
- Images

---

## eBay Data Fields

- Item title
- Current bid / Buy It Now price
- Time remaining
- Seller rating
- Item condition
- Shipping info

---

## Craigslist Data Fields

- Post title
- Price
- Location
- Description
- Contact info (often hidden)
- Post date
- Category

---

## Anti-Bot Notes

| Platform | Notes |
|----------|-------|
| Amazon | Rotating proxies recommended, CAPTCHA on high volume |
| eBay | JS rendering required, moderate rate limiting |
| Craigslist | Easy, but IP bans on abuse |
