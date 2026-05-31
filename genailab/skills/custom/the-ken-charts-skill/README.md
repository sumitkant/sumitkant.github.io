# The Ken Charts — Skill Package

A complete skill for creating data-journalism charts in The Ken's editorial
style, backed by 19 reverse-engineered chart replications.

## Folder structure

```
the-ken-charts-skill/
│
├── SKILL.md                  ← The skill: editorial principles + Plotly workflow
├── kenstyle.py               ← Shared style helper (import in every chart script)
├── README.md                 ← This file
│
├── charts/
│   ├── scripts/              ← 19 Plotly Python scripts (ch01–ch19)
│   │   ├── ch01_testing_right.py
│   │   ├── ch02_tables_turned.py
│   │   └── ... (ch03–ch19)
│   │
│   └── rendered/             ← 19 interactive HTML charts (open in browser)
│       ├── ch01_testing_right.html
│       ├── ch02_tables_turned.html
│       └── ... (ch03–ch19)
│
├── references/               ← Original Ken source images (19 charts)
│   ├── TestingRight.jpg          → ch01
│   ├── browser_chart_1.jpg       → ch02
│   ├── fintech_roundup_1.jpg     → ch03
│   ├── maternity_1.jpg           → ch04
│   ├── range-of-roadsters-updated.jpg → ch05
│   ├── shooting-for-the-moon-updated.jpg → ch06
│   ├── Temasek-1-1-1.jpg         → ch07
│   ├── AI-funding-1-1.jpg        → ch08
│   ├── meitun_1-1.jpg            → ch09
│   ├── VietnamEwallet_1.jpg      → ch10
│   ├── axis-turnaround-1.jpg     → ch11
│   ├── BusinessModels-1-1.jpg    → ch12
│   ├── Paytm-personal-loan1.jpg  → ch13
│   ├── MWG-2.jpg                 → ch14
│   ├── OTA-1-1-1.jpg             → ch15
│   ├── Sea-Group_Shopee-2.jpg    → ch16
│   ├── reliance_retail_1.jpg     → ch17
│   ├── Cultfit2-2.webp           → ch18
│   └── crucialanchor.jpg         → ch19
│
└── templates/                ← Starter files for new charts
    ├── kenstyle.py               ← Copy of helper (self-contained use)
    ├── example_stacked_bar.py    ← Stacked / marimekko pattern
    ├── example_semicircle_panels.py ← Panel + custom shape pattern
    ├── build_all.py              ← Renders all chXX scripts → html/
    └── index.html                ← Gallery page linking all charts
```

## Quick start

```bash
pip install plotly
cd charts/scripts
python ch01_testing_right.py   # writes html/ch01_testing_right.html
# or render everything:
cd ../..
python templates/build_all.py
```

Open any file in `charts/rendered/` in a browser. No server needed.

## Using the skill

Read `SKILL.md` top-to-bottom once. The key sections:

1. **Principles 1–11** — The Ken's editorial design decisions with examples.
2. **Recurring elements table** — The specific things Ken adds to every chart.
3. **Implementation workflow** — 7 steps from "I have data" to working Plotly code.
4. **Quick reference** — The 11 non-negotiables on one page.

`kenstyle.py` implements everything the skill describes. Every chart script
in `charts/scripts/` is a worked example of the principles applied.

## Chart index

| # | File | Title | Chart type |
|---|------|--------|------------|
| 01 | ch01_testing_right | Testing right | 100% stacked horizontal bar |
| 02 | ch02_tables_turned | Tables turned | Multi-line time series |
| 03 | ch03_fintech_frenzy | Fintech frenzy | Vertical bars + horizontal panel |
| 04 | ch04_coming_of_age | Coming of age | Stacked bars + bubbles + CAGR arc |
| 05 | ch05_range_of_roadsters | Range of roadsters | Proportional pill comparison |
| 06 | ch06_shooting_for_the_moon | Shooting for the moon | Grouped bars + NPA bubbles |
| 07 | ch07_doubling_down | Doubling down | Table with embedded bars |
| 08 | ch08_funding_funnel | The funding funnel | Grouped bars + I-beam lollipops |
| 09 | ch09_food_anchor | The food anchor | Full-width stacked revenue strips |
| 10 | ch10_giant_momo | Giant MoMo | Marimekko + call-out leaders |
| 11 | ch11_turning_the_tables | Turning the tables | Semicircle panels + bar pairs |
| 12 | ch12_bumper_year | Bumper year | Bars + bubbles + pie |
| 13 | ch13_main_character | Becoming the main character | Overlapping bars + ratio bubbles |
| 14 | ch14_bhx_pie | BHX's piece of the pie | Pie with hero serif numbers |
| 15 | ch15_lay_of_the_land | Lay of the land | Pie with leader call-outs |
| 16 | ch16_upstart_faceoff | Upstart face-off | 2×3 slope small multiples |
| 17 | ch17_reliance_ebidta | Reliance's EBIDTA game | Side-by-side donuts |
| 18 | ch18_two_caps | Two caps, one table | Dual marimekko with alt. labels |
| 19 | ch19_crucial_anchor | Crucial anchor | Sankey + nested bars |
