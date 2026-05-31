"""
ch16 — "Upstart face-off" (The Ken)
2x3 small multiples: a Shopee vs Tiktok Shop slope per country, with gain/loss
pills (red loss + down triangle, green gain + up triangle).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

CYAN = "#22C7E0"; MAG = "#EC1C8E"; RED = "#F0473A"; GREEN = "#46C13B"
W, H = 1080, 1080

# name, ymax, shopee(22,23), tiktok(22,23), loss, gain
panels = [
    ("Thailand",     60, (56,49), (4,21),  -7, 17),
    ("Vietnam",      80, (63,61), (4,24),  -2, 20),
    ("The Philippines",60,(60,54), (4,16),  -6, 12),
    ("Indonesia",    42, (36,40), (5,9),    4,  4),
    ("Malaysia",     80, (78,63), (2,18),  -15, 16),
    ("Singapore",    60, (53,52), (0.5,4),  -1, 4),
]
# grid domains
cols_x = [(0.05,0.30),(0.38,0.63),(0.71,0.96)]
rows_y = [(0.40,0.62),(0.08,0.30)]

fig = ks.canvas(width=W, height=H, bg=ks.WHITE)
fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False))

for idx,(name,ymax,shop,tik,loss,gain) in enumerate(panels):
    r, c = divmod(idx, 3)
    dx, dy = cols_x[c], rows_y[r]
    ax = "" if idx==0 else str(idx+1)
    xa, ya = "x"+ax, "y"+ax
    xal, yal = "xaxis"+ax, "yaxis"+ax
    # panel grey bg
    fig.add_shape(type="rect", xref="paper", yref="paper", x0=dx[0], x1=dx[1], y0=dy[0], y1=dy[1],
                  fillcolor="#F0F0F0", line=dict(width=0), layer="below")
    # axes
    step = max(10, (ymax//4)//5*5 or 10)
    fig.update_layout(**{
        xal: dict(domain=list(dx), anchor=ya, range=[-0.18,1.18], visible=True, showgrid=False,
                 zeroline=False, tickmode="array", tickvals=[0,1], ticktext=["2022","2023"],
                 ticks="", tickfont=dict(family=ks.BODY,size=14,color=ks.INK), fixedrange=True),
        yal: dict(domain=list(dy), anchor=xa, range=[0,ymax], visible=True, showgrid=True,
                 gridcolor="#DDDDDD", tickmode="array",
                 tickvals=list(range(0,ymax+1,step)),
                 ticks="", zeroline=False, fixedrange=True,
                 tickfont=dict(family=ks.BODY,size=12,color="#888")),
    })
    for ser,col in [(shop,CYAN),(tik,MAG)]:
        fig.add_trace(go.Scatter(x=[0,1], y=list(ser), mode="lines+markers", xaxis=xa, yaxis=ya,
                      line=dict(color=col,width=5),
                      marker=dict(symbol="square", size=13, color=col), cliponaxis=False,
                      hoverinfo="skip"))
    # panel title
    fig.add_annotation(xref="paper", yref="paper", x=(dx[0]+dx[1])/2, y=dy[1]+0.022,
                       text=name, showarrow=False, font=dict(family=ks.BODY,size=20,color="#444"))
    # gain/loss pills near 2023 ends
    def pill(val, color, yref_val, up):
        px = dx[1]-0.02
        # paper y for the data value
        py = dy[0] + yref_val/ymax*(dy[1]-dy[0])
        tri = "▲" if up else "▼"
        fig.add_annotation(xref="paper", yref="paper", x=px, y=py+ (0.018 if up else -0.018),
                           text=tri, showarrow=False, font=dict(size=12, color=color))
        fig.add_annotation(xref="paper", yref="paper", x=px, y=py, showarrow=False,
                           text=f"<b>{val}</b>", font=dict(family=ks.BODY,size=14,color="white"),
                           bgcolor=color, borderpad=3)
    pill(loss, RED,  shop[1], up=False)   # Shopee loss
    pill(gain, GREEN, (tik[1]+shop[1])/2 if False else tik[1]+ymax*0.12, up=True)  # Tiktok gain

ks.header(fig, "Upstart face-off",
          "Tiktok Shop has been eating into Shopee's market share<br>in most of Southeast Asia",
          style="serif", title_size=58, subtitle_size=21, y_title=0.99, y_sub=0.92)
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=0.745, showarrow=False,
                   text="Market share (%)", font=dict(family=ks.BODY,size=20,color="#555"))
ks.legend_chips(fig, [("Shopee",CYAN),("Tiktok Shop",MAG),("Gain/loss (% points)",RED)],
                y=0.715, xs=[0.20,0.40,0.62], size=16)
ks.footer(fig, "Graphic by Aishwarya N, 2 Sep '24", "Source: Momentum Works", y=0.01)

if __name__ == "__main__":
    print(ks.render(fig, "ch16_upstart_faceoff"))
