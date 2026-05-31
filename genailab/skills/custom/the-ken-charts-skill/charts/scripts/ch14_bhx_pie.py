"""
ch14 — "BHX's piece of the pie" (The Ken)
A single pie of MWG revenue share with big serif numbers and a leader-line
call-out for the tiny Bluetronics slice.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

W, H = 1100, 1000
# clockwise from 12 o'clock
labels = ["Thế Giới Di Động", "Bluetronics", "Điện máy Xanh", "BHX"]
vals   = [25.7, 0.4, 51.0, 22.5]
colors = ["#F4ED7A", "#6B4A2A", "#F7B928", "#4FD0DD"]
ROT = 0
pdx, pdy = (0.10, 0.90), (0.05, 0.66)

fig = ks.canvas(width=W, height=H, bg=ks.WHITE)
fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False))
fig.add_trace(go.Pie(labels=labels, values=vals, sort=False, direction="clockwise",
              rotation=ROT, hole=0.0, pull=[0,0,0,0.03],
              marker=dict(colors=colors, line=dict(color="white", width=2)),
              textinfo="none", domain=dict(x=list(pdx), y=list(pdy)), showlegend=False,
              hovertemplate="%{label}: %{value}%<extra></extra>"))

cents = ks.pie_centroids(vals, pdx, pdy, W, H, rotation=ROT, rfrac=0.6)
# big slices: name + big serif number
big = {"Thế Giới Di Động": 60, "Điện máy Xanh": 96, "BHX": 56}
for (cx, cy, ang), name, val in zip(cents, labels, vals):
    if name in big:
        fig.add_annotation(xref="paper", yref="paper", x=cx, y=cy+0.03, showarrow=False,
                           text=name, font=dict(family=ks.BODY, size=22, color=ks.INK))
        fig.add_annotation(xref="paper", yref="paper", x=cx, y=cy-0.045, showarrow=False,
                           text=f"<b>{val:g}</b>",
                           font=dict(family=ks.SERIF, size=big[name], color=ks.INK))
# Bluetronics leader call-out (outside, right)
bx, by, _ = cents[1]
fig.add_annotation(xref="paper", yref="paper", x=0.93, y=by, xanchor="left", showarrow=False,
                   text="Bluetronics<br><b style='font-size:22px'>0.4</b>",
                   font=dict(family=ks.BODY, size=18, color=ks.INK))
ks.paper_arrow(fig, x_head=0.78, y_head=by, dx_px=90, dy_px=0, color=ks.INK, width=1.2)

ks.header(fig, "BHX's piece of the pie",
          "In 2021, BHX contributed nearly a quarter of MWG's record US$5.2 billion revenue",
          style="serif", title_size=58, subtitle_size=21, y_title=0.99, y_sub=0.915)
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=0.70, showarrow=False,
                   text="MGW's revenue share", font=dict(family=ks.BODY, size=22, color="#555"))
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=0.675, showarrow=False,
                   text="(in %)", font=dict(family=ks.BODY, size=15, color="#888"))
ks.footer(fig, "Graphic by Adhithi Priya R, 30 May '22", "Source: Mobile World Group", y=0.01)

if __name__ == "__main__":
    print(ks.render(fig, "ch14_bhx_pie"))
