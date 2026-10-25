# Decision brief: protect decision quality before moving budget

## Decision question
Which categories and cities lead in reported sales, and are these summaries sufficient to guide merchandising or local-market investment?

## Answer
The summaries show where to investigate next, but do not support a budget shift. The workbook’s saved summaries lack verified currency, reporting period, profit, cost, returns, and the full city population. Revenue alone cannot establish growth or profitability.

## Evidence

| Signal | Result | What it supports |
|---|---:|---|
| Reported sales across 11 categories | 4.466 billion source units | Category baseline, subject to measure and period validation |
| Top three categories | 34.4% of category total | Shortlist for deeper margin analysis |
| Displayed Top 10 city range | 48.09m–49.99m source units | Cities in this subset are closely grouped |
| Blank customer bucket | 11.42m source units, about 0.26% | Customer attribution needs validation |

No claim is made that the top categories are most profitable, top cities are best growth markets, or a mapping defect is confirmed.

## Action plan
1. Validate product and customer keys, duplicate IDs, nulls, and measure reconciliation. Recalculate the blank-customer share from order-level data.
2. Document date range, currency, gross/net definition, discounts, tax, refunds, and the precise sales measure.
3. Add margin, order count, average order value, repeat purchase, inventory/stock-outs, and monthly trends.
4. Test a category or city intervention only after validation. Measure incremental contribution margin against a holdout group, with return and stock guardrails.

## Data needed next
Order and order-line IDs, order date/status, product and category keys, quantity, price, discounts, cost, pseudonymized customer ID, channel, geography, returns/refunds/cancellations, shipping, inventory, campaign exposure, and test/control assignment.

## Limitations
This is an aggregate analysis of saved PivotTable results. The embedded Data Model rows could not be queried in this environment. Currency and reporting period are unspecified; the city summary is Top 10 only; product/category examples are validation flags, not confirmed defects. These are next-step recommendations, not an uplift estimate.
