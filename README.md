# 0.0_git_plugin_data_enrichment_schema_models

## README of READMEs | Data Enrichment Schema Plugin Library

This repository contains **schema plugins** for web data extraction. These are the "what to extract" definitions that plug into execution environments.

---

## Architecture Overview

| Component | Purpose | Location |
|-----------|---------|----------|
| **Execution Environment** | HOW to fetch HTML (requests, browsers, stealth) | [0.0_git_universal_protocol_os_handshake](https://github.com/intent-tensor-theory/0.0_git_universal_protocol_os_handshake) |
| **Schema Plugins** | WHAT to extract from HTML | **This Repository** |

---

## Repository Structure

```
0.0_git_plugin_data_enrichment_schema_models/
│
├── 0.1_data_enrichment_strategies/       ← Strategy overview (the "why")
│
├── 1.0_curl_execution_environment_models/ ← Execution configs (the "how to fetch")
│   ├── 1.1_simple_curl_static_html_request_model/
│   ├── 1.2_dynamic_browser_javascript_render_model/
│   └── 1.3_stealth_managed_antibot_bypass_model/
│
└── 2.0_schema_extraction_logic_models/    ← Extraction schemas (the "what to pull")
    ├── 2.1_selector_xpath_css_definitions/
    ├── 2.2_parser_transformation_logic/
    └── 2.3_wrapper_site_specific_extraction/
        ├── 2.3.1_google/
        ├── 2.3.2_business_directories/
        ├── 2.3.3_social_media_platforms/
        ├── 2.3.4_ecommerce_platforms/
        ├── 2.3.5_review_platforms/
        ├── 2.3.6_real_estate_platforms/
        ├── 2.3.7_job_platforms/
        ├── 2.3.8_domain_tools/
        └── 2.3.9_government_data_sources/
```

---

## Numbering System (ISA Compliant)

| Prefix | Layer | Description |
|--------|-------|-------------|
| `0.x` | Meta/Strategy | The "why" - overall enrichment philosophy |
| `1.x` | Execution | The "how" - curl models and browser configs |
| `2.x` | Extraction | The "what" - schemas, selectors, parsers |

---

## Coding Principles

This repository follows [Intent Tensor Theory Coding Principals](https://github.com/intent-tensor-theory/0.0_Coding_Principals_Intent_Tensor_Theory):

- **Ghostless Coding**: Every name declares full intent
- **Writables Doctrine**: Single-stream data pipeline
- **PRE-X MetaMapping**: Schemas define decisions before runtime
- **Infrastructure Semantic Anchoring (ISA)**: `0.0_git_plugin_` prefix anchors this as foundational plugin layer

---

## Sub-README Index

| Section | README Location |
|---------|-----------------|
| Data Enrichment Strategies | [0.1_data_enrichment_strategies/README.md](./0.1_data_enrichment_strategies/README.md) |
| Curl Execution Models | [1.0_curl_execution_environment_models/README.md](./1.0_curl_execution_environment_models/README.md) |
| Schema Extraction Models | [2.0_schema_extraction_logic_models/README.md](./2.0_schema_extraction_logic_models/README.md) |

---

## Quick Start

1. Identify your target platform in `2.3_wrapper_site_specific_extraction/`
2. Check which execution model is required (simple curl vs browser vs stealth)
3. Copy the schema into your extraction pipeline
4. The schema plugs into the execution environment - it just works

---

## License

Schema plugins for data enrichment workflows.
