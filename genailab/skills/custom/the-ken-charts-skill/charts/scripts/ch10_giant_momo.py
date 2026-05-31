"""
ch10 — "Giant MoMo" (The Ken)
A single full-width stacked bar (marimekko-ish) of e-wallet market share, with
big in-segment labels and call-out tags for the thin slices.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

# darkest -> lightest red ramp
segs = [
    ("MoMo", 53, "#7A0E22", "white", 64),
    ("ViettelPay", 25.2, "#B23A4E", "white", 52),
    ("AirPay", 10.6, "#8C2230", "white", 40),
    ("ZaloPay", 5.3, "#F2A0AE", ks.INK, 30),
    ("Others", 4, "#F2778C", ks.INK, 26),
    ("GrabPay", 2, "#111111", "white", 24),
]
TOTAL = sum(s[1] for s in segs)

fig = ks.canvas(width=820, height=620, bg=ks.WHITE, plot_x=(0.05, 0.97), plot_y=(0.22, 0.68))
fig.update_layout(
    xaxis=dict(domain=[0.05,0.97], range=[0, TOTAL], visible=False, fixedrange=True),
    yaxis=dict(domain=[0.22,0.68], range=[0, 1], visible=False, fixedrange=True),
)

x = 0
big = {"MoMo", "ViettelPay", "AirPay"}
centers = {}
for name, val, color, tcol, fs in segs:
    fig.add_shape(type="rect", xref="x", yref="y", x0=x, x1=x+val, y0=0, y1=1,
                  fillcolor=color, line=dict(color="white", width=1.5))
    cx = x + val/2; centers[name] = cx
    if name in big:
        fig.add_annotation(x=cx, y=0.62, text=name, showarrow=False, xref="x", yref="y",
                           font=dict(family=ks.BODY, size=20, color=tcol))
        fig.add_annotation(x=cx, y=0.38, text=f"<b>{val}</b>", showarrow=False, xref="x", yref="y",
                           font=dict(family=ks.SERIF, size=fs, color=tcol))
    else:
        fig.add_annotation(x=cx, y=0.5, text=f"<b>{val}</b>", showarrow=False, xref="x", yref="y",
                           font=dict(family=ks.SERIF, size=fs, color=tcol))
    x += val

# call-out tags for thin slices
def tag(name, label, bg, fg, ty, side="up"):
    cx = centers[name]
    px = 0.05 + cx / TOTAL * (0.97 - 0.05)
    fig.add_annotation(xref="paper", yref="paper", x=px, y=ty, showarrow=False,
                       text=f"<b>{label}</b>",
                       font=dict(family=ks.BODY, size=15, color=fg),
                       bgcolor=bg, borderpad=4)
    y_anchor = 0.68 if side == "up" else 0.22
    ks.paper_arrow(fig, x_head=px, y_head=y_anchor, dx_px=0,
                   dy_px=(-22 if side == "up" else 22), color="#444", width=1)

tag("ZaloPay", "ZaloPay", "#F06A86", "white", 0.76)
tag("GrabPay", "GrabPay", "#111111", "white", 0.83)
tag("Others",  "Others",  "#E0566F", "white", 0.14, side="down")

ks.header(fig, "Giant MoMo",
          "MoMo holds a dominant position, while ViettelPay, operated by Vietnam's<br>largest telco, has quickly become a key player",
          style="serif", title_size=40, subtitle_size=17, y_title=0.985, y_sub=0.905)
fig.add_annotation(xref="paper", yref="paper", x=0.42, y=0.745, showarrow=False,
                   text="Vietnam's e-wallet market share (in %)",
                   font=dict(family=ks.BODY, size=17, color="#555"))
ks.footer(fig, "Graphic by Aishwarya V; 28 Jan, '22", "Source: Boku 2021 Mobile Wallets Report",
          y=0.01)

if __name__ == "__main__":
    print(ks.render(fig, "ch10_giant_momo"))
