# GroMush sitemap

Part of `SPEC-2026-10-19-gromush-site`. Status: approved by Michael, 2026-11-03 (Q12 in `prd.md`).

Anthony's briefs describe about 30 pages under 8 different navigations. This sitemap consolidates them into 26 pages, 5 navigation items and one call to action. Page names are Dutch because they are the site's labels. Template letters refer to the wireframes.

## Primary navigation

```
[GroMush logo]   Zwammen ▾   Voor wie ▾   Ons verhaal ▾   Inspiratie   Contact      [ Gratis ProefBox ]
```

| Item | Dropdown |
|---|---|
| Zwammen | Alle zwammen · Gele · Roze · Witte · Blauwe · Grijze* · Italiaanse oesterzwam |
| Voor wie | Chefs · Grootkeukens · Speciaalzaken · Thuis & MushLove |
| Ons verhaal | Over Anthony · Kweekproces · Buitenkweek · Leveringsregio |
| Inspiratie | (no dropdown) |
| Contact | (no dropdown) |
| CTA | Gratis ProefBox → `/proefbox` |

\* only while the grey oyster is in the range (Q1, R17).

## Page tree

```
/                                   Home                          A  full-screen synopsis
├── /zwammen                        Alle zwammen (overview)       B
│   ├── /zwammen/gele-oesterzwam    Product                       C  (×6, one template)
│   ├── /zwammen/roze-oesterzwam
│   ├── /zwammen/witte-oesterzwam
│   ├── /zwammen/blauwe-oesterzwam
│   ├── /zwammen/grijze-oesterzwam  *Q1
│   └── /zwammen/italiaanse-oesterzwam
├── /voor-wie                       Voor wie (4-way router)       D-lite
│   ├── /voor-wie/chefs             Audience                      D
│   ├── /voor-wie/grootkeukens      Audience + needs helper       D
│   ├── /voor-wie/speciaalzaken     Audience + intake form        D
│   └── /voor-wie/thuis             Thuis & MushLove (community)  D
├── /ons-verhaal                    Over Anthony                  E
│   ├── /ons-verhaal/kweekproces    Binnenkweek in 4 fases        F
│   ├── /ons-verhaal/buitenkweek    Plan + interest (nothing exists yet)  F
│   └── /ons-verhaal/adopteer       Adopteer een emmer  F + form
├── /inspiratie                     Methods + recipe dialogs      G
├── /leveringsregio                 Region hub + map              H-lite
│   ├── /leveringsregio/knokke-heist   Town landing               H  (×5, one template)
│   ├── /leveringsregio/damme
│   ├── /leveringsregio/sluis
│   ├── /leveringsregio/brugge
│   └── /leveringsregio/blankenberge
├── /proefbox                       ProefBox request              I
├── /contact                        Contact + reason selector     I
└── legal: /privacy  /cookies  /voorwaarden
```

Site-wide: the tasting-box promo dialog (R35), a footer with delivery towns, email, socials and legal links. No cookie banner: the site sets no cookies and loads nothing from third parties (R41).

## Footer

```
GroMush · Ambachtelijk gekweekt          Zwammen          Voor wie            Ons verhaal        Leveringsregio
Van kwekerij tot bord.                    Alle zwammen     Chefs               Over Anthony       Knokke-Heist
info@gromush.be                           (6 varieties)    Grootkeukens        Kweekproces        Damme · Sluis
[Instagram] [Facebook]                                     Speciaalzaken       Buitenkweek        Brugge · Blankenberge
                                                           Thuis & MushLove    Adopteer
─────────────────────────────────────────────────────────────────────────────────────────────────────
© GroMush · Privacy · Cookies · Voorwaarden
```

## Consolidation decisions (what changed from the briefs)

| Brief(s) | Proposal | Why |
|---|---|---|
| "Voor particulieren" (no brief) + Community / MushLove | Merged into **`/voor-wie/thuis` "Thuis & MushLove"** | No particulieren brief exists, and the landing pages route the fourth audience to community already. One home-audience page beats two thin ones. |
| Voor wie brief (section or page) | **`/voor-wie`** is a short router page reusing the homepage's four cards | The nav parent needs a destination, and it doubles as a share link for the four audiences. |
| "Producten" / "Onze soorten" / "Onze zwammen" / "Onze paddenstoelen" | **Zwammen**, at `/zwammen/...` | This is the homepage brief's label. It is short, and "producten" sounds like a webshop, which the brief rejects. |
| `/voor-speciaalzaken` vs `/voor-wie/speciaalwinkels` | **`/voor-wie/speciaalzaken`** | One scheme for all audiences. "Speciaalzaken" covers bakers and butchers, not only shops. |
| "Over ons" / "Over GroMush" / "Ons verhaal", plus "Beleving", "Voedselbos", "Word mede-eigenaar" nav items | **Ons verhaal** dropdown holding about, process, outdoor and adoption | Five nav items became one. Process and adoption are part of the story, not separate destinations. |
| Adoption sold on 3 pages | One **`/ons-verhaal/adopteer`** page; community and Buitenkweek link to it | One source of truth for adoption prices and conditions (R24). |
| "Locaties" nav item, no hub brief | **Leveringsregio** hub under Ons verhaal plus the footer | The towns are SEO landing pages, not nav destinations, and "Locaties" wrongly implies GroMush has branches (R30). |
| "Gratis Chef Box" `/chef-box` / "Gratis proefbox" / push modal | **`/proefbox`**, one name (R5) | The same offer had three names. "ChefBox" is kept for the paid subscription. |
| "Afhalen en bestellen" footer link, no brief | Dropped. Home-cook orders go through `/contact` with reason "Bestelling thuis (afhalen)"; the pick-up place is communicated after the request (Q8). | No pick-up place or schedule was given. |
| "Reserveer nu" (Over ons) | Dropped. Nothing is bookable yet (Q9); "Kom langs?" links to contact with a reason. | No bookable offer is defined. |
| Separate "Speciaalwinkels" and "Contact" rounded-sans styling | One type system site-wide | The design directions settle the type system. |
| Testimonials / Cases (Chef, Grootkeuken) | Dropped (R3) | No real quotes exist. |
| Extra species (Black Pearl, koningsoesterzwam, pruikzwam, shiitake), 8 future outdoor species | A non-clickable "binnenkort" row of the 8 future outdoor species on Buitenkweek only (removable, R45); the other extra species nowhere | The briefs say "Je kan er niet op klikken". |

## Page count

| Group | Pages |
|---|---|
| Home | 1 |
| Zwammen | 1 + 6 |
| Voor wie | 1 + 4 |
| Ons verhaal | 1 + 3 |
| Inspiratie | 1 |
| Leveringsregio | 1 + 5 |
| Conversion | 2 |
| Legal | 3 |
| **Total** | **29** (26 content + 3 legal) |

There are 9 page templates (A–I). Every page uses one of them.
