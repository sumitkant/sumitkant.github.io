"""
ch05 — "Range of roadsters" (The Ken)
Bespoke comparison: a price pill (width ∝ price) plus three fixed stat pills
(range / 0-100 time / top speed) per EV. Pills are rounded bars (cornerradius).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

ORANGE = "#F5933B"; LAV = "#C9C6F0"; PINK = "#F3BCC6"; GREEN = "#BFE3B6"

cars = [  # name, bold?, price, range_km, time_s, top_kmh
    ("Xiaomi SU7",            True,  215900, "700 km", "5.28 sec", "210 km/h"),
    ("Tesla Model 3<br>RWD",  False, 245900, "606 km", "6.10 sec", "200 km/h"),
    ("Porsche<br>Taycan",     False, 898000, "430 km", "5.40 sec", "230 km/h"),
    ("Xpeng P7",              False, 239900, "586 km", "6.70 sec", "170 km/h"),
    ("Zeekr 007<br>Ehanced RWD", False, 209900, "688 km", "5.60 sec", "210 km/h"),
]

PMAX = 898000
SCALE = 78.0 / PMAX        # price pill max width = 78 units
XR = [0, 100]

fig = ks.canvas(width=1160, height=1100, bg=ks.CREAM, plot_x=(0.0,1.0), plot_y=(0.04,0.74))
fig.update_layout(
    xaxis=dict(domain=[0.20,0.99], range=XR, visible=False, fixedrange=True),
    yaxis=dict(domain=[0.04,0.74], range=[0,10], visible=False, fixedrange=True),
)

def pill(x0, x1, yc, h, color, text, fz=18, bold=True, tcol=ks.INK):
    fig.add_shape(type="path", xref="x", yref="y",
                  path=ks.rounded_rect_path(x0, yc-h/2, x1, yc+h/2, h/2),
                  fillcolor=color, line=dict(width=0), layer="below")
    fig.add_annotation(x=(x0+x1)/2, y=yc, xref="x", yref="y", showarrow=False,
                       text=f"<b>{text}</b>" if bold else text,
                       font=dict(family=ks.BODY, size=fz, color=tcol))

n = len(cars)
row_h = 10.0 / n
for i, (name, bold, price, rng, tm, spd) in enumerate(cars):
    yc = 10 - (i + 0.5) * row_h
    price_y = yc + row_h*0.22
    stat_y  = yc - row_h*0.22
    # car name (left)
    fig.add_annotation(xref="paper", yref="y", x=0.18, y=yc, xanchor="right",
                       showarrow=False, text=(f"<b>{name}</b>" if bold else name),
                       font=dict(family=ks.BODY, size=24 if bold else 22, color=ks.INK))
    # price pill (scaled)
    pw = price * SCALE
    pill(0, pw, price_y, row_h*0.30, ORANGE, f"{price:,} yuan", fz=18, tcol=ks.INK)
    # three stat pills (fixed columns)
    pill(0, 18, stat_y, row_h*0.26, LAV, rng, fz=16)
    pill(20, 38, stat_y, row_h*0.26, PINK, tm, fz=16)
    pill(45, 63, stat_y, row_h*0.26, GREEN, spd, fz=16)

ks.header(fig, "Range of roadsters",
          "The Xiaomi SU7 electric vehicle was introduced into a crowded market, but<br>was priced low to attract buyers",
          style="serif", title_size=62, subtitle_size=24, y_title=0.985, y_sub=0.915)

# custom legend (price + three stat swatches)
fig.add_annotation(xref="paper", yref="paper", x=0.30, y=0.80, xanchor="left", showarrow=False,
                   text=f"<span style='color:{ORANGE}'>●</span> <b>Price in China</b>",
                   font=dict(family=ks.BODY, size=18, color=ks.INK))
fig.add_annotation(xref="paper", yref="paper", x=0.315, y=0.775, xanchor="left", showarrow=False,
                   text="1 Yuan = US$ 0.14", font=dict(family=ks.BODY, size=14, color="#888"))
ks.legend_chips(fig, [("Range", LAV)], y=0.80, xs=[0.55], size=17)
ks.legend_chips(fig, [("Time for 0–100 km/h", PINK)], y=0.775, xs=[0.55], size=17)
ks.legend_chips(fig, [("Top Speed", GREEN)], y=0.75, xs=[0.55], size=17)

ks.footer(fig, "Graphic by Kashvi B, 29 Apr '24", "Source: The Ken research", y=0.01)

if __name__ == "__main__":
    print(ks.render(fig, "ch05_range_of_roadsters"))
