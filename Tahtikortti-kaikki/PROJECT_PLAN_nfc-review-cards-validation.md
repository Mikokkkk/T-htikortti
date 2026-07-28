# Project Plan: NFC/QR Google-Review Cards for Restaurants — Validation MVP

> Generated from Wispr Flow dictation on 2026-07-23. Source: transcript from 2026-07-22 22:19 (1,190 words, dictated in Claude). Source language: Finnish. A 2-word fragment at 22:18 was the lead-in and is excluded.

## 1. Summary

Launch and validate a product business selling tap-to-review NFC/QR cards (~30€ each) to restaurants. A customer taps the card (or scans the QR) and is taken straight to the venue's Google review page, making it frictionless to leave a positive review and boosting the restaurant's local Google visibility. The first market is restaurants in the Helsinki capital region ("stadi" bars and party spots), with other industries to follow once proven. Before building any fulfilment or setup process, the priority is to VALIDATE demand: stand up a simple landing website (built with Claude Code, hosted on Vercel) with a low-commitment "request a quote / order" form, and run a cold-email campaign to ~100–200 scraped restaurant addresses. The single most important outcome is a clean signal of interest — clicks and quote requests — plus an assessment of which outreach method reaches the most inboxes.

## 2. Goal & success criteria

- **Goal:** Determine whether restaurants want this product, cheaply and fast, via a live landing page + a cold-email test — with interest measured, not assumed.
- **Success criteria:**
  - [ ] Landing site live on Vercel with promo imagery, service + team copy, and a working quote/order form.
  - [ ] Form captures at minimum a company email; optionally quantity of cards and the desired Google-review link.
  - [ ] A list of ~100–200 target restaurants (name + email) in a Google Sheet.
  - [ ] Cold-email pitch sent to that list via the existing automation.
  - [ ] Interest quantified: number of link clicks and number of quote requests.
  - [ ] Written deliverability assessment: expected inbox-reach and best D2C outreach method.

## 3. Scope

- **In scope:** Validation only — landing page, cold-email test, interest measurement, deliverability assessment. Non-binding "request a quote" flow (company email only) to maximize response.
- **Out of scope (for now):** Card sourcing/fulfilment automation, payment integration, account setup, delivery logistics, scaling to non-restaurant industries, AI marketing-video posting. These are explicitly deferred until interest is confirmed. ("nyt tärkeintä on se että halutaan vaan määrittää kuinka paljon klikkauksia me saadaan" — the most important thing right now is just to measure how many clicks we get.)

## 4. Context & constraints

- **Stack / tools (as voiced):** Website built with Claude Code, hosted on Vercel; Google Sheets for the lead list; "Eppu's" existing Python→Gmail automation (reads a Google Doc pitch + Gmail + the Sheet, then sends from your own Gmail); own Gmail as the sending account.
- **Sales motion:** Primarily online validation now; in-person walk-in demo pitch described as the eventual sales method (deliver ~50 cards/day around the capital region if demand appears).
- **Constraints:** Move fast and cheap; keep the ask non-binding; quality AND quantity on the email ("hyvä sähköposti / pitch, sit lähetään se meiningillä").

## 5. Assumptions & open questions

**Assumptions (inferred — correct if wrong):**
- The link behind each NFC card = the restaurant's Google review URL.
- Price point is ~30€ per card ("kolmekymppiä").
- "Request a quote" = a lightweight lead form (company email + quantity), followed by manual, personal follow-up and later invoicing ("me olemme sinuun henkilökohtaisesti yhteydessä ja varmistamme maksutiedot").
- Sending is from your personal Gmail via Eppu's script.

**Open questions (need your decision):**
- **Card supplier:** Where do the physical NFC/QR cards come from, at what unit cost? (Determines the 30€ margin.)
- **Legal / compliance:** Cold B2B email and scraping business contacts in Finland/EU is governed by GDPR + ePrivacy. Sending 200 unsolicited emails from a personal Gmail carries both legal and deliverability risk — needs a compliant approach (opt-out, sender identity). **Flagging as a real blocker to resolve before sending.**
- **Deliverability:** Bulk-sending from personal Gmail risks spam-foldering and account limits. Confirm whether to use a proper sending domain/ESP instead — this ties directly to the assessment you asked for.
- **"Eppu" access:** What does the automation need to run (Gmail API credentials, the Google Doc, the Sheet)? Is Eppu available to wire it up?
- **Domain:** What domain/brand name for the landing site?
- **Lead source:** Scrape from Google Maps/Places for capital-region restaurants — confirm geography and any target sub-segment (bars vs. full restaurants).

## 6. Workstreams & tasks

### Workstream A: Validation landing site

#### T1 — Build the landing page (Claude Code)
- **Objective:** A single, fast landing page that explains the product and captures interest.
- **Steps / approach:** Build with Claude Code. Sections: hero with promo images of the NFC/QR cards; how it works (tap → Google review → more visibility); who we are / team; the pitch (restaurants boost Google reviews organically, one customer at a time); a prominent "Request a quote / Order" call to action.
- **Inputs / dependencies:** Promo images (T2); copy from the pitch.
- **Acceptance criteria:** Responsive page, loads fast, renders the form (T3), deployable.
- **Source:** "me haluttais rakentaa sen nettisivun maailman helposti Cloud-kodeilla... näytetään hyvät promokuvat... kerrotaan meidän palvelusta."

#### T2 — Source promo images of the product
- **Objective:** Good visuals of NFC/QR review cards in restaurant context.
- **Steps / approach:** Find relevant royalty-safe images online, or generate them; select a small on-brand set for the hero and how-it-works sections.
- **Inputs / dependencies:** None.
- **Acceptance criteria:** ≥3 usable, licensing-safe promo images.
- **Source:** "etitään netistä relevantit kuvat, pistä ne sinne sivulle."

#### T3 — Build the "request a quote / order" form
- **Objective:** A low-friction, non-binding interest capture.
- **Steps / approach:** Form fields: company email (required), quantity of cards (optional), desired Google-review link (optional). Framed as "Request a quote" — not "Contact us". Store submissions (e.g. to a Sheet/DB) and confirm on submit. Copy stresses no commitment + fast personal follow-up.
- **Inputs / dependencies:** T1.
- **Acceptance criteria:** Submissions are captured and retrievable; email validation works; explicit "non-binding" copy present.
- **Source:** "tehdään vaan tilaus... kysyt tarjouspyyntö... se ei sido niitä mihinkään... paina tästä linkistä niin olemme sähköpostitse yhteydessä."

#### T4 — Deploy to Vercel with click analytics
- **Objective:** Live site with interest tracking.
- **Steps / approach:** Deploy to Vercel; add lightweight analytics to count visits and CTA clicks; verify the form end-to-end in production.
- **Inputs / dependencies:** T1–T3; domain decision (open question).
- **Acceptance criteria:** Public URL live; clicks + form submissions measurable.
- **Source:** "hostaa sen verselillä silleen vaan me saatais nopeesti trafiikkiä."

### Workstream B: Lead list

#### T5 — Scrape ~100–200 capital-region restaurants into a Google Sheet
- **Objective:** A clean target list.
- **Steps / approach:** Collect restaurant name + contact email (and city/area) for Helsinki-region restaurants/bars into a Google Sheet, deduplicated.
- **Inputs / dependencies:** Geography confirmation; a scraping source (e.g. Google Maps/Places).
- **Acceptance criteria:** ≥100 rows with valid-format emails, no duplicates.
- **Source:** "skreipataan vaikka Google Sheetsii... 200 osoitetta."

### Workstream C: Cold-email campaign

#### T6 — Write the pitch email (+ promo images)
- **Objective:** A strong, on-message cold email.
- **Steps / approach:** Adapt the spoken walk-in pitch into email form: noticed your restaurant is hard to find locally on Google → our NFC card gets your customers leaving more positive reviews → easy one-tap → soft CTA to request a quote. Include promo images. Keep it credible and personal.
- **Inputs / dependencies:** T2.
- **Acceptance criteria:** Final copy + subject line + images, reviewed against the pitch intent.
- **Source:** "tehdään tänne tosi hyvä promosähköpostipitjaus... mut sähköpostimuodossa... hyvät promokuvat."

#### T7 — Wire up and run Eppu's send automation
- **Objective:** Send the campaign through the existing script.
- **Steps / approach:** Configure Eppu's Python automation to read the pitch (Google Doc), pull addresses from the Sheet (T5), and send from your Gmail. **Do a small test batch first** (deliverability + rendering) before the full run.
- **Inputs / dependencies:** T5, T6; Eppu access; legal/deliverability decisions (Section 5).
- **Acceptance criteria:** Test batch delivers correctly; full run completes with a send log.
- **Source:** "lähetään Epun automaatioon... se lukee google docsin, gmailin, sheetsit ja lähettää sun gmailista naps naps naps."

### Workstream D: Measurement & assessment

#### T8 — Measure interest (go/no-go signal)
- **Objective:** Quantify demand.
- **Steps / approach:** Track landing-page clicks and quote-request submissions; attribute to the campaign; report totals and conversion rate.
- **Inputs / dependencies:** T4, T7.
- **Acceptance criteria:** A short report: emails sent, opens/clicks (if measurable), site visits, quote requests, conversion %.
- **Source:** "tärkeintä on määrittää kuinka paljon klikkauksia ja kuinka moni painaa 'lähetän mun sähköpostin, oon kiinnostunut'."

#### T9 — Deliverability / outreach-method assessment
- **Objective:** Advise on the best way to actually reach inboxes.
- **Steps / approach:** Assess spam risk of bulk-sending from personal Gmail; estimate inbox-reach; compare methods (personal Gmail script vs. proper sending domain/ESP vs. warmed inbox) for direct-to-consumer cold outreach; recommend one.
- **Inputs / dependencies:** None (can run in parallel).
- **Acceptance criteria:** Written recommendation with expected reach rate and the risks of each method.
- **Source:** "mä haluun että se arvioidaan... mikä on paras metodi lähettää... meneekö ne suoraan roskapostiin... kuinka paljon ihmisiä me saavutetaan."

### Workstream E: Later (deferred until validated)

#### T10 — In-person pitch + fulfilment kit
- **Objective:** The walk-in sales motion once demand is shown.
- **Notes:** Physical card demo; deliver ~50 cards/day around the capital region; per-card link setup. Defer.
- **Source:** "kävellään ravintolaan, meillä on korttikärjys... 50 korttia päivässä."

#### T11 — AI marketing-video auto-posting
- **Objective:** Steady social content by an agent.
- **Notes:** Reuse the AI marketing-video approach; an agent posts at a steady cadence. Defer.
- **Source:** "markkinointivideot, joku agentti vaan postaa niitä tasaiseen tahtiin."

## 7. Execution order

Parallel start: (A: T1→T2→T3→T4 for the site) and (B: T5 lead list) and (D: T9 deliverability assessment). Then C: T6 → T7 (test batch → full send) once site + list are ready. Then D: T8 measurement after the send. E (T10, T11) only after T8 shows positive interest. Resolve Section 5 legal/deliverability blockers before T7.

## 8. Deliverables

- Live Vercel landing site with a working quote/order form.
- Google Sheet of ~100–200 target restaurants.
- Cold-email pitch (copy + images) and a completed send with logs.
- Interest report (clicks + quote requests).
- Deliverability / outreach-method recommendation.

## 9. Handoff notes

- **Validate before you build ops** — the dictation is explicit that measuring interest is the #1 priority; don't invest in fulfilment/payments yet.
- **Legal + deliverability are genuine blockers** for the email blast — resolve the Section 5 questions before T7. Bulk-sending 200 cold emails from a personal Gmail is the riskiest part of the plan.
- Keep the form ask non-binding — that framing is a deliberate design choice you emphasized.
- This is a **separate project** from the June 30 "AI Marketing Demo Pipeline" plan (that one was AI-generated marketing creative for cosmetology firms). They may share tooling (scraping, cold email, AI video) but are different offerings.
