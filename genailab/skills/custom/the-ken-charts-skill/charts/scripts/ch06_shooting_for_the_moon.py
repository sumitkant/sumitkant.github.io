"""
ch06 — "Shooting for the moon" (The Ken)
Grouped bars (PAT / Revenue / AUM) per fiscal year + a purple bubble per year
sized by gross NPA %.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

MAG = "#D6248E"; GREEN = "#16C098"; GOLD = ks.KEN["gold"]; PURPLE = "#7E72CE"

groups = ["FY21", "FY22", "FY23"]
pat = [-101, -35, 91]
rev = [327, 642, 1275]
aum = [816, 1951, 4644]
npa = [7.2, 2.9, 2.3]
npa_cy = [1700, 2450, 4950]          # bubble vertical centres
gx = [0, 1, 2]
W = 0.24

fig = ks.canvas(width=1180, height=1180, bg=ks.CREAM, plot_x=(0.04, 0.99), plot_y=(0.06, 0.70))
fig.update_layout(
    xaxis=dict(domain=[0.04,0.99], range=[-0.55,2.55], visible=False, fixedrange=True),
    yaxis=dict(domain=[0.06,0.70], range=[-350,5400], visible=False, fixedrange=True),
)

def bars(vals, off, color, fmt):
    fig.add_trace(go.Bar(x=[g+off for g in gx], y=vals, width=W, marker_color=color,
                  cliponaxis=False, hoverinfo="skip"))
    for g, v in zip(gx, vals):
        ylab = v + 130 if v >= 0 else v - 130
        fig.add_annotation(x=g+off, y=ylab, text=f"<b>{fmt(v)}</b>", showarrow=False,
                           xref="x", yref="y", font=dict(family=ks.BODY, size=20, color=ks.INK))

bars(pat, -0.26, MAG,   lambda v: f"{v:,}")
bars(rev,  0.00, GREEN, lambda v: f"{v:,}")
bars(aum,  0.26, GOLD,  lambda v: f"{v:,}")

# zero baseline
fig.add_shape(type="line", xref="x", yref="y", x0=-0.55, x1=2.55, y0=0, y1=0,
              line=dict(color=ks.INK, width=2))
# group labels under baseline
for g, name in zip(gx, groups):
    fig.add_annotation(x=g, y=-230, text=f"<b>{name}</b>", showarrow=False, xref="x", yref="y",
                       font=dict(family=ks.BODY, size=22, color=ks.INK))

# NPA bubbles
fig.add_trace(go.Scatter(x=gx, y=npa_cy, mode="markers+text",
              marker=dict(size=[v*21 for v in npa], color=PURPLE, line=dict(width=0)),
              text=[f"<b>{v}</b>" for v in npa], textposition="middle center",
              textfont=dict(family=ks.BODY, size=[40,26,22], color="white"),
              cliponaxis=False, hoverinfo="skip"))

ks.header(fig, "Shooting for the moon",
          "Kreditbee's disbursals in the year ended March 2023 grew by 140% to nearly<br>Rs 14,000 crore, turning the company profitable",
          style="serif", title_size=62, subtitle_size=24, y_title=0.985, y_sub=0.915)

items = [("Profit after tax (in Rs cr)", MAG), ("Revenue (in Rs cr)", GREEN)]
ks.legend_chips(fig, items, y=0.815, xs=[0.16, 0.55], size=20)
items2 = [("Assets under management (in Rs cr)", GOLD), ("Gross non-performing assets (in %)", PURPLE)]
ks.legend_chips(fig, items2, y=0.778, xs=[0.16, 0.55], size=20)

ks.footer(fig, "Graphic by Kashvi B, 14 May '24", "Source: Crisil Ratings", y=0.01)

if __name__ == "__main__":
    print(ks.render(fig, "ch06_shooting_for_the_moon"))
