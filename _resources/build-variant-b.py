#!/usr/bin/env python3
"""Genereer /index-b/ (kopijdeck B, uitgesproken speels) vanuit index.html.

Structuurwijzigingen gebeuren altijd eerst in index.html (deck A); daarna
dit script draaien vanaf de repo-root:  python3 _resources/build-variant-b.py

Elke (A, B)-tekstpaar hieronder moet exact één keer voorkomen — het script
faalt luid als een slot niet meer matcht, zodat de decks nooit stil
uiteenlopen.
"""
import os
import re

src = open("index.html").read()

# --- 1. relatieve paden ./ -> ../ ------------------------------------------
out = src.replace('href="./', 'href="../').replace('src="./', 'src="../').replace('srcset="./', 'srcset="../')
out = re.sub(r'(srcset="[^"]*)', lambda m: m.group(1).replace(', ./', ', ../'), out)

# --- 2. head: titel, noindex, canonical -> A, geen JSON-LD ------------------
out = out.replace(
    "<title>GroMush | Verse oesterzwammen uit Knokke-Heist voor chefs &amp; particulieren</title>",
    "<title>GroMush | Verse oesterzwammen uit Knokke-Heist (versie B)</title>\n  <meta name=\"robots\" content=\"noindex\">")
jsonld = re.search(r'  <script type="application/ld\+json">.*?</script>\n', out, re.S)
out = out.replace(jsonld.group(0), "")

# --- 3. nav: Klant wijst naar A, geen aria-current --------------------------
out = out.replace('<li><a href="../" aria-current="page">Klant</a></li>',
                  '<li><a href="../">Klant</a></li>')

# --- 4. kopijdeck B ----------------------------------------------------------
PAIRS = [
    # hero
    ("""            <span class="line-1">Paddenstoelen zoals je ze nog nooit hebt beleefd.</span>
            <span class="line-2">Van spore tot jouw bord.</span>""",
     """            <span class="line-1">Paddenstoelen waar zelfs chefs stil van worden.</span>
            <span class="line-2">En ze groeien hier om de hoek.</span>"""),
    ("""<p class="lead">Puur en ambachtelijk gekweekt &mdash; binnen in onze zeecontainer &eacute;n buiten in het voedselbos. Boordevol smaak, geplukt op de dag dat jij ze proeft.</p>""",
     """<p class="lead">Binnen in een zeecontainer, buiten in een voedselbos. Klinkt gek, smaakt geniaal &mdash; en het bewijs wordt geplukt op de dag dat jij het proeft.</p>"""),
    ("""<!-- copy: hero.cta-1 --><a class="btn btn--photo" href="../oesterzwammen/">Ontdek onze soorten</a>""",
     """<!-- copy: hero.cta-1 --><a class="btn btn--photo" href="../oesterzwammen/">Toon me de soorten</a>"""),
    ("""<!-- copy: hero.cta-2 --><a class="btn btn--outline" href="../chefbox/#proefbox">Vraag een proefbox aan</a>""",
     """<!-- copy: hero.cta-2 --><a class="btn btn--outline" href="../chefbox/#proefbox">Proefbox scoren (gratis)</a>"""),
    ("""<!-- copy: hero.cue --><span>Scroll &mdash; het verhaal groeit vanzelf</span>""",
     """<!-- copy: hero.cue --><span>Scroll. De zwammen groeien niet vanzelf&hellip; ok&eacute;, eigenlijk wel.</span>"""),
    # ticker (items komen 2x voor in de gedupliceerde track)
    ("<span>Vijftien-plus soorten</span>", "<span>Vijftien-plus soorten, nul photoshop</span>"),
    ("<span>Ambachtelijk gekweekt</span>", "<span>Gekweekt met obsessie</span>"),
    ("<span>100% lokaal</span>", "<span>100% lokaal (echt)</span>"),
    # underground
    ("""<h2 id="underground-h">Het echte werk zie je niet</h2>""",
     """<h2 id="underground-h">Het beste deel zie je niet. Typisch.</h2>"""),
    ("""              <p class="scene__step">Onder elk zwammetje zit een netwerk van kilometers fijne draden: <strong>mycelium</strong>. Het verbindt, groeit, breekt af en bouwt opnieuw op &mdash; de stille motor van elk gezond ecosysteem.</p>""",
     """              <p class="scene__step">Onder elk zwammetje zit een netwerk van kilometers fijne draden: <strong>mycelium</strong>. Het verbindt alles met alles, breekt af en bouwt weer op. Zeg maar het internet, maar dan nuttig.</p>"""),
    ("""              <p class="scene__step">In onze kwekerij in Knokke&#8209;Heist geven we dat netwerk precies wat het nodig heeft: vers substraat, de juiste vochtigheid en veel geduld. De rest doet de natuur.</p>""",
     """              <p class="scene__step">Wij geven dat netwerk vers substraat, de juiste vochtigheid en af en toe een opbeurend woord. Daarna vooral: niet in de weg lopen.</p>"""),
    ("""              <p class="scene__step scene__aside">Ja, we praten &eacute;cht iets te graag over mycelium. Vraag er gerust eens naar &mdash; dan ben je wel een uurtje zoet.</p>""",
     """              <p class="scene__step scene__aside">Waarschuwing: vraag Anthony nooit &lsquo;wat is mycelium eigenlijk?&rsquo; Tenzij je een vrije namiddag hebt.</p>"""),
    ("""<p class="scene__hook">Tijd om naar boven te komen.</p>""",
     """<p class="scene__hook">Genoeg gegraven. Naar boven.</p>"""),
    # farm
    ("""<h2 id="farm-h">Het begon met een fascinatie</h2>""",
     """<h2 id="farm-h">Begonnen uit pure obsessie</h2>"""),
    ("""              <p class="scene__step">Sommige ondernemers starten een bedrijf omdat ze een gat in de markt zien. Bij mij begon het anders &mdash; met een jarenlange fascinatie voor de verborgen wereld van schimmels en mycelium.</p>""",
     """              <p class="scene__step">Sommige ondernemers zien een gat in de markt. Ik zag een schimmel en was verkocht. Ieder zijn ding.</p>"""),
    ("""              <p class="scene__step">Uit die passie is GroMush ontstaan: een kleinschalige kwekerij in Knokke&#8209;Heist waar ik elke kweekcyclus met de hand opvolg, van substraat tot oogst.</p>""",
     """              <p class="scene__step">Dus staat er nu een kwekerij in Knokke&#8209;Heist waar ik elke kweekcyclus persoonlijk opvolg, van substraat tot oogst. De zwammen en ik &mdash; wij hebben iets.</p>"""),
    ("""              <p class="scene__step">Vakmanschap boven massaproductie. Kwaliteit boven kwantiteit. Samenwerking boven verkoop. Zo simpel is het eigenlijk.</p>""",
     """              <p class="scene__step">Vakmanschap boven massaproductie. Kwaliteit boven kwantiteit. Zwammen boven zowat alles, eerlijk gezegd.</p>"""),
    ("""            <p class="scene__signoff">&mdash; Anthony Watteeuw, kweker</p>""",
     """            <p class="scene__signoff">&mdash; Anthony Watteeuw, kweker (en voltijds mycelium-fan)</p>"""),
    ("""<!-- copy: farm.sticker --><span class="sticker" aria-hidden="true">Ambachtelijke teelt</span>""",
     """<!-- copy: farm.sticker --><span class="sticker" aria-hidden="true">Handwerk, hoor</span>"""),
    # process
    ("""<h2 id="process-h">Van stro tot bord</h2>""",
     """<h2 id="process-h">Van stro tot bord &mdash; met een vleugje magie</h2>"""),
    # werelden
    ("""          <span class="line-1">Binnen &eacute;n buiten.</span>
          <span class="line-2">&Eacute;&eacute;n passie.</span>""",
     """          <span class="line-1">Twee werelden.</span>
          <span class="line-2">Nul compromissen.</span>"""),
    ("""<p class="lead" style="max-width: 42rem; margin-inline: auto">Onze zwammen groeien op twee plekken die niet harder konden verschillen &mdash; en dat proef je.</p>""",
     """<p class="lead" style="max-width: 42rem; margin-inline: auto">Een zeecontainer met discolicht en een voedselbos vol vogels. Onze zwammen kiezen zelf hun vibe.</p>"""),
    ("""            <p>Gecontroleerde vochtigheid, mist en licht: hier oogsten we het hele jaar door oesterzwammen van constante topkwaliteit.</p>""",
     """            <p>Mist, paars licht en een strak klimaat: het ziet eruit als sciencefiction, maar er groeit gewoon topkwaliteit. Het hele jaar door.</p>"""),
    ("""            <p>Op boomstammen, op het ritme van de seizoenen: shiitake en bosgenoten groeien hier 100% natuurlijk.</p>""",
     """            <p>Boomstammen, seizoenen en verder niets: hier doet de natuur het werk. Wij komen vooral oogsten.</p>"""),
    # varieties
    ("""            <span class="line-1">Twaalf karakters.</span>
            <span class="line-2">&Eacute;&eacute;n kwekerij.</span>""",
     """            <span class="line-1">Twaalf karakters.</span>
            <span class="line-2">Nul photoshop.</span>"""),
    ("""<p class="lead" style="max-width: 42rem; margin-inline: auto">Van de klassieke grijze oesterzwam tot shiitake, morieltje en de diepzwarte Black Pearl: elk met een eigen karakter, kleur en smaak. Kies je favoriet &mdash; of laat de chef in jou beslissen.</p>""",
     """<p class="lead" style="max-width: 42rem; margin-inline: auto">Van de brave grijze tot de Black Pearl die n&eacute;t iets te mysterieus doet: allemaal karakter, allemaal familie. Kies je favoriet. Of neem ze allemaal &mdash; wij oordelen niet.</p>"""),
    ("""<span class="parade__note">Mild en zacht, veelzijdig in de keuken.</span>""",
     """<span class="parade__note">Mild, zacht en overal goed in. De schoonzoon onder de zwammen.</span>"""),
    ("""<span class="parade__note">Stevig en mals, de klassieker.</span>""",
     """<span class="parade__note">De klassieker. Doet nooit moeilijk.</span>"""),
    ("""<span class="parade__note">Fijn en fris, licht nootachtig.</span>""",
     """<span class="parade__note">Licht nootachtig en altijd vrolijk.</span>"""),
    ("""<span class="parade__note">Vol van smaak en mooi stevig.</span>""",
     """<span class="parade__note">Vol van smaak. Lichtjes dramatisch van kleur.</span>"""),
    ("""<span class="parade__note">Fruitig en licht ziltig, kort bakken.</span>""",
     """<span class="parade__note">Fruitig, ziltig en dol op aandacht. Kort bakken.</span>"""),
    ("""<span class="parade__note">Licht en sappig, op z&rsquo;n best in de zomer.</span>""",
     """<span class="parade__note">Piekt in de zomer. Zoals wij allemaal.</span>"""),
    ("""<span class="parade__note">Diepdonkere kop, stevige beet, volle smaak.</span>""",
     """<span class="parade__note">Draagt altijd zwart. Smaakt navenant cool.</span>"""),
    ("""<span class="parade__note">Intens, aards en boordevol umami.</span>""",
     """<span class="parade__note">Umami-bom. Vraag maar aan Japan.</span>"""),
    ("""<span class="parade__note">Goudglanzend, zijdezacht en licht zoet.</span>""",
     """<span class="parade__note">Glimt alsof hij gepoetst is. Is gewoon zo.</span>"""),
    ("""<span class="parade__note">Knapperige steeltjes, diep bosaroma.</span>""",
     """<span class="parade__note">Knapperig steeltje, bosaroma van formaat.</span>"""),
    ("""<span class="parade__note">De delicatesse waar chefs voor omrijden.</span>""",
     """<span class="parade__note">Chefs rijden ervoor om. Letterlijk.</span>"""),
    ("""<span class="parade__note">De legendarische vitaliteitszwam.</span>""",
     """<span class="parade__note">Drinkt men als thee. Legende doet de rest.</span>"""),
    ("""          <a class="btn btn--cream" href="../oesterzwammen/">Bekijk alle soorten</a>""",
     """          <a class="btn btn--cream" href="../oesterzwammen/">Ontdek alle soorten (2 zijn camerashy)</a>"""),
    # route
    ("""<h2 id="route-h">Geen voedselkilometers, <span class="accent">wel smaak</span></h2>""",
     """<h2 id="route-h">Voedselkilometers? Wij doen <span class="accent">voedselmeters</span></h2>"""),
    ("""            <p>Veel bijzondere paddenstoelen leggen duizenden kilometers af voor ze op een bord belanden. De onze hooguit dertig minuten: &rsquo;s ochtends geoogst, dagvers geleverd in Knokke&#8209;Heist, Damme en Brugge. Zonder omweg, zonder koelcel-marathon.</p>""",
     """            <p>Sommige paddenstoelen vliegen business class de halve wereld rond. De onze zitten hooguit een half uurtje in een bestelwagentje richting Knokke&#8209;Heist, Damme of Brugge. Jetlagvrij, dus.</p>"""),
    ("""<!-- copy: route.sticker --><span class="sticker sticker--sand scene__sticker" aria-hidden="true">Dagvers geleverd</span>""",
     """<!-- copy: route.sticker --><span class="sticker sticker--sand scene__sticker" aria-hidden="true">Geen jetlag</span>"""),
    ("""<p class="scene__hook">En dan: het bord.</p>""",
     """<p class="scene__hook">Volgende halte: jouw bord.</p>"""),
    # plate
    ("""<h2 id="plate-h">Waar chefs ze laten schitteren</h2>""",
     """<h2 id="plate-h">Chefs staan er (beleefd) voor in de rij</h2>"""),
    ("""          <p>In restaurants, bistro&rsquo;s en thuiskeukens van Knokke&#8209;Heist tot Brugge krijgen onze zwammen de hoofdrol: gegrild, gewokt of gewoon kort gebakken in goeie boter. Meer hebben ze niet nodig.</p>""",
     """          <p>Van sterrenzaak tot keukentafel: onze zwammen spelen overal de hoofdrol. Gegrild, gewokt of gewoon in goeie boter. Applaus is niet verplicht, maar het gebeurt.</p>"""),
    # eigenaar
    ("""<h2 id="eigenaar-h">Word eigenaar van je eigen oogst</h2>""",
     """<h2 id="eigenaar-h">Word eigenaar van je eigen oogst (ja, echt)</h2>"""),
    ("""          <p style="max-width: 44rem">De magie hoeft niet bij kijken te blijven: kweek zelf mee, thuis of in ons voedselbos.</p>""",
     """          <p style="max-width: 44rem">Kijken is leuk, oogsten is beter. Kweek zelf mee &mdash; thuis op het aanrecht of in ons voedselbos.</p>"""),
    ("""                <p>Kweek je eigen oesterzwammen vanuit je keuken. Eenvoudig, leerrijk en verrassend lekker.</p>""",
     """                <p>Oesterzwammen kweken naast je koffiezet. Eenvoudiger dan een kamerplant in leven houden.</p>"""),
    ("""                <p>Word mede-eigenaar van een stuk voedselbos en ontvang jaarlijks jouw oogst verse paddenstoelen.</p>""",
     """                <p>Jouw eigen boomstam in het voedselbos, jouw jaarlijkse oogst. Landeigenaar worden was nooit z&oacute; lekker.</p>"""),
    ("""          <p class="scene__beleven">Of kom het gewoon beleven: rondleidingen, proeverijen en workshops in de kwekerij.<a class="btn btn--cream" href="../contact/">Plan je bezoek</a></p>""",
     """          <p class="scene__beleven">Of kom gewoon eens kijken: rondleidingen, proeverijen en workshops. Wij praten, jij proeft.<a class="btn btn--cream" href="../contact/">Plan je bezoek</a></p>"""),
    # router
    ("""          <span class="line-1">Honger gekregen?</span>
          <span class="line-2">Vertel ons wie je bent.</span>""",
     """          <span class="line-1">Honger?</span>
          <span class="line-2">Dachten we al.</span>"""),
    ("""<p class="lead">Chef, grootkeuken of thuiskok: voor elk bord hebben we een aanbod op maat.</p>""",
     """<p class="lead">Chef, grootkeuken of thuiskok: zeg wie je bent, dan maken we het lekker concreet.</p>"""),
    ("""          <a class="btn btn--cream" href="../chefbox/#proefbox">Vraag je gratis proefbox aan</a>""",
     """          <a class="btn btn--cream" href="../chefbox/#proefbox">Gratis proefbox scoren</a>"""),
    ("""          <a class="cta-link" href="../bestel/">of bekijk hoe bestellen werkt</a>""",
     """          <a class="cta-link" href="../bestel/">of spiek hoe bestellen werkt</a>"""),
]

# ticker-items komen 2x voor (gedupliceerde track); alle andere slots 1x
EXPECTED = {"<span>Vijftien-plus soorten</span>": 2,
            "<span>Ambachtelijk gekweekt</span>": 2,
            "<span>100% lokaal</span>": 2}

for old, new in PAIRS:
    want = EXPECTED.get(old, 1)
    have = out.count(old)
    assert have == want, f"slot verwacht {want}x, gevonden {have}x: {old[:70]}..."
    out = out.replace(old, new)

os.makedirs("index-b", exist_ok=True)
open("index-b/index.html", "w").write(out)
print(f"index-b/index.html geschreven ({len(out.splitlines())} regels)")
