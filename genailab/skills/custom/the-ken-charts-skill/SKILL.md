---
name: the-ken-charts
description: Write Plotly code in The Ken's editorial data-journalism style. Use when a user wants to create a chart in The Ken's visual style, asks what makes The Ken's visualizations compelling, or wants to turn a dataset into a story the way The Ken does. The skill covers their editorial principles (opinionated titles, hero numbers, annotation-as-narration, color-as-character, shape-as-emphasis), their recurring visual elements, and how to implement everything in interactive Plotly HTML.
---

# The Ken — visual storytelling principles and Plotly implementation

This skill was built by reverse-engineering 19 of The Ken's published data graphics. The goal is not to copy their aesthetic but to internalize *why* they make each design choice — and then apply that reasoning to new charts.

---

## 1. The title is the headline, not the label

The single biggest difference between a Ken chart and a dashboard widget is the title.

**Dashboard title**: "Q-type distribution across Indian exam boards"
**Ken title**: "Testing right" — with subtitle "Some boards focus more on questions that test rote-learning rather than real-world application"

The title takes a *stance*. The subtitle delivers the *evidence* in one sentence. Together they write the lede before the reader looks at a single bar.

More examples from the 19 charts:

| Chart | What a lazy title would say | What The Ken actually wrote |
|---|---|---|
| ch10 | Vietnam e-wallet market share | **Giant MoMo** |
| ch06 | Kreditbee financials FY21–23 | **Shooting for the moon** |
| ch12 | Annual VC funding 2017–2022 | **Bumper year** |
| ch08 | AI startup funding by stage | **The funding funnel** |
| ch18 | Cult.fit / Curefoods cap tables | **Two caps, one table** |

**Rule**: Write the title as if it's the first sentence of the article. Make it specific enough to be interesting, vague enough to make the reader look at the chart. Then use the subtitle to close the gap.

**In Plotly**: Both title and subtitle are `fig.add_annotation(yref="paper")` calls — never the built-in `fig.layout.title`, which doesn't give enough typographic control. Place the title at y ≈ 0.96 (Playfair Display, bold, 48–68px) and subtitle at y ≈ 0.88 (Libre Franklin, 18–26px). `kenstyle.header(fig, title, subtitle, style)` handles both.

---

## 2. Every chart has one hero number — make it massive

Every Ken chart has a protagonist number. It is rendered 2–4× larger than surrounding data labels. The size encodes editorial emphasis, not data value.

**ch10 — Giant MoMo**: "53" in enormous serif fills the center of MoMo's segment. You absorb 53 before you read the word "MoMo." The number *is* the insight (dominance), and the size confirms it.

**ch14 — BHX's piece of the pie**: "51" (Điện máy Xanh's share) and "22.5" (BHX) are in massive serif inside their slices. The hierarchy is clear: "51" at ~96px, others at ~60px and ~56px. The size tells you which number to care about first.

**ch12 — Bumper year**: "40.6" (2021 funding) is visibly taller than the other bar labels. The chart doesn't need an annotation saying "2021 was the outlier" — the number's size says it.

**ch07 — Doubling down**: "2,300" in the money column is bold like every other value — but the column itself is highlighted in light cyan, making it the visual anchor. The Avg. ticket bars grow right, but "2,300" is what the eye snaps to.

**Rule**: Before you write any code, decide which number is the protagonist. Size it, bold it, or spatially isolate it. The reader should know what to read first without a label saying "look here."

**In Plotly**: For pies and marimekko, suppress `textinfo` and place individual `fig.add_annotation` calls with `font.size` scaled per slice (e.g. 96px for 51%, 60px for 22%). For bars, use `textposition="outside"` with a larger font for the hero bar. `kenstyle.pie_centroids()` computes where to place per-slice annotations.

---

## 3. Annotation as narration, not labeling

Ken annotations don't just name data — they argue a point.

**ch04 — Coming of age**: A dotted red arc curves from the 2010 bar to the 2023 bar with "+21%" at the apex. The arc shape implies trajectory; the dotted line implies projection. You could have put "+21% CAGR" in a footnote, but the arc *draws* the growth story across the chart.

**ch19 — Crucial anchor**: The Sankey shows 189,459 flowing to anchor investors, which splits seven ways. One annotation says "38%" next to the Mutual Funds link. That single number tells you that out of the anchor slice, mutual funds took over a third — making them the real protagonist of the chart, invisible without the annotation.

**ch08 — The funding funnel**: The magenta I-beam rising above each bar is labeled with the number of rounds. It says: "the value of deals is growing, but *also* look at how many rounds are happening." The I-beam height is a second story layered on top of the first.

**ch16 — Upstart face-off**: Red pills (–7, –2, –6, –15, –1) sit near Shopee's 2023 endpoints; green pills (+17, +20, +12, +16, +4) float near Tiktok's. You could have put these in a legend or table. Instead they're embedded in the chart, positioned so your eye naturally follows the slope to its conclusion and immediately reads the verdict.

**Rule**: For each chart, identify the *editorial point* that a casual reader might miss. Then add one annotation that delivers it. This is not the same as labeling every bar — it is naming the thing the data proves.

**In Plotly**: Use `fig.add_annotation(xref="paper", yref="paper")` for free-floating editorial notes. Use `fig.add_shape(type="path")` for drawn elements (arcs, arrows). `kenstyle.paper_arrow()` places arrows in paper space. Keep annotation text short — a number, a percentage, a 3-word phrase.

---

## 4. Color as character, not category

Ken's color choices are not arbitrary categorical assignments. Each color carries a role in the story.

**ch03 — Fintech frenzy**: Four sector bars are navy. One — Fintech — is gold. Navy says "background" or "supporting cast." Gold says "this is the subject of the article." The color encodes editorial priority, not just category membership.

**ch10 — Giant MoMo**: The six segments ramp from deepest maroon (#7A0E22) for MoMo to near-black (#111111) for GrabPay. Darker = more established / dominant. The color itself communicates market order before you read a number.

**ch04 — Coming of age**: Services are purple (heritage, depth, value) and Products are light blue (newer, lighter category). The chromatic contrast is soft but deliberate — purple has gravitas, light blue suggests growth potential.

**ch18 — Two caps, one table**: Cult.fit's segments ramp teal→cyan→sky→cornflower→periwinkle→purple→violet→magenta — cool to warm, young to established? Curefoods runs gold→amber→orange→red→crimson→maroon — hot palette for a food company. The ramp makes 8 segments legible without a legend because you can track the gradient.

**ch16 — Upstart face-off**: Shopee is cyan, Tiktok is magenta. These aren't brand colors — they're high-contrast complementaries. The slopes' directions are legible instantly because the two lines can't be confused.

**Rule**: Before assigning colors, ask: "Who is the protagonist?" Color them distinctly. "Who is the background?" Use a muted color family. "Is there a sequence?" Use a ramp. "Are there two competing entities?" Use high-contrast complementaries.

**In Plotly**: `kenstyle.KEN` provides the full palette. Use `KEN["gold"]` for protagonists, `KEN["navy"]` for supporting bars. Build ramps explicitly (e.g. a list of hex colors from dark to light). Never let Plotly auto-assign colors — the default palette has no editorial intent.

---

## 5. Size and shape carry meaning beyond value

Ken regularly invents chart geometry to match the editorial need. Shape is not just aesthetic — it encodes a concept.

**Semicircles (ch11 — Turning the tables)**: A pink half-disk sits above each FY's bars. Its area is proportional to operating profit. It doesn't replace the bars (NNPA, NIM) — it adds a *third* metric as a shape that naturally suggests "growing weight" as it gets larger toward FY24. A line would have shown the same data; a semicircle makes the growth feel architectural.

**Price pills (ch05 — Range of roadsters)**: Each car gets an orange bar whose width is proportional to its price. The Porsche pill spans the full width of the chart; the others cluster at 24–27%. No y-axis needed. The pill shape (rounded rectangle) signals "badge" — a qualitative judgment packaged as a measured fact.

**Lollipop I-beams (ch08 — The funding funnel)**: A thin magenta line rises from each bar top, capped with a horizontal stroke, with the round count at the tip. The "lollipop" format separates the rounds story from the value story, using height for rounds on a secondary implicit scale. It's a layered chart that doesn't look layered.

**CAGR arc (ch04)**: The dotted red curve from 2010 to 2023 is drawn with an SVG Bézier — not a chart element at all, but a design element that *argues* for a trend across a gap in the data.

**Rule**: Ask "what shape *feels* like this data?" Operating profit accruing over time feels like weight building — hence the growing semicircle. Price hierarchy feels like runway length — hence proportional pills. Growth across a gap feels like a trajectory — hence the arc. Then implement that shape.

**In Plotly**: `kenstyle.rounded_rect_path()` builds pill shapes as SVG paths for `add_shape(type="path")`. `kenstyle.semicircle_path()` builds half-disks. Arcs use Bézier paths (`C` commands in SVG). Bubbles use `go.Scatter` markers with explicit `size` lists where **diameter ∝ value** (not √value — Ken bubbles are not area-proportional, they are diameter-proportional for visual clarity).

---

## 6. Grey panels isolate mini-stories

When a chart shows multiple comparable units (time periods, countries, companies), Ken often wraps each unit in a grey rounded panel. This has two effects: it groups data that belongs together, and it signals that each panel is *a story within the story*.

**ch11 — Turning the tables**: Seven FY panels, left to right. The semicircle grows, the NNPA bar shrinks. Each panel is Axis Bank in that year. You read them as a filmstrip — individual frames that form a narrative.

**ch16 — Upstart face-off**: Six country panels, 2×3 grid. Each is a self-contained slope chart with its own y-scale. The panels communicate "these are separate markets, not one aggregate." The gain/loss pills inside each panel deliver the verdict independently.

**ch08 — The funding funnel**: Dotted bracket lines under the x-axis create two implicit panels: "Seed" and "in Series A." This is a softer version of the panel — not a box, but a boundary.

**Rule**: If your chart shows multiple comparable units, consider giving each unit its own visual container (grey rounded rect, bracket, light band). The container says: "within here, one story. Across all of them, a bigger story."

**In Plotly**: Draw panels with `add_shape(type="path", path=kenstyle.rounded_rect_path(...), fillcolor="#ECEAE5")`. For grid layouts (small multiples), give each panel its own axis-domain pair (`xaxis`, `xaxis2`, ...) and draw the panel background as a shape in paper space. For brackets, draw lines + end-caps in paper space with `add_shape`.

---

## 7. The two typographic eras

Ken's charts split into two visual modes depending on the publication period:

**Newer pieces (2021+)**: Warm cream canvas (`#F7F4EF`), serif display headline (Playfair Display, Title Case, bold), body in Libre Franklin. Wordmark: `◁ THE KEN` in black. Footer brand color: black. These charts feel editorial, like a magazine.

**Older pieces (2019–2020)**: White canvas, heavy sans headline (Archivo Black, ALL CAPS), wordmark `THE-KEN` in grey. Footer brand color: grey. These charts feel more like data product, less editorial.

The distinction signals authority: serif + cream = "we're telling you a story." Heavy caps + white = "we're presenting facts." Both are confident; neither is decorative.

**In Plotly**: `kenstyle.header(fig, title, subtitle, style="serif")` for cream-canvas pieces. `kenstyle.header(fig, title, subtitle, style="heavy")` for white-canvas pieces. The `style` param switches both the font family and the case transform.

---

## 8. The footer is a trust signal, not a formality

Every Ken chart has exactly the same footer format:

```
◁ THE KEN    [center] Graphic by [Name], [Date]    [right] Source: [Specific source]
```

Three things make this notable:
1. The graphic credit **names an individual**, not "The Ken team." This is accountability journalism applied to visual work.
2. The source is **specific** — "Axis Bank's annual reports" not "company reports"; "Prime Database" not "public data."
3. The left-right-center layout ensures the eye can find attribution without a hunt.

The footer's consistency across 19 charts means a reader who recognises it immediately knows: this chart was made by a journalist who stands behind the numbers.

**In Plotly**: `kenstyle.footer(fig, "Graphic by Kashvi B, 22 Sep '24", "Source: Axis Bank's annual reports")` places all three elements. Never skip the footer. Never write "Source: Various."

---

## 9. Comparison through overlap and nesting

Several Ken charts encode "A is a part of B" through visual containment rather than arithmetic.

**ch13 — Becoming the main character**: A wide light-teal bar (total operational revenue) sits behind a narrower dark-teal bar (financial services revenue). Both start at zero. The dark bar's height relative to the light bar *is* the ratio — you don't need to calculate it. The growing orange bubble above (the ratio as %) is the annotation-as-narration layer.

**ch19 — Crucial anchor**: Three overlapping horizontal bars — total IPO proceeds (longest), anchor book (medium), mutual funds (shortest). All start at zero. The visual nesting communicates "these are subsets of each other" without a Venn diagram or a table.

**Rule**: When showing "A is a subset of B," draw A on top of B from the same baseline, narrower. The visual containment makes the proportion legible before any number is read.

**In Plotly**: `fig.update_layout(barmode="overlay")`. Draw the widest bar first (back), narrowest last (front). Width matters: wider bar recedes visually; narrower bar advances. All bars share `x=0` as the origin.

---

## 10. The "axis break" as editorial judgment

In Bumper Year (ch12), the six bars show CY17–CY21 plus "Jan'22–Jun'22." The last bar covers only half a year. Ken marks this with a "//" break symbol between the last two bars and a different x-label format.

This is not a data convention — it's an editorial judgment. The chart is saying: "We know Jan–Jun 2022 isn't comparable to a full year. We're showing it anyway because it's directionally meaningful. The break is honest."

**Rule**: When comparing non-comparable time periods, explicitly mark the difference. The "//" is not decoration — it's a statement of honesty. A reader who misses it might draw a wrong conclusion; the symbol prevents that.

**In Plotly**: Use a wider gap in the numeric x positions (e.g. CY21 at x=4, Jan'22 at x=5.4 instead of 5) combined with a paper-space annotation of `"//"` between them.

---

## 11. Recurring visual vocabulary: what Ken always adds

Beyond the structural principles, Ken consistently adds specific elements that elevate visualization from "chart" to "editorial":

| Element | Where it appears | What it adds |
|---|---|---|
| Large serif hero number | Pies, marimekko, donut holes | Immediate magnitude read |
| Call-out leader line | Tiny slices (Bluetronics 0.4%, GrabPay 2%) | No data left unlabeled |
| Value-sized bubble | Grouped bars (ch06, ch08), line charts (ch12) | Third dimension without a third axis |
| CAGR arc or trend arc | ch04, ch10 (implicitly) | Draws growth trajectory across time gap |
| Gain/loss pill | ch16 slope charts | Delivers verdict without math |
| I-beam lollipop | ch08 | Second metric that rises above the first |
| Rounded panel container | ch11, ch08 | Isolates per-unit story |
| Fraction legend (A/B = %) | ch13 | Explains the ratio before you see the data |
| Axis break "//" | ch12 | Honest comparability signal |
| Pink/warm semicircle | ch11 | Area-as-weight for a third metric |
| Marimekko full-width bar | ch01, ch09, ch10, ch18 | "The whole universe" = one bar |

---

## Implementation workflow: writing Plotly code for a new Ken-style chart

When asked to create a Ken-style chart, follow this sequence:

### Step 1: Identify the editorial claim
Before touching code, answer: "What is the one thing this data proves?" That claim becomes the title. The supporting fact becomes the subtitle.

> *"AI-enabled startups raised more per deal in 2024 than 2023, especially at Series A"*
> → Title: **"The funding funnel"** / Subtitle: "Fewer AI startups are getting funded, but those that do are raising larger cheques—especially at Series A"

### Step 2: Identify the hero number
Which number should the reader absorb first? Size it or isolate it accordingly.

> *The 2024 AI-enabled Series A bar is 188.4 — the tallest in the chart. It gets the largest value label.*

### Step 3: Choose the chart type based on the story shape

| Story shape | Chart type |
|---|---|
| "X dominates; others trail" | Marimekko / horizontal bar with protagonist color |
| "Both grew, but differently" | Grouped bars, same scale |
| "A is becoming B over time" | Overlapping bars (wide behind, narrow in front) |
| "The whole splits into parts" | Pie / donut — sort by size, hero slice first or center |
| "Before vs. after across many units" | Small-multiple slope charts |
| "Flow from source to destinations" | Sankey |
| "Three things happening simultaneously" | Grouped bars + bubble (third variable) |
| "A trend across a gap" | Line with CAGR arc annotation |
| "Ranking with a secondary dimension" | Horizontal bars + badge pills for secondary metric |

### Step 4: Assign colors editorially

1. Protagonist: `KEN["gold"]`, `KEN["teal"]`, or a vivid color.
2. Background/supporting: `KEN["navy"]`, muted greys, desaturated versions.
3. Two competitors: high-contrast complementary (cyan + magenta for Shopee/Tiktok).
4. A sequence or ramp: build an explicit gradient list.
5. Negative values: `KEN["red"]` or `KEN["magenta"]`.
6. Growth/positive: `KEN["green"]` or `KEN["teal"]`.

### Step 5: Add the annotation-as-narration

Ask: "What editorial point might a fast reader miss?" Add one annotation that delivers it. Typical patterns:
- A percentage: "38%" near the most important Sankey link
- A growth rate: "+21%" with an arc spanning the time period
- A verdict: "–7" red pill on the losing slope, "+17" green pill on the winner
- A comparison: "54X" in the subtitle or as a floating annotation

### Step 6: Canvas and layout (the non-negotiables)

```python
import kenstyle as ks

# Choose era
style = "serif"    # cream canvas, Playfair — for 2021+ editorial stories
# style = "heavy"  # white canvas, Archivo Black ALL CAPS — for fact-forward older style

fig = ks.canvas(
    width=1100, height=720,             # adjust per chart density
    bg=ks.CREAM if style=="serif" else ks.WHITE,
    plot_x=(0.06, 0.96),                # horizontal data region
    plot_y=(0.10, 0.76),                # vertical data region — leave room for header/footer
)

# ALWAYS numeric x for bar/grouped charts:
gx = [0, 1, 2, 3]
fig.update_layout(xaxis=dict(
    range=[-0.6, 3.6],
    tickmode="array", tickvals=gx, ticktext=["FY21","FY22","FY23","FY24"]
))

# Header
ks.header(fig, "Your title here", "One-sentence insight", style=style,
          title_size=56, subtitle_size=22)

# Footer — ALWAYS present, ALWAYS specific
ks.footer(fig, "Graphic by [Name], [Date]", "Source: [Specific source]")

# Render — interactive HTML, no Chrome
ks.render(fig, "my_chart_name")
```

### Step 7: The layout rule (domain, not margins)

```python
# DON'T: use big margins to make room for headers
# margins get out of control and yref="paper" annotations misbehave

# DO: tiny margins + axis domain
fig.update_layout(margin=dict(l=10,r=10,t=10,b=10))
# Header lives in paper y [0.80..1.0]
# Data plot lives in yaxis domain [0.10..0.76]
# Footer lives in paper y [0.0..0.08]
# All three are reliable, composable, predictable
```

---

## Quick reference: The Ken's non-negotiables

1. **Title = editorial claim.** Not "Q-type distribution" — "Testing right."
2. **Subtitle = evidence in one sentence.** Specific, not vague.
3. **Hero number = sized for importance,** not for value.
4. **One annotation = the editorial point** the data proves but doesn't shout.
5. **Protagonist color = distinct.** Every other color = supporting cast.
6. **Size/shape = concept.** Semicircle = weight. Arc = trajectory. Pill = badge. Nested bar = subset.
7. **Grey panel = one mini-story.** Grid of panels = sequence of mini-stories.
8. **Footer = always.** Individual credit. Specific source. ◁ THE KEN wordmark.
9. **Numeric x always.** String categories on bar axes silently break in Plotly.
10. **Domain, not margins.** Tiny margins + axis domain = reliable paper-space layout.
11. **`kenstyle.render()` = pure HTML.** No Chrome. No Kaleido. Just Plotly.

---

*Implementation helpers live in `kenstyle.py` (shipped with this skill). The file provides `canvas`, `header`, `footer`, `legend_chips`, `paper_arrow`, `rounded_rect_path`, `semicircle_path`, `pie_centroids`, and `render`. Full examples: `example_stacked_bar.py` and `example_semicircle_panels.py`.*
