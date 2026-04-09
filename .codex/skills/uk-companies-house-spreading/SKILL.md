---
name: uk-companies-house-spreading
description: Read UK Companies House financial-statement PDFs, extract and reconcile key line items, and populate a standardized Excel spreading workbook with audit trail and review flags.
---

# UK Companies House Financial Spreading

## Overview

This skill transforms an unstructured UK Companies House financial statement PDF into an analyst-reviewable spreading workbook.

Core responsibilities:
1. OCR and parse the statement.
2. Extract relevant line items with source trace.
3. Map values into a standard template.
4. Run reconciliation and quality checks.
5. Output a completed workbook with review-ready logs.

Principles:
- Be conservative.
- Prefer transparency over false precision.
- Do not fabricate values.
- Leave unsupported fields blank and flag them.

## When To Use

Use this skill when the user asks to:
- spread UK Companies House financials from PDF into an Excel template,
- extract two-year financial values (current and prior year),
- produce traceable mapping and validation evidence,
- prepare an analyst-ready workbook with manual-review cues.

## Inputs

Expected inputs:
1. One UK Companies House financial statement PDF.
2. One Excel spreading template workbook.

Optional context:
- preferred output file name,
- explicit year mapping guidance,
- known currency/unit basis if the PDF is unclear.

## Output Contract

Primary output:
1. One populated workbook based on the input template.

Required workbook content:
1. Main template sheet:
- preserve label structure exactly as template-defined,
- write current year and prior year values to designated value columns,
- do not overwrite unrelated labels/formulas/cells.
2. Raw_Extraction sheet:
- extracted label,
- extracted value,
- reporting year,
- source section,
- page or note reference,
- confidence,
- mapping decision,
- comments.
3. Validation_Log sheet:
- mapping checks,
- duplication checks,
- arithmetic checks,
- year-alignment checks,
- OCR anomaly flags,
- unit-basis flags,
- manual review triggers.
4. Metadata sheet:
- company name,
- reporting period end,
- prior year end,
- currency,
- unit basis,
- source PDF name,
- extraction timestamp,
- overall reliability (High / Medium / Low),
- summary notes.
5. Review_Summary sheet:
- extraction outcome,
- key unresolved questions,
- material validation flags,
- assumptions used,
- manual review priorities,
- overall assessment.

Secondary output (chat summary):
- extraction status,
- workbook population status,
- major unresolved issues,
- reliability rating,
- manual-review requirement.

If full population fails:
- still provide a structured failure summary,
- include partial extraction results when available,
- never fail silently.

## Workflow

Follow this sequence:

1. OCR and document understanding:
- identify company name, reporting period, year columns, currency, unit basis,
- identify major sections (P&L, balance sheet, notes).
2. Raw extraction:
- capture all relevant line items before final mapping,
- include supporting notes (debtors, creditors, lease, D&A, tax, borrowings).
3. Standard field mapping:
- map source labels into template fields using explicit rule precedence.
4. Validation and reconciliation:
- run mapping, duplication, year-alignment, arithmetic, and OCR checks.
5. Workbook population:
- write only supported values,
- keep unsupported fields blank,
- tag whether each value is reported, derived, remapped, or unresolved.
6. Final review packaging:
- complete Validation_Log, Metadata, and Review_Summary.

## Standard Field Set

Income statement fields:
- Net Sales
- Other Income
- Total Revenue
- Cost of Goods Sold (COGS)
- Gross Profit
- SG&A Expenses
- Other Expenses
- Total Operating Expenses
- EBITDA
- Depreciation & Amortization
- Operating Income (EBIT)
- Interest Income
- Interest Expense
- Gain/Loss on Asset Sales
- Other Non-Operating Items
- Net Other Income / (Expenses)
- Income Before Tax
- Income Tax Expense
- Net Income

Balance sheet fields:
- Cash and Cash Equivalents
- Accounts Receivable
- Inventory
- Prepaid Expenses
- Other Current Assets
- Total Current Assets
- PP&E
- Accumulated Depreciation
- Goodwill
- Other Intangible Assets
- Long term investment
- Other Long-Term Assets
- Operating lease right of use asset
- Total Non-Current Assets
- Total Assets
- Accounts Payable
- Accrued Expenses
- Short-Term Loans
- Current Portion of Long-Term Debt
- Current Portion of Lease Liabilities
- Amounts due to related parties (current)
- Taxes Payable
- Short term provisions
- Other Current Liabilities
- Total Current Liabilities
- Provision
- Long-Term Debt
- Deferred Tax
- Lease Liabilities
- Amounts due to related parties (non-current)
- Other Long-Term Liabilities
- Total Non-Current Liabilities
- Total Liabilities
- Common Stock
- Retained Earnings
- Others
- Total Equity
- Total Liabilities and Equity

## Mapping Rules (Core)

1. Prefer direct disclosed values over derived values.
2. Use notes when primary statements are aggregated.
3. Use residual balancing only when unavoidable and log it.
4. Never use residual balancing for headline fields unless unavoidable:
- Net Sales
- EBITDA
- EBIT
- Net Income
- Cash
- Total Assets
- Total Liabilities
- Total Equity
5. For each populated field, set status:
- reported
- derived
- remapped
- unresolved

Common label mappings:
- Revenue/Turnover/Sales -> Net Sales
- Other operating income -> Other Income
- Cost of sales -> COGS
- Operating profit/(loss) -> EBIT
- Profit before taxation -> Income Before Tax
- Tax on profit -> Income Tax Expense
- Profit for the financial year -> Net Income
- Cash at bank and in hand -> Cash and Cash Equivalents
- Trade debtors/receivables -> Accounts Receivable
- Prepayments/accrued income -> Prepaid Expenses
- Tangible assets -> PP&E
- Trade creditors/payables -> Accounts Payable
- Accruals -> Accrued Expenses
- Called up share capital/share capital -> Common Stock
- Profit and loss account/retained earnings -> Retained Earnings

Residual logic examples:
- Other Current Assets = Total Current Assets - cash - AR - inventory - prepaid.
- Other Current Liabilities = Total Current Liabilities - identified current liability components.
- Other Long-Term Liabilities = Total Non-Current Liabilities - identified non-current components.

## Validation Rules

1. Mapping validation:
- avoid mapping subtotals into detail fields,
- avoid mapping net assets as total assets,
- avoid using total debtors as AR if a breakdown exists.
2. Duplication checks:
- remove double counting across debtors/creditors/admin expense/operating profit mappings.
3. Year alignment:
- confirm current/prior year column consistency across statements and notes.
4. Arithmetic checks:
- Gross Profit = Total Revenue - COGS
- Total Operating Expenses = SG&A + Other Expenses
- EBITDA = EBIT + D&A
- Net Income = Income Before Tax - Tax
- Total Assets = Total Current Assets + Total Non-Current Assets
- Total Liabilities = Total Current Liabilities + Total Non-Current Liabilities
- Total Liabilities and Equity = Total Liabilities + Total Equity
- Total Assets = Total Liabilities and Equity
5. Tolerance:
- <=1% mismatch: minor mismatch
- >1% mismatch: material mismatch
- scaling anomalies: possible unit mismatch
6. OCR anomaly detection:
- missing negatives,
- wrong year capture,
- character confusion (1 vs I, 0 vs O),
- bracketed negatives missed,
- decimal shifts.

## Excel Population Rules

1. Keep template labels unchanged.
2. Write current year and prior year into designated value columns.
3. Keep unsupported fields blank (do not force zero).
4. If one year is unreliable, populate only the reliable year and leave the other blank.
5. Preserve template formulas/structure whenever present.

## Stop And Request Manual Review

Stop automated completion and mark manual review required when any material condition applies:
- unreadable PDF or poor OCR preventing reliable table parsing,
- ambiguous source/template selection,
- workbook protection/corruption or unsafe write target,
- unresolved year alignment ambiguity,
- material mapping uncertainty for headline fields,
- material arithmetic failures that cannot be reconciled,
- likely OCR corruption affecting sign/scale/decimals,
- insufficient data for meaningful spreading.

If stop condition is triggered:
1. Populate only clearly supported values.
2. Leave uncertain values blank.
3. Record reasons in Validation_Log, Review_Summary, and Metadata.
4. Set overall reliability to Medium or Low.
5. If workbook is still generated, append REVIEW REQUIRED in output name.

## Final Deliverable Criteria

The output is acceptable only if:
1. Workbook is structurally usable for analyst review.
2. Raw extraction trail is visible.
3. Validation outcomes are explicit and traceable.
4. Assumptions are clearly stated.
5. Material uncertainty is flagged, not hidden.
