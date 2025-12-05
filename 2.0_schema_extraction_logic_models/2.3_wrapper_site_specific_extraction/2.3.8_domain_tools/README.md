# 2.3.8_domain_tools

## Domain Tool Schemas

Extraction schemas for domain lookup and WHOIS data.

---

## Platform Overview

| Tool | Execution Model | Data Type |
|------|-----------------|-----------|
| **WHOIS** | 1.1 Simple Curl | Domain registration data |

---

## Schemas in This Folder

```
2.3.8_domain_tools/
└── whois_domain_lookup_schema/
```

---

## WHOIS Data Fields

- Domain name
- Registrar
- Registration date
- Expiration date
- Updated date
- Registrant name (if not private)
- Registrant organization
- Registrant email
- Registrant phone
- Name servers
- Domain status

---

## WHOIS Endpoints

**Command line:**
```bash
whois example.com
```

**Web APIs:**
- whois.domaintools.com
- who.is
- whois.icann.org

---

## Privacy Notes

Many domains use privacy protection services that mask registrant data. Fields may return:
- "REDACTED FOR PRIVACY"
- Proxy service contact info
- Generic placeholder data

---

## Use Cases

- Lead generation (finding domain owners)
- Brand protection (monitoring registrations)
- Due diligence (verifying business legitimacy)
- Competitive research
