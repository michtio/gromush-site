# Prompt: build the full GroMush site

Paste the text below into a new Claude Code session started in `/Users/michtio/dev/gromush-site`.

---

We're building the full GroMush website. The design direction is approved: Anthony (the client) signed off on the final homepage prototype on 2026-11-03. Your job is to get from that prototype to a complete, production-ready site, through the spec process. Respond in English; all site copy stays Dutch (nl-BE, "je/jouw").

## Read first, in this order

1. `specs/2026-10-19-gromush-site/prd.md`: requirements, open questions and the decisions log. The decisions log is the source of truth for every content decision made with Anthony (prices, organic claims, pick-up, ProefBox/ChefBox, grijze, outdoor growing from January 2027, phone/WhatsApp, logo, taglines, inbox, and more). Read every row.
2. `specs/2026-10-19-gromush-site/sitemap.md`: 26 pages plus legal, nav, footer, templates A–I. The low-fi wireframes are in `.impeccable/prototypes/directions/wireframes.html`.
3. `specs/2026-10-19-gromush-site/content-inventory.md`: all of Anthony's brief copy per page, with the contradictions already resolved in the decisions log.
4. `PRODUCT.md` and `DESIGN.md` at the repo root. DESIGN.md currently documents direction A only. It must be updated to the final merged system before the build: one type system (Young Serif, Work Sans, Kaushan Script for handwriting, Courier Prime only in cards), grid paper, tape, polaroids, flip cards, D's form, the van, the colour tokens. Run the Impeccable `document` command on `final.html` for that (see Tools).
5. **The approved design:** `.impeccable/prototypes/directions/final.html`. It is the visual and behavioural reference for every page. Its sections are documented in the decisions log (2026-10-19, "Final homepage prototype is a merge").
6. **Anthony's latest email and attachments:** `_resources/2026-11-mails-anthony/` (`_mail.txt`, the full Buitenkweek PDF, the hero reference screenshot). All of his earlier briefs are in `_resources/2026-10-mails-anthony/` (one folder per page, with images).

The repo root also contains an older static site (index.html, bestel/, chefbox/, etc.) from before the October briefs. Per the decisions log it is ignored. Do not build on it, and do not delete it without asking.

## Process (non-negotiable)

Spec-driven development, using the `spec-driven-development` skill:

1. **Finish the PRD.**
   - Fold in the 2026-11-03 decisions and the new Buitenkweek brief (see "Known conflicts" below; raise them, don't resolve them yourself).
   - List what's still open: Q7 (which Facebook page), Q10 (one canonical taste/texture line per variety; offer a drafted set from Anthony's own wording for him to approve), Q12 (sitemap approval), Q13 (platform), CRM and privacy-policy authorship, and the remaining site questions 1–6 from the inventory, which mostly close with Q12.
   - Ask me those questions in one batch. Only I set `approved`.
2. **Write plan.md** with a Fable planner (`craft-planner` if the stack is Craft):
   - vertical slices, each with its R ids and a runnable verification gate;
   - a slice per page template (A–I), plus foundations (tokens and components from final.html, header/footer/nav, forms and their mail delivery, legal, SEO and structured data, redirects for the old site's URLs, performance and accessibility gates).
   - I approve it before any build starts.
3. **Build slice by slice** with Opus builder agents (`craft-site-builder` for templates if Craft). Every brief cites the slice id, its R ids, their acceptance criteria and the gate. Reviews report per R id. At most 5 agents at once.
4. **Per page, after it's built:** Impeccable `audit` → fix everything (P0 to P3, not only P0/P1) → `harden` → `polish`. Then a finish review against final.html. Michael's bar is the audit round on the prototypes: WCAG 2.2 AA, 44×44 targets, real link paths, form failure path, no-JS readable, intentional reduced motion, reflow at 200% text, srcset everywhere, no overflow from 320 to 1440.

## Hero change Anthony asked for (homepage, at least on desktop)

Anthony wants the first block's mycelium to "move differently" and take the structure of his reference (`_resources/2026-11-mails-anthony/Schermafbeelding 2026-10-26 om 11.03.22.png`):
- centred title "Van kwekerij tot bord" with the intro and one button;
- the six varieties in round medallions with their names set on a curve above each one, in a ring around the title (three per side);
- dense, finely branching hyphae radiating between and behind them.

Recommendation to put to me before building: take the structure and the motion (hyphae growing outward from the centre and branching towards each medallion as the page loads and scrolls, medallions resolving as their branch arrives), but keep the approved materials: ink on straw, not the reference's dark green with glowing gold lines. Anthony's own Buitenkweek brief says "geen overdreven magische lichteffecten". Keep these from final.html: the Zaak/Particulier actions, the "Vraag aan" per variety, the seeded generator approach with static no-JS paths, and the collision probes (zero line-over-label hits).
- **Mobile:** keep the current trunk-and-twig list unless the radial layout genuinely works at 390.
- **Prototype:** build this as a variant in `final.html` first and show me before it moves into the build.

## Known conflicts in the new Buitenkweek brief (raise with me, don't decide)

- **"Biologisch":** the headline "Puur natuur, biologisch en regeneratief", the step "Selectie van biologische boomstammen", "Biologisch voedselbos" and the footer line all claim organic. Decisions log Q6: GroMush is not certified yet, so no organic claims until the certificate exists. Propose wording without "biologisch".
- **Status:** the brief describes the food forest and log ownership as existing ("meerdere oogsten", "productief gedurende meerdere jaren"). Decisions log Q5: outdoor growing starts January 2027, and is presented as coming, never as active.
- **Species:** the logs carry shiitake and pruikzwam, and the "EXTRA BLOK" asks for a column of future species (the 8 from `Extra Blok !!! Buitenkweek`, `Buitenkweek-paddenstoelen.zip`). The decisions log says the extra species are sold later and the 8 future species are not on the launch site. Anthony now explicitly asks for the extra block, so ask me whether it goes in as a non-clickable "binnenkort" column.
- **Adoption:** "Ontdek de formules" implies published formulas or prices. The decisions log says no prices, adoption is a request (paid by bank transfer), and nothing is bookable yet. The CTA must lead to a request or interest form, not formulas.
- **Visual language:** the brief prescribes its own look: dark green #10190B, moss #75882D, ivory, Cormorant/Inter, mosgroen buttons, a dark hero with an overlay. The approved design system wins. Translate its structure (hero, "Wat is een voedselbos?", six process steps, ownership section, six-benefit bar, closing CTA) into the final.html world, and say where you do.
- **Photography:** it asks for photorealistic forest and log images that don't exist yet. Use what's in `_resources/2026-10-mails-anthony/Buitenkweek-pagina-webiste-gromush/` (`hero-buitenkweek.jpeg`, `voedselbos.jpeg` and the numbered jpgs) and flag the gaps.

## Other open items to carry

- **Proefbox photo:** it has "ChefBox" burned into the box, so the free ProefBox needs another image.
- **Grijze:** it reuses the Italiaanse cut-out until Anthony sends a real photo.
- **AI imagery:** many supplied images are AI-generated (a van, branded crates, a food forest with a school visit). They're fine for now, per Anthony, but list the ones that show things that don't exist, for replacement before launch.
- **La Réserve:** the hotel photo (Knokke) must not be used without written permission.

## Tools and environment

- **Impeccable skill:** `/Users/michtio/dev/hybridinteractive/ledgerly/.cursor/skills/impeccable/`. Read SKILL.md, run `scripts/impeccable context` once, and use the `reference/{audit,harden,polish,document}.md` playbooks and `craft-floor.md` before any UI edit.
- **DDEV for everything** (`ddev composer`, `ddev craft`, `ddev npm`); nothing on the host. No plugin installs without my approval.
- **Browser checks:** the `chrome-devtools-isolated` MCP for interactive checks. For batch screenshots and probes, use the headless tools in `.impeccable/tools/` (git-ignored; read its README.md first):
  - `fullshot.py`: screenshots, with `PRE_JS`, `SHOT_SEL` and `FONT_SIZE`;
  - `check.py`: JS errors and expressions;
  - `sweep.js`: 44px targets;
  - `probes.sh`: the hero network collision probes, which must stay at zero;
  - `scrollprobe.py`: scroll-driven sections;
  - `nojs.py`: scripts disabled;
  - `levering/build_levering.py`: the delivery-section generator, which writes into final.html by absolute path.

  Run `pkill -f remote-debugging-port` if headless Chromes pile up.
- **Prototypes:** `.impeccable/prototypes/directions/` (final.html, final-levering.html with the three delivery variants, and A–D), served locally with `python3 -I -m http.server 8765 --directory .impeccable/prototypes/directions`.
- **Git:** no commits unless I ask. No AI attribution in commits or PRs.

Start with step 1: read everything listed above, then come back to me with the PRD update and one batch of questions. Don't write code yet.
