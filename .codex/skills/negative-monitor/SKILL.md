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

## Layer 1: Retrieval And Logging

### Goal

For each company, query public sources and store every retrieved finding with source traceability.

### Retrieval Scope

Search at least:
- insolvency and legal notices,
- company registry filings,
- major news sites,
- company announcements,
- public social / press-release pages,
- court / petition / liquidation sites when available.

### Query Groups

Use these query groups:
- `legal_insolvency`
- `creditor_action`
- `liquidity_stress`
- `financial_reporting_stress`
- `operational_shutdown`
- `commercial_stress`
- `governance_fraud`
- `adverse_media`

Example patterns:
- `"<company> liquidation OR insolvency OR winding up"`
- `"<company> creditors meeting OR statutory demand"`
- `"<company> charge OR debenture OR secured borrowing"`
- `"<company> accounts overdue OR late filing"`
- `"<company> ceased trading OR business closure"`
- `"<company> penalty OR set-off OR dispute"`

### Required Raw Evidence Fields

Store each retrieved item as one row in `raw_evidence` with:
- `run_id`
- `company_name`
- `jurisdiction`
- `company_number`
- `query_group`
- `search_query`
- `source_website`
- `source_type`
- `title`
- `event_date`
- `publish_date`
- `url`
- `snippet`
- `raw_text`
- `language`
- `initial_relevance`
- `initial_risk_hint`
- `retrieval_timestamp`
- `dedup_key`

Mandatory rule:
- `source_website` must always be populated as a dedicated field.

### Layer 1 Excel Output

Export one workbook for all companies:
- `negative_event_monitoring_YYYYMMDD.xlsx` or `negative_event_monitoring_{run_id}.xlsx`

Workbook sheets:
- `raw_evidence`: full row-level evidence log.
- `deduped_events`: deduplicated candidate events.
- `run_summary`: per-company summary stats.

`run_summary` must include:
- number of raw hits,
- number of deduplicated events,
- number of high-risk events,
- latest event date,
- highest severity.

`deduped_events` fields:
- `run_id`
- `company_name`
- `event_cluster_id`
- `normalized_event`
- `category`
- `severity`
- `signal_stage`
- `event_date`
- `first_seen_date`
- `source_count`
- `source_websites`
- `support_urls`
- `evidence_summary`

## Layer 2: Classification And Summary

### Goal

Convert logged evidence into structured risk intelligence.

### Processing Steps

1. Deduplicate overlapping reports for the same underlying event.
2. Extract factual event statements.
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

Additionally, in the final assistant message (chat output):
- Paste the full alert-ready text (the contents that would be written to the `.txt` summary) directly in the message.
- Provide the Excel workbook path and JSON path.
- Provide a small human-readable preview table:
  - `run_summary` (all rows).
  - Top 10 rows of `deduped_events` (sorted by severity desc, then event_date desc when available).
  - Top 10 rows of `raw_evidence` (include `source_website`, `title`, `url`, `publish_date`, `initial_relevance`).
- Do not paste the full raw evidence dataset into chat (it can be large); only preview and point to the workbook.

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
