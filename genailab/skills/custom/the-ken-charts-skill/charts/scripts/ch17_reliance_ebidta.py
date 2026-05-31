"""
ch17 — "RELIANCE'S EBIDTA GAME" (The Ken, heavy style)
Two donuts (FY2015 / FY2019) of segment EBITDA share with a red dotted lasso
flagging the consumer businesses.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

W, H = 1180, 1040
INDIGO="#5C4D9D"; VIOLET="#6E3F9E"; CYAN="#29ABE2"; ORANGE="#F26B21"
RED="#E2231A"; GREY="#8C8C8C"

def donut(fig, labels, vals, colors, dx, dy, center, rot=0):
    fig.add_trace(go.Pie(labels=labels, values=vals, sort=False, direction="clockwise",
                  rotation=rot, hole=0.5,
                  marker=dict(colors=colors, line=dict(color="white", width=2)),
                  textinfo="none", domain=dict(x=list(dx), y=list(dy)), showlegend=False,
                  hovertemplate="%{label}: %{value}%<extra></extra>"))
    cents = ks.pie_centroids(vals, dx, dy, W, H, rotation=rot, rfrac=0.74)
    for (cx, cy, ang), name, val, col in zip(cents, labels, vals, colors):
        tcol = "white" if col in (INDIGO,VIOLET,CYAN,RED) else ks.INK
        fig.add_annotation(xref="paper", yref="paper", x=cx, y=cy+0.022, showarrow=False,
                           text=f"<b>{val:g}</b>", font=dict(family=ks.BODY,size=22,color=tcol))
        fig.add_annotation(xref="paper", yref="paper", x=cx, y=cy-0.028, showarrow=False,
                           text=name, font=dict(family=ks.BODY,size=14,color=tcol))
    ccx, ccy = (dx[0]+dx[1])/2, (dy[0]+dy[1])/2
    fig.add_annotation(xref="paper", yref="paper", x=ccx, y=ccy, showarrow=False,
                       text=center, font=dict(family=ks.BODY,size=22,color=ks.INK))

fig = ks.canvas(width=W, height=H, bg=ks.WHITE)
fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False))

donut(fig, ["R&M*","Petchem","E&P**","Organized<br>retail","Others"],
      [46,26.8,18.2,1.8,7.1], [INDIGO,VIOLET,CYAN,ORANGE,GREY],
      (0.04,0.46),(0.18,0.66),"FY 2015")
donut(fig, ["R&M*","Petchem#","E&P**","Organised<br>retail","Digital<br>services","Others"],
      [26.3,42.9,1.9,7.1,17.5,4.3], [INDIGO,VIOLET,CYAN,ORANGE,RED,GREY],
      (0.54,0.96),(0.18,0.66),"FY 2019")

# divider
fig.add_shape(type="line", xref="paper", yref="paper", x0=0.5, x1=0.5, y0=0.16, y1=0.66,
              line=dict(color="#DDDDDD", width=2))

ks.header(fig, "Reliance's EBIDTA game",
          "Consumer businesses now contribute 24.6% of consolidated segment EBITDA<br>(vs. 1.8% in FY15)",
          style="heavy", title_size=48, subtitle_size=20, y_title=0.985, y_sub=0.90)
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=0.78, showarrow=False,
                   text="Retail's contribution to Reliance's consolidated revenue",
                   font=dict(family=ks.BODY, size=20, color="#555"))
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=0.745, showarrow=False,
                   text="<span style='color:%s'>▢</span>  consumer businesses" % RED,
                   font=dict(family=ks.BODY, size=16, color=ks.INK))
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=0.075, showarrow=False,
                   text="*Refining & Marketing; **Exploration & Production; #Petrochemicals",
                   font=dict(family=ks.BODY, size=14, color=ks.INK))
ks.footer(fig, "Graphic by Prajakta Patil", "Source: Company", y=0.0,
          wordmark="THE-KEN", brand_color=ks.GREY)

if __name__ == "__main__":
    print(ks.render(fig, "ch17_reliance_ebidta"))
