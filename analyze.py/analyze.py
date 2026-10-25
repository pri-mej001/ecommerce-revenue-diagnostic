#!/usr/bin/env python3
"""Rebuild the aggregate e-commerce diagnostic using only Python's stdlib."""
from __future__ import annotations
import csv
import json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data"
OUT=ROOT/"analysis"
def load_rows(filename,label_column):
    with (DATA/filename).open("r",encoding="utf-8-sig",newline="") as handle:
        rows=[{label_column:row[label_column],"sales_source_units":Decimal(row["sales_source_units"])} for row in csv.DictReader(handle)]
    if not rows: raise ValueError(f"No data rows found in {filename}")
    if len({str(row[label_column]) for row in rows})!=len(rows): raise ValueError(f"Duplicate {label_column} values in {filename}")
    if any(row["sales_source_units"]<0 for row in rows): raise ValueError(f"Negative sales found in {filename}; inspect before interpreting")
    return rows
def dec_string(value,places=4): return f"{value:.{places}f}"
def make_bar_svg(rows,label_column,title,filename):
    width,left,right,top,row_h=960,190,100,82,42
    height=top+row_h*len(rows)+34
    max_value=max(Decimal(row["sales_source_units"]) for row in rows)
    plot_w=width-left-right; unit=Decimal(1000000); max_scaled=max_value/unit; bar_h=22
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img">','<style>text{font-family:Arial,Helvetica,sans-serif;fill:#17233b}.title{font-size:23px;font-weight:700}.subtitle{font-size:13px;fill:#5e6c84}.label{font-size:14px}.value{font-size:13px;fill:#344563}.bar{fill:#1877a8}.grid{stroke:#e5eaf0;stroke-width:1}</style>',f'<text class="title" x="{left}" y="32">{title}</text>',f'<text class="subtitle" x="{left}" y="55">Saved workbook summary; source units; currency and period unspecified</text>']
    for tick in range(5):
        x=left+int(plot_w*tick/4); val=max_scaled*Decimal(tick)/Decimal(4)
        parts += [f'<line class="grid" x1="{x}" y1="{top-10}" x2="{x}" y2="{top+row_h*len(rows)-8}"/>',f'<text class="subtitle" text-anchor="middle" x="{x}" y="{top+row_h*len(rows)+12}">{val:.0f}m</text>']
    for idx,row in enumerate(rows):
        y=top+idx*row_h; label=str(row[label_column]); scaled=Decimal(row["sales_source_units"])/unit; bar_width=int(plot_w*float(scaled/max_scaled))
        parts += [f'<text class="label" text-anchor="end" x="{left-12}" y="{y+16}">{label}</text>',f'<rect class="bar" x="{left}" y="{y}" width="{bar_width}" height="{bar_h}" rx="3"/>',f'<text class="value" x="{left+bar_width+9}" y="{y+16}">{scaled:,.2f}m</text>']
    parts.append("</svg>"); (OUT/filename).write_text("\n".join(parts),encoding="utf-8")
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    categories=load_rows("category_sales.csv","category"); cities=load_rows("top10_city_sales.csv","city")
    categories.sort(key=lambda r:Decimal(r["sales_source_units"]),reverse=True)
    total=sum((Decimal(r["sales_source_units"]) for r in categories),Decimal(0)); top3=sum((Decimal(r["sales_source_units"]) for r in categories[:3]),Decimal(0))
    city_values=[Decimal(r["sales_source_units"]) for r in cities]; mean=sum(city_values,Decimal(0))/Decimal(len(cities)); low=min(city_values); high=max(city_values); blank=Decimal("11415763.1766")
    summary={"scope":"Saved aggregate PivotTable summaries only","units":"source sales units; currency and period unspecified","category_count":len(categories),"category_sales_total":dec_string(total),"top_three_categories":[{"category":r["category"],"sales_source_units":dec_string(Decimal(r["sales_source_units"]))} for r in categories[:3]],"top_three_share_pct":dec_string(top3/total*100,2),"top10_city_count":len(cities),"top10_city_min_sales":dec_string(low),"top10_city_max_sales":dec_string(high),"top10_city_relative_range_pct":dec_string((high-low)/mean*100,2),"blank_customer_bucket_sales":dec_string(blank),"blank_customer_share_of_category_total_pct_approx":dec_string(blank/total*100,3),"limitations":["No transaction-level rows available","Currency and reporting period unspecified","City file contains only displayed Top 10","Customer bucket is from a separate PivotTable and should be recalculated at a consistent grain"]}
    (OUT/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    make_bar_svg(categories,"category","Sales by category","category_mix.svg"); make_bar_svg(cities,"city","Sales in displayed Top 10 cities","top10_city_sales.svg")
    print(f"Category sales total: {total:.4f} source units"); print(f"Top-three category share: {summary['top_three_share_pct']}%"); print(f"Top-10 city range: {low:.2f}–{high:.2f} source units"); print("Generated analysis/summary.json and SVG charts.")
if __name__=="__main__": main()
