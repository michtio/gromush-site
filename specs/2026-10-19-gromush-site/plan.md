---
id: PLAN-2026-10-19-gromush-site
prd: SPEC-2026-10-19-gromush-site
status: in-progress      # draft | approved | in-progress | done
approved_by: Michael Thomas
approved_on: 2026-11-03
---

# Plan: GroMush website (static build from the approved PRD)

Source documents: `prd.md` (approved 2026-11-03), `sitemap.md` (29 pages, templates A–I), `content-inventory.md` (per-page copy), the approved design reference `.impeccable/prototypes/directions/final.html`, wireframes `.impeccable/prototypes/directions/wireframes.html`, and `DESIGN.md` (rewritten 2026-11-03 to document final.html).

## Architecture decisions

- **AD1 Generator: Python 3 stdlib only, in the repo, output committed.** `python3 -I build.py` reads `src/data/*.json` and `src/templates/**`, writes plain HTML/CSS/JS to `docs/`. Weighed against: Jekyll on GitHub Pages (Liquid and `_data/` would cover R36, but the HTML would only exist after GitHub builds it, so no local gate could run before a commit, and local preview needs Ruby on the host); Eleventy or Astro (Node, which on Michael's host means a DDEV project this repo does not have, for a site with no runtime JS framework); hand-maintained HTML (fails R36 and AC6/AC14). Python is already on the host, the existing QA tools are stdlib Python run with `python3 -I`, and the output is what GitHub Pages serves as-is (AC34).
- **AD2 Single data source = JSON files under `src/data/`.** `site.json` (name, origin, base path, email, phone, WhatsApp, locality, socials, legal links), `flags.json` (`certified_organic`, `startup_phase`, `show_future_species`, `phone_published`), `varieties.json` (slug, name, Latin, three taste words, taste sentence, accent token, cut-out and photo ids, pips, `in_range`, nav order; Q10 table verbatim), `towns.json` (slug, name, sub-areas, map coordinates from `build_levering.py`, hero image), `audiences.json`, `recipes.json`, `future_species.json`, `forms.json` (fields, options, reasons, modes), `images.json` (the R44 register: file, alt, flagged, approved_by). JSON because it is stdlib, AI-editable and one format for data and recipes; long page prose stays in the page template, not in JSON.
- **AD3 Template engine: a minimal one written in S1 (`src/gen/template.py`, under 250 lines, unit-tested).** Supports `{{ expr }}` (escaped), `{{{ expr }}}` (raw partials), `{% if %}`, `{% for %}`, `{% include "x.html" with {...} %}`, `{% extends %}` / `{% block %}`, and helpers `url()`, `abs_url()`, `picture()`, `t()`. `string.Template` is too weak for loops and includes; a third-party engine breaks "no dependencies on the host".
- **AD4 Base-path safety.** Every internal href, src and srcset goes through `url('/zwammen/')`, which prefixes `site.base` (`/gromush-site/` now, `/` at the domain launch); canonical, OG and sitemap use `abs_url()` = `site.origin + site.base + path`. The link checker (AD16) fails any internal path that bypasses the helper.
- **AD5 URL shape: one directory per page with `index.html`, links and canonicals with a trailing slash (`/zwammen/`, `/zwammen/gele-oesterzwam/`).** Works without server configuration on GitHub Pages and at a domain root later. R8's scheme is unchanged; the trailing slash is the one addition (decisions-log row, see Rollout).
- **AD6 Publishing: GitHub Pages "Deploy from a branch", branch `main`, folder `/docs`, with `docs/.nojekyll`.** The old site stays untouched in the repo root (served today from `main` + `/`, `build_type=legacy`). Switching the source to `/docs` replaces what is served at `https://michtio.github.io/gromush-site/` and is a Michael approval point (Rollout). A GitHub Actions deployment was weighed and rejected for now: it adds a workflow and a second build, while the committed `docs/` is already the verified artefact. Docs: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site and https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- **AD7 Forms: plain HTML `mailto:`, no service (decision 2026-11-03).** Each `<form>` has `action="mailto:info@gromush.be?subject=<form subject>" method="post" enctype="text/plain"`, so without JS the browser hands the fields to the mail app. With JS, `forms.js` validates inline, then builds `mailto:info@gromush.be?subject=…&body=…` with `encodeURIComponent` (one "Label: value" line per field, Dutch labels from `forms.json`, CRLF line breaks) and navigates to it; the body is kept under ~1,800 characters by truncating the free-text message with a note, because some mail clients cut long mailto URLs. After the hand-off the form is replaced by a note: "Je mailprogramma opent met je aanvraag. Verstuur die mail om je aanvraag af te ronden." with info@gromush.be and phone/WhatsApp as the fallback (R33, AC28, AC29). Spec: RFC 6068 (https://www.rfc-editor.org/rfc/rfc6068). Trade-off accepted by Michael: arrival depends on the visitor sending the mail.
- **AD8 No confirmation email, no spam layer.** R33a is dropped and R34 is the privacy line only: nothing is transmitted by the site, so there is no submission to confirm or filter.
- **AD9 Kept for later:** the form engine keeps the mail hand-off in one function (`submitRequest(form, data)`), so a form service can replace it in one slice if Anthony ever wants one.
- **AD10 Pre-selection by query parameter (`?soort=blauwe`, `?reden=grootkeuken`, `?modus=thuis`) applied by JS on load; links also carry the form anchor.** Without JS the selector shows its default and the visitor chooses. The Grootkeukens needs helper is the first fieldset of the needs form itself, so prefill (R20) is free and no-JS is identical.
- **AD11 Fonts self-hosted (R41):** Young Serif, Work Sans (400/500/600 + italic 400), Kaushan Script, Courier Prime (400/700) as latin-subset woff2 (https://gwfh.mranftl.com/fonts), all OFL, `font-display: swap`, preload of the display face only. final.html's Google Fonts link is removed.
- **AD12 Images:** `tools/images.py` (stdlib `subprocess` around `cwebp`, `avifenc`, `sips`) renders each source into avif + webp + jpeg at 400/800/1200/1600 px; `picture()` emits `<picture>` with avif and webp sources plus a jpeg fallback with width, height, `loading`, `decoding` and the Dutch alt from `images.json` (R37). Cut-outs keep webp with alpha and a png fallback.
- **AD13 Hero network: generated at build time, animated at run time.** The seeded hyphae generator (`mulberry32`, `regenerate()`) is ported to Python so the SVG paths are in the HTML fully grown; JS only animates. No-JS and reduced motion render the complete network with zero script (R12, AC12, AC13). The radial variant uses the same approach: medallions as links with the plain name as accessible name, curved labels as aria-hidden SVG `textPath`, routing gated by the collision probes.
- **AD14 Recipes: progressive dialogs.** Each recipe is a full `<article>` in the page; with JS, cards open it in a native `<dialog>` (`showModal`, focus returns to the card, Escape and backdrop close). Without JS the articles read in place (R26, AC24).
- **AD15 ProefBox promo (R35):** one `<dialog>` partial, state in `sessionStorage` (not a cookie; the cookie page says so), shown on the second page view of the session after 8 s or 40 % scroll, never on `/proefbox/`, `/contact/`.
- **AD16 Committed QA scripts in `tools/` (repo root), not in the git-ignored `.impeccable/tools/`.** The CDP tools are copied and generalised. New: `lint_content.py` (AC1, AC2, AC3a, AC4, AC7, AC21, AC22 on visible text of `docs/**/*.html`, exit 1 on any hit), `check_links.py` (every href/src/srcset/action resolved against `--base`; internal paths must carry the base; external hosts only from an allowlist: `mailto:`, `tel:`, `wa.me`, `instagram.com`, `facebook.com`), `overflow.py` (320/390/768/1024/1440), `serve.sh` (serves `docs/` under the real sub-path at `http://127.0.0.1:8765/gromush-site/`), `qa.sh <page-path...>` (the standard gate). External links are limited to an allowlist (wa.me, instagram.com, facebook.com, gegevensbeschermingsautoriteit.be for the privacy page's complaint link).
- **AD17 Removed-variety forward pages (R17):** for every variety with `in_range: false` the generator emits `docs/zwammen/<slug>/index.html` with `noindex`, a meta refresh and a canonical to `/zwammen/`, one visible link, and leaves it out of the sitemap, nav, listings, cross-sells and form options (AC14, AC15).
- **AD18 Structured data from data, not prose (R40):** `Organization` site-wide, `LocalBusiness` on the homepage with `addressLocality` only, `Product` without `offers`, `Recipe` on the inspiration page. Nothing else.
- **AD19 Navigation is one partial rendered from `src/data/nav.json`** (five items, two dropdowns from data, CTA "Gratis ProefBox" → `/proefbox/`), so AC8 holds by construction; disclosure buttons with `aria-expanded`; the mobile menu reuses final.html's pattern.
- **AD20 Builders: Opus builder agents (general-purpose, model opus), at most 5 concurrently.** Each brief names the slice id, R ids, pasted ACs and the gate, per `references/review-and-traceability.md`.

## Standard gate and per-page bar

Every slice's verification gate includes the **standard gate** on the pages it delivers, served through `tools/serve.sh` (URL prefix `http://127.0.0.1:8765/gromush-site`):

```
python3 -I build.py --base /gromush-site/                       # exit 0, "N pages written"
python3 -I -m unittest discover -s src/gen/tests                 # OK
python3 -I tools/lint_content.py docs                            # "0 hits"
python3 -I tools/check_links.py docs --base /gromush-site/       # "0 broken, 0 off-base"
python3 -I tools/overflow.py <url>                               # "320 ok 390 ok 768 ok 1024 ok 1440 ok"
python3 -I tools/check.py <url> 390 "$(cat tools/sweep.js)"      # errors: [] and {"n":0}
python3 -I tools/check.py <url> 1440 "$(cat tools/sweep.js)"     # errors: [] and {"n":0}
python3 -I tools/nojs.py <url> 390 <scratch>/nojs.png            # nav, sections, forms visible; imgsBroken 0
FONT_SIZE=32 python3 -I tools/fullshot.py <url> <scratch>/x 320  # scrollWidth 320, no clipped text
```

Lighthouse mobile runs through the chrome-devtools MCP `lighthouse_audit` tool against the served URL: Performance, Accessibility, Best Practices and SEO all ≥ 90, LCP < 2.5 s, CLS < 0.1 (R39), on the pages the slice names.

The **per-page bar** in every page slice's manual checks: the Impeccable loop `audit` → fix all P0–P3 → `harden` → `polish` → finish review against `final.html`; WCAG 2.2 AA by keyboard and VoiceOver; 44×44 targets; real link paths; form invalid path and mail hand-off note; no-JS readable; reduced motion intentional; reflow at 200 % text at 320 px; `srcset` on every content image; no horizontal overflow 320–1440.

## Slices

### S1: Data source, generator and page shell

- **Deliverable:** `python3 -I build.py` writes `docs/` from `src/data/*.json` and templates, with one smoke page (`/`) using the shell (head, skip link, placeholder header and footer), the base-path helper, `docs/.nojekyll` and `docs/404.html`.
- **Requirements:** R1, R4, R8, R36, R41
- **Layers:** `build.py`, `src/gen/template.py`, `src/gen/build.py`, `src/gen/tests/`, `src/data/` (all files of AD2, Q10 taste lines verbatim), `src/templates/layouts/base.html`, `tools/serve.sh`, `README-build.md`.
- **Verification gate:** `python3 -I build.py --base /gromush-site/` exit 0; `python3 -I build.py --base /` exit 0 and `grep -c 'href="/gromush-site/' docs/index.html` prints 0; `python3 -I -m unittest discover -s src/gen/tests` OK (escaping, if/for/include/extends, `url()` with both bases, `in_range` filtering, flags); `grep -rn -E 'Gromush|GRO MUSH|GroMUSH' docs` prints nothing; `git status --short` shows nothing under the old site files.
- **Manual checks:** required: Michael changes one taste word in `varieties.json`, rebuilds, sees it on the smoke page; optional: none.
- **Size:** one session; M
- **Builder:** Opus builder agent

### S2: QA scripts and gates

- **Deliverable:** `tools/` holds the committed QA scripts of AD16 and `tools/qa.sh` runs the standard gate on any list of page paths.
- **Requirements:** R1, R2, R2a, R3, R5, R21, R23, R38, R41
- **Layers:** `tools/lint_content.py` with `tools/lint_rules.json`, `tools/check_links.py`, `tools/overflow.py`, `tools/netreq.js` (request hosts and `document.cookie`, AC37), copies of the CDP tools, `tools/qa.sh`, fixture HTML under `tools/tests/` with known violations.
- **Verification gate:** `python3 -I tools/lint_content.py tools/tests/fixtures` prints exactly the 9 seeded hits and exits 1; `python3 -I tools/lint_content.py docs` prints "0 hits"; `python3 -I tools/check_links.py tools/tests/fixtures --base /gromush-site/` reports the 3 seeded broken/off-base links; on `docs` "0 broken, 0 off-base"; `tools/qa.sh /` runs end to end on the S1 smoke page.
- **Manual checks:** required: read the word lists against AC2, AC3a, AC4, AC7, AC21, AC22 and confirm "gepland voor 2027" is the only allowed timing phrase; optional: none.
- **Size:** one session; M
- **Builder:** Opus builder agent (parallel with S3)

### S3: Design tokens, shared components and image pipeline

- **Deliverable:** `src/static/css/site.css` carries final.html's tokens and global styles; shared partials (buttons, slip with tape, grid paper, coupon, polaroid, flip card, stat pips, section head, icon sprite, variety chip, audience card, town card, closing banner) render from data; fonts self-hosted; `tools/images.py` and `picture()` produce responsive images; a components page `docs/_dev/componenten/` (noindex, not in sitemap) shows every component.
- **Requirements:** R4, R15, R37, R38, R41
- **Layers:** CSS, fonts, `tools/images.py`, `src/gen/picture.py`, partials, `images.json`, components page.
- **Verification gate:** standard gate on `/_dev/componenten/`; `check.py <url> 390 "$(cat tools/netreq.js)"` lists only `127.0.0.1` and `document.cookie` is empty; `check.py <url> 1440 "$(cat tools/contrast.js)"` 0 failures (color-mix cases computed by hand); `grep -rc 'fonts.googleapis' docs` prints 0; every `<img>` on the components page has width, height, srcset and alt (`check_links.py --images`).
- **Manual checks:** required: side-by-side with final.html at 1440 and 390 for each component; reduced motion on flip cards; optional: Michael adopts the components page as the living reference.
- **Size:** one session; L (split off the image pipeline if the components page is not done by mid-session)
- **Builder:** Opus builder agent (parallel with S2)

### S4: Header, navigation, footer and ProefBox promo

- **Deliverable:** Every generated page has the identical header (logo, five items, two dropdowns from data, "Gratis ProefBox" CTA, mobile menu), the footer of `sitemap.md` and R9, the skip link, and the promo dialog of R35.
- **Requirements:** R5, R6, R7, R9, R35, R38
- **Layers:** `partials/header.html`, `footer.html`, `promo.html`, `src/static/js/site.js`, `nav.json`; footer phone/WhatsApp conditional on `flags.phone_published` (AC5).
- **Verification gate:** standard gate on `/` and `/_dev/componenten/`; `check.py <url> 390 "$(cat tools/nav-a11y.js)"` prints `ok` (Tab reaches every item and dropdown, Escape closes, `aria-expanded` toggles); `check_links.py --same-chrome` finds identical header and footer across all pages; `tools/promo.js` prints `none shown dismissed-none`; with `phone_published=false`, `grep -rc 'tel:' docs` is 0.
- **Manual checks:** required: VoiceOver through header and footer; dropdowns on touch (390) and hover (1440); promo closes with button, Escape and backdrop and returns focus; promo never on `/proefbox/`, `/contact/`; reduced motion; optional: 200 % text with the mobile menu open.
- **Size:** one session; M
- **Builder:** Opus builder agent (after S3)

### S5: Form engine, ProefBox page (template I)

- **Deliverable:** The form engine (fields from `forms.json`, inline validation, the `mailto:` hand-off of AD7 with the native `mailto:` action as the no-JS path, the after-hand-off note with email and phone/WhatsApp, the privacy line) and the `/proefbox/` page with its form and copy.
- **Requirements:** R5, R31, R33, R34, R38, R41
- **Layers:** `partials/form.html`, `src/static/js/forms.js`, `forms.json`, `pages/proefbox.html`.
- **Verification gate:** standard gate on `/proefbox/`; `check.py <url>/proefbox/ 390 "$(cat tools/func.js)"` prints `ok`: empty submit focuses the first invalid field and opens nothing; a valid submit sets `location` to a `mailto:info@gromush.be` URL whose decoded subject contains "ProefBox" and whose body contains every filled field (AC28), then shows the hand-off note with the address and phone (AC29); `nojs.py` shows `action` starting `mailto:info@gromush.be`, `enctype text/plain`, method post (AC28a); `grep -c -i -E 'is ontvangen|is verstuurd|captcha' docs/proefbox/index.html` is 0 (AC29, AC32); `netreq.js` after a submit lists only the site origin (AC37).
- **Manual checks:** required: per-page bar on `/proefbox/`; a real hand-off in Apple Mail and in Gmail-in-browser (via the OS mailto handler) produces a readable mail to info@gromush.be; screen-reader announcement of errors and of the hand-off note; `?soort=blauwe` pre-ticks the blue oyster; optional: a long message is truncated with the note.
- **Size:** one session; M
- **Builder:** Opus builder agent (after S4)

### S6: Contact page with reason selector and home-cook order mode (template I)

- **Deliverable:** `/contact/` with the reason selector of R32, pre-selection from `?reden=`, the home-cook pick-up mode of R42, a contact details card and the region links.
- **Requirements:** R9, R32, R33, R34, R42
- **Layers:** `pages/contact.html`, `forms.json`, `forms.js` mode switching.
- **Verification gate:** standard gate on `/contact/`; `check.py <url>/contact/?reden=grootkeuken 390 "document.querySelector('#f-reden').value"` prints `grootkeuken` (AC31); `?reden=bestelling-thuis` shows the pick-up copy and no address or `€`, and the generated mail body and hand-off note say Anthony confirms the pick-up personally (AC38).
- **Manual checks:** required: per-page bar; every reason matches R32's list exactly; optional: none.
- **Size:** one session; S
- **Builder:** Opus builder agent (after S5)

### S7: Legal pages

- **Deliverable:** `/privacy/`, `/cookies/`, `/voorwaarden/` as drafted placeholders on a plain text template, stating that requests are sent by the visitor's own mail app to info@gromush.be (no processor, nothing stored by the site), "no cookies, one sessionStorage key for the promo", and a visible "concepttekst" note.
- **Requirements:** R9, R34, R41
- **Layers:** `pages/legal/*.html`, `layouts/text.html`.
- **Verification gate:** standard gate on the three pages; `check_links.py` confirms the privacy link from every form resolves.
- **Manual checks:** required: per-page bar; Michael reads the drafts; optional: none.
- **Size:** one session; XS
- **Builder:** Opus builder agent (after S4)

### S8: SEO, sitemap, robots, structured data and forward pages

- **Deliverable:** Every page has a unique title and meta description, OG tags, canonical; `sitemap.xml` and `robots.txt` at the base; JSON-LD per AD18; removed-variety forward pages per AD17; `/_dev/` excluded.
- **Requirements:** R1, R8, R17, R40
- **Layers:** `src/gen/seo.py`, base head, `tools/check_seo.py`.
- **Verification gate:** `python3 -I tools/check_seo.py docs --base /gromush-site/` prints `0 problems`; with `grijze.in_range=false`, the forward page has noindex, refresh and canonical to `/gromush-site/zwammen/`, `grep -c grijze docs/sitemap.xml` is 0, and `grep -rl 'Grijze oesterzwam' docs | grep -v grijze-oesterzwam` prints nothing (AC14, AC15); restore and rebuild.
- **Manual checks:** required: homepage and one product page JSON-LD in Google's Rich Results test; optional: none.
- **Size:** one session; S
- **Builder:** Opus builder agent (after S4; AC14 reruns after S11)

### S9a: Radial hero prototype (approval gate)

- **Deliverable:** A radial hero variant of `final.html` (desktop ≥ 1100 px: centred title, intro and slip with both actions, six medallions three per side with curved names, hyphae growing from the centre; below 1100 px the trunk-and-twig list) for Michael's approval before S9.
- **Requirements:** R10, R10a, R10b, R12
- **Layers:** `final.html` (prototype only), extended collision probes.
- **Verification gate:** probes print `net 0 label 0 rev net 0 label 0` at 1100, 1280, 1440, 1600, 1920 (AC10a); `check.py` at 390 and 320: six links visible, `scrollWidth` equals the width (AC10c); each medallion's accessible name is the plain variety name (AC10b); the reduced-motion screenshot shows the full network.
- **Manual checks:** required: Michael approves the variant (blocks S9); optional: none.
- **Size:** one session; M
- **Builder:** Opus builder agent. **Started 2026-11-03, before plan approval, as design exploration at Michael's request (same exception as the earlier prototypes).**

### S9: Homepage (template A)

- **Deliverable:** `/` as the scroll-driven story of `final.html` with the approved hero, delivery variant 1 with the van, flip cards with the Q10 taste words, taped polaroids, the outdoor note reworded to R23 ("gepland voor 2027", no month or harvest), the audience grid with coupon, the grower block and the ProefBox form (S5 engine).
- **Requirements:** R4, R10, R10a, R10b, R11, R12, R16, R23, R37, R38, R39, R40
- **Layers:** `pages/home.html`, `src/gen/hyphae.py`, `src/static/js/home.js`, `build_levering.py` logic moved to `src/gen/levering.py`.
- **Verification gate:** standard gate on `/`; collision probes zero at all five widths; `check.py <url>/ 1440 "$(cat tools/story-order.js)"` prints the scene ids in R11 order and every scene is reachable by Tab/Page Down (AC11); reduced-motion fullshot shows the full network and all scenes (AC12); `nojs.py` reports the network paths complete (AC13); `scrollprobe.py` samples the van route at three positions without layout jumps; Lighthouse mobile ≥ 90, LCP < 2.5 s, CLS < 0.1 (AC36).
- **Manual checks:** required: per-page bar; AC10 at 1440; medallion links announce plain names; keyboard focus on a medallion completes the drawing; optional: 1920 and 1100 visual pass.
- **Size:** one session; L (split S9.1 hero + delivery, S9.2 remaining scenes if needed)
- **Builder:** Opus builder agent (after S9a approval and S5)

### S10: Range overview (template B)

- **Deliverable:** `/zwammen/` lists every in-range variety with photo, name, taste words and link, plus the ProefBox and inspiration links.
- **Requirements:** R4, R13, R17, R37, R38, R40
- **Layers:** `pages/zwammen.html`, variety card partial.
- **Verification gate:** standard gate on `/zwammen/`; card count equals the in-range count in `varieties.json`; with `grijze.in_range=false` the card is gone (AC14), restore.
- **Manual checks:** required: per-page bar; optional: none.
- **Size:** one session; S
- **Builder:** Opus builder agent (wave 1)

### S11: Product template ×6 (template C)

- **Deliverable:** Six product pages from one template in R14 order, per-variety accent, "Bestel" to `/contact/?reden=bestelling-thuis&soort=<slug>#formulier` and "Vraag aan" to `/proefbox/?soort=<slug>#formulier`, cross-sell from data, Product JSON-LD without price.
- **Requirements:** R2a, R3, R4, R14, R15, R16, R17, R37, R38, R39, R40
- **Layers:** `pages/zwam.html`, `varieties.json` extended with intro, characteristics, uses, who-for, packaging, storage.
- **Verification gate:** standard gate on `/zwammen/gele-oesterzwam/` and `/zwammen/blauwe-oesterzwam/`; `tools/check_sections.py docs/zwammen/*/index.html --order hero,intro,smaak,tijdlijn,kweker,keuken,voor-wie,product,bewaren,andere,slot` prints `6 ok` (AC16); `check.py <url>/proefbox/?soort=blauwe 390 "document.querySelector('#chk-blauwe').checked"` prints true (AC17); AC14 rerun; Lighthouse on one product page ≥ 90.
- **Manual checks:** required: per-page bar on two pages; accent never dominates the base palette (R15); grijze flagged in `images.json` until Anthony's photo arrives; optional: all six at 390.
- **Size:** one session; M
- **Builder:** Opus builder agent (wave 1)

### S12: Audience template, Chefs page and /voor-wie router (template D, D-lite)

- **Deliverable:** Template D (problem → offer → own primary action in hero and closing) with `/voor-wie/chefs/` and the `/voor-wie/` router reusing the homepage audience grid.
- **Requirements:** R2a, R4, R5, R18, R37, R38, R40
- **Layers:** `layouts/audience.html`, `pages/voor-wie/chefs.html`, `pages/voor-wie/index.html`, `audiences.json`.
- **Verification gate:** standard gate on both pages; `check_sections.py --primary-action` finds the ProefBox link in the hero and closing of chefs (AC18); the AC3a rule passes on chefs.
- **Manual checks:** required: per-page bar; "ChefBox" appears only for the paid order; optional: none.
- **Size:** one session; M
- **Builder:** Opus builder agent (wave 1)

### S13: Grootkeukens page with needs helper and needs form

- **Deliverable:** `/voor-wie/grootkeukens/` on template D with the start-up statement (flag), the needs helper as the first fieldset of the needs form, no kilogram figure, price or formula, primary action "Bespreek jouw behoefte".
- **Requirements:** R2a, R18, R19, R20, R33, R34
- **Layers:** `pages/voor-wie/grootkeukens.html`, `forms.json`, `forms.js` step styling.
- **Verification gate:** standard gate; with `startup_phase=true` the statement precedes the helper (`check_sections.py --before startup,helper`, AC19), with `false` it is absent and nothing else changes; `grep -E -c 'kg|kilo|€'` on the page is 0 (AC20); the generated mail body contains the four helper answers.
- **Manual checks:** required: per-page bar; helper usable by keyboard only and without JS; optional: none.
- **Size:** one session; M
- **Builder:** Opus builder agent (wave 2)

### S14: Speciaalzaken page with intake form, and Thuis & MushLove page

- **Deliverable:** `/voor-wie/speciaalzaken/` (template D, intake form, no free-trial promise) and `/voor-wie/thuis/` (template D, consumer tone; actions: order for pick-up, follow MushLove on Facebook and Instagram, adopt a bucket; nothing bookable).
- **Requirements:** R2a, R9, R18, R21, R24, R33, R34, R42
- **Layers:** `pages/voor-wie/speciaalzaken.html`, `pages/voor-wie/thuis.html`, `forms.json` (intake form).
- **Verification gate:** standard gate on both; AC21 rule 0 hits on speciaalzaken; the MushLove Facebook id appears on thuis and nowhere else outside it; no workshop, visit or date presented as bookable (AC22 rule plus a "reserveer/boek" rule on thuis); the intake form's mail body contains every field.
- **Manual checks:** required: per-page bar on both; flagged community images used as atmosphere only, never as evidence; optional: none.
- **Size:** one session; M
- **Builder:** Opus builder agent (wave 2)

### S15: Ons verhaal (template E)

- **Deliverable:** `/ons-verhaal/` in Anthony's voice with the real photos (family, cameraman, grower), consumer tone allowed, no "100% biologisch", no reservation flow.
- **Requirements:** R2, R2a, R25, R37, R38, R40
- **Layers:** `pages/ons-verhaal/index.html`, three real images through the pipeline.
- **Verification gate:** standard gate; `lint_content.py` 0 hits; the page's images are the three real ones per `images.json` (`flagged: false`).
- **Manual checks:** required: per-page bar; optional: Michael reads the voice.
- **Size:** one session; S
- **Builder:** Opus builder agent (wave 1)

### S16: Kweekproces and Adopteer (template F)

- **Deliverable:** `/ons-verhaal/kweekproces/` (four indoor phases plus harvest and delivery, real photography, polaroid and phase-line components) and `/ons-verhaal/adopteer/` (bucket adoption by form, no price, no log sets, link to the Buitenkweek interest registration).
- **Requirements:** R22, R23, R24, R33, R34, R37, R38
- **Layers:** `layouts/process.html`, `pages/ons-verhaal/kweekproces.html`, `pages/ons-verhaal/adopteer.html`, `forms.json` (adoption form).
- **Verification gate:** standard gate on both; `grep -E -c 'boomstam|€|249|49'` on the adoption page is 0 and the form is present (AC23); AC22 rule 0 hits; the adoption form's mail body contains every field.
- **Manual checks:** required: per-page bar; process figures only where the inventory marks them as Anthony's text; optional: none.
- **Size:** one session; M
- **Builder:** Opus builder agent (wave 2)

### S17: Buitenkweek (template F, plan page)

- **Deliverable:** `/ons-verhaal/buitenkweek/` in R43's order: hero "Buitenkweek op boomstammen, gepland voor 2027", "Wat is een voedselbos?" as a general explanation, six log-growing steps as method with ink-style illustrations, the removable future-species row (R45), closing "Hou me op de hoogte" interest registration on a taped grid-paper note.
- **Requirements:** R2, R23, R33, R34, R43, R44, R45
- **Layers:** `pages/ons-verhaal/buitenkweek.html`, `future_species.json` (8 species, one neutral line each, drafted for Anthony's check), six SVG step illustrations, `forms.json` (interest form).
- **Verification gate:** standard gate; `check_sections.py --order hero,voedselbos,methode,soorten,interesse` prints ok (AC39); AC2 and AC22 rules 0 hits; with `show_future_species=false` the section, heading and anchor are gone and the rest of the page is byte-identical (AC41), restore; no link or focus stop inside the row and every item contains "binnenkort" (AC42); `grep -c 'hero-buitenkweek\|voedselbos.jpeg' docs` is 0.
- **Manual checks:** required: per-page bar; copy checked line by line against the PRD table "what stays and what goes"; optional: Anthony checks the 8 species lines (blocks launch, not the slice).
- **Size:** one session; M
- **Builder:** Opus builder agent (wave 3)

### S18: Inspiratie with recipe dialogs (template G)

- **Deliverable:** `/inspiratie/` with the two cooking methods, the tip block, the recipe collection from `recipes.json` (4 at launch, no fixed count) opening in accessible dialogs with ingredients, steps, servings and the variety link, consumer tone allowed, a ProefBox block.
- **Requirements:** R2a, R5, R26, R27, R37, R38, R40
- **Layers:** `pages/inspiratie.html`, `partials/recipe.html`, `src/static/js/recipes.js`, `recipes.json` (the 4 supplied recipes, ghee/boter made consistent), dish images.
- **Verification gate:** standard gate; card count equals `recipes.json` length (AC25; a fifth recipe in a scratch copy gives 5); `check.py "$(cat tools/dialog.js)"` prints `open focus-inside esc-closed focus-returned` (AC24); `nojs.py` reports four readable recipe articles; `check_seo.py` finds 4 valid Recipe objects.
- **Manual checks:** required: per-page bar; VoiceOver in a dialog; dialog at 390 near-fullscreen with internal scroll; optional: print view.
- **Size:** one session; M
- **Builder:** Opus builder agent (wave 2)

### S19: Town pages ×5 (template H)

- **Deliverable:** Five town pages from one template: unique H1, title and meta, local hero image, sub-areas, the four audiences, ProefBox CTA, towns presented as delivery regions only.
- **Requirements:** R2a, R28, R30, R37, R38, R39, R40
- **Layers:** `pages/leveringsregio/gemeente.html`, `towns.json` extended with hero, intro and sub-areas (the brief's Blankenberge copy error fixed).
- **Verification gate:** standard gate on `/leveringsregio/brugge/` and `/leveringsregio/sluis/`; `check_seo.py` proves five unique titles, descriptions and H1s (AC26); no "gevestigd in / kweken in / kwekerij in <town>" on any town page (AC27); Lighthouse on one town page ≥ 90.
- **Manual checks:** required: per-page bar on two pages; the AI hand-over image is not used as proof of delivery (R44); La Réserve photo not used; optional: all five at 390.
- **Size:** one session; M
- **Builder:** Opus builder agent (wave 3)

### S20: Leveringsregio hub with stylised map (template H-lite)

- **Deliverable:** `/leveringsregio/` showing all towns on the stylised region map of delivery variant 1, with a link to each town page and the ProefBox CTA.
- **Requirements:** R29, R30, R37, R38
- **Layers:** `pages/leveringsregio/index.html`, `src/gen/levering.py` from S9 in a static mode.
- **Verification gate:** standard gate; `check.py` counts five town links on the map and five in the list; `nojs.py` shows the map and all labels; `netreq.js` shows no map-service host.
- **Manual checks:** required: per-page bar; labels readable at 320 and 200 % text; optional: none.
- **Size:** one session; S
- **Builder:** Opus builder agent (wave 3, after S9)

### S21: Site-wide performance, accessibility and launch checklist

- **Deliverable:** The whole site passes the standard gate and Lighthouse, the image register is resolved, and the publishing switch is prepared.
- **Requirements:** R7, R37, R38, R39, R40, R41, R44
- **Layers:** `tools/crawl.py` (AC9), `tools/qa.sh --all`, `images.json` approvals, publishing section in `README-build.md`.
- **Verification gate:** `tools/qa.sh --all` exit 0 over all 29 pages; `python3 -I tools/crawl.py docs --base /gromush-site/` prints `29/29 within 2 clicks`; Lighthouse mobile ≥ 90 on `/`, `/zwammen/gele-oesterzwam/`, `/leveringsregio/brugge/`, `/voor-wie/grootkeukens/`, `/inspiratie/`, `/proefbox/`; `netreq.js` on five pages lists only the site origin and no cookie (AC37); a `--base /` build passes `check_links.py` too.
- **Manual checks:** required: image register review with Anthony (AC40); keyboard and VoiceOver pass on one page per template; axe via the chrome-devtools a11y flow on one page per template (AC35); optional: 1920 pass on the homepage.
- **Size:** one session; M
- **Builder:** Opus builder agent (last)

### Parallelism

- Already running: S9a (prototype in `final.html`, independent of the build).
- Foundations: S1 → (S2 ‖ S3) → S4 → (S5 ‖ S7 ‖ S8) → S6.
- Wave 1 (after S5, max 5): S10, S11, S12, S15.
- Wave 2 (after S9a approval): S9, S13, S14, S16, S18.
- Wave 3: S17, S19, S20 (S20 after S9).
- Final: S21.

## Coverage

| Requirement | Slices |
|---|---|
| R1 | S1, S2, S8 |
| R2 | S2, S15, S17 |
| R2a | S2, S11, S12, S13, S14, S15, S18, S19 |
| R3 | S2, S11 |
| R4 | S1, S3, S9, S10, S11, S12 |
| R5 | S4, S5, S12, S18 |
| R6 | S4 |
| R7 | S4, S21 |
| R8 | S1, S8 |
| R9 | S4, S6, S7, S14 |
| R10 | S9a, S9 |
| R10a | S9a, S9 |
| R10b | S9a, S9 |
| R11 | S9 |
| R12 | S9a, S9 |
| R13 | S10 |
| R14 | S11 |
| R15 | S3, S11 |
| R16 | S9, S11 |
| R17 | S8, S10, S11 |
| R18 | S12, S13, S14 |
| R19 | S13 |
| R20 | S13 |
| R21 | S2, S14 |
| R22 | S16 |
| R23 | S2, S9, S16, S17 |
| R24 | S14, S16 |
| R25 | S15 |
| R26 | S18 |
| R27 | S18 |
| R28 | S19 |
| R29 | S20 |
| R30 | S19, S20 |
| R31 | S5 |
| R32 | S6 |
| R33 | S5, S6, S13, S14, S16, S17 |
| R34 | S5, S6, S7, S13, S14, S16, S17 |
| R35 | S4 |
| R36 | S1 |
| R37 | S3, S9, S10, S11, S12, S15, S16, S18, S19, S20, S21 |
| R38 | S2, S3, S4, S5, every page slice, S21 |
| R39 | S9, S11, S19, S21 |
| R40 | S8, S9, S10, S11, S12, S15, S18, S19, S21 |
| R41 | S1, S2, S3, S4, S5, S7, S21 |
| R42 | S6, S14 |
| R43 | S17 |
| R44 | S14, S17, S19, S21 |
| R45 | S17 |

Every MUST has at least one slice. Every slice has R ids.

## Test strategy

- **Unit (automatic):** template engine, `url()`/`abs_url()` under both bases, `in_range` and flag filtering, `picture()` output, hyphae generator determinism (`python3 -I -m unittest`).
- **Build-output checks (automatic, every slice):** `lint_content.py` (AC1, AC2, AC3a, AC4, AC7, AC21, AC22), `check_links.py` (real paths, base-path safety, image attributes, identical header and footer), `check_seo.py` (AC15, AC26, R40), `check_sections.py` (AC16, AC18, AC19, AC39), `crawl.py` (AC9).
- **Browser checks (automatic, headless Chrome via `tools/`):** JS errors, 44 px sweep, overflow at five widths, no-JS visibility, reduced-motion and 200 % text screenshots, hero collision probes, form flows, dialog and promo flows, request hosts and cookies (AC37).
- **Lighthouse (semi-automatic):** chrome-devtools MCP, mobile, on the pages named per slice and site-wide in S21.
- **Manual:** per-page bar, real mail hand-off in two mail clients (AC28, AC28a), Michael's approval of the radial hero, Anthony's sight on the Q10 taste words, the 8 species lines and the image register (AC40).
- **Regression before each merge:** `tools/qa.sh --all` on the full build, with both `--base /gromush-site/` and `--base /`.

## Rollout and migration

1. Build output is committed in `docs/` from S1 on; the old site files in the repo root are not touched, moved or deleted.
2. (No form account needed: forms hand off to the visitor's mail app, AD7.)
3. PRD decisions-log rows to add when this plan is approved: URLs carry a trailing slash (AD5); pre-selection by query parameter is JS-only (AD10). `sitemap.md` drops its mention of a cookie consent banner (overruled by R41).
4. **Approval point (Michael):** after S21, switch GitHub Pages from `main` + `/` to `main` + `/docs`. This replaces what `https://michtio.github.io/gromush-site/` serves (the old site disappears from the URL while its files stay in the repo). Rollback is switching back to `/`.
5. Post-switch smoke: `curl -I https://michtio.github.io/gromush-site/zwammen/` returns 200; one real ProefBox hand-off from the live URL arrives at info@gromush.be.
6. The domain launch (gromush.be, DNS, mail authentication, `--base /`, retiring the old files) is the separate PRD named in the PRD's non-goals; this plan only proves the `--base /` build is link-clean (S21).

## Risks

- **mailto hand-off loses requests:** visitors without a configured mail app (common on shared or work PCs, and some Android setups) get nothing from the click; mitigated by the always-visible address and phone/WhatsApp beside every form and the hand-off note, and by keeping the hand-off in one function (AD9) so a form service can be added later if requests go missing.
- **Long mailto URLs truncated by some clients:** body capped at ~1,800 characters, free text truncated with a note.
- **Sub-path breakage:** all paths go through `url()`; `check_links.py` fails off-base links; S21 checks the `--base /` build.
- **Generator drift from `final.html`:** S3's components page is the living comparison; every finish review is against `final.html`; the hyphae and delivery generators are ported with determinism tests.
- **Radial hero rejected or delayed:** S9 ships with the approved trunk-and-twig hero at all widths and R10 returns to Michael as a scope decision.
- **AI imagery (R44):** `images.json` flags every listed image; `check_links.py --images` warns on flagged images in evidence positions; AC40 is handled with Anthony in S21.
- **Content still owed by Anthony:** ProefBox photo (S5 ships with a cut-out mix), grijze photo (Italiaanse cut-out, flagged), the 8 species lines (drafted in S17), 2 more recipes (data only).
- **Corrected Q10 taste words need Anthony's sight:** one place (`varieties.json`), one edit and rebuild (AC6).
- **Trailing-slash URLs differ from the sitemap's bare slugs:** decisions-log row; `check_seo.py` enforces one form.
- **One Pages source at a time:** the switch is explicit in Rollout; `docs/` is never deleted by scripts, only rewritten.
- **Lighthouse ≥ 90 on image-heavy pages:** avif + webp + sizes, lazy loading below the fold, preloaded LCP image, subset fonts; measured per slice.
