#!/usr/bin/env python3
"""Erzeugt die Weiterleitungsseiten r/kNNN/index.html.

Aufruf:  python3 build.py [kunden.json] [anzahl]
kunden.json (privat, NICHT ins Repo): {"k001": {"name": "Beispiel", "url": "https://g.page/r/XXXX/review"}}
Nicht zugewiesene Nummern leiten auf die Startseite weiter.
Nur https-Links zu google.com / g.page / goo.gl / maps.app.goo.gl sind erlaubt.
"""
import json, os, sys
from urllib.parse import urlparse
from html import escape

ALLOWED = ("google.com", "g.page", "goo.gl", "maps.app.goo.gl", "g.co")
HOME = "https://triageshop.art/"

def ok(url):
    u = urlparse(url)
    host = (u.hostname or "").lower()
    return u.scheme == "https" and any(host == d or host.endswith("." + d) for d in ALLOWED)

TEMPLATE = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Weiterleitung</title>
<meta http-equiv="refresh" content="0; url={url}">
<link rel="canonical" href="{url}">
<script>location.replace({jsurl});</script>
<style>body{{font-family:Arial,sans-serif;margin:48px 20px;color:#14213D}}a{{color:#14213D;font-weight:700}}</style>
</head>
<body>
<p>Weiterleitung zur Bewertungsseite &hellip; <a href="{url}">Hier klicken, falls nichts passiert.</a></p>
</body>
</html>
"""

def main():
    cust_file = sys.argv[1] if len(sys.argv) > 1 else None
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    customers = {}
    if cust_file and os.path.exists(cust_file):
        customers = json.load(open(cust_file, encoding="utf-8"))
    root = os.path.dirname(os.path.abspath(__file__))
    ids = [f"k{n:03d}" for n in range(1, count + 1)]
    ids += [i for i in customers if i not in ids]
    for i in ids:
        url = HOME
        if i in customers:
            url = customers[i]["url"].strip()
            if not ok(url):
                sys.exit(f"{i}: Link nicht erlaubt oder kein https: {url}")
        d = os.path.join(root, "r", i)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(TEMPLATE.format(url=escape(url, quote=True), jsurl=json.dumps(url)))
    print(f"{len(ids)} Weiterleitungen erzeugt, {len(customers)} zugewiesen.")

if __name__ == "__main__":
    main()
