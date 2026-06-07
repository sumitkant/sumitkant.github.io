---
name: book-distiller
description: Distill a book, paper, or long document into three grounded deliverables — a Fact Book, an Insight Book, and a Story that stitches them together. Use this whenever the user uploads a PDF/document and wants the key ideas, the "few things worth reading," a distillation, a summary they can trust, or asks to be told what a book is really about. Trigger it for any "read this book/paper for me," "what are the main ideas," "give me the facts and the takeaways," or "condense this" request over a substantial document — even if the user doesn't say the word "distill."
---

# Book Distiller

Turn a long document into three layers that are deliberately kept separate, because a fact and an interpretation have different truth-conditions and blurring them produces confident-sounding invention.

Work **only** from the uploaded text. Never add information from outside the document. If you ever feel the urge to add outside knowledge, mark that sentence with ⚠ so the user can see it is not from the book.

## Workflow

1. Read the actual document (the uploaded file, not your memory of similar books).
2. Produce the three parts below, in order.
3. End with a short honesty pass.

Default scale: **25–40 facts** and **8–12 insights**. Don't promise a page count — counts are controllable, page counts are not.

## Part 1 — Facts

What the document *states*, checkable against a page.

- Reword each fact into one plain-language sentence. Do not quote.
- Pin every fact to its page, e.g. `(p.12)`.
- Keep them atomic and non-narrative — a dense reference list, numbered continuously.
- Group by concept for readability, but keep numbering global so insights can reference them.
- Import nothing the page doesn't support.

**Example:**
`11. Temperature 0 is greedy decoding — the highest-probability token is always picked. (p.10)`

## Part 2 — Insights

The "so what" — implications, connections, the point the author is driving at. By definition these go beyond any single page, so they are **not** page-pinned. Instead, each insight cites the **fact numbers** it rests on, giving an audit trail: insight → facts → pages.

- Label this section clearly as interpretation, not the author's stated words.
- Each insight: one short paragraph, ending with the facts it builds on, e.g. `(builds on facts 4, 9, 26)`.

**Example:**
`The whole book rests on one mental model — the LLM as a next-token prediction engine — and almost every technique is just a different way to bias that prediction. (builds on facts 4, 9, 26)`

## Part 3 — Story

The facts and insights woven into a single narrative.

Narrative aids memory, but it also *wants* causality and will manufacture links the author never claimed. Guard against this with one rule: **let the document's own structure be the story's spine.** Follow the order in which the document builds its concepts (what must be understood before what) rather than an order invented to make the prose flow. Any connective tissue you add on top of that gets carried by an insight that's already labelled as interpretation — never stated as the document's own claim.

## Honesty pass (close every distillation with this)

A few sentences, plainly:
- Confirm the facts are traceable and reworded, not quoted.
- Name where the fact/insight line blurred — which "facts" actually carried interpretation, which insights are your synthesis rather than the author's words.
- Flag any numbers or claims that are the author's *starting points / examples* rather than universal rules.

## When the method is weak

Say so when it applies. This works best on technical, definitional, or argument-driven documents, where pages *assert* things. It is weaker on narrative nonfiction and fiction, and on books where the worked examples *are* the argument — there, compressing to facts throws away the substance. Tell the user when the document is a poor fit rather than forcing it.