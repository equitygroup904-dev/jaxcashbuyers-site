# jaxcashbuyers.com

Static site for Jax Cash Buyers, hosted on GitHub Pages from `/docs`.

- `build.py` — core pages (copy, SEO titles/meta, schema, layout)
- `build_site.py` — builds everything into `docs/`: core pages, blog posts, blog index, redirects, sitemap.xml, robots.txt
- `raw/blog.json` — the 238 posts migrated from Carrot
- `content/posts/*.md` — new posts (see `content/POSTING.md`)
- `img/` — images migrated from Carrot + share image

Rebuild: `pip install markdown && python3 build_site.py`
Lead form: GHL "Contact Form" (aaSmOX0UTKOiDY0aSTeF), so leads land in the Jacksonville Cash Home Buyers sub-account.
