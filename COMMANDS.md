# Slack commands — how to use them

Tag Claude in Slack with one of these commands plus the info it needs. Each command runs the same way every time, in the format below.

| Command | What it does | How to use it | Standing defaults |
|---|---|---|---|
| `#LandARV` | Full spec-build analysis for a vacant lot — pulls sold comps + finished ARV, land sales / per-lot basis, and the max land price (MAO) you can pay and still hit your profit target. | Post `#LandARV` with a parcel link or address (e.g. `#LandARV 223 Herbert Douglas Dr` or a `search.ncpafl.com` parcel link). Only add build size, $/sqft, or margin if you want to override a default. | Build size 1,630 sqft · Build cost $175/sqft · Soft costs $25K · Carry/financing $35K · Selling costs $40K · Target profit 15% |
| `#CONTRACT` | Prepares the seller's Purchase and Sale Agreement in GHL, sends James a review copy first, then e-sends it to the seller once James approves. | Copy the **#CONTRACT post template** below, fill it in, post it in `#acquisitions`, and tag Claude. James replies `send` in the thread to release it. | EMD $0 · Inspection 10 business days · Closing 30 days out (defaults pending James's OK) · Buyer: American Equity Group LLC · Closing agent: Patriot Title |
| `#NEEDJAMES` | Flags a lead for James to handle personally and routes it to acquisitions. | Fires from the offer workflow (`seller-offer-range` skill) when a deal is out of the normal box: mobile/manufactured, multifamily, commercial, $400K+, out of area, large structural repairs, uncertain land value over ~$50K, or any subject-to / creative deal. Routes to Slack `#acquisitions` and GHL stage "Creative / Subto / NeedJames". | — |

## `#LandARV` — what you get back

When you post `#LandARV` with a lot, Claude returns, in this order:

1. **Comps + finished ARV** — recent sold new-construction comps near the lot, with an ARV range.
2. **Land sales / lot basis** — what raw lots in the area or subdivision have traded for.
3. **Spec-build MAO math** — backs into the max all-in land price using your standing assumptions:

   ```
   Finished ARV
   − Build cost       (build size × $/sqft)
   − Soft costs       ($25K: permits, impact fees, utilities, design)
   − Carry / financing ($35K, 12 mo)
   − Selling costs    ($40K: ~6% commission + closing)
   − Target profit    (15% of ARV)
   = Max all-in land price
   ```

4. **Cushion** — how much room is left vs. the price you're being quoted or offering.

**Inputs Claude asks for (only if you don't give them):**

- Parcel link or address — required
- Build size in sqft — default 1,630
- Build cost $/sqft — default $175
- Target profit margin — default 15%

> These are estimates — confirm build cost with your GC and ARV with an agent BPO before committing.

## `#CONTRACT` — sending a purchase agreement

**Rule: every contract goes to James for review first. Nothing goes to a seller until James replies `send`.**

**Before you post:** the seller must be in GHL with their **full name exactly as on the deed** and a **working email**. If the email is wrong, the contract goes nowhere.

### `#CONTRACT` post template (copy, fill in, post in `#acquisitions`)

```
#CONTRACT @Claude
Address: 
Seller name (exactly as on deed): 
Seller email: 
Seller phone: 
Price: $
EMD: $0
Inspection days: 10
Closing date: 
Co-owner name + email (if any): 
Notes for James: 
```

- **Required:** Address, Seller name, Seller email, Price, Closing date.
- EMD and Inspection days are pre-filled with the defaults — change them if the deal is different.
- Write the closing date as a date (e.g. `11/24/2026`), not "30 days."
- Leave Co-owner blank if the seller is the only person on the deed.

**What happens when you post `#CONTRACT`:**

1. Claude finds the seller's contact and fills the contract fields on it: Property Address, City, Zip, County, Assessor ID (RE#), Contract Price, Contract EMD, Contract Balance at Closing (price − EMD), Contract Closing Date (written out, e.g. "November 24, 2026"), Contract Inspection Days.
2. Claude replies in the thread with the terms it filled in and anything missing.
3. Claude sends a **review copy to James** (equitygroup904@gmail.com) from the GHL template "Purchase and Sale Agreement - Template".
4. James checks it and replies `send` in the thread (or says what to change).
5. Claude e-sends the agreement to the seller from **sales@jaxcashbuyers.com**, linked to the deal, with James CC'd — and moves the deal to **Motivated Seller / Agreement Sent**.
6. The seller gets an email → reviews → signs → GHL emails the signed copy to the seller and James.

**Doing it by hand in GHL (if Claude isn't available):**

1. Open the seller's contact and fill in the contract fields listed in step 1 above.
2. Post the terms in `#acquisitions` and get James's OK.
3. On the contact, go to **Documents → New → Purchase and Sale Agreement - Template**, check the preview, and **Send**.
4. Then post `#CONTRACTSENT` so the sync moves the deal to Agreement Sent.

**Good to know:**

- The seller only signs and dates — every term fills in from GHL. If something shows blank, a field on the contact is empty.
- If a seller says they didn't get it, have them check **Spam/Junk** for an email from Jacksonville Cash Home Buyers.
- Every owner on the deed must sign. If there's a co-owner, give Claude their name and email so they're added as a second signer.
- `#CONTRACT` sends the agreement. `#CONTRACTSENT` only moves the deal stage — use it after a contract was sent by hand.
