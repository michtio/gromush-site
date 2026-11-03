Fixtures for tools/lint_content.py and tools/check_links.py, laid out like docs/ (base /gromush-site/).

Seeded lint hits (9), one per marked line `<!-- seed: ... -->`:
1. index.html: R1 "Gromush" in the meta description
2. zwammen/gele-oesterzwam/: R2 "biologische" in an alt text
3. voor-wie/chefs/: R2a "superfood" on a professional page
4. voor-wie/thuis/: R2a medical claim "geneest ontstekingen" (health words on this consumer page are fine)
5. voor-wie/grootkeukens/: R3 "Vanaf € 12"
6. proefbox/: R5 "gratis ChefBox"
7. voor-wie/speciaalzaken/: R21 "gratis proeflevering" in main (the header CTA is outside main)
8. ons-verhaal/buitenkweek/: R23 "ons voedselbos"
9. ons-verhaal/buitenkweek/: R23 month "september"

Seeded link problems (3), all in links/index.html: a broken page link, an href without the base, a relative srcset candidate.
Everything else in these files is a negative control and must not be reported.
