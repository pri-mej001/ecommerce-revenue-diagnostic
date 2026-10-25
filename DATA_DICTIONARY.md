# Data dictionary and metric rules

## Category aggregate (`data/category_sales.csv`)

| Field | Type | Definition |
|---|---|---|
| `category` | text | Category label shown in the workbook's saved category PivotTable |
| `sales_source_units` | decimal | Saved PivotTable value for the workbook's `Total Sales` measure; currency and period are not identified |

## City aggregate (`data/top10_city_sales.csv`)

| Field | Type | Definition |
|---|---|---|
| `city` | text | City label shown in the workbook's saved Top 10 city PivotTable |
| `sales_source_units` | decimal | Saved PivotTable value; only the displayed top ten cities are included |

## Metrics

- **Category total:** Sum of all 11 category values in the saved summary. This is the denominator for category shares.
- **Category share:** Category sales divided by category total.
- **Top-three share:** Sum of the three largest category values divided by category total. This is a mix/concentration descriptor, not a performance target.
- **Top-10 city spread:** Maximum minus minimum among only the ten displayed cities. Relative spread is this difference divided by their mean.
- **Blank customer share:** 11,415,763.1766 source units in the saved customer summary's blank bucket divided by the category total. This is approximate and must be recomputed from the model at a consistent grain before remediation sizing.

## Source and quality

The source workbook contains seven Power Query connections (`categories`, `cities`, `countries`, `customers`, `employees`, `products`, `sales`) and an embedded Data Model. This project includes only two saved summary extracts. It does not include customer-level records, employee names, transaction data, source-system credentials, or the complete dimension tables.

The total categories in the saved pivot is 4,466,259,165.5233; summing its displayed category rows gives 4,466,259,165.5234, with a tiny floating-point rounding difference. The category values are sorted descending. The Top 10 city subtotal reconciles to its ten displayed values within rounding.

Currency, date range, customer-count denominator, gross/net definition, margin, order count, return status, and full city universe are not available in these extracts.
