# GroMush website: content inventory from Anthony's 27 briefing emails (Oct 2026)

Source: `/Users/michtio/dev/gromush-site/_resources/2026-10-mails-anthony/` (27 folders, mails dated 11 to 14 Oct 2026, all from Anthony Watteeuw <info@gromush.be>).
Method: every `_mail.txt` read; all 25 PDF briefs text-extracted (`pdftotext` plus `pdftohtml -xml` to recover font colour), and every mockup page in the PDFs viewed. Zip archives were only listed, not extracted. All 27 PDFs/mails were readable; none were corrupt.

### How to read the briefs (important)

- The client says the **intended copy is in RED and italics**. In practice the red marking (font colour `#ee220c`) is used **only in 8 of the 25 PDFs**: Homepage, Chef, Gele oesterzwam, Blauwe oesterzwam, Grootkeuken, Onze zwammen, Binnenkweek, Community (partly). In those 8, red = copy, black = structure/notes. The homepage also uses **green bold** (`#1db100`) for one emphatic instruction (no scroll page, fullscreen fades).
- The **other 17 PDFs contain no red text at all**. In those, copy and instructions are mixed. Copy is usually the text in quotes or directly after a "Titel:" / "Tekst:" / "CTA:" label. Treat it as copy, but confirm with the client.
- Most briefs are clearly **AI-generated prompts addressed to "Claude"** ("Bouw nu de pagina…", "VISUELE ONTWERPBRIEFING VOOR CLAUDE", "PROMPT OM DIRECT TE KOPIËREN NAAR CLAUDE"). Each has an AI-generated **full-page mockup image** (usually page 1) as its "visual reference". The mockups often **disagree with the brief text**: different headlines, different pricing, invented phone numbers, testimonials, extra sections. These are listed per page and in section 3.
- Several mockups are reused. All 5 product PDFs (geel, roze, wit, grijs, Italiaans) contain the **same yellow-oyster mockup**; the blauwe PDF has no mockup. All 5 local landing PDFs contain the **same Knokke-Heist mockup**.
- Emails with an empty body (signature only): Adoptie, Buitenkweek, Communitypagina (one Drive link), Extra Blok Buitenkweek, Inspiratie, Speciaalwinkels, Over ons, Blankenberge, Grijze, Italiaanse. Emails with real instructions: Homepage, Chef, Gele (the template rule). The rest only list or embed images.

---

## 1. Business summary

**What GroMush is.** GroMush is an artisanal ("ambachtelijk gekweekt") oyster-mushroom farm run by **Anthony Watteeuw**: founder, grower, ex-cinematographer/cameraman with his own production company, father of 4, pescatarian. It is based in **Knokke-Heist (8300)**. The homepage names **Westkapelle** (a part of Knokke-Heist) as the network's central node, "Kweek & vertrekpunt". The indoor farm is in a converted **sea container** (asset filename `Binnenkwekerij-zeecontainer-…`). The business is small-scale and in a **start-up phase**. Grootkeuken FAQ, in red: "Momenteel zijn we in een opstartfase, waardoor grote volumes nog niet gegarandeerd zijn."

**Contact data found.**
- Email: info@gromush.be
- Website: www.gromush.be
- WhatsApp/phone: +32 499 24 23 59 (from the email signature link and the restaurant flyer "0499 24 23 59")
- Instagram: https://www.instagram.com/gromush.be/
- Facebook: **two different IDs**. The email signature uses `profile.php?id=61590322125848`. The Community brief uses `profile.php?id=61594707453474`, possibly a separate MushLove page.
- Mockups show **invented** phone numbers (+32 479 12 34 56, +32 472 45 67 89, +32 479 36 32 01). The briefs themselves forbid fictitious numbers.

**Core message.** "**Van kwekerij tot (uw) bord**". Supporting line: "GroMush produceert lokaal gekweekte oesterzwammen om mensen opnieuw te verbinden met hun voedsel." The brand stands for lokaal, ambachtelijk, vers, smaakvol, duurzaam, transparant, innovatief, verbindend. "Maar vooral: GroMush laat mensen deel worden van het verhaal achter hun voedsel."

**Central metaphor.** **Mycelium** = network. "één netwerk → verschillende paddenstoelen → verschillende mensen → één lokale voedselgemeenschap." It recurs across the whole site, but must stay subtle after the homepage.

### Products / varieties

Core range: **6 oyster mushrooms**, grown indoors. Latin names come from the Onze zwammen brief (red):

| Variety | Latin | Homepage taste words (red) | Product-page hero (copy) | Accent colour (product template) |
|---|---|---|---|---|
| Grijze oesterzwam | Pleurotus ostreatus | Zacht • aards • umami | "De klassieker. Puur van smaak." (alt: "Puur van smaak. Sterk in elke keuken.") | warm leigrijs / stone grey, taupe |
| Roze (zalm) oesterzwam | Pleurotus djamor | Zacht • sappig • subtiel | "Kleur met karakter. Smaak die blijft hangen." | gedempt oudroze / warm rosé |
| Witte oesterzwam | Pleurotus ostreatus | Mild • fris • delicaat | "Puur van smaak. Eindeloos veelzijdig." | warm ivoor / crème, zand/taupe |
| Gele oesterzwam | Pleurotus citrinopileatus | Fruitig • zoet • fris | "Fris van kleur. Vol van smaak." | warm geel / goud |
| Blauwe oesterzwam | P. ostreatus var. columbinus | Krachtig • peperig • rijk | "Karaktervol van kleur. Krachtig van smaak." | gedempt blauwgrijs / petrol |
| Italiaanse oesterzwam | Pleurotus pulmonarius | Intens • vlezig • rijk | "Warm van karakter. Verfijnd van smaak." (alt: "Karaktervol van kleur. Verfijnd op het bord.") | muted terracotta / warm clay |

- **Italiaanse = zomeroesterzwam.** The asset filename `zomeroesterzwam-italiaanse-oesterzwam-…` and the Latin name *P. pulmonarius* both point to the same species. The Speciaalwinkels brief lists "Zomeroesterzwam" instead of Italiaanse.
- **Grey oyster status is contradictory.** It is in the homepage nav, homepage hero, the grijze product page and others. But the **Community** and **Inspiratie** briefs say "de grijze oesterzwam maakt geen deel meer uit van het assortiment" and "VIJF SOORTEN". The **restaurant price flyer** also lists only 5 (wit, geel, roze, blauw, Italiaans).
- **Other species mentioned:**
  - Black Pearl oesterzwam appears in mockups for the homepage block 3 (replacing Italiaans), Chef and Onze zwammen.
  - Koningsoesterzwam (*P. eryngii*) appears in the Chef/Onze zwammen/Grootkeuken mockups and the Speciaalwinkels list.
  - Pruikzwam / Lion's Mane (*Hericium*) appears in mockups, the Speciaalwinkels list, the buitenkweek logs and the Onze zwammen hero.
  - Shiitake is outdoor-grown on logs (Onze zwammen, Buitenkweek, Speciaalwinkels).
- **Future outdoor species**, from the "Extra Blok" zip: morieltje (morel), shiitake, paarse ridderzwam, judasoor, wijnrode stropharia (tuinreus), reishi, nameko, pioppino ("Piopino").
- A `girolle` (chanterelle) photo is in the Adoptie folder. No brief text mentions it.

### Growing methods

- **Binnenkweek (indoor), current.** Straw substrate in **20L buckets** in a climate-controlled grow room / container. The 4 phases:
  1. Pasteurisatie met koud water: straw in onion bags soaked 24h in cold water, drained 24h.
  2. Opbouw in lagen in 20L-emmers: alternating straw and spawn ("broed").
  3. Incubatie: about 2 weeks. The infopanel says "Ongeveer 2-3 weken", 20–24°C as guide value, dark, ventilated.
  4. Fruiting: temperature per species, high humidity, light, fresh air. "85–95%" only if accurate. Purple grow light.
  Then: Oogst & levering. The homepage USPs are "Klimaat gestuurd / Optimale luchtvochtigheid / Jaarrond productie".
- **Buitenkweek (outdoor).** Hardwood logs in a "beschermd biologisch **voedselbos**" (food forest). 6 steps: selection of organic logs → inoculeren (drill + spawn) → seal with natural wax → incubatie → vruchtvorming → oogsten. Tagline: "**Puur natuur, biologisch en regeneratief**".
  - **Status is contradictory.** The Onze zwammen brief insists outdoor growing is a **future project**: "Voorjaar 2027: start", "Voorjaar 2028: eerste oogst verwacht", never presented as active.
  - The Buitenkweek, Adoptie and Over ons briefs describe it as existing and sell log adoption.
  - The Binnenkweek brief also warns not to suggest all production already happens in a food forest.

### Service area

Knokke-Heist (home base), **Damme, Sluis (NL, Zeeuws-Vlaanderen), Brugge, Blankenberge** "en omgeving". Landing pages name sub-areas:
- Brugge: Sint-Andries, Sint-Kruis, Assebroek, Koolkerke, Dudzele, Male
- Damme: Oostkerke, Hoeke, Lapscheure, Moerkerke, Sijsele
- Blankenberge: Uitkerke, Zwankendamme, Lissewege, Wenduine/De Haan border

**Inconsistent town lists:**
- Over ons: "leveren in Knokke, Damme en Brugge".
- Grootkeuken hero: "Actief in Knokke-Heist · Sluis · Damme · Brugge".
- Chef animation: 4 towns, no Blankenberge.
- Contact: Knokke-Heist, Damme, Sluis, Brugge.

### Customer segments ("vier werelden")

1. **Chefs / restaurants.** Want taste, quality, special varieties, inspiration.
2. **Grootkeukens.** Hospitals, woonzorgcentra, schools, company restaurants, caterers, hotels, institutions. Want reliability, volume, food safety, logistics, price.
3. **Speciaalwinkels / speciaalzaken.** Bakers, greengrocers, butchers/traiteurs, cheese/deli, organic shops, horeca/lunch bars.
4. **Particulieren / community (MushLove).** Families, home cooks, plus schools, youth movements, associations and neighbourhood initiatives.

### Offers and conversion products

| Offer | Where | Details as stated |
|---|---|---|
| **Gratis Proefbox** (free tasting box) | Homepage block 7, Chef, Onze zwammen, Grootkeuken FAQ, Proefbox push brief | Free mixed box of varieties. "Beschikbaar voor professionele klanten in onze leveringsregio." CTA "Bestel je/jouw gratis proefbox". Homepage note: may link to info@gromush.be. |
| **Gratis Chef Box** | Contact, Inspiratie, all 5 landing pages | Presented as **free**, for chefs. Slug `/chef-box`. The Inspiratie mockup shows it as "3 seizoensrecepten, tips van onze chef…". Probably the same thing as the Proefbox, under a different name (see contradictions). |
| **ChefBox-abonnementen** (paid) | Chef page | **ChefBox Flexibel**: vanaf 1 kg, "Bestel wanneer u het nodig heeft", 1 or more varieties, weekly delivery, 10% korting vanaf 3kg, 20% vanaf 5kg. **ChefBox Select / Vaste levering** ("POPULAIR"): vanaf 1kg weekly, mix of 4 varieties, priority on special mushrooms, flexible, 15% vanaf 1kg / 20% vanaf 3kg / 30% vanaf 5kg. The brief says "drie abonnementskaarten" but only 2 are specified (section 12 missing). The mockup shows 3 different tiers: Basis 5kg/wk, Select 15kg/wk, Exclusief 25kg/wk. |
| **Leveringsformules grootkeuken** | Grootkeuken | **START**: vanaf 5kg/week, weekly, choice of varieties, flexible. **PROFESSIONEEL** (recommended): vanaf 10kg/week, mix, fixed delivery day, 10% korting. **PARTNER**: "Vanaf 10kg" (same threshold as Professioneel, likely an error), custom delivery, long-term, priority, 20% korting. Flagged as "voorbeelden voor het ontwerp". The mockup shows 25 kg / 75 kg / "op maat". |
| **Restaurant price list** (flyer `fromules restaurant.jpg`, real printed A5) | Chef folder | Losse bestelling: 1–3 kg €27,00/kg; 3–5 kg €24,30 (10%); >5 kg €21,60 (20%). Vaste wekelijkse levering: 1–3 kg €22,95 (15%); 3–5 kg €21,60 (20%); >5 kg €18,90 (30%). Minimum 1 kg, prices excl. btw. "Mix van 5 soorten" or "Apart per soort". **These discount tiers match the ChefBox Flex/Select text**, so the flyer is likely the real price source. |
| **Product packaging** | All product pages | 250 g / 500 g / 1 kg / larger on request. Availability "Volgens oogst en seizoen". Local delivery for horeca. Buttons "Bestel →" and "Vraag beschikbaarheid". |
| **Emmer-adoptie** | Adoptie, Community | "€ 49 / per cyclus": 20L bucket with your number, choice of oyster species, "1 volle oogst (ca. 2–3 kg)", updates, pick-up or delivery. The Community brief says not to show prices yet. |
| **Boomstammen-adoptie / eigenaar worden** | Adoptie, Buitenkweek, Over ons nav ("Word mede-eigenaar") | "€ 249 / per jaar", set of 4 inoculated logs, several species, multiple harvests per year, GroMush maintains. Labels such as GRO-001 Shiitake… GRO-004 Zomeroesterzwam. |
| **MushLove community** | Community + elsewhere | Free. Join via Facebook and Instagram. Follow the process, workshops and kooksessies, food-forest visits, order and pick up locally ("Bestel & haal af"), adopt a bucket, schools and associations. |
| **Workshops / rondleiding / proeverij / bezoek** | Community, Over ons ("Reserveer nu", "Kom langs & beleef") | No dates or prices. Do not invent any. |

**Ordering mechanics.** There is **no webshop or checkout**. The Onze zwammen brief: "Bestellen" goes to the contact form, "Maak hiervan geen winkelwagen". The Grootkeuken FAQ: "rechtstreeks via de kweker door email of whatsapp". Delivery is personal, by GroMush's own van ("Via onze bestelwagen…"), in "luchtdoorlatende kratten". Shelf life "Minimum een week". Storage "In de koelkast met een temperatuur van 4°C". Several mockups show cart and account icons. These should be dropped.

### Tone of voice

Warm, personal (Anthony's "ik"), premium-culinary, artisanal, natural, honest. "Not an aggressive webshop". Never "marktleider" or "beste van België". Briefs repeatedly ban unproven claims: biologisch/certified, health, guaranteed volumes, fake reviews. Customers are addressed as **"je/jouw"**. The flyer uses "u". Premium food brand, editorial/food-magazine feel.

### Recurring brand phrases (verbatim)

- Baselines:
  - "AMBACHTELIJK GEKWEEKT." (the official baseline per the Gele brief: "verzin geen nieuwe tagline")
  - "Puur van hier" (flyer logo)
  - "Puur natuurlijk lokaal genieten" (flyer)
  - "Lokaal. Ambachtelijk. Buitengewoon." (Over ons banner image)
  - "Lokaal is lekkerder." (Speciaalwinkels)
  - "Puur natuur. Eerlijke smaak." (Buitenkweek footer)
  - "Natuurlijk proces. Ambachtelijk gekweekt. Voor de beste smaak." (Binnenkweek footer)
- "Van kwekerij tot bord" / "Van kwekerij tot uw bord" / "Van onze kwekerij naar jouw bord." / "Van kwekerij tot keuken"
- "Lokaal gekweekt. Lokaal verbonden."
- "Een paddenstoel groeit niet alleen. Hij groeit dankzij zijn netwerk. GroMush doet hetzelfde."
- "Geen lange keten. Geen onnodige tussenstappen. Gewoon verse paddenstoelen, lokaal gekweekt."
- "Eén kwekerij. Verschillende behoeften."
- "Voor elke tafel een eigen verhaal."
- "Proef het verschil." / "Proef GroMush. Helemaal gratis." / "Eerst proeven. Dan samen groeien." / "Ontdek GroMush. Proef het zelf."
- "Klein beginnen. Lokaal groeien. Samen bouwen aan iets duurzaams."
- "Ik wil weten waar mijn eten vandaan komt."
- "Jullie zorgen voor duizenden maaltijden. Wij zorgen voor de paddenstoelen."
- "Meer dan paddenstoelen. Een lokale community."
- Sign-off "MushLove" in every email signature.
- Name rule (Gele brief): always "**GroMush**". Never Gromush, Gro Mush or GroMUSH. The briefs themselves violate this ("GRO MUSH", "GROmush", file names "gromuch").

---

## 2. Per page

Order: homepage → audience pages → product pages → process pages → local landing pages → community / adoption / about / contact / inspiration / other.

### 2.1 Homepage

Brief: `Homepagina - website - GroMush/_drive/Homepagina-website-gromush.pdf` (51 pp, red copy + mockups on pp. 4, 7, 14, 22, 33, 42, 48).
Email (verbatim intent): "**BELANGRIJK : de animatie voor het mycelium netwerk vindt je terug in de video!** Je krijgt hier ook enkele voorbeelden in foto's. **GRAAG OP DEZE MANIER AUB.**" The video is `Mycelium growth animation.mp4` (175 s, 640×360, a timelapse reference; not viewable here). The example photos are `Schermafbeelding 2026-08-13 om 23.46.25.png` (white radial hyphae on black, watermarked) and `…23.46.36.png` (black radial branching on white, a Google image result). Both are radial mycelium growth references.
URL: `/`.

**Global rules (green, emphasised).** "De homepage moet beginnen met leven! De homepage mag geen scrol pagina worden, de blokken moeten overgaan als een fullscreen synopsis verhaal, met fade in - fade out overgangs effecten. Uiteraard moet de bezoeker scrollen." So: full-screen scenes with fade transitions. No classic hero photo of a mushroom.

**Navigation (red).**
1. Voor wie? (A Voor chefs, B Voor grootkeukens, C Voor speciaalwinkels, D Voor particulieren)
2. Zwammen (A Gele, B Roze, C Blauwe, D Witte, E Grijze, F Italiaanse oesterzwam)
3. Over ons
4. Inspiratie
5. Contact

**Mycelium as site-wide metaphor.** Lines grow from the mycelium in four directions:
- CHEFS: Mycelium → paddenstoel → keuken → bord
- GROOTKEUKENS: Mycelium → productie → logistiek → grootkeuken → duizenden maaltijden
- SPECIAALWINKELS: Mycelium → paddenstoel → winkel → klant
- COMMUNITY: Mycelium → emmer → groei → oogst → persoon

**Block 1, Hero animation.**
- Full screen, green background. One small light point in the centre. On scroll, fine pearl-white hyphae grow and branch towards six points, accelerating with scroll.
- Title "**Van kwekerij tot bord**". Text "**Ambachtelijk gekweekte oesterzwammen, lokaal geproduceerd met respect voor natuur, mens en smaak.**" CTA "**Ontdek onze oesterzwammen**".
- 6 nodes become growth points. Circular photos of the 6 oysters appear one by one (grijs, wit, geel, roze/zalm, blauw, Italiaans), each linking to its product page. The network should "breathe and grow". Scrolling back zooms out slowly.
- Mockup p4: olive-green background, gold hyphae, 6 circular photos with curved labels, gold pill CTA, "tot bord" in gold italic.

**Block 2, "Lokaal gekweekt. Lokaal verbonden."** About 100–110vh, 40/60 split.
- Left: overline "LOKAAL GEKWEEKT. LOKAAL VERBONDEN." Serif headline "**Vanuit Knokke-Heist naar de hele streek.**" An animated line, then three text blocks:
  - "Gekweekt in Knokke-Heist": "GroMush kweekt ambachtelijke oesterzwammen lokaal in Knokke-Heist, dicht bij de mensen en keukens waarvoor ze bestemd zijn."
  - "Korte keten": "Door lokaal te kweken houden we de afstand tussen kweker, chef en consument klein. Minder kilometers, meer versheid en rechtstreeks contact."
  - "Een netwerk dat groeit": "Vanuit Knokke-Heist verbinden we ons met Damme, Sluis, Brugge, Blankenberge en de omliggende streek."
- Right: an **artistic organic region map**, not Google Maps. A faint coast/polder map of West-Vlaanderen and Zeeuws-Vlaanderen. Central node **01 Westkapelle** with the GroMush logo, "Kweek & vertrekpunt". Nodes:
  - 02 Knokke: "Chefs & lokale horeca"
  - 03 Sluis: "Horeca & streeknetwerk"
  - 04 Damme, 05 Brugge, 06 Blankenberge: each "Restaurants & speciaalzaken"
  - Round photo nodes "like fruiting bodies at the end of a hypha", with a soft shadow, not touristic.
- Animation sequence: centre point → hypha → branches → connections to Damme, Sluis, Brugge → photos → nodes glow → left text appears. Slow and organic, not technical.
- Three core values with line icons: "LOKAAL GEKWEEKT / Kweek in Knokke-Heist", "KORTE KETEN / Vers van kweker naar keuken", "DUURZAAM & RESPECTVOL / Voor natuur, mens en smaak".
- CTAs: "**ONTDEK ONS VERHAAL →**" (filled) and "**WORD ONDERDEEL VAN HET NETWERK →**" (outline). Targets are not specified.
- Closing line, large: "**Een paddenstoel groeit niet alleen. Hij groeit dankzij zijn netwerk. GroMush doet hetzelfde.**"
- Colours: warm off-white/cream, deep moss green, soft olive, earth tones, subtle gold. No bright green. No generic "eco" look.
- Mockup p7 differs: the text column says "Van Knokke-Heist naar de hele streek", adds a 4th USP "Gastronomische kwaliteit", and shows a **GroMush-branded electric van** in the foreground (VW ID Buzz style, "100% elektrisch").

**Block 3, Oesterzwammen (first product block).** 100vh, cream paper background, 38–40% text.
- Overline "OESTERZWAMMEN". Title "**Oesterzwammen van topkwaliteit.**" Intro "**Zes bijzondere oesterzwammen, elk met hun eigen kleur, textuur en karakter. Ambachtelijk gekweekt in Knokke-Heist, met aandacht voor kwaliteit, versheid en smaak.**" CTA "**ONTDEK ONS ASSORTIMENT →**".
- USPs: "AMBACHTELIJK GEKWEEKT / Met zorg en aandacht", "VERS & LOKAAL / Recht uit Knokke-Heist", "RESPECTVOL / Voor natuur, mens en smaak".
- Right: 6 round photos in a loose organic circle/hexagon, with taste words (see table in section 1). Centre text: "6 bijzondere soorten / Ambachtelijk gekweekt in Knokke-Heist". Very subtle beige/gold hyphae between photos.
- Scroll animation: text staggers in, then grijs → roze → wit → geel → blauw → Italiaans appear with SVG path-drawing hyphae.
- Hover: 5–8% scale, the hypha brightens. Click opens the product page.
- Mockup p14 shows "**Black Pearl oesterzwam**" instead of Italiaanse, and "ZES BIJZONDERE OESTERZWAMMEN" in the centre.

**Block 4, "Binnen gekweekt x buiten gekweekt".** 100vh cinematic split: dark purple-lit grow room on the left, warm outdoor logs/straw on the right, glowing mycelium in the centre.
- Title "**Van gecontroleerde groei tot de kracht van de natuur**". Subtitle "**Twee manieren van kweken. Eén missie: uitzonderlijke oesterzwammen met respect voor mens, natuur en smaak.**"
- Left card (dark glass): "**Binnen gekweekt**" / "**Precisie die je kunt proeven.**" / "In onze gecontroleerde kweekruimtes creëren we het klimaat waarin oesterzwammen optimaal kunnen groeien. Temperatuur, luchtvochtigheid, luchtstroom en licht worden nauwkeurig afgestemd op elke soort." USPs: KLIMAAT GESTUURD / OPTIMALE LUCHTVOCHTIGHEID / JAARROND PRODUCTIE. CTA "**Ontdek onze binnenkweek →**" to the binnenkweek page.
- Right card (light glass): "**Buiten gekweekt**" / "**Groeien met het ritme van de natuur.**" / "Buiten laten we het mycelium samenwerken met zijn natuurlijke omgeving. Hout, stro, seizoenen en bodem vormen samen een levende kringloop waarin paddenstoelen hun plaats vinden." USPs: NATUURLIJKE KRINGLOOP / SEIZOENSGEBONDEN / RESTSTROMEN ALS VOEDINGSBODEM. CTA "**Ontdek onze buitenkweek →**" to the buitenkweek page.
- Centre: "**Verbonden door mycelium**" / "Of we nu binnen of buiten kweken, het begint allemaal met hetzelfde levende netwerk. Mycelium verbindt, voedt en brengt leven voort."
- 4-phase scroll animation and subtle hovers.
- "WAT CLAUDE NIET MAG DOEN": no excessive mycelium, root tree, psychedelic, sci-fi, neon, biotech look or standard two-column site. Mockup p22 matches.

**Block 5, "Voor elke tafel een eigen verhaal".** Warm off-white, airier, no big mycelium.
- Title "**VOOR ELKE TAFEL / Een eigen verhaal.**" Intro "Van de chef die op zoek is naar bijzondere smaken tot de grootkeuken die dagelijks voor veel mensen kookt. Speciaal winkels die graag lokale producten aanbieden en natuurlijk voor wie thuis gewoon lekker en lokaal wil eten."
- 4 full-photo cards with a dark gradient (the brief says "drie kaarten" and its ASCII art shows 3, but specifies 4):
  - VOOR CHEFS: "Bijzondere zwammen voor bijzondere gerechten." / "Verse, lokale oesterzwammen voor chefs die smaak, textuur en seizoensgebonden producten centraal zetten." / "Ontdek voor chefs →"
  - VOOR GROOTKEUKENS: "Lokaal gekweekt. Gemaakt voor grotere volumes." / "Verse oesterzwammen voor grootkeukens, zorginstellingen, scholen en andere professionele keukens." / "Ontdek voor grootkeukens →"
  - VOOR WINKEL: "Van kwekerij naar jouw winkel" / "Ontdek bijzondere oesterzwammen en haal de smaak van onze lokale kwekerij naar je eigen winkel." / "Ontdek voor winkel →". Photo: a greengrocer weighing coloured oysters on a scale while a customer waits, the shop assistant in shorts.
  - VOOR THUIS: "Van kwekerij naar jouw keuken." / "…naar je eigen keuken." / "Ontdek voor thuis →". Photo: a family cutting coloured oysters at a wooden table.
- Hover: the selected card grows, the others dim. Text CTA arrow moves 5–8 px.
- Footer message: "**Eén kwekerij. Verschillende behoeften.**" / "We kweken lokaal in Knokke-Heist en bouwen aan een lokaal netwerk met chefs, grootkeukens en liefhebbers in Knokke-Heist, Sluis, Damme, Brugge, Blankenberge en de omgeving." / "Knokke-Heist · Damme · Sluis · Brugge · Blankenberge" with pins.
- Mockup p33 shows only 3 cards (chefs, grootkeukens, thuis), with mycelium roots glowing below.

**Block 6, "De kweker achter GroMush".** 50/50 split.
- Left: the real photo of Anthony (hat, blue shirt, crate of mixed oysters in a misty grow room). In the folder, `Anthony-watteeuw-paddenstoel-kweker-…png` shows a flat cap, blue shirt and a GroMush crate. Rounded 20–28 px. Profile panel: "ANTHONY / Kweker & oprichter GroMush", "KNOKKE-HEIST / Lokale productie", "AMBACHTELIJK / Gekweekt met zorg en aandacht".
- Right: label "DE KWEKER ACHTER GROMUSH". Headline "**Ik wil weten waar mijn eten vandaan komt.**" Intro "GroMush is ontstaan vanuit een fascinatie voor de wereld van paddenstoelen en de overtuiging dat lokaal voedsel opnieuw dichter bij de mensen mag komen." Three paragraphs:
  - "Vanuit Knokke-Heist bouw ik aan een kleinschalige, ambachtelijke kwekerij waar oesterzwammen met aandacht voor smaak, kwaliteit en natuurlijke processen worden gekweekt."
  - "Ik wil niet zomaar paddenstoelen produceren. Ik wil een korte verbinding creëren tussen kweker, chef en consument."
  - "Verse zwammen die niet eerst honderden kilometers afleggen, maar rechtstreeks uit de lokale omgeving komen. Producten waarvan je weet waar ze vandaan komen én wie ze heeft gekweekt."
- Statement (black, i.e. suggested): "Klein beginnen. / Lokaal groeien. / Samen bouwen aan iets duurzaams." CTA "**ONTDEK HET VERHAAL ACHTER GROMUSH →**".
- Subtle botanical oyster line drawing, cascade fade-in (80–120 ms), hover zoom ≤1.02.
- Mockup p42 shows a different Anthony (straw hat, apron, yellow oysters). Use the real photo.

**Block 7, "Proef GroMush" (final conversion).** Dark moss/wood background, proefbox image plus text.
- Overline "VERS UIT ONZE KWEEKRUIMTE". Headline "**Proef het verschil.**" Text "Ontdek onze ambachtelijk gekweekte oesterzwammen en proef zelf het verschil in smaak, textuur en versheid." / "We stellen graag een gratis proefbox samen met een selectie van onze soorten."
- Single green CTA "**Bestel je gratis proefbox →**" ("mag gelinkt worden met gmail account info@gromush.be"). Trust line: "Voor chefs • grootkeukens • speciaalzaken".
- Mockup p48 instead shows the Proefbox-push design: "Proef GroMush. Helemaal gratis.", a cream background, "Eerst proeven. Dan samen groeien.", and a town bar "Knokke-Heist / Damme / Sluis / Brugge".

**Not specified:** footer and header visuals (beyond the nav list), particulier routing target, "Ontdek ons verhaal"/"Word onderdeel van het netwerk" targets.

---

### 2.2 Voor wie (audience overview section/page)

Brief: `Voor-wie-pagina-website-gromush.pdf` (6 pp, no red). An AI "UI/UX & visual briefing for Claude" including an English copy-paste prompt. Email embeds 4 images.
Purpose: a 4-column audience section "Voor wie kweken we?", extending homepage block 5 from 3 to 4 cards. It is unclear whether this is a standalone page or the homepage block. The nav parent is "Voor wie?".

- **Header.**
  - Background #F5F2E8. Sprout icon #48664A. Overline "VOOR WIE KWEKEN WE?" (#17251B, 0.15em tracking).
  - H2 "**Voor elke tafel een eigen verhaal.**" (Playfair/Cormorant, #10251A, 42–52px).
  - Intro "Van de chef die op zoek is naar een bijzondere oesterzwam tot de keuken die dagelijks voor honderden mensen kookt. Van de ambachtelijke speciaalzaak tot wie thuis gewoon beter wil eten."
- **4 cards.** Grid: 4 columns above 1200px, 2×2 on tablet, 1 column or swipe on mobile. Radius 28px, 520–580px tall, photo top with forest gradient bottom (#10251A→#0D1C14), round icon badge, olive pill CTA #48664A.
  - VOOR CHEFS: "Bijzondere zwammen voor bijzondere gerechten." / "Verse, lokale oesterzwammen voor chefs die smaak, textuur en seizoensgebonden producten centraal zetten." / "Ontdek voor chefs →". Chef plating with tweezers.
  - VOOR GROOTKEUKENS: "Lokaal gekweekte zwammen. Gemaakt voor grotere volumes." / "Verse oesterzwammen voor grootkeukens, zorginstellingen, scholen en andere professionele keukens." / "Ontdek voor grootkeukens →"
  - VOOR SPECIAALWINKELS: "Kwaliteit in het rek. Vers uit de polder." / "Verrijk je assortiment met dagverse, ambachtelijk gekweekte zwammen voor klanten die kiezen voor lokaal en kwaliteit." / "Ontdek voor winkels →"
  - VOOR THUIS (community): "Van onze kwekerij naar jouw keuken." / "Verse oesterzwammen, rechtstreeks uit de lokale kwekerij. Ontdek nieuwe smaken en kook zelf met bijzondere zwammen." / "Ontdek voor thuis →"
- **Below.** Glowing gold/white hyphae (#E8BF59/#FFF) converge into a central badge. Corner photo accents: blue/grey oysters bottom-left, yellow and pink bottom-right.
- **Footer of section.** H3 "**Één kwekerij. Verschillende behoeften.**" (sic, "Één"). "Wij kweken lokaal in Knokke-Heist en bouwen aan een netwerk met chefs, grootkeukens, speciaalzaken en liefhebbers in de hele regio." Location pills: Knokke-Heist ⤍ Damme ⤍ Sluis ⤍ Brugge ⤍ Blankenberge.
- The mockup is the same 3-card image as homepage block 5.

### 2.3 Voor chefs

Brief: `Chefpagina - website - gromush.pdf` (20 pp, red copy; mockup p2). Email: "volledig uitgeschreven chefpagina pdf. De content staat in het rood en in cursief." Assets via Drive.
URL suggested elsewhere: `/voor-wie/chefs`.
Goal: primary conversion **PROEFBOX AANVRAGEN**, secondary **START EEN CHEFBOX-ABONNEMENT**. Chef questions to answer: consistent quality, reliable delivery, taste, preparation, shelf life, local, quick extra orders.

Sections in order. Mobile order is stated: Hero, Soorten, Waarom, Recepten, Kweekproces, ChefBox, Lokale levering, Proefbox, **Testimonials**, Footer.
1. **Hero** (70–80% viewport, dark culinary photo, mycelium grows on load on the left). "**Paddenstoelen met karakter.**" plus, in gold, "**Voor chefs die smaak willen laten groeien.**" Sub "Ambachtelijk gekweekte gourmetpaddenstoelen, rechtstreeks van de kweker naar jouw keuken." CTA 1 "Ontdek onze soorten". CTA 2 (primary) "Vraag een proefbox aan".
2. **Onze soorten** (cream, horizontal carousel). Gele "Delicaat · Aromatisch"; Roze "Fruitig · Zacht"; Witte (no descriptor given); Blauwe "Intens · Umami"; Grijze "Intens · Umami" (duplicate of blauwe); Italiaanse "Diep · Hartig". There is an orphan line "Stevig · Elegant". The descriptors also **differ from the homepage taste words**. Cards link to product pages. "Bekijk alle soorten" below. Hover: a mycelium line links to the next section.
3. **Waarom chefs kiezen voor GroMush** (5 gold line icons): Uitzonderlijke smaak / Unieke texturen / Visueel onderscheidend / Veelzijdig inzetbaar / Rechtstreeks van de kweker, each with a one-liner (e.g. "Van amuse tot hoofdgerecht, van vegetarisch tot verfijnde begeleiding").
4. **Heerlijk koken met oesterzwammen** (deep forest). 3 dish cards labelled "GroMush gerecht": "Forest Pulled Mushroom Burger" (Bekijk hoe), "Geroosterde oesterzwam met kruiden-ghee, miso en citroen" (Bekijk hoe), "Vlaamse stoofpot van oesterzwam" (Bekijk recept). "Meer inspiratie" opens the inspiration page. The mockup shows different dishes ("Geel met beurre noisette en hazelnoot", etc.).
5. **Rechtstreeks uit onze kwekerij naar jouw keuken.** "Wij oogsten wanneer de paddenstoelen op hun best zijn…". 5-step line: 01 Kwekerij / 02 Oogst / 03 Verpakking / 04 Levering ("Gekoeld en op tijd geleverd, op de dag die jij kiest.") / 05 Jouw keuken. CTA "Ontdek ons kweekproces".
6. **ChefBox abonnementen** (deep forest, big wooden ChefBox photo left). "Kies het abonnement dat past bij jouw keuken." Flex and Select cards as in the section 1 table. The CTA on both is "Prijs". Gold glow on Select. Under the cards, large and not small print: "**Alle abonnementen zijn flexibel en aanpasbaar aan jouw behoefte.**"
7. **Lokaal geleverd, vers van hier.** "Wij leveren persoonlijk in de regio. Korte keten, maximale versheid zonder groothandel." Region cards:
   - Knokke-Heist: "Persoonlijke levering in Knokke-Heist." / "Levering Knokke-Heist" to the Knokke page. May open a modal for postcode/restaurant data.
   - Sluis: "Dagverse levering in Sluis."
   - Damme: "Vers van de kweker in Damme."
   - Brugge: "Snel geleverd in Brugge."
   - Blankenberge: **copy-paste error**, the card title and text still say "Brugge / Snel geleverd in Brugge" while the CTA says "Levering Blankenberge".
   Plus a subtle region map with green pins and mycelium-like lines from GroMush. Regional CTA: "Zit jouw restaurant in onze regio? Neem contact op en ontdek wat we voor jouw keuken kunnen betekenen." / "Bespreek jouw levering" + "Vraag een proefbox aan".
8. **Eerst proeven?** "Vraag jouw proefbox aan en ontdek welke soorten passen bij jouw keuken." 4 benefits: Verschillende soorten uitproberen / Ideaal om te testen in jouw gerechten / Geen verplichtingen / Snel en eenvoudig aangevraagd. Large CTA "Vraag proefbox aan". Same destination everywhere.
9. **Proefbox form.** Brief: "naar email info@gromush.be. Open een formulier of aparte pagina." Fields: Naam, Restaurant, Functie, E-mail, Telefoon, Adres restaurant, Stad, Welke soorten interesseren je?, Geschat weekvolume, Gewenste leverregio, Opmerkingen. Button "Mijn proefbox aanvragen". Thanks text "Bedankt. We nemen persoonlijk contact met je op."
10. **Final CTA.** "**PROEF GROMUSH**" / "Ontdek welke paddenstoelen jouw keuken kunnen laten groeien."

- Mycelium "red thread" per section: hero kweker→paddenstoel; region GroMush→Knokke→Sluis→Damme→Brugge; ChefBox GroMush→wekelijkse levering→keuken.
- Key message: "GroMush is geen gewone leverancier. GroMush is een partner voor mijn keuken."
- Three primary CTAs only: proefbox, soorten, Start een ChefBox.
- Section numbering skips 2, 12, 23–24. There is no testimonials section content, although the mobile order and the mockup (fictional chef quotes) include one.
- **Mockup differences:**
  - Nav: Home, Onze paddenstoelen, Voor chefs, Voor grootkeukens, Word mede-eigenaar, Inspiratie, Over GroMush, Contact, plus button "Proefbox aanvragen".
  - 7 varieties incl. Black Pearl, Koningsoesterzwam, Pruikzwam.
  - 3 ChefBox tiers (Basis 5kg, Select 15kg, Exclusief 25kg per week).
  - "Wat chefs over GroMush zeggen" testimonials.

### 2.4 Voor grootkeukens

Brief: `Grootkeukenpagina-storytelling-build.pdf` (28 pp, red/red-italic copy; mockup p1). Email lists Drive zips (Locaties, Kweekproces-tot-bord) and logo.
URL suggested: `/voor-wie/grootkeukens`.
Audience: hospitals, woonzorgcentra, schools, company restaurants, caterers, hotels, institutions, meal producers. Must feel different from the chef page: reliability, volume, continuity, food safety, logistics, price, local delivery.
Primary conversion: **BESPREEK JOUW BEHOEFTE**. Secondary: VRAAG EEN OFFERTE AAN, VRAAG EEN PROEFLEVERING AAN, BESPREEK JOUW VOLUME. A sticky "Bespreek jouw behoefte" bar on mobile.

Sections (copy in red):
1. **Hero.** Large-kitchen photo with multiple staff, GN trays and mushrooms in volume, mycelium illustration on the left. "**Lokaal gekweekt.**" plus, in gold, "**Betrouwbaar geleverd.**" "Verse gourmetpaddenstoelen voor grootkeukens, zorginstellingen, scholen, bedrijfsrestaurants en catering." / "Van lokale kwekerij naar professionele keuken, met aandacht voor kwaliteit, continuïteit en voedselveiligheid." CTAs "Bespreek jouw behoefte →", "Vraag een offerte aan". Pin line: "Actief in Knokke-Heist · Sluis · Damme · Brugge".
2. **Four promises** (cream): 01 Vaste levering ("Geplande wekelijkse leveringen afgestemd op jouw verbruik.") / 02 Schaalbaar ("Van kleinere professionele volumes tot structurele afnames.") / 03 Lokaal ("Rechtstreeks van onze kwekerij naar jouw keuken.") / 04 Vers ("Geoogst met aandacht voor optimale kwaliteit en houdbaarheid.").
3. **Voor wie?** "Voor professionele keukens met grote ambities." / "Van dagelijkse maaltijden tot grootschalige catering: GroMush groeit mee met jouw keuken." 4 photo cards, each CTA "Proef gratis →": Zorg & ziekenhuizen ("Verse lokale producten voor dagelijkse maaltijden."), Scholen ("Gezonde en veelzijdige ingrediënten voor grote groepen."), Bedrijfsrestaurants ("Lokale producten die passen binnen een modern voedingsbeleid."), Catering & horeca ("Betrouwbare volumes voor professionele bereiding.").
4. **Onze paddenstoelen, jouw mogelijkheden.** "Verschillende soorten, elk met een eigen karakter en toepassingen in de grootkeuken." Carousel of the 6, each with name, taste, texture and uses. Example: "Grijze oesterzwam / Aards · Umami · Vlezig / Toepassingen: Soepen · sauzen · warme maaltijden · vegetarische bereidingen / Bekijk soort →". "Bekijk alle soorten".
5. **Gemak in de grootkeuken.** "**Minder gedoe. Meer product.**" / "Ontworpen om efficiënt te werken in professionele keukens." Weinig snijverlies / Eenvoudig te verwerken / Consistente kwaliteit / Veelzijdig inzetbaar.
6. **Voeding & gezondheid.** "Een veelzijdig ingrediënt voor gezonde maaltijden." / "Paddenstoelen zijn een veelzijdig onderdeel van een gevarieerd voedingspatroon…" Only provable nutrition info (fibre, calories, protein…). No medical or superfood claims. CTA "Neem contact".
7. **Van lokale kwekerij naar jouw keuken.** "Een korte keten tussen kweker en professionele keuken." Timeline with 5 round photos: 01 Kwekerij (photo: collecting straw) "Ambachtelijk gekweekt met respect voor natuur en grondstoffen." / 02 Oogst (mushrooms in buckets) / 03 Verpakking / 04 Levering (GroMush van) "Op tijd geleverd, op de dag die jij kiest." / 05 Jouw keuken "Van kweker naar keuken, voor duizenden maaltijden." CTA "Ontdek ons kweekproces →".
8. **Lokaal geleverd, vers van hier.** "Persoonlijk geleverd in onze regio. Korte keten, maximale versheid." 5 location cards with CTA "Bespreek levering →". **Blankenberge has a copy-paste error**: "Foto van Brugge / Snel en gekoeld geleverd in Brugge". The brief also says "vier kaarten".
9. **Regiokaart.** 5 green pins, organic lines from GroMush. "Levering afgestemd op jouw locatie en behoefte." CTA "Plan een levering →".
10. **Capaciteit.** "**Gebouwd om mee te groeien.**" / "Onze productie wordt modulair opgebouwd, zodat we onze capaciteit kunnen uitbreiden naarmate de vraag groeit." Visual scale: Kweekruimte ↓ Productie ↓ Wekelijkse oogst ↓ Vaste leveringen ↓ Professionele keuken. No kg figures until final. CTA "Bespreek jouw verwachte volume".
11. **Leveringsformules.** "Een leveringsformule op maat." START / PROFESSIONEEL / PARTNER (see section 1 table).
12. **Behoeftecalculator** ("one of the most modern parts"). "Hoeveel heeft jouw keuken nodig?" / "Vertel ons kort hoe jouw keuken werkt en ontvang een voorstel op maat."
    - Q1 meals/day: <500 / 500–1.000 / 1.000–5.000 / 5.000–10.000 / >10.000
    - Q2 mushroom frequency: 1×/wk / 2–3× / 4–5× / dagelijks
    - Q3 varieties: multi-select of the 6
    - Q4 location: the 5 towns
    - Output: "Jouw behoefte", an indicative calculation labelled as indication only. Progress indicator. CTA "Ontvang een persoonlijk voorstel →". **No formula is given.**
13. **Voedselveiligheid & traceerbaarheid.** "**Kwaliteit begint vóór de keuken.**" 5 icons: Batchregistratie / Oogstdatum / Herkomst / Bewaaradvies / Hygiëne. Only real procedures. CTA "Neem contact".
14. **Duurzaamheid.** "Lokaal voedsel met een kortere keten." 4 pillars: Lokaal / Korte keten / Efficiënte productie / Circulaire mogelijkheden ("…reststromen en gebruikt substraat nuttig in te zetten").
15. **FAQ accordion** (answers in red):
    - Volumes? "Momenteel zijn we in een opstartfase, waardoor grote volumes nog niet gegarandeerd zijn."
    - Soorten? "Witte, roze, gele, blauwe, grijze, Italiaanse oesterzwammen."
    - Vaste wekelijkse leveringen? "Bij grotere leveringen zullen er vaste dagen binnen de week afgesproken worden."
    - Combineren? "Ja dat kan zeker, ook wat afhankelijk van de oogsten."
    - Verpakt? "In luchtdoorlatende kratten."
    - Geleverd? "Via onze bestelwagen worden ze persoonlijk geleverd."
    - Hoe lang vers? "Minimum een week."
    - Bewaren? "In de koelkast met een temperatuur van 4°C."
    - Meerdere locaties? "Wij kunnen op meerdere locaties leveren."
    - Raamovereenkomst? "Dat is mogelijk zodra wij jullie behoeften weten."
    - Eerst testen? "Zeker! GroMush biedt via de website een gratis proefbox aan."
    - Bestellen? "Dat kan rechtstreeks via de kweker door email of whatsapp."
16. **Proeflevering.** "Eerst testen in jouw keuken?" / "Ontvang een proeflevering en ontdek welke GroMush-soorten passen bij jouw menu, volume en keukenwerking." ✓ Verschillende soorten ✓ Testen in je eigen keuken ✓ Geen langdurige verplichting ✓ Persoonlijk advies. CTA "Vraag een proeflevering aan →".
17. **Contact form** "Bespreek jouw behoefte."
    - Fields: Naam, Organisatie, Functie, E-mail, Telefoon, Adres, Type keuken (dropdown: Ziekenhuis, Woonzorgcentrum, School, Bedrijfsrestaurant, Catering, Hotel, Andere), Aantal maaltijden per dag, Geschat paddenstoelvolume, Gewenste leverfrequentie, Interessante soorten, Bericht.
    - CTA "Vraag een voorstel aan". After sending: "Bedankt. We nemen persoonlijk contact met je op."
18. **Slot.** Dark forest with mycelium. "**Jullie zorgen voor duizenden maaltijden.**" plus, in gold, "**Wij zorgen voor de paddenstoelen.**" / "Samen bouwen we aan een lokale, betrouwbare en smaakvolle voedselketen." CTAs "Bespreek jouw behoefte" / "Vraag een proeflevering". Legal links.

- The mobile order lists "**13. Cases**" (testimonials), but no Cases content is given. The mockup shows fictional testimonials ("Keukenverantwoordelijke, Zorgcentrum…").
- Closing idea: "Laten we samen jouw keuken laten groeien."
- **Mockup:** formulas Start 25 kg/week, Professioneel 75 kg/week, Partner "Volume op maat"; "Waarom samenwerken met GroMush?" strip; varieties shown incl. Koningsoesterzwam and Pruikzwam.

### 2.5 Voor speciaalzaken / speciaalwinkels

Brief: `Speciaalwinkels-pagina-website-gromush.pdf` (19 pp, no red; mockup p1). Empty email.
URL proposed: **`/voor-speciaalzaken`**. This conflicts with `/voor-wie/speciaalwinkels` in the landing briefs.
SEO title: "Verse oesterzwammen voor speciaalzaken | GroMush". Meta: "GroMush levert ambachtelijk gekweekte oesterzwammen aan speciaalzaken in Knokke-Heist, Damme, Sluis, Brugge en omgeving. Ontdek het assortiment en vraag informatie aan."
Audience: bakers, greengrocers, butchers/traiteurs, cheese/deli, bio shops, horeca/lunch bars, local food shops. Conversion: contact form for kennismaking, proeflevering or prijsinformatie.

**Design deviations.**
- Its own palette: #102D20, #183B2A, #456C48, #A8B99A, #F5F2E9, #FFFDF7, **mustard yellow #E6D83E** for CTAs, #292D29.
- **Rounded sans-serif headings** (Manrope/Nunito Sans) instead of serif.
- Own nav: Home, Voor speciaalzaken, Producten, Over ons, Recepten, Contact, plus CTA "Levering aanvragen" with a truck icon. Sticky.

Sections:
1. **Hero** (480–560px). Grey plastic transport crate full of mixed oysters (geel, roze, blauw, grijs, wit) with subtle GroMush branding. Label "VOOR LOKALE SPECIAALZAKEN". H1 "**De smaak van echte natuur, rechtstreeks naar jouw zaak.**" Intro "GroMush levert verse, ambachtelijk gekweekte oesterzwammen aan speciaalzaken in Knokke-Heist, Damme, Sluis, Brugge en omgeving. Bijzondere smaken, een lokaal verhaal en kwaliteit die je klanten kunnen proeven." Yellow CTA "Ontdek onze producten →" (scrolls). Secondary "Hoe werkt samenwerken?" Round badge "LOKAAL GEKWEEKT". The mockup badge says "LOKAAL BIO DUURZAAM".
2. **Jouw lokale partner voor verse oesterzwammen.** "Wil je jouw klanten iets bijzonders aanbieden? Met GroMush voeg je een verrassend, veelzijdig en smaakvol product toe aan je assortiment…" Four cards:
   - Bakkers: "Een verrassend ingrediënt voor hartige broodjes, focaccia en creatieve broodspecialiteiten."
   - Groente & fruit: "Verrijk je assortiment met kleurrijke, verse paddenstoelen van een lokale kweker."
   - Beenhouwers & traiteurs: "Een veelzijdig ingrediënt voor bereidingen, maaltijdschotels en verrassende vegetarische alternatieven."
   - Horeca & delicatessen: "Voor winkels en keukens die hun klanten willen laten kennismaken met bijzondere smaken."
3. **Ontdek ons assortiment** (dark forest). "ONS ASSORTIMENT / Diverse soorten, eindeloze mogelijkheden" / "Van zacht en verfijnd tot uitgesproken en karaktervol…" Product row: 1 Gele (citrino), 2 Witte, 3 Roze (zalmroze), 4 Blauwe, 5 Grijze, 6 **Zomeroesterzwam**, 7 **Koningsoesterzwam**, 8 **Shiitake**, 9 **Pruikzwam (Lion's Mane)**. No "Italiaanse". Show shiitake and pruikzwam "afhankelijk van beschikbaarheid". CTA "Bekijk het volledige assortiment →".
4. **Waarom kiezen voor GroMush?** Four benefits with quoted copy:
   - Lokaal en dichtbij: "Een kweker uit de regio, met korte lijnen en persoonlijk contact…"
   - Vers en ambachtelijk
   - Veelzijdig in gebruik
   - Persoonlijke samenwerking: "Rechtstreeks contact met de kweker om assortiment, volumes en levermomenten…"
   Photo of a crate handover. "Biologisch" only if certified. The mockup says "100% lokaal en biologisch".
5. **Meer dan een paddenstoel.** "Oesterzwammen zijn veelzijdig, herkenbaar en verrassend toegankelijk…" Three inspiration blocks: Vers in de winkel / Klaar om te ontdekken / Een eigen specialiteit.
6. **Hoe werkt samenwerken?** "SAMENWERKEN MET GROMUSH / Van eerste kennismaking tot verse levering". Stap 1 Vertel ons over je zaak / Stap 2 Stem het aanbod af / Stap 3 Start met een eerste levering. CTA "Bespreek jouw eerste levering →". Do not promise a free trial delivery.
7. **Rechtstreeks van de kweker.** "GroMush vertrekt vanuit een eenvoudige overtuiging: goed eten begint bij aandacht voor wat de natuur ons biedt…" Signed "Anthony Watteeuw / Zaakvoerder en kweker bij GroMush". CTA "Leer GroMush kennen →" to Over ons. Use a real photo; no fake portrait.
8. **Laten we samenwerken** (polder at sunset background). "**Laten we samen meer smaak op tafel brengen.**" / "Ben je bakker, groente- en fruitwinkelier, beenhouwer, traiteur of uitbater van een speciaalzaak? Vertel ons wat je zoekt…" Yellow CTA "Vraag informatie aan →". "Of mail naar info@gromush.be". Contact block: GroMush, Anthony Watteeuw (zaakvoerder en kweker), Knokke-Heist, info@gromush.be. Handwritten "Lokaal is lekkerder."
9. **Form** "Vertel ons over jouw zaak".
   - Fields: Naam, Naam van de zaak, E-mailadres, Type speciaalzaak (Bakkerij / Groente- en fruitwinkel / Beenhouwerij / Traiteur / Kaas- of delicatessenwinkel / Bio- of natuurvoedingswinkel / Horeca / Andere), Gemeente, Interesse in soorten, Geschat gewenst volume, Gewenste leverfrequentie (both optional), Vrij bericht, consent checkbox.
   - Button "Verstuur mijn aanvraag". Real backend, no fake success.
10. **Footer.** Logo, "Ambachtelijk gekweekt", "Verse paddenstoelen, rechtstreeks van de kweker." Nav, email, IG/FB, legal.

- **Mockup:** phone "+32 479 12 34 56" (fake), "Levering in Knokke-Heist, Damme, Sluis, Brugge en omliggende regio", headline "Laten we samenwerken!".

### 2.6 Voor particulieren

**No dedicated brief exists.** The homepage nav lists "D - Voor particulieren" and the homepage card "VOOR THUIS → Ontdek voor thuis". The Voor-wie brief calls the 4th card "VOOR COMMUNITY / THUIS". The landing pages send the 4th audience to `/community`. Likely the Community page fills this role. See open questions.

---

### 2.7 Onze zwammen (overview / "Ontdek onze zwammen")

Brief: `GroMush | Ontdek onze zwammen.pdf` (8 pp, red copy; screenshot mockup p2). Email: Product-zwammen.zip.
Purpose: show the range and the indoor vs outdoor difference, inspire, drive orders via the contact form. Audience: chefs, restaurants, bistros, local food shops, consumers. It targets "Bekijk alle soorten" links from product pages.

- **Header/nav.** Logo with "Ambachtelijk gekweekt". Accent CTA "**Bestellen**" goes straight to the contact form; no cart.
- **Hero.** Dark, with mixed mushrooms: grey, blue, yellow, pink, white oysters, king oysters, lion's mane, shiitake. Title "**Ontdek onze zwammen**" ("onze zwammen" in moss green). Intro "**Van ambachtelijke binnenkweek tot authentieke buitenkweek.**" Primary CTA "**Bestellen**" (contact form). Secondary "**Laat je inspireren**" (inspiration page).
- **Twee werelden, één passie.** "Sommige zwammen groeien het hele jaar door in ons klimaatgecontroleerde kweekhuis. Andere krijgen de tijd in de natuur op boomstammen. Ontdek het verschil."
  - Card A, "Binnenkweek / Het hele jaar door beschikbaar": Constante kwaliteit, Gecontroleerd klimaat, Duurzaam en lokaal. CTA "Ontdek binnenkweek".
  - Card B, "Buitenkweek / Een natuurlijk groeiproces, met de seizoenen": Langzame, natuurlijke groei, Seizoensgebonden oogst, Intense, authentieke smaak. **Future project.** Timeline block "**Onze buitenkweek komt eraan**": "Voorjaar 2027: start van het buitenkweekproject." / "Voorjaar 2028: eerste oogst verwacht." State that the harvest is an expectation. CTA "Ontdek onze plannen".
- **Onze binnengekweekte zwammen.** "Met zorg gekweekt in onze klimaatgecontroleerde kweekruimte voor een constante kwaliteit, het hele jaar door." The text says "**acht productkaarten**" but lists 6 (the mockup shows 8: + Black Pearl, Koningsoesterzwam, Pruikzwam):
  - Grijze (P. ostreatus): "Mild, hartig en licht nootachtig. Stevig met sappige beet." Pasta, risotto, wildgerechten.
  - Blauwe (P. ostreatus var. columbinus): "Uitgesproken en stevig, met een prachtige kleur." Pasta, gevogelte, wokgerechten.
  - Gele (P. citrinopileatus): "Zacht en licht fruitig, met een elegante gele kleur." Vis, schaaldieren, salades.
  - Roze (P. djamor): "Opvallend van kleur, met een licht zoete, spekachtige smaak." BBQ, stroganoff, Aziatische gerechten.
  - Witte (P. ostreatus): "Elegant, zacht en verfijnd. Ideaal voor witte sauzen." Pasta, gevogelte, roomsaus.
  - Italiaanse (P. pulmonarius): "Een elegante oesterzwam met een zachte, licht nootachtige smaak en een fijne, sappige textuur. Veelzijdig in de keuken en heerlijk wanneer goudbruin gebakken." Pasta, risotto, gegrilde gerechten, wok en mediterrane bereidingen.
- **Onze buitengekweekte zwammen.** Shiitake on logs photo. "Gekweekt op natuurlijke boomstammen en strobalen, in harmonie met de seizoenen." Langzame groei / Intense smaak / Volledig natuurlijk groeiproces / Beperkt beschikbaar. Announcement "Buitenkweek in voorbereiding": "We starten ons buitenkweekproject in het voorjaar van 2027. De eerste oogst verwachten we in het voorjaar van 2028." Same timeline. CTA "**Volg onze buitenkweek**" goes to the GroMush **Facebook page**. Never say "nu beschikbaar". The dates must be easy to edit.
- **Waarom chefs kiezen voor GroMush** (6 icons): Lokaal geteeld / Dagelijks vers geoogst / Duurzaam geproduceerd / Speciaal geselecteerd voor gastronomie / Wekelijkse levering mogelijk / Persoonlijk advies.
- **Closing CTA.** "**Welke zwam past op jouw menukaart?**" / "Vraag een proefbox aan en ontdek zelf de kwaliteit en smaak van GroMush." Primary "Proefbox aanvragen" (contact form with proefbox request). Secondary "Of neem contact op".
- **Rules:** no fictitious stock, prices, labels or availability. Alt texts. Semantic HTML.
- **Mockup nav:** Home, Over GroMush, Onze zwammen, Kweekwijze, Voor chefs, Contact, plus "Bestel proefbox".

### 2.8 Product page template: Gele oesterzwam (master)

Brief: `Productpagina Gele oesterzwam.pdf` (16 pp, red copy; mockup p2).
Email (verbatim): "**BELANGRIJK !!! Deze structuur en paginaopbouw geldt voor alle productpagina's. Dus ook voor de roze, witte, blauwe, grijze en Italiaanse oesterzwammen.**" Also: "De tekstinhoud staat in de bijlage in het rood gemarkeerd."
URL pattern (from other briefs): `/producten/gele-oesterzwam`.
Build instruction: build yellow first, then abstract the template.

**Template data model** (stated). Dutch keys in the gele brief, English keys in the others: name, slug, heroImage, galleryImages, accentColor, shortDescription, flavor/smaak, texture/textuur, appearance/uiterlijk, keuken/culinaryUses, flavorProfile, quote, packaging, availability, storage, relatedProducts.

**Sections** (numbering in the brief jumps from 1 to 5):
1. **Hero.** Dark close-up, mushrooms on the right. Label "GELE OESTERZWAM". Title "**Fris van kleur. Vol van smaak.**" Sub "**Lokaal gekweekt in Knokke-Heist. Vers geoogst voor jouw keuken.**" CTA "**Bestel gele oesterzwammen →**". USPs: Lokaal gekweekt / Vers geoogst / Ambachtelijk / Korte keten. Light parallax and fade.
2. **Introductie** (cream, 2 columns). Label "DE PADDENSTOEL". "**Een kleur die je niet kunt negeren**" / "De gele oesterzwam brengt niet alleen smaak, maar ook kleur en karakter. Met haar zonnige kleur en elegante waaiervormige hoeden is ze een opvallende verschijning in elke keuken." Characteristics:
   - SMAAK: Fris, aromatisch en zacht paddenstoelachtig.
   - TEXTUUR: Vlezig maar verfijnd, met een aangename beet.
   - UITERLIJK: Zonnig geel, met elegante waaiervormige hoeden.
   - KEUKEN: Van eenvoudige bereidingen tot verfijnde gerechten.
3. **Smaakprofiel.** "Hoe smaakt hij?" Smaak ●●●●○, Textuur ●●●●○, Aardsheid ●●●○○, Geur ●●●○○ (culinary indicators, not science). Quote "**"Een paddenstoel die kleur geeft aan het bord én karakter aan het gerecht."**"
4. **Van kwekerij tot keuken** (deep forest). "Lokaal gekweekt. Lokaal verbonden." Timeline with a mycelium line:
   - 01 GROEIEN: Het mycelium krijgt de tijd om zich volledig te ontwikkelen.
   - 02 VRUCHTEN: De eerste vruchtlichamen verschijnen en de gele kleur komt tevoorschijn.
   - 03 OOGSTEN: We oogsten op het moment dat de paddenstoelen op hun best zijn.
   - 04 LEVEREN: Vanuit onze kwekerij vertrekken ze vers richting keuken.
5. **Onze kweker block.** Added later; it is in the gele mockup and described in the roze/wit/blauw/grijs/Italiaans briefs. Not in the gele text. Placed after the timeline and before product info. Label "ONZE KWEKER". "GroMush — lokaal gekweekt, met passie en vakmanschap" / "GroMush is een kleinschalige kwekerij waar we met veel zorg onze oesterzwammen kweken. Kwaliteit, duurzaamheid en een korte keten staan bij ons centraal. We geloven in de kracht van lokaal en de puurheid van een natuurlijk product." Quote "We willen mensen laten genieten van eerlijke, kwaliteitsvolle oesterzwammen, rechtstreeks van bij ons." — GroMush. CTA "Lees meer over onze kwekerij →" to Over ons.
6. **Gastronomische keukensectie.** Restaurant-level dish photo. "**Gele oesterzwam in de keuken**". Perfect voor: ✓ Gebakken ✓ Gegrild ✓ In sauzen & pasta ✓ Lauwwarme gerechten ✓ Gastronomische bereidingen. CTA "**Bekijk meer inspiratie →**".
7. **Voor wie?** Background photo. "**Voor elke keuken die iets bijzonders wil**".
   - CHEFS: "Voor gerechten waar smaak, textuur en presentatie samenkomen."
   - THUISKEUKEN: "Makkelijk te verwerken in dagelijkse én bijzondere gerechten."
   - VEGETARISCHE KEUKEN: "Een natuurlijke manier om textuur en diepte aan een gerecht toe te voegen."
   The mockup title is "Voor wie is deze soort?".
8. **Productinformatie.** "Beschikbaar bij GroMush / Gele oesterzwam / **Vers gekweekt in België**". Verpakking 250 g / 500 g / 1 kg / Grotere hoeveelheden op aanvraag. Beschikbaarheid "Volgens oogst en seizoen." Voor horeca: "Voor horeca en professionele keukens is levering binnen onze lokale regio mogelijk." Buttons "Bestel →" and "**Vraag beschikbaarheid**". No price; the destination of "Bestel" is unspecified.
9. **Bewaren.** "Zo bewaar je ze het best" / "Bewaar oesterzwammen gekoeld en gebruik ze bij voorkeur zo vers mogelijk." Tip card "Tip van GroMush": "Bewaar ze niet luchtdicht afgesloten wanneer er veel condens kan ontstaan. Een ademende verpakking helpt de kwaliteit te behouden."
10. **Andere oesterzwammen** (cross-sell). "Ontdek onze andere oesterzwammen":
    - Roze: Krachtige kleur · opvallend op het bord
    - Blauwe: Stevige structuur · karaktervolle uitstraling
    - Witte: Elegant · veelzijdig
    - Grijze: Klassiek · culinair veelzijdig
    - Italiaanse: Bijzonder uiterlijk · gastronomisch karakter
    CTA "Bekijk alle soorten (ga je naar pagina onze zwammen) →". The brief says "zes kaarten naast elkaar" but lists 5. Mobile: swipe.
11. **Slot** (dark, farm photo). "**Van onze kwekerij naar jouw bord.**" / "Geen lange keten. Geen onnodige tussenstappen. Gewoon verse paddenstoelen, lokaal gekweekt." GroMush, *Ambachtelijk gekweekt.* CTA "**Ontdek GroMush →**".

- Accent per species as in the section 1 table. Forest green always dominant.
- Photography: hero cluster, close-up of gills, farm/mycelium, hand harvesting, packaging, gastronomic dish, other species.
- Animation: fade, image reveal, mycelium line, gentle hovers. No big parallax.
- UX journey: WOW → NIEUWSGIERIG → BEGRIJPEN → VERTROUWEN → INSPIRATIE → PRODUCT → ACTIE.
- The mockup nav includes **search and cart icons**, "Onze soorten" dropdown and "Recepten", plus a handwritten "Natuurlijk en puur".

### 2.9 Roze oesterzwam

Brief: `Productpagina roze oesterzwam.pdf` (13 pp, no red; mockup p1 = gele mockup). Email embeds 2 images.
Slug **`/producten/roze-oesterzwam`**. Same template, accent muted old-rose (not neon or Barbie pink).

- Hero: "**Kleur met karakter. Smaak die blijft hangen.**" Same subtext. CTA "Bestel roze oesterzwammen →".
- Intro: "**Een kleur die meteen opvalt**" / "De roze oesterzwam is een echte blikvanger. Haar uitgesproken kleur en elegante vorm geven elk gerecht een bijzonder karakter, terwijl haar stevige structuur zich uitstekend leent voor warme bereidingen."
  - Smaak: "Aromatisch en karaktervol, met een uitgesproken paddenstoelensmaak."
  - Textuur: "Stevig en vlezig, met een aangename beet."
  - Uiterlijk: "Opvallend roze, met elegante waaiervormige hoeden."
  - Keuken: "Bijzonder geschikt voor bakken, grillen en gastronomische bereidingen."
- Smaakprofiel 5/4/3/4. Quote "Een opvallende paddenstoel die niet alleen kleur, maar ook karakter aan het bord geeft."
- Timeline 02: "…de karakteristieke roze kleur ontwikkelt zich."
- **Onze kweker** block (defined here as "het nieuwe blok dat we hebben toegevoegd").
- Keuken: "Door haar opvallende kleur is de roze oesterzwam bijzonder geschikt voor gerechten waarbij uitstraling en smaak samenkomen." ✓ Gebakken ✓ Gegrild ✓ Pasta & sauzen ✓ Lauwwarme gerechten ✓ Gastronomische bereidingen.
- New **editorial highlight**: "Voor een bord dat mag opvallen." / "De natuurlijke roze kleur maakt deze soort bijzonder geschikt als visueel element in moderne en creatieve gerechten."
- Voor wie: CHEFS (as geel) / THUISKEUKEN "Voor wie een bijzonder ingrediënt wil gebruiken in dagelijkse of feestelijke gerechten." / VEGETARISCHE KEUKEN "Voor extra textuur, kleur en diepte in het gerecht."
- Product info and storage identical.
- Others: Gele "Fris van kleur · veelzijdig" + Blauwe/Witte/Grijze/Italiaanse as in the gele page.
- "**Geen nieuwe afbeeldingen genereren**": use placeholders.
- Positioning: OPVALLEND → GASTRONOMISCH → KARAKTERVOL → LOKAAL → AMBACHTELIJK.

### 2.10 Witte oesterzwam

Brief: `PRODUCTPAGINA WITTE OESTERZWAM.pdf` (13 pp, no red; mockup = gele). Email embeds 2 images, incl. `zomer-oesterzwam-…png` (a pale "summer oyster", possibly meant for Italiaans; to verify).
Slug **`/producten/witte-oesterzwam`**, accentColor "ivory". Positioning: puur · elegant · veelzijdig · verfijnd, timeless and accessible.

- Hero: "**Puur van smaak. Eindeloos veelzijdig.**" CTA "Bestel witte oesterzwammen →".
- Intro: "**Puur, elegant en verrassend veelzijdig**" / "De witte oesterzwam is een tijdloze klassieker. Met haar zachte kleur, elegante vorm en veelzijdige karakter past ze moeiteloos in uiteenlopende gerechten — van een eenvoudige bereiding tot een verfijnd bord."
  - Smaak: "Zacht, aromatisch en verfijnd."
  - Textuur: "Stevig en sappig, met een aangename beet."
  - Uiterlijk: "Zacht wit tot ivoorkleurig…"
  - Keuken: "Een veelzijdige basis voor zowel dagelijkse als gastronomische bereidingen."
- Smaakprofiel 4/4/3/3. Quote "Een verfijnde klassieker die zich thuis voelt in elke keuken."
- Timeline 02: "…ontwikkelen hun karakteristieke vorm en lichte kleur." Onze kweker block.
- Keuken: "De witte oesterzwam is een echte alleskunner…" ✓ Gebakken ✓ Gegrild ✓ Pasta & risotto ✓ Sauzen ✓ Soepen ✓ Gastronomische bereidingen.
- Highlight: "Een klassieker die altijd past." / "Van een snelle doordeweekse bereiding tot een verfijnd gastronomisch bord: de witte oesterzwam laat zich gemakkelijk combineren."
- Voor wie title "**Voor elke keuken die goed wil koken**": CHEFS "Een veelzijdige paddenstoel die zich gemakkelijk laat verwerken in uiteenlopende gerechten." / THUISKEUKEN "Toegankelijk, veelzijdig en eenvoudig te bereiden." / VEGETARISCHE KEUKEN "Een mooie basis voor gerechten waarin textuur en smaak centraal staan."
- Others: Gele / Roze / Blauwe / Grijze / Italiaanse.
- "Geen nieuwe stijl": keep header, footer, fonts, buttons, radius, etc.

### 2.11 Blauwe oesterzwam

Brief: `PRODUCTPAGINA BLAUWE OESTERZWAM.pdf` (12 pp, **red copy**, **no mockup image**). Email embeds 3 images. Note the file `Eigenschappen-grijze-oesterzwam-…png` sits in the blauwe folder.
Slug **`/producten/blauwe-oesterzwam`**, accentColor "blue-grey" (muted petrol). Keywords "karaktervol · stevig · diep van kleur · veelzijdig · gastronomisch". Must look stronger than Witte.

- Hero: "**Karaktervol van kleur. Krachtig van smaak.**" Primary CTA just "**Bestel**".
- Intro: "**Een paddenstoel met karakter**" / "De blauwe oesterzwam valt op door haar natuurlijke blauwgrijze kleur en stevige structuur. Ze is een veelzijdige paddenstoel voor bereidingen waarin smaak, textuur en uitstraling samenkomen."
  - Smaak: as roze.
  - Textuur: "Stevig, vlezig en aangenaam beetvast."
  - Uiterlijk: "Blauwgrijze tot grijzige waaiervormige hoeden."
  - Keuken: "Uitstekend geschikt voor bakken, grillen en warme gastronomische bereidingen."
- Smaakprofiel 5/5/4/4. Quote "**Een stevige paddenstoel met een uitgesproken karakter.**"
- Timeline 02: "…ontwikkelen hun karakteristieke blauwgrijze kleur." Onze kweker block.
- Keuken: "Dankzij haar stevige structuur en karaktervolle uitstraling komt de blauwe oesterzwam bijzonder goed tot haar recht in warme bereidingen." ✓ Gebakken ✓ Gegrild ✓ Geroosterd ✓ Pasta & risotto ✓ Sauzen ✓ Gastronomische bereidingen.
- Highlight: "**Voor gerechten met karakter.**" / "De stevige structuur en blauwgrijze kleur maken deze oesterzwam interessant voor gerechten waarin de paddenstoel echt zichtbaar en voelbaar mag zijn."
- Voor wie: CHEFS "Voor gerechten waarin textuur, smaak en presentatie samenkomen." / THUISKEUKEN "Voor wie een karaktervolle paddenstoel wil gebruiken in warme bereidingen." / VEGETARISCHE KEUKEN "Een stevige en veelzijdige basis voor gerechten waarin de paddenstoel centraal mag staan."
- Others: Gele "Fris van kleur · veelzijdig", Roze, Witte, Grijze, Italiaanse.

### 2.12 Grijze oesterzwam

Brief: `GRIJZE OESTERZWAM.pdf` (12 pp, no red; mockup = gele). Empty email; no images in the folder.
No slug stated (pattern implies `/producten/grijze-oesterzwam`). Positioning: "de tijdloze klassieker". Accent warm stone grey/taupe.
This brief **slightly deviates from the template**: 3 instead of 4 characteristics, a 6-item use grid, an editorial photo overlay, a cream (not dark) closing section, and a different others-carousel copy.

- Hero: label GRIJZE OESTERZWAM. "**De klassieker. Puur van smaak.**" ("Mijn voorkeur"; alt "Puur van smaak. Sterk in elke keuken."). CTA "Bestel grijze oesterzwammen →". USPs with sublines: Lokaal gekweekt / In Knokke-Heist; Vers geoogst / Rechtstreeks uit onze kwekerij; Ambachtelijk / Met zorg gekweekt; Korte keten / Van kweker naar keuken.
- Hero photo: on dark wood/stone, no crate, no logo.
- Intro: "**De oesterzwam die overal thuishoort**" / "De grijze oesterzwam is een echte klassieker. Zijn zachte, aardse smaak en stevige structuur maken hem bijzonder veelzijdig in de keuken. Van eenvoudig gebakken tot verfijnd gastronomisch: deze paddenstoel past zich moeiteloos aan." Smaak "Zacht & hartig" / Textuur "Stevig & sappig" / Uiterlijk "Natuurlijk grijs".
- Smaakprofiel title "**Puur karakter, eindeloze mogelijkheden**", 4/5/4/3. Quote "Een vertrouwde klassieker die zich thuis voelt in elke keuken."
- Timeline:
  - 01 "In onze kwekerij krijgt het mycelium de tijd en omstandigheden om zich volledig te ontwikkelen."
  - 02 "Wanneer de omstandigheden juist zijn, verschijnen de eerste vruchtlichamen."
  - 03 "We oogsten de paddenstoelen op het moment waarop ze op hun best zijn."
  - 04 "Vers vanuit Knokke-Heist naar jouw keuken."
- Onze kweker block.
- Keuken: "De grijze oesterzwam is een veelzijdige basis voor talloze bereidingen. Door zijn stevige structuur kan hij mooi worden aangebakken en gekaramelliseerd, maar hij voelt zich net zo goed thuis in sauzen, pasta's, risotto's en gastronomische gerechten." 6-tile grid: Gebakken "Goudbruin en hartig" / Gegrild "Krachtige geroosterde smaak" / Geroosterd "Diep en aromatisch" / Pasta & risotto "Romig en rijk" / Sauzen "Extra umami en diepte" / Gastronomisch "Van klassiek tot verfijnd".
- Editorial photo overlay: "DE KLASSIEKER VAN DE KEUKEN" / "Eenvoudig wanneer het kan. Verfijnd wanneer het moet."
- Voor wie, "Voor elke keuken": CHEFS "Een betrouwbare klassieker…" / THUISKEUKEN "Makkelijk om mee te koken…" / VEGETARISCHE KEUKEN "Stevig en veelzijdig…".
- Product info: Verpakking (same sizes), Herkomst "GroMush — Knokke-Heist", Beschikbaarheid "Volgens oogst en seizoen", Levering "Lokale professionele levering". No webshop tables.
- Storage: "…Bewaar ze niet volledig luchtdicht, zodat overtollig vocht kan ontsnappen."
- "Ontdek ook onze andere variëteiten": others carousel uses **hero headlines as descriptors** (Gele "Fris van kleur. Vol van smaak." etc.).
- Closing: warm cream (others: dark), same copy.
- Key thought: "Dit is de klassieke oesterzwam, maar dan op het niveau van GroMush."

### 2.13 Italiaanse oesterzwam

Brief: `ITALIAANSE OESTERZWAM.pdf` (12 pp, no red; mockup = gele). Empty email, no images in the folder.
Slug implied `/producten/italiaanse-oesterzwam` (confirmed in the Community brief). Positioning: warm, refined, gastronomic. No Italian clichés (flags, red-white-green, Vespas, Tuscany). Accent muted terracotta / warm clay.

- Hero: "**Warm van karakter. Verfijnd van smaak.**" (alt "Karaktervol van kleur. Verfijnd op het bord." — "Ik zou de eerste gebruiken."). CTA "Bestel Italiaanse oesterzwammen →". USPs as grijs.
- Intro: "**Een oesterzwam met een warme uitstraling**" / "De Italiaanse oesterzwam combineert een elegante uitstraling met een uitgesproken culinaire veelzijdigheid. De warme, aardse kleur en stevige structuur maken hem bijzonder geschikt voor gerechten waarin smaak, textuur en presentatie samenkomen." Smaak "Aromatisch & verfijnd" / Textuur "Stevig & sappig" / Uiterlijk "Warm beige tot aardse tinten".
- Smaakprofiel title "**Een verfijnd karakter**", 5/4/4/4. Quote "Warm van karakter, stevig van structuur en gemaakt voor de keuken."
- Timeline as grijs, but 04 reads "Zo vertrekken ze vers vanuit Knokke-Heist naar jouw keuken." Onze kweker block.
- Keuken: "Dankzij zijn stevige structuur en verfijnde smaak is de Italiaanse oesterzwam bijzonder veelzijdig. Bak hem goudbruin, grill hem kort of verwerk hem in een gastronomische bereiding waarin de paddenstoel zelf centraal mag staan." Grid:
  - Gebakken: "Karamelliseer de randen…"
  - Gegrild: "Ideaal voor een krachtige, licht geroosterde smaak."
  - Geroosterd: "Mooi als onderdeel van warme groenten…"
  - Pasta & risotto: "Een natuurlijke combinatie met romige en hartige bereidingen."
  - Sauzen: "Geeft extra diepte aan sauzen en jus."
  - Gastronomisch: "Een elegante keuze voor verfijnde borden."
- Editorial photo: "ITALIAANSE OESTERZWAM / Voor gerechten waarin eenvoud en karakter samenkomen." No chef, no logo.
- Voor wie "Voor elke keuken die iets bijzonders wil": CHEFS "Voor verfijnde gerechten…" / THUISKEUKEN "Veelzijdig in elke bereiding / Van eenvoudig gebakken tot een uitgebreid diner." / VEGETARISCHE KEUKEN "Een stevige basis…".
- Product info: Verpakking; Beschikbaarheid "afhankelijk van oogst en seizoen"; Herkomst GroMush, Knokke-Heist; Levering "lokale professionele levering / rechtstreeks vanuit de kwekerij".
- Others carousel lists **only Gele, Roze, Witte, Blauwe, Grijze** with hero headlines.
- Closing: cream, same copy.

---

### 2.14 Binnenkweek: "Ons kweekproces — Binnenkweek in 4 fases"

Brief: `Binnenkweek-proces-webpagina.pdf` (10 pp, red copy; mockup p1). Email lists Drive files: Anthony photo, zeecontainer photo, 4 phase zips.
Purpose: a behind-the-scenes look at the indoor process. Communicate Ambacht / Kennis / Versheid. Must be **authentic**: show the current indoor bucket growing, and do not suggest all production happens in a food forest.

- **Hero** (300–380px, near-black to forest). Grey oysters growing from straw. Overline "**VAN STRO TOT VERSE ZWAMMEN**". Title "**Ons kweekproces**" / "**Binnenkweek in 4 fases**" ("in 4 fases" in olive). Intro "**Ambachtelijk, duurzaam en met respect voor het natuurlijke ritme van de paddenstoel. Ontdek hoe we stro en broed omvormen tot verse oesterzwammen, met aandacht voor iedere stap.**"
- **4 phase blocks.** 42/58 split: info left, documentary photo right with a round tip badge. Big olive number, 3 benefits, a sage info panel with icons.
  - **FASE 1 — Pasteurisatie met koud water.** "We laten het stro in zakken 24u weken in koud water, zodat het substraat voorbereid wordt op de volgende stap. Daarna laten we het overtollige water 24u uitlekken."
    - Benefits: Een eenvoudige voorbereiding van het stro. / Ongewenste omstandigheden voor de kweek zoveel mogelijk beperken. / De structuur van het stro behouden.
    - Panel "Zo werkt het": 1 Stro in uienzakken → 2 Weken onder water → 3 Laten uitlekken → 4 Klaar voor gebruik.
    - Tip: "Gebruik schoon, koud water en laat het stro goed uitlekken."
    - Show "24 uur" only if it matches the actual protocol.
  - **FASE 2 — Opbouw in lagen in 20L-emmers.** "We verdelen het voorbereide stro en het paddenstoelenbroed in afwisselende lagen over onze 20-literemmers. Zo krijgt het mycelium de kans om zich door het substraat te verspreiden."
    - Benefits: gelijkmatige verdeling / gestructureerde opbouw / praktische en schaalbare kweekmethode.
    - Panel "Opbouw in lagen": Laag stro → Laag broed → Herhalen tot de emmer gevuld is → Licht aandrukken, niet verdichten, with stylised bucket cross-sections.
    - Tip: "Vul de emmer zonder het substraat te sterk samen te drukken."
  - **FASE 3 — Incubatie: het mycelium neemt over.** Title "3. Incubatie — ongeveer 2 weken". "In de incubatieruimte krijgt het mycelium de tijd om het stro te koloniseren. We houden de omstandigheden zo stabiel mogelijk en volgen de ontwikkeling van de emmers op."
    - Benefits: donkere ruimte / gecontroleerde temperatuur / goede luchtkwaliteit.
    - Panel: "20–24°C als richtwaarde" / "Weinig tot geen licht" / "Ongeveer 2 -3 weken" / "Voldoende ventilatie".
    - Tip: "Controleer of het mycelium het substraat voldoende heeft gekoloniseerd voordat je naar de volgende fase gaat."
  - **FASE 4 — Fruiting: de oesterzwammen groeien.** Title "4. Fruiting — de groei en oogst". "Wanneer het mycelium voldoende ontwikkeld is, verhuizen de emmers naar de fruitingruimte. Met passende temperatuur, hoge luchtvochtigheid, licht en voldoende luchtverversing stimuleren we de vorming van verse oesterzwammen."
    - Panel: Temperatuur per soort / Hoge luchtvochtigheid / Gerichte vochtsturing / Groei en opvolging. "85–95%" only if accurate. Replace "minimum 2 weken" with species-dependent wording.
    - Tip: "Houd het klimaat stabiel en stem de luchtverversing af op de groei."
    - This is the visual highlight, with purple light if real.
- **Oogst & levering banner.** "**Na de groei oogsten we onze oesterzwammen op het juiste moment. We verpakken ze met zorg en brengen ze vers naar chefs, winkels en andere lokale klanten.**" Icons: Vers geoogst / Met zorg verpakt / Lokaal geleverd / Dagverse kwaliteit.
- **Footer CTA.** "Natuurlijk proces. Ambachtelijk gekweekt. Voor de beste smaak." Button "**Ontdek onze zwammen**" to the overview.
- Animations: progress line through the phases, fades. No parallax or carousel. Mobile: each phase a vertical card.
- **Mockup extras not in the text:**
  - Nav: Home, Over GroMush, Onze zwammen, Kweekproces, Voor chefs, Contact + "Bestel proefbox".
  - Phase 1 "12–24 uur" and "Uit laten lekken 30–60 min" (contradicts the 24h text).
  - "Fruiting — minimum 2 weken".
  - A block "**Word eigenaar van GroMush emmers**" (Ontdek onze GroMush emmers).
  - "**Over de kweker Anthony Watteeuw**".
  - "**Lokaal in Knokke-Heist, Damme & Brugge**" with the van.
  - "Klaar om lokaal het verschil te maken? Bestel gratis proefbox".
  - Footer strip with phone "+32 479 36 32 01" (fake) and "Geen pesticiden of schadelijke stoffen".

### 2.15 Buitenkweek: "Puur natuur, biologisch en regeneratief" (+ Extra Blok)

Brief: `Buitenkweek-pagina-website-gromush.pdf` (16 pp, no red; mockup p1). Empty email. Folder has 5 technique photos, `hero-buitenkweek.jpeg` and `voedselbos.jpeg`.
**The PDF text is truncated**: it ends mid-sentence in section 12 ("Hero-titel ongeveer"). The nav-link list in section 3 is also missing ("in deze volgorde:" followed by nothing).
Purpose: introduce outdoor log growing in a protected organic food forest and invite people to **become owner of their own set of logs**. Central message "**Puur natuur, biologisch en regeneratief.**" Palette: #10190B, moss #75882D, ivory #F4F1E8, wood #745333.

- **Nav.** Transparent over the hero, active "Buitenkweek", button "**Bestel proefbox →**". Mockup nav: Home, Over GroMush, Binnenkweek, Buitenkweek, Word eigenaar, Voor chefs, Contact.
- **Hero** (410–500px). Stacked logs with oysters and lion's mane in a sunlit food forest. Label "BUITENKWEEK". H1 "**Puur natuur, / biologisch en / regeneratief**" ("regeneratief" in moss). Intro "**Sommige smaken kunnen alleen door de natuur worden gecreëerd. Onze buitengekweekte paddenstoelen groeien langzaam op boomstammen in een beschermd biologisch voedselbos.**" Icons: Biologisch / Duurzaam / Regeneratief / 100% natuurlijk. No buttons.
- **Wat is een voedselbos?** (35/65). "Een voedselbos is een duurzaam ecosysteem waarin bomen, struiken, kruiden, bloemen, insecten en schimmels samenleven zoals in een natuurlijk bos. Zonder pesticiden, met maximale biodiversiteit en respect voor de natuur. De boomstammen waarop onze paddenstoelen groeien maken deel uit van deze natuurlijke kringloop. Zo werken wij samen met de natuur, niet ertegen." CTA "**Meer over ons voedselbos**" (no target page exists). Forest path photo at 2.1:1.
- **Ons biologische kweekproces** (6 cards):
  1. Selectie van biologische boomstammen: "Gezonde hardhouten stammen worden zorgvuldig geselecteerd."
  2. Inoculeren: "We boren gaten en brengen zorgvuldig biologisch broed in de stammen aan."
  3. Afsluiten met natuurlijke was: "De gaten worden afgesloten met natuurlijke was om uitdroging en infecties te helpen voorkomen."
  4. Incubatie: "De stammen worden gestapeld en krijgen de tijd om het mycelium te laten doorgroeien." (mockup: "6 tot 18 maanden")
  5. Vruchtvorming: "Wanneer de omstandigheden gunstig zijn, verschijnen de eerste paddenstoelen."
  6. Oogsten: "Met de hand geoogst op het juiste moment, voor een optimale smaak en kwaliteit."
- **EXTRA BLOK** (inserted in the PDF; verbatim): "Ik wil dat je een nieuwe kolom maakt met toekomstige paddenstoelen die worden gekweekt. Alle paddenstoelen worden verstuurd via mail, jij plaatst ze mooi naast elkaar met een kort woordje uitleg eronder. **Je kan er niet op klikken!**"
  - The images are in the separate email "Extra Blok !!! Buitenkweek" (`Buitenkweek-paddenstoelen.zip`, 8 PNGs): Morieltje, Shiitake, Paarse ridderzwam, Judasoor, Wijnrode stropharia (tuinreus), Reishi, Nameko, Pioppino.
  - **The "kort woordje uitleg" texts are not supplied.**
- **Word eigenaar van jouw eigen boomstammen** (dark, 35/65). "Bij GroMush kan je investeren in een eigen set biologische boomstammen. Iedere set wordt voorzien van verschillende soorten paddenstoelenstammen, zoals shiitake, pruikzwam en oesterzwammen." / "Wij verzorgen de volledige kweek, opvolging en het onderhoud in ons beschermd voedselbos." Italic accent "Jij geniet van de oogst en volgt online de ontwikkeling van jouw boomstammen." CTA "**Ontdek de formules**". Photo with wooden ID tags GRO-001 Shiitake / GRO-002 Pruikzwam / GRO-003 Oesterzwam Grijs / GRO-004 Zomeroesterzwam.
- **6 reasons bar:**
  - Persoonlijke boomstammen: "Jouw eigen set, jouw eigen oogst."
  - Biologisch voedselbos: "…zonder pesticiden, volgens de gekozen kweekmethode."
  - Volledig onderhouden: "Wij doen het kweekwerk, jij volgt mee."
  - Meerdere oogsten: "Het oogstritme hangt af van de soort en de omstandigheden."
  - Productief gedurende meerdere jaren
  - Voor gezinnen en bedrijven: "Een tastbare, lokale en natuurlijke ervaring."
- **Closing CTA.** "**De natuur groeit op haar eigen tempo. Ontdek hoe jij deel kunt uitmaken van het GroMush voedselbos.**" Button "**Word eigenaar van jouw boomstammen**" (to the formulas section or the adoption page).
- **Footer.** "Ambachtelijk gekweekt" / "**Puur natuur. Eerlijke smaak.**" Blocks: "Biologisch gekweekt in een beschermd voedselbos." / "Met respect voor de natuur." / "Voor chefs, fijnproevers en iedereen die bewust kiest voor kwaliteit."
- The responsive section is cut off.

---

### 2.16 Local landing page: Knokke-Heist

Brief: `LOKALE LANDINGSPAGINA KNOKKE-HEIST .pdf` (24 pp, no red; mockup p1 shared by all 5 landing PDFs). Email: one Drive image.
Purpose: a visual story of GroMush's home base. Route visitors to chefs/grootkeukens/speciaalwinkels/community/Ons verhaal/contact/Chef Box. Main conversion: **gratis Chef Box** for chefs.
Nav: active category "**Locaties**", yellow CTA "**Gratis Chef Box**". Mockup nav: Home, Over ons, Locaties, Producten, Community, Contact.
SEO title "**Lokale oesterzwammen in Knokke-Heist | GroMush**". Meta "Ontdek GroMush in Knokke-Heist: ambachtelijk gekweekte oesterzwammen voor restaurants, grootkeukens, speciaalwinkels en particulieren."
Palette (shared with all landing pages): #10251A, #1C3828, #48664A, #DDE4D2, #F5F2E8, #17251B, #E8BF59.

Sections:
1. **Nav.** Sticky, darkening on scroll.
2. **Hero** (520–650px). Knokke-Heist coast/promenade at golden hour plus a wooden crate of grey/white/yellow/pink oysters. Overline "ONZE LOCATIE". H1 "**Knokke-Heist.**" Sub "**Van onze kwekerij naar de topkeuken en jouw tafel.**" Intro "Knokke-Heist is de plek waar onze reis vertrekt. Vanuit onze lokale kwekerij brengen we verse, ambachtelijk gekweekte oesterzwammen naar restaurants, grootkeukens, speciaalwinkels en particulieren in de regio." Handwritten "**Lokaal gekweekt. Voor een bewuste toekomst.**" Staggered 1–1.4s intro.
3. **Gastronomische regio.** "EEN UNIEKE REGIO / **Gastronomie, natuur en lokale kwaliteit.**" / "Knokke-Heist heeft een uitgesproken culinaire identiteit, waar smaak, presentatie en kwaliteit een belangrijke rol spelen… we willen de afstand tussen kweker en gebruiker zo klein mogelijk maken." Icons: Lokale kweek / Bewuste keuzes / Culinaire veelzijdigheid / Persoonlijk contact. Photo overlay "Knokke-Heist / Een culinaire hotspot met een lokaal verhaal." No claims about partners.
4. **Voor wie leveren we in Knokke-Heist?** (dark). "SAMEN MET DE REGIO". 4 cards:
   - Voor chef-koks: "Geef je gerechten meer karakter met verse oesterzwammen, een bijzondere textuur en een wereld aan culinaire mogelijkheden." / "Ontdek voor chefs"
   - Voor grootkeukens: "Ontdek hoe lokaal gekweekte oesterzwammen een veelzijdige aanvulling kunnen zijn op professionele menu's."
   - Voor speciaalwinkels: "Breng karaktervolle paddenstoelen naar klanten die bewust kiezen voor smaak, kwaliteit en een lokaal verhaal." / "Ontdek voor winkels"
   - Voor onze community: "Ontdek de wereld van paddenstoelen via inspiratie, culinaire ideeën, activiteiten en gedeelde nieuwsgierigheid." / "Ontdek de community"
5. **Ons verhaal.** "**Van de kust, voor de kust.**" / "GroMush vertrekt vanuit een fascinatie voor paddenstoelen, hun natuurlijke groeikracht en hun plaats in onze voeding. Vanuit onze kwekerij in de regio Knokke-Heist… Zo bouwen we stap voor stap aan een lokale samenwerking tussen kweker, keuken en community." Link "Ontdek ons verhaal".
6. **Locatie & contact** (compact sage card). "DICHTBIJ GEKWEEKT / **Onze uitvalsbasis: Knokke-Heist.**" / "Vanuit Knokke-Heist bouwen we aan lokale samenwerkingen… We horen graag van je." "Neem contact op". **No map pin unless the farm address is public.**
7. **Gratis Chef Box.** "PROEF HET VERSCHIL / **Ontdek GroMush. Proef het zelf.**" / "Ben je chef-kok en wil je onze oesterzwammen leren kennen? Vraag je gratis Chef Box aan en ontdek zelf de smaak, textuur en culinaire mogelijkheden van onze kweek." Button "**Vraag je gratis Chef Box aan →**". No invented conditions.
8. **Footer** (existing).

- Detailed animation timings: hover 200–350ms, text 400–650ms, images 500–800ms, stagger 70–120ms. Reuse the existing library (GSAP/Framer). Intersection Observer, once only. Respect reduced motion.
- **Mockup:** "Gratis Chef Box aanvragen", fake phone +32 472 45 67 89, icon "Biologisch en duurzaam", "Onze locatie / De perfecte uitvalsbasis voor lokale levering in de hele regio".

### 2.17 Local landing page: Brugge

Brief: `_drive/LOKALE LANDINGSPAGINA BRUGGE .pdf` (11 pp, no red; Knokke mockup). Email: Drive PDF + 3 Unsplash photos.
**Gives explicit routes:** `/voor-wie/chefs`, `/voor-wie/grootkeukens`, `/voor-wie/speciaalwinkels`, `/community`, `/ons-verhaal`, `/contact`, `/chef-box`. (Same list in Damme, Blankenberge and Sluis.)
Sub-areas: Sint-Andries, Sint-Kruis, Assebroek, Koolkerke, Dudzele, Male. Shop examples: Ezelstraat, Langestraat, Katelijnestraat.
Rule: Brugge is a **delivery/partner region**, not the farm location. The farm is in "Knokke-Heist/Westkapelle".
Mood: heritage, reien, Michelin, gold afternoon light, brick + forest green. Rhythm dark–light–dark–light–dark. Nav as Knokke.

- **Hero.** "ONZE LEVERINGSREGIO / **Brugge.** / **Verse paddenstoelen voor een verfijnde culinaire traditie.**" / "Vanuit onze kwekerij in de regio Knokke-Heist brengen we dagvers geplukte oesterzwammen naar de keukens, speciaalzaken en fijnproevers van Brugge. Ambachtelijk gekweekt, rijk aan textuur en vol karakter." Handwritten "**Dichtbij gekweekt. Met verfijning geserveerd.**" Crate with grijze, gele, roze, blauwe, Italiaanse oysters.
- **Section 3.** "CULTUUR OP HET BORD / **Waar historisch ambacht en moderne smaak samenkomen.**" Two paragraphs: Brugge's gastronomy, then "Met GroMush leveren we een lokaal polderproduct… met de hand geplukt… stevige textuur, een diepe umamismaak…". Icons: Culinair niveau / Dagverse pluk / Duurzame herkomst / Persoonlijk contact. Overlay "Brugge. Een stad met smaak."
- **Section 4.** "VERBONDEN MET DE STAD / Voor wie leveren we in Brugge en omgeving?" / "Van ambitieuze keukenchefs tot ambachtelijke speciaalzaken en nieuwsgierige thuiskoks: ontdek hoe GroMush verfijning brengt in jouw keuken." Cards:
  - Chefs: "Verrijk je menukaart met dagverse oesterzwammen van topkwaliteit, unieke variëteiten en een ongeëvenaarde vlezige textuur."
  - Grootkeukens: "Kies voor een voedzaam, duurzaam en betrouwbaar lokaal ingrediënt…"
  - Speciaalwinkels: "Bied je klanten karaktervolle, ambachtelijk gekweekte paddenstoelen met een transparant en eerlijk verhaal."
  - Community: "Sluit je aan bij MushLove: laat je inspireren door recepten, **kweeksets** en de wondere wereld van het mycelium." "Kweeksets" is not offered anywhere else.
- **Section 5.** "**Van Knokke-Heist naar Brugge.**" Mycelium as the metaphor for "een hecht lokaal netwerk"; "zonder omwegen of lange transportroutes."
- **Section 6.** "DICHTBIJ DE BRUGSE KEUKEN / Verse oesterzwammen voor Brugge en de stadsrand." / "…Sint-Andries, Sint-Kruis, Assebroek en omstreken. … We komen graag bij je langs om onze zwammen te laten proeven…" "Bespreek een samenwerking" to `/contact`.
- **Section 7 (Chef Box).** "PROEF HET VERSCHIL IN JOUW KEUKEN / Ontdek GroMush. Proef het zelf." / "Ben je chef-kok of keukenchef in Brugge of omgeving?… Vraag geheel vrijblijvend een gratis Chef Box aan…" to `/chef-box`.
- **Footer** lists "Contactgegevens (E-mail, Telefoon, **Adres kwekerij Knokke-Heist**)". This conflicts with the Knokke brief, which says no address unless public.
- SEO title "Verse oesterzwammen in Brugge | GroMush Korte Keten". H1 "Brugge. Verse paddenstoelen voor een verfijnde culinaire traditie."

### 2.18 Local landing page: Damme

Brief: `LOKALE LANDINGSPAGINA DAMME.pdf` (12 pp, no red). Email embeds 2 Unsplash photos + a Drive webp.
Sub-areas: Oostkerke, Hoeke, Lapscheure, Moerkerke, Sijsele. Mood: rustic polder, Damse Vaart with poplars, Schellemolen, morning mist, Brugse Ommeland. Farm stated as "Knokke-Heist/Westkapelle".

- **Hero.** "ONZE LEVERINGSREGIO / **Damme.** / **Lokale paddenstoelen voor een authentieke polderkeuken.**" / "Vanuit onze kwekerij in de regio Knokke-Heist willen we ook in Damme en de omliggende polderstreek chefs, speciaalzaken en liefhebbers laten kennismaken met verse, ambachtelijk gekweekte oesterzwammen." Handwritten "**In de polder geworteld. Met passie gekweekt.**"
- **Section 3.** "DE SMAAK VAN DE POLDERS / **Poldergastronomie, ambachtelijk geïnspireerd.**" Two paragraphs. Icons: Lokale verankering / Ambachtelijke kweek / Veelzijdig in de keuken / Persoonlijk contact. Overlay "Damme. Een streek met karakter."
- **Section 4.** "SAMEN MET DE STREEK / Voor wie leveren we in Damme en omgeving?" Cards:
  - Chefs: "Geef je poldergerechten extra diepgang met dagverse oesterzwammen, unieke variëteiten en een ongeëvenaarde textuur."
  - Grootkeukens: "…betrouwbaar, voedzaam en lokaal ingrediënt…"
  - Speciaalwinkels: "Bied je klanten dagverse, lokaal gekweekte zwammen met een eerlijk verhaal en uitgesproken kwaliteit."
  - Community: "Word onderdeel van MushLove: laat je inspireren door recepten, kweeksets en culinaire verhalen."
- **Section 5.** "**Van Knokke-Heist naar Damme.**" "…Damme, met haar rijke polderlandschap en culinaire ziel, is voor ons een natuurlijke partner."
- **Section 6.** "DICHTBIJ ONZE POLDERPARTNERS / Verse oesterzwammen voor Damme en de polderstreek." / "…Damme, Oostkerke, Sijsele, Moerkerke en omgeving…"
- **Section 7.** Chef Box: "Ben je chef-kok of keukenchef in Damme of de polderstreek?…"
- SEO title "Verse oesterzwammen in Damme en de polderstreek | GroMush".

### 2.19 Local landing page: Sluis

Brief: `LOKALE LANDINGSPAGINA SLUIS .pdf` (22 pp, no red). Email: Drive crate photo + zips.
Region: Sluis and Zeeuws-Vlaanderen (Dutch border). Mood: historic fortified town, canals, Burgundian food culture, Dutch–Belgian gastronomy, warm evening light. Structure and length mirror the Knokke brief.

- **Hero.** "ONZE LEVERINGSREGIO / **Sluis.** / **Lokale paddenstoelen voor een bourgondische keuken.**" / "Vanuit onze kwekerij in de regio Knokke-Heist willen we ook in Sluis en omgeving chefs, speciaalwinkels en liefhebbers laten kennismaken met verse, ambachtelijk gekweekte oesterzwammen." Handwritten "**Dichtbij gekweekt. Met smaak gedeeld.**" If a composite looks fake, use the Sluis photo plus a separate product photo.
- **Section 3.** "DE SMAAK VAN DE STREEK / **Bourgondisch genieten, lokaal geïnspireerd.**" Three paragraphs. Icons: Lokale samenwerking / Ambachtelijke kweek / Veelzijdig in de keuken / Persoonlijk contact. Overlay "Sluis. Een streek met smaak."
- **Section 4.** "Voor wie leveren we in Sluis en omgeving?" / "Van professionele keukens tot speciaalzaken en liefhebbers…" Card texts are mostly Knokke-like; grootkeukens: "Ontdek een veelzijdig ingrediënt voor professionele menu's, creatieve bereidingen en plantaardige gerechten."
- **Section 5.** "**Van Knokke-Heist naar Sluis.**" "…de verbinding maken met omliggende regio's, waaronder Sluis en Zeeuws-Vlaanderen."
- **Section 6.** "DICHTBIJ ONZE KLANTEN / Verse oesterzwammen voor Sluis en omgeving." / "Vanuit de regio Knokke-Heist willen we lokale samenwerkingen opbouwen… Neem contact op…" No fictitious map.
- **Section 7.** Chef Box: "Ben je chef-kok in Sluis of omgeving?… Vraag je gratis Chef Box aan en proef zelf het verschil."
- SEO title "Verse oesterzwammen in Sluis en omgeving | GroMush". H1 "Sluis. Lokale paddenstoelen voor een bourgondische keuken." Routes listed as "voorstellen".

### 2.20 Local landing page: Blankenberge

Brief: `LOKALE LANDINGSPAGINA BLANKENBERGE.pdf` (11 pp, no red). Empty email; folder has a Blankenberge photo, an Unsplash photo, zips.
Sub-areas: Uitkerke, Zwankendamme, Lissewege, Wenduine/De Haan. Mood: fresh, lively coast, the Pier, zeedijk, Paravang, Uitkerkse Polders, fish bistros, beach bars.

- **Hero.** "ONZE LEVERINGSREGIO / **Blankenberge.** / **Verse oesterzwammen voor een levendige kustgastronomie.**" / "Vanuit onze kwekerij in de regio Knokke-Heist brengen we ambachtelijk gekweekte oesterzwammen naar de keukens, speciaalzaken en liefhebbers in Blankenberge. Dagvers geplukt, vol smaak en dichtbij gekweekt." Handwritten "**Verfrissend lokaal. Met zeewind en smaak.**"
- **Section 3.** "VERS VAN DE KUST- EN POLDERGROND / **Waar de zilte zeelucht en de rijkdom van het polderland samenkomen.**" Text pairs oysters with fish dishes. Icons: Zilte korte keten / Dagverse oogst / Veelzijdig op de kaart / Persoonlijke service. Overlay "Blankenberge. Een stad met dynamiek."
- **Section 4.** "SAMEN MET DE KUSTSTREEK / Voor wie leveren we in Blankenberge en omgeving?" Cards:
  - Chefs: "Breng extra textuur en diepte in je kaart met dagvers geoogste oesterzwammen, bijzondere variëteiten en een uniek polderverhaal."
  - Grootkeukens, speciaalwinkels: variations on the Brugge texts.
  - Community: "…recepten, kweeksets en culinaire verhalen."
- **Section 5.** "**Van Knokke-Heist naar Blankenberge.**" "…Blankenberge slechts een steenworp verwijderd… Zo houden we de keten minimaal en de smaak maximaal."
- **Section 6.** "DICHTBIJ DE KUSTKEUKEN / Verse oesterzwammen voor Blankenberge en de polderstreek." / "…Blankenberge, Uitkerke, Lissewege, Zwankendamme… een **proefproeverij** op maat van jouw keuken."
- **Section 7.** Chef Box: "…ervaar de kwaliteit direct op het werkblad."
- SEO title "Verse oesterzwammen in Blankenberge | GroMush Korte Keten".

---

### 2.21 Community: MushLove

Brief: `COMMUNITY : MUSHLOVE webpagina -gromush.pdf` (16 pp, red copy for most headings; mockup p1). Email: Drive screenshot (B&W photo of a school group in the GroMush food forest with sign "GroMush voedselbos / paddenstoelen op boomstammen").
URL `/community` (from the landing briefs).
Main conversion: "**WORD LID VAN MUSHLOVE — VOLG ONS OP FACEBOOK & INSTAGRAM**". Facebook `https://www.facebook.com/profile.php?id=61594707453474`, Instagram `https://www.instagram.com/gromush.be/`.
Members can: follow the process, see photos and videos of adopted buckets, workshops and cooking sessions, the food forest, order and pick up locally, adopt a bucket, meet others. It also targets schools, youth movements, associations and neighbourhood initiatives.
Palette: #123A2A, #0D2B20, #F5F0E5, #EAE1D0, #D6C6AA, gold #D9B66F, muted pink. Serif + Inter/Manrope, occasional handwriting.

1. **Header.** Cream, logo, CTA "**wordt lid**" (sic), active "Community". Sticky.
2. **Hero.** Person holding a bucket of pink oysters. Label "**MUSHLOVE COMMUNITY**". Title "**Meer dan paddenstoelen. Een lokale community.**" Intro (black) "Bij GroMush draait het niet alleen om kweken en oogsten, maar vooral om verbinden. Met MushLove brengen we mensen, scholen, verenigingen en lokale partners samen rond lekker eten, natuur en duurzaam groeien." Primary "**Word lid van MushLove →**" (to Facebook or a choice page). Secondary "**Ontdek wat je kunt beleven ↓**". Handwritten "**Volg onze reis, deel jouw verhaal en word deel van MushLove.**" Icons: Volg ons proces / Workshops & kooksessies / Ontdek het voedselbos / Samen maken we het lokaal.
3. **Wat kan je doen?** "**Ontdek, beleef, proef.**" / "MushLove is er voor iedereen die meer wil weten, meer wil proeven en meer wil beleven. Of je nu een nieuwsgierige hobbykok bent, een gezin met kinderen, een leerkracht of een vereniging: er is altijd een manier om mee te groeien." 4 photo cards, **all CTAs pointing to the same Facebook URL**:
   - Volg ons proces: "Van mycelium tot oogst. Bekijk onze video's en foto's en ontdek hoe onze oesterzwammen groeien." / Volg het proces
   - Workshops & kooksessies: "Leer over paddenstoelen, ontdek nieuwe smaken en beleef hoe je ze zelf heerlijk klaarmaakt." / Ontdek de activiteiten
   - Bezoek het voedselbos: "Ontdek hoe natuur, voedsel en biodiversiteit samenkomen. Leer, proef en beleef het buiten." / Ontdek het voedselbos
   - Bestel & haal af: "Geniet van verse oesterzwammen uit onze kwekerij. Ontdek het aanbod en bestel om lokaal af te halen." / Bekijk het aanbod
4. **Adopteer een emmer** (dark). "ADOPTEER EEN EMMER / **Jouw eigen oesterzwammen, rechtstreeks van onze kwekerij.**" / "Met een MushLove-emmer haal je een stukje GroMush in huis. Je adopteert een emmer waarin wij het kweekproces begeleiden. Ondertussen volg je hoe jouw oesterzwammen groeien, tot het moment waarop je zelf kunt oogsten. Je krijgt toegang tot updates met foto's en video's van de verschillende groeifasen…" Benefits: Je eigen oogst / Volg de groei / Steun lokaal / Samen leren. CTA "**Ontdek hoe emmeradoptie werkt →**" + "Ik wil een emmer adopteren". **Do not show prices** (this conflicts with €49 on the Adoptie page). Timeline: Adoptie → Mycelium → Kolonisatie → Eerste knoppen → Groei → Oogst.
5. **Van eerste draadje tot eigen oogst.** "Elke emmer heeft zijn eigen verhaal. Via MushLove delen we foto's, video's en updates…" 4 example images with badges MYCELIUM / GROEI / EERSTE KNOPPEN / OOGSTKLAAR. No fake live tracker. CTA "**Volg MushLove op Facebook & Instagram →**".
6. **Scholen & verenigingen.** "SAMEN LEREN, SAMEN GROEIEN / **Ook jouw klas of vereniging hoort erbij.**" / "We willen GroMush laten groeien tot een plek waar mensen elkaar ontmoeten en samen ontdekken waar hun voedsel vandaan komt…" Activities list. CTA "**Organiseer iets samen met GroMush →**" (contact, subject "School of vereniging"). Block "Een idee voor jouw klas, club of buurt? Vertel ons wat je wilt organiseren. Samen bekijken we wat haalbaar is."
7. **Workshops.** "**Samen ontdekken. Samen koken. Samen proeven.**" Tiles: Ontdek de paddenstoel / Koken met karakter / Naar buiten. Each "Ontdek de activiteit →". No invented dates.
8. **Ontdek onze oesterzwammen.** "**VIJF SOORTEN, VIJF KARAKTERS / Ontdek welke oesterzwam bij jou past.**" Cards with slugs:
   - Gele: "Fris van kleur, aromatisch en verfijnd." `/producten/gele-oesterzwam`
   - Roze: "Opvallend, kleurrijk en gastronomisch." `/producten/roze-oesterzwam`
   - Witte: "Puur, zacht en veelzijdig."
   - Blauwe: "Stevig, karaktervol en uitgesproken."
   - Italiaanse: "Warm, verfijnd en gastronomisch."
   "**Belangrijk: de grijze oesterzwam maakt geen deel meer uit van het assortiment en mag nergens in deze productselectie verschijnen.**" "Ontdek deze soort →" / "Bekijk alle oesterzwammen →".
9. **Inspiratie voor thuis.** "VAN PAN NAAR BORD / Je eigen oesterzwammen. Wat maak je ermee?" 3 links. "Ga naar de inspiratiepagina →" (no duplicate recipe page).
10. **Lokale verbinding.** "**Lokaal geworteld. Samen verbonden.**" / "Vanuit Knokke-Heist willen we mensen uit de ruime regio verbinden…" Illustrative map: Knokke-Heist, Sluis, Damme, Blankenberge, Brugge en omgeving. No photo bubbles. "Een lokale community groeit wanneer mensen elkaar vinden." CTA "**Ontdek waar we leveren →**".
11. **Big CTA.** "Word deel van MushLove." / "Volg hoe onze oesterzwammen groeien, ontdek workshops, leer koken, beleef de natuur en ontmoet mensen die net als jij houden van lokaal en eerlijk voedsel. Je hoeft geen kweker of chef te zijn. Nieuwsgierigheid is genoeg." Buttons "Volg MushLove op Facebook →" / "Volg MushLove op Instagram →". "Van kweek tot keuken. Van individu tot community. Samen laten we lokaal groeien."
12. **Footer.** "AMBACHTELIJK GEKWEEKT." + "Geen lange keten…". Links: Onze soorten, Inspiratie, Over GroMush, Community, Contact, **Afhalen en bestellen**. Social: Facebook/Instagram "MushLove".

- **Mockup:** "Voor scholen en verenigingen" (typo), shows 5 oysters, "Laat je inspireren" box, social CTA "Volg ons op Facebook & Instagram", plus cart/account icons.

### 2.22 Adoptie: "Adopteer een emmer of een set boomstammen"

Brief: `Adoptiepagina-emmer-boomstam-website-gromush.pdf` (18 pp, no red; mockup p1). Empty email. Folder has 3 Gemini images (bucket "EMMER-015" in the forest, logs with tags) and a girolle photo.
Palette: #101308, #202715, #596923, #8C9A3B, #F7F6F0, #EAE9DB, #25251E. Serif + Inter/Manrope.

- **Header** (transparent). Nav **Home, Over GroMush, Onze zwammen, Kweekproces, Adopteer (active), Voor chefs, Contact**. Button "**Bestel proefbox ›**".
- **Hero** (~350px). Dark food forest with stacked logs, a white bucket labelled "EMMER-015 — Jouw emmer", a log tag "GRO-042 — Jouw boomstam". H1 "**Adopteer een emmer of een set boomstammen**" ("set boomstammen" in moss). Exact intro "**Word deel van ons groeiproces en geniet van verse, ambachtelijke paddenstoelen recht uit ons biologisch voedselbos.**"
- **Kies jouw manier om deel uit te maken van GroMush.** "Of je nu kiest voor een enkele emmer in onze binnenkweek, of voor een set boomstammen in ons beschermd voedselbos, jij krijgt een uniek kijkje achter de schermen én deelt mee in de oogst."
  - Card 1, "**Adopteer een emmer**": "Kies jouw favoriete oesterzwam en adopteer een 20L kweekemmer in onze binnenkweek." Bullets: Je kiest de soort paddenstoel / Je emmer krijgt een uniek nummer / Volg de groei van jouw emmer / Ontvang de oogst van jouw emmer / Perfect voor particulieren, gezinnen en paddenstoelenliefhebbers. CTA "Adopteer een emmer ›".
  - Card 2, "**Adopteer een set boomstammen**": "Adopteer een set boomstammen in ons biologisch voedselbos en geniet van de natuurlijke rijkdom van buitengekweekte paddenstoelen." Bullets: Verschillende soorten op jouw set / Jouw set krijgt een uniek nummer / Volg de seizoenen en de oogsten / Meerdere oogsten per jaar / Duurzaam, biologisch en regeneratief / Ideaal voor chefs, bedrijven en families. CTA "Adopteer een set boomstammen ›".
- **Wat krijg je als adoptant?** (dark):
  - Uniek inzicht: "Volg het volledige groeiproces van jouw emmer of boomstammen."
  - Jouw eigen oogst: "Ontvang de verse paddenstoelen van jouw adoptie."
  - Duurzaam & lokaal: "Biologisch gekweekt met respect voor natuur en mens."
  - Updates & beeldmateriaal: "Ontvang foto's en updates van jouw kweek."
  - Steun ambacht: "Help mee aan een eerlijk en duurzaam voedingssysteem."
- **Hoe werkt het?** (5 steps):
  1. Kies jouw adoptie: "Kies een emmer of een set boomstammen en jouw favoriete soort(en)."
  2. Wij starten de kweek: "…uniek nummer en wij starten het groeiproces."
  3. Volg de groei: "Je ontvangt regelmatig updates en foto's van de ontwikkeling."
  4. Geniet van de oogst: "Je ontvangt jouw verse paddenstoelen op het juiste moment."
  5. De cyclus gaat door: "Jouw emmer of boomstammen blijven productief voor vele oogsten."
- **Price cards** (to be centrally configurable):
  - **Emmer adoptie** / 20L binnenkweek / **€ 49 / per cyclus**: 20L kweekemmer met jouw nummer / Keuze uit diverse oesterzwammen / 1 volle oogst (ca. 2–3 kg) / Updates tijdens de kweek / Ophalen of levering mogelijk.
  - **Boomstammen adoptie** / Set van 4 stammen / **€ 249 / per jaar**: Set van 4 geïnoculeerde stammen / Verschillende soorten paddenstoelen / Meerdere oogsten per jaar / Updates & seizoensinfo / Onderhoud en kweek volledig door GroMush.
  - Note: "De cyclus gaat door / productief voor vele oogsten" conflicts with "1 volle oogst" per cycle.
- **Closing banner.** "**Word deel van iets echts.**" / "Adopteer vandaag nog jouw emmer of set boomstammen." CTA "**Ik wil adopteren ›**".
- **Footer values:** **Biologisch gecertificeerd** / Lokaal en ambachtelijk / Duurzaam en regeneratief / Transparant en eerlijk / Met liefde gekweekt. "Biologisch gecertificeerd" conflicts with the many "no unconfirmed bio claim" rules.
- **Adoption flow:** choose → price/conditions → preferences → contact data → review → confirm via existing payment integration. **No fake payment.** There is no backend yet.

### 2.23 Over ons: "Over GroMush | Wie is Anthony Watteeuw?"

Brief: `over ons - pagina - website - gromush.pdf` (23 pp, no red; mockup p1). Empty email.
Folder:
- real `familie-watteeuw-anthony.jpg` (Anthony, partner and 4 children, selfie)
- real `Schermafbeelding … 21.59.20.png` (Anthony as a cameraman with a Steadicam-type rig)
- `file_000…png` (Anthony with a crate in the grow room, AI-styled)
- a banner "Lokaal. Ambachtelijk. Buitengewoon." with "MushLove" handwriting
- 2 Unsplash images

URL: `/ons-verhaal` per the landing briefs; the nav label is "Over ons" or "Over GroMush" depending on the brief. SEO title "**Over GroMush | Het verhaal van kweker Anthony Watteeuw**". Meta "Ontdek het verhaal achter GroMush: de passie van Anthony Watteeuw voor ambachtelijk gekweekte oesterzwammen, gezonde voeding, lokale teelt en leven in harmonie met de natuur."
Palette: #18230F, #283516, #56651F, #78842F, #F5F1E7, #FBF9F3, #EAE4D8, #171713. Serif (Cormorant/Playfair/Lora) + Inter/Manrope + Caveat accents.

- **Nav.** Home, Over GroMush (active), Onze zwammen, Kweekproces, **Voedselbos, Beleving, Word mede-eigenaar**, Contact. CTA "**Reserveer nu**" with a calendar icon, to a "reservatie- of contactflow". **No reservation flow is defined anywhere.**
- **Hero** (460–500px). Warm grow-room photo.
  - Left: "Wie is / **Anthony Watteeuw?**" ("Anthony" in olive). Subtitle "**Kweker. Dromer. Vader. Verbinder.**" Intro "Ik ben Anthony, oprichter en kweker bij GroMush. Mijn reis bracht me van de wereld van beeld en film naar de wondere wereld van paddenstoelen. Wat begon als nieuwsgierigheid, groeide uit tot een diepe passie en een missie: **gezonde voeding, lokale teelt en pure beleving delen met zoveel mogelijk mensen.**" CTA "Ontdek ons verhaal" scrolls to "Mijn verhaal".
  - Centre: Anthony with crossed arms in a GroMush apron. Use the real photo; do not alter his face.
  - Right: handwritten quote "**De natuur heeft alle antwoorden. Wij moeten alleen luisteren en zorgen.**" — Anthony. Oysters growing at the bottom right.
- **Mijn verhaal**, "Een pad van creatie naar cultivatie." 5 story cards:
  1. **De wereld van beeld**: "Van jongs af aan had ik een passie voor verhalen vertellen in beeld. Als cinematograaf en cameraman werkte ik voor TV & Film en bouwde ik mijn eigen productiehuis uit. Talloze ervaringen, reizen en projecten leerden me kijken, doorzetten en creëren."
  2. **Vader worden**: "Toen onze 4 kinderen kwamen, verschoof alles. Ik wilde er zijn. Echte momenten. Ik koos ervoor om meer thuis te zijn en mijn leven anders in te richten. Mijn focus kwam te liggen op wat echt belangrijk is: familie, gezondheid en bewust leven."
  3. **Gezonde keuzes**: "Als pescotariër ontdekte ik hoe voeding je energie, gezondheid en geluk bepaalt. Ik verdiepte me in de voedingswaarde van paddenstoelen: een natuurlijke krachtpatser vol eiwitten, vitaminen en mineralen. Een plantaardig superfood met ongelooflijke voordelen." (A health/superfood claim; the Grootkeuken brief forbids superfood language.)
  4. **De magie van mycelium**: "Ik raakte gefascineerd door mycelium, het 'internet van de natuur'. … Ik begon ze te kweken. Thuis. Voor mijn gezin, familie en vrienden."
  5. **Een missie geboren**: "Wat begon als een kleine passie, groeide uit tot een droom: een ambachtelijke kwekerij waar kwaliteit, duurzaamheid en beleving centraal staan. Vandaag deel ik die beleving met onze lokale gemeenschap."
- **Waar ik voor sta** (5 values):
  - Natuurlijk & biologisch: "**We werken 100% biologisch** en met respect voor de natuur." (Unverified claim.)
  - Lokaal & eerlijk: "We telen lokaal in Knokke-Heist en leveren in Knokke, Damme en Brugge."
  - Gezondheid eerst: "Voeding die voedt. Echt, puur en boordevol goede eigenschappen."
  - Beleving delen: "Van rondleiding tot proeverij, we brengen mensen dichter bij de natuur en elkaar."
  - Duurzaam denken: "We bouwen aan een toekomst waarin mens en natuur samen groeien."
- **Filosofie + familiefoto.** Quote "Ik geloof in de kracht van eenvoud, de wijsheid van de natuur en de magie die ontstaat wanneer we zorg dragen voor elkaar en onze planeet. Samen kunnen we een gezondere, mooiere toekomst kweken." — Anthony Watteeuw. Traits:
  - Kweker met een hart: "Ik kweek niet alleen paddenstoelen, ik kweek verbinding."
  - Levensgenieter: "Koken, natuur, reizen en tijd met mijn gezin geven me energie."
  - Altijd blijven leren: "De natuur is mijn grootste leraar. Elke dag ontdek ik iets nieuws."
  Photo of Anthony with his 4 children in the farm. Use the real photo or a placeholder.
- **Laten we samen groeien** (dark). "GroMush is meer dan een kwekerij. Het is een beweging. Een lokaal verhaal, met grote dromen. Voor onze kinderen. Voor jouw gezondheid. Voor onze planeet." / "Bedankt dat je deel uitmaakt van dit verhaal." CTAs "**Ontdek onze zwammen**" (product page) and "**Kom langs & beleef**" (visit/reservation/contact). Three cards: Ambachtelijk gekweekt "Met liefde en vakmanschap." / In harmonie met de natuur "Duurzaam en respectvol." / Voor mens & milieu "Gezond, lokaal en eerlijk."

### 2.24 Contact

Brief: `Contact-pagina-website-gromush.pdf` (21 pp, no red; mockup p1). Email embeds 6 images.
URL `/contact`. SEO title "**Contact GroMush | Ambachtelijk gekweekte oesterzwammen**". Meta "Neem contact op met GroMush voor verse oesterzwammen, professionele aanvragen, samenwerkingen of vragen over onze lokale paddenstoelenkwekerij." One H1 "Laten we verbinden."
Palette: #153B2D, #0C281F, #356B4A, #A8BBA2, #F7F5EE, #EAE5D8, yellow #E6C65B, #252923. **Rounded sans-serif** typography (like Speciaalwinkels). Goals: route visitors fast, convince pros to request the **gratis Chef Box**, strengthen the brand.

- **Nav.** Logo + "ambachtelijk gekweekt", active "Contact", CTA "**Gratis Chef Box**" (yellow) to the Chef Box page. Mockup nav: Home, Over ons, Locaties, Producten, Community, Contact.
- **Hero** (forest gradient, hands holding oysters). Label "CONTACT · GRO MUSH". H1 "**Laten we verbinden.**" (the mockup says "Laten we verbinding maken."). "Heb je een vraag, wil je samenwerken of meer weten over onze oesterzwammen? We horen graag van je." + "Of je nu chef-kok, inkoper, speciaalzaak, thuiskweker of nieuwsgierige liefhebber bent: bij GroMush begint een mooi verhaal vaak met een eenvoudig gesprek." Optional handwriting "Samen laten groeien." CTAs "**Stel je vraag**" (scroll to form) and "**Ontdek onze oesterzwammen**".
- **Hoe kunnen we jou helpen?** Label "VOOR WIE KWEKEN WE?". "GroMush brengt verse, ambachtelijk gekweekte oesterzwammen naar mensen en organisaties die bewust kiezen voor smaak, kwaliteit en een lokaal verhaal." 4 cards:
  - Voor chef-koks: "Geef je gerechten extra karakter met verse oesterzwammen in verschillende kleuren, structuren en smaken. Ontdek welke variëteiten bij jouw keuken passen." / **Ontdek de Chef Box**
  - Voor grootkeukens: "Op zoek naar een veelzijdig plantaardig ingrediënt voor jouw keuken? Bespreek met GroMush welke producten en volumes aansluiten bij jouw behoeften." / **Bespreek je aanvraag**
  - Voor speciaalwinkels: "Wil je jouw klanten laten kennismaken met bijzondere oesterzwammen?…" / **Verken de mogelijkheden**
  - Voor de community: "Ben je gepassioneerd door paddenstoelen, voeding, duurzaamheid of zelf kweken?…" / **Word deel van het verhaal**
- **Ontdek onze verse oesterzwammen** (dark). "VAN KLEUR TOT KARAKTER". "Van zacht en verfijnd tot uitgesproken en karaktervol: iedere oesterzwam heeft een eigen uitstraling, textuur en culinaire mogelijkheden." 6 cards (**includes grey**):
  - Witte: "Zacht van kleur, veelzijdig in de keuken."
  - Gele: "Een opvallende kleur en een verfijnde uitstraling."
  - Roze: "Een kleurrijke verschijning die meteen opvalt."
  - Blauwe: "Een karaktervolle verschijning met een koele kleurtoon."
  - Grijze: "Een herkenbare klassieker met een robuuste uitstraling."
  - Italiaanse: "Een elegante variëteit met een uitgesproken presentatie."
  CTA "Bekijk alle oesterzwammen".
- **We horen graag van je** (form left, details right).
  - Label "NEEM CONTACT OP". "Een concrete vraag, een idee voor samenwerking of gewoon benieuwd naar onze paddenstoelen? Laat iets van je horen. Vertel ons waarmee we je kunnen helpen."
  - Fields: Naam* ("Je naam"), E-mail* ("jij@voorbeeld.be"), Organisatie of zaak, **Waarvoor wil je contact opnemen?*** (Chef-kok / restaurant; Grootkeuken; Speciaalwinkel; Community / zelf kweken; Bestellen; Samenwerking; Andere vraag), Onderwerp, Bericht* ("Vertel ons gerust wat je in gedachten hebt…"), privacy.
  - Button "**Verstuur mijn bericht**". Validation, loading, error and success states. Spam protection. No fake success.
  - **Dynamic preselect** of the category from the customer cards.
- **Contact info card.** E-mail "Stuur ons gerust je vraag of voorstel." info@gromush.be (mailto). Phone only if confirmed. Socials. "Bij GroMush houden we het graag persoonlijk. We denken met je mee en bekijken samen welke mogelijkheden er zijn."
- **Geworteld in de streek.** "LOKAAL VERBONDEN". "GroMush vertrekt vanuit Knokke-Heist en bouwt aan een lokaal netwerk rond verse, ambachtelijk gekweekte oesterzwammen. We willen de verbinding versterken tussen kweker, keuken, winkel en liefhebber." + "Neem contact op om te bespreken wat mogelijk is voor jouw locatie en vraag." Region text links: Knokke-Heist, Damme, Sluis, Brugge (Blankenberge omitted) to the location pages. Presented as delivery regions, not branches.
- **Promo CTA.** "VOOR CHEFS / **Ontdek GroMush. Proef het zelf.**" / "Ben je chef-kok en benieuwd wat onze verse oesterzwammen voor jouw keuken kunnen betekenen? Ontdek de mogelijkheden van de GroMush Chef Box." Button "**Vraag de gratis Chef Box aan**".
- **Footer.** "Verse oesterzwammen, met aandacht gekweekt en met liefde voor smaak, natuur en lokaal vakmanschap." Links: Home, Over ons, Producten, **Locaties**, Community, Contact. Email, social, legal.
- Suggested components: ContactHero, CustomerTypeGrid, OysterMushroomGrid, ContactForm, ContactDetails, LocalRegionSection, ChefBoxCTA.

### 2.25 Inspiratie: "Zo bak je oesterzwammen écht lekker"

Brief: `Inspirtie-gerechten-pagina-website-gromush.pdf` (22 pp, no red; mockup p1). Empty email.
Folder: 3 AI pan photos (golden with thyme, yellow oysters in a pan, sizzling pink in cast iron), a ChefBox webp, and `Gerechten.zip` (curry, roasted mushroom "flower", stew with mash, a screenshot).
Four parts: 2 cooking methods, 6 recipe cards opening in a **modal** (hard requirement: no separate recipe pages or routes), a free ChefBox promo, and the existing nav/footer.
Nav: Home, Onze soorten, Over ons, Inspiratie, Community, Contact. Palette as Community.

1. **Hero** (2.3–2.7:1). Dark pan with golden oysters. Label "GROMUSH INSPIRATIE". H1 "**Zo bak je oesterzwammen écht lekker.**" / "Van sappig en zacht tot goudbruin en krokant. Ontdek twee manieren om oesterzwammen te bereiden en laat je inspireren door zes verrassende gerechten." CTAs "Ontdek de twee bakmethodes ↓" and "Ontdek de recepten ↓". USPs: Lokaal gekweekt — in Knokke-Heist / Vers geoogst — rechtstreeks uit onze kwekerij / Ambachtelijk — met zorg gekweekt / Korte keten — van kweker naar keuken.
2. **Eerst vocht. Dan kleur. Dan smaak.** "Oesterzwammen bevatten van nature veel vocht…" Process line 01 VOCHT → 02 VERDAMPEN → 03 OLIE → 04 KLEUR → 05 KRUIDEN.
3. **Two methods:**
   - **METHODE 01, Droog bakken → grillen → boter → kruiden.** "Voor een intense smaak en een mooie, goudbruine korst." 7 steps: Verhit de pan / Voeg de droge oesterzwammen toe (no oil/butter) / Laat het vocht ontsnappen / Voeg olijfolie toe / Grill en kleur / Werk af met boter / Kruid. Accent "*Eerst droog. Daarna bakken. Zo geef je de oesterzwam de kans om mooi te kleuren.*" Photo: dry steel/black pan, no water.
   - **METHODE 02, Koken in water → uitkoken → olie → grillen → kruiden.** "Een alternatieve bereidingswijze waarbij je het vocht eerst laat vrijkomen." 6 steps: Verwarm de pan (beperkt water) / Breng aan de kook / Laat het vocht uitkoken / Voeg olijfolie toe / Bak en grill / Kruid. Accent "*Eerst laten garen in vocht. Daarna de ruimte geven om te kleuren.*" Photo: steel pan with a little bubbling water. No "best method" claims.
4. **Signature tip** (dark). "DE GROMUSH-BEREIDINGSFORMULE / **Geef ze tijd om smaak te ontwikkelen.**" Formula VOCHT → VERDAMPEN → OLIE → KLEUR → KRUIDEN. Tips: Gebruik een ruime pan / Bak niet te veel paddenstoelen tegelijk / Roer niet voortdurend / Kruid op het einde.
5. **Laat je inspireren.** "6 HEERLIJKE RECEPTEN" / "Van een snelle maaltijd tot een verfijnd gerecht. Klik op een recept en ontdek hoe je jouw GroMush-oesterzwammen op een andere manier kunt bereiden." **Exactly 6 cards required, but only 4 recipes are supplied:**
   1. **Forest Pulled Mushroom Burger**, 2 burgers. Full ingredients (300 g oysters, brioche, red cabbage, carrot, rucola, red onion, mayo, mustard, apple vinegar, olive oil, smoked paprika, maple/honey, BBQ sauce) and 4-part method (pulled oysters, boscoleslaw, GroMush-saus, opbouw). "Wat maakt dit gerecht echt GroMush?" Note: it says "jouw **zelfgekweekte** oesterzwammen".
   2. **Geroosterde oesterzwam met kruiden-ghee, miso en citroen**, 4 persons, vegetarian. 800 g–1 kg (yellow/blue/grey clusters). Oven 190°C 25–35 min covered, then 220°C 8–12 min. Inconsistency: the ingredient list says "100 g boter" while the method says "Smelt de ghee". Serving tip "Mijn GroMush-signatuur".
   3. **Vlaamse stoofpot van oesterzwammen met rode wijn**, 4 persons, with mash. Full list and 5 steps. Wine tip (Côtes du Rhône / Merlot).
   4. **Oesterzwammen in romige kokos-curry met rijst** ("GroMush Coconut Curry"), 4 persons. Full list and 6 steps. Tip.
   - Recipes 5–6 are missing. The mockup shows 6 different dishes: Pasta met gele oesterzwam, Bruschetta met roze oesterzwam, Rijstbowl met witte oesterzwam, Burger met blauwe oesterzwam, Soep van Italiaanse oesterzwam, Wok met oesterzwam en seizoensgroenten.
   - The modal example uses "Pasta met gele oesterzwammen" without quantities ("verzin geen hoeveelheden").
   - Prep times are not given for any recipe.
6. **Modal spec.** 900–1100px. Photo, title, intro, prep time, servings, ingredients (left), steps (right), tip, mushroom type, link to the product, optional print. Close via X, outside click or Esc. Focus trap and return. Mobile near-fullscreen. Data model: id, title, image, description, mushroomType, prepTime, servings, ingredients, steps, tip.
7. **Gratis GroMush ChefBox promo** (directly under the recipes). Label "GRATIS CHEFBOX". "**Ontvang onze gratis GroMush ChefBox.**" / "Wil je ontdekken wat je allemaal met onze oesterzwammen kunt doen? Vraag onze gratis ChefBox aan en laat je inspireren door smaak, textuur en nieuwe culinaire mogelijkheden." CTA "Vraag jouw gratis ChefBox aan →". Benefits: Inspiratie met onze oesterzwammen / Culinaire tips en bereidingsideeën / Nieuwe combinaties om te ontdekken / Rechtstreeks verbonden met GroMush. Photo of a box with yellow, pink, white, blue and Italian oysters. Make conditions clear before confirming.
8. **Footer.** Links: Onze soorten, Inspiratie, Over GroMush, Community, Contact, Afhalen en bestellen. Socials "MushLove".

- Acceptance criterion 13: "**De grijze oesterzwam nergens in het actuele assortiment wordt opgenomen.**"

### 2.26 Proefbox push notification (in-site promo overlay) + proefbox request page

Brief: `Proefbox-pushmelding-pagina-website-gromush.pdf` (7 pp, no red; mockup p1). Email embeds the colourful logo and an image.
It is **not a browser push**. It is an in-site promotional modal or card ("geen browser-pushmelding waarvoor bezoekers toestemming moeten geven"). Target: professional clients (chefs, restaurants, grootkeukens, speciaalwinkels).

- **Copy.**
  - Label "PROEF GRO MUSH". Title "**Proef GroMush. Helemaal gratis.**"
  - "Ontdek de smaak, textuur en kleuren van onze ambachtelijk gekweekte oesterzwammen. Vraag jouw gratis proefbox aan en ontdek welke soorten bij jouw keuken passen."
  - Benefits: Lokaal gekweekt / Knokke-Heist; Verschillende soorten / Ontdek onze kleuren en smaken; Rechtstreeks geleverd / Van kweker naar keuken.
  - CTA "**BESTEL JOUW GRATIS PROEFBOX →**" with the subline "Beschikbaar voor professionele klanten in onze leveringsregio."
  - Closing script "**Eerst proeven. Dan samen groeien.**"
- **Visual.** Background #F7F4EA, olive headings and buttons. The open wooden proefbox with white, yellow, pink, blue and grey oysters (matches homepage mockup p48).
- **Behaviour.**
  - Trigger: one calm trigger (on a product/contact page, time on site, or scroll position). Not on first view.
  - Desktop: modal/card, text left and image right, light dim.
  - Mobile: compact, image on top.
  - Remember dismissal per consent rules. Not on every page change. Once per session. Focus management. Reduced motion respected.
- **CTA destination: a dedicated proefbox page.** Title "**Vraag jouw gratis GroMush-proefbox aan.**" Intro "Maak kennis met onze verschillende soorten verse oesterzwammen en ontdek welke variëteiten aansluiten bij jouw keuken."
  - Form: Naam, Naam van restaurant/grootkeuken/winkel, E-mail, Telefoon (optional), Type onderneming, Leveringsgemeente, Gewenste soorten of opmerkingen.
  - Button "**Vraag mijn proefbox aan**". State that it is for professionals in the delivery region. No minimums or dates.
  - Fallback: the contact form with "Chef-kok / restaurant" preselected.

### 2.27 Extra foto content: oesterzwammen

Email "EXTRA FOTO CONTENT - oesterzwammen" (14 Oct). Only a Drive zip `Extra oesterzamfoto's.zip` (158 MB, **106 files**, all Unsplash stock oyster/mushroom photos, e.g. skyler-ewing, ryan-waldman, victor-birai). **No brief or instructions.** Presumably a general image pool. Licensing is fine (Unsplash), but it conflicts with the many "geen generieke stockfoto" rules.

### 2.28 Extra Blok: Buitenkweek

Email "Extra Blok !!! Buitenkweek - webpagina" (13 Oct). Empty body. `Buitenkweek-paddenstoelen.zip` with 8 future outdoor species (see 2.15). Its instructions live inside the Buitenkweek PDF ("EXTRA BLOK !!!!!!!!!!!!!": non-clickable row of future mushrooms with a short explanation each). **Explanatory texts are not provided.**

---

## 3. Cross-cutting findings

### 3.1 Navigation: at least eight different versions

| Source | Items | Header CTA |
|---|---|---|
| Homepage brief (red, authoritative?) | Voor wie? (chefs, grootkeukens, speciaalwinkels, particulieren) · Zwammen (6 oysters) · Over ons · Inspiratie · Contact | none specified |
| Speciaalwinkels | Home · Voor speciaalzaken · Producten · Over ons · Recepten · Contact | "Levering aanvragen" |
| Landing pages (all 5) + Contact mockup | Home · Over ons · **Locaties** · Producten · Community · Contact | "Gratis Chef Box" |
| Inspiratie | Home · Onze soorten · Over ons · Inspiratie · Community · Contact | none |
| Over ons | Home · Over GroMush · Onze zwammen · Kweekproces · **Voedselbos · Beleving · Word mede-eigenaar** · Contact | "**Reserveer nu**" |
| Adoptie | Home · Over GroMush · Onze zwammen · Kweekproces · **Adopteer** · Voor chefs · Contact | "Bestel proefbox" |
| Buitenkweek (mockup; text list missing) | Home · Over GroMush · Binnenkweek · Buitenkweek · Word eigenaar · Voor chefs · Contact | "Bestel proefbox" |
| Chef/Grootkeuken mockups | Home · Onze paddenstoelen · Voor chefs · Voor grootkeukens · Word mede-eigenaar · Inspiratie · Over GroMush · Contact | "Proefbox aanvragen" / "Bespreek jouw behoefte" |
| Onze zwammen | logo + "Bestellen" (to contact form) | "Bestellen" |

Pages that exist but appear in **no** nav: Binnenkweek, Buitenkweek, Community (in some), Adoptie (in some), Locaties overview (no brief for an overview page), the Proefbox/Chef Box page.

Footer link sets also vary. Community/Inspiratie add "**Afhalen en bestellen**", a page with no brief.

### 3.2 URL slugs mentioned

- `/producten/{gele,roze,witte,blauwe,italiaanse}-oesterzwam` (grijze implied)
- `/voor-wie/chefs`, `/voor-wie/grootkeukens`, `/voor-wie/speciaalwinkels` (landing briefs)
- `/voor-speciaalzaken` (Speciaalwinkels brief): **conflict**
- `/community`, `/ons-verhaal`, `/contact`, `/chef-box`
- No slugs for: home sub-pages, onze zwammen, inspiratie, binnenkweek, buitenkweek, adoptie, location pages, proefbox page, afhalen.

The section label "Zwammen" (homepage) vs "Producten" vs "Onze soorten" vs "Onze zwammen" vs "Onze paddenstoelen" is also unresolved. The same applies to "Speciaalwinkels" vs "Speciaalzaken" and "Over ons" vs "Over GroMush" vs "Ons verhaal".

### 3.3 Recurring components (candidates for a shared component/content model)

- **Mycelium line/animation** (SVG path drawing): homepage hero (signature), then progressively subtler (process timelines, region maps, card connectors).
- **Audience "Voor wie" cards** (4: chefs, grootkeukens, speciaalwinkels, thuis/community): homepage block 5, Voor-wie, Contact, 5 landing pages. Copy differs per page.
- **Variety grid/carousel** (6 oysters, round or card photos, taste words, link to product): homepage block 3, Chef, Grootkeuken, Contact, Community, product cross-sell. Each brief has its own descriptor set.
- **Product template** (one entry type, 6 entries), see 2.8.
- **"Onze kweker" block** (identical copy across product pages).
- **"Van kwekerij tot keuken" timeline** (4 steps on product pages, 5 steps on chef/grootkeuken).
- **Region map / town cards** (Knokke-Heist, Sluis, Damme, Brugge, Blankenberge) with mycelium lines: homepage block 2, Chef, Grootkeuken, Community, Contact text links.
- **Free proefbox / Chef Box CTA banner**: homepage block 7, chef, onze zwammen, all landing pages, contact, inspiratie, plus the site-wide push modal.
- **Dark closing banner** "Van onze kwekerij naar jouw bord." on product pages.
- **USP icon rows** (Lokaal gekweekt / Vers geoogst / Ambachtelijk / Korte keten).
- **Forms** (all must post to a real backend, never fake success): Proefbox/Chef Box request, Grootkeuken "Bespreek jouw behoefte" + calculator, Speciaalwinkel "Vertel ons over jouw zaak", general Contact (with category preselect), chef ChefBox/delivery modal, adoption flow, "School of vereniging" contact subject.
- **Recipe dataset + modal** (Inspiratie, also linked from Chef "Bekijk hoe/recept").

### 3.4 Conversion goals by page

| Page | Primary | Secondary |
|---|---|---|
| Home | Bestel je gratis proefbox | Ontdek assortiment / binnen- / buitenkweek / audiences / verhaal |
| Chef | Vraag een proefbox aan | Start een ChefBox; Ontdek onze soorten; Levering per gemeente |
| Grootkeuken | Bespreek jouw behoefte | Offerte, proeflevering, calculator |
| Speciaalwinkel | Contact form (kennismaking/proeflevering/prijs) | "Levering aanvragen" |
| Products | Bestel (destination undefined) | Vraag beschikbaarheid; inspiratie |
| Onze zwammen | Bestellen (contact form) | Proefbox aanvragen; Laat je inspireren; Volg buitenkweek (Facebook) |
| Landing pages | Gratis Chef Box | Audience pages, Ons verhaal, Contact |
| Community | Follow on Facebook/Instagram | Emmeradoptie; school/vereniging contact |
| Adoptie | Adopteer (emmer/boomstammen) | Bestel proefbox |
| Over ons | Reserveer nu / Kom langs & beleef | Ontdek onze zwammen |
| Contact | Form | Gratis Chef Box |
| Inspiratie | Gratis ChefBox | Recipes |

### 3.5 SEO intent

- **Local SEO town pages**: Knokke-Heist, Brugge, Damme, Sluis, Blankenberge, each with a proposed SEO title, meta and H1, plus sub-municipality names for long-tail queries. No location-overview page has been briefed, though "Locaties" appears in the nav.
- **Very long keyword-stuffed image filenames** (e.g. `Grootkeuken-oesterzwammen-verse-paddenstoelen-gerechten-keuken-catering-school-ziekenhuis-zorginstellingen-vers-ambachtelijk-gekweekt-gromush-knokke-heist-kwekerij-lokaal-geleverd-knokke-heist-damme-brugge.png`). The client clearly intends image SEO. They should become clean slugs plus proper alt text. The filenames contain typos ("geteelt", "gekweete", "ambachteljk", "gromuch", "kwerkerij", "Piopino").
- Explicit SEO titles/meta exist for Speciaalwinkels, Contact, Over ons and the 5 landing pages. None exist for home, chef, grootkeuken, products, community, inspiratie or adoptie.
- Several briefs forbid fake structured data (addresses, opening hours, reviews).

### 3.6 Design system: inconsistent across briefs

- **Typography.** Most briefs use an elegant serif (Playfair / Cormorant Garamond / Lora) for headings with Inter/Manrope body and occasional Caveat-style script. **Speciaalwinkels and Contact ask for rounded sans-serif headings** (Manrope / Nunito Sans).
- **Palettes differ per brief.** Forest greens range #10190B…#18230F…#123A2A…#153B2D…#10251A. Accents vary: gold #D9B66F / #E8BF59, mustard #E6D83E, yellow #E6C65B, moss #75882D / #8C9A3B. Briefs say the existing site palette takes precedence, but **there is no existing site**: every brief says "use the existing GroMush components/codebase".
- **Logo.** Asset `Groene GroMush-oesterzwammenlogo.png` is a colourful oyster cluster with leaf, green "GroMush" wordmark and "AMBACHTELIJK GEKWEEKT". There is also a round-badge variant. The flyer uses a different white logo with "PUUR VAN HIER". The mockups each show yet another logo. All briefs say "use the real logo, do not invent one".
- **Homepage interaction model** (full-screen fade "synopsis", no normal scroll page) differs from every other page (normal scrolling editorial pages).

### 3.7 Contradictions, duplicates, errors

1. **Grey oyster in or out of the range.** In: homepage, Chef, Grootkeuken (FAQ lists it), Contact, Onze zwammen, Grijze product page, all product cross-sells. Out: Community and Inspiratie ("maakt geen deel meer uit van het assortiment"; acceptance criterion), flyer (5 varieties), Community "VIJF SOORTEN".
2. **Italiaanse vs Zomeroesterzwam vs Black Pearl.** Same species, two names (Speciaalwinkels uses "Zomeroesterzwam"). Black Pearl replaces Italiaans in the homepage block 3 mockup.
3. **Extra species** (koningsoesterzwam, pruikzwam, shiitake, Black Pearl) appear in some briefs and mockups but not in the 6-product nav or template.
4. **Buitenkweek status.** "Future project, start spring 2027, first harvest spring 2028, never present as active" (Onze zwammen) vs Buitenkweek, Adoptie (€249/yr log sets, "Meerdere oogsten per jaar"), Over ons ("Voedselbos", "Word mede-eigenaar"), Community ("Bezoek het voedselbos") and the Drive screenshot of a school visit to the "GroMush voedselbos", all presenting it as existing.
5. **"Gratis Chef Box" vs paid "ChefBox-abonnementen" vs "Gratis Proefbox".** The chef page uses ChefBox for paid subscriptions and Proefbox for the free trial. Contact, Inspiratie and the landing pages call the free trial the "gratis Chef Box" (slug `/chef-box`). The Inspiratie mockup describes it as recipes and tips. The grootkeuken has "proeflevering". Speciaalwinkels says do NOT promise a free trial delivery. Proefbox push says "for professional clients only", while the homepage and Inspiratie address home cooks too.
6. **Pricing.**
   - ChefBox text (Flex/Select from 1 kg) vs the chef mockup (5/15/25 kg tiers) vs the flyer (€27/kg base with the same discount percentages).
   - Grootkeuken formulas in the text (5/10/10 kg, Partner threshold duplicated) vs the mockup (25/75 kg/op maat). The brief says only use them once guaranteed.
   - Adoption €49/€249 (Adoptie) vs "toon geen prijzen" (Community).
   - Chef ChefBox CTA is just "Prijs" with no price shown.
7. **Organic/"bio" claims.** "100% biologisch" (Over ons), "Biologisch gecertificeerd" (Adoptie footer), "biologisch voedselbos", "100% natuurlijk" (Buitenkweek, flyer), "LOKAAL BIO DUURZAAM" badge (Speciaalwinkels mockup) vs repeated rules: "Gebruik 'biologisch' niet als productclaim zonder bevestigde certificering" (Speciaalwinkels, Contact, Binnenkweek, Knokke).
8. **Health claims.** Over ons ("natuurlijke krachtpatser… plantaardig superfood met ongelooflijke voordelen") vs Grootkeuken ("Geen medische claims. Geen overdreven 'superfood'-taal").
9. **Service-area lists** vary (Blankenberge missing in Chef animation, Contact, Grootkeuken hero and Over ons; Sluis missing in Over ons).
10. **Copy-paste errors.**
    - Chef page Blankenberge card titled "Brugge / Snel geleverd in Brugge".
    - Grootkeuken Blankenberge card "Foto van Brugge / Snel en gekoeld geleverd in Brugge".
    - Grootkeuken Partner "Vanaf 10kg" equals Professioneel.
    - Chef "drie abonnementskaarten" but two defined.
    - Chef Grijze and Blauwe share "Intens · Umami"; Witte has no descriptor.
    - Gele brief "zes kaarten naast elkaar" but five cards.
    - Homepage block 5 "drie kaarten" but four.
    - Onze zwammen "acht productkaarten" but six.
    - Inspiratie "exact zes recepten" but four supplied.
    - Recipe 2 butter vs ghee.
    - Voor-wie "Één kwekerij" (accent typo).
    - Community header CTA "wordt lid" (typo).
11. **Testimonials/cases.** Chef (mobile order item 9) and Grootkeuken (item 13 "Cases") list them; there is no content, and mockups show fabricated quotes. Community and Speciaalwinkels forbid invented testimonials.
12. **Fake phone numbers** in mockups vs the real 0499 24 23 59. Several briefs say: show a phone only if confirmed.
13. **Farm address.** Landing footers list "Adres kwekerij Knokke-Heist". Knokke says no pin/address unless public. The homepage puts the hub at Westkapelle.
14. **Facebook URL** differs between the email signature and the Community brief.
15. **Ordering.** No webshop ("geen winkelwagen"), yet mockups show cart, account and search icons. Product pages have a "Bestel →" button with no defined destination. Community mentions "Bestel & haal af" (local pick-up) and footers "Afhalen en bestellen" (no page).
16. **Binnenkweek timings.** 24h soak/24h drain (text) vs "12–24 uur" and "30–60 min" (mockup). Incubation "ongeveer 2 weken" vs "2–3 weken". Fruiting "minimum 2 weken" in the mockup though the text says to drop it.
17. **Taste descriptors** differ per brief for the same variety (e.g. Gele: homepage "Fruitig • zoet • fris"; Chef "Delicaat · Aromatisch"; Onze zwammen "Zacht en licht fruitig"; flyer "Mild en verfijnd"). One canonical set is needed per variety.
18. **"Kweeksets"** offered on the Brugge, Damme and Blankenberge community cards. Not defined anywhere.
19. **Homepage block 7 headline**: text "Proef het verschil." vs mockup "Proef GroMush. Helemaal gratis." (= push brief).
20. **Contact H1**: "Laten we verbinden." (text) vs "Laten we verbinding maken." (mockup).
21. **Copy register**: mostly "je/jouw"; the flyer and the homepage hero ("uw bord") use "u".

### 3.8 Briefs not readable / incomplete

- All PDFs extracted fine. None image-only.
- **Buitenkweek PDF is truncated** (ends mid-section 12; the nav link list is missing).
- Mockup `Mycelium growth animation.mp4` (175 s) could not be viewed. It is the binding reference for the hero animation.
- Empty-body emails are listed under "How to read the briefs" at the top.

---

## 4. Open questions for the client

**Scope & structure**
1. Which navigation is final? The homepage brief's "Voor wie? / Zwammen / Over ons / Inspiratie / Contact" omits Binnenkweek, Buitenkweek, Community, Adoptie, Locaties and Proefbox. Where do those live: sub-menu, footer, or contextual links only?
2. Is "Voor particulieren" a separate page, or is it the Community page? No brief exists for a particulieren page.
3. Is "Voor wie" a standalone overview page, or only the homepage section?
4. Do you want a "Locaties" overview page (the nav item exists in the landing briefs)? An "Afhalen en bestellen" page? A separate Proefbox/Chef Box request page at `/chef-box`?
5. Confirm URL scheme: `/voor-wie/speciaalwinkels` or `/voor-speciaalzaken`? "Speciaalwinkels" or "speciaalzaken" as the label? "Over ons", "Over GroMush" or "Ons verhaal"?

**Products**

6. Is the **grijze oesterzwam** still in the range? (Community/Inspiratie/flyer say no; the homepage and its own product page say yes.)
7. Is "Italiaanse oesterzwam" the same product as "Zomeroesterzwam" (*P. pulmonarius*)? Which name do we use?
8. Are Black Pearl, koningsoesterzwam, pruikzwam and shiitake sold now, later, or not at all?
9. Please supply one canonical taste/texture description per variety. The briefs contain 4–5 conflicting sets.
10. Product page "Bestel →": where should it go (contact form with product preselected, WhatsApp, email)? Are consumers allowed to order 250 g packs, and how (delivery or pick-up)?

**Offers & pricing**

11. What exactly is the **free box**: "Proefbox" or "Chef Box"? Is it for professionals only or also for home cooks? Contents, conditions, one per business? And is "ChefBox" then the paid subscription?
12. ChefBox subscriptions: two tiers (Flex/Select, from 1 kg, per the text) or three (Basis 5 kg / Select 15 kg / Exclusief 25 kg, per the mockup)? May we publish the flyer prices (€27/kg etc., excl. btw)?
13. Grootkeuken formulas: are 5 / 10 kg per week real? What is the Partner threshold? May volumes and discounts be published given the "opstartfase"?
14. Adoption: are €49/cyclus and €249/jaar final, and can they be shown (the Community brief says no prices)? Is there a payment provider, or is it request-only? What happens after "Ik wil adopteren"?
15. What is "kweeksets" (Brugge/Damme/Blankenberge cards)? Is this a product?

**Outdoor growing / food forest**

16. Does the food forest and log cultivation exist today? If not, should the Buitenkweek, Adoptie (log sets) and Over ons ("Voedselbos", "Word mede-eigenaar") pages follow the 2027/2028 "coming soon" framing from the Onze zwammen brief?
17. Please send the short explanatory texts for the 8 future outdoor species in the "Extra Blok" (morieltje, shiitake, paarse ridderzwam, judasoor, wijnrode stropharia, reishi, nameko, pioppino).
18. Please resend the Buitenkweek PDF (truncated at section 12) and its nav list.

**Claims & data**

19. Is GroMush **certified organic**? If not, "100% biologisch", "Biologisch gecertificeerd" and "biologisch voedselbos" must go.
20. May we publish the phone/WhatsApp number 0499 24 23 59 and a farm address (Westkapelle?) or keep it email-only? Which Facebook page is correct: the signature `61590322125848` or the community `61594707453474`? Is there a separate MushLove Instagram?
21. Health/nutrition statements (Over ons "superfood"): may we keep them, or tone them down per the Grootkeuken rule?
22. Testimonials/cases for Chef and Grootkeuken: do you have real quotes? If not, drop the section.

**Experiences**

23. "Reserveer nu" / "Kom langs & beleef" / rondleiding / proeverij / workshops / school visits: what is actually bookable, and how (form, email, external tool)?
24. "Bestel & haal af": is there a local pick-up point and schedule?

**Content gaps**

25. Inspiratie needs 6 recipes but only 4 were supplied. Please send the other 2, or confirm the mockup's set (pasta geel, bruschetta roze, rijstbowl wit, burger blauw, soep Italiaans, wok). Also prep times for all.
26. Homepage CTAs "Ontdek ons verhaal" and "Word onderdeel van het netwerk": where do they link? (Over ons / Community?)
27. Homepage interaction: confirm the full-screen, fade-transition, scroll-driven "synopsis" model applies only to the homepage, and that other pages scroll normally.
28. Typography: serif headings (most briefs) or rounded sans (Speciaalwinkels/Contact)? Which logo is master (colour oyster logo vs flyer "Puur van hier" logo)? Which tagline(s) besides "Ambachtelijk gekweekt" are approved ("Puur van hier", "Lokaal is lekkerder", "Lokaal. Ambachtelijk. Buitengewoon.")?
29. Photography: many supplied images are AI-generated (ChatGPT/Gemini) or Unsplash stock, yet the briefs insist on real photos. Which are approved for production? Is a real photo shoot planned (Anthony, farm, buckets, van, dishes)? Does the GroMush delivery van exist (it appears in mockups)? Is the La Réserve Knokke photo licensed?
30. Forms: which inbox(es) receive submissions (info@gromush.be for all)? Any CRM? GDPR/privacy policy text?

---

## 5. Asset inventory (notable files)

Paths are relative to `_resources/2026-10-mails-anthony/`. "AI" = AI-generated per filename or appearance. Zips were listed, not extracted. Duplicate zips across folders are identical by checksum.

### Brand / global

| File | Shows |
|---|---|
| `Chefpagina…/Groene GroMush-oesterzwammenlogo.png` (= `Grootkeuken…/_drive/…logo (1).png`, = `Push melding…/ChatGPT Image 4 okt 2026, 09_53_27.png`) | Colour logo: oyster cluster (white, yellow, pink, blue) + leaf, green "GroMush", "AMBACHTELIJK GEKWEEKT" |
| `Grootkeuken…/_drive/GroMush-paddenstoel-kwekerij-…-anthony-watteeuw….png` | Round-badge version of the logo |
| `Chefpagina…/fromules restaurant.jpg` | **Photo of the real printed A5 "Voor restaurants" flyer with the price list** (5 varieties, €27/kg base, discount tiers, 0499 24 23 59, "Puur van hier", "Teelt in België") |
| `Anthony-watteeuw-paddenstoel-kweker-…png` (in Homepage/_drive, Binnenkweek/_drive, Gele/_drive) | Anthony in flat cap and blue shirt with a GroMush crate of mixed oysters in the misty bucket grow room (homepage block 6 photo) |
| `Binnenkwekerij-zeecontainer-gromush-…png` | Purple-lit corridor of buckets with oysters (indoor grow container; AI-styled) |
| `Onze zwammen…/Buitenkwekerij-gromush-…voedselbos….png` | Logs with mushrooms in a meadow/forest |
| `Homepagina…/Mycelium growth animation.mp4` | 175 s, 640×360 mycelium-growth reference video (**binding reference for the hero animation**) |
| `Homepagina…/Schermafbeelding 2026-08-13 om 23.46.25.png`, `…23.46.36.png` | Radial mycelium growth references (white-on-black, watermarked; black-on-white, from Google image search) |

### Homepage zips

| Zip | Contents |
|---|---|
| `Oesterzwammen.zip` (= `soorten-zwammen.zip` in landing/contact folders) | 6 variety photos: gele, grijs-blauwe, grijze, witte, zomer/Italiaanse, roze (SEO filenames) |
| `_drive/Producten.zip` | 5 "ChatGPT Image 3 okt 2026" cut-out oyster clusters (AI) |
| `_drive/Locaties.zip` (also in Grootkeuken) | Town photos: blankenberge.jpg, sluis, brugge-restaurants…, damme-restaurants…, knokke-heist… |
| `_drive/Binnen-buitenkweek.zip` | Binnenkwekerij-zeecontainer + Buitenkwekerij-voedselbos images |
| `Lokaal-netwerk.zip` | 3 "ChatGPT Image 6 okt 2026" (AI), likely region-network/map visuals |

### Audience pages

| File | Shows |
|---|---|
| `Voor-wie…/ChatGPT Image 3 okt 2026, 14_20_02.png` (= Chef `08_28_50`) | Chef plating oysters with tweezers (AI) |
| `ChatGPT Image 3 okt 2026, 14_11_02.png` (Voor wie, Grootkeuken, Contact) | Large kitchen: chef with crates of yellow, pink and white oysters (AI) |
| `Gemini_Generated_Image_olp82bolp82bolp8.jpeg` (Voor wie, Speciaalwinkels) | Greengrocer in a green apron in front of crates of oysters (AI) |
| `MushLove-mushroomgemeenschap in het bos.png` (Voor wie, Community, Contact) | Community in the forest (AI) |
| `voor wie.zip` (in all landing folders) | The 4 audience images above |
| `Chefpagina…/_drive/GroMush-Proefbox-ChefBox-selectie-….png` (+ `.webp` in several folders) | Wooden "GroMush ChefBox" crate with mixed oysters (AI) |
| `Product-zwammen.zip` (Chef, Gele, Grootkeuken, Onze zwammen, Speciaalwinkels) | 6 cut-out oyster cluster images (AI, transparent bg) |
| `Grootkeuken…/Grootkeuken-oesterzwammen-…png`, `Precisie bij het dresseren van paddenstoelen.png` | Large-kitchen / plating images (AI) |
| `Grootkeuken…/_drive/Kweekproces-tot-bord.zip` | Boer en chef met oesterzwammenkist, binnenkwekerij container, chef-kok, Anthony, ChatGPT image: the 5-step timeline |
| `Speciaalwinkels…/mido-art-…`, `odiseo-castrejon-…` (Unsplash) | Shop/produce stock photos |

### Product pages

| File | Shows |
|---|---|
| `Gele…/gromuch-gele-oesterzwam-oogst-ambachtelijk-knokke-heist.png` | Yellow oyster harvest |
| `Gele…/Goudbruin geroosterde paddenstoelenbloem、】【.png` | Roasted mushroom "flower" dish (recipe 2 visual; odd characters in the filename) |
| `Gele…/_drive/Gouden oesterzwammen op bemoste boomstronk.png` | Yellow oysters on a mossy stump |
| `Gele…/Aziatische-keuken-brugge-oesterzwammen-grill-….webp` | Asian-style grilled oyster dish |
| `Gele…/_drive/Van kwekerij tot keuken.zip` | 4 timeline photos (substrate, yellow oysters, Anthony, ChefBox) |
| `Blauwe…/Blauwgrijze oesterzwamcluster.png`, `…op bemoste boomstam.png` | Blue-grey oyster clusters |
| `Blauwe…/Eigenschappen-grijze-oesterzwam-….png` | Grey oyster "properties" image (filename says grijze but sits in the blauwe folder) |
| `Blauwe…/Van kwekerij tot keuken.zip` | Blue oysters with Anthony, blue oyster farm photo, ChefBox, generic photo |
| `Productpagina-wit…/witte-oesterzwam-anthony-watteeuw-….png`, `ChatGPT … 14_31_16.png` | White oyster cluster (cut-out, AI) |
| `Productpagina-wit…/zomer-oesterzwam-kwekerij-….png` | "Zomer"/Italian oyster (in the witte folder) |
| `1_VpAIBoO3uWefTmG-ixjqEw.jpg` (wit, roze, zips) | Generic web image, purpose unclear |
| `productpagina-roze…/roze-oesterzwam-…png`, `zalm-oesterzwam-…png` | Pink/salmon oysters |
| Grijze, Italiaanse | **No images supplied** |

### Process pages

| File | Shows |
|---|---|
| `Binnenkweek…/_drive/Fase-1-pasteurisatie.zip` | 1 phone photo + 1 screenshot (straw soaking): **real** |
| `Fase_2-Innoculatie.zip` | Phone photo (IMG2026…) + screenshot: real |
| `Fase-3_Incubaitie.zip` | 2 phone photos (Sept/Oct 2026): real incubation |
| `Fase_4_oogsten.zip` | "Mistige oesterzwammenkwekerij in emmers.png" + Anthony photo |
| `Buitenkweek…/1791908204329.jpg` … `1791909333504.jpg` (5) | Log-cultivation technique reference collages (chainsaw cutting, drilling, plug inoculation, wax/tape sealing) |
| `Buitenkweek…/hero-buitenkweek.jpeg`, `voedselbos.jpeg` | Hero logs-in-forest and food-forest path images |
| `Extra Blok…/Buitenkweek-paddenstoelen.zip` | 8 future species: morieltje, shiitake, paarse ridderzwam, judasoor, wijnrode stropharia, reishi, nameko, pioppino |
| `Onze zwammen…/shiitake-op-boom.jpeg`, `shiitake-seta-…jpg`, `shiitake.jpg` | Shiitake (on logs) |
| `Onze zwammen…/Paddenstoelen-Zwammen-kwekerij-GroMush-…png` | Mixed species still life: oysters, pink, yellow, shiitake, lion's mane (AI; hero) |

### Local landing pages

| File | Shows |
|---|---|
| `Overdracht van een krat verse paddenstoelen.png` (all landing folders, Contact) | Hand-over of a crate of fresh mushrooms (AI) |
| `Landingspagina-Knokke…/knokke-heist-gromush-…webp` | Knokke-Heist |
| `Landingspagina-Knokke…/La ReserveMeubili_sept23_BA_305.jpg` | Terrace of La Réserve hotel, Knokke (third-party photo; check licence) |
| `Landingspagina-brugge…/brugge-restaurants-…jpg`, `_drive/` 3 Unsplash (linoleum…, melis-gecginci…, shiv-prasad…) | Brugge |
| `landingspagina-damme…/Damme-restaurant-….jpeg`, `damme-levering-….jpeg`, `_drive/damme-restaurants-….webp`, Unsplash mark-pecar, milan-de-clercq | Damme (Damse Vaart etc.) |
| `landingspagina-sluis…/Schilderachtig Sluis aan het water.png` (AI), `xlarge_sluis-pays-bas_….jpg`, Unsplash christian-paul-stobbe, milan-de-clercq | Sluis |
| `landingspagina-blankenberge…/blankenberge.jpg`, Unsplash afaf-fizazi | Blankenberge |

### Community / adoption / about / contact / inspiration / other

| File | Shows |
|---|---|
| `Communitypagina…/Gemini_Generated_Image_uixqe8….jpeg` | White GroMush-branded bucket with oysters, lion's mane and pink oysters (AI) |
| `Communitypagina…/Gemini_Generated_Image_xx3whk….jpeg` | Wooden board engraved "MushLove community by GroMush" with mushrooms (AI) |
| `Communitypagina…/_drive/Schermafbeelding 2026-10-13 om 10.00.48.png` | B&W photo: guide with a school group at logs in the "GroMush voedselbos" (AI-looking) |
| `Communitypagina…/Ontdek,beleef,proef.zip` | workshops.png, volg ons proces.jpeg, Bezoek voedselbos.png, Anthony photo: the 4 activity cards |
| `Adoptie…/Gemini_Generated_Image_a8emp…`, `…pn5s2…`, `…y2ill…` | Bucket "EMMER-0xx" in the forest; logs with GroMush tags "Variëteit: Oesterzwam, Batch #24" (AI) |
| `Adoptie…/girolle-1-0x1080.jpg` | Chanterelles on moss (not mentioned in any brief) |
| `over-ons…/familie-watteeuw-anthony.jpg` | **Real** family selfie: Anthony, partner, 4 children |
| `over-ons…/Schermafbeelding 2026-10-13 om 21.59.20.png` | **Real** Anthony as cameraman with a professional rig ("De wereld van beeld") |
| `over-ons…/file_000000003ac88210ac140c76f615d911.png` | Anthony with a crate in the grow room (AI-styled) |
| `over-ons…/ambachtelijk-gekweekte-paddenstoelen-…anthony-watteeuw….png` | Banner: logo + "LOKAAL. AMBACHTELIJK. BUITENGEWOON." + Anthony with a crate + "MushLove" script |
| `over-ons…/richard-keeler-…`, `skyler-ewing-…` (Unsplash) | Forest / mushroom stock |
| `contactpagina…/kim-leary-…`, `thomas-le-…` (Unsplash) | Mushroom stock (hands, clusters) |
| `Inspiratie…/Goudbruin gebakken paddenstoelen met tijm.png`, `Goudgele oesterzwammen in de pan.png`, `Sissende roze oesterzwammen in gietijzeren pan.png` | Pan shots for the hero and methods (AI) |
| `Inspiratie…/Gerechten.zip` | Romige curry met rijst, geroosterde paddenstoelenbloem, paddenstoelenstoof met puree, a screenshot: recipe photos |
| `Push melding…/ChatGPT Image 4 okt 2026, 09_53_27.png` | Colour logo |
| `EXTRA FOTO CONTENT…/_drive/Extra oesterzamfoto's.zip` | 158 MB, 106 Unsplash stock mushroom photos, no instructions |

PDF mockups (one per brief, mostly page 1) are AI-generated full-page designs. They are useful for layout intent only, not as copy sources.
