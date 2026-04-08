# Taxonomy

- `Legal / Insolvency`: liquidation, bankruptcy, winding-up, insolvency filing -> `High`
- `Legal / Insolvency`: creditors meeting, statutory demand, winding-up petition -> `High`
- `Liquidity Stress`: new charge, secured borrowing, refinancing, bridge financing -> `Medium`
- `Liquidity Stress`: tax arrears, payroll delay, HMRC petition -> `High`
- `Financial Reporting Stress`: overdue accounts, late filing, audit delay -> `Low` or `Medium`
- `Financial Reporting Stress`: going concern warning, material uncertainty -> `High`
- `Operational Shutdown`: ceased trading, shutdown, closure, factory suspension -> `High`
- `Commercial Stress`: major customer loss, contract termination, order cancellation -> `Medium`
- `Commercial Stress`: penalty, set-off, deduction, receivable dispute -> `High`
- `Governance / Fraud`: fraud investigation, sanctions, audit qualification -> `Medium` or `High`
- `Market / Reputation`: lawsuit, product recall, adverse media -> `Low` or `Medium`

## Severity Rules

- `Low`: weak early warning, not yet directly tied to repayment default.
- `Medium`: clear stress signal likely impacting liquidity, revenue, or willingness to pay.
- `High`: strong default/shutdown/legal-action evidence, or material receivable impairment.

## Signal Stage Rules

- `early_warning`: early stress signals (example: new charge).
- `pre_default`: escalated distress with probable default trajectory (example: creditors meeting).
- `default`: formal insolvency/default state (example: liquidation).
