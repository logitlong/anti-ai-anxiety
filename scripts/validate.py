"""Checks the site data before each deploy. Exit code 1 blocks the deploy."""
import json, re, sys
err = []
def need(cond, msg):
    if not cond: err.append(msg)
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
def tri(x, where):
    need(isinstance(x, dict) and all(isinstance(x.get(k), str) and x[k].strip() for k in ("zh", "ja", "en")),
         f"{where}: needs non-empty zh / ja / en text")
data = {}
for f in ["events.json", "feed.json", "graveyard.json", "deaths.json", "voices.json", "skills.json"]:
    try:
        data[f] = json.load(open(f, encoding="utf-8"))
    except Exception as e:
        err.append(f"{f}: not valid JSON ({e})")
if "feed.json" in data:
    F = data["feed.json"]
    need(DATE.match(str(F.get("updated", ""))), "feed.json: 'updated' must be YYYY-MM-DD")
    items = F.get("items", [])
    need(isinstance(items, list) and items, "feed.json: 'items' must be a non-empty list")
    need(len(items) <= 80, "feed.json: keep at most 80 items")
    srcs = set()
    for i, x in enumerate(items):
        w = f"feed.json items[{i}]"
        need(DATE.match(str(x.get("d", ""))), f"{w}: 'd' must be YYYY-MM-DD")
        need(x.get("verdict") in ("skip", "try", "wait"), f"{w}: verdict must be skip / try / wait")
        need(x.get("panic") in (1, 2, 3, 4, 5), f"{w}: panic must be 1-5")
        tri(x.get("t"), w + ".t"); tri(x.get("why"), w + ".why")
        need(str(x.get("src", "")).startswith("http"), f"{w}: src must be a URL")
        k = (x.get("src"), (x.get("t") or {}).get("en"))
        need(k not in srcs, f"{w}: duplicate item"); srcs.add(k)
if "events.json" in data:
    seen = set()
    for i, e in enumerate(data["events.json"].get("events", [])):
        w = f"events.json events[{i}]"
        need(DATE.match(str(e.get("d", ""))), f"{w}: 'd' must be YYYY-MM-DD")
        need(e.get("r") in ("us", "cn"), f"{w}: r must be us / cn")
        need(e.get("c") in ("model", "product", "price", "voice", "oss", "shutdown", "policy", "agent", "people"), f"{w}: bad category c")
        need(e.get("p") in (1, 2, 3, 4, 5), f"{w}: p must be 1-5")
        tri(e.get("t"), w + ".t")
        need(str(e.get("src", "")).startswith("http"), f"{w}: src must be a URL")
        if "f" in e or "o" in e:
            tri(e.get("f"), w + ".f"); tri(e.get("o"), w + ".o"); tri(e.get("life"), w + ".life")
        k = (e.get("d"), (e.get("t") or {}).get("en"))
        need(k not in seen, f"{w}: duplicate event"); seen.add(k)
if err:
    print("Data check failed:\n- " + "\n- ".join(err[:50])); sys.exit(1)
print("Data check passed:", len(data["events.json"]["events"]), "events,", len(data["feed.json"]["items"]), "feed items")
