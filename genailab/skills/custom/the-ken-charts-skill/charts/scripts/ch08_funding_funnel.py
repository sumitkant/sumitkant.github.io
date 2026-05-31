"""
ch08 — "The funding funnel" (The Ken)
Grouped bars (2023/2024/2025) with a magenta "total rounds" I-beam rising from
each bar top, plus under-axis brackets for Seed / Series A.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

ORANGE = "#F4A93C"; GREEN = "#5DC020"; PINK = "#F46FA8"; MAG = "#C0179E"

groups = ["AI-native", "AI-enabled", "AI-native", "AI-enabled"]
# bar values and round counts per group, by year (2023,2024,2025)
vals = {
    0: [(30,11),(40.4,20),(21.3,14)],
    1: [(58.2,74),(83.7,95),(80.6,64)],
    2: [(64.8,2),(81,3),(96.7,7)],
    3: [(164.9,18),(188.4,27),(255.5,19)],
}
year_colors = [ORANGE, GREEN, PINK]
gx = [0, 1, 2, 3]
W = 0.26
RSCALE = 2.9

fig = ks.canvas(width=1280, height=940, bg="#F2EFEA", plot_x=(0.06, 0.99), plot_y=(0.12, 0.66))
fig.update_layout(
    xaxis=dict(domain=[0.06,0.99], range=[-0.55,3.55], visible=False, fixedrange=True),
    yaxis=dict(domain=[0.12,0.66], range=[0,330], visible=True, showgrid=True,
               gridcolor="#DAD7D2", tickmode="array", tickvals=[0,75,150,225,300],
               ticks="", zeroline=False, fixedrange=True,
               tickfont=dict(family=ks.BODY, size=16, color=ks.INK)),
)

offs = [-0.27, 0, 0.27]
for g in gx:
    for (val, rounds), off, col in zip(vals[g], offs, year_colors):
        x = g + off
        fig.add_trace(go.Bar(x=[x], y=[val], width=W, marker_color=col,
                      cliponaxis=False, hoverinfo="skip"))
        # value label inside bottom
        fig.add_annotation(x=x, y=8, text=f"<b>{val}</b>", showarrow=False, xref="x", yref="y",
                           font=dict(family=ks.BODY, size=15, color=ks.INK))
        # total-rounds I-beam rising from bar top
        top = val + rounds * RSCALE
        fig.add_shape(type="line", xref="x", yref="y", x0=x, x1=x, y0=val, y1=top,
                      line=dict(color=MAG, width=2))
        fig.add_shape(type="line", xref="x", yref="y", x0=x-0.06, x1=x+0.06, y0=top, y1=top,
                      line=dict(color=MAG, width=2))
        fig.add_annotation(x=x, y=top+9, text=f"<b>{rounds}</b>", showarrow=False,
                           xref="x", yref="y", font=dict(family=ks.BODY, size=16, color=ks.INK))
    # (group label placed in paper space below — see loop after)
    pass

# group labels just under the baseline (paper space)
gpx = [0.06 + (g + 0.55) / 4.10 * (0.99 - 0.06) for g in gx]
for g, px in zip(gx, gpx):
    fig.add_annotation(xref="paper", yref="paper", x=px, y=0.105, yanchor="top",
                       text=groups[g], showarrow=False,
                       font=dict(family=ks.BODY, size=16, color=ks.INK))

# baseline
fig.add_shape(type="line", xref="x", yref="y", x0=-0.55, x1=3.55, y0=0, y1=0,
              line=dict(color=ks.INK, width=2.5))

# Seed / Series A brackets (paper space, below group labels)
def bracket(x0, x1, label):
    yb = 0.065
    fig.add_shape(type="line", xref="paper", yref="paper", x0=x0, x1=x1, y0=yb, y1=yb,
                  line=dict(color=ks.INK, width=1.5, dash="dot"))
    for xe in (x0, x1):
        fig.add_shape(type="line", xref="paper", yref="paper", x0=xe, x1=xe,
                      y0=yb, y1=yb+0.02, line=dict(color=ks.INK, width=1.5))
    fig.add_annotation(xref="paper", yref="paper", x=(x0+x1)/2, y=yb-0.005, yanchor="top",
                       text=f"<b>{label}</b>", showarrow=False,
                       font=dict(family=ks.BODY, size=18, color=ks.INK))
bracket(0.10, 0.52, "Seed")
bracket(0.55, 0.97, "in Series A")

ks.header(fig, "The funding funnel",
          "Fewer AI startups are getting funded, but those that do are raising larger<br>cheques—especially at Series A",
          style="serif", title_size=56, subtitle_size=24, y_title=0.99, y_sub=0.905)
fig.add_annotation(xref="paper", yref="paper", x=0.40, y=0.78, xanchor="center", showarrow=False,
                   text="AI startups funding (in million $)",
                   font=dict(family=ks.BODY, size=22, color="#555"))
items = [("2023", ORANGE), ("2024", GREEN), ("2025", PINK), ("Total rounds", MAG)]
ks.legend_chips(fig, items, y=0.735, xs=[0.10, 0.22, 0.34, 0.46], size=18)
# I-beam glyph for last legend item drawn over its chip
ks.footer(fig, "Graphic by Sakshi M, 11 Feb '26", "Source:  Tracxn", y=0.0)

if __name__ == "__main__":
    print(ks.render(fig, "ch08_funding_funnel"))
