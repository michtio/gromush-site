#!/usr/bin/env python3
"""Genereer /index-b/ (kopijdeck B, uitgesproken speels) vanuit index.html.

Structuurwijzigingen gebeuren altijd eerst in index.html (deck A); daarna
dit script draaien vanaf de repo-root:  python3 _resources/build-variant-b.py

Elke (A, B)-tekstpaar hieronder moet exact het verwachte aantal keer
voorkomen — het script faalt luid als een slot niet meer matcht, zodat de
decks nooit stil uiteenlopen.

Scene-volgorde (index.html): hero, kweek, varieties, proces (incl. de
compacte founder-noot), route, plate, beleef, eigenaar, router.
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
    # ---- hero ----------------------------------------------------------
    ("""<span class="kicker">GroMush &mdash; Knokke&#8209;Heist &middot; Ontdek de magie</span>""",
     """<span class="kicker">GroMush &mdash; Knokke&#8209;Heist &middot; Schimmels met een reputatie</span>"""),
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
    # ---- ticker (items komen 2x voor in de gedupliceerde track) ---------
    ("<span>Dagvers geplukt</span>", "<span>Vanmorgen nog geplukt</span>"),
    ("<span>100% lokaal</span>", "<span>100% lokaal (echt)</span>"),
    ("<span>Vijftien-plus soorten</span>", "<span>Vijftien-plus soorten, nul photoshop</span>"),
    ("<span>Ambachtelijk gekweekt</span>", "<span>Gekweekt met obsessie</span>"),
    ("<span>Van kwekerij tot keuken in 30 minuten</span>",
     "<span>Van kwekerij tot keuken in 30 minuten, zonder file</span>"),
    # ---- kweek ---------------------------------------------------------
    ("""<span class="kicker"><span class="kicker__chapter">1</span>De kweek</span>""",
     """<span class="kicker"><span class="kicker__chapter">1</span>Waar het gebeurt</span>"""),
    ("""          <span class="line-1">Binnen &eacute;n buiten.</span>
          <span class="line-2">&Eacute;&eacute;n passie.</span>""",
     """          <span class="line-1">Twee werelden.</span>
          <span class="line-2">Nul compromissen.</span>"""),
    ("""<p class="lead" style="max-width: 42rem; margin-inline: auto">Onze zwammen groeien op twee plekken die niet harder konden verschillen &mdash; en dat proef je.</p>""",
     """<p class="lead" style="max-width: 42rem; margin-inline: auto">Een zeecontainer met paars licht en een voedselbos vol vogels. Onze zwammen kiezen zelf hun vibe.</p>"""),
    ("""<p class="kweek__note">Op beide plekken doet hetzelfde onzichtbare draadnetwerk het werk: <strong>mycelium</strong>. Wij geven het vers substraat, vocht en tijd; de natuur regelt de oogst.</p>""",
     """<p class="kweek__note">Op beide plekken doet hetzelfde onzichtbare draadnetwerk het werk: <strong>mycelium</strong>. Wij leveren substraat, vocht en veel geduld. Mycelium doet de rest en stuurt geen factuur.</p>"""),
    ("""            <h3>Binnenkweek <span class="accent">&middot; de zeecontainer</span></h3>""",
     """            <h3>Binnenkweek <span class="accent">&middot; de discocontainer</span></h3>"""),
    ("""            <p>Gecontroleerde vochtigheid, mist en licht: hier oogsten we het hele jaar door oesterzwammen van constante topkwaliteit.</p>""",
     """            <p>Mist, paars licht en een strak klimaat: het ziet eruit als sciencefiction, maar er groeit gewoon topkwaliteit. Het hele jaar door.</p>"""),
    ("""            <h3>Buitenkweek <span class="accent">&middot; het voedselbos</span></h3>""",
     """            <h3>Buitenkweek <span class="accent">&middot; het bos doet mee</span></h3>"""),
    ("""            <p>Op boomstammen, op het ritme van de seizoenen: shiitake en bosgenoten groeien hier 100% natuurlijk.</p>""",
     """            <p>Boomstammen, seizoenen en verder niets: hier doet de natuur het werk. Wij komen vooral oogsten.</p>"""),
    ("""<p class="scene__hook">Maar wat groeit daar dan allemaal?</p>""",
     """<p class="scene__hook">Ja maar, wat komt daar dan uit?</p>"""),
    # ---- varieties -----------------------------------------------------
    ("""            <span class="line-1">Zeven oesterzwammen.</span>
            <span class="line-2">&Eacute;&eacute;n familie.</span>""",
     """            <span class="line-1">Zeven oesterzwammen.</span>
            <span class="line-2">Zeven persoonlijkheden.</span>"""),
    ("""<p class="lead" style="max-width: 42rem; margin-inline: auto">Van de klassieke grijze tot de diepzwarte Black Pearl: elke oesterzwam heeft een eigen kleur, beet en smaak. En daarnaast kweken we shiitake, nameko, pioppino, morieltje en meer &mdash; ruim vijftien soorten in totaal.</p>""",
     """<p class="lead" style="max-width: 42rem; margin-inline: auto">Van de brave grijze tot de Black Pearl die n&eacute;t iets te mysterieus doet: allemaal oesterzwam, allemaal karakter. Daarnaast staan shiitake, nameko, pioppino en morieltje te wachten op hun moment &mdash; ruim vijftien soorten in totaal.</p>"""),
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
    ("""          <a class="btn btn--cream" href="../oesterzwammen/">Bekijk alle soorten</a>""",
     """          <a class="btn btn--cream" href="../oesterzwammen/">Ontdek alle soorten (sommige zijn camerashy)</a>"""),
    # ---- proces --------------------------------------------------------
    ("""<span class="kicker"><span class="kicker__chapter">3</span>Ons werkproces</span>""",
     """<span class="kicker"><span class="kicker__chapter">3</span>Hoe het werkt</span>"""),
    ("""<h2 id="proces-h">Van stro tot bord</h2>""",
     """<h2 id="proces-h">Van stro tot bord &mdash; met een vleugje magie</h2>"""),
    ("""<p class="lead" style="max-width: 44rem">Zwammen kweken is koken in slow motion: eerst alles kiemvrij, dan zaaien, dan vooral geduld.</p>""",
     """<p class="lead" style="max-width: 44rem">Zwammen kweken is koken in slow motion: eerst alles kiemvrij, dan zaaien, dan heel lang niets doen. Dat laatste is het moeilijkste.</p>"""),
    ("""            <h3>Schoon beginnen <span class="process__term">(pasteuriseren)</span></h3>
            <p>We stomen stro en substraat kiemvrij &mdash; zo krijgen alleen &oacute;nze zwammen een kans.</p>""",
     """            <h3>Grote schoonmaak <span class="process__term">(pasteuriseren)</span></h3>
            <p>We stomen stro en substraat kiemvrij. Sorry ongenode schimmels: geen toegang.</p>"""),
    ("""            <h3>Zaaien <span class="process__term">(inoculeren)</span></h3>
            <p>We mengen mycelium &mdash; het &lsquo;zaad&rsquo; van de zwam &mdash; door het substraat.</p>""",
     """            <h3>Zaaien <span class="process__term">(inoculeren)</span></h3>
            <p>We mengen mycelium door het substraat. Zeg maar het zaadje van de zwam, alleen met duizend armen.</p>"""),
    ("""            <h3>Laten doorgroeien</h3>
            <p>Weken van rust en warmte: het mycelium doorweeft het substraat als wortels.</p>""",
     """            <h3>Laten doorgroeien</h3>
            <p>Weken rust en warmte. Wij kijken toe en doen alsof we niet ongeduldig zijn.</p>"""),
    ("""            <h3>Zwammen laten komen</h3>
            <p>Frisse lucht en vocht geven het startsein: tijd om paddenstoelen te maken.</p>""",
     """            <h3>Zwammen laten komen</h3>
            <p>Frisse lucht en vocht als startsein. En dan gaat het pl&oacute;ts razendsnel.</p>"""),
    ("""            <h3>Plukken</h3>
            <p>Met de hand, precies op het juiste moment.</p>""",
     """            <h3>Plukken</h3>
            <p>Met de hand, op het juiste moment. Te vroeg is jammer, te laat is zonde.</p>"""),
    ("""            <h3>Op jouw bord</h3>
            <p>Dagvers geleverd voor optimale smaak.</p>""",
     """            <h3>Op jouw bord</h3>
            <p>Dagvers geleverd. Vanaf hier is het jouw verdienste.</p>"""),
    ("""            <span class="kicker">De kweker</span>""",
     """            <span class="kicker">De schuldige</span>"""),
    ("""            <h3>Het begon met een fascinatie</h3>""",
     """            <h3>Begonnen uit pure obsessie</h3>"""),
    ("""            <p>Geen gat in de markt, maar een jarenlange fascinatie voor mycelium: zo ontstond GroMush. Een kleinschalige kwekerij in Knokke&#8209;Heist waar ik elke kweekcyclus met de hand opvolg, van substraat tot oogst.</p>""",
     """            <p>Geen gat in de markt, wel een jarenlange obsessie voor mycelium. Zo ontstond GroMush: een kleinschalige kwekerij in Knokke&#8209;Heist waar ik elke kweekcyclus persoonlijk opvolg. De zwammen en ik, wij hebben iets.</p>"""),
    ("""            <p class="scene__signoff">&mdash; Anthony Watteeuw, kweker</p>""",
     """            <p class="scene__signoff">&mdash; Anthony Watteeuw, kweker (en voltijds mycelium-fan)</p>"""),
    ("""            <a class="btn btn--cream" href="../over-ons/">Lees het hele verhaal</a>""",
     """            <a class="btn btn--cream" href="../over-ons/">Lees het hele verhaal (het is lang)</a>"""),
    ("""<!-- copy: proces.sticker --><span class="sticker" aria-hidden="true">Ambachtelijke teelt</span>""",
     """<!-- copy: proces.sticker --><span class="sticker" aria-hidden="true">Handwerk, hoor</span>"""),
    # ---- route ---------------------------------------------------------
    ("""<h2 id="route-h">Geen voedselkilometers, <span class="accent">wel smaak</span></h2>""",
     """<h2 id="route-h">Voedselkilometers? Wij doen <span class="accent">voedselmeters</span></h2>"""),
    ("""            <p>Veel bijzondere paddenstoelen leggen duizenden kilometers af voor ze op een bord belanden. De onze hooguit dertig minuten: &rsquo;s ochtends geoogst, dagvers geleverd in Knokke&#8209;Heist, Damme en Brugge. Zonder omweg, zonder koelcel-marathon.</p>""",
     """            <p>Sommige paddenstoelen vliegen business class de halve wereld rond. De onze zitten hooguit een half uurtje in een bestelwagentje richting Knokke&#8209;Heist, Damme of Brugge. Jetlagvrij, dus.</p>"""),
    ("""<span class="stat__label">voedselkilometers</span>""",
     """<span class="stat__label">voedselkilometers, geteld</span>"""),
    ("""<span class="stat__label">soorten paddenstoelen</span>""",
     """<span class="stat__label">soorten, en er komen er bij</span>"""),
    ("""<!-- copy: route.sticker --><span class="sticker sticker--sand scene__sticker" aria-hidden="true">Dagvers geleverd</span>""",
     """<!-- copy: route.sticker --><span class="sticker sticker--sand scene__sticker" aria-hidden="true">Geen jetlag</span>"""),
    ("""<p class="scene__hook">En dan: het bord.</p>""",
     """<p class="scene__hook">Volgende halte: jouw bord.</p>"""),
    # ---- plate ---------------------------------------------------------
    ("""<h2 id="plate-h">Waar chefs ze laten schitteren</h2>""",
     """<h2 id="plate-h">Chefs staan er (beleefd) voor in de rij</h2>"""),
    ("""          <p>In restaurants, bistro&rsquo;s en thuiskeukens van Knokke&#8209;Heist tot Brugge krijgen onze zwammen de hoofdrol: gegrild, gewokt of gewoon kort gebakken in goeie boter. Meer hebben ze niet nodig.</p>""",
     """          <p>Van sterrenzaak tot keukentafel: onze zwammen spelen overal de hoofdrol. Gegrild, gewokt of gewoon in goeie boter. Applaus is niet verplicht, maar het gebeurt.</p>"""),
    # ---- beleef --------------------------------------------------------
    ("""<span class="kicker"><span class="kicker__chapter">6</span>Beleef het zelf</span>""",
     """<span class="kicker"><span class="kicker__chapter">6</span>Kom eens langs</span>"""),
    ("""<h2 id="beleef-h">Zes manieren om de kwekerij binnen te stappen</h2>""",
     """<h2 id="beleef-h">Zes manieren om bij ons binnen te vallen</h2>"""),
    ("""<p class="lead" style="max-width: 44rem">Het netwerk onder de grond verbindt alles met alles. Bovengronds doen wij hetzelfde: van rondleiding tot oogstdag, kies wat bij je past en kom langs.</p>""",
     """<p class="lead" style="max-width: 44rem">Onder de grond verbindt het mycelium alles met alles. Bovengronds doen wij hetzelfde: van rondleiding tot oogstdag, kies wat bij je past en val gerust binnen.</p>"""),
    ("""              <p>Wandel mee door de zeecontainer en het voedselbos. Je ziet, ruikt en voelt hoe een zwam ontstaat.</p>""",
     """              <p>Wandel mee door de zeecontainer en het voedselbos. Je ziet, ruikt en voelt hoe een zwam ontstaat. Meestal wil daarna niemand nog naar buiten.</p>"""),
    ("""              <p>Maak je eigen kweekemmer en neem hem mee naar huis. Enkele weken later oogst je op je aanrecht.</p>""",
     """              <p>Maak je eigen kweekemmer en neem hem mee naar huis. Enkele weken later staat er oogst op je aanrecht. Opscheppen mag.</p>"""),
    ("""              <p>Zeven soorten naast elkaar op tafel. Je smaakt meteen waarom chefs zo kieskeurig zijn.</p>""",
     """              <p>Zeven soorten naast elkaar op tafel. Je smaakt meteen waarom chefs zo kieskeurig d&oacute;en.</p>"""),
    ("""              <p>Een chef kookt ter plaatse met wat die ochtend geoogst is. Kleine tafel, groot bord.</p>""",
     """              <p>Een chef kookt ter plaatse met wat die ochtend geoogst is. Kleine tafel, groot bord, geen menukaart.</p>"""),
    ("""              <p>Op verkenning tussen de boomstammen: hoe een bos eten geeft en er vooral niets voor terugvraagt.</p>""",
     """              <p>Op verkenning tussen de boomstammen: hoe een bos eten geeft en er niets voor terugvraagt. Behalve wat regen.</p>"""),
    ("""              <p>Twee keer per jaar oogsten we samen. Jij plukt, wij zorgen voor koffie en verhalen.</p>""",
     """              <p>Twee keer per jaar oogsten we samen. Jij plukt, wij zorgen voor koffie en veel te lange verhalen.</p>"""),
    ("""<a class="beleef__card-cta" href="../contact/">Plan je bezoek</a>""",
     """<a class="beleef__card-cta" href="../contact/">Zet je naam op de lijst</a>"""),
    # ---- eigenaar ------------------------------------------------------
    ("""          <span class="kicker">Zelf aan de slag</span>""",
     """          <span class="kicker">Zelf proberen</span>"""),
    ("""<h2 id="eigenaar-h">Word eigenaar van je eigen oogst</h2>""",
     """<h2 id="eigenaar-h">Word eigenaar van je eigen oogst (ja, echt)</h2>"""),
    ("""          <p style="max-width: 44rem">De magie hoeft niet bij kijken te blijven: kweek zelf mee, thuis of in ons voedselbos.</p>""",
     """          <p style="max-width: 44rem">Kijken is leuk, oogsten is beter. Kweek zelf mee &mdash; thuis op het aanrecht of in ons voedselbos.</p>"""),
    ("""                <h3>Eigen kweekemmer</h3>""",
     """                <h3>Je eigen kweekemmer</h3>"""),
    ("""                <p>Kweek je eigen oesterzwammen vanuit je keuken. Eenvoudig, leerrijk en verrassend lekker.</p>""",
     """                <p>Oesterzwammen kweken naast je koffiezet. Eenvoudiger dan een kamerplant in leven houden.</p>"""),
    ("""                <h3>Eigen boomstam</h3>""",
     """                <h3>Je eigen boomstam</h3>"""),
    ("""                <p>Word mede-eigenaar van een stuk voedselbos en ontvang jaarlijks jouw oogst verse paddenstoelen.</p>""",
     """                <p>Jouw eigen boomstam in het voedselbos, jouw jaarlijkse oogst. Landeigenaar worden was nooit z&oacute; lekker.</p>"""),
    ("""          <p class="scene__beleven">Vertel ons wat je van plan bent: thuis op het aanrecht of een stam in het bos. We zetten je op weg.<a class="btn btn--cream" href="../contact/">Vraag info aan</a></p>""",
     """          <p class="scene__beleven">Zeg maar wat je van plan bent: aanrecht of boomstam. Wij zetten je op weg, met net iets te veel enthousiasme.<a class="btn btn--cream" href="../contact/">Vraag info aan</a></p>"""),
    # ---- router --------------------------------------------------------
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

# Slots die meer dan 1x in de markup staan. De ticker-track is gedupliceerd
# voor de naadloze marquee-lus; de beleef-kaarten delen dezelfde CTA.
EXPECTED = {
    "<span>Dagvers geplukt</span>": 2,
    "<span>100% lokaal</span>": 2,
    "<span>Vijftien-plus soorten</span>": 2,
    "<span>Ambachtelijk gekweekt</span>": 2,
    "<span>Van kwekerij tot keuken in 30 minuten</span>": 2,
    """<a class="beleef__card-cta" href="../contact/">Plan je bezoek</a>""": 6,
}

for old, new in PAIRS:
    want = EXPECTED.get(old, 1)
    have = out.count(old)
    assert have == want, f"slot verwacht {want}x, gevonden {have}x: {old[:70]}..."
    out = out.replace(old, new)

# Deck B mag speels zijn, maar niet strijdlustig.
assert "vecht" not in out.lower(), "deck B: 'vechten' hoort hier niet"

# Elk kopijslot van deck A moet ook in deck B staan (zelfde skelet).
slots_a = set(re.findall(r'<!-- copy: ([\w.\-]+) -->', src))
slots_b = set(re.findall(r'<!-- copy: ([\w.\-]+) -->', out))
assert slots_a == slots_b, f"kopijslots lopen uiteen: {slots_a ^ slots_b}"

os.makedirs("index-b", exist_ok=True)
open("index-b/index.html", "w").write(out)
print(f"index-b/index.html geschreven ({len(out.splitlines())} regels, "
      f"{len(PAIRS)} kopijslots vervangen, {len(slots_a)} slots in het skelet)")
