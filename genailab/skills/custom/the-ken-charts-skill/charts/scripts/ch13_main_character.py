"""
ch13 — "Becoming the main character" (The Ken)
Overlapping bars (total op revenue B behind, financial-services revenue A in
front) with an orange bubble per quarter sized by the ratio A/B.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

LTEAL = "#A9E0E0"; DTEAL = "#0E6E78"; ORANGE = "#F6B26B"
W, H = 1120, 1080

q   = ["Sep '21","Dec '21","Mar '22","Jun '22","Sep '22","Dec '22","Mar '23","Jun '23","Sep '23"]
B   = [1086,1456,1540,1680,1914,2062,2334,2342,2519]
A   = [89,125,168,271,349,446,475,522,571]
pct = [8.2,8.5,10.9,16.1,18.2,21.6,20.3,22.2,22.7]
gx  = list(range(len(q)))

fig = ks.canvas(width=W, height=H, bg=ks.WHITE, plot_x=(0.05, 0.99), plot_y=(0.10, 0.66))
fig.update_layout(
    xaxis=dict(domain=[0.05,0.99], range=[-0.6,8.6], visible=False, fixedrange=True),
    yaxis=dict(domain=[0.10,0.66], range=[0,3350], visible=False, fixedrange=True),
)
# B behind (wide), A in front (narrow)
fig.add_trace(go.Bar(x=gx, y=B, width=0.66, marker_color=LTEAL, cliponaxis=False, hoverinfo="skip"))
fig.add_trace(go.Bar(x=gx, y=A, width=0.34, marker_color=DTEAL, cliponaxis=False, hoverinfo="skip"))
fig.update_layout(barmode="overlay")
for x, b, a in zip(gx, B, A):
    fig.add_annotation(x=x, y=b+70, text=f"<b>{b:,}</b>", showarrow=False, xref="x", yref="y",
                       font=dict(family=ks.BODY, size=18, color=ks.INK))
    fig.add_annotation(x=x, y=a+70, text=f"<b>{a}</b>", showarrow=False, xref="x", yref="y",
                       font=dict(family=ks.BODY, size=16, color=ks.INK))
# ratio bubbles
bub_y = [b+430 for b in B]
fig.add_trace(go.Scatter(x=gx, y=bub_y, mode="markers",
              marker=dict(size=[p*6.6 for p in pct], color=ORANGE, line=dict(width=0)),
              cliponaxis=False, hoverinfo="skip"))
for x, y, p in zip(gx, bub_y, pct):
    fig.add_annotation(x=x, y=y, xref="x", yref="y", showarrow=False,
        text=f"<b>{p}</b><span style='font-size:13px'>%</span>",
        font=dict(family=ks.BODY, size=21, color=ks.INK))
# baseline + quarter labels
fig.add_shape(type="line", xref="x", yref="y", x0=-0.6, x1=8.6, y0=0, y1=0,
              line=dict(color=ks.INK, width=1.5))
for x, qq in zip(gx, q):
    fig.add_annotation(x=x, y=-150, text=qq, showarrow=False, xref="x", yref="y",
                       font=dict(family=ks.BODY, size=15, color=ks.INK))

# legend block (fraction = bubble)
fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.15, x1=0.85, y0=0.74, y1=0.815,
              fillcolor="#EEF2F2", line=dict(width=0), layer="below")
fig.add_annotation(xref="paper", yref="paper", x=0.22, y=0.793, xanchor="left", showarrow=False,
                   text="<span style='color:%s'>■</span> Revenue from financial services (A)" % DTEAL,
                   font=dict(family=ks.BODY, size=16, color=ks.INK))
fig.add_annotation(xref="paper", yref="paper", x=0.22, y=0.762, xanchor="left", showarrow=False,
                   text="<span style='color:%s'>■</span> Total operational revenue (B)" % LTEAL,
                   font=dict(family=ks.BODY, size=16, color=ks.INK))
fig.add_shape(type="line", xref="paper", yref="paper", x0=0.225, x1=0.55, y0=0.7775, y1=0.7775,
              line=dict(color=ks.INK, width=1.5))
fig.add_annotation(xref="paper", yref="paper", x=0.60, y=0.7775, xanchor="left", showarrow=False,
                   text="= <span style='color:%s'>●</span> %% (A/B)" % ORANGE,
                   font=dict(family=ks.BODY, size=16, color=ks.INK))
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=0.70, showarrow=False,
                   text="Figures in Rs cr", font=dict(family=ks.BODY, size=15, color="#666"))

ks.header(fig, "Becoming the main character",
          "Financial services like distributing loans is fuelling Paytm's pivot",
          style="serif", title_size=56, subtitle_size=23, y_title=0.99, y_sub=0.905)
ks.footer(fig, "Graphic by Adhithi Priya R, 13 Nov '23", "Source: Paytm's earnings release", y=0.0)

if __name__ == "__main__":
    print(ks.render(fig, "ch13_main_character"))
