"""
ch03 — "FINTECH FRENZY" (The Ken, heavy older style)
Left: total funding by sector (vertical bars; Fintech highlighted).
Right: fintech sub-sector breakdown (horizontal bars) in a grey panel,
linked with an arrow.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

NAVY, AMBER = ks.KEN["navy"], ks.KEN["gold"]

sectors = ["Hyper<br>local", "Food<br>tech", "Ride<br>hailing", "E commerce", "Fintech"]
svals   = [2.5, 3.4, 3.6, 17.7, 9.7]
scolors = [NAVY, NAVY, NAVY, NAVY, AMBER]

fin = [("Payments", 4271.7), ("Alternative Lending", 1658.5), ("Others", 997.6),
       ("Internet First<br>Insurance Platforms", 980.03), ("Consumer Finance", 841.4),
       ("Finance &<br>Accounting Tech", 510.3), ("Investment Tech", 359.0),
       ("Robo Advisors", 76.8)]
fin_names = [f[0] for f in fin]; fin_vals = [f[1] for f in fin]

fig = ks.canvas(width=1000, height=680, bg=ks.WHITE, plot_y=(0.10, 0.70))

# grey panel behind right chart
fig.add_shape(type="rect", xref="paper", yref="paper",
              x0=0.50, x1=1.0, y0=0.06, y1=0.80, fillcolor="#EFEFEF",
              line=dict(width=0), layer="below")

# left vertical bars
fig.add_trace(go.Bar(x=sectors, y=svals, marker=dict(color=scolors), width=0.55,
              text=[f"<b>{v}</b>" for v in svals], textposition="outside",
              textfont=dict(family=ks.BODY, size=18, color=ks.INK), cliponaxis=False,
              xaxis="x", yaxis="y", hovertemplate="%{x}: $%{y} bn<extra></extra>"))
fig.update_layout(
    xaxis=dict(domain=[0.04,0.46], anchor="y", visible=True, showticklabels=True,
               showline=False, showgrid=False, zeroline=False,
               tickfont=dict(family=ks.BODY, size=14, color=ks.INK), ticks="",
               range=[-0.6,4.6], fixedrange=True),
    yaxis=dict(domain=[0.10,0.62], anchor="x", visible=False, range=[0,20], fixedrange=True),
)
fig.add_shape(type="line", xref="x", yref="y", x0=-0.6, x1=4.6, y0=0, y1=0,
              line=dict(color=ks.INK, width=2))

# right horizontal bars (xaxis2/yaxis2)
fig.add_trace(go.Bar(y=fin_names, x=fin_vals, orientation="h", marker=dict(color=AMBER),
              width=0.62, text=[f"<b>{v:,.1f}</b>" if v != 980.03 else "<b>980.03</b>" for v in fin_vals],
              textposition="outside", textfont=dict(family=ks.BODY, size=14, color=ks.INK),
              cliponaxis=False, xaxis="x2", yaxis="y2",
              hovertemplate="%{y}: $%{x} mn<extra></extra>"))
fig.update_layout(
    xaxis2=dict(domain=[0.76,0.985], anchor="y2", visible=False, range=[0,5200], fixedrange=True),
    yaxis2=dict(domain=[0.08,0.74], anchor="x2", autorange="reversed", ticks="",
                tickfont=dict(family=ks.BODY, size=13, color=ks.INK),
                showgrid=False, zeroline=False, fixedrange=True),
)

fig.add_annotation(xref="paper", yref="paper", x=0.04, y=0.82, xanchor="left",
                   text="Total funding by Sector <b>($ bn)</b>", showarrow=False,
                   font=dict(family=ks.BODY, size=18, color="#444"))
fig.add_annotation(xref="paper", yref="paper", x=0.755, y=0.82, xanchor="center",
                   text="Fintech funding <b>($ mn)</b>", showarrow=False,
                   font=dict(family=ks.BODY, size=18, color="#444"))
ks.paper_arrow(fig, x_head=0.515, y_head=0.60, dx_px=-70, dy_px=0, width=1.5)

ks.header(fig, "Fintech frenzy",
          "In the last decade, fintechs saw most investments after e-commerce",
          style="heavy", title_size=44, subtitle_size=17, y_title=0.99, y_sub=0.885)
ks.footer(fig, "Graphic by Prajakta Patil", "Source: Tracxn", y=0.01,
          wordmark="THE-KEN", brand_color=ks.GREY)

if __name__ == "__main__":
    print(ks.render(fig, "ch03_fintech_frenzy"))
