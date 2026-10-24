"""Fetch the latest uploads from the Johnny's Music Lab YouTube RSS feed into data/youtube.json."""
import json
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

CHANNEL_ID = "UCVhJVJStOItucQ5JFmFjYQQ"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
OUT = Path(__file__).resolve().parents[2] / "data" / "youtube.json"

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}

with urllib.request.urlopen(FEED_URL, timeout=30) as resp:
    root = ET.fromstring(resp.read())

items = []
for entry in root.findall("atom:entry", NS):
    vid = entry.findtext("yt:videoId", namespaces=NS)
    items.append({
        "id": vid,
        "title": entry.findtext("atom:title", namespaces=NS),
        "link": entry.find("atom:link", NS).get("href"),
        "published": entry.findtext("atom:published", namespaces=NS),
        "thumbnail": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
    })

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({"items": items}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Wrote {len(items)} videos to {OUT}")
