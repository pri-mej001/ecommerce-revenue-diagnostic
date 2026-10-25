-- Run from the project root with the SQLite command-line tool:
--   sqlite3 ecommerce.db < sql/analysis.sql
-- This uses sqlite3 shell directives (.import), not server-side SQL syntax.

.bail on
DROP TABLE IF EXISTS category_sales;
DROP TABLE IF EXISTS top10_city_sales;

CREATE TABLE category_sales (
    category TEXT PRIMARY KEY,
    sales_source_units REAL NOT NULL CHECK (sales_source_units >= 0)
);

CREATE TABLE top10_city_sales (
    city TEXT PRIMARY KEY,
    sales_source_units REAL NOT NULL CHECK (sales_source_units >= 0)
);

.mode csv
.import --skip 1 data/category_sales.csv category_sales
.import --skip 1 data/top10_city_sales.csv top10_city_sales

-- 1) Category sales mix and cumulative share
WITH category_mix AS (
    SELECT
        category,
        sales_source_units,
        sales_source_units / SUM(sales_source_units) OVER () AS share_of_category_total,
        ROW_NUMBER() OVER (ORDER BY sales_source_units DESC) AS sales_rank
    FROM category_sales
)
SELECT
    category,
    ROUND(sales_source_units, 2) AS sales_source_units,
    ROUND(100.0 * share_of_category_total, 2) AS share_pct,
    sales_rank
FROM category_mix
ORDER BY sales_rank;

-- 2) Top-three category share
WITH ranked AS (
    SELECT sales_source_units,
           ROW_NUMBER() OVER (ORDER BY sales_source_units DESC) AS rn
    FROM category_sales
)
SELECT ROUND(100.0 * SUM(CASE WHEN rn <= 3 THEN sales_source_units ELSE 0 END)
                  / SUM(sales_source_units), 2) AS top_three_share_pct
FROM ranked;

-- 3) Spread among the displayed Top 10 cities only (not the full city universe)
SELECT
    ROUND(MIN(sales_source_units), 2) AS min_top10_city_sales,
    ROUND(MAX(sales_source_units), 2) AS max_top10_city_sales,
    ROUND(100.0 * (MAX(sales_source_units) - MIN(sales_source_units))
                 / AVG(sales_source_units), 2) AS relative_range_pct
FROM top10_city_sales;

-- 4) Customer attribution figure from a separate saved PivotTable.
-- This value is disclosed as a parameter because the underlying customer rows
-- are not included in this aggregate-only project.
SELECT
    11415763.1766 AS blank_customer_bucket_sales_source_units,
    ROUND(100.0 * 11415763.1766 / SUM(sales_source_units), 3)
        AS approximate_share_of_category_total_pct
FROM category_sales;
