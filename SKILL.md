---
name: negative-monitor
description: Monitor negative public events for one or more companies, preserve full evidence, classify repayment-risk signals, and produce Excel + JSON + alert-ready summaries.
---

# Negative Monitor

## Overview

This skill performs negative-event monitoring in two layers for one or multiple companies.
It preserves all retrieval evidence for auditability, then extracts and classifies repayment-risk signals for downstream warning channels.

## When To Use

Use this skill when the user asks to:
- monitor negative public events for counterparties,
- assess repayment-risk signals from legal/news/registry/public sources,
- produce an evidence workbook with raw and deduplicated records,
- generate structured JSON summaries and concise warning messages.

## Input Schema

Accept input in this shape:

```json
{
  "companies": [
    {
      "company_name": "BRAVADO LIMITED",
      "jurisdiction": "UK",
      "company_number": "01584795",
      "aliases": []
    }
  ],
  "search_window_days": 180,
  "language": "en"
}
```

Required:
- `companies[].company_name`

Optional:
- `companies[].jurisdiction`
- `companies[].company_number`
- `companies[].aliases`
- `search_window_days`
- `language`

## Workflow Decision Tree

1. Layer 1 retrieval and evidence logging always runs first.
2. Layer 2 extraction and classification runs on logged evidence.
3. Never discard Layer 1 evidence, even when low relevance.
4. Only Layer 2 summaries are sent to warning channels.

## Layer 1: Taxonomy-Guided Retrieval And Logging

### Goal

Use the taxonomy.md as the retrieval backbone to maximize recall of public negative signals relevant to repayment risk.

For each company, Layer 1 should:
1. use the taxonomy as the search anchor,
2. expand each risk signal into slightly generalized public wording,
3. search across registry, legal, news, and company-announcement sources,
4. preserve all retrieved evidence with full traceability.

Do not search only the literal taxonomy labels.

Examples:
- `liquidation` → `winding up`, `administration`, `insolvency notice`
- `new charge` → `registered charge`, `debenture`, `new facility`
- `shutdown` → `ceased trading`, `operations suspended`, `business closure`

### Retrieval Rule

For each company and each taxonomy category, generate 2–3 search variants:
- exact risk term
- generalized public wording
- source-targeted query where relevant

Examples:
- `"<company> liquidation OR winding up"`
- `"<company> charge OR debenture OR refinancing"`
- `site:gov.uk "<company>" insolvency`
- `site:thegazette.co.uk "<company>" petition`

Use jurisdiction-specific public sources when jurisdiction is available.

Examples:
- UK: Companies House, Gazette, gov.uk notices
- HK: Companies Registry, HKEX announcements, Gazette
- SG: ACRA, SGX announcements, Gazette
- US: SEC filings, state business registry, Chapter 11 notices
- CN: National Enterprise Credit Information Publicity System, court announcements, exchange filings
- Global: Reuters, Bloomberg, company press releases, major news websites

If jurisdiction is unavailable, prioritize global news and company announcements.

### Logging Rule

Keep every retrieved record in `raw_evidence`, even if relevance is uncertain.

Each row must include:
- `company_name`
- `taxonomy_category`
- `taxonomy_seed_signal`
- `search_query`
- `source_website`
- `title`
- `publish_date`
- `url`
- `snippet`
- `raw_text`
- `initial_relevance`
- `retrieval_timestamp`
- `dedup_key`

### Deduplication Rule

Within the same company, duplicate articles / filings referring to the same underlying event must be deduplicated in `deduped_events`.

Deduplication applies only within the same company.

Deduplication key:
`company_name + normalized_title + publish_date + source_website`

Rules:
- keep all rows in `raw_evidence`
- keep only one row per event in `deduped_events`
- populate `source_count`
- retain matched queries in `support_queries`

If the same article mentions multiple monitored companies, keep one record for each company.

### Excel Output Rule

Layer 1 must generate exactly one Excel workbook for each monitoring run.

File name:
`negative_event_monitoring_<run_date>.xlsx`

Example:
`negative_event_monitoring_20260409.xlsx`

Workbook sheets:
- `raw_evidence`
- `deduped_events`
- `run_summary`

## Layer 2: Classification And Summary

### Goal

Convert logged evidence into structured risk intelligence.

### Processing Steps

1. Extract factual event statements.
3. Classify event into the taxonomy.
4. Assign `severity` (`Low`, `Medium`, `High`).
5. Assign `signal_stage` (`early_warning`, `pre_default`, `default`).
6. Generate per-company structured summary and alert text.

### Taxonomy

(See `references/taxonomy.md`.)

## Output Contract

For each monitoring run, produce:
1. Excel evidence workbook (all companies, all Layer 1 evidence retained).
2. Structured JSON summary file:
- `negative_event_summary_YYYYMMDD.json` or `negative_event_summary_{run_id}.json`
3. Alert-ready concise text per company.

Chat Output Rules
When triggered from chatbox like Slack/Codex mention like @codex:
- send final result back to the same Slack or chatbox thread
- message body contains only alert related text
- attach exactly one file: the generated xlsx workbook
- do not include any other sections
Alert text template:

```text
[Company] <company_name>
Risk Level: <overall_risk_level>
Key Signals: <signal_1>; <signal_2>; <signal_3>
Implication: <risk_implication>
Source Websites: <site_1>; <site_2>
```

## Operating Rules

- Keep taxonomy stable across runs for consistent downstream scoring.
- Keep retrieval (Layer 1) and classification (Layer 2) logically separated.
- Do not post raw evidence directly to warning groups.
- Preserve and export all raw evidence for audit and review.
- If relevance is uncertain, keep the record and lower `initial_relevance`; do not drop it.
