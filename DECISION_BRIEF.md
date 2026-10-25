# E-commerce merchandising and market diagnostic

## Decision

Use the saved category summaries to prioritize margin and availability checks, and repair customer attribution before customer-level work. Do not reallocate city spend from this view: the Top 10 cities are closely grouped, and the rest of the city universe is not shown.

## Four business questions

| Business question | Evidence-based answer | Practical next step |
|---|---|---|
| Is the category sales mix concentrated? | Top three categories (Confections, Meat, Poultry) = **34.39%** of 4.466B source units. | Compare category contribution margin, stock-outs, and repeat orders before prioritizing spend. |
| How far apart are the category leader and smallest category? | Confections **574.1M** vs Shell fish **308.8M**; leader is **1.86×** the smallest, a **265.3M** gap. | Review assortment breadth, margin, promotion exposure, and availability. Sales alone do not explain the gap. |
| Are the displayed Top 10 cities clearly separated? | **48.09M–49.99M**; range equals **3.88%** of their mean. | Do not treat the rank order as a city opportunity ranking. Add all cities, dates, customer base, acquisition costs, and margin. |
| Is customer attribution ready for CRM analysis? | Blank customer bucket **11.42M**, approximately **0.256%** of category sales. | Trace blank customer keys and quantify affected orders; recompute using consistent order-level denominator. |

## Data needed to approve a commercial test

- Verified sales definition, currency, date range, and net/gross treatment.
- Cost, discounts, returns, cancellations, shipping, and contribution margin.
- Order count, monthly trend, average order value, repeat rate, and inventory availability.
- Full city population, eligible customer base, acquisition cost, and campaign exposure.
- Validated product/category and customer keys; a holdout/control flag for any test.

## Limitations

This analysis uses saved aggregate PivotTable values because the workbook's embedded Data Model rows were not queryable in this environment. No transaction-level analysis was performed. The city view includes only the saved Top 10. Currency and time period are unspecified. The blank customer bucket comes from a separate saved summary, so its share is approximate until recalculated at consistent grain. These results describe sales mix, not profit, growth, customer value, or causal lift.
