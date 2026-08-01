# GroMush — gromush.be

Statische website voor GroMush, een ambachtelijke oesterzwammenkwekerij in
Knokke-Heist (levering in regio Knokke-Heist, Damme en Brugge).

**Live:** https://michtio.github.io/gromush-site/

## Stack

Puur HTML, CSS en vanilla JS; geen build-stap, geen frameworks — GitHub Pages
serveert de repo as-is. Enige uitzonderingen: de homepage-scrollytelling
draait op een zelf gehost GSAP + ScrollTrigger (`assets/vendor/gsap/`, enkel
geladen op `/` en `/index-b/`) en een handvol Font Awesome Free-iconen
(`assets/vendor/fontawesome/`, CC BY 4.0, inline gebruikt). Geen CDN's,
dus GDPR-proof.
De site is zo opgezet dat hij later 1-op-1 naar een CMS (Craft) kan verhuizen:
componenten en tokens zijn gedocumenteerd op [`/design-system/`](design-system/index.html).

```
├── index.html              # Homepage: scrollytelling "van spore tot bord" (kopijdeck A)
├── index-b/                # Zelfde verhaal, uitgesproken speelse kopij (deck B, noindex)
│                           #   → regenereren via _resources/build-variant-b.py
├── index-v1/               # Archief: eerste iteratie van de story-homepage (noindex)
├── restaurant/             # Subpagina per klantprofiel
├── grootkeuken/
├── particulier/
├── oesterzwammen/          # Soortenoverzicht
├── chefbox/                # Gratis proefbox voor professionele keukens
├── bestel/                 # Bestellen: stappen + praktisch (accordeons)
├── contact/
├── privacy/                # GDPR-verklaring (geen cookies, geen tracking)
├── design-system/          # Interne stijlgids (noindex)
├── 404.html
├── sitemap.xml / robots.txt
└── assets/
    ├── css/main.css        # Design tokens + componenten
    ├── css/story.css       # Homepage-scenes (scrollytelling), fallback-first
    ├── js/main.js          # Nav-toggle, scroll reveals, hero-fade
    ├── js/story.js         # GSAP-scenes homepage (reduced-motion gate, pins ≥48rem)
    ├── vendor/gsap/        # GSAP + ScrollTrigger, zelf gehost (zie README aldaar)
    ├── fonts/              # Self-hosted Epilogue (variabel) + Old Standard TT
    └── img/                # Geoptimaliseerde webp's + responsive varianten + SVG-logo's
```

## Lokaal bekijken

```sh
python3 -m http.server 8765
# → http://localhost:8765
```

## Design

- **Kleuren:** cream `#fdf8ee`, groen `#334727`, goud `#9b8843`, zand `#d0bf7c`,
  schaduw `#353535` (buiten, rechtsonder).
- **Typografie:** Epilogue (titels & tekst), Old Standard TT (serif-accenten).
  Self-hosted woff2 (GDPR: geen Google Fonts CDN).
- **Logo:** `assets/img/logo.svg` (lockup), `logo-badge.svg` (cirkel),
  `logo-mark.svg` (beeldmerk), `favicon.svg`.
- **Motion:** hero fade-in/-out, side reveals, zoom-out hovers; alles achter
  `prefers-reduced-motion`.
- **Homepage-scrollytelling:** negen scenes van spore tot bord, in deze volgorde:
  `hero` (foto-hero met gedokte ticker + golf boven de fold) → `kweek`
  (binnen- én buitenkweek) → `varieties` (parade van zeven oesterzwammen) →
  `proces` (van stro tot bord in gewone taal, plus de compacte founder-noot) →
  `route` (leverronde met polaroid per halte) → `plate` → `beleef`
  (interactieve belevingskaart op het mycelium-netwerk: zes knooppunt-knoppen
  openen elk hun kaart) → `eigenaar` → `router`. Hoofdstuknummers 1 tot 6 lopen
  van `kweek` tot `beleef`; de twee afsluiters blijven ongenummerd.
  Contract: de CSS-standaardtoestand is de áfgewerkte pagina; JS spoelt enkel
  terug en scrubt vooruit, en pint alleen vanaf 48rem via `gsap.matchMedia`.
  Geen JS, reduced motion en mobiel krijgen automatisch een complete statische
  versie: de belevingskaart wordt dan een gewoon kaartenraster met alle zes
  belevingen. Twee kopijdecks: `/` (warm vakmanschap) en `/index-b/`
  (uitgesproken speels, noindex, gegenereerd met
  `python3 _resources/build-variant-b.py`). `/index-v1/` is het archief van de
  eerste iteratie en gebruikt nog de scenes `underground` en `farm`; die CSS en
  JS blijven daarom bestaan.

Volledige referentie: [`/design-system/`](design-system/index.html).

## SEO / performance / a11y

- Per pagina: title, description, canonical, Open Graph, `LocalBusiness` +
  `BreadcrumbList` JSON-LD; handmatige `sitemap.xml` + `robots.txt`.
- Webp's met `srcset` (800w-varianten), width/height-attributen, lazy loading
  buiten de viewport, gepreloade fonts.
- Skip-link, landmark-semantiek, zichtbare focus, AA-contrast (hoverkleuren van
  de briefing zijn daarvoor licht bijgestuurd — zie design system).

## Open punten

- **Foto's koning oesterzwam & pruikzwam** ontbreken; die tegels tonen een
  placeholder-illustratie (`/oesterzwammen/`).
- **Social links** (Facebook/Instagram/YouTube): URL's nog niet gekend, dus
  bewust weggelaten uit de footer. Toevoegen in de footer van elke pagina +
  `sameAs` in de JSON-LD op de homepage.
- **Prijzen** staan op "op aanvraag" tot de tarieven vastliggen.
- **Online boeken** (cal.com-embed in het origineel) is vervangen door
  WhatsApp/telefoon/mail-CTA's: statisch, sneller en GDPR-vriendelijker.
- **Eigen domein:** bij verhuis naar gromush.be een `CNAME`-bestand toevoegen
  en de absolute URL's in canonicals/sitemap/JSON-LD aanpassen.

De originele screenshots en bronbeelden staan lokaal in `_resources/`
(gitignored, enkel referentiemateriaal).
