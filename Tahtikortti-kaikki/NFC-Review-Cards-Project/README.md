# Tähtikortti — Validation MVP

Landing site + outreach assets for validating demand for NFC/QR Google-review cards
for restaurants. Built to execute `PROJECT_PLAN_nfc-review-cards-validation.md`
(Workstream A: landing site; T6: cold-email pitch; T9: deliverability assessment).

"Tähtikortti" is a **working brand name** — rename freely.

## What's here

```
NFC-Review-Cards-Project/
├─ public/index.html      → the landing page (Finnish, self-contained)
├─ vercel.json            → Vercel static config
├─ cold-email-pitch.md    → the cold email (Finnish) + subject lines (T6)
├─ leads-template.csv     → lead-list columns for the ~100–200 restaurants (T5)
└─ DELIVERABILITY-ASSESSMENT.md → how to actually reach inboxes (T9)
```

## 1. Preview locally

Open `public/index.html` in a browser, or:

```bash
cd NFC-Review-Cards-Project
npx serve public
```

## 2. Make the quote form capture leads (required before going live)

The form currently shows a success message but doesn't store submissions until you
connect an endpoint. Fastest no-backend option:

1. Create a free form at https://formspree.io (2 min).
2. Copy its endpoint URL (e.g. `https://formspree.io/f/xxxxxx`).
3. In `public/index.html`, set `const FORM_ENDPOINT = "https://formspree.io/f/xxxxxx";`

Submissions then arrive by email / in your Formspree inbox.

## 3. Deploy to Vercel

```bash
npm i -g vercel      # once
cd NFC-Review-Cards-Project
vercel               # log in, accept defaults → preview URL
vercel --prod        # production URL
```

Or: push this folder to a GitHub repo and "Import Project" at vercel.com.

## 4. Turn on interest tracking (the whole point of validation)

In the Vercel dashboard for the project, enable **Web Analytics**. The page already
fires two custom events — `cta_click` (someone pressed "Pyydä tarjous") and
`quote_request` (someone submitted the form). These are your go/no-go signal.

## 5. Custom domain

Add your domain in Vercel → Settings → Domains. (Domain name is an open decision —
see the project plan, Section 5.)

## Before any cold email goes out

Read `DELIVERABILITY-ASSESSMENT.md` first. Sending ~200 cold emails from a personal
Gmail is the riskiest step in the whole plan and can get the address throttled or
land everything in spam. There's a safer setup that takes ~30 min.
