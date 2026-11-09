# ATS Projects — Authorized Channel Partner (React)

A React recreation of **atsproject.in**: 30 ATS Group (ATS Greens / ATS
Homekraft) projects across Noida, Greater Noida and Ghaziabad, with project detail pages, city
landing pages, enquiry forms and full SEO plumbing.

> **Disclaimer:** This is a channel-partner website. It is **not** the
> official ATS Group website (official: https://www.ats.ind.in/).

## Stack

- Vite 5 + React 18 + react-router-dom 6, plain CSS (no Tailwind)
- Clean URLs: `/`, `/projects`, `/projects/:slug`, `/projects-in-:city`
  (3 cities), `/about`, `/contact`, custom 404

## Run it

```bash
npm install
npm run dev      # local dev
npm run build    # production build into dist/
npm run preview  # preview the build
```

Deploy the `dist/` output (or the whole project on Vercel — `vercel.json`
is included with SPA rewrites, security headers and legacy redirects).

## Where everything lives

| What | Where |
| --- | --- |
| **All editable values** — domain, phone `8799756026`, WhatsApp number, EmailJS keys, tracking IDs, logo/OG paths, city list | `src/config.js` |
| Project data (30 in-scope projects, scraped 2026-11-05) | `src/data/projects.js` (generated) |
| Raw scrape audit copy | `projects-data.json` (project root) |
| Enquiry lead logic (EmailJS + WhatsApp fallback) | `src/lib/lead.js` |
| Conversion tracking + cookie consent state | `src/lib/tracking.js` |
| Sitemap / robots | `public/sitemap.xml`, `public/robots.txt` (generated) |
| Images | `public/images/projects/{slug}/`, `public/images/city/`, `public/images/home/` |
| Icons / OG image | `public/assets/` (generated from the ATS logo) |

To regenerate data/sitemap/icons after a re-scrape:

```bash
python3 tools/scrape.py        # re-scrape atsproject.in (needs bs4 + Pillow)
node tools/gen-data.mjs        # projects.js, sitemap, robots, vercel.json
python3 tools/gen-assets.py    # favicons, app icons, OG image, webmanifest
```

## Forms

The enquiry form sends via **EmailJS REST** using the keys in
`src/config.js` (taken from the source site's own `SITE_CFG`:
service `service_fkmfynb`, template `template_bdjcyq6`). **If the email
send fails, WhatsApp automatically opens with the enquiry pre-filled** —
a lead is never lost silently. Always run one live test enquiry after
deploying before saying the form works.

## Tracking

`src/lib/tracking.js` queues every conversion event (`page_view`,
`view_project`, `form_submit`, `form_error`, `call_click`,
`whatsapp_click`, `cookie_consent`) to `window.dataLayer`. GA / Google
Ads / Meta Pixel load **only after cookie consent** and only when their
IDs are filled in `src/config.js` (`gaId`, `googleAdsId`, `metaPixelId`
— all blank placeholders by default).

## Legacy URL redirects (in `vercel.json`)

- `/projects-in-{city}/{slug}/index.html` → `/projects/{slug}` (301)
- `/projects-in-{city}/index.html` → `/projects-in-{city}` (301)
- `/{slug}/index.html` → `/projects/{slug}` (301)
- `/index.html` → `/` (301)
- Everything else rewrites to `/index.html` (SPA)

The app also handles these paths in-browser (`LegacyRedirects` in
`src/App.jsx`) for non-Vercel hosts.

## Content notes (important)

- Prices and RERA numbers are **exactly as published on atsproject.in**.
  Where a page published no price, the site shows “Price on Request”;
  where it published no RERA number (upcoming projects, e.g. ATS
  Destinaire Phase 2 — “Coming Soon”), the site shows “Coming Soon” and
  **no number was invented**.
- The source homepage schema claimed a 4.9 rating / 5,670 reviews; that
  aggregate rating was deliberately **not** carried into this site's
  structured data.
- Final scope confirmed by the user: only Noida, Greater Noida and
  Ghaziabad are published (30 projects). The other source cities were
  removed from the site data, city routes, images, sitemap and redirects.
  Chandigarh and Dehradun were also error pages with zero projects.
- Images are the projects' own published images, converted to WebP
  (max width 1600px) with lazy loading; heroes load eager.
