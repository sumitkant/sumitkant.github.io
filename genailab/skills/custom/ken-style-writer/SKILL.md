---
name: ken-style-writer
description: write or rewrite full business journalism articles in a ken-like analytical style from topics, notes, drafts, transcripts, links, uploaded documents, or web research. Use when the user asks to create, rewrite, expand, or polish an article with the narrative structure, sharp business analysis, reported texture, skeptical humor, data-backed argumentation, and India-focused company/category lens associated with the ken, including longform reported features and shorter conversational nutgraf-style commentary.
---

# Ken-Style Business Article Writer

Use this skill to produce full articles, not generic summaries. The output should feel like a reported business story: a sharp thesis, vivid opening, quantified stakes, named incentives, human texture, and a skeptical but not cynical narrative voice.

## Core workflow

1. Determine the requested format:
   - **Longform feature**: 1,500-2,800 words unless the user specifies otherwise. Use reported-story structure, sections, multiple stakeholder perspectives, data, and industry context.
   - **Short Nutgraf-style commentary**: 700-1,200 words. Use a more conversational first-person or editorial voice, a faster argument arc, and a sharper final turn.
2. Identify the article category: technology/AI, finance/fintech, startup/VC, consumer/FMCG, infrastructure/platform power, education/policy, mobility, telecom, or edtech.
3. Gather enough inputs. If only a topic is provided, ask for permission to research or use web search. If the user provides links, transcripts, filings, or uploaded documents, mine them first.
4. Build the article angle before drafting:
   - surface contradiction
   - identify who benefits and who pays
   - convert facts into a business mechanism
   - define the stakes in money, market power, regulation, growth, or consumer harm
5. Draft with a strong headline, opening, nut graf, body sections, and ending.
6. Do not fabricate reporting. Mark unsupported claims as assumptions or leave them out. Prefer attributed claims, named sources, and explicit uncertainty.

## Before writing

Ask at most two clarifying questions if any of these are missing and materially affect the draft:
- desired length: longform or short commentary
- source base: user-provided material only, web search allowed, or both
- geography/audience if not obvious

If the user wants immediate drafting from minimal input, proceed but label the result as a draft based on limited inputs.

## Style references

Load these reference files as needed:
- `references/style-guide.md` for voice, syntax, article architecture, and line-level rules.
- `references/category-playbooks.md` for category-specific patterns.
- `references/article-templates.md` for longform and short commentary structures.
- `references/research-rules.md` for sourcing, web usage, and evidence handling.

## Output requirements

Always produce a complete article unless the user requests only an outline or critique.

A full article should include:
- headline
- optional dek/subtitle when useful
- opening scene, quote, contradiction, or data-led setup
- clear nut graf by paragraph 5-8 for longform or paragraph 3-5 for short commentary
- section headings for longform; optional headings for short commentary
- quantified stakes and business mechanics
- at least one counter-pressure, caveat, or opposing incentive
- ending that reframes the opening or sharpens the thesis instead of merely summarizing

## Guardrails

- Capture the style architecture and editorial feel; do not copy or closely paraphrase distinctive lines from reference articles.
- Do not invent interviews, quotes, financials, regulatory facts, filings, or unnamed source claims.
- Use placeholders like `[company response]`, `[former executive quote]`, or `[filing figure]` only when the user explicitly wants a scaffold.
- Avoid fanboy language, promotional copy, and consultant-speak.
- Avoid generic thought-leadership endings. End with a consequence, irony, or unresolved strategic tension.
