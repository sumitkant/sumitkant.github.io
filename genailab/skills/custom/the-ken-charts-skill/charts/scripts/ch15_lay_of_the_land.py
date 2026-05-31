"""
ch15 — "Lay of the land" (The Ken)
B2C OTA market-share pie with big serif "~" numbers and leader-line brand
call-outs for the small slices.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

W, H = 1080, 1080
# clockwise from 12 o'clock
labels = ["EaseMyTrip","cleartrip","yatra","Paytm","ixigo","Others","MakeMyTrip"]
vals   = [18, 11, 3, 3, 2, 9, 54]          # geometry (sums 100)
shown  = ["~18","~10-12","~3","~3","~2","~9","~52"]
colors = ["#8DD3DA","#2BB6B6","#1C6E64","#5BBF3B","#F5D60E","#BEBEBE","#CDEDEC"]
ROT = 0
pdx, pdy = (0.06, 0.78), (0.05, 0.66)

fig = ks.canvas(width=W, height=H, bg=ks.WHITE)
fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False))
fig.add_trace(go.Pie(labels=labels, values=vals, sort=False, direction="clockwise",
              rotation=ROT, hole=0.0,
              marker=dict(colors=colors, line=dict(color="white", width=2)),
              textinfo="none", domain=dict(x=list(pdx), y=list(pdy)), showlegend=False,
              hovertemplate="%{label}: %{value}%<extra></extra>"))
cents = ks.pie_centroids(vals, pdx, pdy, W, H, rotation=ROT, rfrac=0.62)

# inside labels for the big slices
inside = {"EaseMyTrip":("EaseMyTrip.com",40), "cleartrip":("",46),
          "Others":("Others",30), "MakeMyTrip":("MakeMyTrip",64)}
for (cx, cy, ang), name, sh in zip(cents, labels, shown):
    if name in {"EaseMyTrip","MakeMyTrip","Others","cleartrip"}:
        brand, ns = inside[name]
        if brand:
            fig.add_annotation(xref="paper", yref="paper", x=cx, y=cy+0.035, showarrow=False,
                               text=brand, font=dict(family=ks.BODY, size=20, color="#333"))
        fig.add_annotation(xref="paper", yref="paper", x=cx, y=cy-0.04, showarrow=False,
                           text=f"<b>{sh}</b>", font=dict(family=ks.SERIF, size=ns, color="#333"))

# outside leader call-outs for small slices on the right
out = {"yatra":("yatra","#E2231A"), "Paytm":("Paytm","#1B3A6B"), "ixigo":("ixigo","#7A1FA2")}
oy = {"yatra":0.42, "Paytm":0.32, "ixigo":0.23}
for (cx, cy, ang), name in zip(cents, labels):
    if name in out:
        brand, col = out[name]
        ty = oy[name]
        fig.add_annotation(xref="paper", yref="paper", x=0.86, y=ty, xanchor="left", showarrow=False,
                           text=f"<b>{brand}</b>", font=dict(family=ks.BODY, size=20, color=col))
        ks.paper_arrow(fig, x_head=cx, y_head=cy, dx_px=int((0.85-cx)*W), dy_px=int((ty-cy)*H),
                       color="#888", width=1)

ks.header(fig, "Lay of the land",
          "While MakeMyTrip has a comfortable lead, EMT has quickly risen to<br>the second spot over the last two years",
          style="serif", title_size=58, subtitle_size=21, y_title=0.99, y_sub=0.915)
fig.add_annotation(xref="paper", yref="paper", x=0.42, y=0.70, showarrow=False,
                   text="B2C market share in FY22 <span style='font-size:14px'>(in %)</span>",
                   font=dict(family=ks.BODY, size=22, color="#555"))
ks.footer(fig, "Graphic by Adhithi Priya R, 09 Jul '22", "Source: The Ken research", y=0.01)

if __name__ == "__main__":
    print(ks.render(fig, "ch15_lay_of_the_land"))
