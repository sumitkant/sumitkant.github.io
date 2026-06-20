# HTML Visual Story

A self-contained `.html` file that presents the summary as a visual story in the style of The Ken's data graphics: a bold headline, a single strong visualization, the full set of summary bullets, and gray footnote links. One file per story (the summary). Save to the outputs directory and present it.

## Choose the visualization from the content

Pick ONE primary visualization that matches what the data actually is. Don't force a chart onto prose that has no numbers — fall back to the hero banner image then.

| What the content is | Visualization to build |
| --- | --- |
| A vs B (or a few entities) compared across several metrics | **Comparison table** or **paired bars** — one row per metric, two+ columns. (Ken: "One-upping each other") |
| Parts of a whole / share / ownership / stakeholders | **Donut** or **segmented horizontal bar** with inline labels. (Ken: "Wheel of fortune", "Two caps, one table") |
| Change over time / trajectory / rise-and-fall | **Line chart**, latest values labeled at the right. (Ken: "Tables turned") |
| Dated events / milestones / a release sequence | **Vertical timeline** with date nodes |
| Performance / speed / throughput / scores / efficiency | **Dial/gauge** or **KPI bars** with oversized numbers and a ratio callout (e.g. "15×") |
| Ranking / ordered-by-value | **Ordered horizontal bars**, biggest first |
| Amounts over years + a secondary metric | **Bar + bubble combo** (Ken: "Bumper year") |
| One dominant figure carries the story | **Big-number KPI callout** with supporting context |
| Distribution across many categories | **Stacked bars** per category (Ken: "Testing right") |
| No clean quantitative structure | **Hero banner** = the article's `og:image` (no fabricated chart) |

Rules:
- **If both a banner image and a viable data viz exist, prefer the viz.**
- Use only numbers that appear in the source. Never invent data points to fill a chart. If only one or two numbers exist, a KPI callout beats a fake multi-point chart.
- Label every value directly on the visualization (The Ken almost never relies on axes alone — the numbers sit on the bars/slices).

## Page structure (in this exact order)

1. **Title** — the summary's insight headline. Heavy weight, large, tight leading.
2. **Objective** — one sentence under the title: what this is about / the "so what". Medium weight, muted color.
3. **Hero visualization** (or banner if no viz fits) — the single chart chosen above, with a colored legend where needed.
4. **Summary bullets** — ALL the summary bullets from the chat output (this is the point: more detailed than a bare Ken graphic). Custom colored bullet markers, not default discs.
5. **Footnotes** — every link (source, references, code repo, model card, API docs, paper), in small gray text. Lead with `Source:`.

## Styling

- **Font: Plus Jakarta Sans for everything** (load from Google Fonts). Weights: 800 for title, 700 for chart numbers and section labels, 600 for bullets' lead, 400–500 for body and footnotes. (The Ken itself uses a serif display, but the brief specifies Plus Jakarta Sans — honor the brief.)
- Self-contained: inline `<style>`, inline SVG/CSS charts, no external JS libraries. White background, one centered column ~860px max-width, generous whitespace.
- **The Ken palette** (flat, saturated, numbers sit on the color):
  ```
  --ken-indigo:#6B5BD2;  --ken-orange:#F2792B;  --ken-sky:#67C7E8;
  --ken-gold:#F4B61C;    --ken-lime:#DDE86B;     --ken-green:#2BA24C;
  --ken-blue:#1C75BC;    --ken-magenta:#C2249A;
  --ink:#14110F;  --muted:#6B7280;  --hair:#E9E7E2;  --footnote:#9AA0A6;
  ```
- Big bold numbers live *inside* bars/slices in white or ink, as in the uploads. Minimal or no gridlines. Hairline `--hair` dividers between table rows.
- Footnote links: `--footnote` gray, underline on hover, wrap as a small block. Keep `None found` / `Not released` as plain gray text.
- Quality floor: responsive down to ~360px, visible focus on links, `prefers-reduced-motion` respected if any motion is used. Keep motion minimal — a single load fade at most.

## Filename

Descriptive, e.g. `gemma4-cerebras-visual-story.html`.

## Relationship to the other outputs

This HTML is **in addition to** the chat summary, innovation profiles, and the TiddlyWiki `.tid` files — it doesn't replace them. The `.tid` files stay as the wiki-import artifact; the `.html` is the shareable visual story. Use the same headline, objective, bullets, and links across all of them so they stay consistent.
