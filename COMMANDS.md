# Slack commands — how to use them

Tag Claude in Slack with one of these commands plus the info it needs. Each command runs the same way every time, in the format below.

| Command | What it does | How to use it | Standing defaults |
|---|---|---|---|
| `#LandARV` | Full spec-build analysis for a vacant lot — pulls sold comps + finished ARV, land sales / per-lot basis, and the max land price (MAO) you can pay and still hit your profit target. | Post `#LandARV` with a parcel link or address (e.g. `#LandARV 223 Herbert Douglas Dr` or a `search.ncpafl.com` parcel link). Only add build size, $/sqft, or margin if you want to override a default. | Build size 1,630 sqft · Build cost $175/sqft · Soft costs $25K · Carry/financing $35K · Selling costs $40K · Target profit 15% |
| `CREATE PSA` | Sends the seller a Purchase and Sale Agreement through GHL (pre-signed by James, no review step). | Post in `#acquisitions` starting with `CREATE PSA` and the fields in the template below. Checked hourly, Mon–Sat 8 AM–7 PM ET. | Title company: Patriot or Duane · James CC'd |
| `RESEND PSA` | Re-sends a PSA for the same address, with any changed terms (pulls back the old copy first). | Reply `RESEND PSA` in the original `CREATE PSA` thread, listing any fields that change. | Without it, the same address won't re-send within 3 days · Won't resend once the seller has signed |
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

## `CREATE PSA` — send a Purchase and Sale Agreement to the seller through GHL

Post in `#acquisitions`, starting with `CREATE PSA`:

```
CREATE PSA
Seller Name:
Seller Email:            (one per seller if 2+ sellers)
Street Address:
City/State/Zip:
Legal Description:
EMD:
Cash to seller at closing:
Total Purchase Price:
Closing Date:
Title Company: Patriot or Duane
Inspection Period: (days)
```

**Rules**

- EMD + Cash at closing must equal Total Purchase Price.
- Title Company is named in Clause 1 (EMD) and 3(a) (Closing).
- LLC/trust: "<signer> on behalf of <entity>".

**What happens**

- Checked hourly, Mon–Sat 8 AM–7 PM ET.
- Missing or mismatched info: you get a reply listing what's needed; answer in that thread.
- Sent: `CONTRACT SENT` post in `#acquisitions` + "PSA SENT" in your thread. James is CC'd. Confirm receipt with the seller.

## `RESEND PSA` — send a corrected or new copy

Reply `RESEND PSA` in the original `CREATE PSA` thread. If something on the contract changes, list only the changed fields in the same reply, for example:

```
RESEND PSA
Total Purchase Price: 95,000
Cash to seller at closing: 94,000
```

- Anything you don't list stays the same. EMD + Cash at closing must still equal Total Purchase Price.
- The old copy is pulled back first, so the seller can only sign the new one (named "rev 2", "rev 3", …).
- If the seller already signed, it won't resend. Changes then need an addendum.
- Checked on the same hourly schedule as `CREATE PSA`.

## `#CONTRACT` — retired

> Replaced by `CREATE PSA` (Nov 2026). Contracts are pre-signed by James, so there is no review step. Use `CREATE PSA` to send a contract. `#CONTRACTSENT` still works for moving the deal stage when a contract was sent by hand in GHL.
