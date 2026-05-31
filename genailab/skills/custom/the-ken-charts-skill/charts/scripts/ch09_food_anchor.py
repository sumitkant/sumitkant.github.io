"""
ch09 — "The food anchor" (The Ken)
Two full-width horizontal stacked bars (revenue by type, revenue by sector) in
grey bands, plus a total-revenue strip.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

BLUE = "#0A6CD6"; CYAN = "#34C0EC"; NAVY = "#0A2370"

def stacked_strip(fig, y0, y1, segs, total):
    """segs: list of (value, color, label1, label2). Lay across x 0..total."""
    x = 0
    for val, color, l1, l2 in segs:
        fig.add_shape(type="rect", xref="x", yref="y", x0=x, x1=x+val, y0=y0, y1=y1,
                      fillcolor=color, line=dict(color="white", width=2))
        cx = x + val/2
        fig.add_annotation(x=cx, y=(y0+y1)/2+0.16*(y1-y0), text=f"<b>{l1}</b>", showarrow=False,
                           xref="x", yref="y", font=dict(family=ks.BODY, size=22, color="white"))
        fig.add_annotation(x=cx, y=(y0+y1)/2-0.22*(y1-y0), text=l2, showarrow=False,
                           xref="x", yref="y", font=dict(family=ks.BODY, size=15, color="white"))
        x += val

TOTAL = 16.75
fig = ks.canvas(width=1000, height=720, bg=ks.WHITE, plot_x=(0.05, 0.95), plot_y=(0.10, 0.74))
fig.update_layout(
    xaxis=dict(domain=[0.05,0.95], range=[0, TOTAL], visible=False, fixedrange=True),
    yaxis=dict(domain=[0.10,0.74], range=[0, 10], visible=False, fixedrange=True),
)

# grey bands
for y0, y1 in [(7.0, 9.4), (1.0, 3.4)]:
    fig.add_shape(type="rect", xref="paper", yref="y", x0=0.0, x1=1.0, y0=y0, y1=y1,
                  fillcolor="#EFEFEF", line=dict(width=0), layer="below")

# total revenue strip (top)
fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.0, x1=1.0, y0=0.80, y1=0.875,
              fillcolor="#EFEFEF", line=dict(width=0), layer="below")
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=0.8375, showarrow=False,
                   text="Total revenue: <b>RMB 16.75 bn</b>",
                   font=dict(family=ks.BODY, size=24, color=ks.INK))

# Revenue breakdown by type
fig.add_annotation(xref="paper", yref="y", x=0.5, y=9.7, showarrow=False,
                   text="Revenue breakdown by type (RMB 'bn)",
                   font=dict(family=ks.BODY, size=19, color="#444"))
stacked_strip(fig, 7.1, 9.3, [
    (10.80, BLUE, "10.80", "Commission"),
    (2.86,  CYAN, "2.86",  "Online<br>marketing"),
    (3.09,  NAVY, "3.09",  "Other services<br>and sales"),
], TOTAL)

# Revenue breakdown by sector
fig.add_annotation(xref="paper", yref="y", x=0.5, y=3.7, showarrow=False,
                   text="Revenue breakdown by sector (RMB 'bn)",
                   font=dict(family=ks.BODY, size=19, color="#444"))
stacked_strip(fig, 1.1, 3.3, [
    (9.49, BLUE, "9.49", "Food delivery"),
    (3.09, CYAN, "3.09", "In-store,<br>hotel & travel"),
    (4.17, NAVY, "4.17", "New initiatives*"),
], TOTAL)

ks.header(fig, "The food anchor", "Food delivery business remains Meituan's key revenue driver",
          style="serif", title_size=44, subtitle_size=19, y_title=0.985, y_sub=0.905)
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=0.05, showarrow=False,
                   text="*New initiatives include micro-loan business, bike-sharing, car-hailing, and B2B food<br>distribution services; (US$1=RMB7.1)",
                   font=dict(family=ks.BODY, size=13, color=ks.INK))
ks.footer(fig, "Graphic by Prajakta Patil", "Source: Meituan Dianping's 1Q2020 financial results",
          y=0.0, wordmark="THE-KEN", brand_color=ks.GREY)

if __name__ == "__main__":
    print(ks.render(fig, "ch09_food_anchor"))
