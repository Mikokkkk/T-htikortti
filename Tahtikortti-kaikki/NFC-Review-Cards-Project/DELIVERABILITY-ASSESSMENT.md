# Deliverability & outreach-method assessment (T9)

Answers the question from your dictation: *"if we send these mass emails, what's the
best method, do they go straight to spam, and how many people do we actually reach?"*

Short version: **do not blast ~200 cold emails from your personal Gmail via the Python
script.** It's the fastest way to burn the address and land in spam. A ~30-minute setup
on a separate domain gets you dramatically better reach and keeps you legal. And for
this specific product, in-person + a smaller, warmer email batch will out-perform a
mass blast.

---

## 1. Is it even legal in Finland?

Mostly yes — if you target companies, not people.

- **Registered companies (Oy, Oyj):** B2B cold email is permitted **without prior
  consent** on a *legitimate-interest* basis, as long as every message has a clear
  **opt-out** and the offer is professionally relevant. A card that boosts a
  restaurant's Google visibility clearly is.
- **Sole traders (toiminimi) and private individuals:** need **prior consent** — do
  not cold-email these. Filter your list to Oy/Oyj (the `company_type` column in
  `leads-template.csv`).
- Finland's Electronic Communications Services Act (ePrivacy) plus GDPR govern this.
  Finland is relatively permissive for B2B, but the opt-out and honest sender identity
  are non-negotiable.

Practical: keep a suppression list of anyone who replies "POISTA", and never email
them again.

## 2. Why the personal-Gmail blast fails

- A personal `@gmail.com` account has a practical send cap around **~500 recipients/day**,
  and cold-sending trips throttling well before that.
- As of 2025–2026, Gmail/Yahoo/Microsoft enforce **bulk-sender rules**: spam-complaint
  rate must stay under **0.30%** (aim <0.10%), bounces under **2%**, and marketing mail
  needs **SPF + DKIM + DMARC** and an **RFC 8058 one-click unsubscribe** header.
- Since **November 2025**, non-compliant bulk mail is **rejected outright** (hard
  bounces), not just sent to spam.
- A personal Gmail can't be properly authenticated for cold outreach the way a domain
  inbox can — so a script firing "naps naps naps" from it is exactly the pattern spam
  filters punish. Expected inbox placement: **poor, and degrading with every send.**

## 3. The setup that actually reaches inboxes (~30 min)

1. **Use a separate sending domain**, not your main one — e.g. `try-tahtikortti.fi`
   or `tahtikortti-mail.fi`. This protects your primary domain's reputation.
2. **Set up a Google Workspace (or Outlook) inbox** on that domain and configure
   **SPF, DKIM, DMARC** (Workspace walks you through it).
3. **Warm the inbox** for ~2–3 weeks before real volume: start 5–10/day and ramp.
   Tools like instantly.ai / warmy.io automate this.
4. **Send in small batches** (20–40/day), personalised, not one 200-blast.
5. **Include a one-click unsubscribe** and a plain-text opt-out line (the pitch
   already has one).
6. **Keep bounces low** — verify emails before sending (e.g. with a verifier) so you
   stay under the 2% bounce / 0.3% complaint lines.

You can still use Eppu's Python script — just point it at the **Workspace domain
inbox** instead of personal Gmail, throttle it, and add the unsubscribe header.

## 4. Expected reach (rough, honest numbers)

| Method | Inbox placement | Reply rate (cold B2B) | Verdict |
|---|---|---|---|
| Personal Gmail, 200 blast | ~20–40% (falling) | <1% | Avoid |
| Warmed domain inbox, batched + authenticated | ~80–90% | ~1–5% | **Recommended for email** |
| In-person walk-in + card demo | ~100% seen | Much higher (face-to-face) | **Best for this product** |

For 200 addresses, a warmed/authenticated setup might reach ~160–180 inboxes and
yield a handful of replies. The same effort walking into 15–20 nearby restaurants
with the physical card will likely produce more real conversations — this product
demos best in person.

## 5. Recommendation for the validation goal

Your #1 goal is a clean read on interest (clicks + quote requests). Best mix:

1. **Landing page live first** (done — deploy it) with analytics on.
2. **In-person: visit 15–20 capital-region restaurants** with a printed card and the
   landing URL. Fastest, highest-signal validation.
3. **Email: one warmed, authenticated domain inbox**, 20–40 personalised sends/day to
   **Oy/Oyj restaurants only**, each driving a click to the page.
4. Measure `cta_click` + `quote_request` in Vercel Analytics. If interest is real,
   *then* build fulfilment/payment.

Skip the 200-from-Gmail blast entirely — it risks your address, your deliverability,
and gives you a noisy signal.

---

### Sources
- Gmail bulk sender requirements 2026 — https://www.warmy.io/blog/email-deliverability/gmail-bulk-sender-requirements-explained/
- Google bulk sender rules / 0.10% spam threshold — https://firstsales.io/blog/google-bulk-sender-rules-2026/
- 90%+ cold email deliverability guide — https://instantly.ai/blog/how-to-achieve-90-cold-email-deliverability-in-2025/
- GDPR cold email B2B (2026) — https://prospeo.io/s/gdpr-cold-email-b2b
- B2B email list Finland / GDPR compliance — https://www.quarvio.io/blog/b2b-email-list-finland
