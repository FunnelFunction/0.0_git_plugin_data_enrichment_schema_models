# 2.3.7_job_platforms

## Job Platform Schemas

Extraction schemas for job listing and employment sites.

---

## Platform Overview

| Platform | Execution Model | Data Type | Anti-Bot Level |
|----------|-----------------|-----------|----------------|
| **Indeed** | 1.2 Dynamic | Job postings, salaries | Medium |
| **Glassdoor Jobs** | 1.2-1.3 | Jobs, company data | Medium-Heavy |

---

## Schemas in This Folder

```
2.3.7_job_platforms/
├── indeed_job_posting_schema/
└── glassdoor_job_posting_schema/
```

---

## Indeed Data Fields

- Job title
- Company name
- Location
- Salary (when posted)
- Job type (full-time, part-time, contract)
- Description
- Requirements
- Benefits
- Post date
- Apply link

---

## Glassdoor Jobs Data Fields

- Job title
- Company name + rating
- Location
- Salary estimate
- Description
- Company reviews link
- Easy apply status

---

## Endpoint Patterns

**Indeed:**
```
/jobs?q=software+engineer&l=Miami
```

**Glassdoor:**
```
/Job/jobs.htm?sc.keyword=software+engineer&locT=C&locId=1154170
```

---

## Anti-Bot Notes

| Platform | Notes |
|----------|-------|
| Indeed | JS rendering, rate limiting, CAPTCHA on volume |
| Glassdoor | Login walls for some data, fingerprinting |
