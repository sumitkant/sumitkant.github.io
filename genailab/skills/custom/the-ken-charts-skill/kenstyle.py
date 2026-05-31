"""
kenstyle.py — house-style helpers for replicating "The Ken" data visualizations
in Plotly, with a pure-Plotly INTERACTIVE pipeline (HTML output, no Chrome/Kaleido).

Design notes captured from reverse-engineering The Ken's graphics:

  Typography
  ----------
  • "serif" headlines  → high-contrast serif display (Playfair Display here;
    Tiempos Headline in originals). Used on 2021-onwards pieces.
  • "heavy" headlines  → ultra-bold sans, ALL-CAPS (Archivo Black here). Older
    2019-2020 pieces.
  • body / data labels → clean grotesque sans (Libre Franklin here).

  Canvas
  ------
  • Warm off-white (#F7F4EF) for newer pieces; pure white for older ones.
  • Footer row: "◁ THE KEN" wordmark left, "Graphic by <name>, <date>" centre,
    "Source: <src>" right — muted grey.

  Layout trick (important!)
  -------------------------
  Plotly annotation `yref="paper"` is *plot-area* relative, which makes it
  fiddly to drop a title into a big top margin. So we keep margins SMALL and
  instead carve the plotting region out with axis `domain`. That leaves clean
  [0,1] paper bands: header above the plot, footer below — both addressable
  with intuitive y values (≈0.95 for title, ≈0.02 for footer).

Pipeline
--------
  fig = ks.canvas(...)        # blank styled figure with a plot band
  ... add traces on the carved axes ...
  ks.header(...); ks.footer(...)
  ks.render(fig, "my_chart")  # writes interactive HTML you can open in a browser
"""

import os
import math
import plotly.graph_objects as go
import plotly.io as pio

# ── Fonts ────────────────────────────────────────────────────────────────
SERIF = "Playfair Display, Georgia, serif"
HEAVY = "Archivo Black, Arial Black, sans-serif"
BODY  = "Libre Franklin, Arial, sans-serif"

# ── Canvas colours ───────────────────────────────────────────────────────
CREAM   = "#F7F4EF"
WHITE   = "#FFFFFF"
INK     = "#1A1A1A"
GREY    = "#9A958C"
GREY_LT = "#C9C4BC"
PANEL   = "#ECEAE5"

# ── Recurring Ken palette ──────────────────────────────────────────────────
KEN = dict(
    teal="#15A89C", teal_dk="#0F7C73", cyan="#36C5E0", cyan_lt="#7FD8E8",
    sky="#4FB0E6", magenta="#E5179E", pink="#F06FB0", gold="#F5B81E",
    amber="#F39237", orange="#F47B3F", purple="#7E6FD0", purple_dk="#5B3F9E",
    grape="#8E44AD", green="#3DBB3D", lime="#C6D63C", navy="#1F3A93",
    blue="#1E63D0", red="#E23B2E", maroon="#7A0E22",
)

OUTDIR = os.environ.get("KEN_OUTDIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "html"))


# ── Blank styled canvas ────────────────────────────────────────────────────
def canvas(width=1000, height=720, bg=CREAM,
           plot_x=(0.0, 1.0), plot_y=(0.10, 0.78)):
    """
    Return a styled, blank figure. The primary data axes ('x','y') are placed in
    the given paper-space domains, leaving a header band above plot_y[1] and a
    footer band below plot_y[0]. Margins are tiny so paper-space ≈ figure-space.
    """
    fig = go.Figure()
    fig.update_layout(
        width=width, height=height,
        paper_bgcolor=bg, plot_bgcolor=bg,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family=BODY, color=INK, size=15),
        showlegend=False,
        xaxis=dict(domain=list(plot_x), visible=False, fixedrange=True),
        yaxis=dict(domain=list(plot_y), visible=False, fixedrange=True),
    )
    return fig


# ── Header ──────────────────────────────────────────────────────────────────
def header(fig, title, subtitle=None, style="serif",
           title_size=48, subtitle_size=19, x=0.5, anchor="center",
           y_title=0.96, y_sub=None, color=INK, sub_color=INK):
    fam = SERIF if style == "serif" else HEAVY
    txt = title.upper() if style == "heavy" else title
    fig.add_annotation(
        xref="paper", yref="paper", x=x, y=y_title,
        xanchor=anchor, yanchor="top", align=anchor, showarrow=False,
        text=f"<b>{txt}</b>",
        font=dict(family=fam, size=title_size, color=color),
    )
    if subtitle:
        if y_sub is None:
            y_sub = y_title - (title_size / fig.layout.height) * 1.35
        fig.add_annotation(
            xref="paper", yref="paper", x=x, y=y_sub,
            xanchor=anchor, yanchor="top", align=anchor, showarrow=False,
            text=subtitle,
            font=dict(family=BODY, size=subtitle_size, color=sub_color),
        )
    return fig


# ── Footer ───────────────────────────────────────────────────────────────────
def footer(fig, graphic_by=None, source=None, y=0.015,
           wordmark="THE KEN", brand_color=INK):
    fig.add_annotation(
        xref="paper", yref="paper", x=0.0, y=y, xanchor="left", yanchor="bottom",
        text=f"<b>◁ {wordmark}</b>", showarrow=False,
        font=dict(family=HEAVY, size=15, color=brand_color))
    if graphic_by:
        fig.add_annotation(
            xref="paper", yref="paper", x=0.5, y=y, xanchor="center", yanchor="bottom",
            text=graphic_by, showarrow=False,
            font=dict(family=BODY, size=12, color=GREY))
    if source:
        fig.add_annotation(
            xref="paper", yref="paper", x=1.0, y=y, xanchor="right", yanchor="bottom",
            text=source, showarrow=False,
            font=dict(family=BODY, size=12, color=GREY))
    return fig


# ── Manual coloured-chip legend (square/line markers) ─────────────────────────
def legend_chips(fig, items, y, xs=None, x_start=0.10, gap=0.20, size=16,
                 glyph="■", color=INK):
    """items: list of (label, color). Place left-to-right at paper-y."""
    if xs is None:
        xs = [x_start + i * gap for i in range(len(items))]
    for (label, c), xx in zip(items, xs):
        fig.add_annotation(
            xref="paper", yref="paper", x=xx, y=y, xanchor="left", yanchor="middle",
            showarrow=False,
            text=f"<span style='color:{c}'>{glyph}</span> {label}",
            font=dict(family=BODY, size=size, color=color))
    return fig


# ── Rounded-rectangle SVG path (for pill / badge shapes via add_shape) ────────
def rounded_rect_path(x0, y0, x1, y1, r):
    """Return an SVG path string for a rounded rectangle. Coordinates are in the
    same ref as the shape (paper or axis). r in the same units."""
    r = min(r, abs(x1 - x0) / 2, abs(y1 - y0) / 2)
    return (f"M {x0+r},{y0} L {x1-r},{y0} Q {x1},{y0} {x1},{y0+r} "
            f"L {x1},{y1-r} Q {x1},{y1} {x1-r},{y1} "
            f"L {x0+r},{y1} Q {x0},{y1} {x0},{y1-r} "
            f"L {x0},{y0+r} Q {x0},{y0} {x0+r},{y0} Z")


# ── Paper-space arrow (annotation axref/ayref can't be 'paper'; use pixels) ───
def paper_arrow(fig, x_head, y_head, dx_px, dy_px, color=INK, width=1.6,
                arrowhead=2, arrowsize=1.2):
    fig.add_annotation(
        xref="paper", yref="paper", x=x_head, y=y_head,
        ax=dx_px, ay=dy_px, axref="pixel", ayref="pixel",
        text="", showarrow=True, arrowhead=arrowhead, arrowsize=arrowsize,
        arrowwidth=width, arrowcolor=color)
    return fig


# ── Pie/donut slice centroids in paper coords (matches go.Pie convention) ─────
def pie_centroids(values, domain_x, domain_y, fig_w, fig_h,
                  rotation=0, rfrac=0.6):
    """Return [(x_paper, y_paper, mid_angle_deg), ...] for each slice centre,
    assuming go.Pie(direction='clockwise', sort=False, rotation=rotation).
    rfrac is the label radius as a fraction of the pie radius."""
    total = float(sum(values))
    cx = (domain_x[0] + domain_x[1]) / 2
    cy = (domain_y[0] + domain_y[1]) / 2
    r_px = min((domain_x[1]-domain_x[0]) * fig_w,
               (domain_y[1]-domain_y[0]) * fig_h) / 2
    rx = rfrac * r_px / fig_w
    ry = rfrac * r_px / fig_h
    cents, cum = [], 0.0
    for v in values:
        frac = v / total
        ang = 90 - rotation - 360 * (cum + frac / 2)     # math degrees
        rad = math.radians(ang)
        cents.append((cx + rx * math.cos(rad), cy + ry * math.sin(rad), ang))
        cum += frac
    return cents


# ── Semicircle (half-disk) path in paper coords, dome up ──────────────────────
def semicircle_path(cx, base_y, r_x, r_y, n=48):
    pts = []
    for i in range(n + 1):
        t = math.pi * i / n                      # 0..pi
        pts.append((cx - r_x * math.cos(t), base_y + r_y * math.sin(t)))
    d = "M " + " L ".join(f"{x:.4f},{y:.4f}" for x, y in pts) + " Z"
    return d


# ── Interactive render (HTML) ─────────────────────────────────────────────────
def render(fig, name, outdir=None, open_browser=False, include_plotlyjs="cdn"):
    """Write an interactive HTML file (no Chrome/Kaleido). Returns the path."""
    outdir = outdir or OUTDIR
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"{name}.html")
    config = dict(displayModeBar=False, responsive=True)
    pio.write_html(fig, path, include_plotlyjs=include_plotlyjs,
                   full_html=True, config=config)
    if open_browser:
        try:
            fig.show(config=config)
        except Exception:
            pass
    return path
