"""
ch19 — "Crucial anchor" (The Ken)
Top: a Sankey of IPO proceeds -> anchor investors -> investor types.
Bottom: nested horizontal bars (total / anchor book / mutual funds) per IPO.
NOTE: anchor-book and mutual-fund sub-values in the bottom panel are visual
estimates (only totals are published in the source).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kenstyle as ks
import plotly.graph_objects as go

W, H = 1100, 1320
GOLD="#F5B81E"; GREEN="#16A085"; TEAL="#36C5E0"; PINK="#F06FB0"
GREY="#BDBDBD"; ORANGE="#F39237"; RED="#E23B2E"; BLUE="#2D9CDB"; PUR="#7B5BD0"

fig = ks.canvas(width=W, height=H, bg=ks.CREAM)
fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False))

# ── Sankey (top) ─────────────────────────────────────────────────────────────
labels = ["Total IPO proceeds\n534,231", "Anchor investors\n189,459", "",
          "Foreign Portfolio\nInvestors (FPIs)  89,058", "Mutual Funds  71,504",
          "Insurance companies  16,431", "Alternative Investment Funds  6,749",
          "Venture-capital firms  1,215", "Financial Institutions/banks  126",
          "Others  4,376"]
node_colors = [PUR, BLUE, PUR, GOLD, GREEN, TEAL, PINK, GREY, ORANGE, RED]
src = [0,0, 1,1,1,1,1,1,1]
tgt = [1,2, 3,4,5,6,7,8,9]
val = [189459,344772, 89058,71504,16431,6749,1215,126,4376]
link_colors = ["rgba(80,140,220,0.45)","rgba(140,110,210,0.45)",
               "rgba(245,184,30,0.5)","rgba(22,160,133,0.5)","rgba(54,197,224,0.5)",
               "rgba(240,111,176,0.55)","rgba(189,189,189,0.55)","rgba(243,146,55,0.6)",
               "rgba(226,59,46,0.6)"]
fig.add_trace(go.Sankey(
    arrangement="snap",
    domain=dict(x=[0.10, 0.72], y=[0.40, 0.80]),
    node=dict(label=labels, color=node_colors, pad=14, thickness=26,
              line=dict(width=0),
              x=[0.01, 0.35, 0.35, 0.99,0.99,0.99,0.99,0.99,0.99,0.99],
              y=[0.55, 0.30, 0.80, 0.10,0.30,0.46,0.58,0.66,0.72,0.80]),
    link=dict(source=src, target=tgt, value=val, color=link_colors),
    textfont=dict(family=ks.BODY, size=12, color=ks.INK)))
fig.add_annotation(xref="paper", yref="paper", x=0.40, y=0.395, showarrow=False,
                   text="* until 11 November 2025", font=dict(family=ks.BODY,size=13,color="#666"))
fig.add_annotation(xref="paper", yref="paper", x=0.41, y=0.55, showarrow=False,
                   text="<b>38%</b>", font=dict(family=ks.BODY,size=15,color=ks.INK))

# ── Nested bars (bottom) ─────────────────────────────────────────────────────
comp = ["Hyundai Motor India","One 97 Communications","LIC","Swiggy","Tata Capital",
        "Zomato","NTPC Green Energy","LG Electronics India","HDB Financial Services",
        "Lenskart Solutions"]
total  = [27859,18300,20557,11327,15512,9375,10000,11605,12500,7278]
anchor = [8200,8200,5500,5000,4500,4100,3900,3400,3300,3200]   # estimated
mf     = [2800,1000,700,2100,1500,1300,1500,1600,1300,1100]    # estimated
yy = list(range(len(comp)))[::-1]

fig.update_layout(
    barmode="overlay",
    xaxis2=dict(domain=[0.18,0.93], anchor="y2", range=[0,30000], visible=True, showgrid=False,
                zeroline=False, tickmode="array", tickvals=[0,10000,20000,30000],
                ticktext=["0","10,000","20,000","30,000"], ticks="",
                tickfont=dict(family=ks.BODY,size=13,color=ks.INK), fixedrange=True),
    yaxis2=dict(domain=[0.05,0.27], anchor="x2", range=[-0.7,len(comp)-0.3], visible=True,
                tickmode="array", tickvals=yy, ticktext=comp, ticks="", showgrid=False,
                zeroline=False, tickfont=dict(family=ks.BODY,size=13,color=ks.INK), fixedrange=True),
)
fig.add_trace(go.Bar(y=yy, x=total, orientation="h", width=0.62, marker_color="#1746C9",
              xaxis="x2", yaxis="y2", cliponaxis=False, hoverinfo="skip"))
fig.add_trace(go.Bar(y=yy, x=anchor, orientation="h", width=0.62, marker_color=BLUE,
              xaxis="x2", yaxis="y2", cliponaxis=False, hoverinfo="skip"))
fig.add_trace(go.Bar(y=yy, x=mf, orientation="h", width=0.62, marker_color="#4FE0A0",
              xaxis="x2", yaxis="y2", cliponaxis=False, hoverinfo="skip"))
for y, t in zip(yy, total):
    fig.add_annotation(x=t+400, y=y, xref="x2", yref="y2", xanchor="left", showarrow=False,
                       text=f"<b>{t:,}</b>", font=dict(family=ks.BODY, size=13, color=ks.INK))

fig.add_annotation(xref="paper", yref="paper", x=0.5, y=0.335, showarrow=False,
                   text="In India's biggest IPOs...", font=dict(family=ks.SERIF, size=26, color=ks.INK))
ks.legend_chips(fig, [("Total IPO proceeds","#1746C9"),("Anchor book",BLUE),("Mutual funds","#4FE0A0")],
                y=0.305, xs=[0.22,0.46,0.66], size=15)

ks.header(fig, "Crucial anchor",
          "Anchor investors, especially mutual funds, played a big role in India's IPOs,<br>including its biggest ones",
          style="serif", title_size=62, subtitle_size=22, y_title=0.985, y_sub=0.93)
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=0.85, showarrow=False,
                   text="All figures in Rs crore", font=dict(family=ks.BODY,size=15,color="#555"))
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=0.825, showarrow=False,
                   text="IPOs between January 2021 and November* 2025",
                   font=dict(family=ks.SERIF,size=22,color=ks.INK))
ks.footer(fig, "Graphic by Sakshi M, 17 Nov '25", "Source: Prime Database", y=0.0)

if __name__ == "__main__":
    print(ks.render(fig, "ch19_crucial_anchor"))
