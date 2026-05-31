"""
ch02 — "TABLES TURNED" (The Ken, heavy older style)
Multi-line time series of browser market share, Jan 2013 - Apr 2019.
Monthly points interpolated through control points (original monthly series
isn't published) to recreate the curve shapes.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go
import numpy as np

def series(ctrl):
    xs = np.array([c[0] for c in ctrl]); ys = np.array([c[1] for c in ctrl])
    fine = np.arange(0, 76)
    return fine, np.interp(fine, xs, ys)

chrome = series([(0,0.17),(6,1),(12,3),(18,5),(24,8),(30,11),(36,14),
                 (42,18),(48,24),(54,30),(60,38),(66,46),(70,52),(73,57),(75,59.0)])
uc     = series([(0,26.4),(6,29),(12,34),(18,40),(24,46),(30,54),(36,59),(37,59),
                 (38,46),(40,57),(44,56),(48,54),(52,52),(56,48),(60,44),(66,38),
                 (72,30),(73,25),(75,24.5)])
opera  = series([(0,30.9),(6,31),(10,33),(12,32),(18,28),(24,24),(30,20),(36,16),
                 (42,13),(48,10),(54,8),(60,7),(66,6.5),(72,6),(75,5.38)])
others = series([(0,42.5),(6,41),(12,38),(18,33),(24,28),(30,22),(36,17),(42,14),
                 (48,13),(54,12),(60,12),(66,12),(70,12),(73,11.5),(75,11.1)])

lines = [
    ("Google Chrome", chrome, ks.KEN["gold"], 59.0, "59.0", 0.17),
    ("UC Browser",    uc,     "#4F6FD0",       24.5, "24.5", 26.4),
    ("Opera",         opera,  ks.KEN["red"],   5.38, "5.38", 30.9),
    ("Others",        others, "#2FD6C6",       11.1, "11.1", 42.5),
]

fig = ks.canvas(width=900, height=620, bg=ks.WHITE, plot_x=(0.07, 0.90), plot_y=(0.12, 0.74))

for name, (xs, ys), color, endv, endlbl, startv in lines:
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name=name,
                  line=dict(color=color, width=3.2, shape="spline", smoothing=1.0),
                  cliponaxis=False, hovertemplate=name+": %{y:.1f}%<extra></extra>"))
    for xv, val in [(0, startv), (75, endv)]:
        fig.add_trace(go.Scatter(x=[xv], y=[val], mode="markers", showlegend=False,
                      marker=dict(symbol="square-open", size=9, color=color,
                                  line=dict(width=2)), cliponaxis=False,
                      hoverinfo="skip"))
    fig.add_annotation(x=77, y=endv, text=f"<b>{endlbl}</b>", showarrow=False,
                       xanchor="left", font=dict(family=ks.BODY, size=15, color=ks.INK))
    lab_y = startv if startv >= 3 else startv + 3.0
    fig.add_annotation(x=-2, y=lab_y, text=f"<b>{startv}</b>", showarrow=False,
                       xanchor="right", font=dict(family=ks.BODY, size=15, color=ks.INK))

tick_months = [0,12,24,36,48,60,72,75]
tick_text   = ["Jan<br>2013","Jan<br>2014","Jan<br>2015","Jan<br>2016",
               "Jan<br>2017","Jan<br>2018","Jan<br>2019","Apr<br>2019"]
fig.update_layout(
    xaxis=dict(domain=[0.07,0.90], visible=True, range=[-4,80], showgrid=False,
               zeroline=False, tickmode="array", tickvals=tick_months,
               ticktext=tick_text, ticks="", fixedrange=True,
               tickfont=dict(family=ks.BODY, size=12, color=ks.INK)),
    yaxis=dict(domain=[0.12,0.74], visible=True, range=[-3,64], showgrid=False,
               zeroline=False, tickmode="array", tickvals=[0,20,40,60], ticks="",
               fixedrange=True, tickfont=dict(family=ks.BODY, size=14, color=ks.INK)),
)

ks.header(fig, "Tables turned",
          "UC Browser has over the past couple of years tumbled fast",
          style="heavy", title_size=38, subtitle_size=16,
          x=0.0, anchor="left", y_title=0.99, y_sub=0.875)

items = [("Google Chrome", ks.KEN["gold"]), ("UC Browser", "#4F6FD0"),
         ("Opera", ks.KEN["red"]), ("Others", "#2FD6C6")]
ks.legend_chips(fig, items, y=0.80, xs=[0.07,0.30,0.50,0.64], size=14, glyph="━")
fig.add_annotation(xref="paper", yref="paper", x=0.80, y=0.80, xanchor="left",
                   text="(in %)", showarrow=False,
                   font=dict(family=ks.BODY, size=13, color=ks.INK))

ks.footer(fig, None, "Source: Statcounter", y=0.01, wordmark="THE-KEN", brand_color=ks.GREY)

if __name__ == "__main__":
    print(ks.render(fig, "ch02_tables_turned"))
