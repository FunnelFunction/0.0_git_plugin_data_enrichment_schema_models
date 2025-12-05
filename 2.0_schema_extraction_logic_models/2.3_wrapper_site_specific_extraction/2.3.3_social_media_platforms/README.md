# 2.3.3_social_media_platforms

## Social Media Platform Schemas

Extraction schemas for social media platforms. **These are the dicey ones** - heavy anti-bot protection.

---

## Platform Overview

| Platform | Execution Model | Anti-Bot Level | Notes |
|----------|-----------------|----------------|-------|
| **LinkedIn** | 1.3 Stealth | HEAVY | Aggressive detection, account bans |
| **Facebook** | 1.3 Stealth | HEAVY | Login walls, fingerprinting |
| **Instagram** | 1.3 Stealth | HEAVY | Rate limiting, API restrictions |
| **Twitter/X** | 1.2-1.3 | Medium-Heavy | API changes frequently |
| **TikTok** | 1.3 Stealth | HEAVY | Advanced fingerprinting |
| **YouTube** | 1.2 Dynamic | Medium | JS rendering required |
| **Reddit** | 1.1-1.2 | Low-Medium | API available, rate limits |

---

## Schemas in This Folder

```
2.3.3_social_media_platforms/
├── linkedin/
│   ├── linkedin_profile_schema/
│   ├── linkedin_company_page_schema/
│   └── linkedin_job_posting_schema/
├── facebook/
│   ├── facebook_profile_schema/
│   └── facebook_business_page_schema/
├── instagram/
│   └── instagram_profile_schema/
├── twitter_x/
│   └── twitter_x_profile_schema/
├── tiktok/
│   └── tiktok_profile_schema/
├── youtube/
│   ├── youtube_channel_schema/
│   └── youtube_video_metadata_schema/
└── reddit/
    └── reddit_post_thread_schema/
```

---

## LinkedIn Data Fields

- Profile: Name, headline, location, connections, experience, education
- Company: Name, industry, size, headquarters, employees
- Jobs: Title, company, location, description, requirements

---

## Anti-Bot Requirements (Stealth Platforms)

For LinkedIn, Facebook, Instagram, TikTok:
- Residential proxy rotation
- Browser fingerprint randomization
- Human-like delays (3-10s between actions)
- Session management
- CAPTCHA solving integration
- Account warm-up periods

**Recommended:** Use managed scraping APIs (ScraperAPI, ZenRows) for these platforms.
