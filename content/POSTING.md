# SEO blog posts — instructions for the automated writer

Two new posts per week (Tuesday and Friday), published automatically and shared to Google Business Profile and
Facebook (James approved auto-publish with no review, 10/27/2026; 2 per week + GMB/Facebook sharing, 10/29/2026).

## Pick a topic (rotate the 9 target topics)
Rotate through these in order. Look at the newest file in `content/posts/` (its `topic:` line) and use the NEXT one
(after mobile-home, start again at probate). If `content/posts/` is empty, start at probate.

| topic key | Who we're targeting | Matching page to link |
|---|---|---|
| probate | heirs / personal representatives selling a house in probate | /selling-house-during-probate/ (also /selling-inherited-home/) |
| foreclosure | behind on payments, notice of default, auction date | /avoiding-foreclosure/ |
| subject-to | owners who owe close to what the house is worth, want out of the payment | /how-we-buy-houses/ |
| divorce | couples splitting and needing to sell the house | /selling-home-during-divorce/ |
| bankruptcy | owners in or considering Chapter 7/13 who need to sell | /avoiding-foreclosure/ |
| eviction | landlords dealing with non-paying tenants / evictions | /how-we-buy-houses/ |
| tired-landlord | landlords who want out of rentals (repairs, tenants, vacancies) | /how-we-buy-houses/ |
| vacant-land | owners of vacant lots and acreage (taxes, inherited land, no plans for it) | /get-a-cash-offer-today/ |
| mobile-home | owners of mobile/manufactured homes on land or in parks | /how-we-buy-houses/ |

- Pair the topic with ONE area and never repeat a topic + area combo (check `content/posts/` and `raw/blog.json`
  titles first). Areas: Jacksonville neighborhoods (Arlington, Westside, Northside, Southside, Mandarin, Riverside,
  Springfield, Murray Hill, San Marco, Regency, Baymeadows, Oceanway), Duval County, Nassau County (Yulee, Fernandina
  Beach, Callahan, Hilliard), Clay County (Middleburg, Fleming Island, Orange Park, Green Cove Springs), St. Johns County
  (St. Augustine, Ponte Vedra, Nocatee), Baker County (Macclenny). Vacant land and mobile homes fit Nassau/Clay/Baker best.
- Aim for a search people actually type, e.g. "sell house in probate Jacksonville", "stop foreclosure Orange Park",
  "sell my house subject to Jacksonville", "sell house during divorce Duval County", "sell house in bankruptcy Florida",
  "sell rental property with tenants Jacksonville", "sell vacant land Nassau County", "sell mobile home with land Middleburg".
- Subject-to: explain it in plain words (we take over the existing mortgage payments; the loan stays in the seller's
  name; due-on-sale risk exists), say it isn't right for everyone, and tell readers to talk to an attorney.
  Bankruptcy: selling during bankruptcy usually needs the trustee's/court's approval — say so, and say we're not attorneys.

## Write it
- File: `content/posts/<url-slug>.md` (lowercase, hyphens, include the area). Front matter:
  ```
  ---
  title: How to Sell a House in Probate in Jacksonville
  description: <=155 chars, includes the keyword and a reason to click
  date: YYYY-MM-DD
  topic: probate
  image: /img/blog/<url-slug>.jpg
  ---
  ```
- 900–1,300 words. Plain, helpful, written for a stressed homeowner. H2/H3 headings, short paragraphs, one list.
- Include: the keyword in the title, first paragraph and one H2; one internal link to the matching page in the table
  (or a /sell-my-house-fast-<city>/ page) and one to /get-a-cash-offer-today/.
- Phone is always (904) 750-3565. Company name: Jax Cash Buyers. James Stallworth is the owner (local, veteran-owned).

## Cover image (every post)
`python3 tools/make_cover.py <topic> "<title>" img/blog/<url-slug>.jpg`
It makes a 1200x630 card: a photo for the topic (img/blog-bg/), the title, a green topic label, James's photo in a
circle and the phone number. Open the image and check the title is fully visible and readable before publishing.
Never use photos of sellers or anyone other than James, and never AI-generate images of real people.

## Guardrails (never break)
- No made-up statistics, prices, dates, laws or case numbers. If a fact needs a source, leave it out or say "check with your attorney/county".
- No fake testimonials or quotes. No promises of a price, a closing date, or that we buy every house.
- Legal/tax topics (probate, bankruptcy, divorce, eviction, subject-to, foreclosure): general info only, and say we're not attorneys or tax advisors.
- No copied text from other sites.

## Publish
1. `python3 build_site.py` (must print without errors). If `__pycache__/` shows as changed afterwards, `git checkout -- __pycache__`.
2. Spot-check `docs/blog/<slug>/index.html` (title, cover image, links, phone).
3. Commit "Blog post: <title>" and push to main. GitHub Pages deploys in ~1–2 minutes.
4. Share to Google Business Profile + Facebook through GHL Social Planner (location RUJDZc7TyNghXiWDMthZ only):
   - Get the connected accounts with operation `get-account`; use the `id` of the platform "google" account
     ("Jax Cash Buyers") and the platform "facebook" page. Skip any account that is missing or expired and say so.
   - One `create-post` per platform (so each keeps its own caption): type "post", status "scheduled",
     scheduleDate = now + 15 minutes (UTC ISO), media [{url: "https://www.jaxcashbuyers.com/img/blog/<slug>.jpg", type: "image/jpeg"}],
     userId = James Stallworth's GHL user id (look it up with the users operations; if it can't be found, try without it).
   - Google caption: 2–3 sentences (under 1,400 characters) summarizing the post, ending with "Read more:" + the post URL
     and "Call (904) 750-3565". gmbPostDetails {gmbEventType "STANDARD", actionType "learn_more", url: <post URL>}.
   - Facebook caption: 3–5 short sentences, a question to the reader, the post URL, "Call or text (904) 750-3565",
     and 3–5 local hashtags (e.g. #Jacksonville #JaxRealEstate #SellMyHouseFast). facebookPostDetails {type "post"}.
   - idempotencyKey "blog-<slug>-gmb" / "blog-<slug>-fb".
5. Post in Slack #operations: ":robot_face: Auto — New blog post is live: <title> https://www.jaxcashbuyers.com/blog/<slug>/ — shared to Google Business ✅/❌ and Facebook ✅/❌ (automated, not James)"
