#!/usr/bin/env python3
"""Generate genailab/llm-benchmarks/llmbenchmarks.html and one page per benchmark.

Usage:  python build.py [output_dir]
Edit the data_*.py files to change content; re-run to regenerate.
"""
import html, json, os, sys, re
from data_nli import NLI
from data_rc import RC
from data_qa_cs import QA, CS
from data_lm import LM
from data_cls_gen import CLS, SUITES, GEN, SYN

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..")
UPDATED = "October 2026"

CATS = {
    "nli":         ("NLI",                        "#6366f1"),
    "rc":          ("Reading Comprehension",      "#0ea5e9"),
    "qa":          ("Question Answering",         "#10b981"),
    "commonsense": ("Commonsense Reasoning",      "#f59e0b"),
    "lm":          ("Language Modeling",          "#f43f5e"),
    "cls":         ("Similarity & Classification","#8b5cf6"),
    "suite":       ("Benchmark Suites",           "#14b8a6"),
    "gen":         ("Generation",                 "#ec4899"),
    "synthetic":   ("Synthetic / Probing",        "#64748b"),
}
CATS_SHORT = {"nli": "NLI", "rc": "Reading Comp.", "qa": "QA", "commonsense": "Commonsense", "lm": "Language Modeling", "cls": "Similarity & Cls.", "suite": "Suite", "gen": "Generation", "synthetic": "Synthetic"}
PAPERS = {"GPT-1": "#1a1a18", "GPT-2": "#c85c2a", "GPT-3": "#0f766e"}

ALL = NLI + RC + QA + CS + LM + CLS + SUITES + GEN + SYN
ORDER = list(CATS.keys())
ALL.sort(key=lambda b: (ORDER.index(b["category"]), b["name"].lower()))

E = html.escape

def hex_rgb(h):
    h = h.lstrip("#"); return ",".join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))

MONTHS = ("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")
def short_date(label):
    """'Oct 2019' -> "Oct'19"; a bare year or a range is left as is."""
    m = re.fullmatch(r"(%s) (\d{4})" % "|".join(MONTHS), label.strip())
    return f"{m.group(1)}'{m.group(2)[2:]}" if m else label

def papers_used(b):
    seen = []
    for g in b["gpt"]:
        if g["paper"] not in seen: seen.append(g["paper"])
    return seen

# ──────────────────────────────────────────────────────────────────────────
# Shared chrome
# ──────────────────────────────────────────────────────────────────────────
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>\n  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Google+Sans+Flex:opsz,wght@6..144,300..800&family=Fira+Code:wght@400;500;700&display=swap" rel="stylesheet"/>'

def nav(back_href, back_label, depth):
    logo = "../" * depth + "images/Main_Logo.svg"
    return f'''<nav>
  <div class="nav-inner">
    <a href="https://sumitkant.github.io/" class="nav-logo">
      <object type="image/svg+xml" data="{logo}" height="60" style="display:block; pointer-events:none;"></object>
    </a>
    <a href="{back_href}" class="nav-back"><svg viewBox="0 0 24 24"><polyline points="15 18 9 12 15 6"/></svg>{back_label}</a>
  </div>
</nav>'''

BASE_CSS = """
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { font-size: 16px; scroll-behavior: smooth; }
    body { background: var(--bg); color: var(--text-primary); font-family: var(--font); -webkit-font-smoothing: antialiased; line-height: 1.6; min-height: 100vh; position: relative; overflow-x: hidden; }
    a { color: inherit; text-decoration: none; }
    h1, h2, h3, .hero-title, .tile h3, .sec-head h2, .stat b, .sota-box .big, .pager a { font-family: var(--font-head); }
    /* static ambient wash — cheap to paint (no filter: blur, no animation) */
    .ambient { position: fixed; inset: 0; z-index: 0; pointer-events: none;
      background:
        radial-gradient(640px 640px at 8% 0%, rgba(199,210,254,.75), transparent 70%),
        radial-gradient(600px 600px at 100% 18%, rgba(253,230,138,.7), transparent 70%),
        radial-gradient(560px 560px at 38% 70%, rgba(186,230,253,.65), transparent 70%),
        radial-gradient(500px 500px at 85% 100%, rgba(251,207,232,.6), transparent 70%); }
    .ambient span { display: none; }
    .grain { position: fixed; inset: 0; z-index: 0; pointer-events: none; opacity: .35; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .07 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }
    nav { position: sticky; top: 0; z-index: 200; height: var(--nav-h); background: rgba(242,239,233,.9); border-bottom: 1px solid var(--border); }
    .nav-inner { max-width: var(--content-w); margin: 0 auto; padding: 0 2rem; height: 100%; display: flex; align-items: center; justify-content: space-between; }
    .nav-back { display: flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 500; color: var(--text-secondary); transition: color .15s; }
    .nav-back:hover { color: var(--text-primary); }
    .nav-back svg { width: 14px; height: 14px; stroke: currentColor; fill: none; stroke-width: 2; }
    .page { position: relative; z-index: 1; max-width: var(--content-w); margin: 0 auto; padding: 0 2rem 5rem; }
    .glass { background: rgba(255,255,255,.62); border: 1px solid rgba(255,255,255,.8); box-shadow: 0 1px 0 rgba(255,255,255,.7) inset, 0 10px 30px -12px rgba(26,26,24,.16); border-radius: var(--radius); }
    .tile.glass, .filters.glass { backdrop-filter: blur(14px) saturate(1.4); -webkit-backdrop-filter: blur(14px) saturate(1.4); background: rgba(255,255,255,.5); }
    .pill { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 999px; font-size: 11px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; line-height: 1.3; white-space: nowrap; }
    .pill::before { content: ''; width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
    .chip { display: inline-flex; align-items: center; padding: 2px 8px; border-radius: 6px; font-size: 10.5px; font-weight: 700; font-family: var(--mono); letter-spacing: .02em; color: #fff; white-space: nowrap; }
    footer.site { position: relative; z-index: 1; max-width: var(--content-w); margin: 0 auto; padding: 1.5rem 2rem 3rem; font-size: 12.5px; color: var(--text-tertiary); display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px; }
    footer.site a { color: var(--text-secondary); }
    @media (max-width: 640px) { .page { padding: 0 1rem 4rem; } .nav-inner { padding: 0 1rem; } footer.site { padding: 1.5rem 1rem 3rem; } }
"""

VARS = """
    :root {
      --bg: #f2efe9; --border: rgba(0,0,0,.08);
      --text-primary: #1a1a18; --text-secondary: #6b6b65; --text-tertiary: #a8a8a0;
      --accent: #c85c2a; --font: 'Google Sans Flex', system-ui, sans-serif; --font-head: 'Plus Jakarta Sans', 'Google Sans Flex', system-ui, sans-serif; --mono: 'Fira Code', ui-monospace, monospace;
      --radius: 18px; --nav-h: 72px; --content-w: 1100px;
    }
"""

def footer(depth):
    return f'''<footer class="site">
  <span>Sumit Kant · GenAI Lab · LLM Benchmarks · updated {UPDATED}</span>
  <span><a href="{'../' * depth}genai-lab.html">GenAI Lab</a> · <a href="{'../' * depth}blog.html">Blog</a></span>
</footer>'''

# ──────────────────────────────────────────────────────────────────────────
# Index page
# ──────────────────────────────────────────────────────────────────────────
INDEX_CSS = """
    body.index nav { background: transparent; border-bottom-color: transparent; transition: background .25s, border-color .25s; }
    body.index nav.solid { background: rgba(242,239,233,.9); border-bottom-color: var(--border); }
    .hero-band { position: relative; z-index: 1; margin-top: calc(-1 * var(--nav-h)); padding-top: var(--nav-h); margin-bottom: 22px; width: 100%; background: var(--bg) url('llmbenchmarks-hero.jpg') no-repeat; background-size: 100% auto; background-position: center 50%; }
    .hero-band::before { content: ''; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(242,239,233,.55) 0%, rgba(242,239,233,.35) 22%, rgba(242,239,233,0) 42%); }
    .hero-band::after { content: ''; position: absolute; left: 0; right: 0; bottom: 0; height: 70px; background: linear-gradient(180deg, rgba(242,239,233,0), var(--bg)); }
    .hero { position: relative; z-index: 1; max-width: var(--content-w); margin: 0 auto; padding: 2.2rem 2rem 3rem; height: clamp(300px, 27.5vw, 540px); display: flex; flex-direction: column; justify-content: center; }
    @media (max-width: 900px) { .hero-band { background-size: cover; background-position: 70% 50%; } .hero-band::before { background: linear-gradient(90deg, rgba(242,239,233,.9) 0%, rgba(242,239,233,.7) 55%, rgba(242,239,233,.5) 100%); } .hero { height: auto; min-height: 280px; padding: 2.4rem 1rem 3rem; } }
    .hero-sub { max-width: 400px; }
    @media (max-width: 760px) { .hero-band { background-position: 70% 45%; } .hero-band::before { background: linear-gradient(90deg, rgba(242,239,233,.94) 0%, rgba(242,239,233,.8) 60%, rgba(242,239,233,.55) 100%); } .hero { min-height: 300px; padding: 2.6rem 1rem 3.4rem; } }
    .hero-eyebrow { font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: var(--text-tertiary); font-weight: 600; margin-bottom: 10px; }
    .hero-title { font-size: clamp(2rem, 5vw, 3.1rem); font-weight: 800; line-height: 1.08; letter-spacing: -.03em; margin-bottom: 12px; }
    .hero-title strong { color: var(--accent); font-weight: 800; }
    .hero-sub { font-size: 15.5px; color: #3d3d39; line-height: 1.65; }
    .hero-stats { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 20px; }
    .stat { padding: 10px 16px; border-radius: 14px; display: flex; flex-direction: column; min-width: 110px; }
    .stat b { font-size: 22px; font-weight: 800; letter-spacing: -.02em; line-height: 1.1; }
    .stat span { font-size: 11px; color: var(--text-secondary); font-weight: 500; text-transform: uppercase; letter-spacing: .06em; margin-top: 2px; }

    .filters { position: sticky; top: calc(var(--nav-h) + 10px); z-index: 50; padding: 14px 16px; margin: 0 0 22px; display: flex; flex-direction: column; gap: 10px; }
    .filters-row { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
    .search { flex: 1 1 240px; display: flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 12px; background: rgba(255,255,255,.6); border: 1px solid rgba(0,0,0,.06); }
    .search svg { width: 15px; height: 15px; stroke: var(--text-tertiary); fill: none; stroke-width: 2; flex-shrink: 0; }
    .search input { flex: 1; border: 0; background: transparent; font: inherit; font-size: 13.5px; color: var(--text-primary); outline: none; min-width: 0; }
    .search input::placeholder { color: var(--text-tertiary); }
    .fbtn { font: inherit; font-size: 12px; font-weight: 600; padding: 6px 12px; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background: rgba(255,255,255,.5); color: var(--text-secondary); cursor: pointer; transition: all .15s; display: inline-flex; align-items: center; gap: 7px; }
    .fbtn:hover { background: rgba(255,255,255,.85); color: var(--text-primary); }
    .fbtn .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--c, var(--text-tertiary)); box-shadow: 0 0 0 3px rgba(var(--crgb, 0,0,0), .15); }
    .fbtn.active { background: var(--c, var(--text-primary)); border-color: transparent; color: #fff; }
    .fbtn.active .dot { background: #fff; box-shadow: none; }
    .fbtn.paper.active { background: var(--c); }
    .flabel { font-size: 10.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--text-tertiary); margin-right: 2px; }
    .fsep { width: 1px; height: 18px; background: rgba(0,0,0,.1); margin: 0 4px; }
    .count { margin-left: auto; font-size: 12px; color: var(--text-secondary); font-variant-numeric: tabular-nums; }
    select.sort { font: inherit; font-size: 12px; font-weight: 600; padding: 6px 10px; border-radius: 999px; border: 1px solid rgba(0,0,0,.08); background: rgba(255,255,255,.5); color: var(--text-secondary); cursor: pointer; }

    .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
    .tile { position: relative; display: flex; flex-direction: column; gap: 8px; padding: 16px 16px 14px; min-height: 230px; overflow: hidden; transition: transform .22s cubic-bezier(.2,.8,.2,1), box-shadow .22s, border-color .22s; --c: #999; }
    .tile::before { content: ''; position: absolute; inset: auto -55% -45% auto; width: 110%; height: 130%; background: radial-gradient(closest-side, rgba(var(--crgb), .34), transparent 72%); pointer-events: none; }
    .tile:hover { transform: translateY(-4px); box-shadow: 0 1px 0 rgba(255,255,255,.7) inset, 0 24px 40px -18px rgba(var(--crgb), .45); border-color: rgba(255,255,255,.95); }
    .tile.hidden { display: none; }
    .tile-top { display: flex; justify-content: space-between; align-items: center; gap: 8px; position: relative; }
    .tile .pill { color: var(--c); background: rgba(var(--crgb), .12); flex: 0 1 auto; min-width: 0; overflow: hidden; text-overflow: ellipsis; font-size: 10px; }
    .tile .pill::before { flex-shrink: 0; }
    .tile-papers { display: flex; gap: 4px; }
    .tile h3 { font-size: 17px; font-weight: 800; letter-spacing: -.02em; line-height: 1.15; position: relative; }
    .tile .full { font-size: 11.5px; color: var(--text-tertiary); margin-top: -6px; font-weight: 500; }
    .tile p { font-size: 12.5px; color: #3d3d39; line-height: 1.5; flex: 1; position: relative; }
    .tile-foot { display: block; padding-top: 10px; border-top: 1px dashed rgba(0,0,0,.1); font-size: 11.5px; color: var(--text-secondary); position: relative; }
    .tile-foot .lbl { display: block; font-size: 9.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--text-tertiary); margin-bottom: 1px; }
    .tile-foot b { font-size: 13px; color: var(--text-primary); font-weight: 700; }
    .tile-foot .sat { display: grid; grid-template-columns: auto 1fr; column-gap: 8px; align-items: center; }
    .tile-foot .sat .dot { width: 9px; height: 9px; border-radius: 50%; grid-row: span 2; }
    .tile-foot .sat.yes .dot { background: #10b981; box-shadow: 0 0 0 3px rgba(16,185,129,.18); }
    .tile-foot .sat.no .dot { background: #f59e0b; box-shadow: 0 0 0 3px rgba(245,158,11,.2); }
    .tile-foot .sat b { font-size: 12.5px; color: var(--text-primary); }
    .tile-foot .sat small { font-size: 11px; color: var(--text-secondary); }
    .tile-top .released { flex-shrink: 0; font-size: 11.5px; font-weight: 500; color: var(--text-tertiary); white-space: nowrap; }
    .tile-foot .sota .lbl { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .tile-foot .sota small { display: block; font-size: 10.5px; color: var(--text-tertiary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .empty { display: none; padding: 40px; text-align: center; color: var(--text-secondary); font-size: 14px; }
    .empty.show { display: block; }
    .legend { margin-top: 36px; padding: 18px 20px; display: flex; flex-wrap: wrap; gap: 8px 18px; font-size: 12px; color: var(--text-secondary); }
    .legend .pill { color: var(--c); background: rgba(var(--crgb), .12); }
    .legend .chip { margin-right: 2px; }
    @media (max-width: 1000px) { .grid { grid-template-columns: repeat(3, 1fr); } }
    @media (max-width: 760px) { .grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 600px) { .grid { grid-template-columns: 1fr; } .filters { position: static; } .count { margin-left: 0; width: 100%; } .tile { min-height: 0; } }
"""

def tile(b):
    name, color = CATS[b["category"]]
    chips = "".join(f'<span class="chip" style="background:{PAPERS[p]}" title="Evaluated in the {p} paper">{p}</span>' for p in papers_used(b))
    sota = b["sota"]
    sota_score = E(str(sota["score"]).split("·")[0].strip()) if b["category"] != "gen" or b["slug"] != "wmt-translation" else "per pair"
    sota_model = E(sota["model"].split("(")[0].split(" / ")[0].split(" · ")[0].strip())
    if b["slug"] == "gpt3-synthetic-tasks": sota_score, sota_model = "n/a", "no shared leaderboard"
    search = E(" ".join([b["name"], b["full"], b["desc"], name] + papers_used(b)).lower())
    return f'''<a class="tile glass" href="{b['slug']}.html" style="--c:{color};--crgb:{hex_rgb(color)}" data-cat="{b['category']}" data-papers="{' '.join(papers_used(b))}" data-year="{b['released']}" data-name="{E(b['name']).lower()}" data-search="{search}">
  <div class="tile-top"><span class="pill" title="{E(name)}">{E(CATS_SHORT[b['category']])}</span><span class="released" title="Released">{E(short_date(b['released_label']))}</span></div>
  <h3>{E(b['name'])}</h3>
  <div class="full">{E(b['full'])}</div>
  <p>{E(b['desc'])}</p>
  <div class="tile-foot">
    <div class="sat {'yes' if sota['saturated'] else 'no'}"><span class="dot"></span><b>{'Saturated' if sota['saturated'] else 'Not saturated'}</b><small>{'models at or beyond human level' if sota['saturated'] else 'models still below human level'}</small></div>
  </div>
</a>'''

def build_index():
    cat_btns = "".join(f'<button class="fbtn cat" data-cat="{k}" style="--c:{c};--crgb:{hex_rgb(c)}"><span class="dot"></span>{E(n)}</button>' for k, (n, c) in CATS.items())
    paper_btns = "".join(f'<button class="fbtn paper" data-paper="{p}" style="--c:{c};--crgb:{hex_rgb(c)}">{p}</button>' for p, c in PAPERS.items())
    tiles = "\n".join(tile(b) for b in ALL)
    legend = "".join(f'<span class="pill" style="--c:{c};--crgb:{hex_rgb(c)}">{E(n)} · {sum(1 for b in ALL if b["category"]==k)}</span>' for k, (n, c) in CATS.items())
    n_g1 = sum(1 for b in ALL if "GPT-1" in papers_used(b)); n_g2 = sum(1 for b in ALL if "GPT-2" in papers_used(b)); n_g3 = sum(1 for b in ALL if "GPT-3" in papers_used(b))
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="description" content="{len(ALL)} classic LLM benchmarks across {len(CATS)} categories — what each one tests, release dates, state-of-the-art scores and a dedicated page for each."/>
  <title>LLM Benchmarks — GenAI Lab — Sumit Kant</title>
  <meta property="og:type" content="website"/>
  <meta property="og:title" content="LLM Benchmarks — GenAI Lab"/>
  <meta property="og:description" content="The exams every language model had to sit before it was allowed to call itself intelligent."/>
  <meta property="og:url" content="https://sumitkant.github.io/genailab/llm-benchmarks/llmbenchmarks.html"/>
  <meta property="og:image" content="https://sumitkant.github.io/genailab/llm-benchmarks/llmbenchmarks-og.jpg"/>
  <meta property="og:image:width" content="1200"/><meta property="og:image:height" content="630"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="LLM Benchmarks — GenAI Lab"/>
  <meta name="twitter:description" content="The exams every language model had to sit before it was allowed to call itself intelligent."/>
  <meta name="twitter:image" content="https://sumitkant.github.io/genailab/llm-benchmarks/llmbenchmarks-og.jpg"/>
  {FONTS}
  <style>{VARS}{BASE_CSS}{INDEX_CSS}</style>
</head>
<body class="index">
<div class="ambient"><span class="b1"></span><span class="b2"></span><span class="b3"></span><span class="b4"></span></div>
<div class="grain"></div>
{nav("../../genai-lab.html", "GenAI Lab", 2)}
<div class="hero-band">
  <header class="hero">
    <p class="hero-eyebrow">GenAI Lab</p>
    <h1 class="hero-title">LLM <strong>Benchmarks</strong></h1>
    <p class="hero-sub">The exams every language model had to sit before it was allowed to call itself intelligent.</p>
  </header>
</div>
<main class="page">

  <section class="filters glass" aria-label="Filters">
    <div class="filters-row">
      <label class="search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.5" y2="16.5"/></svg><input id="q" type="search" placeholder="Search benchmarks and categories" autocomplete="off"/></label>
      <select class="sort" id="sort" aria-label="Sort"><option value="cat">Sort: category</option><option value="name">Sort: name</option><option value="year">Sort: year ↑</option><option value="year-desc">Sort: year ↓</option></select>
      <span class="count" id="count"></span>
    </div>
    <div class="filters-row">
      <span class="flabel">Category</span>
      <button class="fbtn cat active" data-cat="all" style="--c:#1a1a18;--crgb:26,26,24"><span class="dot"></span>All</button>{cat_btns}
    </div>
  </section>

  <section class="grid" id="grid">
{tiles}
  </section>
  <div class="empty" id="empty">Nothing matches that filter. Try clearing the search or picking another category.</div>

</main>
{footer(2)}
<script>
(function() {{
  const navEl = document.querySelector('nav'), band = document.querySelector('.hero-band');
  function navState() {{ navEl.classList.toggle('solid', window.scrollY > band.offsetHeight - navEl.offsetHeight - 10); }}
  window.addEventListener('scroll', navState, {{ passive: true }}); navState();
  const grid = document.getElementById('grid');
  const tiles = Array.from(grid.querySelectorAll('.tile'));
  const q = document.getElementById('q'), count = document.getElementById('count'), empty = document.getElementById('empty'), sort = document.getElementById('sort');
  const catBtns = Array.from(document.querySelectorAll('.fbtn.cat'));
  const paperBtns = Array.from(document.querySelectorAll('.fbtn.paper'));
  const catOrder = {json.dumps(ORDER)};
  let cat = 'all', papers = new Set();

  function apply() {{
    const needle = q.value.trim().toLowerCase();
    let shown = 0;
    tiles.forEach(t => {{
      const okCat = cat === 'all' || t.dataset.cat === cat;
      const tp = t.dataset.papers.split(' ');
      const okPaper = papers.size === 0 || [...papers].every(p => tp.includes(p));
      const okQ = !needle || t.dataset.search.includes(needle);
      const show = okCat && okPaper && okQ;
      t.classList.toggle('hidden', !show); if (show) shown++;
    }});
    count.textContent = shown + ' of ' + tiles.length;
    empty.classList.toggle('show', shown === 0);
    try {{ localStorage.setItem('llmb-filter', JSON.stringify({{cat, papers:[...papers], q:q.value, sort:sort.value}})); }} catch(e) {{}}
  }}
  function resort() {{
    const v = sort.value;
    const sorted = tiles.slice().sort((a,b) => {{
      if (v === 'name') return a.dataset.name.localeCompare(b.dataset.name);
      if (v === 'year') return (+a.dataset.year - +b.dataset.year) || a.dataset.name.localeCompare(b.dataset.name);
      if (v === 'year-desc') return (+b.dataset.year - +a.dataset.year) || a.dataset.name.localeCompare(b.dataset.name);
      return (catOrder.indexOf(a.dataset.cat) - catOrder.indexOf(b.dataset.cat)) || a.dataset.name.localeCompare(b.dataset.name);
    }});
    sorted.forEach(t => grid.appendChild(t));
  }}
  catBtns.forEach(b => b.addEventListener('click', () => {{ cat = b.dataset.cat; catBtns.forEach(x => x.classList.toggle('active', x === b)); apply(); }}));
  paperBtns.forEach(b => b.addEventListener('click', () => {{ const p = b.dataset.paper; if (papers.has(p)) papers.delete(p); else papers.add(p); b.classList.toggle('active', papers.has(p)); apply(); }}));
  q.addEventListener('input', apply);
  sort.addEventListener('change', () => {{ resort(); apply(); }});
  // deep-link: ?cat=nli&paper=GPT-2
  const u = new URLSearchParams(location.search);
  if (u.get('cat') && catOrder.includes(u.get('cat'))) {{ cat = u.get('cat'); catBtns.forEach(x => x.classList.toggle('active', x.dataset.cat === cat)); }}
  (u.get('paper') || '').split(',').filter(Boolean).forEach(p => {{ papers.add(p); const b = paperBtns.find(x => x.dataset.paper === p); if (b) b.classList.add('active'); }});
  if (!u.toString()) {{ try {{ const s = JSON.parse(localStorage.getItem('llmb-filter') || 'null'); if (s) {{ cat = s.cat || 'all'; catBtns.forEach(x => x.classList.toggle('active', x.dataset.cat === cat)); (s.papers||[]).forEach(p => {{ papers.add(p); const b = paperBtns.find(x => x.dataset.paper === p); if (b) b.classList.add('active'); }}); q.value = s.q || ''; sort.value = s.sort || 'cat'; resort(); }} }} catch(e) {{}} }}
  apply();
}})();
</script>
</body>
</html>
'''

# ──────────────────────────────────────────────────────────────────────────
# Detail pages
# ──────────────────────────────────────────────────────────────────────────
DETAIL_CSS = """
    .hero { padding: 3rem 0 2rem; display: grid; grid-template-columns: 1fr; gap: 18px; }
    .hero-eyebrow { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 10px; }
    .hero-eyebrow .pill { color: var(--c); background: rgba(var(--crgb), .14); }
    .hero-title { font-size: clamp(2rem, 5vw, 3.2rem); font-weight: 800; line-height: 1.05; letter-spacing: -.035em; }
    .hero-full { font-size: 14px; color: var(--text-tertiary); font-weight: 500; margin-top: 6px; }
    .hero-sub { font-size: 15.5px; color: var(--text-secondary); line-height: 1.7; max-width: 680px; margin-top: 12px; }
    .hero-meta { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 18px; }
    .badge { display: inline-flex; align-items: center; gap: 7px; padding: 7px 13px; border-radius: 999px; font-size: 12.5px; font-weight: 600; color: var(--text-secondary); }
    .badge b { color: var(--text-primary); }
    .badge svg { width: 13px; height: 13px; stroke: var(--c); fill: none; stroke-width: 2.2; }
    .badge.sota { background: rgba(var(--crgb), .14); border-color: rgba(var(--crgb), .25); color: var(--text-primary); }

    .layout { display: grid; grid-template-columns: minmax(0, 1fr) 220px; gap: 32px; align-items: start; }
    .toc { position: sticky; top: calc(var(--nav-h) + 20px); padding: 14px 6px 14px 14px; font-size: 12.5px; }
    .toc .flabel { display: block; font-size: 10px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--text-tertiary); margin-bottom: 8px; }
    .toc a { display: block; padding: 5px 8px; border-radius: 8px; color: var(--text-secondary); border-left: 2px solid transparent; }
    .toc a:hover { color: var(--text-primary); background: rgba(255,255,255,.5); }
    .toc a.active { color: var(--c); border-left-color: var(--c); font-weight: 600; }
    .toc .n { font-family: var(--mono); font-size: 10px; color: var(--text-tertiary); margin-right: 6px; }

    section.card { padding: 26px 28px; margin-bottom: 18px; scroll-margin-top: calc(var(--nav-h) + 16px); }
    .sec-head { display: flex; align-items: baseline; gap: 12px; margin-bottom: 14px; }
    .sec-num { font-family: var(--mono); font-size: 11px; font-weight: 700; color: var(--c); letter-spacing: .08em; }
    .sec-head h2 { font-size: 21px; font-weight: 800; letter-spacing: -.02em; }
    .lede { font-size: 13.5px; color: var(--text-secondary); margin: -6px 0 14px; }
    .prose p { font-size: 15px; line-height: 1.75; color: #2a2a27; margin-bottom: 14px; max-width: 70ch; }
    .prose p:last-child { margin-bottom: 0; }

    .facts { display: grid; grid-template-columns: 1fr 1fr; gap: 10px 22px; }
    .fact { padding: 10px 0; border-bottom: 1px dashed rgba(0,0,0,.1); }
    .fact .k { font-size: 10.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--text-tertiary); margin-bottom: 3px; }
    .fact .v { font-size: 13.5px; line-height: 1.5; }
    .paper-card { margin-top: 16px; padding: 14px 16px; border-radius: 12px; background: rgba(var(--crgb), .08); border: 1px solid rgba(var(--crgb), .18); display: flex; gap: 14px; align-items: flex-start; }
    .paper-card svg { width: 18px; height: 18px; stroke: var(--c); fill: none; stroke-width: 2; flex-shrink: 0; margin-top: 3px; }
    .paper-card .t { font-weight: 700; font-size: 14px; }
    .paper-card .a { font-size: 12.5px; color: var(--text-secondary); margin-top: 2px; }
    .paper-card a.l { display: inline-block; margin-top: 6px; font-size: 12px; font-weight: 600; color: var(--c); }

    .examples { display: grid; gap: 12px; }
    .ex { padding: 14px 16px; border-radius: 12px; background: rgba(255,255,255,.55); border: 1px solid rgba(0,0,0,.06); }
    .ex .t { font-size: 11px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--c); margin-bottom: 8px; }
    .ex .row { display: grid; grid-template-columns: 120px 1fr; gap: 10px; padding: 5px 0; font-size: 13.5px; line-height: 1.55; }
    .ex .row .k { font-size: 11px; font-weight: 700; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: .06em; padding-top: 3px; }
    .ex .row .v { white-space: pre-wrap; }
    .ex .ans { margin-top: 8px; padding: 8px 12px; border-radius: 8px; background: rgba(var(--crgb), .12); font-size: 13px; }
    .ex .ans b { color: var(--c); font-size: 10.5px; letter-spacing: .08em; text-transform: uppercase; margin-right: 8px; }

    .tablewrap { overflow-x: auto; }
    table.res { width: 100%; border-collapse: collapse; font-size: 13.5px; table-layout: fixed; }
    table.res col.c-paper { width: 70px; } table.res col.c-setting { width: 30%; } table.res col.c-score { width: 24%; }
    table.res th { text-align: left; font-size: 10.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--text-tertiary); padding: 8px 10px 8px 0; border-bottom: 1px solid rgba(0,0,0,.12); }
    table.res td { padding: 11px 10px 11px 0; border-bottom: 1px dashed rgba(0,0,0,.1); vertical-align: top; line-height: 1.5; overflow-wrap: anywhere; }
    table.res td.score { font-weight: 700; font-family: var(--mono); font-size: 12.5px; overflow-wrap: anywhere; }
    table.res td.score span { display: block; }
    table.res td.note { color: var(--text-secondary); font-size: 12.5px; }

    .sota-grid { display: grid; grid-template-columns: 1.2fr 1fr 1fr; gap: 14px; }
    .sota-box { padding: 16px 18px; border-radius: 14px; background: rgba(255,255,255,.55); border: 1px solid rgba(0,0,0,.06); }
    .sota-box .k { font-size: 10.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--text-tertiary); margin-bottom: 6px; }
    .sota-box .big { font-size: 30px; font-weight: 800; letter-spacing: -.03em; line-height: 1.05; color: var(--c); }
    .sota-box .big.sm { font-size: 17px; line-height: 1.3; }
    .sota-box .v { font-size: 14px; font-weight: 600; line-height: 1.4; }
    .sota-box .s { font-size: 12px; color: var(--text-secondary); margin-top: 4px; }
    .sat { display: inline-flex; align-items: center; gap: 6px; margin-top: 10px; padding: 4px 10px; border-radius: 999px; font-size: 11px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; }
    .sat.yes { background: rgba(16,185,129,.14); color: #047857; }
    .sat.no { background: rgba(245,158,11,.16); color: #b45309; }
    .sota-note { margin-top: 14px; font-size: 13px; color: var(--text-secondary); line-height: 1.6; }
    .sota-note a { color: var(--c); font-weight: 600; }

    .win { margin: 14px 0; border-radius: 12px; overflow: hidden; background: #16161a; border: 1px solid rgba(0,0,0,.25); box-shadow: 0 12px 28px -16px rgba(0,0,0,.5); }
    .win-bar { display: flex; align-items: center; gap: 8px; padding: 9px 14px; background: #202026; border-bottom: 1px solid rgba(255,255,255,.06); }
    .win-bar i { width: 10px; height: 10px; border-radius: 50%; background: #3a3a44; display: inline-block; }
    .win-bar i:nth-child(1) { background: #ff5f57; } .win-bar i:nth-child(2) { background: #febc2e; } .win-bar i:nth-child(3) { background: #28c840; }
    .win-bar span { margin-left: auto; font-family: var(--mono); font-size: 11px; color: #8a8a96; }
    .win pre { margin: 0; padding: 16px 18px; overflow-x: auto; font-family: var(--mono); font-size: 12.5px; line-height: 1.65; color: #e6e6ea; tab-size: 4; }
    .win pre .c { color: #7c7c8a; } .win pre .s { color: #a5d6a7; } .win pre .k { color: #c792ea; } .win pre .f { color: #82aaff; } .win pre .n { color: #f78c6c; }
    .step { font-size: 13.5px; font-weight: 700; margin: 18px 0 2px; display: flex; align-items: center; gap: 8px; }
    .step .no { width: 20px; height: 20px; border-radius: 6px; background: var(--c); color: #fff; font-size: 11px; display: inline-flex; align-items: center; justify-content: center; font-family: var(--mono); }
    .step-sub { font-size: 12.5px; color: var(--text-secondary); margin-bottom: 4px; }

    ul.plain { list-style: none; display: grid; gap: 8px; }
    ul.plain li { position: relative; padding-left: 20px; font-size: 14px; line-height: 1.6; color: #2a2a27; }
    ul.plain li::before { content: ''; position: absolute; left: 0; top: 10px; width: 8px; height: 8px; border-radius: 2px; background: var(--c); transform: rotate(45deg); opacity: .8; }
    ul.refs li a { color: var(--c); font-weight: 600; }
    ul.refs li small { display: block; color: var(--text-tertiary); font-family: var(--mono); font-size: 11px; word-break: break-all; }

    .pager { display: flex; justify-content: space-between; gap: 12px; margin-top: 10px; }
    .pager a { flex: 1; padding: 14px 16px; display: flex; flex-direction: column; gap: 2px; font-size: 14px; font-weight: 700; transition: transform .2s; }
    .pager a:hover { transform: translateY(-2px); }
    .pager a span { font-size: 10.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--text-tertiary); }
    .pager a.next { text-align: right; align-items: flex-end; }
    .pager a.all { flex: 0 0 auto; align-items: center; justify-content: center; color: var(--text-secondary); font-weight: 600; }
    @media (max-width: 900px) { .layout { grid-template-columns: 1fr; } .toc { display: none; } .sota-grid { grid-template-columns: 1fr; } .facts { grid-template-columns: 1fr; } }
    @media (max-width: 600px) { section.card { padding: 20px 16px; } .ex .row { grid-template-columns: 1fr; gap: 2px; } .pager { flex-direction: column; } .pager a.next { align-items: flex-start; text-align: left; } }
"""

def code(src, lang="python", title="python"):
    s = E(src)
    # light syntax tint
    s = re.sub(r"(#[^\n]*)", r'<span class="c">\1</span>', s)
    s = re.sub(r"(&quot;[^\n]*?&quot;|&#x27;[^\n]*?&#x27;)", r'<span class="s">\1</span>', s)
    s = re.sub(r"\b(import|from|for|in|def|return|if|else|with|as|print|lambda|not|and|or|None|True|False)\b", r'<span class="k">\1</span>', s)
    return f'<div class="win"><div class="win-bar"><i></i><i></i><i></i><span>{E(title)}</span></div><pre>{s}</pre></div>'

def quick_load(b):
    q = b["quick"]
    if not q["hf"]:
        return None
    cfg = f', "{q["config"]}"' if q["config"] and not q["config"].startswith("<") else (', "<task>"' if q["config"] else "")
    split = f', split="{q["split"]}"' if q["split"] else ""
    return f'''from datasets import load_dataset

ds = load_dataset("{q["hf"]}"{cfg}{split})
print(ds)            # columns: {q["fields"].split('.')[0][:90]}
print(ds[0])'''

SCORE_SNIPPETS = {
 "nli": '''# Score each label by the log-likelihood of its verbaliser after the pair (GPT-3 style)
LABELS = ["True", "Neither", "False"]      # entailment / neutral / contradiction
def prompt(ex): return f"{ex['premise']}\\nQuestion: {ex['hypothesis']} True, False, or Neither?\\nAnswer:"
correct = 0
for ex in ds:
    if ex["label"] < 0: continue
    scores = [loglik(prompt(ex), " " + lab) for lab in LABELS]
    correct += int(scores.index(max(scores)) == ex["label"])
print("accuracy", correct / len(ds))''',
 "nli2": '''LABELS = ["True", "False"]              # entailment / not_entailment
def prompt(ex):
    a = ex.get("premise") or ex.get("question"); b = ex.get("hypothesis") or ex.get("sentence")
    return f"{a}\\nQuestion: {b} True or False?\\nAnswer:"
acc = sum(int(max(range(2), key=lambda i: loglik(prompt(ex), " " + LABELS[i])) == ex["label"]) for ex in ds) / len(ds)
print("accuracy", acc)''',
 "pair_cls": '''# Binary pair classification: compare log P(" yes") vs log P(" no")
def prompt(ex):
    k = [c for c in ex if c not in ("label", "idx", "word")][:2]
    return f"Sentence 1: {ex[k[0]]}\\nSentence 2: {ex[k[1]]}\\nQuestion: Do these mean the same thing? yes or no?\\nAnswer:"
acc = sum(int((loglik(prompt(ex), " yes") > loglik(prompt(ex), " no")) == bool(ex["label"])) for ex in ds) / len(ds)
print("accuracy", acc)''',
 "single_cls": '''LABELS = {"sst2": ["negative", "positive"], "cola": ["unacceptable", "acceptable"]}["sst2"]  # pick the task
def prompt(ex): return f"{ex['sentence']}\\nQuestion: Is this sentence {LABELS[0]} or {LABELS[1]}?\\nAnswer:"
preds = [max(range(2), key=lambda i: loglik(prompt(ex), " " + LABELS[i])) for ex in ds]
from sklearn.metrics import accuracy_score, matthews_corrcoef
print("acc", accuracy_score(ds["label"], preds), "mcc", matthews_corrcoef(ds["label"], preds))''',
 "boolq": '''def prompt(ex): return f"{ex['passage']}\\nQuestion: {ex['question']}?\\nAnswer:"
acc = sum(int((loglik(prompt(ex), " yes") > loglik(prompt(ex), " no")) == bool(ex["label"])) for ex in ds) / len(ds)
print("accuracy", acc)''',
 "copa": '''def prompt(ex):
    conn = "because" if ex["question"] == "cause" else "so"
    return f"{ex['premise'][:-1]} {conn}"
def lower_first(s): return s[0].lower() + s[1:]
acc = 0
for ex in ds:
    s = [loglik(prompt(ex), " " + lower_first(ex[c])) for c in ("choice1", "choice2")]
    acc += int(s.index(max(s)) == ex["label"])
print("accuracy", acc / len(ds))''',
 "wsc": '''# Partial scoring: substitute each candidate into the sentence and score only the text *after* the blank
def split_on(ex):
    if "sentence" in ex:                      # WinoGrande: sentence with "_"
        pre, post = ex["sentence"].split("_"); opts = [ex["option1"], ex["option2"]]; gold = int(ex["answer"]) - 1
    else:                                     # SuperGLUE WSC: use span2 (pronoun) position
        t = ex["text"]; i = t.index(ex["span2_text"]); pre, post = t[:i], t[i + len(ex["span2_text"]):]
        opts = [ex["span1_text"]]; gold = ex["label"]
    return pre, post, opts, gold
acc = 0
for ex in ds:
    pre, post, opts, gold = split_on(ex)
    s = [loglik(pre + o, post) for o in opts]
    acc += int(s.index(max(s)) == gold)
print("accuracy", acc / len(ds))''',
 "mc_endings": '''# Multiple choice by length-normalised log-likelihood of each ending (acc_norm)
def choices(ex):
    if "endings" in ex: return ex["ctx"], ex["endings"], int(ex["label"])              # HellaSwag
    if "sol1" in ex:    return ex["goal"], [ex["sol1"], ex["sol2"]], ex["label"]       # PIQA
    story = " ".join(ex[f"input_sentence_{i}"] for i in range(1, 5))                  # Story Cloze
    return story, [ex["sentence_quiz1"], ex["sentence_quiz2"]], ex["answer_right_ending"] - 1
acc = 0
for ex in ds:
    ctx, ends, gold = choices(ex)
    s = [loglik(ctx, " " + e) / max(1, len(e)) for e in ends]
    acc += int(s.index(max(s)) == gold)
print("acc_norm", acc / len(ds))''',
 "mc_letters": '''# Science MC: score each option text as a continuation of "Question: … Answer:"
acc = 0
for ex in ds:
    q = ex.get("question") or ex["question_stem"]
    texts, labels = ex["choices"]["text"], ex["choices"]["label"]
    s = [loglik(f"Question: {q}\\nAnswer:", " " + t) / max(1, len(t)) for t in texts]
    acc += int(labels[s.index(max(s))] == ex["answerKey"])
print("acc_norm", acc / len(ds))''',
 "mc_passage": '''acc = 0
for ex in ds:
    ctx = f"Article: {ex['article']}\\n\\nQuestion: {ex['question']}\\nAnswer:"
    s = [loglik(ctx, " " + o) / max(1, len(o)) for o in ex["options"]]
    acc += int("ABCD"[s.index(max(s))] == ex["answer"])
print("accuracy", acc / len(ds))''',
 "record": '''acc = 0
for ex in ds:
    ctx = ex["passage"].replace("@highlight\\n", "- ") + "\\n"
    s = [loglik(ctx, ex["query"].replace("@placeholder", e)) for e in ex["entities"]]
    acc += int(ex["entities"][s.index(max(s))] in ex["answers"])
print("accuracy", acc / len(ds))''',
 "multirc": '''from collections import defaultdict
by_q = defaultdict(list)                     # group rows by question for EM
for ex in ds:
    p = f"{ex['paragraph']}\\nQuestion: {ex['question']}\\nCandidate answer: {ex['answer']}\\nIs the candidate correct? yes or no?\\nAnswer:"
    pred = int(loglik(p, " yes") > loglik(p, " no"))
    by_q[(ex["idx"]["paragraph"], ex["idx"]["question"])].append((pred, ex["label"]))
em = sum(all(p == g for p, g in v) for v in by_q.values()) / len(by_q)
preds = [p for v in by_q.values() for p, _ in v]; golds = [g for v in by_q.values() for _, g in v]
from sklearn.metrics import f1_score
print("F1a", f1_score(golds, preds), "EM", em)''',
 "lambada": '''# Predict the final word; count it correct only if the whole word is produced greedily
correct = 0
for ex in ds:
    ctx, target = ex["text"].rsplit(" ", 1)
    out = generate(ctx, max_new_tokens=8).strip().split()
    correct += int(out and out[0].strip(".,!?\\"'") == target.strip(".,!?\\"'"))
print("accuracy", correct / len(ds))''',
 "closed_qa": '''import re, string
def norm(s):
    s = s.lower(); s = "".join(c for c in s if c not in string.punctuation)
    s = re.sub(r"\\b(a|an|the)\\b", " ", s); return " ".join(s.split())
FEW = "Q: who wrote the novel 1984?\\nA: George Orwell\\n\\nQ: what is the capital of australia?\\nA: Canberra\\n\\n"
em = 0
for ex in ds:
    golds = ex.get("answer") or ex.get("answers") or ex["answer"]["aliases"]
    pred = generate(FEW + f"Q: {ex['question']}\\nA:", max_new_tokens=16, stop="\\n")
    em += int(norm(pred) in {norm(g) for g in golds})
print("exact match", em / len(ds))''',
 "gen_qa": '''import evaluate
metric = evaluate.load("squad_v2")           # for DROP use the official drop_eval.py from allenai/allennlp-reading-comprehension
preds, refs = [], []
for ex in ds:
    p = f"{ex['context'] if 'context' in ex else ex['passage']}\\nQuestion: {ex['question']}\\nAnswer (or 'unanswerable'):"
    out = generate(p, max_new_tokens=32, stop="\\n").strip()
    preds.append({"id": ex["id"], "prediction_text": "" if out.lower().startswith("unanswerable") else out, "no_answer_probability": float(out.lower().startswith("unanswerable"))})
    refs.append({"id": ex["id"], "answers": ex["answers"]})
print(metric.compute(predictions=preds, references=refs))''',
 "conv_qa": '''# Feed the running dialogue; score each turn with token-F1 against the references
def f1(pred, gold):
    p, g = pred.lower().split(), gold.lower().split(); common = sum(min(p.count(w), g.count(w)) for w in set(p))
    if not common: return 0.0
    pr, rc = common / len(p), common / len(g); return 2 * pr * rc / (pr + rc)
scores = []
for ex in ds:
    hist = ex["story"] + "\\n\\n"
    for q, a in zip(ex["questions"], ex["answers"]["input_text"]):
        pred = generate(hist + f"Q: {q}\\nA:", max_new_tokens=24, stop="\\n").strip()
        scores.append(f1(pred, a)); hist += f"Q: {q}\\nA: {a}\\n"
print("F1", sum(scores) / len(scores))''',
 "ppl": '''# Word-level perplexity with a sliding window (so every token sees up to max_len of context)
import torch, math
text = "\\n\\n".join(ds["text"]) if "text" in ds.column_names else "\\n".join(ds[ds.column_names[0]])
enc = tok(text, return_tensors="pt").input_ids[0]
max_len, stride, nll, n_tok = 1024, 512, 0.0, 0
for start in range(0, enc.size(0), stride):
    end = min(start + max_len, enc.size(0)); trg = end - start if start == 0 else min(stride, end - start)
    ids = enc[start:end].unsqueeze(0).to(model.device); labels = ids.clone(); labels[:, :-trg] = -100
    with torch.no_grad(): nll += model(ids, labels=labels).loss.item() * trg
    n_tok += trg
    if end == enc.size(0): break
n_words = len(text.split())
print("token ppl", math.exp(nll / n_tok), "| word ppl (comparable to GPT-2 table)", math.exp(nll / n_words))''',
 "bpb": '''import torch, math
raw = open("enwik8", "rb").read() if "enwik8" in DATASET else open("text8", "rb").read()
test = raw[95_000_000:]                       # standard split: last 5M bytes
text = test.decode("utf-8", errors="replace")
enc = tok(text, return_tensors="pt").input_ids[0]
nll, max_len, stride = 0.0, 1024, 1024
for i in range(0, enc.size(0) - 1, stride):
    ids = enc[i:i + max_len].unsqueeze(0).to(model.device)
    with torch.no_grad(): nll += model(ids, labels=ids).loss.item() * (ids.size(1) - 1)
print("bits per byte", nll / (math.log(2) * len(test)))''',
 "summ": '''import evaluate
rouge = evaluate.load("rouge")
preds, refs = [], []
for ex in ds.select(range(500)):
    out = generate(ex["article"][:6000] + "\\nTL;DR:", max_new_tokens=100)
    preds.append(" ".join(out.split(". ")[:3])); refs.append(ex["highlights"])
print(rouge.compute(predictions=preds, references=refs, use_stemmer=True))
lead3 = [" ".join(ex["article"].split(". ")[:3]) for ex in ds.select(range(500))]
print("lead-3 baseline", rouge.compute(predictions=lead3, references=refs, use_stemmer=True))''',
 "mt": '''import sacrebleu
src, tgt = "fr", "en"                          # direction: fr -> en
FEW = "".join(f"French: {ex['translation']['fr']} = English: {ex['translation']['en']}\\n" for ex in ds.select(range(5)))
hyps, refs = [], []
for ex in ds.select(range(5, 505)):
    out = generate(FEW + f"French: {ex['translation'][src]} = English:", max_new_tokens=96, stop="\\n")
    hyps.append(out.strip()); refs.append(ex["translation"][tgt])
print(sacrebleu.corpus_bleu(hyps, [refs]))     # report the signature too''',
 "regression": '''import re
from scipy.stats import pearsonr, spearmanr
preds, golds = [], []
for ex in ds:
    p = f"On a scale of 0 to 5, how similar are these sentences?\\n1: {ex['sentence1']}\\n2: {ex['sentence2']}\\nScore:"
    m = re.search(r"\\d+(\\.\\d+)?", generate(p, max_new_tokens=4)); preds.append(float(m.group()) if m else 2.5); golds.append(ex["label"])
print("pearson", pearsonr(preds, golds)[0], "spearman", spearmanr(preds, golds)[0])''',
 "cbt": '''acc = 0
for ex in ds:
    ctx = " ".join(ex["sentences"]) + " "
    s = [loglik(ctx, ex["question"].replace("XXXXX", o)) for o in ex["options"]]
    acc += int(ex["options"][s.index(max(s))] == ex["answer"])
print("accuracy", acc / len(ds))''',
 "suite": '''# Loop every task of the suite and compute the official metric with `evaluate`
import evaluate
TASKS = ["cola", "sst2", "mrpc", "qqp", "mnli", "qnli", "rte"]   # GLUE; for SuperGLUE use boolq, cb, copa, multirc, record, rte, wic, wsc.fixed
for t in TASKS:
    d = load_dataset(DATASET, t, split="validation" if t != "mnli" else "validation_matched")
    metric = evaluate.load(DATASET.split("/")[-1], t)
    preds = [predict(t, ex) for ex in d]      # your per-task prompting / scoring goes here
    print(t, metric.compute(predictions=preds, references=d["label"]))''',
 "synthetic": '''# Regenerate GPT-3's arithmetic probe: 2,000 random problems per sub-task, exact-match scoring
import random
def problems(digits, op, n=2000, seed=0):
    r = random.Random(seed); lo, hi = 10 ** (digits - 1), 10 ** digits - 1
    for _ in range(n):
        a, b = r.randint(lo, hi), r.randint(lo, hi)
        yield f"Q: What is {a} {'plus' if op == '+' else 'minus'} {b}?\\nA:", str(a + b if op == '+' else a - b)
FEW = "Q: What is 48 plus 76?\\nA: 124\\n\\nQ: What is 97 minus 29?\\nA: 68\\n\\n"
for d in (2, 3, 4, 5):
    for op in "+-":
        ps = list(problems(d, op)); ok = sum(generate(FEW + q, max_new_tokens=8, stop="\\n").strip() == a for q, a in ps)
        print(f"{d}-digit {op}: {ok / len(ps):.1%}")''',
}

HELPERS = '''import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL = "gpt2"                                   # or "Qwen/Qwen2.5-1.5B", "meta-llama/Llama-3.2-1B", …
tok = AutoTokenizer.from_pretrained(MODEL); model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.bfloat16).eval().to("cuda")

@torch.no_grad()
def loglik(context, continuation):
    """Sum of log-probs of `continuation` tokens given `context` — the standard multiple-choice scorer."""
    ids = tok(context + continuation, return_tensors="pt").input_ids.to(model.device)
    n_ctx = len(tok(context).input_ids)
    logp = model(ids).logits.log_softmax(-1)[0, :-1]
    return logp.gather(1, ids[0, 1:, None])[n_ctx - 1:].sum().item()

@torch.no_grad()
def generate(prompt, max_new_tokens=32, stop=None):
    ids = tok(prompt, return_tensors="pt").input_ids.to(model.device)
    out = model.generate(ids, max_new_tokens=max_new_tokens, do_sample=False, pad_token_id=tok.eos_token_id)
    text = tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True)
    return text.split(stop)[0] if stop else text'''

def quickstart(b):
    q = b["quick"]; parts = []
    parts.append('<div class="step"><span class="no">1</span>Install</div>')
    parts.append(code("pip install -U datasets transformers evaluate lm-eval sacrebleu rouge-score scikit-learn", "bash", "shell"))
    parts.append('<div class="step"><span class="no">2</span>Load the data</div>')
    parts.append(f'<p class="step-sub">{E(q["fields"])}</p>')
    load = quick_load(b)
    if load: parts.append(code(load, title="python · load"))
    elif b["slug"] == "text8": parts.append(code("curl -LO http://mattmahoney.net/dc/text8.zip && unzip text8.zip   # one 100,000,000-character file", "bash", "shell"))
    elif b["slug"] == "gpt3-synthetic-tasks": parts.append(code('from datasets import load_dataset\nds = load_dataset("EleutherAI/arithmetic", "arithmetic_2da", split="validation")   # 2-digit addition, regenerated by EleutherAI\nprint(ds[0])', title="python · load"))
    parts.append('<div class="step"><span class="no">3</span>Score a model</div>')
    parts.append('<p class="step-sub">Two helpers cover every benchmark in this collection: <code>loglik</code> for anything multiple-choice (score each option, pick the highest) and <code>generate</code> for anything free-form. Swap <code>MODEL</code> for whatever you are evaluating.</p>')
    parts.append(code(HELPERS, title="python · helpers"))
    snippet = SCORE_SNIPPETS[q["kind"]]
    if q["kind"] in ("bpb", "suite"): snippet = f'DATASET = "{q["hf"] or b["slug"]}"\n' + snippet
    parts.append(code(snippet, title="python · evaluate"))
    if q["lmeval"]:
        parts.append('<div class="step"><span class="no">4</span>Or use lm-evaluation-harness</div>')
        task = q["lmeval"].split(" (")[0].split(" ·")[0].split(",")[0].strip()
        parts.append(f'<p class="step-sub">Task name(s): <code>{E(q["lmeval"])}</code>. The harness reproduces the GPT-3 prompt formats and reports the standard metric.</p>')
        parts.append(code(f'lm_eval --model hf --model_args pretrained={"gpt2"},dtype=bfloat16 \\\n        --tasks {task} --num_fewshot 0 --batch_size auto --output_path results/', "bash", "shell"))
    return "\n".join(parts)

def build_detail(i, b):
    cname, color = CATS[b["category"]]
    prev_b = ALL[i - 1] if i > 0 else ALL[-1]; next_b = ALL[(i + 1) % len(ALL)]
    chips = "".join(f'<span class="chip" style="background:{PAPERS[p]}">{p}</span>' for p in papers_used(b))
    facts = "".join(f'<div class="fact"><div class="k">{E(k)}</div><div class="v">{E(v)}</div></div>' for k, v in b["facts"])
    what = "".join(f"<p>{E(p)}</p>" for p in b["what"])
    exs = ""
    for ex in b["examples"]:
        rows = "".join(f'<div class="row"><div class="k">{E(k)}</div><div class="v">{E(v)}</div></div>' for k, v in ex["fields"])
        t = f'<div class="t">{E(ex["title"])}</div>' if ex["title"] else ""
        ans = f'<div class="ans"><b>Answer</b>{E(ex["answer"])}</div>' if ex["answer"] and ex["answer"] != "—" else ""
        exs += f'<div class="ex">{t}{rows}{ans}</div>'
    gpt_rows = "".join(f'<tr><td><span class="chip" style="background:{PAPERS[g["paper"]]}">{g["paper"]}</span></td><td>{E(g["setting"])}</td><td class="score">{"".join(f"<span>{E(x.strip())}</span>" for x in g["score"].split(" · "))}</td><td class="note">{E(g["note"])}</td></tr>' for g in b["gpt"])
    s = b["sota"]
    big_cls = "big sm" if len(str(s["score"])) > 14 else "big"
    sat = '<span class="sat yes">✓ saturated · at or above human level</span>' if s["saturated"] else '<span class="sat no">open · below human level</span>'
    if s["human"] in ("n/a",) or s["human"].startswith("not"): sat = '<span class="sat no">no human baseline</span>' if not s["saturated"] else '<span class="sat yes">✓ effectively saturated</span>'
    pit = "".join(f"<li>{E(p)}</li>" for p in b["pitfalls"])
    refs = "".join(f'<li><a href="{E(u)}" target="_blank" rel="noopener">{E(l)}</a><small>{E(u)}</small></li>' for l, u in b["refs"])
    hf_link = f'<a class="l" href="https://huggingface.co/datasets/{b["quick"]["hf"]}" target="_blank" rel="noopener">Hugging Face ↗</a>' if b["quick"]["hf"] else ""
    sections = [("glance", "At a glance"), ("what", "What it tests"), ("examples", "Examples"), ("gpt", "Reported results"), ("sota", "State of the art"), ("quickstart", "Quickstart"), ("pitfalls", "Pitfalls"), ("refs", "References")]
    toc = "".join(f'<a href="#{sid}"><span class="n">{n:02d}</span>{E(t)}</a>' for n, (sid, t) in enumerate(sections, 1))
    cat_link = f'llmbenchmarks.html?cat={b["category"]}'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="description" content="{E(b['name'])} — {E(b['desc'])}"/>
  <title>{E(b['name'])} — LLM Benchmarks — GenAI Lab</title>
  {FONTS}
  <style>{VARS}{BASE_CSS}{DETAIL_CSS}
    :root {{ --c: {color}; --crgb: {hex_rgb(color)}; }}
    .ambient {{ background: radial-gradient(640px 640px at 8% 0%, rgba({hex_rgb(color)},.28), transparent 70%), radial-gradient(600px 600px at 100% 18%, rgba(253,230,138,.6), transparent 70%), radial-gradient(560px 560px at 38% 70%, rgba(186,230,253,.55), transparent 70%); }}
  </style>
</head>
<body>
<div class="ambient"><span class="b1"></span><span class="b2"></span><span class="b3"></span><span class="b4"></span></div>
<div class="grain"></div>
{nav("llmbenchmarks.html", "LLM Benchmarks", 2)}
<main class="page">
  <header class="hero">
    <div>
      <div class="hero-eyebrow"><a class="pill" href="{cat_link}">{E(cname)}</a>{chips}</div>
      <h1 class="hero-title">{E(b['name'])}</h1>
      <div class="hero-full">{E(b['full'])}</div>
      <p class="hero-sub">{E(b['desc'])}</p>
      <div class="hero-meta">
        <span class="badge glass"><svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>Released <b>{E(b['released_label'])}</b></span>
        <span class="badge glass"><svg viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>Metric <b>{E(s['metric'])}</b></span>
        <span class="badge glass sota"><svg viewBox="0 0 24 24"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>SOTA <b>{E(str(s['score']))}</b> · {E(s['model'].split('(')[0].strip())} ({s['year']})</span>
      </div>
    </div>
  </header>

  <div class="layout">
    <div>
      <section class="card glass" id="glance">
        <div class="sec-head"><span class="sec-num">01</span><h2>At a glance</h2></div>
        <div class="facts">{facts}</div>
        <div class="paper-card">
          <svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
          <div><div class="t">{E(b['paper']['title'])}</div><div class="a">{E(b['paper']['authors'])} · {E(b['paper']['venue'])}</div>
          <a class="l" href="{E(b['paper']['url'])}" target="_blank" rel="noopener">Read the paper ↗</a> {hf_link}</div>
        </div>
      </section>

      <section class="card glass prose" id="what">
        <div class="sec-head"><span class="sec-num">02</span><h2>What it tests</h2></div>
        {what}
      </section>

      <section class="card glass" id="examples">
        <div class="sec-head"><span class="sec-num">03</span><h2>Examples</h2></div>
        <p class="lede">Items from the dataset (or representative items where the originals are not freely redistributable).</p>
        <div class="examples">{exs}</div>
      </section>

      <section class="card glass" id="gpt">
        <div class="sec-head"><span class="sec-num">04</span><h2>Reported results</h2></div>
        <p class="lede">Scores reported on this benchmark, with the evaluation setting each one used.</p>
        <div class="tablewrap"><table class="res"><colgroup><col class="c-paper"/><col class="c-setting"/><col class="c-score"/><col/></colgroup><thead><tr><th>Paper</th><th>Setting</th><th>Reported</th><th>Context</th></tr></thead><tbody>{gpt_rows}</tbody></table></div>
      </section>

      <section class="card glass" id="sota">
        <div class="sec-head"><span class="sec-num">05</span><h2>State of the art</h2></div>
        <div class="sota-grid">
          <div class="sota-box"><div class="k">Best known · {E(s['metric'])}</div><div class="{big_cls}">{E(str(s['score']))}</div>{sat}</div>
          <div class="sota-box"><div class="k">Model</div><div class="v">{E(s['model'])}</div><div class="s">{s['year']}</div></div>
          <div class="sota-box"><div class="k">Human baseline</div><div class="v">{E(s['human'])}</div></div>
        </div>
        <p class="sota-note">{E(s['note'])} Source: <a href="{E(s['source'])}" target="_blank" rel="noopener">{E(s['source'].replace('https://','').split('/')[0])} ↗</a> · checked {UPDATED}.</p>
      </section>

      <section class="card glass" id="quickstart">
        <div class="sec-head"><span class="sec-num">06</span><h2>Quickstart</h2></div>
        <p class="lede">Load the benchmark and score a Hugging Face causal LM on it in a few lines.</p>
        {quickstart(b)}
      </section>

      <section class="card glass" id="pitfalls">
        <div class="sec-head"><span class="sec-num">07</span><h2>Pitfalls</h2></div>
        <ul class="plain">{pit}</ul>
      </section>

      <section class="card glass" id="refs">
        <div class="sec-head"><span class="sec-num">08</span><h2>References</h2></div>
        <ul class="plain refs">{refs}</ul>
      </section>

      <nav class="pager">
        <a class="glass prev" href="{prev_b['slug']}.html"><span>← Previous</span>{E(prev_b['name'])}</a>
        <a class="glass all" href="llmbenchmarks.html">All benchmarks</a>
        <a class="glass next" href="{next_b['slug']}.html"><span>Next →</span>{E(next_b['name'])}</a>
      </nav>
    </div>
    <aside class="toc glass"><span class="flabel">On this page</span>{toc}</aside>
  </div>
</main>
{footer(2)}
<script>
(function() {{
  const links = Array.from(document.querySelectorAll('.toc a'));
  const secs = links.map(a => document.querySelector(a.getAttribute('href')));
  function update() {{
    const y = window.scrollY + 160; let idx = 0;
    secs.forEach((s, i) => {{ if (s && s.offsetTop <= y) idx = i; }});
    links.forEach((l, j) => l.classList.toggle('active', idx === j));
  }}
  window.addEventListener('scroll', update, {{ passive: true }}); update();
}})();
</script>
</body>
</html>
'''

def main():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "llmbenchmarks.html"), "w", encoding="utf-8") as f: f.write(build_index())
    for i, b in enumerate(ALL):
        with open(os.path.join(OUT, f"{b['slug']}.html"), "w", encoding="utf-8") as f: f.write(build_detail(i, b))
    # machine-readable manifest for the GenAI Lab page / future use
    manifest = [{"slug": b["slug"], "name": b["name"], "category": CATS[b["category"]][0], "released": b["released_label"], "papers": papers_used(b), "sota": b["sota"]["score"], "sota_model": b["sota"]["model"], "desc": b["desc"]} for b in ALL]
    with open(os.path.join(OUT, "benchmarks.json"), "w", encoding="utf-8") as f: json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"wrote index + {len(ALL)} pages to {OUT}")

if __name__ == "__main__":
    main()
