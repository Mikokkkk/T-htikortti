# Project Plan: AI Marketing Demo Pipeline

> Generated from Wispr Flow dictation on 2026-07-23. Source window: 2026-06-30 (4 transcripts, 1,526 words, primarily one 1,435-word session dictated in Comet). Source language: Finnish.

## 1. Summary

Build a reusable Claude skill (plus supporting workflow) that takes a single input — a small business's website URL — and automatically produces a complete, branded marketing demo package: brand analysis, target-audience definition, a value/brand message, a content plan, AI-generated demo images, short animated videos, and a UGC content plan. The package is assembled with a cold-outreach "teaser" email so it can be sent to the business as a no-cost proof of value. The commercial motive: run an AI-native marketing service agency that outpaces slower, pricier traditional agencies by demoing value up front, converting interested firms into a small paid pilot (~50–100€), then into a value-based full offer. First target niche: small cosmetology firms that sell products/services online.

## 2. Goal & success criteria

- **Goal:** A working skill where feeding in a firm's website URL yields a copy-paste-ready demo package + teaser email, with minimal manual steps.
- **Success criteria:**
  - [ ] Given only a URL, the pipeline outputs: brand profile, audience profile, brand message, content plan, ≥3 demo images, ≥1 animated video, and a UGC plan.
  - [ ] Output includes a ready-to-send teaser email referencing the generated assets.
  - [ ] End-to-end run on one real cosmetology firm completes without manual re-prompting between stages.
  - [ ] At least one real firm receives a demo and responds (funnel validation).
  - [ ] One paid pilot (~50–100€) closed from the first outreach batch.

## 3. Scope

- **In scope:** Small cosmetology firms first (deliberately small, to "practice" and harden the product before larger clients); demo generation; teaser outreach; paid pilot; value-based offer.
- **Out of scope (for now):** Large/enterprise clients; large ad-spend management; anything beyond generating and pitching demo creative. Scale to bigger clients only after the pipeline is proven.

## 4. Context & constraints

- **Stack / tools (as voiced):** Claude with a custom connector; Higgsfield (via MCP) for image + video generation; "nano-banana" (Gemini image model) for the first-pass still images; email for outreach; Comet / Wispr Flow for capture.
- **Access needed by executing agents:** Web access to scrape target sites; Higgsfield MCP (image/video); an image model for stills (nano-banana or equivalent); an email/sending tool; a source of firm contact emails; a place to store generated assets.
- **Constraints:** Keep per-demo generation cost low (demos are free to the prospect); start narrow (one niche) and master it before expanding; speed is the core value proposition.

## 5. Assumptions & open questions

**Assumptions (inferred — correct if wrong):**
- The demo package is delivered by email as a teaser, not as a live site.
- "nano-banana" = Google Gemini image generation for initial stills; Higgsfield animates those stills into short videos.
- The skill should be self-serve from a single URL input, with optional overrides (brand notes, pitch angle).
- Geography starts in Finland / Helsinki (a prior "Helsinki market sectors analysis" was referenced).

**Open questions (need your decision):**
- **Lead sourcing:** How do we get cosmetology firms' contact emails? (Apollo is available in this workspace and could do exactly this — confirm and I'll wire it in.)
- **Sending tool:** Which email channel for outreach — Gmail, an Apollo sequence, or something else?
- **Consent/legal:** Is generating and sending demo creative built from a firm's own brand imagery acceptable for cold outreach in your target markets? Any opt-out handling needed?
- **Budget:** Cap on generation credits per demo, and monthly outreach volume?
- **Pilot terms:** Fixed 50–100€, or scaled by firm size? What exactly does the pilot deliver?

## 6. Workstreams & tasks

### Workstream A: Brand extraction

#### T1 — Scrape and structure a firm's brand from its website
- **Objective:** From a URL, extract a structured brand profile.
- **Steps / approach:** Fetch the site (and key linked pages/socials); pull brand image, brand story, aesthetic, colour scheme, tone, product/service list, and representative images.
- **Inputs / dependencies:** Target URL; web access.
- **Acceptance criteria:** Returns a JSON/markdown brand profile with: brand_story, aesthetic, colour_scheme, values, product_list, sample_image_urls. Fails gracefully on thin sites.
- **Suggested agent/skill:** Web-scraping/browser agent.
- **Source:** "otetaan firman nettisivut, cloudessa pystyy skriippaa sieltä ne informaatio ja kuvia ja sen brändin imagon" (take the firm's website, Claude scrapes the info, images and brand image).

### Workstream B: Audience & message

#### T2 — Define the target audience for the brand
- **Objective:** Derive who the brand sells to.
- **Steps / approach:** From T1's profile, define target audience across: age, gender, style, lifestyle, values.
- **Inputs / dependencies:** T1.
- **Acceptance criteria:** Audience profile covering all five attributes, justified by brand evidence.
- **Source:** "määrittää sille brändille sen kohderyhmän... age, gender style, lifestyle values."

#### T3 — Define brand message / value proposition
- **Objective:** Produce the brand message and value proposition (arvolupaus).
- **Steps / approach:** Synthesize T1+T2 into a one-line value proposition and 2–3 supporting message pillars.
- **Inputs / dependencies:** T1, T2.
- **Acceptance criteria:** One value proposition + supporting pillars, on-brand and audience-aligned.
- **Source:** "Define brand message. Mikä on arvolupaus?" (what is the value proposition?).

### Workstream C: Content generation

#### T4 — Draft a content plan
- **Objective:** A concrete content plan for the demo.
- **Steps / approach:** Based on T1–T3, plan the demo content set (formats, hooks, platforms). Specify how many stills/videos and their themes.
- **Inputs / dependencies:** T1–T3.
- **Acceptance criteria:** Content plan listing each asset, its purpose, platform, and the prompt intent.
- **Source:** "Make a draft content plan and prompt."

#### T5 — Generate first-pass demo images (nano-banana)
- **Objective:** Produce the initial still images.
- **Steps / approach:** Turn each planned still into an image prompt tuned to the audience/context/platform; generate with nano-banana (Gemini image) or equivalent.
- **Inputs / dependencies:** T4; image model access.
- **Acceptance criteria:** ≥3 on-brand demo images matching the content plan.
- **Source:** "fill the first generated images with nano-banana."

#### T6 — Animate images into short videos (Higgsfield)
- **Objective:** Create short animated videos from the stills.
- **Steps / approach:** Feed T5 images into Higgsfield (via MCP) to produce short animated/video versions.
- **Inputs / dependencies:** T5; Higgsfield MCP.
- **Acceptance criteria:** ≥1 short video derived from the generated stills, on-brand.
- **Source:** "animated videos from the original pictures"; "Higgsfield sitä MCP:tä ja siellä promptaa niitä kuvia ja videoita."

#### T7 — Produce a UGC content plan + optimal creator
- **Objective:** A UGC angle for the brand.
- **Steps / approach:** Define a UGC content plan and prompt Higgsfield to create the optimal creator persona/asset for it.
- **Inputs / dependencies:** T1–T3; Higgsfield.
- **Acceptance criteria:** UGC plan + at least one generated "optimal creator" asset.
- **Source:** "I also want a UGC content plan and prompt Higgs field to create the optimal creator."

### Workstream D: Packaging & outreach

#### T8 — Assemble the demo package
- **Objective:** Bundle all assets into one deliverable.
- **Steps / approach:** Collect brand profile, audience, message, content plan, images, video(s), UGC assets into a single shareable package.
- **Inputs / dependencies:** T1–T7.
- **Acceptance criteria:** One organized package (folder/doc) ready to attach or link.

#### T9 — Draft the teaser outreach email
- **Objective:** A cold "we made you this" teaser.
- **Steps / approach:** Write a short teaser email framing the demo, ending with a soft interest ask; personalize per firm.
- **Inputs / dependencies:** T8.
- **Acceptance criteria:** Copy-paste-ready, personalized teaser email referencing the specific assets.
- **Source:** "me lähetetään niille demosähköpostiin, okei me tehtiin teille tämmönen... se oli tiiseri. Kiinnostaako tämä juttu teitä?"

#### T10 — Build the target lead list (cosmetology firms + emails)
- **Objective:** A list of small cosmetology firms with contact emails.
- **Steps / approach:** Source firms in the target geography; collect website URL + contact email for each. (Apollo can do this — see open questions.)
- **Inputs / dependencies:** Lead-sourcing tool; geography decision.
- **Acceptance criteria:** ≥20 firms with URL + verified email.
- **Source:** "me tarvitaan ne osoitteet... sit me voidaan itse vaan pistää sähköposteja" (we need the addresses, then we can send emails).

### Workstream E: Skill-ification

#### T11 — Wrap A–D into a reusable custom skill
- **Objective:** One skill that runs the whole pipeline from a URL.
- **Steps / approach:** Package T1–T9 as a custom skill taking inputs `website_url` (required) and optional `brand_notes` / `pitch_angle`; define custom attributes (brand image, aesthetic, colour scheme, values; audience age/gender/style/lifestyle/values; brand message/value proposition); orchestrate the stages end to end.
- **Inputs / dependencies:** T1–T9 proven manually first.
- **Acceptance criteria:** Running the skill on a new URL produces the full package with no manual stage-by-stage prompting.
- **Source:** "tänkin vois tehdä skilliks... custom skilli, että aina kun vaan pistää firman nettisivut... define the brand image, custom attributes."

### Workstream F: Pilot → offer funnel (commercial)

#### T12 — Define the paid pilot and value-based offer
- **Objective:** The conversion path after interest.
- **Steps / approach:** Specify the ~50–100€ paid pilot deliverable; define how value is demonstrated; template the follow-on value-based offer.
- **Inputs / dependencies:** Pilot-terms decision (open question).
- **Acceptance criteria:** Written pilot definition + value-demo method + offer template.
- **Source:** "maksullinen pilotti joku 50-100 euroa... näytetään et se luo arvoa... sit konkreettinen tarjous mikä ne hyväksyy."

## 7. Execution order

T1 → T2 → T3 → T4 → (T5 → T6, T7 in parallel after T5/T3) → T8 → T9. In parallel: T10 (lead list) once geography is set. Then T11 (skill-ification) after the manual pipeline works end to end. T12 can be drafted anytime; it gates real outreach.

## 8. Deliverables

- A reusable Claude skill: `website_url` → full branded demo package.
- Per-run demo package (brand profile, audience, message, content plan, images, video(s), UGC assets).
- Teaser outreach email template + personalization.
- Target lead list (firms + emails).
- Pilot definition + value-based offer template.

## 9. Handoff notes

- Prove the pipeline **manually on one real cosmetology firm before skill-ifying** — the dictation explicitly wants to master one niche/pilot, then scale.
- Keep per-demo generation cheap; demos are free to the prospect.
- Higgsfield MCP and Apollo (lead sourcing) both appear available in this workspace — likely fastest paths for T6/T7 and T10.
- Resolve the Section 5 open questions (lead sourcing, sending tool, consent, budget, pilot terms) before live outreach.
- Three short "message to Pekka" transcripts in the same window were operational drafts (requesting offer specs before a meeting), not part of this project — noted but excluded.
