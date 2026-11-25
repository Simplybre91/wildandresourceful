#!/usr/bin/env python3
"""Builds the Wild & Resourceful site.

Posts live in _src/posts/<slug>.html: a JSON header in an HTML comment, then the post body.
Run:  python3 _src/build.py   (writes the pages into the repo root)
"""
import json, re, html, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "_src"
SITE_URL = "https://wildandresourceful.com"
SITE_NAME = "Wild & Resourceful"
TAGLINE = "Useful posts for everyday life."
CATS = ["Outdoors", "Tech", "Trades", "Shopping", "AI", "Deals", "Travel"]

LINKS = [
    ("gumroad", "Gumroad", "https://ranumbreanna.gumroad.com", "All my products live here. This site just links out."),
    ("amazon", "Amazon", "https://link.amazon/B0ajHIUrO", "simplybre's Amazon Page: things I actually use."),
    ("pinterest", "Pinterest", "https://www.pinterest.com/SimplyBreBusiness/", "@SimplyBreBusiness: every post gets a pin."),
    ("instagram", "Instagram", "https://www.instagram.com/glowupinsilence91/", "@glowupinsilence91: products and books."),
]
ICONS = {
    "gumroad": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 8h14l-1 12H6L5 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
    "amazon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="9" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/><path d="M3 4h2l2.4 11h10.4L20 7H6.2"/></svg>',
    "pinterest": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 22v-7"/><path d="M8 3h8l-1 6 3 3H6l3-3-1-6z"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
}
DEAL = ("The Subscription Audit Checklist is free on Gumroad right now. Find the subscriptions you're not using before the next renewal hits.",
        "https://ranumbreanna.gumroad.com/l/dmttiu", "Get it on Gumroad →")
# Trending: slugs in order (top = #1). Unknown slugs are skipped.
TRENDING = ["how-to-get-contractor-license-minnesota", "start-house-cleaning-business-school-hours"]

e = lambda s: html.escape(str(s), quote=True)
cslug = lambda c: c.lower()


def load_posts():
    posts = []
    for f in sorted((SRC / "posts").glob("*.html")):
        raw = f.read_text()
        m = re.match(r"\s*<!--(.*?)-->\s*(.*)", raw, re.S)
        meta = json.loads(m.group(1)); meta["body"] = m.group(2).strip()
        meta.setdefault("slug", f.stem)
        posts.append(meta)
    return sorted(posts, key=lambda p: p["date"], reverse=True)


def fdate(d):
    return datetime.date.fromisoformat(d).strftime("%b %-d, %Y")


def icons():
    return "".join(f'<a href="{u}" target="_blank" rel="noopener" title="{n}" aria-label="{n}">{ICONS[k]}</a>' for k, n, u, _ in LINKS)


def page(title, desc, path, main, side, active=None, extra_head=""):
    canon = SITE_URL + path
    nav = f'<a href="/" class="{"on" if active is None else ""}">Home</a>' + "".join(
        f'<a href="/category/{cslug(c)}/" class="{"on" if active == c else ""}">{c}</a>' for c in CATS)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
{extra_head}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="/"><b>{SITE_NAME}</b><span>{TAGLINE}</span></a>
  <form class="search" action="/search/" method="get" role="search"><input name="q" type="search" placeholder="Search posts…" aria-label="Search posts"><button type="submit">Search</button></form>
  <div class="icons">{icons()}</div>
  <a class="sub-btn" href="#subscribe">Subscribe</a>
</div></header>
<nav class="cats" aria-label="Categories"><div class="wrap">{nav}</div></nav>
<div class="wrap page"><main id="main">{main}</main><aside id="side">{side}</aside></div>
<footer><div class="wrap"><span>{SITE_NAME}: a blog, not a store. Products live on Gumroad. New posts Monday, Wednesday and Friday.</span><div class="icons">{icons()}</div></div></footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""


def sidebar(posts, current=None):
    others = [p for p in posts if p is not current]
    if current:
        others = [p for p in others if p["cat"] == current["cat"]] + [p for p in others if p["cat"] != current["cat"]]
    related = others[:5]
    by = {p["slug"]: p for p in posts}
    trend = [by[s] for s in TRENDING if s in by][:5]
    out = """<section class="subbox" id="subscribe"><h3>Like posts like this?</h3>
<div>Subscribe free. One email when something's actually worth your time:</div>
<ul><li>New blog posts (Mon, Wed, Fri)</li><li>Deals worth clicking, when I find them</li><li>New products, the day they go live</li></ul>
<form class="subForm"><input type="email" name="email" required placeholder="Your email address" aria-label="Your email address"><button class="sub-btn" type="submit">Subscribe — it's free</button></form>
<div class="ok">Thanks! Check your inbox to confirm.</div></section>
<p class="rhythm">New posts every Monday, Wednesday and Friday.</p>"""
    out += '<section class="follow"><h3>Follow &amp; shop</h3>' + "".join(
        f'<a href="{u}" target="_blank" rel="noopener"><span>{ICONS[k]}</span><div><b>{n}</b><small>{e(note)}</small></div></a>' for k, n, u, note in LINKS) + "</section>"
    if related:
        out += '<section><h3>You might be interested in</h3>' + "".join(
            f'<a class="mini" href="/{p["slug"]}/"><span class="thumb">{e(p["cat"])}</span><div><em>{e(p["cat"])}</em><b>{e(p["title"])}</b></div></a>' for p in related) + "</section>"
    if trend:
        out += '<section><h3>Trending this week</h3><ol class="trend">' + "".join(
            f'<li><div><a href="/{p["slug"]}/">{e(p["title"])}</a><small>{e(p["cat"])} · {fdate(p["date"])}</small></div></li>' for p in trend) + "</ol></section>"
    out += f'<section class="deal"><h3>Deal of the week</h3><p>{e(DEAL[0])}</p><a class="go" href="{DEAL[1]}" target="_blank" rel="noopener">{e(DEAL[2])}</a></section>'
    out += '<section class="browse"><h3>Browse by category</h3>'
    for c in CATS:
        n = sum(1 for p in posts if p["cat"] == c)
        out += f'<a href="/category/{cslug(c)}/"><span>{c}</span><small>{(str(n) + (" post" if n == 1 else " posts")) if n else "Coming soon"}</small></a>'
    return out + "</section>"


def feed_main(posts, cat=None):
    lst = [p for p in posts if not cat or p["cat"] == cat]
    head = cat or "Latest posts"
    sub = f"Everything filed under {cat}." if cat else "Useful posts for everyday life: outdoors, home, tech, trades, saving money and more."
    chips = f'<a href="/" class="{"on" if not cat else ""}">All</a>' + "".join(
        f'<a href="/category/{cslug(c)}/" class="{"on" if cat == c else ""}">{c}</a>' for c in CATS)
    items = "".join(f"""<div class="item"><a class="thumb" href="/{p['slug']}/" aria-hidden="true" tabindex="-1">{e(p['cat'])}</a>
<div><span class="label" style="margin-top:0">{e(p['cat'])}</span><h2><a href="/{p['slug']}/">{e(p['title'])}</a></h2>
<p>{e(p['dek'])}</p><small>{fdate(p['date'])} · {p['read']} min read</small></div></div>""" for p in lst)
    if not items:
        items = '<div class="empty">Posts in this category are coming soon. New posts go up Monday, Wednesday and Friday.</div>'
    return f'<div class="feed-head"><h1>{e(head)}</h1><p>{e(sub)}</p></div><div class="chips">{chips}</div>{items}'


def post_main(p):
    photo = ""
    if p.get("photo"):
        cap = f'<figcaption>{e(p["photoCaption"])}</figcaption>' if p.get("photoCaption") else ""
        photo = f'<figure><img src="{e(p["photo"])}" alt="{e(p.get("photoCaption") or p["title"])}">{cap}</figure>'
    tags = "".join(f"<span>{e(t)}</span>" for t in p.get("tags", []))
    return f"""<article>
<div class="crumb"><a href="/">Home</a> » <a href="/category/{cslug(p['cat'])}/">{e(p['cat'])}</a></div>
<span class="label">{e(p['cat'])}</span>
<h1>{e(p['title'])}</h1>
<div class="meta">{fdate(p['date'])} · {p['read']} minute read · Filed under <a href="/category/{cslug(p['cat'])}/">{e(p['cat'])}</a></div>
{photo}
{p['body']}
<div class="next"><b>Your one next step</b>{e(p['next'])}</div>
<div class="tags">{tags}</div>
</article>"""


def write(path, text):
    f = ROOT / path.strip("/") / "index.html" if not path.endswith(".xml") and not path.endswith(".txt") and not path.endswith(".json") else ROOT / path.strip("/")
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text)


def main():
    posts = load_posts()
    for p in posts:
        assert p["cat"] in CATS, f'{p["slug"]}: unknown category {p["cat"]}'
    write("/", page(f"{SITE_NAME} — {TAGLINE}", "Useful posts for everyday life: outdoors, home, tech, trades, shopping, AI, deals and travel. New posts Monday, Wednesday and Friday.",
                    "/", feed_main(posts), sidebar(posts)))
    for c in CATS:
        write(f"/category/{cslug(c)}/", page(f"{c} — {SITE_NAME}", f"{c} posts from {SITE_NAME}: useful posts for everyday life.",
                                             f"/category/{cslug(c)}/", feed_main(posts, c), sidebar(posts), active=c))
    for p in posts:
        ld = json.dumps({"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "datePublished": p["date"],
                         "author": {"@type": "Person", "name": "Simply Bre"}, "description": p["dek"],
                         "mainEntityOfPage": f"{SITE_URL}/{p['slug']}/"})
        write(f"/{p['slug']}/", page(f"{p['title']} — {SITE_NAME}", p["dek"], f"/{p['slug']}/", post_main(p), sidebar(posts, p),
                                     active=p["cat"], extra_head=f'<meta property="og:type" content="article"><script type="application/ld+json">{ld}</script>'))
    write("/search/", page(f"Search — {SITE_NAME}", "Search posts on Wild & Resourceful.", "/search/",
                           '<div class="feed-head"><h1 id="sh">Search</h1><p id="sc"></p></div><div id="results"></div>', sidebar(posts),
                           extra_head='<meta name="robots" content="noindex">'))
    idx = [{"slug": p["slug"], "title": p["title"], "dek": p["dek"], "cat": p["cat"], "date": fdate(p["date"]), "read": p["read"],
            "text": re.sub(r"<[^>]+>", " ", p["body"]) + " " + " ".join(p.get("tags", []))} for p in posts]
    write("/posts.json", json.dumps(idx))
    urls = ["/"] + [f"/category/{cslug(c)}/" for c in CATS] + [f"/{p['slug']}/" for p in posts]
    write("/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          "".join(f"<url><loc>{SITE_URL}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("/robots.txt", f"User-agent: *\nDisallow: /_src/\nDisallow: /search/\nSitemap: {SITE_URL}/sitemap.xml\n")
    print(f"Built {len(posts)} posts, {len(CATS)} categories.")


if __name__ == "__main__":
    main()
