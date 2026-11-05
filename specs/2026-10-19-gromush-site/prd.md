---
id: SPEC-2026-10-19-gromush-site
title: GroMush website (fresh build from Anthony's October briefs)
status: in-progress      # draft | approved | in-progress | done | superseded
owner: Michael Thomas (Bleu Chaud)
approved_by: Michael Thomas
approved_on: 2026-11-03
linear:
supersedes:
---

# GroMush website

Source material: 27 briefing emails from Anthony Watteeuw (11 to 14 Oct 2026), extracted to `_resources/2026-10-mails-anthony/`, plus his 3 Nov 2026 email (`_resources/2026-11-mails-anthony/`: homepage approval, hero reference, Buitenkweek PDF). The working digest of all 25 PDF briefs, with per-page copy, 21 logged contradictions and 30 client questions, lives with this spec as `content-inventory.md`. This PRD ignores the previous site and its design entirely. The approved visual and behavioural reference is `.impeccable/prototypes/directions/final.html`.

## Problem and outcome

GroMush is a one-person, start-up oyster-mushroom farm in Knokke-Heist (Westkapelle) run by Anthony Watteeuw. It grows six oyster varieties indoors in 20L straw buckets and sells them direct, with no wholesaler, to chefs, large kitchens, speciality shops and home cooks in Knokke-Heist, Damme, Sluis, Brugge and Blankenberge. Today there is no website that turns that story into requests (gromush.be is a TransIP parking page). Anthony has written 25 page briefs, but they disagree on navigation, offers, prices, range and claims, and they describe roughly 30 pages for a business that converts through one action: **a professional asks for a free tasting box, or a home cook asks for an order, and Anthony follows up personally.**

Once this ships, any visitor understands within one screen what GroMush is ("Van kwekerij tot bord": local, artisanal, direct from the grower). Each of the four audiences finds a page written for them, and a professional in the delivery region can request a free tasting box or start a conversation in under a minute. Every submission lands in Anthony's inbox. The site is honest: no invented prices, reviews, certifications or availability.

## Users and context

- **Chefs and restaurant owners** (primary, highest value). Mostly mobile, often between services. They want taste, texture, special varieties, reliable delivery and a low-risk way to try.
- **Large kitchens** (hospitals, care homes, schools, company restaurants, caterers, hotels). Desktop, procurement mindset. They want reliability, volume honesty, food safety, logistics and a contact person.
- **Speciality shops** (greengrocers, bakers, butchers/traiteurs, delis, organic shops). They want a local story for their shelf, a simple way to start, and no free-trial promises.
- **Home cooks and community** (MushLove). Equal primary buyers with professionals (decision 2026-10-19). Instagram and Facebook driven, mobile. They want to order for pick-up, recipes, the story, the process, and things to join (bucket adoption; workshops and visits later).
- **Search visitors** for "oesterzwammen + [town]". They land on town pages or product pages.
- **Anthony** (owner, not technical, no budget). He sends content and corrections; Michael maintains the static site with AI (Q13).

## Scope

- Homepage told as a scroll-driven story, as in `final.html`, opening with the mycelium hero. On desktop the hero takes the radial structure of Anthony's reference (six variety medallions ringed around a centred title, hyphae growing between them); mobile keeps the trunk-and-twig list unless the radial layout works at 390 px. The variant is prototyped in `final.html` and shown to Michael before it moves into the build.
- Range: one overview page plus one page per variety, all from one product template.
- Four audience pages: Chefs, Grootkeukens, Speciaalzaken, Thuis & MushLove (community).
- Story and process: Ons verhaal (about Anthony), Kweekproces (indoor, 4 phases), Buitenkweek (a short, honest page about the plan for outdoor log growing; nothing of it exists today).
- Bucket adoption as a request, and an interest registration for outdoor growing (no online payment, no log-set offer).
- Inspiration: cooking methods plus a recipe collection opening in a dialog.
- Local pages: a Leveringsregio hub plus five town landing pages.
- Conversion: a free ProefBox request page and form, a general contact form with reason pre-selection (including home-cook orders for pick-up), a grootkeuken needs form with a needs helper, and a speciality-shop intake form, all plain HTML: on submit the visitor's own mail app opens with the request pre-filled to info@gromush.be (`mailto:`), because a static site has no server and no form service is used for now.
- One calm, dismissible in-site promo for the ProefBox.
- Static HTML, CSS and JS, hosted on GitHub Pages for now (Q13, Q21). Content is maintained in the repo by Michael with AI assistance; repeated content (varieties, towns, contact details, status flags) comes from one source in the repo.
- Dutch (nl-BE) only, SEO basics, draft legal pages (privacy, cookies), privacy compliance.

## Non-goals

- No CMS, no CRM, no database, no server-side code, no third-party form service; no stored copy of form submissions (Q13, Q14, 2026-11-03 forms decision).
- No analytics, tracking or social embeds (Q15), so no consent banner.
- No launch work: the production domain (gromush.be), DNS, mail authentication and retiring the old site are a separate PRD (Q21).
- No webshop, cart, account, checkout or online payment. Orders and adoption are requests that Anthony confirms personally; payment is by bank transfer or cash, outside the site.
- No prices, discounts, volume tiers, formulas or adoption prices anywhere on the site (Q4). Every pricing question routes to contact.
- No browser push notifications. The "push melding" brief is an in-site promo.
- No live bucket or log tracker ("volg online de ontwikkeling"), booking calendar or ticketing for workshops, visits, tastings or school sessions (Q9).
- No testimonials or cases section until real, attributable quotes exist.
- No product pages for species that are not sold (Black Pearl, koningsoesterzwam, pruikzwam, shiitake, the 8 future outdoor species). The 8 future species appear only as a non-clickable "binnenkort" row on Buitenkweek (Q16, R45).
- No log-set adoption, ownership, formulas, benefits or harvest expectations for outdoor growing, and no imagery presented as GroMush's forest or logs (Q17).
- No pick-up address or schedule on the site; it is communicated after the request (Q8).
- No French or English versions.
- No separate pages for recipes: they open in a dialog on the inspiration page.
- No migration of anything from the previous site.

## Requirements

### Brand and content integrity
- **R1** The brand name MUST always render as "GroMush", including in titles, alt text and metadata. (MUST)
- **R2** The site MUST NOT use "biologisch", "bio", "ecologisch", "gecertificeerd" or "100% biologisch" (terms protected by EU Regulation 2018/848) unless the "certified organic" flag in the data source is on. Unverified claims are absent, not softened. (MUST)
- **R2a** Health and "superfood" language MAY appear only on consumer pages (Thuis & MushLove, Inspiratie, Ons verhaal); professional pages (Chefs, Grootkeukens, Speciaalzaken, town pages, product pages' professional blocks) MUST stay factual. Medical claims (prevents, cures, treats) MUST NOT appear anywhere. (MUST)
- **R3** The site MUST NOT show prices, discounts, volume tiers, dates, availability, addresses or testimonials that are not in the content, and MUST NOT show prices at all in this release (Q4). Where content is missing, the section is hidden, never filled with placeholder data. (MUST)
- **R4** Each variety MUST have one canonical name, Latin name, three taste words and one taste-and-texture sentence (Q10, table below), and every component that shows the variety (homepage, overview, product cross-sell, audience pages, community, forms) MUST use those canonical fields. (MUST)
- **R5** The free trial offer MUST be called "ProefBox" site-wide, including the header CTA "Gratis ProefBox" (Q24). The paid order or subscription for chefs MUST be called "ChefBox" and MUST never label the free offer. (MUST)

### Navigation and structure
- **R6** The primary navigation MUST hold at most six items plus one persistent call to action for the ProefBox, and MUST be identical on every page. (MUST)
- **R7** Every page in the sitemap MUST be reachable from the primary navigation, its dropdowns or the footer within two clicks of the homepage. (MUST)
- **R8** URLs MUST follow one Dutch scheme, as listed in `sitemap.md`, with lowercase slugs and no dates or IDs. (MUST)
- **R9** The footer MUST carry the delivery towns, the email address, the phone number as a call link and a WhatsApp link (Q7), the locality "Westkapelle" without street address, Instagram (`gromush.be`) and the GroMush Facebook page (`profile.php?id=61590322125848`), and the legal links. The Thuis & MushLove page additionally links the MushLove Facebook page (`profile.php?id=61594707453474`). (MUST)

### Homepage
- **R10** On viewports of 1100 px and wider, the homepage MUST open with a centred title "Van kwekerij tot bord", the intro line and the hero actions (Q19), ringed by six round variety medallions (three per side) with the variety name set on a curve above each, and hyphae that grow outward from the centre and branch to each medallion as the page loads and scrolls. Materials stay those of `final.html` (ink on straw), not the reference's dark green and glowing gold. (MUST)
- **R10a** Each medallion MUST be a link with the variety's plain name as accessible name and a "Vraag aan" action that opens the request form with that variety pre-selected; no drawn line MAY cross a label or medallion at any width from 1100 to 1920 px (collision probes at zero). (MUST)
- **R10b** Below 1100 px the hero MUST show the six varieties as a readable list (the `final.html` trunk-and-twig layout unless the radial prototype proves itself at 390 px). (MUST)
- **R11** Below the opening, the homepage MUST tell the story in this order, as in `final.html`: delivery region, the range, growing, the four audiences, the grower, the ProefBox request form. Each scene MUST be reachable by normal scrolling and keyboard. (MUST)
- **R12** With reduced motion enabled, or without JavaScript, the homepage MUST render the same content as a static, readable page with the network shown fully grown. (MUST)

### Range and products
- **R13** The overview page MUST list every variety marked as in the range, with photo, name and taste words, each linking to its product page. (MUST)
- **R14** Every product page MUST use one template with these sections in order: hero, introduction with characteristics, flavour profile, "van kwekerij tot keuken" timeline, the grower block, kitchen uses, who it suits, product information (packaging, availability, delivery or pick-up), storage, the other varieties, closing. (MUST)
- **R15** Each product page SHOULD take its accent colour from the variety while keeping the site's base palette dominant. (SHOULD)
- **R16** The product page "Bestel" action MUST open the request form with that variety pre-selected. (MUST)
- **R17** A variety removed from the range (one change in the data source) MUST disappear from every listing, cross-sell and form option, and its URL MUST forward to the overview page (on static hosting: a noindex page with meta refresh and a canonical to `/zwammen`). (MUST)

### Audiences
- **R18** Each audience page MUST lead with the problem that audience has, state what GroMush offers them, and end in its own primary action: Chefs → ProefBox; Grootkeukens → "Bespreek jouw behoefte"; Speciaalzaken → intake form; Thuis & MushLove → order for pick-up, follow on social channels, or adopt a bucket. (MUST)
- **R19** The Grootkeukens page MUST state plainly that GroMush is in a start-up phase and cannot yet guarantee large volumes, as long as the start-up flag in the data source is on. (MUST)
- **R20** The Grootkeukens page SHOULD offer a short needs helper (meals per day, mushroom frequency, varieties, town) whose answers prefill the needs form. It MUST NOT display a calculated kilogram figure, price or formula. (SHOULD)
- **R21** The Speciaalzaken page MUST NOT promise a free trial delivery. (MUST)
- **R42** Home-cook orders MUST be presented as pick-up requests: the form and its confirmation say that Anthony confirms the order, the pick-up moment and the place personally, that harvest days vary, and that payment is by transfer or cash at pick-up. No address, schedule or pack price is shown. (MUST)

### Process, story and adoption
- **R22** The Kweekproces page MUST present the four indoor phases (pasteurisation, layering in 20L buckets, incubation, fruiting) and the harvest and delivery step, using real farm photography where it exists. (MUST)
- **R23** Outdoor growing MUST be presented as a plan, never as existing: no page may describe the food forest, logs, outdoor harvests or log sets as existing, available, adoptable or bookable, and no page names a start month or harvest date (Q17). The only timing allowed is "gepland voor 2027". (MUST)
- **R24** The adoption page MUST let a visitor request a bucket adoption by form, with no price (Q4). It MUST NOT offer log sets; it MAY link to the Buitenkweek interest registration. (MUST)
- **R25** The Ons verhaal page MUST tell Anthony's story in his own voice, with the real photos he supplied (family, cameraman, grower). (MUST)
- **R43** The Buitenkweek page MUST be a short plan page in the `final.html` design system, in this order: hero ("buitenkweek op boomstammen, gepland voor 2027"), "Wat is een voedselbos?" as a general explanation (not "ons voedselbos"), how log growing works in six steps (written as method, illustrated, no photo presented as GroMush's), the future-species row (R45), and a closing interest registration ("Hou me op de hoogte"). It MUST NOT carry the brief's log-ownership section or six-benefit bar. Its copy MUST pass R2 and R23. (MUST)
- **R45** The future-species row MUST show the 8 species (morieltje, shiitake, paarse ridderzwam, judasoor, wijnrode stropharia, reishi, nameko, pioppino) as non-clickable items, each marked "binnenkort" with one neutral line (no health or availability claim), and MUST be removable or hideable with a single change in the data source, leaving no gap or orphan heading. (MUST)

### Inspiration
- **R26** The inspiration page MUST present the two cooking methods and a recipe collection, where each recipe opens in an accessible dialog with ingredients, steps, servings and the variety used, linking to that variety's page. (MUST)
- **R27** The recipe collection MUST show however many recipes are in the data source, with no fixed count (4 at launch). (MUST)

### Local pages
- **R28** Each delivery town MUST have a landing page with its own H1, title, meta description, local hero image, sub-areas served, the four audiences and the ProefBox call to action. (MUST)
- **R29** A Leveringsregio hub MUST show all delivery towns on a stylised region map (not an embedded map service) and link to each town page. (MUST)
- **R30** Town pages MUST present towns as delivery regions, not as GroMush locations. Only "Westkapelle" may be named as the place GroMush grows. (MUST)

### Conversion and forms
- **R31** The ProefBox request MUST collect name, business name, business type, email, delivery town, optional phone, varieties of interest and a message, and MUST state that the box is free and for professionals in the delivery region. (MUST)
- **R32** The general contact form MUST offer a reason selector (chef/restaurant, grootkeuken, speciaalzaak, bestelling thuis (afhalen), adoptie emmer, interesse buitenkweek, school of vereniging, samenwerking, andere), pre-selected when the visitor arrives from an audience, product or adoption link. (MUST)
- **R33** Every form MUST validate inline and, when valid, open the visitor's mail app with a `mailto:` to info@gromush.be whose subject names the form and whose body lists every field in readable Dutch ("Naam: …"). The page MUST then say plainly that the request is only sent once they send that mail, and MUST show the address info@gromush.be and the phone/WhatsApp number as the alternative if no mail app opens. It MUST NOT claim the request was received. Without JavaScript the form MUST still work through the native `action="mailto:…"` with `enctype="text/plain"`. (MUST)
- **R34** Every form MUST include a privacy line linking to the privacy policy, and MUST NOT show a visual puzzle. (Spam protection is not needed: nothing is sent by the site itself.) (MUST)
- **R35** The ProefBox promo MUST appear at most once per session, never on first page view, never on the ProefBox or contact page, and MUST close with a button, Escape or a click outside, and remember the dismissal. (MUST)

### Maintainability
- **R36** Content repeated across pages (varieties and their fields, towns, contact details, social links, form recipient, the claims flags of R2 and R19, the future-species toggle of R45) MUST live in one source in the repo, so that one change updates every page; the published output MUST be plain static HTML, CSS and JS. (MUST)
- **R37** Every content image MUST be served in responsive sizes (srcset) in a modern format with a fallback, with explicit width and height and Dutch alt text. (MUST)

### Quality
- **R38** Every page MUST meet WCAG 2.2 AA, including 44×44 px targets, reflow at 200 % text, and no horizontal overflow from 320 to 1440 px. (MUST)
- **R39** Every page MUST score at least 90 for Performance, Accessibility, Best Practices and SEO in Lighthouse mobile, with LCP under 2.5 s and CLS under 0.1 on a throttled 4G profile. (MUST)
- **R40** Every page MUST have a unique title and meta description, Open Graph tags, a canonical URL, and appear in the XML sitemap. Structured data MUST be limited to facts in the content (Organization, Product without price, Recipe; LocalBusiness only with locality, no street address). (MUST)
- **R41** The site MUST set no cookies and make no third-party requests: no analytics, no social embeds, no form service, fonts and scripts self-hosted. (MUST)
- **R44** Every image that shows something that does not exist (see "Imagery flagged for replacement") SHOULD be replaced before launch, and MUST NOT be used where it is the evidence for a claim about something that does not exist (for example a food-forest photo as proof that GroMush has one). Illustrated delivery (the van in the delivery section) is accepted (Q20). (SHOULD / MUST)

## Acceptance criteria

- **AC1 (R1)** Given any published page, when its rendered HTML is searched case-sensitively, then "Gromush", "GRO MUSH" and "GroMUSH" do not occur outside unedited user input.
- **AC2 (R2)** Given the "certified organic" flag is off, when every page is rendered, then none contains "biologisch", "bio-", "ecologisch" or "gecertificeerd".
- **AC3 (R2)** Given the flag is turned on and the site rebuilt, when the pages render, then organic wording may appear where the content holds it.
- **AC3a (R2a)** Given the Grootkeukens, Chefs and Speciaalzaken pages, when they are searched, then "superfood" and health benefit claims do not appear.
- **AC4 (R3)** Given any page, when it renders, then no price, currency sign, discount percentage or "vanaf" figure appears.
- **AC5 (R3)** Given the phone number is removed from the data source, when the footer and contact page render, then no phone or WhatsApp link appears.
- **AC6 (R4, R36)** Given the yellow oyster's taste words are changed once in the data source, when the homepage, overview, the Chefs page and the cross-sell on the pink oyster page render, then all show the new words.
- **AC7 (R5)** Given every page, when it is searched, then "Chef Box" and "ChefBox" never label the free offer.
- **AC8 (R6)** Given any two pages, when their primary navigations are compared, then items, order and the call to action are identical.
- **AC9 (R7)** Given the sitemap, when a crawler starts at the homepage, then every listed page is found within two clicks.
- **AC10 (R10)** Given a 1440 px visitor on the homepage, when the page loads and they scroll, then hyphae grow from the centre and each of the six medallions resolves as its branch arrives.
- **AC10a (R10a)** Given widths 1100, 1280, 1440, 1680 and 1920, when the collision probes run before and after the full reveal, then they report zero line-over-label and zero line-over-medallion hits.
- **AC10b (R10a)** Given a screen-reader user, when they reach the hero, then each medallion is announced by its plain variety name, not by the curved-letter fragments.
- **AC10c (R10b)** Given a 390 px and a 320 px visitor, when the hero renders, then all six varieties are readable and actionable without horizontal scroll.
- **AC11 (R11)** Given a keyboard-only visitor, when they press Tab and Page Down from the top of the homepage, then they reach every scene and every link in story order.
- **AC12 (R12)** Given "prefers-reduced-motion: reduce", when the homepage loads, then no scroll-linked animation runs and every scene's text and links are visible.
- **AC13 (R12)** Given JavaScript is disabled, when the homepage loads, then all text, images and links are present and the network is drawn fully grown.
- **AC14 (R13, R17)** Given the grey oyster is removed from the range in the data source, when the overview, homepage, the product cross-sells and the request form render, then the grey oyster appears in none of them.
- **AC15 (R17)** Given the same removal, when `/zwammen/grijze-oesterzwam` is requested, then it is a noindex page that forwards to `/zwammen` and declares it canonical, and it is absent from the XML sitemap.
- **AC16 (R14)** Given any two product pages, when their section order is compared, then it matches R14.
- **AC17 (R16)** Given the blue oyster page, when the visitor activates "Bestel", then the request form opens with "Blauwe oesterzwam" selected.
- **AC18 (R18)** Given each audience page, when it renders, then its primary action matches R18 and appears in the hero and the closing section.
- **AC19 (R19)** Given the start-up flag is on, when the Grootkeukens page renders, then the start-up statement appears above the needs helper.
- **AC20 (R20)** Given the visitor completes the needs helper, when the form opens, then it is prefilled with their answers and no kilogram figure or price is shown.
- **AC21 (R21)** Given the Speciaalzaken page, when it is searched, then "gratis" and "proeflevering" do not appear.
- **AC22 (R23)** Given every page, when it is searched, then outdoor growing appears only as a plan ("gepland voor 2027"), and no copy says "ons voedselbos", names a month, a harvest or a log set, or offers adoption or ownership of logs.
- **AC23 (R24)** Given the adoption page, when it renders, then the bucket request form is available, no price is shown, and no log set is offered.
- **AC24 (R26)** Given a recipe card, when the visitor activates it, then a dialog opens with focus inside it. When they press Escape, then it closes and focus returns to the card.
- **AC25 (R27)** Given the data source holds 4 recipes, when the page renders, then exactly 4 cards show with no empty slots.
- **AC26 (R28)** Given each town page, when its head is inspected, then the title, meta description and H1 are unique to that town.
- **AC27 (R30)** Given the Brugge page, when it is searched, then it does not say GroMush is located or grows in Brugge.
- **AC28 (R31, R33)** Given a valid ProefBox request, when it is submitted, then a `mailto:info@gromush.be` URL is opened whose subject names the ProefBox and whose body contains every filled-in field, and the page shows the "verstuur de mail om af te ronden" note with the email address and phone/WhatsApp.
- **AC28a (R33)** Given JavaScript is disabled, when a valid request is submitted, then the browser hands the form to the mail app through the native `mailto:` action.
- **AC29 (R33)** Given any page with a form, when it renders, then the email address and phone/WhatsApp are visible next to the form, and no copy says the request "is ontvangen" or "is verstuurd".
- **AC30 (R33)** Given a submission without an email address, when it is submitted, then the field is flagged inline and nothing is sent.
- **AC31 (R32)** Given the visitor clicks "Bespreek jouw behoefte" on the Grootkeukens page, when the contact form loads, then "Grootkeuken" is selected.
- **AC32 (R34)** Given every form, when it renders, then it has a privacy line linking to `/privacy/` and no captcha or puzzle.
- **AC33 (R35)** Given a first-time visitor, when they load their first page, then no promo appears. When they dismiss the promo on a later page, then it does not reappear that session.
- **AC34 (R36)** Given the build output, when it is inspected, then it is plain HTML, CSS and JS that GitHub Pages serves as-is, and every repeated field in it matches the single data source.
- **AC35 (R38)** Given each page template, when it is tested with axe, the 44 px target sweep, 200 % text at 320 px, and a manual keyboard and screen-reader pass, then there are no WCAG 2.2 AA failures.
- **AC36 (R39)** Given the homepage, a product page and a town page, when Lighthouse mobile runs, then every category scores at least 90, LCP is under 2.5 s and CLS is under 0.1.
- **AC37 (R41)** Given any page, when it loads with an empty cache or a form is submitted, then no cookie is set and no network request leaves the site's own origin.
- **AC38 (R42)** Given a home cook submits an order request, when the mail body and the on-page note are generated, then both say Anthony confirms the pick-up personally, and neither contains an address or price.
- **AC39 (R43)** Given the Buitenkweek page, when it renders, then its sections appear in R43's order, it has no ownership section or benefit bar, its closing action opens the interest registration, and AC2 and AC22 pass on it.
- **AC41 (R45)** Given the future-species toggle is switched off in the data source, when the Buitenkweek page is rebuilt, then the row and its heading are gone, no empty space or broken anchor remains, and nothing else changes.
- **AC42 (R45)** Given the row is shown, when a visitor clicks or tabs through it, then no item is a link or focus stop, and each item reads "binnenkort".
- **AC40 (R44)** Given the launch checklist, when the image register is reviewed, then every flagged image is either replaced or approved in writing by Anthony, and none is used as the evidence for a claim.

## Constraints

- **Language:** Dutch (Belgium), addressed as "je/jouw" throughout. The flyer's "u" is not used.
- **Accessibility:** WCAG 2.2 AA (R38); the European Accessibility Act applies to a commercial site.
- **Privacy:** GDPR. Form data never touches the site: the visitor's own mail app sends it to info@gromush.be. No processor, no cookies, so no consent banner (R41). Privacy and cookie policies are drafted by us as placeholders and replaced once the final texts exist (Q22).
- **Organic terms:** "biologisch", "bio" and "ecologisch" are protected by EU Regulation 2018/848 for products and their production; GroMush's certification is in progress (Q6), so R2 applies until the certificate exists.
- **Performance:** R39 budgets. The hero animation must not block first paint, and the mycelium is drawn by code (seeded generator, static paths for no-JS), not a video.
- **Budget and maintenance:** Anthony has no budget. The site is static files, maintained by Michael with AI; no paid or third-party services.
- **Honesty and imagery:** all supplied images may be used for now (Q11), but no fabricated testimonials, phone numbers or certifications, and images that show things that do not exist are flagged for replacement (R44).
- **Hosting:** GitHub Pages (`michtio.github.io/gromush-site`), so every link and asset path MUST work under the `/gromush-site/` sub-path as well as at a domain root later. gromush.be (TransIP parking page, mail on Google Workspace) is out of scope (Q21).
- **Old site:** the old static site in the repo root is not built on and not deleted without Michael's approval; where the new build is published from is a plan decision.

## Open questions

All answered; each answer is a requirement, a non-goal or a decisions-log row.

- [x] **Q1** Grey oyster is sold.
- [x] **Q2** Italiaanse = zomeroesterzwam; name "Italiaanse oesterzwam".
- [x] **Q3** ProefBox (free) and ChefBox (paid).
- [x] **Q4** No prices on the site.
- [x] **Q5** Outdoor growing is a plan (refined by Q17).
- [x] **Q6** Not certified organic yet.
- [x] **Q7** Phone, WhatsApp, Westkapelle; GroMush and MushLove Facebook pages both real (R9).
- [x] **Q8** Home cooks pick up; address communicated later.
- [x] **Q9** Nothing is bookable yet.
- [x] **Q10** Corrected taste set below adopted; Anthony may edit (one change in the data source).
- [x] **Q11** All supplied images may be used for now.
- [x] **Q12** Sitemap approved (closes inventory site questions 1–6).
- [x] **Q13** Static HTML, CSS and JS; no CMS.
- [x] **Q14** No CRM; plain emails through a form.
- [x] **Q15** No analytics, no embeds.
- [x] **Q16** Future species in, removable with one change (R45).
- [x] **Q17** Forest plot does not exist; outdoor growing is a plan, nothing is promised (R23, R43).
- [x] **Q18** Hero recommendation approved.
- [x] **Q19** Hero actions: the slip with both actions under the centred title; "Ontdek onze oesterzwammen" dropped.
- [x] **Q20** Delivery variant 1 (route with the van) chosen; the van is an illustration.
- [x] **Q21** GitHub Pages only; launch is a separate PRD.
- [x] **Q22** We draft privacy and cookie policies as placeholders.
- [x] **Q23** Work from the Buitenkweek PDF as it is.
- [x] **Q24** "ProefBox".

Left for `plan.md` (how, not what): the mechanism for R36's single data source, and where the build is published from without deleting the old site.

### Q10: canonical taste lines

Corrected against the known culinary character of each species; the briefs' words were partly wrong (golden oyster called "vlezig", pink "zacht", Italiaanse "intens"). Two facts matter to chefs and are now stated: pink and blue lose most of their colour when cooked. Anthony may adjust to how his own harvest tastes.

| Variety | Latin | Three taste words (cards, buttons) | One sentence (product page, overview) |
|---|---|---|---|
| Gele | *Pleurotus citrinopileatus* | Nootachtig · fruitig · delicaat | Licht nootachtig met een fruitige geur; dun en teer, dus kort en heet bakken. |
| Roze | *Pleurotus djamor* | Hartig · houtig · stevig | Hartig en licht houtig, krokant gebakken met een spekachtige toets; steviger van beet dan andere oesterzwammen, en bij het bakken verbleekt het roze naar goudbruin. |
| Witte | *Pleurotus ostreatus* | Mild · zacht · veelzijdig | Mild en zacht van smaak, mals van structuur: een rustige basis voor sauzen, pasta en risotto. |
| Blauwe | *P. ostreatus* var. *columbinus* | Hartig · aards · vlezig | Hartig en licht aards, vlezig en stevig; de blauwe tint verkleurt naar grijs in de pan. |
| Italiaanse | *Pleurotus pulmonarius* | Mild · licht zoet · mals | Mild en licht zoet, met een nootachtige toets en dunne, malse hoeden. |
| Grijze | *Pleurotus ostreatus* | Hartig · umami · stevig | De klassieker: hartig met een ronde umami, stevig en vlezig van beet. |

The homepage cards in `final.html` still carry the old words and are updated in the build.

## Buitenkweek (2026-11 brief): what stays and what goes

The plot does not exist today. The page explains the plan and collects interest; it promises nothing to buyers or would-be log owners (Q17).

| Brief section | Decision |
|---|---|
| Hero "Puur natuur, biologisch en regeneratief", intro, four icons | Kept as hero, reworded: "Puur natuur, langzaam en regeneratief" with "Buitenkweek op boomstammen, gepland voor 2027". No "biologisch" (R2), no "100% natuurlijk", no icons that state facts about a forest that does not exist. |
| "Wat is een voedselbos?" | Kept as a general explanation of the concept ("een voedselbos is…"), never "ons voedselbos". "Meer over ons voedselbos" button dropped. |
| "Ons biologische kweekproces", six steps | Kept as "Zo werkt kweken op boomstammen": method, not report. "biologische boomstammen" becomes "gezonde hardhouten stammen", "biologisch broed" becomes "broed". Illustrated in the site's ink style; no photo presented as GroMush's. |
| EXTRA BLOK: 8 future species | Kept as R45, non-clickable, "binnenkort", one neutral line each (no health claim for reishi), removable with one change. |
| "Word eigenaar van jouw eigen boomstammen", "investeren", "Ontdek de formules", GRO-001…004 labels | Dropped. Would read as an offer, and with "meerdere jaren productief" as a return on investment. |
| Six-benefit bar | Dropped: every item is a promise about a product that does not exist. |
| Closing CTA | Kept as "De natuur groeit op haar eigen tempo." with "Hou me op de hoogte" (interest registration, reason "interesse buitenkweek"). |
| Page-specific footer | Dropped; one global footer (R6, R9). |
| Look: dark green, moss, Cormorant/Inter, dark overlay hero | Translated into `final.html`: straw and ink, Young Serif, Work Sans, Kaushan for the one handwritten note, grid paper and tape; the closing CTA as a taped grid-paper note. |
| Photography | `hero-buitenkweek.jpeg` and `voedselbos.jpeg` not used (AI images of a forest that does not exist; the hero is also botanically wrong). The five numbered jpgs are third-party screenshots, not used. The 8 species images from the Extra Blok zip are used in the row. |

## Content dependencies (block launch, not PRD approval)

- **ProefBox photo:** the supplied box has "ChefBox" burned into it, so it cannot illustrate the free ProefBox (R5). Needs another image.
- **Grijze photo:** reuses the Italiaanse cut-out until Anthony sends a real one.
- **La Réserve (Knokke):** the hotel photo is not used without written permission.
- **Buitenkweek:** the 8 future-species lines (we draft, Anthony checks); illustrations for the six steps.
- **Recipes:** 4 at launch; 2 more later.
- **Flavour scores (Smaak, Textuur, Aardsheid, Geur, 1–5) per variety:** set by us from culinary knowledge, relative within the range and consistent with the Q10 taste table; Anthony confirms or corrects them.

### Imagery flagged for replacement (R44)

AI-generated images that show things that do not exist. Usable for now (Q11), replaced or approved in writing before launch.

| Image (in `_resources/2026-10-mails-anthony/`) | Shows something that does not exist |
|---|---|
| `…/GroMush-Proefbox-ChefBox-selectie-….png/.webp` (Chef, Inspiratie, Push, product folders) | Wooden crate branded "GroMush ChefBox" |
| `Adoptie…/Gemini_Generated_Image_a8emp…`, `…pn5s2…`, `…y2ill…` | Buckets labelled "EMMER-0xx" in a forest; logs with GroMush tags "Batch #24" |
| `Communitypagina…/Gemini_Generated_Image_uixqe8…` | White GroMush-branded bucket with lion's mane |
| `Communitypagina…/Gemini_Generated_Image_xx3whk…` | Engraved board "MushLove community by GroMush" |
| `Communitypagina…/_drive/Schermafbeelding 2026-10-13 om 10.00.48.png` | School group at the "GroMush voedselbos" (does not exist until 2027) |
| `Communitypagina…/Ontdek,beleef,proef.zip` (workshops, Bezoek voedselbos) | Workshops and food-forest visits (not bookable, forest not active) |
| `Onze zwammen…/Buitenkwekerij-gromush-…voedselbos….png`, `Buitenkweek…/hero-buitenkweek.jpeg`, `voedselbos.jpeg` | The GroMush food forest and log cultivation |
| `Onze zwammen…/Paddenstoelen-Zwammen-kwekerij-GroMush-…png` | Shiitake and lion's mane as part of the current range |
| `…/Overdracht van een krat verse paddenstoelen.png` (all town pages, Contact) | An AI hand-over scene presented as a GroMush delivery (not viewed in this pass; flagged from the inventory) |
| `Binnenkwekerij-zeecontainer-gromush-…png` | Purple-lit grow corridor (AI-styled version of the real container) |
| `over-ons…/file_000000003ac88210ac140c76f615d911.png` | Anthony with a crate in the grow room (AI-styled) |

AI images of people who are not real (chef with tweezers, large-kitchen chef, greengrocer, MushLove community in the forest) are also on this list where they stand for real customers.

## Decisions log

| Date | Decision | Ruled by |
|---|---|---|
| 2026-10-19 | Start from Anthony's October briefs only; ignore the previous site and its design. | Michael |
| 2026-10-19 | Proposed: no checkout; ordering and adoption are requests that Anthony confirms (from the Onze zwammen brief "maak hiervan geen winkelwagen" and the absence of a payment provider). Pending confirmation in Q8. | Proposed by Claude |
| 2026-10-19 | Proposed: consolidate the eight navigation variants in the briefs into one (see `sitemap.md`). | Proposed by Claude |
| 2026-10-19 | Proposed: testimonials and cases dropped until real quotes exist (several briefs forbid invented ones). | Proposed by Claude |
| 2026-10-19 | Professionals and home cooks are equal primary buyers; the site is commercial and must sell the mushrooms (not a documentary). | Michael |
| 2026-10-19 | Ordering is a request that Anthony confirms; no checkout (settles the ordering half of Q8; pick-up/delivery for home cooks still open). | Michael |
| 2026-10-19 | Stack open: static HTML prototypes now, production stack decided in plan.md. | Michael |
| 2026-10-19 | Visual direction round (Impeccable, seed 2c06b3cc): "Mycelium order map" leads; Marktkraam, Zwammenkaarten and Kweekpatroon are built as full alternate prototypes in `.impeccable/prototypes/directions/`. | Michael |
| 2026-10-19 | Prototypes built by Vibe workers before PRD approval, at Michael's explicit request (exception to the approved-spec rule for design exploration only). | Michael |
| 2026-10-19 | Q1: the grey oyster (grijze oesterzwam) is sold; it is a full variety on the site, not "nog te bevestigen". | Michael (for Anthony) |
| 2026-10-19 | Q2: Italiaanse oesterzwam and zomeroesterzwam are the same species (*P. pulmonarius*); the site uses "Italiaanse oesterzwam" because it sells better. | Michael (for Anthony) |
| 2026-10-19 | Q3: "ProefBox" is the free tasting order; "ChefBox" is the paid order or subscription. "Chef Box" as a name for the free box is dropped. | Michael (for Anthony) |
| 2026-10-19 | Q4: no prices, discounts, tiers or adoption prices on the site; every pricing question routes to contact (keeps negotiating room). | Michael (for Anthony) |
| 2026-10-19 | Q5: outdoor growing (food forest, logs) starts January 2027; until then it is presented as coming, never as active. | Michael (for Anthony) |
| 2026-10-19 | Q6: not certified organic yet; certification is in progress. No "biologisch" or "gecertificeerd" claim until the certificate exists. | Michael (for Anthony) |
| 2026-10-19 | Q7 (part): phone 0499 24 23 59 may be published, also as WhatsApp. Location shown as "Westkapelle" only, no street address. Facebook page still to be defined. | Michael (for Anthony) |
| 2026-10-19 | Q8: home cooks pick up only, at the home address (communicated later, not on the site). Harvest days vary; pack quantities are not fixed yet because the packaging order is still pending. | Michael (for Anthony) |
| 2026-10-19 | Q9: nothing is bookable yet (workshops, visits, tastings, school sessions, kweeksets); keep as a future feature, not on the launch site. | Michael (for Anthony) |
| 2026-10-19 | Q11: all supplied images may be used for now; selection and positioning are refined later. | Michael (for Anthony) |
| 2026-10-19 | Extra species (Black Pearl, koningsoesterzwam, pruikzwam, shiitake): sold later; not on the launch site. | Michael (for Anthony) |
| 2026-10-19 | Product "Bestel" buttons open the request form with that variety pre-selected. | Michael (for Anthony) |
| 2026-10-19 | No online payment for now: orders are paid by bank transfer or cash, on or before pick-up; adoption by bank transfer. Adoption is a request, confirmed by Anthony. | Michael (for Anthony) |
| 2026-10-19 | The 8 future outdoor species ("Extra Blok") are not on the launch site. | Michael (for Anthony) |
| 2026-10-19 | Buitenkweek PDF (truncated at section 12) will be resent by Anthony. | Michael (for Anthony) |
| 2026-10-19 | Health and "superfood" language is allowed on consumer (B2C) pages; professional pages, grootkeuken above all, stay factual (efficiency, reliability, volume, food safety). | Michael (for Anthony) |
| 2026-10-19 | No testimonials or cases section at launch (none exist yet). | Michael (for Anthony) |
| 2026-10-19 | Inspiratie launches with the 4 supplied recipes; 2 more follow later (being developed and tested). | Michael (for Anthony) |
| 2026-10-19 | Homepage CTA "Ontdek ons verhaal" links to Over ons (`/ons-verhaal`); "Word onderdeel van het netwerk" links to the community (`/voor-wie/thuis`). | Michael (for Anthony) |
| 2026-10-19 | The colour mushroom logo is the master logo. Approved taglines: "Ambachtelijk gekweekt", "Puur van hier", "Lokaal is lekkerder", "Lokaal. Ambachtelijk. Buitengewoon." | Michael (for Anthony) |
| 2026-10-19 | All form submissions go to info@gromush.be. | Michael (for Anthony) |
| 2026-10-19 | Final homepage prototype is a merge (`final.html`): hero A (slip note on D's grid paper with B's tape and Kaushan Script), varieties C's flip cards (lighter backs, colour-filled stat squares), kweken B's taped polaroids with A's in-photo step badge, outdoor CTA as a taped grid-paper note, "Voor elke tafel" D's grid with coupon cut-out, kweker A, form D, footer A. One type system: Young Serif, Work Sans, Kaushan Script for handwriting, Courier Prime inside the cards. Delivery-area section: three new variants to choose from, one with an electric van on scroll. | Michael |
| 2026-11-03 | Anthony approved the final homepage prototype ("De homepage zag er geweldig uit"). He asks that the hero's mycelium block take the radial structure of his reference (six round variety medallions with curved labels around a centred title, dense branching hyphae between them), at least on desktop. Reference: `_resources/2026-11-mails-anthony/Schermafbeelding 2026-10-26 om 11.03.22.png`. | Anthony, via Michael |
| 2026-11-03 | Buitenkweek brief resent in full (`_resources/2026-11-mails-anthony/Buitenkweek-pagina-website-gromush.pdf`); the earlier truncated PDF is superseded. | Anthony |
| 2026-11-03 | Correction to the row above: the 2026-11-03 PDF is byte-identical to the October one (same MD5, 16 pages) and still ends in section 12. Nothing was superseded; see Q23. | Claude (checked) |
| 2026-11-03 | R2 widened to all EU 2018/848 terms; R2a added to reflect the B2C health-language decision; R3, R20 and R24 aligned with Q4 (no prices); R9 with Q7 (phone, WhatsApp, Westkapelle); R10 split into R10/R10a/R10b for the radial hero; R23 and AC22 aligned with Q5 (January 2027); R42 (home-cook pick-up, Q8), R43 (Buitenkweek structure) and R44 (imagery register) added. Pending Michael's approval of the PRD. | Proposed by Claude |
| 2026-11-03 | Q7: both Facebook pages are real (checked): `61590322125848` is "GroMush", `61594707453474` is "MushLove \| Knokke-Heist". Footer links GroMush; Thuis & MushLove also links MushLove. | Michael (checked by Claude) |
| 2026-11-03 | Q10: corrected taste set adopted (see table); Anthony may edit. | Michael |
| 2026-11-03 | Q12: sitemap approved. | Michael |
| 2026-11-03 | Q13: static HTML, CSS and JS, maintained with AI; no CMS (Anthony has no budget). Overrules the earlier Craft proposal. R36 becomes a single data source in the repo. | Michael |
| 2026-11-03 | Q14: no CRM; forms send plain email via a form service; submissions are not stored. | Michael |
| 2026-11-03 | Q15: no analytics and no embeds for now; therefore no cookies and no consent banner (R41). | Michael |
| 2026-11-03 | Q16: the 8 future outdoor species go in as a non-clickable "binnenkort" row, removable with one change (R45). Reverses the 2026-10-19 row. | Michael |
| 2026-11-03 | Q17: the forest plot does not exist. Outdoor growing is a plan ("gepland voor 2027", no month); no ownership, formulas, benefits or forest imagery. Refines Q5. | Michael |
| 2026-11-03 | Q18, Q19: radial hero recommendation approved; hero keeps the slip with both actions, "Ontdek onze oesterzwammen" dropped. Prototype variant in `final.html` first. | Michael |
| 2026-11-03 | Q20: delivery variant 1 (route with the van) chosen; the van is an illustration and stays. | Michael |
| 2026-11-03 | Q21: GitHub Pages only for now; launch on gromush.be is a separate PRD. | Michael |
| 2026-11-03 | Q22: we draft privacy and cookie policies as placeholders. | Michael |
| 2026-11-03 | Q23: work from the Buitenkweek PDF as it is. | Michael |
| 2026-11-03 | Q24: "ProefBox" (header CTA "Gratis ProefBox"). | Michael |
| 2026-11-03 | Forms are plain HTML with no form service: on submit the visitor's mail app opens with a pre-filled `mailto:` to info@gromush.be (native `mailto:` action without JS). R33 rewritten; R33a dropped (no confirmation email possible); R34 reduced to the privacy line; no processor in the privacy policy. Trade-off accepted: a request only arrives if the visitor actually sends the mail, and visitors without a mail app use the shown address or WhatsApp. | Michael |
| 2026-11-03 | Page URLs carry a trailing slash (`/zwammen/`, `/zwammen/gele-oesterzwam/`): one folder per page, works on GitHub Pages without server config (plan AD5). | Michael (plan approval) |
| 2026-11-03 | Pre-selection by query parameter (`?soort=`, `?reden=`) works only with JavaScript on; without JS the form shows unselected and stays fully usable (plan AD10). | Michael (plan approval) |
| 2026-11-03 | Plan approved; build starts with S1. | Michael |
| 2026-11-03 | Flavour scores per variety: the prototype values were placeholders. Rewritten from culinary knowledge on a scale relative within the range (gele 3/2/2/3, roze 4/4/3/5, witte 2/3/2/2, blauwe 4/5/4/4, grijze 4/4/3/3, italiaanse 3/3/2/2, as Smaak/Textuur/Aardsheid/Intensiteit); to be checked with Anthony. | Michael (Claude drafts) |
| 2026-11-03 | Flavour axes: "Intensiteit" replaced by "Geur" (aroma), because it overlapped with "Smaak"; "Beet" was rejected as it overlaps with "Textuur". Axes now mean: Smaak = how pronounced the flavour is, Textuur = how firm and meaty, Aardsheid = earthy and woody notes, Geur = how strong the aroma is. Scores revised (Smaak/Textuur/Aardsheid/Geur): gele 3/2/2/4, roze 5/4/3/3, witte 2/3/2/2, blauwe 4/5/4/3, grijze 4/4/3/2, italiaanse 3/3/2/2. Supersedes the scores in the row above; to be checked with Anthony. | Michael |
| 2026-11-03 | Italiaanse taste sentence no longer compares with the grijze ("Milder en lichter dan de grijze…"), so it stays true if the grijze leaves the range (R17): now "Mild en licht zoet, met een nootachtige toets en dunne, malse hoeden." | Claude, under Michael's Q10 mandate ("make it correct") |
| 2026-11-03 | R2a narrowed by law: even on consumer pages, nutrition and health claims follow EU Regulation 1924/2006 (only authorised claims, under their conditions; "superfood" and "vol eiwitten, vitaminen en mineralen" are not allowed without them). Ons verhaal: "een natuurlijke krachtpatser vol eiwitten, vitaminen en mineralen. Een plantaardig superfood met ongelooflijke voordelen." replaced by "…en raakte er niet meer van los." (paddenstoelen are also not plantaardig). To confirm with Michael. | Claude (proposed) |
| 2026-11-03 | The grow-room image `fase4-kweekruimte` is AI-generated but art-directed by Anthony; approved for use. | Michael |
| 2026-11-04 | S9a closed: the round-4 radial hero in `final.html` (softened hyphae, probes zero at 1100–1920) is approved; S9 (homepage) may start. | Michael ("continue building, focus on homepage first") |
| 2026-11-05 | All AI-styled images art-directed by Anthony are approved for use (Q11 stands: supplied images may be used); `anthony-krat` is the homepage grower photo, as in `final.html`. Builders do not swap supplied images on their own judgement. | Michael |
| 2026-11-05 | S16 gate: the AC23 grep for "49" matched the phone number (0499…, required by AC29); the gate now uses word boundaries and strips the phone. | Claude (gate fix, no requirement change) |
| 2026-11-05 | Images: `anthony-krat` also in the Ons verhaal hero; the ChefBox-branded crate photo (`proefbox`) restored in the homepage ProefBox section as in `final.html`; Anthony's second Grootkeuken image (also shows species outside the range) used on Grootkeukens. | Michael |
| 2026-11-05 | ProefBox promo also off on /voor-wie/thuis/ (it addresses professionals). | Michael |
| 2026-11-05 | R21 applies to the page content (`<main>`); the header's "Gratis ProefBox" button and other site chrome are out of its scope. | Michael |
| 2026-11-05 | Instagram link on Thuis labelled "GroMush op Instagram" (no separate MushLove account). No consent checkbox on forms: requests rest on art. 6.1.b/6.1.f AVG, stated in the privacy line and policy; the Buitenkweek interest list rests on consent (art. 6.1.a), given by sending the mail, withdrawable by mail; privacy policy updated. | Michael |
| 2026-11-05 | Buitenkweek step 1 "gezonde hardhouten stammen" written as "Stevige stammen kiezen" (R2a lint); Anthony's original wording was "gezonde", to check with him. | Michael |
| 2026-11-05 | Thuis: the "klas, club of buurt" line removed (Q9: school sessions stay off the launch site). | Claude, under Q9 |
