# Weekly SEO post — instructions for the automated writer

One new post per week, published automatically (James approved auto-publish with no review, 10/27/2026).

## Pick a topic
- Seller-intent searches in our area: "sell house fast [city/neighborhood]", "sell inherited house [county]",
  "sell house with code violations Jacksonville", "sell house with tenants", "probate", "foreclosure", "divorce",
  "fire/water damage", "behind on taxes", "mobile home", "land".
- Areas: Jacksonville neighborhoods (Arlington, Westside, Northside, Southside, Mandarin, Riverside, Springfield, Murray Hill,
  San Marco, Regency, Baymeadows, Oceanway), plus Middleburg, Fleming Island, Orange Park, Green Cove Springs, St. Augustine,
  Ponte Vedra, Nocatee, Yulee, Fernandina Beach, Callahan, Hilliard, Macclenny.
- Check `content/posts/` and `raw/blog.json` titles first. Never repeat a topic + area combo.

## Write it
- File: `content/posts/<url-slug>.md` (lowercase, hyphens, include the city). Front matter:
  ```
  ---
  title: How to Sell a House With Code Violations in Jacksonville
  description: <=155 chars, includes the keyword and a reason to click
  date: YYYY-MM-DD
  ---
  ```
- 900–1,300 words. Plain, helpful, written for a stressed homeowner. H2/H3 headings, short paragraphs, one list.
- Include: the keyword in the title, first paragraph and one H2; one internal link to a matching page
  (/avoiding-foreclosure/, /selling-inherited-home/, /selling-house-during-probate/, /selling-home-during-divorce/,
  /compare/, /how-we-buy-houses/, or a /sell-my-house-fast-<city>/ page) and one to /get-a-cash-offer-today/.
- Phone is always (904) 685-8024. Company name: Jax Cash Buyers.

## Guardrails (never break)
- No made-up statistics, prices, dates, laws or case numbers. If a fact needs a source, leave it out or say "check with your attorney/county".
- No fake testimonials or quotes. No promises of a price, a closing date, or that we buy every house.
- Legal/tax topics: general info only, and say we're not attorneys or tax advisors.
- No copied text from other sites.

## Publish
1. `python3 build_site.py` (must print without errors)
2. Spot-check the new page in `docs/blog/<slug>/index.html`
3. Commit "Weekly post: <title>" and push to main. GitHub Pages deploys in ~1 minute.
4. Post in Slack #operations: ":robot_face: Auto — New blog post is live: <title> https://www.jaxcashbuyers.com/blog/<slug>/ (automated, not James)"
