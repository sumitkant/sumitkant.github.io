"""
ch12 — "Bumper year" (The Ken)
Left: lime bars (funding) with cyan bubbles (no. of rounds) + axis break before
the last period. Right: a pie of funding by geography.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

LIME = "#C6D63C"; CYAN = "#36C5E0"
W, H = 1180, 940

periods = ["CY17","CY18","CY19","CY20","CY21","Jan'22<br>- Jun'22"]
fund    = [12.8, 11.3, 16.6, 12.6, 40.6, 15.7]
rounds  = [1.9, 1.9, 2.2, 2.1, 2.6, 0.91]
xpos    = [0, 1, 2, 3, 4, 5.4]

fig = ks.canvas(width=W, height=H, bg=ks.WHITE, plot_x=(0.05, 0.52), plot_y=(0.12, 0.60))
fig.update_layout(
    xaxis=dict(domain=[0.05,0.52], range=[-0.6,6.0], visible=False, fixedrange=True),
    yaxis=dict(domain=[0.12,0.60], range=[0,52], visible=False, fixedrange=True),
)
fig.add_trace(go.Bar(x=xpos, y=fund, width=0.62, marker_color=LIME, cliponaxis=False,
              hoverinfo="skip"))
for x, f in zip(xpos, fund):
    fig.add_annotation(x=x, y=f+1.5, text=f"<b>{f}</b>", showarrow=False, xref="x", yref="y",
                       font=dict(family=ks.BODY, size=20, color=ks.INK))
fig.add_trace(go.Scatter(x=xpos, y=[f+7 for f in fund], mode="markers",
              marker=dict(size=[r*26 for r in rounds], color=CYAN, line=dict(width=0)),
              cliponaxis=False, hoverinfo="skip"))
for x, f, r in zip(xpos, fund, rounds):
    fig.add_annotation(x=x, y=f+7, text=f"<b>{r}</b>", showarrow=False, xref="x", yref="y",
                       font=dict(family=ks.BODY, size=18, color=ks.INK))
fig.add_shape(type="line", xref="x", yref="y", x0=-0.6, x1=6.0, y0=0, y1=0,
              line=dict(color=ks.INK, width=1.5))
def _px(xp):
    return 0.05 + (xp + 0.6) / 6.6 * (0.52 - 0.05)
for x, p in zip(xpos, periods):
    fig.add_annotation(xref="paper", yref="paper", x=_px(x), y=0.10, yanchor="top", text=p,
                       showarrow=False, font=dict(family=ks.BODY, size=16, color=ks.INK))
fig.add_annotation(xref="paper", yref="paper", x=_px(4.95), y=0.115, yanchor="top", text="//",
                   showarrow=False, font=dict(family=ks.BODY, size=20, color=ks.INK))
fig.add_annotation(xref="paper", yref="paper", x=0.06, y=0.66, xanchor="left", showarrow=False,
                   text="Year-on-year funding", font=dict(family=ks.BODY, size=22, color="#555"))
ks.legend_chips(fig, [("Funding (in $ bn)", LIME)], y=0.625, xs=[0.06], size=17)
ks.legend_chips(fig, [("No. of rounds (in '000s)", CYAN)], y=0.625, xs=[0.26], size=17, glyph="●")

# divider
fig.add_shape(type="line", xref="paper", yref="paper", x0=0.55, x1=0.55, y0=0.06, y1=0.68,
              line=dict(color="#CCCCCC", width=2))

# pie (funding by geography)
geo_labels = ["Bengaluru","Mumbai","Gurgaon","Noida","Delhi","Others"]
geo_vals   = [51, 12, 11, 7, 6, 12]
geo_colors = ["#0F4C81","#36A9E1","#A9D6F5","#F2E400","#111111","#BFBFBF"]
txt_cols   = ["white","white",ks.INK,ks.INK,"white",ks.INK]
num_sizes  = [54, 26, 26, 22, 20, 26]
pdx, pdy = (0.58, 0.99), (0.08, 0.60)
ROT = -1.8
fig.add_trace(go.Pie(labels=geo_labels, values=geo_vals, sort=False, direction="clockwise",
              rotation=ROT, hole=0.0,
              marker=dict(colors=geo_colors, line=dict(color="white", width=2)),
              textinfo="none", domain=dict(x=list(pdx), y=list(pdy)), showlegend=False,
              hovertemplate="%{label}: %{value}%<extra></extra>"))
cents = ks.pie_centroids(geo_vals, pdx, pdy, W, H, rotation=ROT, rfrac=0.58)
for (cx, cy, _), name, val, tc, ns in zip(cents, geo_labels, geo_vals, txt_cols, num_sizes):
    fig.add_annotation(xref="paper", yref="paper", x=cx, y=cy, showarrow=False,
        text=f"<span style='font-family:{ks.SERIF};font-size:{ns}px'><b>{val}</b></span>"
             f"<br><span style='font-size:16px'>{name}</span>",
        font=dict(family=ks.BODY, color=tc), align="center")
fig.add_annotation(xref="paper", yref="paper", x=0.78, y=0.66, showarrow=False,
                   text="Funding by geography", font=dict(family=ks.BODY, size=22, color="#555"))
fig.add_annotation(xref="paper", yref="paper", x=0.78, y=0.635, showarrow=False,
                   text="(in %, Jun 2021 - Jun 2022)", font=dict(family=ks.BODY, size=15, color="#888"))

ks.header(fig, "Bumper year", "2021 has been a standout year for venture-capital funding",
          style="serif", title_size=58, subtitle_size=24, y_title=0.99, y_sub=0.905)
ks.footer(fig, "Graphic by Aishwarya V, 13 Oct '22", "Source: Tracxn", y=0.0,
          wordmark="THE-KEN", brand_color=ks.GREY)

if __name__ == "__main__":
    print(ks.render(fig, "ch12_bumper_year"))
