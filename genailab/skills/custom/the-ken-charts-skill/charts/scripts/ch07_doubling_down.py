"""
ch07 — "Doubling down" (The Ken)
A table with a highlighted column and an embedded horizontal-bar column,
drawn entirely with shapes + annotations on a numeric canvas.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

CYAN = "#22A9D6"; CYAN_LT = "#CFEAF6"

rows = [  # year, money invested, n investments, avg ticket
    (2013, 25, 1, 25), (2014, 331, 4, 83), (2015, 60, 1, 60),
    (2016, 413, 3, 138), (2017, 55, 1, 55), (2018, 125, 2, 63),
    (2019, 220, 1, 220), (2020, 43, 1, 43), (2021, 2300, 14, 164),
    (2022, 310, 3, 103),
]
n = len(rows)

# coordinate plane: x 0..100, y rows top->bottom
fig = ks.canvas(width=820, height=640, bg=ks.WHITE, plot_x=(0.02, 0.99), plot_y=(0.07, 0.80))
fig.update_layout(
    xaxis=dict(domain=[0.02,0.99], range=[0,100], visible=False, fixedrange=True),
    yaxis=dict(domain=[0.07,0.80], range=[0, n+1.4], visible=False, fixedrange=True),
)

# column x-centres
X_YEAR, X_MONEY, X_NINV = 6, 22, 50
X_BAR0 = 64                      # avg-ticket bars start here
BARSCALE = 32.0 / 220            # max value 220 -> width 32 units

def yr(i):  # row i (0=first data row) -> y
    return n - i

# highlighted money column band
fig.add_shape(type="rect", xref="x", yref="y", x0=12, x1=34, y0=0.4, y1=n + 1.1,
              fillcolor=CYAN_LT, line=dict(width=0), layer="below")

# header row
hy = n + 0.7
for txt, xx, anchor in [("Year", X_YEAR, "center"),
                        ("Money invested<br>(US$ mn)", X_MONEY, "center"),
                        ("No. of investments", X_NINV, "center"),
                        ("Avg. ticket size (US$ mn)", X_BAR0+4, "left")]:
    fig.add_annotation(x=xx, y=hy, text=txt, showarrow=False, xref="x", yref="y",
                       xanchor=anchor, font=dict(family=ks.BODY, size=15, color="#444"))
# header underline
fig.add_shape(type="line", xref="x", yref="y", x0=0, x1=100, y0=n+0.25, y1=n+0.25,
              line=dict(color=ks.INK, width=1.5))

for i, (year, money, ninv, avg) in enumerate(rows):
    y = yr(i)
    # dotted row separators
    fig.add_shape(type="line", xref="x", yref="y", x0=0, x1=100, y0=y-0.5, y1=y-0.5,
                  line=dict(color="#CCCCCC", width=1, dash="dot"))
    fig.add_annotation(x=X_YEAR, y=y, text=str(year), showarrow=False, xref="x", yref="y",
                       font=dict(family=ks.BODY, size=14, color=ks.INK))
    fig.add_annotation(x=15, y=y, text=f"<b>{money:,}</b>", showarrow=False, xref="x", yref="y",
                       xanchor="left", font=dict(family=ks.BODY, size=15, color=ks.INK))
    fig.add_annotation(x=X_NINV, y=y, text=str(ninv), showarrow=False, xref="x", yref="y",
                       font=dict(family=ks.BODY, size=14, color=ks.INK))
    # avg ticket bar
    w = avg * BARSCALE
    fig.add_shape(type="rect", xref="x", yref="y", x0=X_BAR0, x1=X_BAR0+w,
                  y0=y-0.30, y1=y+0.30, fillcolor=CYAN, line=dict(width=0))
    inside = w > 8
    fig.add_annotation(x=(X_BAR0+w-1) if inside else (X_BAR0+w+1), y=y,
                       text=f"<b>{avg}</b>", showarrow=False, xref="x", yref="y",
                       xanchor="right" if inside else "left",
                       font=dict(family=ks.BODY, size=13,
                                 color="white" if inside else ks.INK))

ks.header(fig, "Doubling down", "Temasek's India investments jumped 54X in 2021",
          style="serif", title_size=44, subtitle_size=18, x=0.0, anchor="left",
          y_title=0.985, y_sub=0.885)
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=0.045, showarrow=False,
                   text="(Figures have been rounded off)",
                   font=dict(family=ks.BODY, size=13, color=ks.INK))
ks.footer(fig, "Graphic by Aishwarya V; 10 Aug, '22", "Source: Tracxn", y=0.0)

if __name__ == "__main__":
    print(ks.render(fig, "ch07_doubling_down"))
