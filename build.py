#!/usr/bin/env python3
"""Builds the new jaxcashbuyers.com pages (same URLs as Carrot) as standalone HTML.
Each page = <head> SEO block (title, meta, canonical, schema) + body sections.
In GHL: page settings get title/meta; body goes in a Custom Code element.
{{FORM_EMBED}} is swapped for the GHL lead form embed once the form exists."""
import json, os, html

PHONE = "(904) 750-3565"
TEL = "+19047503565"
EMAIL = "sales@jaxcashbuyers.com"
ADDR = {"street": "4600 Touchton Rd E, Suite 1150", "city": "Jacksonville", "zip": "32246"}
SITE = "https://www.jaxcashbuyers.com"
OUT = os.path.join(os.path.dirname(__file__), "pages")

AREAS = ["Jacksonville", "Jacksonville Beach", "Atlantic Beach", "Neptune Beach", "Ponte Vedra Beach",
         "St. Augustine", "St. Augustine Beach", "Orange Park", "Green Cove Springs", "Middleburg",
         "Fleming Island", "Fernandina Beach", "Yulee"]

BUSINESS_SCHEMA = {
    "@context": "https://schema.org", "@type": "LocalBusiness", "@id": SITE + "/#business",
    "name": "Jax Cash Buyers", "url": SITE + "/", "telephone": TEL, "email": EMAIL,
    "image": SITE + "/img/og-jax-cash-buyers.jpg",
    "priceRange": "$$",
    "address": {"@type": "PostalAddress", "streetAddress": ADDR["street"], "addressLocality": ADDR["city"],
                "addressRegion": "FL", "postalCode": ADDR["zip"], "addressCountry": "US"},
    "areaServed": [{"@type": "City", "name": a + ", FL"} for a in AREAS],
    "foundingDate": "2007",
    "sameAs": ["https://www.facebook.com/JaxCashBuyers/", "https://www.instagram.com/jaxcashbuyers/",
               "https://www.linkedin.com/company/american-equity-group-llc/", "https://www.twitter.com/JaxCashBuyers/"],
}

CSS = """
:root{--navy:#0f2a47;--green:#1f8a4c;--green-d:#176d3b;--ink:#1d2733;--mute:#5b6775;--line:#e3e8ee;--bg:#f6f8fa}
*{box-sizing:border-box}body{margin:0;font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);line-height:1.6;background:#fff}
a{color:var(--green-d)}.wrap{max-width:1120px;margin:0 auto;padding:0 16px}
.top{background:var(--navy);color:#fff}.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 16px;flex-wrap:wrap}
.logo{color:#fff;text-decoration:none;font-weight:800;font-size:20px;letter-spacing:.3px}.logo span{color:#7fd6a1}
.nav{display:flex;gap:18px;flex-wrap:wrap}.nav a{color:#dbe6f2;text-decoration:none;font-size:15px}.nav a:hover{color:#fff}
.call{background:var(--green);color:#fff;text-decoration:none;font-weight:700;padding:10px 16px;border-radius:8px;white-space:nowrap}
.hero{background:linear-gradient(135deg,#0f2a47 0%,#173d66 100%);color:#fff;padding:48px 0}
.hero .wrap{display:grid;grid-template-columns:1.15fr .85fr;gap:36px;align-items:start}
.hero h1{font-size:40px;line-height:1.15;margin:0 0 14px}.hero p.lead{font-size:19px;color:#dbe6f2;margin:0 0 18px}
.checks{list-style:none;padding:0;margin:0 0 20px}.checks li{padding-left:28px;position:relative;margin:6px 0}
.checks li:before{content:"✓";position:absolute;left:0;color:#7fd6a1;font-weight:800}
.card{background:#fff;color:var(--ink);border-radius:12px;padding:22px;box-shadow:0 10px 30px rgba(0,0,0,.18)}
.card h2{margin:0 0 6px;font-size:22px}.card .sub{color:var(--mute);margin:0 0 12px;font-size:15px}
section{padding:52px 0}section.alt{background:var(--bg)}h2{font-size:30px;line-height:1.2;margin:0 0 14px}h3{font-size:20px;margin:24px 0 8px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.grid2{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.box{background:#fff;border:1px solid var(--line);border-radius:12px;padding:20px}.box h3{margin-top:0}
.step{font-weight:800;color:var(--green);font-size:14px;letter-spacing:1px;text-transform:uppercase}
table.cmp{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden}
table.cmp th,table.cmp td{padding:12px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
table.cmp th{background:var(--navy);color:#fff}table.cmp td:last-child{font-weight:700;color:var(--green-d)}
.quote{background:#fff;border-left:4px solid var(--green);padding:16px 18px;border-radius:8px}.quote b{display:block;margin-top:8px;color:var(--mute);font-weight:600}
.cta{background:var(--green);color:#fff;text-align:center;padding:44px 0}.cta h2{color:#fff}.cta a.btn{display:inline-block;background:#fff;color:var(--green-d);font-weight:800;padding:14px 22px;border-radius:10px;text-decoration:none;margin:6px}
.areas{display:flex;flex-wrap:wrap;gap:10px;padding:0;list-style:none}.areas a{display:block;background:#fff;border:1px solid var(--line);padding:8px 12px;border-radius:999px;text-decoration:none;color:var(--ink)}
details{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:10px 0}summary{font-weight:700;cursor:pointer}
footer{background:#0b1f35;color:#b9c6d4;padding:36px 0;font-size:15px}footer a{color:#dbe6f2}footer .cols{display:grid;grid-template-columns:2fr 1fr 1fr;gap:24px}
.formslot{min-height:420px}.legal{max-width:820px}
.stickycall{display:none}
@media(max-width:860px){.hero .wrap,.grid3,.grid2,footer .cols{grid-template-columns:1fr}.hero h1{font-size:31px}h2{font-size:25px}.nav{display:none}
 .stickycall{display:block;position:fixed;left:0;right:0;bottom:0;background:var(--green);color:#fff;text-align:center;font-weight:800;padding:14px;text-decoration:none;z-index:50}body{padding-bottom:52px}}
"""

NAV = [("/how-we-buy-houses/", "How It Works"), ("/compare/", "Compare"), ("/testimonials/", "Reviews"),
       ("/faq/", "FAQ"), ("/our-company/", "About"), ("/blog/", "Blog"), ("/contact-us/", "Contact")]

CITY_PAGES = {
    "atlantic-beach": ("Atlantic Beach", "Duval", ["Neptune Beach", "Mayport", "Jacksonville Beach"]),
    "fernandina-beach": ("Fernandina Beach", "Nassau", ["Amelia Island", "Yulee", "O'Neil"]),
    "green-cove-springs": ("Green Cove Springs", "Clay", ["Fleming Island", "Middleburg", "Penney Farms"]),
    "jacksonville-beach": ("Jacksonville Beach", "Duval", ["Neptune Beach", "Ponte Vedra Beach", "Atlantic Beach"]),
    "neptune-beach": ("Neptune Beach", "Duval", ["Atlantic Beach", "Jacksonville Beach", "Mayport"]),
    "orange-park": ("Orange Park", "Clay", ["Fleming Island", "Oakleaf", "Middleburg"]),
    "ponte-vedra-beach": ("Ponte Vedra Beach", "St. Johns", ["Nocatee", "Jacksonville Beach", "Palm Valley"]),
    "saint-augustine": ("St. Augustine", "St. Johns", ["St. Augustine Beach", "World Golf Village", "Hastings"]),
    "saint-augustine-beach": ("St. Augustine Beach", "St. Johns", ["Anastasia Island", "Butler Beach", "St. Augustine"]),
    "yulee": ("Yulee", "Nassau", ["Fernandina Beach", "Callahan", "Hilliard"]),
}


def esc(s):
    return html.escape(s, quote=True)


def form_card(title="Get Your Fair Cash Offer", sub="Tell us about the house. We'll call within 24 hours. No obligation."):
    return f"""<div class="card" id="offer"><h2>{title}</h2><p class="sub">{sub}</p>
<div class="formslot">{{{{FORM_EMBED}}}}</div>
<p class="sub" style="margin-top:10px">Prefer to talk? Call <a href="tel:{TEL}"><b>{PHONE}</b></a></p></div>"""


def hero(h1, lead, bullets, form=True):
    li = "".join(f"<li>{b}</li>" for b in bullets)
    right = form_card() if form else ""
    return f"""<section class="hero"><div class="wrap"><div><h1>{h1}</h1><p class="lead">{lead}</p>
<ul class="checks">{li}</ul><a class="call" href="tel:{TEL}">Call {PHONE}</a></div>{right}</div></section>"""


def cta(text="Get a fair cash offer on your house this week."):
    return f"""<section class="cta"><div class="wrap"><h2>{text}</h2><p>No repairs. No commissions. You pick the closing date.</p>
<a class="btn" href="/get-a-cash-offer-today/">Get My Cash Offer</a><a class="btn" href="tel:{TEL}">Call {PHONE}</a></div></section>"""


def steps():
    return """<section><div class="wrap"><h2>How it works</h2><div class="grid3">
<div class="box"><div class="step">Step 1</div><h3>Tell us about the house</h3><p>Fill out the short form or call us. It takes about two minutes.</p></div>
<div class="box"><div class="step">Step 2</div><h3>Get a fair cash offer</h3><p>We look at the house, the repairs and recent sales nearby, then give you a written all-cash offer, usually within 24 hours.</p></div>
<div class="box"><div class="step">Step 3</div><h3>Close on your date</h3><p>We close at a local title company. Close in as little as 7 days, or whenever works for you.</p></div>
</div><p style="margin-top:18px"><a href="/how-we-buy-houses/">See our full process &rarr;</a></p></div></section>"""


def situations():
    return """<section class="alt"><div class="wrap"><h2>We buy houses in any situation</h2><div class="grid3">
<div class="box"><h3><a href="/avoiding-foreclosure/">Facing foreclosure</a></h3><p>Behind on payments or got a notice? Selling fast can protect your credit and stop the clock.</p></div>
<div class="box"><h3><a href="/selling-inherited-home/">Inherited a house</a></h3><p>Out of state, full of belongings, or not worth fixing? We buy it as-is.</p></div>
<div class="box"><h3><a href="/selling-house-during-probate/">Probate property</a></h3><p>We work with personal representatives and probate attorneys every month.</p></div>
<div class="box"><h3><a href="/selling-home-during-divorce/">Divorce</a></h3><p>A quick, clean sale so both sides can move on.</p></div>
<div class="box"><h3>Bad tenants or vacant</h3><p>Tired of being a landlord? We buy rentals with tenants in place.</p></div>
<div class="box"><h3>Major repairs</h3><p>Roof, foundation, fire damage, code violations. Leave it to us.</p></div>
</div></div></section>"""


def testimonials(n=4):
    q = [
        ("James walked us through the entire process and made it easy. We closed within 5 business days and were extremely satisfied.", "Tony Stacey"),
        ("Our house sat with two different realtors for over 13 months. We were tired of paying two mortgages. My husband called James and we closed in less than 2 weeks.", "Alexis Heath"),
        ("They made me a fair offer when others wanted to pay less than 50 cents on the dollar. Closing took only 4 days and they did exactly what they promised.", "Kevin M."),
        ("I was moving 6 hours away for a job and needed to close fast. James explained everything, made a reasonable offer and closed in less than a week.", "Hoyt Osborn"),
        ("Very honest and professional. He bought my property on the date I picked.", "Rodrick E."),
        ("They were thorough through the whole process and made it as smooth as possible. Dependable, honest and trustworthy.", "Renee Shavers"),
        ("Everything you said would happen happened exactly the way you said it would.", "Molly Lewis"),
        ("Fast and simple. They handled all the paperwork. For me, they're the number one cash buyer in St. Augustine.", "Ashley Q."),
        ("Honest and transparent. I highly recommend James and his team.", "Wagner Roberts"),
        ("The whole experience was a pleasure and barely touched my busy schedule. Great communication while I was out of town.", "Walter Hinson"),
    ][:n]
    cells = "".join(f'<div class="quote">{t}<b>— {who}</b></div>' for t, who in q)
    return f'<section><div class="wrap"><h2>What sellers say</h2><div class="grid2">{cells}</div><p style="margin-top:16px"><a href="/testimonials/">Read more reviews &rarr;</a></p></div></section>'


def areas_block():
    links = [("Jacksonville", "/sell-your-house-fast-jacksonville/")] + [
        (v[0], f"/sell-my-house-fast-{k}/") for k, v in CITY_PAGES.items()]
    li = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in links)
    return f'<section class="alt"><div class="wrap"><h2>Where we buy houses</h2><p>We buy in Duval, St. Johns, Clay and Nassau counties.</p><ul class="areas">{li}</ul></div></section>'


def compare_table():
    rows = [("Commissions / fees", "About 5–6% paid by you", "None"),
            ("Closing costs", "Often 1–2% paid by you", "We pay them"),
            ("Repairs", "Negotiated after inspection", "None. We buy as-is"),
            ("Inspection & financing contingencies", "Yes. Deals can fall through", "No bank financing needed"),
            ("Appraisal", "Usually required", "Not needed"),
            ("Showings", "Many", "One visit"),
            ("Time to close", "30–60+ days after an accepted offer", "As little as 7 days, or your date")]
    tr = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
    return f'<table class="cmp"><tr><th></th><th>Listing with an agent</th><th>Selling to Jax Cash Buyers</th></tr>{tr}</table>'


def shell(slug, title, desc, body, extra_schema=None, robots="index,follow"):
    url = SITE + slug
    schemas = [BUSINESS_SCHEMA] + (extra_schema or [])
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s)}</script>' for s in schemas)
    nav = "".join(f'<a href="{u}">{t}</a>' for u, t in NAV)
    head = f"""<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta property="og:site_name" content="Jax Cash Buyers">
<meta property="og:image" content="{BUSINESS_SCHEMA['image']}">
<meta name="google-site-verification" content="DkeoZj04wAXq-HNiT0Lk4BTZlPpk8qzqZa5IVGTnujg">
<meta name="msvalidate.01" content="3C94BA8566B5E48C0E3BF4FB275CA0AA">
{ld}"""
    body_html = f"""<style>{CSS}</style>
<header class="top"><div class="wrap"><a class="logo" href="/">Jax <span>Cash</span> Buyers</a><nav class="nav">{nav}</nav>
<a class="call" href="tel:{TEL}">{PHONE}</a></div></header>
{body}
<footer><div class="wrap cols"><div><b style="color:#fff">Jax Cash Buyers</b><br>{ADDR['street']}<br>{ADDR['city']}, FL {ADDR['zip']}<br>
<a href="tel:{TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a><p>Local, veteran-owned home buyers helping North Florida homeowners since 2007.</p></div>
<div><b style="color:#fff">Sell your house</b><br><a href="/get-a-cash-offer-today/">Get a cash offer</a><br><a href="/how-we-buy-houses/">How it works</a><br><a href="/avoiding-foreclosure/">Foreclosure</a><br><a href="/selling-inherited-home/">Inherited house</a><br><a href="/selling-house-during-probate/">Probate</a><br><a href="/selling-home-during-divorce/">Divorce</a></div>
<div><b style="color:#fff">Company</b><br><a href="/our-company/">About</a><br><a href="/testimonials/">Reviews</a><br><a href="/faq/">FAQ</a><br><a href="/blog/">Blog</a><br><a href="/contact-us/">Contact</a><br><a href="/privacy-policy/">Privacy</a> · <a href="/terms-and-conditions/">Terms</a></div></div>
<div class="wrap" style="margin-top:18px;font-size:13px">© 2026 Jax Cash Buyers. We are home buyers, not real estate agents.</div></footer>
<a class="stickycall" href="tel:{TEL}">Call {PHONE}</a>"""
    return head, body_html


PAGES = {}


def page(slug, title, desc, body, schema=None, robots="index,follow"):
    assert len(title) <= 65, (slug, len(title))
    assert len(desc) <= 160, (slug, len(desc))
    PAGES[slug] = (title, desc, body, schema, robots)


# ---------- HOME ----------
page("/", "Sell My House Fast Jacksonville FL | Cash Offer in 24 Hrs",
     "Sell your Jacksonville house fast for cash. Fair offer in 24 hours, no repairs, no commissions, close in as little as 7 days. Call (904) 750-3565.",
     hero("Sell Your House Fast in Jacksonville for Cash",
          "Get a fair, as-is cash offer in 24 hours. Skip the agents, repairs and months of waiting.",
          ["No repairs or cleaning", "No commissions or fees. We pay closing costs", "Close in as little as 7 days, or on your date", "Local and veteran-owned since 2007"])
     + steps()
     + """<section><div class="wrap grid2"><div><h2>Local Jacksonville home buyers you can trust</h2>
<p>Jax Cash Buyers is a local real estate company owned by James Stallworth, a Navy veteran. Since 2007 we've bought houses all over North Florida, from the Beaches to Middleburg and from Yulee to St. Augustine, and we've been part of more than 475 transactions.</p>
<p>We're not agents and we don't list your house. We buy it ourselves, with our own cash, as-is. That means no showings, no repair requests, no waiting on a buyer's loan and no commission coming out of your check.</p>
<p>Behind on payments, inherited a house, dealing with tenants, divorce, code violations or a house that needs more work than it's worth? We've seen it all, and we can usually make an offer on any house in any condition.</p></div>
<div><h2>What you get</h2><ul class="checks" style="color:var(--ink)"><li>A written cash offer, usually within 24 hours</li><li>No obligation. Take it or leave it</li><li>A closing date you choose</li><li>A local, neutral title company handles closing</li><li>Take what you want and leave the rest behind</li></ul>
<p><a class="call" href="/get-a-cash-offer-today/" style="display:inline-block">Get My Cash Offer</a></p></div></div></section>"""
     + situations() + testimonials() + areas_block() + cta())

# ---------- CASH OFFER ----------
page("/get-a-cash-offer-today/", "Get a Cash Offer for Your House | Jacksonville & St. Augustine",
     "Get a free, no-obligation cash offer for your Jacksonville or St. Augustine house. Any condition. Close on your timeline. Call (904) 750-3565.",
     hero("Get Your Fair Cash Offer Today",
          "Fill out the form and we'll call you within 24 hours to go over your house and your options.",
          ["Any condition, any situation", "No fees, no commissions", "You choose the closing date", "Zero obligation"])
     + """<section><div class="wrap"><h2>What happens after you submit</h2><div class="grid3">
<div class="box"><h3>We call you</h3><p>A quick call to learn about the house and what you need: timing, condition, and any loans or liens.</p></div>
<div class="box"><h3>We see the house</h3><p>One short visit. No cleaning or staging needed.</p></div>
<div class="box"><h3>You get a written offer</h3><p>A clear all-cash number. If it works for you, we close at a local title company on your date.</p></div></div></div></section>"""
     + testimonials(2) + cta("Questions first? Call us anytime."))

# ---------- SELL FAST JAX ----------
page("/sell-your-house-fast-jacksonville/", "Sell Your House Fast Jacksonville | We Buy Houses As-Is",
     "Need to sell your house fast in Jacksonville? We buy as-is for cash. No repairs, no fees, close in as little as 7 days. Call (904) 750-3565.",
     hero("We Buy Houses in Jacksonville As-Is, for Cash",
          "Find out in 24 hours what we can pay for your Jacksonville house. No repairs, no agents, no waiting.",
          ["Behind on payments or facing foreclosure", "Inherited or vacant house", "Tenants you can't get out", "Repairs you can't afford"])
     + """<section><div class="wrap"><h2>Selling in Jacksonville the easy way</h2>
<p>Listing a house in Jacksonville can mean months of showings, inspection repairs, appraisal problems and buyers whose loans fall through. All the while you keep paying the mortgage, taxes, insurance and utilities.</p>
<p>When you sell to Jax Cash Buyers, we buy the house ourselves with cash. We don't need a bank, an appraisal or a list of repairs. You get one fair offer, one visit, and a closing date that fits your life.</p>
<h3>Why Jacksonville homeowners sell to us</h3>
<ul><li><b>As-is:</b> roof leaks, old HVAC, fire damage, junk left behind, all fine.</li><li><b>No fees:</b> no commission and we pay normal closing costs.</li><li><b>Fast or flexible:</b> close in as little as 7 days, or give yourself a few months.</li><li><b>Local:</b> we're based on Touchton Road and buy houses every week across Duval County.</li></ul>
<p>Not sure if selling to us beats listing? <a href="/compare/">See the side-by-side comparison</a>.</p></div></section>"""
     + steps() + situations() + testimonials(2) + cta())

# ---------- WE BUY HOUSES JAX ----------
page("/we-buy-houses-jacksonville-florida/", "We Buy Houses Jacksonville Florida | Jax Cash Buyers",
     "We buy houses in Jacksonville, Florida for cash, in any condition. Fair offer in 24 hours and no fees. Call Jax Cash Buyers at (904) 750-3565.",
     hero("We Buy Houses in Jacksonville, Florida",
          "Cash for houses in any condition, anywhere in Duval County and the surrounding areas.",
          ["Single-family, duplexes, mobile homes and land", "Occupied, vacant or tenant-occupied", "Liens, back taxes or code violations", "No repairs and no fees"])
     + """<section><div class="wrap"><h2>Houses we buy</h2><p>We buy all kinds of property around Jacksonville: older homes that need updating, rentals with tenants, inherited houses, houses with fire or water damage, small multifamily, mobile homes and vacant lots. If you own it and want it gone, ask us.</p>
<p>Every offer is based on the location, condition, needed repairs and recent sales of similar homes nearby. We'll walk you through how we got our number.</p></div></section>"""
     + steps() + areas_block() + cta())

# ---------- HOW IT WORKS ----------
page("/how-we-buy-houses/", "How We Buy Houses in Jacksonville | Simple 3-Step Process",
     "See how Jax Cash Buyers buys houses in Jacksonville: tell us about the house, get a cash offer in 24 hours, and close on your date. No fees.",
     hero("How Our Home Buying Process Works",
          "Three simple steps from first call to cash at closing, on your schedule.",
          ["Offer usually within 24 hours", "Close in as little as 7 days", "Local title company closing", "No fees or commissions"], form=False)
     + steps()
     + """<section class="alt"><div class="wrap"><h2>The details</h2>
<h3>1. Tell us about your house</h3><p>Fill out our short form or call (904) 750-3565. We'll ask about the address, condition, your timeline and any mortgage or liens. Everything stays confidential.</p>
<h3>2. One walkthrough, then a written offer</h3><p>We schedule a short visit at a time that works for you. We look at repairs, the location and recent sales of similar homes nearby, and then give you a fair all-cash offer, usually within 24 hours. There's no pressure and no obligation.</p>
<h3>3. You pick the closing date</h3><p>If you accept, we open title with a local, neutral title company. They handle payoffs, liens and paperwork. You show up, sign, and get paid. That can be as soon as 7 days, or weeks or months out if you need time to move.</p>
<h3>What you don't have to do</h3><ul><li>No repairs, painting or cleaning</li><li>No showings or open houses</li><li>No commissions or closing costs</li><li>No waiting on a buyer's bank</li></ul></div></section>"""
     + testimonials(2) + cta())

# ---------- COMPARE ----------
page("/compare/", "Sell to an Investor vs. List With an Agent | Jacksonville FL",
     "Compare selling your Jacksonville house to a cash buyer vs. listing with an agent: fees, repairs, closing costs and time to close.",
     hero("Selling to Jax Cash Buyers vs. Listing With an Agent",
          "Listing can get a higher top-line price. Selling to us can mean less hassle, no costs and a sure close. Here's how they compare.",
          ["See the real costs side by side", "Factor in holding costs while you wait", "Pick the option that fits your goals"], form=False)
     + f"""<section><div class="wrap">{compare_table()}<p style="color:var(--mute);font-size:14px;margin-top:10px">Agent figures are typical ranges and vary by sale.</p></div></section>
<section class="alt"><div class="wrap grid2"><div><h2>Work the numbers</h2><p>We won't pay full retail. We buy as-is and take on the repairs and the risk. But when you subtract commission, closing costs, repairs, and months of mortgage, taxes, insurance and utilities while a listed house sits, the gap is often much smaller than people expect.</p></div>
<div><h2>When listing makes more sense</h2><p>If your house is updated, you have time, and you don't mind showings, listing with a good local agent may net you more. We'll tell you that honestly. If speed, certainty or condition matter more, a cash sale is usually the better fit.</p></div></div></section>"""
     + cta("See what we'd offer, then decide."))

# ---------- FAQ ----------
faqs = [
    ("Are you agents? Will you list my house?", "No. We're home buyers, not agents. We buy houses ourselves with cash, then repair and resell or rent them."),
    ("How do you decide what to offer?", "We look at the location, the condition, the repairs needed and what similar homes nearby have recently sold for. We'll walk you through how we got our number."),
    ("Do you pay fair prices?", "We buy below retail because we pay for repairs, carry the risk and close fast with cash. Many sellers find the speed, certainty and lack of costs worth it. Our offer is no-obligation, so you can compare."),
    ("Are there any fees or commissions?", "No. There are no commissions or fees, and we pay normal closing costs. The offer we agree on is what you get, minus any mortgage payoff or liens."),
    ("How fast can you close?", "In as little as 7 days once title is clear, or on whatever date works for you."),
    ("Do I need to make repairs or clean out the house?", "No. We buy as-is. Take what you want and leave the rest."),
    ("Can you buy a house with tenants, liens or back taxes?", "Yes. We buy tenant-occupied homes and can often work through liens, back taxes and code violations at closing."),
    ("Is there any obligation if I ask for an offer?", "None. You get a fair offer and decide what's right for you. No pressure."),
    ("What areas do you buy in?", "Jacksonville and the surrounding area, including Duval, St. Johns, Clay and Nassau counties."),
]
faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
faq_schema = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
page("/faq/", "FAQ | Selling Your House for Cash in Jacksonville",
     "Answers to common questions about selling your Jacksonville house for cash: offers, fees, closing time, repairs, tenants and liens.",
     hero("Frequently Asked Questions", "Straight answers about selling your house to Jax Cash Buyers.",
          ["No fees or commissions", "As-is, any condition", "You pick the closing date"], form=False)
     + f'<section><div class="wrap" style="max-width:860px">{faq_html}</div></section>' + cta(),
     schema=[faq_schema])

# ---------- TESTIMONIALS ----------
page("/testimonials/", "Reviews | What Sellers Say About Jax Cash Buyers",
     "Read reviews from Jacksonville and St. Augustine homeowners who sold their houses fast for cash to Jax Cash Buyers.",
     hero("What Our Sellers Say", "We're not happy unless you are. Here's what homeowners we've worked with have shared.",
          ["Real local sellers", "Fast, honest closings", "475+ transactions"], form=False)
     + testimonials(10)
     + '<section class="alt"><div class="wrap"><p>Sold to us? <a href="/contact-us/">Tell us about your experience.</a></p></div></section>' + cta())

# ---------- ABOUT ----------
page("/our-company/", "About Jax Cash Buyers | Local, Veteran-Owned Home Buyers",
     "Jax Cash Buyers is a local, veteran-owned Jacksonville home buying company. Since 2007 we've helped homeowners sell fast for a fair price.",
     hero("About Jax Cash Buyers", "Local, veteran-owned home buyers helping North Florida homeowners since 2007.",
          ["Owned by James Stallworth, Navy veteran", "475+ transactions", "Based in Jacksonville"], form=False)
     + """<section><div class="wrap grid2"><div><h2>Who we are</h2><p>Jax Cash Buyers buys houses directly from homeowners who need a fast, simple sale. That could be because of foreclosure, an inherited or probate property, a divorce, tired-landlord problems, or a house that needs more work than it's worth.</p>
<p>When we commit to buying your house, the whole team is accountable for doing what we said. Whether that means working with a lender, the city on code violations, or the title company, we push until the job is done and you have your money.</p></div>
<div><h2>What we stand for</h2><ul class="checks" style="color:var(--ink)"><li>We care, and we always do the right thing</li><li>Honest, open communication</li><li>A great experience from first call to closing</li><li>Accountability for every promise</li><li>Restoring and revitalizing our community</li><li>Local and veteran-owned. Go Navy!</li></ul></div></div></section>"""
     + testimonials(2) + cta())

# ---------- CONTACT ----------
page("/contact-us/", "Contact Jax Cash Buyers | (904) 750-3565",
     "Contact Jax Cash Buyers in Jacksonville. Call (904) 750-3565 or send us a message about selling your house fast for cash.",
     hero("Let's Talk", "Questions about our process, foreclosure, an inherited house, or anything else? Call or send us a message.",
          [f"Call or text {PHONE}", f"Email {EMAIL}", "We reply quickly. Calls are fastest"])
     + f"""<section><div class="wrap grid2"><div><h2>Contact info</h2><p><b>Jax Cash Buyers</b><br>{ADDR['street']}<br>{ADDR['city']}, FL {ADDR['zip']}</p>
<p>Phone: <a href="tel:{TEL}">{PHONE}</a><br>Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div><h2>Good to know</h2><p>We'll never pressure you. Ask us anything, even just to make sure we're real people.</p></div></div></section>""")

# ---------- SITUATIONS ----------
def situation(slug, title, desc, h1, lead, bullets, body):
    page(slug, title, desc, hero(h1, lead, bullets) + f'<section><div class="wrap" style="max-width:900px">{body}</div></section>'
         + steps() + testimonials(2) + cta())

situation("/avoiding-foreclosure/", "Stop Foreclosure in Jacksonville FL | Sell Before the Auction",
          "Facing foreclosure in Jacksonville? Learn your options and how a fast cash sale can protect your credit. Free, confidential help: (904) 750-3565.",
          "Facing Foreclosure in Jacksonville?", "You have more options than you think, and less time than you'd like. Let's look at them together.",
          ["Free, confidential review of your options", "We can often close before the sale date", "No fees. We pay closing costs"],
          """<h2>Your options when you're behind on payments</h2>
<p>Foreclosure can happen to anyone: a job loss, medical bills, a divorce or a rate change. What matters is acting early. In Florida, foreclosure goes through the courts, which takes time, but every month you wait means more fees and fewer options.</p>
<h3>1. Talk to your lender now</h3><p>Lenders would rather be paid than take a house. Ask about reinstatement, a repayment plan, forbearance or a loan modification.</p>
<h3>2. Get free housing counseling</h3><p>HUD-approved counselors can help for free. Be wary of anyone charging up-front fees to "save" your house.</p>
<h3>3. List the house, if you have time</h3><p>If you have equity and several months, listing may put more in your pocket.</p>
<h3>4. Sell fast for cash</h3><p>If time is short or the house needs work, we can make a cash offer and often close before the auction date. The sale pays off the loan, which can protect your credit from a completed foreclosure.</p>
<p>Every situation is different. Call us and we'll walk through it honestly, even if selling to us isn't the right answer.</p>""")

situation("/selling-inherited-home/", "Sell an Inherited House Fast in Jacksonville | As-Is Cash",
          "Inherited a house in Jacksonville? Sell it as-is for cash. No cleanout, no repairs, no fees. We work with heirs and estates. Call (904) 750-3565.",
          "Sell Your Inherited House in Jacksonville", "Skip the cleanout, repairs and months of carrying costs. We buy inherited houses as-is.",
          ["Leave the belongings behind", "Out-of-state heirs welcome", "We work with your attorney and title company"],
          """<h2>A simple way to settle an inherited house</h2>
<p>Inheriting a house often comes during a hard time, along with taxes, insurance, utilities and repairs, and sometimes several heirs to agree with. Many families don't have the time or money to fix it up and list it.</p>
<p>We buy inherited homes in any condition, full or empty. You don't need to clean out decades of belongings or fix anything. We coordinate with the estate's attorney and a local title company, and we can close quickly or wait until the estate is ready.</p>
<h3>Is probate required?</h3><p>Often, yes, before the house can be sold. See our <a href="/selling-house-during-probate/">probate page</a>. We can make an offer while probate is in progress and close when the court allows.</p>""")

situation("/selling-house-during-probate/", "Sell a House During Probate in Jacksonville FL | Cash Buyers",
          "Selling a probate house in Jacksonville? We buy probate properties as-is and work with personal representatives and attorneys. (904) 750-3565.",
          "Selling a House During Probate", "We help personal representatives sell estate property quickly and cleanly, in any condition.",
          ["Offer during probate, close when cleared", "As-is, no cleanout", "We work with your probate attorney"],
          """<h2>How a probate sale works with us</h2>
<p>In Florida, the personal representative usually needs authority from the court (Letters of Administration) before selling estate property. Some sales also need court approval. Your probate attorney will guide that part. We make it easy on the buying side.</p>
<ul><li>We can make a written offer early, so the estate knows its options.</li><li>We buy as-is, so the estate doesn't spend money on repairs or carrying costs.</li><li>We close through a local title company that handles probate sales regularly.</li></ul>
<p>We're not attorneys and don't give legal advice. Always check with the estate's lawyer.</p>""")

situation("/selling-home-during-divorce/", "Selling a House During Divorce in Jacksonville FL",
          "Need to sell your house during a divorce in Jacksonville? Get a fast, fair cash offer and a clean, simple sale so both sides can move on.",
          "Selling Your House During a Divorce", "A fast, neutral cash sale can make one of the hardest parts of a divorce simpler.",
          ["One offer, split as you agree", "No showings or repairs", "Close on a date that works for both"],
          """<h2>Why a cash sale helps</h2>
<p>Listing during a divorce means agreeing on an agent, a price, repairs, showings and every buyer's offer, sometimes for months. A direct cash sale cuts that down to one decision.</p>
<p>We give both owners the same clear written offer. If you both agree, a local title company handles closing and pays out the proceeds the way your agreement or court order says.</p>
<p>We're not attorneys. Check with your family law attorney about your situation.</p>""")

# ---------- CITY PAGES ----------
for key, (city, county, near) in CITY_PAGES.items():
    slug = f"/sell-my-house-fast-{key}/"
    page(slug, f"Sell My House Fast {city} FL | Cash Home Buyers"[:65],
         f"Sell your {city}, FL house fast for cash. Fair as-is offer in 24 hours, no fees, close in as little as 7 days. Call (904) 750-3565.",
         hero(f"Sell Your House Fast in {city}, FL",
              f"We buy houses in {city} and across {county} County for cash, in any condition.",
              ["No repairs or cleaning", "No commissions or fees", "Close in as little as 7 days", f"Local buyers serving {county} County"])
         + f"""<section><div class="wrap" style="max-width:900px"><h2>We buy houses in {city}</h2>
<p>Need to sell a house in {city} without the hassle of listing? Jax Cash Buyers buys homes in {city}, {near[0]}, {near[1]}, {near[2]} and the rest of {county} County, as-is and for cash.</p>
<p>We help homeowners who are behind on payments, have inherited a house, are going through probate or divorce, are tired of being a landlord, or own a house that needs more repairs than they want to take on. Whatever the reason, you get one fair offer and a closing date you choose.</p>
<h3>Why {city} homeowners sell to us</h3>
<ul><li><b>Speed:</b> a written offer usually within 24 hours, and close in as little as 7 days.</li>
<li><b>As-is:</b> no repairs, no cleaning, no showings.</li><li><b>No costs:</b> no commissions, and we pay normal closing costs.</li>
<li><b>Certainty:</b> no buyer financing to fall through.</li></ul>
<p>Comparing options? See <a href="/compare/">selling to us vs. listing with an agent</a>.</p></div></section>"""
         + steps() + testimonials(2) + areas_block() + cta(f"Get a fair cash offer on your {city} house."))

# ---------- BLOG INDEX (GHL blog replaces this; kept for redirects/SEO) ----------
# GHL's blog element renders /blog/ itself; no page built here.

# ---------- THANK YOU ----------
page("/thank-you/", "Thank You | Jax Cash Buyers",
     "Thanks for reaching out to Jax Cash Buyers. We'll call you within 24 hours to go over your house.",
     f"""<section class="hero"><div class="wrap" style="display:block"><h1>Thanks! Here's what happens next</h1>
<p class="lead">We got your info. Someone from our team will call you within 24 hours to get a few more details so we can make you a fair cash offer.</p>
<a class="call" href="tel:{TEL}">Call us now: {PHONE}</a></div></section>
<section><div class="wrap" style="max-width:860px"><h2>Quick answers</h2>{faq_html}</div></section>""",
     robots="noindex,follow")

# ---------- LEGAL ----------
page("/privacy-policy/", "Privacy Policy | Jax Cash Buyers",
     "Privacy policy for Jax Cash Buyers: what information we collect, how we use it, and your text message and email choices.",
     f"""<section><div class="wrap legal"><h1>Privacy Policy</h1><p><i>Last updated: October 27, 2026</i></p>
<p>Jax Cash Buyers ("we," "us") respects your privacy. This policy explains what we collect on jaxcashbuyers.com and how we use it.</p>
<h3>Information we collect</h3><p>Information you give us, such as your name, phone number, email and property address, and basic usage data like pages visited and browser type.</p>
<h3>How we use it</h3><p>To respond to you, evaluate your property, make an offer, and send updates you've agreed to receive. We do not sell your personal information.</p>
<h3>Text messages</h3><p>If you agree to receive texts, message frequency varies and message and data rates may apply. Reply STOP to opt out or HELP for help. Consent is not a condition of any purchase. Mobile numbers and SMS consent are not shared with third parties or affiliates for marketing purposes.</p>
<h3>Sharing</h3><p>We share information only with service providers who help us operate (for example our CRM, title companies and closing agents) or when required by law.</p>
<h3>Your choices</h3><p>You can ask us to update or delete your information or stop contacting you at any time: {EMAIL} or {PHONE}.</p>
<h3>Contact</h3><p>{ADDR['street']}, {ADDR['city']}, FL {ADDR['zip']}</p></div></section>""")

page("/terms-and-conditions/", "Terms and Conditions | Jax Cash Buyers",
     "Terms and conditions for using jaxcashbuyers.com and receiving communications from Jax Cash Buyers.",
     f"""<section><div class="wrap legal"><h1>Terms and Conditions</h1><p><i>Last updated: October 27, 2026</i></p>
<p>By using jaxcashbuyers.com you agree to these terms.</p>
<h3>No offer or advice</h3><p>Content on this site is general information, not legal, tax or financial advice. Any offer to buy your property is made only in a written agreement signed by both parties.</p>
<h3>We are buyers, not agents</h3><p>Jax Cash Buyers buys property directly and does not act as your real estate agent or broker.</p>
<h3>Communications</h3><p>By submitting your information you agree that we may contact you by phone, text and email about your property. Message and data rates may apply. Reply STOP to opt out of texts. Consent is not a condition of purchase.</p>
<h3>Limitation of liability</h3><p>This site is provided "as is." We are not liable for damages arising from its use.</p>
<h3>Contact</h3><p>{EMAIL} · {PHONE}</p></div></section>""")

# ---------- RESOURCES ----------
page("/resource-page/", "Home Seller Resources | Jacksonville Foreclosure & Selling Help",
     "Free resources for Jacksonville homeowners: foreclosure help, selling options, and guides to selling your house fast.",
     hero("Resources for Jacksonville Homeowners", "Helpful links and guides whether you're selling, behind on payments, or just weighing your options.",
          ["Foreclosure help", "Selling options compared", "Free, no obligation"], form=False)
     + """<section><div class="wrap" style="max-width:900px"><h2>Foreclosure help</h2>
<ul><li><a href="https://www.consumerfinance.gov/housing/" rel="noopener" target="_blank">CFPB: help for homeowners</a>, including how to find a HUD-approved housing counselor</li>
<li><a href="https://www.hud.gov/topics/avoiding_foreclosure" rel="noopener" target="_blank">HUD: avoiding foreclosure</a></li>
<li><a href="/avoiding-foreclosure/">Our guide to your foreclosure options</a></li></ul>
<h2>Selling your house</h2><ul><li><a href="/compare/">Selling to a cash buyer vs. listing with an agent</a></li><li><a href="/how-we-buy-houses/">How our process works</a></li>
<li><a href="/selling-inherited-home/">Selling an inherited house</a></li><li><a href="/selling-house-during-probate/">Selling during probate</a></li><li><a href="/blog/">Our blog</a></li></ul></div></section>""" + cta())


def main():
    os.makedirs(OUT, exist_ok=True)
    index = []
    for slug, (title, desc, body, schema, robots) in PAGES.items():
        head, body_html = shell(slug, title, desc, body, schema, robots)
        name = "home" if slug == "/" else slug.strip("/").replace("/", "_")
        with open(os.path.join(OUT, name + ".html"), "w") as f:
            f.write(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>\n{head}\n</head><body>\n{body_html}\n</body></html>")
        # GHL parts: head code + body custom code
        with open(os.path.join(OUT, name + ".ghl-body.html"), "w") as f:
            f.write(body_html)
        index.append({"slug": slug, "file": name, "title": title, "desc": desc, "robots": robots,
                      "schema": [BUSINESS_SCHEMA] + (schema or [])})
    with open(os.path.join(OUT, "index.json"), "w") as f:
        json.dump(index, f, indent=1)
    print(len(PAGES), "pages")


if __name__ == "__main__":
    main()
