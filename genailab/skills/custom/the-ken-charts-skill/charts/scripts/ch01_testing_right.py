"""
ch01 — "Testing right" (The Ken)
100% horizontal stacked bar: how Indian exam boards split question types.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

states = ["Haryana", "Punjab", "Kerala", "Uttar Pradesh", "Andhra Pradesh",
          "CISCE", "Gujarat", "Odisha", "Nagaland", "West Bengal",
          "Maharashtra", "Himachal Pradesh"]
# stack order per bar: Analysis, Application, Memory, Understanding
analysis      = [0,     22.91, 9.62,  0,     41.67, 23.17, 24.32, 21.54, 22.22, 6.67,  16.28, 25]
application   = [28.68, 8.81,  20.19, 0,     39.58, 34.15, 25.68, 0,     0,     45,    41.86, 9.38]
memory        = [64.71, 26.43, 8.65,  12.24, 0,     0,     8.11,  50.77, 4.76,  0,     4.65,  53.12]
understanding = [6.61,  41.85, 61.54, 87.76, 18.75, 42.68, 41.89, 27.69, 73.02, 48.33, 37.21, 12.5]

cats = [
    ("Analysis",      analysis,      ks.KEN["teal_dk"], "white"),
    ("Application",   application,   ks.KEN["cyan"],    ks.INK),
    ("Memory",        memory,        ks.KEN["magenta"], ks.INK),
    ("Understanding", understanding, ks.KEN["gold"],    ks.INK),
]

fig = ks.canvas(width=1120, height=1200, bg=ks.CREAM,
                plot_x=(0.155, 0.99), plot_y=(0.045, 0.78))

for name, vals, color, txtcol in cats:
    fig.add_trace(go.Bar(
        y=states, x=vals, orientation="h", name=name,
        marker=dict(color=color, line=dict(width=0)),
        text=[f"<b>{v:g}</b>" if v > 0 else "" for v in vals],
        textposition="inside", insidetextanchor="middle",
        textfont=dict(family=ks.BODY, size=21, color=txtcol),
        cliponaxis=False, hovertemplate="%{y}<br>"+name+": %{x}%<extra></extra>",
    ))

fig.update_layout(
    barmode="stack", bargap=0.30,
    xaxis=dict(domain=[0.155, 0.99], visible=False, range=[0, 100], fixedrange=True),
    yaxis=dict(domain=[0.045, 0.78], visible=True, autorange="reversed",
               tickfont=dict(family=ks.BODY, size=21, color=ks.INK),
               showgrid=False, zeroline=False, ticks="", fixedrange=True,
               ticklabelposition="outside left"),
)

ks.header(fig, "Testing right",
          "Some boards focus more on questions that test rote-<br>"
          "learning rather than real-world application",
          style="serif", title_size=68, subtitle_size=27,
          y_title=0.975, y_sub=0.905)

# legend chips
items = [("Analysis", ks.KEN["teal_dk"]), ("Application", ks.KEN["cyan"]),
         ("Memory", ks.KEN["magenta"]), ("Understanding", ks.KEN["gold"])]
ks.legend_chips(fig, items, y=0.815, xs=[0.155, 0.36, 0.58, 0.77], size=22)
fig.add_annotation(xref="paper", yref="paper", x=0.50, y=0.792, showarrow=False,
                   text="(in %)", font=dict(family=ks.BODY, size=18, color=ks.INK))

ks.footer(fig, "Graphic by Kashvi B, 16 Apr '25",
          "Source: Equivalence of Boards report, 2024 by NCERT Parakh", y=0.012)

if __name__ == "__main__":
    print(ks.render(fig, "ch01_testing_right"))
