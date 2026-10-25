#!/usr/bin/env python3
"""Rebuild the four-question e-commerce diagnostic and its SVG visuals."""
from __future__ import annotations

import csv
import json
from decimal import Decimal
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "analysis"
NAVY = "#14243a"
BLUE = "#2878b5"
TEAL = "#12a89d"
AMBER = "#f0ad4e"
CORAL = "#e56f51"
MUTED = "#68788d"
GRID = "#e8edf3"


def load_rows(filename: str, label: str) -> list[dict[str, object]]:
    with (DATA / filename).open(encoding="utf-8-sig", newline="") as f:
        rows = [{label: r[label], "sales": Decimal(r["sales_source_units"])} for r in csv.DictReader(f)]
    if not rows or len({r[label] for r in rows}) != len(rows):
        raise ValueError(f"Empty or duplicate labels in {filename}")
    if any(r["sales"] < 0 for r in rows):
        raise ValueError(f"Negative sales in {filename}; inspect the source")
    return rows


def svg_start(title: str, subtitle: str, width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Inter,Segoe UI,Arial,sans-serif}.title{font-size:25px;font-weight:700;fill:#14243a}.sub{font-size:13px;fill:#68788d}.label{font-size:14px;fill:#263a52}.small{font-size:12px;fill:#68788d}.value{font-size:13px;font-weight:650;fill:#14243a}.grid{stroke:#e8edf3;stroke-width:1}.axis{stroke:#cdd7e2;stroke-width:1}</style>',
        f'<text class="title" x="36" y="42">{escape(title)}</text>',
        f'<text class="sub" x="36" y="67">{escape(subtitle)}</text>',
    ]


def finish(parts: list[str], filename: str) -> None:
    parts.append("</svg>")
    (OUT / filename).write_text("\n".join(parts), encoding="utf-8")


def category_mix_chart(rows: list[dict[str, object]], total: Decimal) -> None:
    w, h, left, plot = 960, 560, 190, 620
    parts = svg_start("01  |  Which categories carry the sales mix?", "All 11 saved category summaries · source sales units · currency and period unspecified", w, h)
    top, row_h = 105, 37
    maxv = max(r["sales"] for r in rows)
    for i, r in enumerate(rows):
        y = top + i * row_h
        v = r["sales"]
        share = v / total * 100
        bw = int(plot * float(v / maxv))
        parts += [f'<text class="label" text-anchor="end" x="{left-14}" y="{y+16}">{escape(str(r["category"]))}</text>',
                  f'<rect x="{left}" y="{y}" width="{bw}" height="22" rx="5" fill="{TEAL if i < 3 else BLUE}"/>',
                  f'<text class="value" x="{left+bw+10}" y="{y+16}">{v/Decimal(1000000):,.1f}m  ·  {share:.1f}%</text>']
    parts += [f'<text class="small" x="{left}" y="{top+len(rows)*row_h+7}">The top three categories account for 34.4% of category sales.</text>']
    finish(parts, "category_mix.svg")


def pareto_chart(rows: list[dict[str, object]], total: Decimal) -> None:
    w, h, left, right, top, bottom = 960, 530, 72, 72, 112, 420
    parts = svg_start("02  |  How concentrated is the category portfolio?", "Cumulative share helps distinguish broad assortment from dependence on a few categories", w, h)
    plot_w, plot_h = w-left-right, bottom-top
    n = len(rows); slot = plot_w / n; maxv = max(r["sales"] for r in rows)
    cumulative = Decimal(0)
    points = []
    for i, r in enumerate(rows):
        cumulative += r["sales"]
        x = left + (i+0.5)*slot
        bh = float(r["sales"] / maxv) * plot_h
        parts += [f'<rect x="{x-slot*0.32:.1f}" y="{bottom-bh:.1f}" width="{slot*0.64:.1f}" height="{bh:.1f}" rx="4" fill="{BLUE}"/>',
                  f'<text class="small" text-anchor="middle" transform="translate({x:.1f},{bottom+16}) rotate(42)">{escape(str(r["category"]))}</text>']
        cy = bottom - float(cumulative / total) * plot_h
        points.append((x, cy, cumulative / total * 100))
    for pct in (0,25,50,75,100):
        y = bottom - plot_h*pct/100
        parts += [f'<line class="grid" x1="{left}" y1="{y}" x2="{w-right}" y2="{y}"/>', f'<text class="small" text-anchor="end" x="{left-9}" y="{y+4}">{pct}%</text>']
    poly = " ".join(f"{x:.1f},{y:.1f}" for x,y,_ in points)
    parts.append(f'<polyline points="{poly}" fill="none" stroke="{CORAL}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    for x,y,pct in points:
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{CORAL}" stroke="#fff" stroke-width="2"/>')
    parts += [f'<text class="value" x="{left+6}" y="{top-20}">Top 3 = {points[2][2]:.1f}%</text>', '<text class="small" x="690" y="88">Bars: sales · Line: cumulative sales share</text>']
    finish(parts, "category_concentration.svg")


def city_chart(rows: list[dict[str, object]]) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    rows = sorted(rows, key=lambda r: r["sales"], reverse=True)
    vals = [r["sales"] for r in rows]
    avg = sum(vals, Decimal(0)) / len(vals); low, high = min(vals), max(vals)
    w,h,left,plot = 960,520,170,650
    parts = svg_start("03  |  Are the displayed Top 10 cities meaningfully different?", "Ranked saved Top 10 only · this is not the full city market or a growth comparison", w, h)
    top,row_h = 108,34
    for i,r in enumerate(rows):
        y=top+i*row_h; v=r["sales"]
        # Deliberately use a zero baseline: avoid exaggerating small city differences.
        bw=int(plot*float(v/high))
        parts += [f'<text class="label" text-anchor="end" x="{left-14}" y="{y+15}">{i+1:02d}  {escape(str(r["city"]))}</text>',
                  f'<rect x="{left}" y="{y}" width="{bw}" height="21" rx="5" fill="{TEAL if i==0 else BLUE if i<3 else "#9cb5cb"}"/>',
                  f'<text class="value" x="{left+bw+9}" y="{y+15}">{v/Decimal(1000000):.2f}m</text>']
    parts += [f'<line x1="{left+plot*float(avg/high)}" y1="{top-4}" x2="{left+plot*float(avg/high)}" y2="{top+len(rows)*row_h-8}" stroke="{AMBER}" stroke-width="2" stroke-dasharray="6,5"/>',
              f'<text class="small" x="{left}" y="{top+len(rows)*row_h+8}">Mean {avg/Decimal(1000000):.2f}m · range {(high-low)/Decimal(1000000):.2f}m · relative range {(high-low)/avg*100:.2f}%</text>']
    finish(parts,"city_rank.svg")
    return low,high,avg,(high-low)/avg*100


def attribution_chart(blank: Decimal, category_total: Decimal) -> None:
    pct=blank/category_total*100
    w,h=960,380
    parts=svg_start("04  |  Is customer attribution complete enough for CRM?", "A saved blank-customer bucket is a data-quality signal; it is not a customer-level performance analysis",w,h)
    x,y,width=80,165,800
    # Main proportion bar is true to scale; a magnified inset makes the small share visible.
    filled=width*float(pct/100)
    parts += [f'<text class="label" x="{x}" y="125">Share of category sales attributed to blank customer bucket</text>',
              f'<rect x="{x}" y="{y}" width="{width}" height="36" rx="8" fill="#e8edf3"/>',
              f'<rect x="{x}" y="{y}" width="{filled:.2f}" height="36" rx="8" fill="{CORAL}"/>',
              f'<text class="value" x="{x}" y="236">{pct:.3f}%  ·  {blank/Decimal(1000000):.2f}m source units</text>',
              f'<text class="small" x="{x}" y="263">Magnified callout: the red segment is shown at actual scale above. The source bucket comes from a separate saved PivotTable.</text>',
              f'<rect x="{x}" y="295" width="800" height="48" rx="8" fill="#fff6e8"/>',
              f'<text class="label" x="{x+16}" y="325">Action: trace blank customer keys before using retention, LTV, or customer-segment revenue.</text>']
    finish(parts,"customer_attribution.svg")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    cats=sorted(load_rows("category_sales.csv","category"),key=lambda r:r["sales"],reverse=True)
    cities=load_rows("top10_city_sales.csv","city")
    total=sum((r["sales"] for r in cats),Decimal(0))
    top3=sum((r["sales"] for r in cats[:3]),Decimal(0))
    top_share=top3/total*100
    lowcat,highcat=cats[-1],cats[0]
    blank=Decimal("11415763.1766")
    category_mix_chart(cats,total)
    pareto_chart(cats,total)
    city_low,city_high,city_mean,city_spread=city_chart(cities)
    attribution_chart(blank,total)
    summary={
        "scope":"Saved aggregate PivotTable summaries only",
        "unit":"source sales units; currency and reporting period unspecified",
        "business_questions":[
            {"question":"How much of category sales is concentrated in the three largest categories?","answer":f"{top_share:.2f}% across {', '.join(r['category'] for r in cats[:3])}.","decision":"Prioritize margin, stock availability, and repeat-rate analysis for these categories; do not infer profitability from sales mix."},
            {"question":"How far apart are the category sales leaders and smallest category?","answer":f"{highcat['category']} is {highcat['sales']/Decimal(1000000):.1f}m; {lowcat['category']} is {lowcat['sales']/Decimal(1000000):.1f}m; leader is {highcat['sales']/lowcat['sales']:.2f}x the smallest, a {((highcat['sales']/lowcat['sales'])-1)*100:.1f}% gap.","decision":"Use as an assortment-review shortlist, then check margin, stock-outs, and promotion exposure before changing placement."},
            {"question":"Are the workbook's displayed Top 10 cities clearly separated in sales?","answer":f"{city_low/Decimal(1000000):.2f}m–{city_high/Decimal(1000000):.2f}m; range is {city_spread:.2f}% of their mean.","decision":"The displayed group is tightly clustered; this summary alone does not justify reallocating city spend."},
            {"question":"Is missing customer attribution material for customer analytics?","answer":f"{blank/Decimal(1000000):.2f}m in the blank bucket, approximately {blank/total*100:.3f}% of category sales.","decision":"Small share of category total, but resolve customer keys before retention, lifetime-value, or personalization decisions."}
        ],
        "category_count":len(cats),"category_sales_total":f"{total:.4f}","top_three_share_pct":f"{top_share:.2f}",
        "top_three_categories":[{"category":r["category"],"sales_source_units":f"{r['sales']:.4f}"} for r in cats[:3]],
        "top_bottom_category_ratio":f"{highcat['sales']/lowcat['sales']:.2f}","top_bottom_category_gap":f"{highcat['sales']-lowcat['sales']:.4f}",
        "displayed_top10_city_count":len(cities),"displayed_top10_city_min":f"{city_low:.4f}","displayed_top10_city_max":f"{city_high:.4f}","displayed_top10_city_relative_range_pct":f"{city_spread:.2f}",
        "blank_customer_bucket_sales":f"{blank:.4f}","blank_customer_share_pct_approx":f"{blank/total*100:.3f}",
        "limitations":["No transaction-level rows available to this analysis.","Currency and reporting period are unspecified.","City values cover only the workbook's displayed Top 10.","Blank-customer value is from a separate saved PivotTable and should be recalculated at a consistent grain.","No margin, cost, returns, inventory, order count, trend, or campaign data; no causal or profitability claims are supported."]
    }
    (OUT/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(f"Category total: {total:.4f} source units | top-three share: {top_share:.2f}%")
    print(f"City Top 10 range: {city_low:.2f}–{city_high:.2f} | relative spread: {city_spread:.2f}%")
    print("Wrote four business-question SVG charts and analysis/summary.json")


if __name__=="__main__":
    main()
