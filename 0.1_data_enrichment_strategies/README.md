# 0.1_data_enrichment_strategies

## Strategy Overview | The "Why" of Data Enrichment

This section defines the high-level strategy for web data extraction before any code is written.

---

## The Two-Part Architecture

Web scraping consists of two distinct components:

| Part | Name | Responsibility |
|------|------|----------------|
| **Part 1** | Execution Environment | The tool/system that fetches HTML (requests, browsers, stealth layers) |
| **Part 2** | Schema/Extraction Logic | The specific instructions for WHAT data to pull from WHERE |

**This repository focuses on Part 2** - the schema plugins that define extraction logic.

---

## Execution Environment Complexity Levels

| Level | Environment Type | When to Use | Anti-Bot Measures |
|-------|-----------------|-------------|-------------------|
| **1.1** | Simple Curl | Static HTML, no JS needed | Basic rate limiting |
| **1.2** | Dynamic Browser | JavaScript-rendered content | JS checks, basic fingerprinting |
| **1.3** | Stealth Managed | Heavy anti-bot protection | IP rotation, CAPTCHA solving, TLS fingerprinting |

---

## Schema Design Philosophy

### PRE-X MetaMapping Applied

Schemas define the decision map BEFORE execution:
- What fields to extract
- What selectors to use
- What transformations to apply
- What the expected output structure looks like

**The kernel never decides - it follows the schema.**

### Writables Doctrine Applied

```
writables = fetchHTML()
writables = applySchema(writables, schema)
writables = transformFields(writables)
writables = validateOutput(writables)
```

Single stream, never rename - only refine.

---

## Platform Categorization Strategy

Platforms are organized by:
1. **Primary function** (search, social, commerce, etc.)
2. **Anti-bot complexity** (determines execution model)
3. **Data yield potential** (email %, phone %, etc.)

See [2.3_wrapper_site_specific_extraction](../2.0_schema_extraction_logic_models/2.3_wrapper_site_specific_extraction/) for platform-specific schemas.
