"""
ch04 — "COMING OF AGE" (The Ken, heavy style)
Left: stacked vertical bars (Services / Products) by year + a dotted CAGR arrow.
Right: grey panel with three proportionally-sized market bubbles.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

PURPLE = "#9B59C6"; LBLUE = "#A9CCEE"; BUBBLE = "#F6CA5B"

years    = ["2010", "2018", "2020<br>estimate", "2023<br>estimate"]
xpos     = [0, 1, 2, 3]
services = [10, 18, 39, 65]
products = [3, 32, 35, 55]
totals   = [13, 50, 74, 120]

fig = ks.canvas(width=1000, height=660, bg=ks.WHITE, plot_x=(0.05, 0.55), plot_y=(0.12, 0.66))

# grey right panel
fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.60, x1=1.0,
              y0=0.06, y1=0.80, fillcolor="#EFEFEF", line=dict(width=0), layer="below")

# stacked bars (numeric x)
fig.add_trace(go.Bar(x=xpos, y=services, marker_color=PURPLE, width=0.55,
              text=[f"<b>{v}</b>" for v in services], textposition="inside",
              insidetextanchor="middle", textfont=dict(family=ks.BODY, size=18, color="white"),
              cliponaxis=False, name="Services", hovertemplate="Services: $%{y} bn<extra></extra>"))
fig.add_trace(go.Bar(x=xpos, y=products, marker_color=LBLUE, width=0.55,
              text=[f"<b>{v}</b>" for v in products], textposition="inside",
              insidetextanchor="middle", textfont=dict(family=ks.BODY, size=18, color=ks.INK),
              cliponaxis=False, name="Products", hovertemplate="Products: $%{y} bn<extra></extra>"))
# totals above bars
for x, t in zip(xpos, totals):
    fig.add_annotation(x=x, y=t + 4, text=f"<b>{t}</b>", showarrow=False,
                       font=dict(family=ks.BODY, size=24, color=ks.INK), xref="x", yref="y")

fig.update_layout(
    barmode="stack", bargap=0.45,
    xaxis=dict(domain=[0.05,0.55], range=[-0.6,3.6], visible=True, showticklabels=True,
               showline=True, linecolor=ks.INK, linewidth=2, ticks="", showgrid=False,
               zeroline=False, tickmode="array", tickvals=xpos, ticktext=years,
               tickfont=dict(family=ks.BODY, size=15, color=ks.INK), fixedrange=True),
    yaxis=dict(domain=[0.12,0.66], visible=False, range=[0,135], fixedrange=True),
)

# dotted CAGR arc + arrowhead + label
fig.add_shape(type="path", xref="paper", yref="paper",
              path="M 0.085,0.34 C 0.18,0.86 0.40,0.86 0.50,0.72",
              line=dict(color=ks.KEN["red"], width=2, dash="dot"))
ks.paper_arrow(fig, x_head=0.505, y_head=0.715, dx_px=-14, dy_px=-12,
               color=ks.KEN["red"], width=2)
fig.add_annotation(xref="paper", yref="paper", x=0.40, y=0.80, showarrow=False,
                   text="<b>+21%</b>", font=dict(family=ks.BODY, size=20, color=ks.INK))

# left legend block (title + chips)
fig.add_annotation(xref="paper", yref="paper", x=0.045, y=0.79, xanchor="left",
                   showarrow=False, text="Mom and child care space",
                   font=dict(family=ks.BODY, size=17, color="#555"))
ks.legend_chips(fig, [("Services", PURPLE)], y=0.745, xs=[0.045], size=15)
ks.legend_chips(fig, [("Products", LBLUE)], y=0.715, xs=[0.045], size=15)
fig.add_annotation(xref="paper", yref="paper", x=0.045, y=0.685, xanchor="left",
                   showarrow=False, text="($ bn)", font=dict(family=ks.BODY, size=14, color="#555"))

# ── bubbles on dedicated axis ────────────────────────────────────────────────
fig.add_trace(go.Scatter(
    x=[0.46, 0.18, 0.80], y=[0.60, 0.22, 0.22], mode="markers",
    marker=dict(size=[170, 78, 26], color=BUBBLE, line=dict(width=0)),
    xaxis="x2", yaxis="y2", cliponaxis=False, hoverinfo="skip"))
fig.update_layout(
    xaxis2=dict(domain=[0.60,1.0], range=[0,1], visible=False, fixedrange=True),
    yaxis2=dict(domain=[0.06,0.80], range=[0,1], visible=False, fixedrange=True),
)
labels = [
    (0.46, 0.66, "<b>$74 bn</b>", 22), (0.46, 0.58, "Maternity &<br>childcare<br>market", 14),
    (0.18, 0.27, "<b>$19 bn</b>", 16), (0.18, 0.10, "Health and wellness<br>nutrition market", 12),
    (0.80, 0.27, "<b>$1.2 bn</b>", 14), (0.80, 0.12, "Digital ad<br>spends", 12),
]
for x, y, txt, sz in labels:
    fig.add_annotation(x=x, y=y, xref="x2", yref="y2", showarrow=False, text=txt,
                       font=dict(family=ks.BODY, size=sz, color=ks.INK))

ks.header(fig, "Coming of age",
          "With over 25 million children born annually in India, the<br>mother and babycare market is thriving",
          style="heavy", title_size=40, subtitle_size=17, y_title=0.99, y_sub=0.90)
ks.footer(fig, None, "Source: Publicly available reports", y=0.01,
          wordmark="THE-KEN", brand_color=ks.GREY)

if __name__ == "__main__":
    print(ks.render(fig, "ch04_coming_of_age"))
