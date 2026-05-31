"""
build_all.py — render every chXX_*.py to an interactive HTML file in ./html/
and write an index.html linking them. Pure Plotly, no Chrome/Kaleido.

Usage:  python build_all.py
"""
import os, sys, glob, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kenstyle as ks

TITLES = {
    "ch01_testing_right": "Testing right",
    "ch02_tables_turned": "Tables turned",
    "ch03_fintech_frenzy": "Fintech frenzy",
    "ch04_coming_of_age": "Coming of age",
    "ch05_range_of_roadsters": "Range of roadsters",
    "ch06_shooting_for_the_moon": "Shooting for the moon",
    "ch07_doubling_down": "Doubling down",
    "ch08_funding_funnel": "The funding funnel",
    "ch09_food_anchor": "The food anchor",
    "ch10_giant_momo": "Giant MoMo",
    "ch11_turning_the_tables": "Turning the tables",
    "ch12_bumper_year": "Bumper year",
    "ch13_main_character": "Becoming the main character",
    "ch14_bhx_pie": "BHX's piece of the pie",
    "ch15_lay_of_the_land": "Lay of the land",
    "ch16_upstart_faceoff": "Upstart face-off",
    "ch17_reliance_ebidta": "Reliance's EBIDTA game",
    "ch18_two_caps": "Two caps, one table",
    "ch19_crucial_anchor": "Crucial anchor",
}

def main():
    mods = sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(HERE, "ch*.py")))
    os.makedirs(ks.OUTDIR, exist_ok=True)
    built = []
    for name in mods:
        mod = importlib.import_module(name)
        path = ks.render(mod.fig, name)
        built.append((name, os.path.basename(path)))
        print("built", path)

    # index.html
    cards = "\n".join(
        f'<a class="card" href="html/{fn}"><span class="n">{name.split("_")[0].upper()}</span>'
        f'<span class="t">{TITLES.get(name, name)}</span></a>'
        for name, fn in built)
    html = f"""<!doctype html><html><head><meta charset="utf-8">
<title>The Ken — chart replications</title>
<style>
 body{{background:#F7F4EF;font-family:'Libre Franklin',Arial,sans-serif;margin:0;padding:40px;color:#1A1A1A}}
 h1{{font-family:'Playfair Display',Georgia,serif;font-size:42px;margin:0 0 6px}}
 p.sub{{color:#9A958C;margin:0 0 28px}}
 .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}}
 .card{{display:flex;flex-direction:column;gap:6px;text-decoration:none;background:#fff;
   border:1px solid #ECEAE5;border-radius:10px;padding:18px 20px;color:#1A1A1A;transition:.15s}}
 .card:hover{{transform:translateY(-2px);box-shadow:0 6px 18px rgba(0,0,0,.07)}}
 .n{{font-size:12px;letter-spacing:.08em;color:#15A89C;font-weight:700}}
 .t{{font-family:'Playfair Display',Georgia,serif;font-size:20px}}
</style></head><body>
<h1>The Ken — chart replications</h1>
<p class="sub">{len(built)} interactive Plotly charts. Click any to open.</p>
<div class="grid">{cards}</div>
</body></html>"""
    idx = os.path.join(HERE, "index.html")
    with open(idx, "w") as f:
        f.write(html)
    print("built", idx)

if __name__ == "__main__":
    main()
