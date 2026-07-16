# GroMush — gromush.be

Statische website voor GroMush, een ambachtelijke oesterzwammenkwekerij in
Knokke-Heist (levering in regio Knokke-Heist, Damme en Brugge).

**Live:** https://michtio.github.io/gromush-site/

## Stack

Bewust dependency-vrij: puur HTML, één CSS-bestand en een handvol vanilla JS.
Geen build-stap, geen frameworks — GitHub Pages serveert de repo as-is.
De site is zo opgezet dat hij later 1-op-1 naar een CMS (Craft) kan verhuizen:
componenten en tokens zijn gedocumenteerd op [`/design-system/`](design-system/index.html).

```
├── index.html              # Klant-keuze (homepage)
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
    ├── js/main.js          # Nav-toggle, scroll reveals, hero-fade
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
