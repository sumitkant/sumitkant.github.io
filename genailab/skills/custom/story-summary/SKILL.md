---
name: story-summary
description: Summarize any content into a tight, story-style brief that keeps every number and fact, removes all filler, and surfaces the single clearest insight — and separately detect, research, and profile any NEW innovation the content launches (a named model, system, method, technique, dataset, benchmark, or framework). Use whenever the user wants a summary, recap, TL;DR, brief, digest, or "summarize this," OR wants to identify/uncover/profile new innovations, techniques, models, or research releases — especially when they want it short, story-like, insight-first, in bullets, or following a 5W1H / who-what-when-where-why-how structure. Trigger this for articles, papers, reports, transcripts, emails, threads, launch posts, or pasted text, even if the user just says "summarize" without naming the format.
---

# Story Summary

Turn content into a ~200-word brief that reads like the story actually happened: one insight-driven headline, then bullets that walk through it. Keep the facts, cut the filler. Then, in **Part 2**, separately detect and research any new innovation the content launches and profile it in a fixed format.

## The method

Before writing, find two things:

1. **The 5W1H spine.** Answer silently: **Who** acted, **What** happened, **When**, **Where**, **Why** it happened, **How** it played out. These are the load-bearing facts — every name, number, date, amount, and outcome lives here. Never drop a quantity to save words; drop adjectives instead.
2. **The insight.** The one non-obvious thing a smart reader takes away — the surprise, the cause, the consequence, the "so what." Everything else is support.

Then write the headline *from the insight*, and the bullets *from the spine*.

## Output format

ALWAYS use exactly this structure and nothing else:

**[Headline: states the insight AND opens a curiosity gap]**

- [Lead bullet: Who + What + the core result, with the key number]
- [bullet]
- [bullet]
- [bullet]
- [Closing bullet: the Why or the So-what / consequence]

Rules for the output:

- **Total ≤ 200 words.** Aim for 120–180. Shorter is better if facts are preserved.
- **4–6 bullets.** Each is one beat of the story in plain narrative prose (a clause or short sentence), not a label. Do NOT write "Who:", "What:", "When:" — weave the 5W1H in naturally so it reads as a story, not a form.
- **Keep all numbers, names, dates, and proper nouns** exactly as given. These are the spine; losing one is a failure.
- **Cut all filler:** hedges ("it should be noted"), throat-clearing, restated context, generic background, and anything the reader already knows.
- **One insight, made obvious.** It headlines the piece and is paid off in the bullets — never teased and abandoned.

## Headline rules

The headline carries the insight *and* makes the reader want the bullets.

- Be **concrete and specific** — a real number or named fact creates more curiosity than a vague tease ("Revenue doubled — but on a cost no one budgeted for" beats "A surprising business update").
- **Never end with a question mark**, and never use clickbait that the bullets don't deliver. The bullets must pay off the headline; that's the only line between curiosity and clickbait.
- Keep it to one line (~6–12 words).

## Examples

**Headline (insight + curiosity), good vs. weak:**
- Good: `Nvidia's 122% jump came from one customer it won't name`
- Weak: `Nvidia reports strong quarterly earnings results` (no insight, no curiosity)

**A full mini-example.** Input: a long earnings article. Output:

**Nvidia's record quarter hides a single-customer risk**

- Nvidia posted $35.1B in Q3 revenue, up 94% year-over-year, beating estimates by $2B.
- Data-center sales drove it: $30.8B, nearly 88% of the total.
- One unnamed customer made up ~13% of revenue — a concentration analysts flagged as fragile.
- CEO Jensen Huang said Blackwell-chip demand is "insane," with supply sold out through 2025.
- The catch: if that one buyer slows AI spending, the growth story wobbles fast.

*(~75 words, every figure preserved, filler gone, insight headlined and paid off.)*

## Part 2 — New innovation profiles

After the story summary, scan the content for any **new innovation** it introduces: a newly named model, system, method, technique, architecture, dataset, benchmark, framework, API, or product capability. The signal is a proper noun the content presents as *new* (launched, released, introduced, proposed, open-sourced), often capitalized.

For **each** distinct innovation found, do this — do NOT skip the research:

1. **Run a separate web search** for that innovation by name (e.g. `"<name>" <vendor> launch`). Don't rely only on the article — confirm and enrich from primary sources. Run more than one query if the first is thin.
2. **Fill the 5W1H silently** for the innovation: who built it, what it is, when it launched, where it runs/applies, why it matters, how it works.
3. **Confirm artifacts and links**: search for and verify the innovation's **code repo** (GitHub/HF), **model card** (Hugging Face or other model hub), **API / developer docs**, and **paper** (arXiv/blog/technical report). Capture the URL for each. If you cannot find one, write `Not released` or `None found` — never invent a link.

If no new innovation is present, write `No new innovation detected.` and stop — do not force one.

### Innovation output format

ALWAYS use exactly this structure, one block per innovation:

```
**Innovation:** [name]
**Objective:** [one sentence — what it's for + the headline numbers/details, e.g. "Cuts agent cost 13% and lifts answer correctness 25% by reusing past work."]
**Detailed description:**
- [feature / mechanism beat]
- [feature / mechanism beat]
- [3–5 bullets total, each a concrete capability or how-it-works detail, numbers kept]
**Limitations:** [known caveats — early/first-party numbers, gated access, schedule, governance, etc.]
**Links:**
- References: [primary source URL(s) — vendor page, launch/blog post]
- Code repo: [URL, or "Not released" / "Not found"]
- Model card: [Hugging Face / model-hub URL, or "None found"]
- API docs: [official API/developer-docs URL, or "None found"]
- Paper link: [arXiv / technical-report URL, or "None found"]
```

When researching each innovation, search specifically for these link targets — a **model card** (Hugging Face or other model hub), **API / developer docs**, a **code repo** (GitHub/HF), and a **paper** (arXiv or technical report). Verify each link resolves to the right artifact before listing it; if a target genuinely doesn't exist, write `None found` rather than guessing or reusing an unrelated URL.

Rules: keep every metric in **Objective** or **Detailed description**. Each innovation gets its own block. Keep blocks tight — the detailed description is 3–5 bullets, not a re-summary of the whole article.

## Part 3 — Downloadable TiddlyWiki output

After showing the summary (and any innovation profiles) in chat, also emit each one as a **separate downloadable file in TiddlyWiki WikiText**, so the user can drop it straight into their wiki. Produce:

- One `.tid` file for the **story summary**.
- One `.tid` file for **each innovation** profiled (never bundle several innovations into one file).

Save them to the outputs directory and surface them with the file-presentation tool.

### WikiText conversion rules

Translate the chat output into TiddlyWiki syntax — do NOT paste Markdown. Strip any chat-only citation markup; the file is clean WikiText.

- **Heading**: the summary's headline (or `Innovation: <name>`) becomes a top-level heading with `! ` (one bang, space, text).
- **Hero image (top of file)**: immediately under the heading, embed a hero image with `[img width=600 [<image-url>]]`. Use the article's lead/social image — its `og:image` meta tag is the reliable source; otherwise the most prominent in-content image. For an innovation file, prefer an image from the innovation's own model card or project page, falling back to the article's hero image. If no usable image URL exists, omit the line rather than invent one.
- **Source URL**: just below the hero image, add a source line linking to the summarized article: `''Source:'' [[<article title or domain>|<article-url>]]`. In an innovation file, set this to the innovation's primary reference URL. Always include the actual summarized-article URL somewhere in the file.
- **Bullets**: use `* ` for each bullet (one level). For the innovation profile's labeled fields, bold the label: `* ''Objective:'' …`.
- **Bold**: wrap emphasis in two single quotes — `''like this''` (not `**…**`).
- **Wiki-links**: wrap the key entities/concepts (model names, companies, methods, datasets, benchmarks) in double square brackets `[[Like This]]` so they become navigable tiddlers. Link the first, most important mention; don't over-link every word.
- **External links** (innovation Links block): use masked syntax `[[Model card|https://…]]`, `[[Code repo|https://…]]`, etc. Keep `None found` / `Not released` as plain text.
- Keep numbers, names, and dates exactly as in the chat version.

### Required bottom line: date + tags

End every file with a single subscript line of tags and the date, each in double square brackets, pipe-separated — matching this shape:

```
,,Tags: [[Topic A]]| [[Topic B]]| [[18 June 2026]],,
```

- Include 1–3 **topic tags** drawn from the content (e.g. the domain, company, or theme), then the **date** as the final bracketed item.
- **Date**: use the source's publication date when known; otherwise today's date. Format it `D Month YYYY` (e.g. `18 June 2026`).
- This line is wrapped in `,,…,,` (TiddlyWiki subscript) exactly as shown, so it renders as a small footer.

### Example `.tid` body

```
! Nvidia's record quarter hides a single-customer risk

[img width=600 [https://example.com/nvidia-q3-hero.jpg]]

''Source:'' [[reuters.com|https://www.reuters.com/example-nvidia-q3]]

* [[Nvidia]] posted $35.1B in Q3 revenue, up 94% year-over-year, beating estimates by $2B.
* Data-center sales drove it: $30.8B, nearly 88% of the total.
* One unnamed customer made up ~13% of revenue — a concentration analysts flagged as fragile.
* The catch: if that one buyer slows AI spending, the growth story wobbles fast.

,,Tags: [[Nvidia]]| [[Earnings]]| [[Semiconductors]]| [[20 November 2025]],,
```

Give each file a short, descriptive filename (e.g. `nvidia-q3-summary.tid`, `context-graph-innovation.tid`).

## Part 4 — HTML visual story

Also produce a self-contained **HTML visual story** for the summary, styled like The Ken's data graphics. The page order is fixed: ''Title → Objective → hero visualization → all summary bullets → gray footnote links'', in Plus Jakarta Sans.

The key step is choosing the right visualization from the content — a comparison becomes a table or paired bars, a timeline becomes a vertical timeline, performance/throughput becomes dials or KPI bars with a ratio callout, composition becomes a donut or segmented bar, a trend becomes a line chart. If both a banner image and a viable chart exist, prefer the chart; if nothing quantitative fits, fall back to the article's hero image. Use only numbers present in the source.

Before building the HTML, read `references/html-visual-story.md` for the full chart-selection table, page structure, the Ken color palette, and styling rules, and `/mnt/skills/public/frontend-design/SKILL.md` for design execution. This HTML is in addition to the `.tid` files, reusing the same headline, objective, bullets, and links.

## Notes

- If the content has no single clean insight, lead with the most consequential fact instead — never invent one.
- If asked for a different length, scale the bullet count but keep the headline + story-in-bullets shape.
- Match the source's language.
