#!/usr/bin/env python3
"""Builds the full static site into dist/ for GitHub Pages:
core pages (from build.py), all migrated blog posts, blog index pages,
redirect stubs, sitemap.xml, robots.txt, 404, CNAME."""
import json, os, re, shutil, html, datetime, hashlib
import markdown
import build as B

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "docs")  # GitHub Pages serves /docs
SITE = B.SITE
FORM_ID = "aaSmOX0UTKOiDY0aSTeF"
FORM_EMBED = (f'<iframe src="https://api.leadconnectorhq.com/widget/form/{FORM_ID}" '
              f'style="width:100%;height:520px;border:none;border-radius:8px" id="inline-{FORM_ID}" '
              f'data-layout="{{\'id\':\'INLINE\'}}" data-trigger-type="alwaysShow" data-activation-type="alwaysActivated" '
              f'data-deactivation-type="neverDeactivate" data-form-name="Contact Form" data-height="520" '
              f'data-layout-iframe-id="inline-{FORM_ID}" data-form-id="{FORM_ID}" title="Get a cash offer"></iframe>'
              f'<script src="https://link.msgsndr.com/js/form_embed.js" defer></script>')

OLD_PHONES = [r"\(?904\)?[\s.-]*513[\s.-]*0229", r"\(?904\)?[\s.-]*245[\s.-]*1663",
              r"\(?904\)?[\s.-]*685[\s.-]*8754", r"\(?904\)?[\s.-]*565[\s.-]*2935"]

REDIRECTS = {
    "/generic-homepage/": "/", "/home-2/": "/", "/sitemap/": "/",
    "/sell-my-house-fast-saint-augustine-3/": "/sell-my-house-fast-saint-augustine/",
    "/privacy/": "/privacy-policy/", "/testimonials/page/2/": "/testimonials/",
    "/blog/author/equitygroup904/": "/blog/", "/sell-your-house/": "/get-a-cash-offer-today/",
    "/go/selling-to-a-professional/": "/compare/", "/go/stop-foreclosure/": "/avoiding-foreclosure/", "/go/we-buy-houses/": "/get-a-cash-offer-today/",
}

BLOG_CSS = """
.post{max-width:780px;margin:0 auto;padding:36px 16px 10px}.post h1{font-size:36px;line-height:1.2;margin:0 0 8px}
.post .meta{color:var(--mute);font-size:14px;margin-bottom:22px}.post img{max-width:100%;height:auto;border-radius:10px;margin:10px 0}
.post h2{font-size:26px;margin:30px 0 10px}.post h3{margin:24px 0 8px}.post li{margin:4px 0}
.postcta{background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:22px;margin:30px 0}
.plist{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.pcard{border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff;display:flex;flex-direction:column}
.pcard img{width:100%;aspect-ratio:16/9;object-fit:cover;background:var(--bg)}.pcard .in{padding:14px 16px}.pcard h3{font-size:18px;margin:0 0 6px}.pcard h3 a{color:var(--ink);text-decoration:none}
.pcard p{color:var(--mute);font-size:15px;margin:0}.pager{display:flex;gap:10px;justify-content:center;margin:28px 0;flex-wrap:wrap}.pager a,.pager span{padding:8px 12px;border:1px solid var(--line);border-radius:8px;text-decoration:none}
.pager span{background:var(--navy);color:#fff}
@media(max-width:860px){.plist{grid-template-columns:1fr}.post h1{font-size:28px}}
"""


def write(slug, content):
    path = os.path.join(DIST, slug.strip("/"), "index.html") if slug != "/" else os.path.join(DIST, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def doc(head, body, extra_css=""):
    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<link rel='preconnect' href='https://fonts.googleapis.com'><link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap' rel='stylesheet'>"
            f"<link rel='icon' href='/favicon.svg' type='image/svg+xml'>\n{head}\n"
            f"{'<style>'+extra_css+'</style>' if extra_css else ''}</head><body>\n{body}\n</body></html>")


def fix_text(s):
    s = s.replace("customer_market_city", "Jacksonville").replace("customer-market_city", "Jacksonville")
    s = s.replace("market_city_", "Jacksonville").replace("market_city", "Jacksonville")
    s = s.replace("customer_marekt_state", "Florida").replace("customer-market_state", "Florida").replace("market_state", "Florida")
    for p in OLD_PHONES:
        s = re.sub(p, B.PHONE, s)
    s = s.replace("904) " + B.PHONE[6:], B.PHONE)  # stray "904) " prefixes from Carrot
    s = s.replace("(" + B.PHONE, B.PHONE).replace(B.PHONE + ")", B.PHONE)
    s = s.replace("https://content.carrot.com/", "/contact-us/").replace("http://content.carrot.com/", "/contact-us/")
    s = s.replace("https://www.jaxcashbuyers.com/", "/").replace("http://www.jaxcashbuyers.com/", "/")
    return s


def img_local(url, imgmap):
    return imgmap.get(url)


def clean_md(md, imgmap):
    md = fix_text(md)

    def repl(m):
        u = m.group(1)
        loc = img_local(u, imgmap)
        return f"\n![]({loc})\n" if loc else ""
    md = re.sub(r"!\[img\]\(([^)]+)\)", repl, md)
    md = re.sub(r"\[\s*\]\([^)]*\)", "", md)            # empty links left by removed images
    md = re.sub(r"\*\*\s*\*\*", "", md)
    md = re.sub(r"^#+\s*$", "", md, flags=re.M)          # empty headings
    md = re.sub(r"^\s*!\s*$", "", md, flags=re.M)        # stray "!" left by removed images
    md = re.sub(r"Buyers\s+([,.])", r"Buyers\1", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def strip_dup_h1(md, title):
    lines = md.split("\n")
    for i, l in enumerate(lines[:6]):
        if l.startswith("# "):
            del lines[i]
            break
    return "\n".join(lines)


def slug_clean(u):
    """Carrot placeholder slugs get a clean URL; the old one redirects."""
    nu = (u.replace("customer-market_city-", "jacksonville-").replace("market_city", "jacksonville")
          .replace("customer_marekt_state", "florida").replace("customer-market_state", "florida"))
    return nu


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    # images
    imgmap = {}
    imgdir = os.path.join(ROOT, "img")
    if os.path.exists(os.path.join(imgdir, "map.json")):
        imgmap = json.load(open(os.path.join(imgdir, "map.json")))
        shutil.copytree(imgdir, os.path.join(DIST, "img"), ignore=shutil.ignore_patterns("map.json"))

    sitemap = []
    today = datetime.date.today().isoformat()

    # core pages
    for slug, (title, desc, body, schema, robots) in B.PAGES.items():
        head, body_html = B.shell(slug, title, desc, body, schema, robots)
        write(slug, doc(head, body_html.replace("{{FORM_EMBED}}", FORM_EMBED)))
        if robots.startswith("index"):
            sitemap.append((SITE + slug, today, "1.0" if slug == "/" else "0.8"))

    # blog posts
    posts = json.load(open(os.path.join(ROOT, "raw", "blog.json")))
    newdir = os.path.join(ROOT, "content", "posts")
    if os.path.isdir(newdir):
        for fn in sorted(os.listdir(newdir)):
            if not fn.endswith(".md"):
                continue
            raw = open(os.path.join(newdir, fn)).read()
            fm, body = raw.split("\n---\n", 1) if raw.startswith("---") else ("", raw)
            meta = dict(l.split(":", 1) for l in fm.strip("-\n").split("\n") if ":" in l)
            meta = {k.strip(): v.strip().strip('"') for k, v in meta.items()}
            if meta.get("draft", "false") == "true":
                continue
            posts.append({"u": f"/blog/{fn[:-3]}/", "t": meta["title"], "h": meta["title"], "d": meta.get("description", ""),
                          "dt": meta["date"] + "T09:00+00:00", "i": meta.get("image", ""), "m": body})
    posts.sort(key=lambda p: p["dt"], reverse=True)
    seen_titles = {}
    built = []
    for p in posts:
        old = p["u"]
        new = slug_clean(old)
        title = fix_text(html.unescape(p["h"] or p["t"].split("|")[0])).strip()
        seo_title = fix_text(html.unescape(p["t"])).replace(" | Jax Cash Buyers", "").strip()
        if len(seo_title) > 52:
            seo_title = seo_title[:52].rsplit(" ", 1)[0]
        seo_title += " | Jax Cash Buyers"
        desc = fix_text(html.unescape(p["d"])).strip()
        body_md = strip_dup_h1(clean_md(p["m"], imgmap), title)
        if len(desc) < 50:
            txt = re.sub(r"[#*\[\]()!_>`-]", "", body_md)
            desc = re.sub(r"\s+", " ", txt)[:150].rsplit(" ", 1)[0] + "…"
        desc = desc[:158]
        date = p["dt"][:10]
        cover = imgmap.get(p["i"]) if p.get("i") else None
        content_html = markdown.markdown(body_md, extensions=["extra", "sane_lists"])
        # duplicate-title posts (Carrot's "-2" copies) point canonical at the first copy
        key = title.lower()
        canonical_slug = seen_titles.get(key, new)
        seen_titles.setdefault(key, new)
        robots = "index,follow" if canonical_slug == new else "noindex,follow"
        art = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": title[:110],
               "datePublished": p["dt"], "dateModified": p["dt"], "author": {"@type": "Organization", "name": "Jax Cash Buyers"},
               "publisher": {"@id": SITE + "/#business"}, "mainEntityOfPage": SITE + new, "description": desc}
        if cover:
            art["image"] = SITE + cover
        body = (f'<article class="post"><h1>{html.escape(title)}</h1>'
                f'<div class="meta">{datetime.date.fromisoformat(date).strftime("%B %-d, %Y")} · Jax Cash Buyers</div>'
                f'{content_html}'
                f'<div class="postcta"><h2 style="margin-top:0">Need to sell your house fast?</h2>'
                f'<p>Get a fair, as-is cash offer in 24 hours. No repairs, no fees, close on your date.</p>'
                f'<a class="call" href="/get-a-cash-offer-today/" style="display:inline-block">Get My Cash Offer</a> '
                f'&nbsp; or call <a href="tel:{B.TEL}"><b>{B.PHONE}</b></a></div></article>')
        head, body_html = B.shell(new, seo_title, desc, body, [art], robots)
        if canonical_slug != new:
            head = head.replace(f'<link rel="canonical" href="{SITE+new}">', f'<link rel="canonical" href="{SITE+canonical_slug}">')
        write(new, doc(head, body_html, BLOG_CSS))
        if old != new:
            REDIRECTS[old] = new
        if robots.startswith("index"):
            sitemap.append((SITE + new, date, "0.6"))
            built.append({"slug": new, "title": title, "desc": desc, "date": date, "cover": cover})

    # blog index, paginated
    per = 12
    pages = [built[i:i + per] for i in range(0, len(built), per)]
    for n, chunk in enumerate(pages, 1):
        slug = "/blog/" if n == 1 else f"/blog/page/{n}/"
        cards = "".join(
            f'<div class="pcard">{f"<img src=\"{c["cover"]}\" alt=\"\" loading=\"lazy\">" if c["cover"] else ""}'
            f'<div class="in"><h3><a href="{c["slug"]}">{html.escape(c["title"])}</a></h3>'
            f'<p>{datetime.date.fromisoformat(c["date"]).strftime("%b %-d, %Y")}</p></div></div>' for c in chunk)
        nav = "".join((f'<span>{i}</span>' if i == n else f'<a href="{"/blog/" if i == 1 else f"/blog/page/{i}/"}">{i}</a>')
                      for i in range(1, len(pages) + 1))
        body = (f'<section class="hero"><div class="wrap" style="display:block"><h1>Home Seller Tips & Guides</h1>'
                f'<p class="lead">Straight talk on selling a house in Jacksonville: foreclosure, probate, inherited homes, repairs, tenants and more.</p></div></section>'
                f'<section><div class="wrap"><div class="plist">{cards}</div><div class="pager">{nav}</div></div></section>' + B.cta())
        t = "Blog | Home Selling Tips for Jacksonville | Jax Cash Buyers" if n == 1 else f"Blog Page {n} | Jax Cash Buyers"
        head, body_html = B.shell(slug, t[:65], "Guides and tips for Jacksonville homeowners on selling fast, foreclosure, probate, inherited houses, repairs and more.", body)
        write(slug, doc(head, body_html, BLOG_CSS))
        sitemap.append((SITE + slug, today, "0.5"))

    # redirect stubs (GitHub Pages has no server redirects; meta refresh + canonical is treated as a redirect by Google)
    for old, new in REDIRECTS.items():
        write(old, f"<!doctype html><html><head><meta charset='utf-8'><title>Moved</title>"
                   f"<link rel='canonical' href='{SITE+new}'><meta name='robots' content='noindex'>"
                   f"<meta http-equiv='refresh' content='0; url={new}'><script>location.replace('{new}')</script></head>"
                   f"<body><a href='{new}'>Continue</a></body></html>")

    # 404
    head, body_html = B.shell("/404.html", "Page Not Found | Jax Cash Buyers", "This page moved. Get a fair cash offer for your Jacksonville house.",
                              '<section class="hero"><div class="wrap" style="display:block"><h1>That page moved</h1><p class="lead">Let\'s get you where you were going.</p>'
                              '<a class="call" href="/">Go to the homepage</a></div></section>' + B.cta(), robots="noindex,follow")
    with open(os.path.join(DIST, "404.html"), "w") as f:
        f.write(doc(head, body_html.replace("{{FORM_EMBED}}", FORM_EMBED)))

    # sitemap / robots / CNAME / favicon / nojekyll
    with open(os.path.join(DIST, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for loc, lm, pr in sitemap:
            f.write(f"<url><loc>{loc}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority></url>\n")
        f.write("</urlset>\n")
    with open(os.path.join(DIST, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    with open(os.path.join(DIST, "CNAME"), "w") as f:
        f.write("www.jaxcashbuyers.com\n")
    open(os.path.join(DIST, ".nojekyll"), "w").close()
    with open(os.path.join(DIST, "favicon.svg"), "w") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0f2a47"/>'
                '<path d="M12 34 32 16l20 18v16H38V38H26v12H12z" fill="#7fd6a1"/></svg>')
    print(f"core {len(B.PAGES)} · posts indexed {len(built)} of {len(posts)} · blog index pages {len(pages)} · redirects {len(REDIRECTS)} · sitemap {len(sitemap)}")


if __name__ == "__main__":
    main()
