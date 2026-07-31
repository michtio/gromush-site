# GSAP (vendored)

Zelf gehost voor GDPR (geen CDN-requests). Enkel geladen op de homepage-varianten
(`/` en `/index-b/`), nergens anders.

- **Versie:** 3.15.0
- **Bestanden:** `gsap.min.js`, `ScrollTrigger.min.js`
  (ongewijzigde dist-builds uit het officiële npm-pakket).
  MotionPathPlugin is bewust niet opgenomen: het bestelwagentje volgt zijn
  route via CSS `offset-path`; GSAP scrubt enkel `offset-distance`.
- **Bron:** https://registry.npmjs.org/gsap/-/gsap-3.15.0.tgz (`package/dist/`)
- **Licentie:** GSAP Standard License — gratis voor commercieel gebruik sinds GSAP 3.13
  (Webflow), alle plugins inbegrepen. Zie `LICENSE.txt` en
  https://gsap.com/standard-license

## Updaten

```sh
curl -sLO https://registry.npmjs.org/gsap/-/gsap-<versie>.tgz
tar xzf gsap-<versie>.tgz
cp package/dist/{gsap,ScrollTrigger}.min.js assets/vendor/gsap/
```

Werk daarna het versienummer in dit bestand bij.
