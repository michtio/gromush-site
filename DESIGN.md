---
name: GroMush
description: "Ambachtelijk gekweekt. Van kwekerij tot bord. Paper laid out on the grower's table: an ink mycelium on straw, taped notes on grid paper, polaroids, cards and coupons."
colors:
  ink: "#2c2318"
  ink-soft: "#5a4a36"
  straw: "#ece2c8"
  straw-deep: "#e0d3b2"
  grid-paper: "#efe2c2"
  paper-card: "#f5ecd6"
  card: "#f6f1e6"
  polaroid: "#f8f4ea"
  kraft: "#c9a878"
  kraft-tint: "#e6d6b3"
  moss: "#4d5a2c"
  form-red: "#a3291f"
  form-red-deep: "#86211a"
  van: "#56702f"
  gele: "#d9a91f"
  roze: "#d9776a"
  witte: "#e8dcc0"
  blauwe: "#5f7890"
  italiaanse: "#b0703f"
  grijze: "#8a8478"
  witte-edge: "#d8ccb0"
  pill-blauwe: "#8fa3b5"
  pill-italiaanse: "#c08a5e"
  pill-grijze: "#a9a296"
  tint-gele: "#e6c35a"
  tint-roze: "#e39a8f"
  tint-witte: "#f1e7d2"
  tint-blauwe: "#8ea3b8"
  tint-italiaanse: "#c98e5f"
  tint-grijze: "#a9a296"
  pip-witte: "#b8a372"
typography:
  display:
    fontFamily: "Young Serif, Georgia, serif"
    fontSize: "clamp(3rem, 6vw, 5.75rem)"
    fontWeight: 400
    lineHeight: 1.02
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Young Serif, Georgia, serif"
    fontSize: "clamp(2.1rem, 4vw, 3.25rem)"
    fontWeight: 400
    lineHeight: 1.12
    letterSpacing: "-0.01em"
  statement:
    fontFamily: "Young Serif, Georgia, serif"
    fontSize: "clamp(1.6rem, 3.2vw, 2.6rem)"
    fontWeight: 400
    lineHeight: 1.25
  title:
    fontFamily: "Young Serif, Georgia, serif"
    fontSize: "clamp(1.45rem, 2.2vw, 1.85rem)"
    fontWeight: 400
    lineHeight: 1.12
    letterSpacing: "-0.01em"
  node-name:
    fontFamily: "Young Serif, Georgia, serif"
    fontSize: "clamp(0.95rem, 2.36cqi, 1.3rem)"
    fontWeight: 400
    lineHeight: 1.15
  card-band:
    fontFamily: "Young Serif, Georgia, serif"
    fontSize: "0.9rem"
    fontWeight: 400
    lineHeight: 1.25
    letterSpacing: "0.03em"
  body:
    fontFamily: "Work Sans, Segoe UI, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.65
  lede:
    fontFamily: "Work Sans, Segoe UI, sans-serif"
    fontSize: "1.12rem"
    fontWeight: 400
    lineHeight: 1.65
  body-sm:
    fontFamily: "Work Sans, Segoe UI, sans-serif"
    fontSize: "0.9rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Work Sans, Segoe UI, sans-serif"
    fontSize: "0.95rem"
    fontWeight: 600
    lineHeight: 1.4
  pill:
    fontFamily: "Work Sans, Segoe UI, sans-serif"
    fontSize: "0.8rem"
    fontWeight: 600
    lineHeight: 1.4
  hand:
    fontFamily: "Kaushan Script, Segoe Script, Brush Script MT, cursive"
    fontSize: "1.15rem"
    fontWeight: 400
    lineHeight: 1.3
  mono:
    fontFamily: "Courier Prime, Courier New, ui-monospace, monospace"
    fontSize: "0.75rem"
    fontWeight: 700
    lineHeight: 1.4
rounded:
  pill: "999px"
  card: "14px"
  photo: "12px"
  menu: "10px"
  plate: "8px"
  field: "4px"
  polaroid: "3px"
spacing:
  gutter: "clamp(1.1rem, 4vw, 4rem)"
  section: "clamp(3.5rem, 7vw, 5.5rem)"
  grid-step: "24px"
  container: "1440px"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.straw}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "0.85rem 1.4rem"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "0.85rem 1.4rem"
  button-secondary-hover:
    backgroundColor: "{colors.straw-deep}"
  button-cta-header:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.straw}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "0.62rem 1.25rem"
  pill-vraag-aan:
    backgroundColor: "{colors.gele}"
    textColor: "{colors.ink}"
    typography: "{typography.pill}"
    rounded: "{rounded.pill}"
    padding: "0.32rem 0.9rem"
  button-submit:
    backgroundColor: "{colors.form-red}"
    textColor: "{colors.straw}"
    rounded: "{rounded.field}"
    padding: "0.62em 1.15em"
  button-submit-hover:
    backgroundColor: "{colors.form-red-deep}"
  input:
    backgroundColor: "{colors.paper-card}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.field}"
    padding: "0.5em 0.7em"
    height: "2.75rem"
  chip:
    backgroundColor: "{colors.paper-card}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.field}"
    padding: "0.4rem 0.85rem 0.4rem 0.45rem"
  slip:
    backgroundColor: "{colors.grid-paper}"
    textColor: "{colors.ink}"
    padding: "2.6rem 1.5rem 1.6rem"
  flip-card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    width: "17.5rem"
    height: "26rem"
  flip-card-request:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.card}"
    rounded: "{rounded.plate}"
  polaroid:
    backgroundColor: "{colors.polaroid}"
    textColor: "{colors.ink}"
    rounded: "{rounded.polaroid}"
    padding: "10px 10px 16px"
  coupon:
    backgroundColor: "{colors.paper-card}"
    textColor: "{colors.ink}"
    padding: "clamp(1.25rem, 2.5vw, 1.75rem)"
  menu-button:
    backgroundColor: "{colors.straw}"
    textColor: "{colors.ink}"
    rounded: "{rounded.menu}"
    width: "44px"
    height: "44px"
  footer:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.straw}"
---

# Design System: GroMush

## Overview

**Creative North Star: "The Grower's Table"**

Everything on the site is paper laid out on Anthony's worktable. The ground is straw paper with a faint horizontal fibre grain; on it, an ink mycelium grows out of one point and reaches every variety. Around it lie the things a grower and his customers handle: a taped order slip on grid paper with a handwritten note, polaroids of the four growing phases taped to the page, collectible variety cards that flip to show their stats, a coupon cut out along a dashed line, and an order form on grid paper with a red stamp of a submit button. Each object has its own stock and its own small tilt, so the page reads as a table, not as a screen.

The network is the one drawn thing. It opens the homepage, becomes the delivery route a small van drives from Westkapelle to the towns, and returns as phase lines and rails. Colour is held back for the mushrooms: the six variety colours appear only on a variety's own card border, pill, chip or hover tint, which is why a mostly brown-on-cream page feels full of colour. Hand lettering (Kaushan Script) is the grower's marker on the paper: notes, batch numbers, step numerals, the signature.

The objects carry honesty, too. A request always sits on paper, never in a floating box. Things that do not exist yet are written as plans, never drawn as if they did.

**Key Characteristics:**
- Straw paper ground with fibre grain; ink for type, rules and every drawn line; no neutral greys, no pure black or white.
- One drawn line (hand-wobbled cubic curves, round caps) for the hero network, the delivery route, phase lines and the mobile trunk.
- Paper objects with their own stock and tilt: grid-paper slip with tape, polaroids, flip cards, dashed-edge coupons.
- Colour rationed to the six varieties; moss only for links and focus; red only in the form.
- Four type voices with strict jobs: Young Serif names, Work Sans informs, Kaushan Script annotates, Courier Prime numbers the cards.

## Colors

A warm paper-and-ink palette, a few paper stocks, and six variety colours held in reserve for the mushrooms.

### Primary
- **Loam Ink** (ink): the voice of the system. All text, every border and rule, every hypha and route line, primary action fills, the selection highlight and the footer ground. 11.96:1 on straw.

### Secondary
- **Moss** (moss): the interactive signal that is not a button. Text links (underlined, offset 0.22em) and the 3px focus ring. Never a fill.
- **Stamp Red** (form-red) and **Deep Stamp Red** (form-red-deep): the order form only. The submit button, the checked chip border, the checked mode letter, invalid-field borders and error text. Nowhere else on the page.

### Tertiary: the varieties
Each variety owns one colour. They are product colours, not brand accents.
- **Citrine Yellow** (gele), **Coral Pink** (roze), **Cream White** (witte), **Slate Blue** (blauwe), **Toasted Amber** (italiaanse), **Ash Grey** (grijze): flip-card borders, hover tints of a variety's hypha, product accents.
- **Pill tints** (pill-blauwe, pill-italiaanse, pill-grijze): the "Vraag aan" pill fill where ink on the true colour falls below 4.5:1.
- **Card tints** (tint-*): chip faces, stat pips and the faint wash on a flip card's back. **Witte Edge** (witte-edge) and **Witte Pip** (pip-witte) stand in for witte where cream on cream would vanish.

### Neutral
- **Straw** (straw): the page ground, the knock-out behind labels in drawings, field hover.
- **Deep Straw** (straw-deep): the one alternate band (the delivery region section) and the outline-button hover.
- **Faded Ink** (ink-soft): secondary copy, taste lines, Latin names, hand notes, captions. 6.6:1 on straw.
- **Grid Paper** (grid-paper) with a 24px ink grid at 7% (grid-step): the slip, the outdoor note, the "Voor elke tafel" band and the request section.
- **Paper Card** (paper-card): coupons, form fields, mode chips, the success note.
- **Card Stock** (card): the flip cards. **Polaroid Stock** (polaroid): the phase photos.
- **Kraft** (kraft): masking tape (at 90%) and the footer baseline. **Kraft Tint** (kraft-tint): the current-step marker on the delivery legend.
- **Van Green** (van): the van's lower body only; deliberately not moss, which stays interactive.

### Named Rules
**The Rationed Colour Rule.** A variety's colour appears only on that variety's own card, pill, chip, product accent or (on hover/focus) its own hypha. Never on a heading, a section ground, a link or a generic button.

**The Ink Action Rule.** Every primary action is ink with straw text. The single exception is the form's submit, which is Stamp Red with a 2px ink border.

**The Red Stays in the Form Rule.** Stamp Red lives inside the request form: submit, checked states, errors. Seeing red anywhere else means something is wrong.

**The Contrast Tint Rule.** When ink text on a variety colour falls below 4.5:1, the pill takes a lighter tint of that hue; witte gets a 1.5px inset ink ring instead.

## Typography

**Display Font:** Young Serif (with Georgia, serif)
**Body Font:** Work Sans (with Segoe UI, sans-serif)
**Hand Font:** Kaushan Script (with Segoe Script, Brush Script MT, cursive)
**Card Font:** Courier Prime (with Courier New, ui-monospace, monospace)

**Character:** Young Serif is soft, round-bracketed and a little old-fashioned, like a grocer's sign painted with care; Work Sans keeps information plain and warm; Kaushan Script is a quick marker note on the paper; Courier Prime is the typed number on a collector's card.

### Hierarchy
- **Display** (400, clamp(3rem, 6vw, 5.75rem), 1.02, -0.02em): "Van kwekerij tot bord" only.
- **Headline** (400, clamp(2.1rem, 4vw, 3.25rem), 1.12): section headings, max ~20ch.
- **Statement** (400, clamp(1.6rem, 3.2vw, 2.6rem), 1.25): one closing thought per section, max 26ch.
- **Title** (400, clamp(1.45rem, 2.2vw, 1.85rem)): block headings (audience coupons, the outdoor note, delivery legend at 1.4rem).
- **Node name** (400, clamp(0.95rem, 2.36cqi, 1.3rem)): variety names in the network, sized in container units so the drawing scales as one piece.
- **Card band** (400, 0.9rem, uppercase, 0.03em): the variety name on a flip card's ink band.
- **Body** (400, 1.0625rem, 1.65): running copy, max 68ch. **Lede** at 1.12rem in faded ink, max 60ch.
- **Label** (600, 0.95rem): form labels, legends, buttons (0.95–1rem).
- **Pill** (600, 0.8rem): "Vraag aan".
- **Hand** (Kaushan 400, 0.9–1.75rem): slip note, batch marks, step numerals in polaroids, the Westkapelle origin, section taglines, the signature.
- **Mono** (Courier Prime 700, 0.75rem): card numbers and stat labels, inside flip cards only.

### Named Rules
**The Four Voices Rule.** Young Serif names things, Work Sans informs and acts, Kaushan Script annotates, Courier Prime numbers cards. Kaushan never sets a heading, a button or a paragraph; Courier Prime never leaves the cards.

**The Single Weight Display Rule.** Young Serif is used only at 400; hierarchy comes from size. Headings use `text-wrap: balance`, paragraphs `pretty`.

## Layout

One centred container (1440px max) with a fluid gutter (clamp(1.1rem, 4vw, 4rem)). Sections breathe at clamp(3.5rem, 7vw, 5.5rem). The header is sticky, transparent at the top, and takes a straw ground with a 1px ink rule once the page scrolls.

**The opening.** At 1280px and up, a 34/66 split: display line, support line and slip on the left, the network on the right, at full small-viewport height. The network is a fixed 900×700 drawing with nodes in percentages and sizes in `cqi`, so lines, cut-outs and labels scale together. 1100–1279px stacks the headline beside the slip with the network below. At 1099px and below the network becomes a vertical trunk list: one wobbling ink trunk down the left, each variety a row joined by a short twig. (A radial desktop variant is being prototyped; see the PRD, R10.)

**The delivery band.** Deep-straw ground. With motion allowed and a tall enough screen, the map is sticky while the route draws from Westkapelle and the van drives it; each town's card appears as the van arrives, beside a sticky three-step legend at 1280px and up. Without motion it is a static map with the van parked at Westkapelle and the town register beside or under it.

**Grids.** Flip cards: three columns from 61.25em with a staggered tilt (-2°, +1.5° and 28px lower, -1°), two columns from 56.25em, a horizontal snap scroller below 40em. Polaroids: four across, two below 1100px, one (max 22rem) below 600px. Coupons: two columns with full-width rows that pair text and photo 1:1.4, one column at 768px. Form: 3:2 form and photo, fields in two columns, one column at 768px.

**Breakpoints in use:** 480, 600, 640, 700, 768, 900 (menu), 1100 (network), 1280.

**The One Piece Rule.** Above 1100px a drawing scales as one piece; nodes never reflow independently. Below it, the drawing is re-expressed (trunk, register), never shrunk until unreadable.

**The Knock-Out Rule.** Text inside a drawing gets a straw plate or a 1px straw halo so no line runs through a letter. Collision probes stay at zero.

## Elevation & Depth

Paper on a table. Depth comes from physical objects: each carries a soft, low contact shadow and a slight tilt, and tape strips cast their own small shadow. The page itself is flat, with a fixed fibre-grain overlay at 14% opacity. UI chrome (header, nav, fields, links) stays flat.

### Shadow Vocabulary
- **Cut-out rest** (`filter: drop-shadow(0 6px 10px rgb(44 35 24 / .28))`): free-standing mushroom cut-outs on the network. Lifts to `0 12px 14px / .34` on hover.
- **Plate** (`filter: drop-shadow(0 8px 10px rgb(44 35 24 / .2))`): cut-outs inside cards.
- **Card** (`box-shadow: 0 18px 30px -18px rgb(44 35 24 / .45), 0 2px 4px rgb(44 35 24 / .12)`): flip cards.
- **Polaroid** (`box-shadow: 0 14px 30px rgb(44 35 24 / .18)`): phase photos.
- **Slip** (`box-shadow: 0 14px 26px -18px rgb(44 35 24 / .45)`): the order slip; the outdoor note uses `0 18px 32px -20px / .45`.
- **Tape** (`box-shadow: 0 2px 5px rgb(44 35 24 / .15)`): masking tape strips.
- **Lift** (`box-shadow: 0 12px 24px -12px rgb(44 35 24 / .45)`): hover on medallions and town cards.

### Named Rules
**The Objects Cast Rule.** Only paper objects and photographed things cast shadows: cut-outs, cards, polaroids, slips, tape. Buttons, fields, the header and section bands are flat and defined by ink rules.

**The Small Tilt Rule.** Objects tilt between -2° and +2° (notes up to -3°, tape ±38°). Text inside a tilted object stays horizontal relative to its object and never drops below AA.

## Shapes

Lines are drawn, edges are ruled, paper is cut. Every connecting line is a cubic Bézier with a seeded hand wobble and round caps; long rails use non-scaling strokes. Network strokes vary (main branches 1.6–2.4, a thicker base taper, filaments 0.8 at 75%). The network is generated deterministically (seeded), so the scripted and script-free pages draw the same lines.

Corner families: full pills for every action and the "Vraag aan" pill; 14px cards with an inner 1px ink keyline at 7px; 12px photos; 8px label plates and card buttons; 4px fields, chips and the submit; 3px polaroids; square paper for the slip, the outdoor note and coupons. Circles mark places and steps: town medallions, step numerals on polaroids (36px, straw, 1px ink), audience letters (2.1rem, 1.5px ink), delivery legend icons (48px).

**The Cut Line Rule.** A 2px dashed ink edge means "cut here": coupons, the form's variety fieldset, the proefbox photo frame, the scissors line above the form. Coupon corners carry dashed crop marks. Dashed is never decoration.

**The Real Cut-Out Rule.** A mushroom standing free on the paper is always a real cut-out asset, never a geometric mask. Round ink-ringed medallions are framed photos.

## Components

### Buttons
Calm, solid and round: an ink pebble.
- **Shape:** full pill (999px).
- **Primary:** ink fill, straw text, 600, 1px ink border, 0.85rem 1.4rem on the slip; 0.62rem 1.25rem for the header CTA.
- **Hover / Focus:** opacity to 0.9 over 0.25s; 3px moss focus ring at 3px offset (straw inside the footer).
- **Secondary:** transparent with ink border and ink text; hover fills deep straw.
- **Submit:** Stamp Red, straw text, 2px ink border, 4px radius, 1.2rem 600; hover Deep Stamp Red; disabled 0.75 opacity with a wait cursor.
- **Text links:** moss, underlined at 0.22em; action links (`link-action`) are ink, 1.5px underline thickening to 2.5px on hover, with a 44px hit area.

### Order slip
- Grid paper, 1px ink border, square corners, rotated -1.5°, max 430px, two kraft tape strips at the top corners (±38°), a Kaushan note top-right rotated -3° ("gratis, voor zaken"). Holds the primary and secondary pills stacked full-width.

### Variety flip card (signature)
- 17.5×26rem (15×25rem on small screens) card stock with a 10px border in the variety colour, 14px radius, inner ink keyline, card shadow.
- **Front:** Courier Prime number, the cut-out filling the card, an ink name band (Young Serif uppercase on card stock), taste words beneath.
- **Back:** card stock washed with 14% of the variety tint; name, italic Latin name, a stats table in Courier Prime with square pips filled in the tint, a one-line headline, packs and availability, and an ink "Vraag aan" request button pinned to the bottom.
- **Behaviour:** a "Draai de kaart" button under each card flips it (0.6s rotateY). Reduced motion turns the flip into a cross-fade; without JS both sides stand one under the other.

### Polaroids
- Polaroid stock, 10px frame with a 16px bottom, 3px radius, alternating ±1.8° tilt, a tape strip, a 36px straw step numeral in Kaushan inside the photo's top-left, an optional smaller second photo pinned top-right with a 5px frame, and a two-line caption (bold step, faded detail). A faint ink phase line runs behind the row on desktop.

### Coupon
- Paper-card ground inside a 2px dashed ink cut line, dashed crop marks on opposite corners, a round audience letter beside the title, photos in a dashed frame with scissors on the top edge.

### Inputs / Fields
- **Style:** paper-card fill, 1.5px ink border, 4px radius, min-height 2.75rem; labels 600 above. Hover fills straw.
- **Focus:** the 3px moss ring (chips use a 3px ink ring).
- **Error:** 2px Stamp Red border and a red 600 message below, wired by aria-describedby; a form-level error box with a 2px red border offers the email address.
- **Mode chips (Zaak / Particulier):** dashed 1.5px ink boxes with a round letter; checked turns the border solid red and fills the letter red.
- **Variety chips:** the same construction filled with the variety tint; checked shows a red tick in place of the letter.
- **Privacy line:** a 1.5rem checkbox with red accent colour and a 44px hit area on the link.

### Navigation
- Logo left (44px), five Work Sans 500 ink links centred with underline on hover and focus, ink pill CTA right ("Gratis ProefBox"). Transparent at the top; straw with a 1px ink rule once scrolled. Below 900px a 44px outlined menu button (10px radius) opens a straw panel with a 1px ink rule; without JS the links wrap under the logo.

### Network node
- A link holding the cut-out, a straw label plate (8px radius) with the name in Young Serif, the taste words and the "Vraag aan" pill. Branches draw from Westkapelle on a short intro then with scroll; nodes fade in from 0.92 scale; hover or focus lifts the cut-out 4px and tints its branch with the variety colour at stroke 3. Reduced motion and no-JS show the network fully grown.

### Delivery route
- A drawn coast, dunes, polder lines and waterways at 12–32% ink; the route in ink; town cards (128px round photo, Young Serif name, sub-areas, arrow) placed on the map; a small illustrated van (Van Green lower body) that drives the route with scroll; a compass rose and a Kaushan "zee". A three-step legend with 48px round icons tracks progress.

### Footer
- The only ink ground: Young Serif wordmark, the kraft baseline, straw links hovering to kraft, 44px link targets, a straw focus ring, legal links under a 30% straw rule.

## Do's and Don'ts

### Do:
- **Do** put every request on paper: the taped grid-paper slip, the grid-paper form with a red submit, or an ink request button on a card.
- **Do** draw every connecting line in ink as a seeded, wobbled cubic curve with round caps, and keep drawn text knocked out (collision probes at zero).
- **Do** keep each variety's colour on that variety only, using its pill tint when ink text would fall below 4.5:1.
- **Do** give paper objects a small tilt and a soft contact shadow, and keep the text in them at AA.
- **Do** use a 2px dashed ink edge only for things you could cut out.
- **Do** honour reduced motion: smooth scroll off, the network fully drawn, the flip a cross-fade, the van parked at Westkapelle.

### Don't:
- **Don't** fill a heading, section band, link or generic button with a variety colour, and don't use Stamp Red outside the form.
- **Don't** give buttons, fields, the header or section bands a shadow; only paper objects and photographed things cast.
- **Don't** set headings, buttons or paragraphs in Kaushan Script, use Courier Prime outside the cards, or bold Young Serif.
- **Don't** use neutral grey for borders or text; rules are ink, secondary text is faded ink (Ash Grey belongs to the grijze variety).
- **Don't** approximate a mushroom's contour with a geometric mask; use a real cut-out.
- **Don't** add the dark-green, moss-button, gold-glow look from the page briefs; the system is ink on straw.
