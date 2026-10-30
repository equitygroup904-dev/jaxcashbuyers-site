# Slack commands — how to use them

Tag Claude in Slack with one of these commands plus the info it needs. Each command runs the same way every time, in the format below.

| Command | What it does | How to use it | Standing defaults |
|---|---|---|---|
| `#LandARV` | Full spec-build analysis for a vacant lot — pulls sold comps + finished ARV, land sales / per-lot basis, and the max land price (MAO) you can pay and still hit your profit target. | Post `#LandARV` with a parcel link or address (e.g. `#LandARV 223 Herbert Douglas Dr` or a `search.ncpafl.com` parcel link). Only add build size, $/sqft, or margin if you want to override a default. | Build size 1,630 sqft · Build cost $175/sqft · Soft costs $25K · Carry/financing $35K · Selling costs $40K · Target profit 15% |
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
