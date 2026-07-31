#!/usr/bin/env python3
"""Batch 260731: nieuwe beelden van Anthony (assortiment-hero, binnen/buiten-
kweek, word-eigenaar, beleven, nieuwe soorten) verwerken naar assets/img.

Zelfde conventies als process-images.py: webp + avif, full-size (max 1600px)
en een 800w-variant. Bronnen mogen webp of png zijn.

Gebruik: python3 _resources/process-images-260731.py
"""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "_resources" / "260731-resources"
OUT = ROOT / "assets" / "img"

WEBP_Q = "82"
AVIF_Q = "58"
FULL_MAX = 1600
VARIANT = 800

MAPPING = {
    # Hero
    "Paddenstoelen-Zwammen-kwekerij-GroMush-Knokke-Heist-vers-ambachtelijk-gekweekt-geteelt-binnenkweek-buitenkweek-geleverd-aan-restaurants-chef-koks-particulieren-grootkeukens-lokaal-in-knokke-heist-damme-brugge.png": "paddenstoelen-assortiment",
    # Twee werelden
    "Binnenkwekerij-zeecontainer-gromush-knokke-heist-oesterzwammen-vers-ambachtelijk-gekweekt-lokaal-geleverd-in-knokke-heist-damme-brugge.webp": "binnenkweek-zeecontainer",
    "Buitenkwekerij-gromush-paddenstoelen-biologisch-gekweekt-voedselbos-knokke-heist-vers-lokaal-ambachtelijk-geleverd-in-knokke-heist-damme-brugge.webp": "buitenkweek-voedselbos",
    # Word eigenaar + beleven
    "word-eigenaar-emmer-oesterzwammen-gromush-kwekerij-knokke-heist-lokaal-gekweekt-ambachtelijk-vers-workshop-aankoop-emmer.webp": "word-eigenaar-emmer",
    "word-eigenaar-van-boomstammetjes-verse-paddenstoelen-zwammen-in-voedselbos-kwekerij-gromush-knokke-heist-vers-gekweekt-lokaal-ambachtelijk.webp": "word-eigenaar-boomstammen",
    "rondleiding-kwekerij-beleving-paddenstoelen-ambachtelijk-vers-en-lokaal-in-knokke-heist-groepen-scholen-koppels.webp": "rondleiding-beleving",
    # Nieuwe soorten (parade + latere soortenpagina)
    "Shiitake-paddenstoel-buitenkweek-gromush-kwekerij-knokke-heist-ambachtelijk-lokaal-geteelt-vers-geleverd-restaurants-knokke-brugge-damme-lokaal.webp": "shiitake-paddenstoel",
    "Nameko-paddenstoel-kwekerij-gromush-knokke-heist-vers-geteelt-ambachtelijke-paddenstoelen-zwammen-levering-knokke-damme-brugge.webp": "nameko-paddenstoel",
    "Reishi-paddenstoel-buitenkwekerij-gromush-knokke-heist-ambachtelijk-biokweek-vers-geleverd-restaurants-chef-kok-knokke-heist-damme-brugge-lokaal.webp": "reishi-paddenstoel",
    "Morieltje-paddenstoelen-buitenkweek-gromush-kwekerij-knokke-heist-vers-lokaal-ambachtelijk-geteelt-geleverd-restaurants-chef-koks-knokke-damme-brugge.webp": "morieltje-paddenstoel",
    "Pioppino-paddenstoelen-kwerkerij-Gromush-knokke-heist-ambachtelijk-gekweekt-vers-geteelt-lokaal-levering-restaurant-chef-kok-knokke-damme-brugge.webp": "pioppino-paddenstoel",
    "Oesterzwam-de-Black-Pearl-gromush-kwekerij-knokke-heist-damme-brugge-ambachtelijk-gekweekt-paddenstoelen-vers-teelt-restaurants-chef-kok.webp": "black-pearl-oesterzwam",
    "judasoor-paddenstoelen-buitenkwekerij-Gromush-lokaal-geteelt-geoogst-knokke-heist-damme-brugge-verse-buiten-paddenstoelen-eetbaar-restaurants-chef-kok-lokaal-geleverd.webp": "judasoor-paddenstoel",
    "wijnrode-stropharia-tuinreus-buitenkwekerij-Gromush-lokaal-geteelt-geoogst-knokke-heist-damme-brugge-verse-buiten-paddenstoelen-eetbaar-restaurants-chef-kok-lokaal-geleverd.webp": "wijnrode-stropharia",
    "paarse-ridderzwam-buitenkweek-gromush-kwekerij-knokke-heist-damme-brugge-paddenstoelen-ambachtelijk-lokaal-vers-levering-restaurants(1).webp": "paarse-ridderzwam",
}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"FOUT: {' '.join(str(c) for c in cmd)}\n{r.stderr}")


def png_size(path):
    out = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
        capture_output=True, text=True,
    ).stdout
    w = h = 0
    for line in out.splitlines():
        if "pixelWidth" in line:
            w = int(line.split()[-1])
        if "pixelHeight" in line:
            h = int(line.split()[-1])
    return w, h


def encode(png, dest_stem, width, manifest):
    with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
        w, h = png_size(png)
        if width and w > width:
            run(["sips", "--resampleWidth", str(width), str(png), "--out", tmp.name])
            src = tmp.name
            w2, h2 = png_size(tmp.name)
        else:
            src = str(png)
            w2, h2 = w, h
        run(["cwebp", "-quiet", "-q", WEBP_Q, src, "-o", f"{dest_stem}.webp"])
        run(["avifenc", "-q", AVIF_Q, "-s", "6", "--jobs", "4", src, f"{dest_stem}.avif"])
        manifest.append((Path(dest_stem).name, w2, h2))


def main():
    manifest = []
    for rel, slug in MAPPING.items():
        src = RES / rel
        if not src.exists():
            sys.exit(f"Ontbreekt: {src}")
        with tempfile.NamedTemporaryFile(suffix=".png") as png:
            if src.suffix == ".webp":
                run(["dwebp", "-quiet", str(src), "-o", png.name])
                source_png = png.name
            else:
                source_png = str(src)
            encode(source_png, OUT / slug, FULL_MAX, manifest)
            w, _ = png_size(source_png)
            if w > VARIANT:
                encode(source_png, OUT / f"{slug}-{VARIANT}", VARIANT, manifest)

    for name, w, h in manifest:
        print(f"{name}\t{w}x{h}")


if __name__ == "__main__":
    main()
