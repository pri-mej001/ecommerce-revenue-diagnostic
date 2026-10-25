-- Run from the project root with SQLite CLI: sqlite3 ecommerce.db < sql/analysis.sql
-- The .import commands below are sqlite3 shell directives.
.bail on
DROP TABLE IF EXISTS category_sales;
DROP TABLE IF EXISTS top10_city_sales;
CREATE TABLE category_sales(category TEXT PRIMARY KEY,sales_source_units REAL NOT NULL CHECK(sales_source_units>=0));
CREATE TABLE top10_city_sales(city TEXT PRIMARY KEY,sales_source_units REAL NOT NULL CHECK(sales_source_units>=0));
.mode csv
.import --skip 1 data/category_sales.csv category_sales
.import --skip 1 data/top10_city_sales.csv top10_city_sales

-- Category mix and rank
WITH category_mix AS (SELECT category,sales_source_units,sales_source_units/SUM(sales_source_units) OVER() AS share,ROW_NUMBER() OVER(ORDER BY sales_source_units DESC) AS sales_rank FROM category_sales)
SELECT category,ROUND(sales_source_units,2) AS sales_source_units,ROUND(100*share,2) AS share_pct,sales_rank FROM category_mix ORDER BY sales_rank;

-- Top-three category share
WITH ranked AS (SELECT sales_source_units,ROW_NUMBER() OVER(ORDER BY sales_source_units DESC) AS rn FROM category_sales)
SELECT ROUND(100*SUM(CASE WHEN rn<=3 THEN sales_source_units ELSE 0 END)/SUM(sales_source_units),2) AS top_three_share_pct FROM ranked;

-- Spread among the workbook's displayed Top 10 cities only
SELECT ROUND(MIN(sales_source_units),2) AS min_top10_city_sales,ROUND(MAX(sales_source_units),2) AS max_top10_city_sales,ROUND(100*(MAX(sales_source_units)-MIN(sales_source_units))/AVG(sales_source_units),2) AS relative_range_pct FROM top10_city_sales;

-- Blank-customer value is from a separate saved PivotTable; recompute at a consistent grain before remediation.
SELECT 11415763.1766 AS blank_customer_bucket_sales_source_units,ROUND(100*11415763.1766/SUM(sales_source_units),3) AS approximate_share_of_category_total_pct FROM category_sales;
