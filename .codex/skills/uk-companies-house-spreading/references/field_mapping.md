# Field Mapping Reference

This document is a structured mapping reference for the skill `uk-companies-house-spreading`.

## Income Statement Mapping

| Template Field | Primary Source Labels | Notes |
|---|---|---|
| Net Sales | Turnover; Revenue; Sales | Prefer disclosed value. |
| Other Income | Other operating income | Keep separate from Net Sales. |
| Total Revenue | Disclosed total revenue | Else derive: Net Sales + Other Income. |
| Cost of Goods Sold (COGS) | Cost of sales | |
| Gross Profit | Gross profit | Else derive: Total Revenue - COGS. |
| SG&A Expenses | Selling and distribution costs; Administrative expenses | Sum if both exist. |
| Other Expenses | Impairment; Exceptional items; Restructuring; Auditor fees | Exclude items already in SG&A. |
| Total Operating Expenses | Operating expenses subtotal | Else derive: SG&A + Other Expenses. |
| Depreciation & Amortization | Depreciation note; Amortisation note | Avoid double counting in SG&A. |
| EBITDA | EBITDA if disclosed | Else derive: EBIT + D&A. |
| Operating Income (EBIT) | Operating profit/(loss) | |
| Interest Income | Interest receivable and similar income | |
| Interest Expense | Interest payable and similar charges; Finance costs | |
| Gain/Loss on Asset Sales | Gain/loss on disposal | Map only if explicit. |
| Other Non-Operating Items | Other non-operating lines | Exclude interest and disposal lines. |
| Net Other Income / (Expenses) | Non-operating subtotal | Else derive from components. |
| Income Before Tax | Profit before taxation | |
| Income Tax Expense | Tax on profit | |
| Net Income | Profit for the financial year | |

## Balance Sheet Mapping

| Template Field | Primary Source Labels | Notes |
|---|---|---|
| Cash and Cash Equivalents | Cash at bank and in hand | |
| Accounts Receivable | Trade debtors; Trade receivables | Prefer note breakdown if available. |
| Inventory | Stocks; Inventory | |
| Prepaid Expenses | Prepayments; Accrued income | |
| Other Current Assets | Residual | TCA - Cash - AR - Inventory - Prepaid. |
| Total Current Assets | Current assets total | |
| PP&E | Tangible assets | |
| Accumulated Depreciation | Accumulated depreciation | Map only if explicit. |
| Goodwill | Goodwill | |
| Other Intangible Assets | Intangible assets (ex-goodwill) | |
| Long term investment | Fixed asset investments; Investments in subsidiaries/associates | |
| Operating lease right of use asset | Right-of-use asset; Lease asset | |
| Other Long-Term Assets | Residual | TNCA minus identified non-current assets. |
| Total Non-Current Assets | Fixed assets total; Non-current assets total | |
| Total Assets | Total assets | |
| Accounts Payable | Trade creditors; Trade payables | Prefer due-within-one-year note detail. |
| Accrued Expenses | Accruals; Accrued liabilities | |
| Short-Term Loans | Bank loans due <1y; Overdrafts; Borrowings due <1y | |
| Current Portion of Long-Term Debt | Debt due within one year | Use only when distinguishable. |
| Current Portion of Lease Liabilities | Lease liabilities due <1y; Finance lease obligations <1y | |
| Amounts due to related parties (current) | Amounts owed to group undertakings <1y; Director/related party loans <1y | |
| Taxes Payable | Corporation tax payable; Taxation and social security | |
| Short term provisions | Short-term provisions | |
| Other Current Liabilities | Residual | TCL minus identified current liabilities. |
| Total Current Liabilities | Creditors: amounts falling due within one year | |
| Provision | Provisions for liabilities | Usually non-current unless split provided. |
| Long-Term Debt | Bank loans due >1y; Borrowings due >1y | |
| Deferred Tax | Deferred tax liabilities | |
| Lease Liabilities | Lease liabilities due >1y; Finance lease obligations >1y | |
| Amounts due to related parties (non-current) | Group/director/related party loans due >1y | |
| Other Long-Term Liabilities | Residual | TNCL minus identified non-current liabilities. |
| Total Non-Current Liabilities | Creditors due >1y plus provisions | Prefer disclosed total if explicit. |
| Total Liabilities | Total liabilities | Else derive TCL + TNCL. |
| Common Stock | Called up share capital; Share capital | |
| Retained Earnings | Profit and loss account; Retained earnings | |
| Others | Other reserves; Revaluation reserve; Merger reserve; Translation reserve | |
| Total Equity | Total equity; Net assets | |
| Total Liabilities and Equity | Total liabilities and equity | Must match Total Assets. |

## Derivation Priority

1. Reported value from primary statement.
2. Reported value from note disclosure.
3. Arithmetic derivation from reliable components.
4. Residual balancing (last resort, always flagged).

## Mandatory Traceability

For every populated field, capture status:
- `reported`
- `derived`
- `remapped`
- `unresolved`

Also record supporting reference:
- source section
- source label
- year
- page/note reference
- confidence

## Validation Focus

- Year alignment must be consistent between statement and notes.
- Duplication must be removed (especially debtors/creditors rollups).
- Headline fields should not rely on residual logic unless unavoidable.
- Material mismatches and OCR anomalies must be escalated to manual review.
