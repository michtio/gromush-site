# Building the GroMush site

The new site is generated from one data source by a small Python script (stdlib only, no packages) and written to `docs/`, which GitHub Pages serves as plain HTML, CSS and JS. The old static site in the repo root is not part of this build and stays untouched.

Spec: `specs/2026-10-19-gromush-site/` (`prd.md`, `plan.md`).

## Build

```sh
python3 -I build.py                        # base from site.json (/gromush-site/)
python3 -I build.py --base /gromush-site/  # GitHub Pages: https://michtio.github.io/gromush-site/
python3 -I build.py --base /               # domain root (later, gromush.be)
```

It prints `N pages written to docs (base ...)` and exits 0, or prints `build failed: ...` and exits 1. Always build with `/gromush-site/` before committing `docs/`.

The build refuses to write into a `docs/` folder that has content but no `.nojekyll` (that would not be a build output). It never deletes files; a file in `docs/` that the build no longer produces is reported as a `warning: stale file` so you can remove it by hand.

## Images and fonts

```sh
python3 -I tools/images.py          # render new or changed images from images.json into src/static/img/r/
python3 -I tools/images.py --force  # re-render everything
python3 -I tools/images.py --prune  # also delete files in img/r/ that the register no longer produces
```

Needs `sips` (macOS), `cwebp` and `avifenc` (Homebrew `webp`, `libavif`); a missing tool is reported and the run exits 1. Add an image: put the source in the repo, add it to `images.json` (id, source, width, height, Dutch alt), run `tools/images.py`, rebuild. The rendered files are committed.

avif and webp are rendered at every width; the jpeg/png fallback only at the smallest width and the largest up to 800 px (`picture.fallback_widths`), which is all a browser without avif/webp support gets.

Fonts are self-hosted in `src/static/fonts/` (OFL, licence files beside them): latin-subset woff2 downloaded once from google-webfonts-helper (`https://gwfh.mranftl.com/api/fonts/<id>?subsets=latin`, plan AD11): Young Serif 400, Work Sans 400/500/600 and italic 400, Kaushan Script 400, Courier Prime 400/700. Nothing is fetched at run time.

## Header, footer and promo

`src/data/nav.json` holds the primary navigation (`main`: five items, dropdown children; `{"from": "varieties"}` and `{"from": "towns"}` fill a list from data), the CTA and the footer columns. The build refuses more than six items, a CTA other than "Gratis ProefBox" to `/proefbox/`, and any "ChefBox" label (R5, R6). `partials/header.html` and `partials/footer.html` render it on every page; `src/static/js/site.js` adds the mobile menu, the dropdown buttons, the header scroll state and the promo. The promo copy, delay (8 s), scroll share (40 %) and the pages it never shows on (`never_on`) are in `site.json` under `promo`; its only state is the sessionStorage key `gromush-promo`.

Components: `src/templates/partials/` holds the shared components of `final.html`; `/_dev/componenten/` shows them all (noindex, never in nav or sitemap).

## Audience pages (template D)

`layouts/audience.html` serves the four `/voor-wie/<slug>/` pages (S12; PRD R18). It finds its audience in `src/data/audiences.json` by the page path and renders problem, offer and the audience's own primary action(s), in the hero and again in the closing band, from that entry's `primary_actions` and `page` (`hero`, `problem`, `offer`, `closing`). A new audience page adds its `page` data and a page file with title, description and its own sections in `{% block sections %}` (also `intro`, `problem`, `offer`); the layout itself does not change. `card` in the same entry feeds the four cards of `/voor-wie/` and the homepage (`partials/audience_grid.html`). Check AC18: `python3 -I tools/check_sections.py docs/voor-wie/chefs/index.html --template audience --primary-action /proefbox/` prints `1 ok`.

## Titles, metadata and SEO

Every page declares its own title and meta description as blocks, in Dutch, with the brand in the title:

```
{% extends "layouts/base.html" %}
{% block title %}Alle zwammen · GroMush{% endblock %}
{% block description %}Zes oesterzwammen, elk met hun eigen kleur, textuur en karakter.{% endblock %}
```

The build fails when a page has no title or description, when a title does not contain "GroMush" (R1), or when two pages share a title or a description (R40). Everything else is generated (`src/gen/seo.py`):

- **Canonical:** `abs_url()` of the page path, trailing slash (`{% block canonical %}` overrides; the 404 page has none).
- **Open Graph:** added to every indexable page from its title, description and canonical; `og:image` defaults to `site.json` `seo.og_image`. A page sets its own image with `{% block head %}{{{ og_image('var-gele') }}}{% endblock %}`.
- **Structured data (AD18):** `Organization` on every page and `LocalBusiness` (locality only, never a street address) on `/`, both from `site.json`. Product pages add `{{{ jsonld_product(v) }}}` and the inspiration page `{{{ jsonld_recipe(r) }}}` per recipe, in `{% block head %}`. Never `offers` or a price; the build refuses them.
- **Noindex:** `{% block robots %}<meta name="robots" content="noindex">{% endblock %}`. Noindex pages, `404.html` and `/_dev/` get no Open Graph and stay out of the sitemap.
- **`sitemap.xml` and `robots.txt`** are written at the base with every indexable page. Under `/gromush-site/` the `robots.txt` is not at the host root, so crawlers ignore it until the site runs at the domain root (`--base /`); it is generated now so it is right at launch.
- **Removed varieties (AD17, R17):** a variety with `in_range: false` gets a forward page at `/zwammen/<slug>/` (`layouts/forward.html`): noindex, a meta refresh and a canonical to `/zwammen/`, not in the sitemap. The build fails if a page template still renders that path.

Check a build: `python3 -I tools/check_seo.py docs --base /gromush-site/` prints `0 problems` (also a step of `tools/qa.sh`).

## Preview

```sh
tools/serve.sh            # http://127.0.0.1:8765/gromush-site/
tools/serve.sh 8766       # another port
tools/serve.sh 8766 /     # for a --base / build
```

## Tests and checks

```sh
python3 -I -m unittest discover -s src/gen/tests
python3 -I -m unittest discover -s tools/tests
tools/qa.sh / /_dev/componenten/                       # the standard gate
python3 -I tools/check_links.py docs --base /gromush-site/ --pending tools/pending_pages.txt --same-chrome
python3 -I tools/check_depth.py docs --base /gromush-site/   # R7: every sitemap page within 2 clicks
python3 -I tools/check_seo.py docs --base /gromush-site/     # R40: titles, descriptions, OG, canonical, sitemap, JSON-LD
python3 -I tools/check_sections.py docs/zwammen/*/index.html --order hero,intro,smaak,tijdlijn,kweker,keuken,voor-wie,product,bewaren,andere,slot   # AC16: '6 ok'
python3 -I tools/check.py <url> 390 "$(cat tools/nav-a11y.js)"   # header keyboard/disclosure check: ok
python3 -I tools/promo.py http://127.0.0.1:<port>/gromush-site [--close escape]   # none shown dismissed-none
```

`tools/pending_pages.txt` lists the sitemap pages that the header and footer link to but that are not built yet; links to them count as "pending", not "broken". A slice that builds a page removes its line.

## Where things live

| Path | What |
|---|---|
| `src/data/site.json` | Name, origin, base path, email, phone, WhatsApp, locality, socials, legal links, shared interface strings (`t()`). |
| `src/data/flags.json` | `certified_organic`, `startup_phase`, `show_future_species`, `phone_published` (true/false). |
| `src/data/varieties.json` | The six oyster varieties: name, Latin name, three taste words, taste sentence (PRD Q10), accent, images, pips, `in_range`, `nav_order`, and `page`: the product-page copy (S11; a missing optional field hides its block). |
| `src/data/towns.json` | Delivery towns: sub-areas, map coordinates, hero image. |
| `src/data/audiences.json` | The four audiences and their primary actions (R18). |
| `src/data/recipes.json` | Recipes for Inspiratie; the page shows however many there are. |
| `src/data/future_species.json` | The 8 "binnenkort" species of Buitenkweek (R45). |
| `src/data/forms.json` | Form fields, contact reasons and modes. |
| `src/data/nav.json` | Primary navigation, CTA and footer columns (S4). |
| `src/data/images.json` | Image register: source, size, Dutch alt, flagged/approved (R37, R44). |
| `src/templates/layouts/` | Page shells (`base.html`). |
| `src/templates/partials/` | Shared pieces (header, footer, later components). |
| `src/templates/pages/` | One file per page: `pages/x/index.html` or `pages/x.html` becomes `/x/`; `pages/404.html` becomes `docs/404.html`. |
| `src/templates/products/zwam.html` | The one product template (S11, R14): the build renders it at `/zwammen/<slug>/` for every variety in the range. Sections carry `data-section`, the page `data-template="product"` (see `tools/check_sections.py`). |
| `src/static/` | Copied as-is into `docs/` (CSS, images, later fonts and JS). |
| `src/gen/` | The generator (`build.py`) and template engine (`template.py`). |

## Common edits

- **Change a variety's taste words:** edit `taste_words` in `src/data/varieties.json`, rebuild. Every page that shows them updates.
- **Take a variety out of the range:** set its `in_range` to `false`, rebuild. Its URL becomes a forward page to `/zwammen/`.
- **Hide the phone number and WhatsApp:** set `phone_published` to `false` in `flags.json`, rebuild.

## Template syntax

`{{ expr }}` prints escaped, `{{{ expr }}}` prints raw HTML. `{% if %}…{% elif %}…{% else %}…{% endif %}`, `{% for x in xs %}…{% else %}…{% endfor %}` (with `loop.index`, `loop.first`, `loop.last`), `{% set x = expr %}`, `{% include "partials/x.html" with {"key": value} %}`, `{% extends "layouts/base.html" %}` with `{% block name %}…{% endblock %}`, `{# comment #}`. Expressions are Python; data keys read as attributes (`site.email`). An included partial sees the globals plus its `with` values only.

Globals in every template: `site`, `flags`, `data` (all data files), `varieties` (in range, in nav order), `base`, and the helpers:

- `url('/zwammen/')`: every internal href, src and srcset goes through it, so links work under `/gromush-site/` and at a domain root.
- `abs_url('/zwammen/')`: full URL for canonical, Open Graph and sitemap.
- `t('skip_link')`: a shared interface string from `site.json`.
- `picture('dish-curry', cls='', sizes='50vw', loading=None, decorative=False)`: `<picture>` with avif and webp sources and a jpeg (or png, for images with transparency) fallback, srcset at 400/800/1200/1600 (never upscaled), width, height, `loading` (lazy unless `"eager": true` in `images.json`) and the Dutch alt from `images.json`. The build fails on an unknown id, a missing alt (`decorative=True` forces `alt=""`), or files not rendered yet.
- `opt('kind', 'primary')`: in a partial, a value passed with `include ... with`, or the default.

Rules the build enforces: the brand is always written "GroMush" (data and output), page URLs are lowercase with a trailing slash, every variety has exactly three taste words, flags are true or false.
