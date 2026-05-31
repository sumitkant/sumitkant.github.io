"""
ch11 — "Turning the tables" (The Ken)
Per-FY grey panels: a pink half-disk (area ∝ operating profit) up top, two bars
(NNPA% teal, NIM% purple) below. Geometry done in paper space.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

TEAL = "#1FB89C"; PURPLE = "#7E72CE"; PINK = "#E879BE"
W, H = 1180, 1080

fy   = ["FY18","FY19","FY20","FY21","FY22","FY23","FY24"]
nnpa = [3.4, 2.1, 1.6, 1.1, 0.7, 0.4, 0.3]
nim  = [3.4, 3.4, 3.5, 3.5, 3.5, 4.0, 4.1]
prof = [16838, 15594, 21749, 23128, 24742, 32048, 37123]
n = len(fy)

fig = ks.canvas(width=W, height=H, bg=ks.CREAM, plot_y=(0.10, 0.70))
fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False))

left, right = 0.045, 0.985
pitch = (right - left) / n
base_bar = 0.135                 # baseline (paper y)
bar_scale = 0.34 / max(nim)      # tallest NIM -> 0.34 paper height
sc_base = 0.52                   # semicircle flat base y
RMAX = pitch * 0.40
pmax = max(prof)

for i in range(n):
    cx = left + (i + 0.5) * pitch
    hw = pitch * 0.46
    # grey rounded panel
    fig.add_shape(type="path", xref="paper", yref="paper",
                  path=ks.rounded_rect_path(cx-hw, 0.075, cx+hw, 0.78, 0.012),
                  fillcolor="#ECEAE5", line=dict(width=0), layer="below")
    # semicircle (op profit)
    r_x = math.sqrt(prof[i]) / math.sqrt(pmax) * RMAX
    r_y = r_x * (W / H)
    fig.add_shape(type="path", xref="paper", yref="paper",
                  path=ks.semicircle_path(cx, sc_base, r_x, r_y),
                  fillcolor=PINK, line=dict(width=0))
    fig.add_annotation(xref="paper", yref="paper", x=cx, y=sc_base-0.03, yanchor="top",
                       text=f"<b>{prof[i]:,}</b>", showarrow=False,
                       font=dict(family=ks.BODY, size=19, color=ks.INK))
    # two bars
    bw = pitch * 0.17
    for val, col, dx in [(nnpa[i], TEAL, -0.20), (nim[i], PURPLE, 0.20)]:
        bx = cx + dx * pitch
        top = base_bar + val * bar_scale
        fig.add_shape(type="rect", xref="paper", yref="paper",
                      x0=bx-bw/2, x1=bx+bw/2, y0=base_bar, y1=top,
                      fillcolor=col, line=dict(width=0))
        fig.add_annotation(xref="paper", yref="paper", x=bx, y=top+0.012, yanchor="bottom",
                           text=f"<b>{val:g}</b>", showarrow=False,
                           font=dict(family=ks.BODY, size=18, color=ks.INK))
    # FY label
    fig.add_annotation(xref="paper", yref="paper", x=cx, y=0.10, yanchor="top",
                       text=fy[i], showarrow=False,
                       font=dict(family=ks.BODY, size=19, color=ks.INK))

# baseline
fig.add_shape(type="line", xref="paper", yref="paper", x0=left-0.005, x1=right+0.005,
              y0=base_bar, y1=base_bar, line=dict(color=ks.INK, width=2.5))

ks.header(fig, "Turning the tables",
          "Axis Bank has been improving its vitals since Amitabh<br>Chaudhry took over as CEO in 2019",
          style="serif", title_size=64, subtitle_size=26, y_title=0.985, y_sub=0.905)
items = [("Net non-performing assets (%)", TEAL), ("Net interest margin (%)", PURPLE),
         ("Operating profit (Rs cr)", PINK)]
ks.legend_chips(fig, items, y=0.815, xs=[0.07, 0.42, 0.72], size=20, glyph="●")
fig.add_annotation(xref="paper", yref="paper", x=0.42, y=0.788, showarrow=False,
                   text="(Rs 1 cr = US$120,000)", font=dict(family=ks.BODY, size=15, color="#888"))
ks.footer(fig, "Graphic by Kashvi B, 22 Sep '24", "Source: Axis Bank's annual reports", y=0.01)

if __name__ == "__main__":
    print(ks.render(fig, "ch11_turning_the_tables"))
