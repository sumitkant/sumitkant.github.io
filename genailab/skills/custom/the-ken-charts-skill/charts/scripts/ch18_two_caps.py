"""
ch18 — "Two caps, one table" (The Ken)
Two full-width stacked bars (cap tables) with labels alternating above/below via
dotted leader lines.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

W, H = 1180, 1060

# name, value, color, side ("up"/"down")
cult = [
    ("Mukesh Bansal",11,"#73E9CB","up"),("Accel",17,"#45CFD6","down"),
    ("Chiratae",11,"#3FB3E0","up"),("Kalaari Capital",10,"#5A8FD4","down"),
    ("Tata Digital",6,"#6E72D0","down"),("Zomato",5,"#7A3FC4","up"),
    ("Esops",8,"#7D1FC9","up"),("Others",32,"#BF22B0","up"),
]
cure = [
    ("Ankit Nagori",28,"#F6B40E","up"),("3 State Ventures",17,"#F59E0E","up"),
    ("Accel",7,"#F47A1E","down"),("Iron Pillar",14,"#E8431A","up"),
    ("Crimson Winter",4,"#E2120E","down"),("Sixteenth Street Asian<br>Gems Fund",4,"#B01818","up"),
    ("Chiratae Ventures",8,"#7A1020","down"),("Others",18,"#2E0A12","up"),
]

fig = ks.canvas(width=W, height=H, bg=ks.WHITE)
fig.update_layout(
    xaxis=dict(domain=[0.04,0.97], range=[0,100], visible=False, fixedrange=True),
    yaxis=dict(domain=[0.05,0.92], range=[0,10], visible=False, fixedrange=True),
)

def strip(segs, y0, y1, title, ty):
    fig.add_annotation(xref="paper", yref="paper", x=0.5, y=ty, showarrow=False,
                       text=title, font=dict(family=ks.BODY, size=21, color="#555"))
    x = 0
    for name, val, col, side in segs:
        fig.add_shape(type="rect", xref="x", yref="y", x0=x, x1=x+val, y0=y0, y1=y1,
                      fillcolor=col, line=dict(color="white", width=1.5))
        cx = x + val/2
        # darker fills -> white number
        tcol = "white" if col[1] in "0123456" and col not in ("#73E9CB","#F6B40E","#F59E0E") else ks.INK
        fig.add_annotation(x=cx, y=(y0+y1)/2, xref="x", yref="y", showarrow=False,
                           text=f"<b>{val}</b>", font=dict(family=ks.BODY, size=18, color=tcol))
        # leader + label
        px = 0.04 + cx/100*(0.97-0.04)
        if side == "up":
            lab_y = (0.92 if y1 > 7 else 0.50)  # placeholder; set per strip below
        x += val

# We place strips and labels manually for control
def labels_for(segs, y0p, y1p, up_y, dn_y):
    x = 0
    for name, val, col, side in segs:
        cx = x + val/2
        px = 0.04 + cx/100*(0.97-0.04)
        if side == "up":
            fig.add_annotation(xref="paper", yref="paper", x=px, y=up_y, yanchor="bottom",
                               text=name, showarrow=False, align="center",
                               font=dict(family=ks.BODY, size=15, color=ks.INK))
            fig.add_shape(type="line", xref="paper", yref="paper", x0=px, x1=px,
                          y0=up_y-0.005, y1=y1p, line=dict(color="#999", width=1, dash="dot"))
        else:
            fig.add_annotation(xref="paper", yref="paper", x=px, y=dn_y, yanchor="top",
                               text=name, showarrow=False, align="center",
                               font=dict(family=ks.BODY, size=15, color=ks.INK))
            fig.add_shape(type="line", xref="paper", yref="paper", x0=px, x1=px,
                          y0=dn_y+0.005, y1=y0p, line=dict(color="#999", width=1, dash="dot"))
        x += val

# Cult.fit strip (upper)
strip(cult, 6.4, 8.2, "Cult.fit's stakeholder (in %)", 0.845)
labels_for(cult, 6.4/10*0.87+0.05, 8.2/10*0.87+0.05, 0.80, 0.595)
# Curefoods strip (lower)
strip(cure, 1.4, 3.2, "Curefoods' stakeholder (in %)", 0.475)
labels_for(cure, 1.4/10*0.87+0.05, 3.2/10*0.87+0.05, 0.43, 0.205)

ks.header(fig, "Two caps, one table",
          "Cult.fit and Curefoods may have gone separate ways, but<br>share key investors at the top",
          style="serif", title_size=58, subtitle_size=22, y_title=0.99, y_sub=0.925)
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=0.045, showarrow=False,
                   text="Note: The numbers are rounded off",
                   font=dict(family=ks.BODY, size=14, color=ks.INK))
ks.footer(fig, "Graphic by Sakshi M, 15 Jul '25", "Source: DRHP, Tracxn", y=0.0)

if __name__ == "__main__":
    print(ks.render(fig, "ch18_two_caps"))
