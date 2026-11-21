"""Merkmale für die Feinbestimmung im geführten Modus.

Nach dem Bestimmungsschlüssel stellt die App weitere Fragen (Form, Farbe, Glanz,
Gewicht, Härte, Salzsäure). Dafür werden die Tabellenangaben hier in grobe Gruppen
eingeteilt. Die Einteilung geschieht zunächst automatisch über Stichwörter in den
Spalten Farbe, Glanz, Ausbildung und Bemerkungen; wo das nicht passt, korrigiert die
Tabelle KORREKTUR am Ende von Hand.

Kürzel
  Farbe:  W farblos/weiß/silberweiß, G grau, Y gelb, R rot/rosa/orange, B braun,
          N grün, L blau/violett, S schwarz
  Glanz:  mt Metallglanz, gl Glas, d Diamant, f Fett/Harz/Wachs, p Perlmutt, s Seide, m matt
  Form:   wue würfelig, rh Rhomboeder, sae säulig, nad nadelig/faserig/strahlig,
          taf tafelig/blättrig, pyr spitz/(di)pyramidal, der derb/körnig, nie nierig/Krusten
  Salzsäure: k braust kräftig (kalt), w braust schwach (erst warm oder als Pulver),
          n braust nicht, None = keine Angabe (Mineral wird bei dieser Frage nicht ausgeschlossen)
  Quelle: T = steht in den Bemerkungen der Tabelle, L = nach Lehrbuchwissen ergänzt
Eine leere Liste bedeutet „unbekannt“: das Mineral bleibt bei dieser Frage im Rennen.
"""
import re

# Reihenfolge ist wichtig: längere Wörter zuerst, damit z. B. „gelbbraun“ gelb und braun trifft
FARBE = [
    ("W", r"farblos|weiß|wasserklar|silber|zinnweiß|trüb|milchig"),
    ("G", r"grau|bleigrau|stahlgrau|\basch"),
    ("Y", r"gelb|honig|erbsen|ocker|messing|gold|weingelb|beige|bernstein|citrin"),
    ("R", r"rot|rosa|orange|fleisch|himbeer|lachs|kupferrot|rötlich|scharlach|zinnober|blutrot|kirsch|nelken"),
    ("B", r"braun|bronze|bräunlich"),
    ("N", r"grün|oliv|smaragd|pistazien|apfelgrün|flaschengrün"),
    ("L", r"blau|violett|bläulich|lila|indigo|purpur"),
    ("S", r"schwarz|schwärzlich|pechschwarz|eisenschwarz|fast schwarz"),
]
ALLE_FARBEN = "alle farben|in allen farben|verschiedenfarbig|gefärbt"

GLANZ = [
    ("mt", r"metallisch|\bMgl\b"),
    ("gl", r"\bGlgl\b|glasglanz|wie Eis"),
    ("d", r"\bDgl\b"),
    ("f", r"\bFgl\b|\bHgl\b|Wachsglanz|Pechglanz"),
    ("p", r"\bPmgl\b"),
    ("s", r"\bSgl\b|seidig"),
    ("m", r"matt|porzellan|rau|erdig"),
]

FORM = [
    ("wue", r"würfel|oktaeder|rhombendodekaeder|ikositetraeder|tetraeder|tetraedrisch|pentagondodekaeder|isometrisch"),
    ("rh", r"rhomboeder|rhomboedrisch|sattelförmig"),
    ("sae", r"prismatisch|säulig|stengelig|stängelig|säulen|prismen|tonnenförmig|langprismatisch|kurzprismatisch|längsgestreift"),
    ("nad", r"nadel|nadlig|faser|strahlig|haarförmig|büschel|garben|fächer|sternförmig|watte|wabenförmig"),
    ("taf", r"tafel|tafelig|täfelchen|blättrig|blättchen|schuppig|plättchen|bleche|rosetten|briefkuvert|parkett"),
    ("pyr", r"pyramid|skalenoeder|speerspitz|spitzpyramidal|oktaederähnlich|linsenförmig"),
    ("der", r"derb|körnig|körner|dicht|spätig|massig|klumpen|eingesprengt|gerundet|zuckerkörnig|kompakt|grobspätig|rundliche"),
    ("nie", r"nierig|traubig|kruste|krustig|kugelig|knollig|stalaktit|überzug|anflug|schalig|halbkugelig|glaskopf|oolith|blumenkohl|sinter|erdig|mehlig|warzig|dendritisch|bäumchen|gestrickt|locken"),
]

# Salzsäure: nur Carbonate brausen. Alles, was hier nicht steht, gilt als „braust nicht“ (Lehrbuch).
SALZSAEURE = {
    "Calcit": ("k", "T"), "Aragonit": ("k", "T"), "Dolomit": ("w", "T"),
    "Strontianit": ("k", "L"), "Witherit": ("k", "L"), "Malachit": ("k", "L"), "Azurit": ("k", "L"),
    "Hydrozinkit": ("k", "L"),
    "Magnesit": ("w", "L"), "Siderit": ("w", "L"), "Rhodochrosit": ("w", "L"), "Smithsonit": ("w", "L"),
    "Galmei": ("w", "L"),
    "Cerussit": (None, "L"),        # wird mit Salpetersäure geprüft – hier keine Angabe
}

# Handkorrekturen: (Name, Tabelle) oder Name -> Felder, die die automatische Einteilung ersetzen
KORREKTUR = {
    "Anhydrit": dict(form="der wue"),                      # Spaltstücke würfelähnlich
    ("Anhydrit", "B 1.2 b"): dict(form="der"),
    "Chabasit": dict(form="wue rh nie"),
    "Phillipsit": dict(form="sae wue"),
    "Harmotom": dict(form="sae"),
    "Xenotim": dict(form="pyr sae"),
    "Apophyllit": dict(form="pyr taf"),
    "Cerussit": dict(farbe="WYBS", form="sae nad"),         # schwarz durch Bleiglanz
    "Anglesit": dict(farbe="WG", form="sae pyr"),
    "Witherit": dict(form="nad pyr"),
    "Fluorit": dict(form="wue der nie"),
    "Triplit–Zwieselit": dict(form="der"), "Triplit": dict(form="der"), "Zwieselit": dict(form="der"),
    "Staurolith": dict(form="sae"),
    "Titanit": dict(form="taf pyr sae"), "Sphen": dict(form="taf sae"),
    "Monazit": dict(form="taf der"),
    "Graphit": dict(form="taf der"), "Molybdänit": dict(form="taf"), "Covellin": dict(form="taf der"),
    "Silber": dict(form="der wue taf nie"), "Gold": dict(form="der taf nie"), "Kupfer": dict(form="der taf nie"),
    "Wismut": dict(form="der rh"), "Antimon": dict(form="der"), "Arsen": dict(form="nie der"),
    "Galenit": dict(form="wue der"), "Bleiglanz": dict(form="der"),
    "Pyrit": dict(form="wue der"), "Markasit": dict(form="pyr nad nie"),
    "Magnetit": dict(form="wue der"), "Chromit": dict(form="der wue"), "Franklinit": dict(form="wue der"),
    "Linneit": dict(form="wue der"), "Gersdorffit": dict(form="wue der"), "Ullmannit": dict(form="wue der"),
    "Cobaltit": dict(form="wue der"), "Chloanthit": dict(form="wue der"), "Skutterudit": dict(form="wue der"),
    "Uraninit": dict(form="der nie wue"), "Arsenopyrit": dict(form="der sae pyr"),
    "Bournonit": dict(form="der taf"), "Kupferglanz": dict(form="der taf"), "Bornit": dict(form="der"),
    "Silberglanz": dict(form="der"), "Tennantit": dict(form="der wue"), "Tetraedrit": dict(form="der wue"),
    "Sphalerit": dict(form="der wue"), "Cuprit": dict(form="der wue nad"), "Wurtzit": dict(form="nad nie"),
    "Pyrrhotin": dict(form="der taf"), "Nickelin": dict(form="der"), "Löllingit": dict(form="der sae"),
    "Wolframit": dict(form="taf nad"), "Ferberit": dict(form="taf nad"),
    "Niobit": dict(form="taf"), "Tantalit": dict(form="sae"), "Mangantantalit": dict(form="taf"),
    "Rutil": dict(form="sae nad der"), "Kassiterit": dict(form="sae der pyr"), "Hämatit": dict(form="taf der"),
    ("Hämatit", "B 2.3"): dict(form="nie nad der"), "Ilmenit": dict(form="der taf"),
    "Zinkit": dict(form="der"), "Pyrargyrit": dict(form="der sae"), "Proustit": dict(form="der sae"),
    "Enargit": dict(form="der sae"), "Millerit": dict(form="nad der"), "Manganit": dict(form="sae nad"),
    "Pyrolusit": dict(form="nad der"), ("Pyrolusit", "A 1.2 a"): dict(form="sae pyr"),
    "Braunit": dict(form="der pyr"), "Bismuthinit": dict(form="nad sae der"), "Antimonit": dict(form="sae nad"),
    "Jamesonit": dict(form="nad sae"), "Boulangerit": dict(form="nad der"),
    "Pyrop": dict(form="der wue"), "Almandin": dict(form="der wue"), "Spessartin": dict(form="der wue"),
    "Grossular": dict(form="der wue"), "Andradit": dict(form="der wue"), "Uwarowit": dict(form="der wue"),
    "Analcim": dict(form="wue der"), "Leucit": dict(form="wue"), "Sodalith": dict(form="wue der"),
    "Hauyn": dict(form="wue der"), "Lasurit": dict(form="der wue"), "Spinell": dict(form="wue"),
    "Diamant": dict(form="wue"), "Periklas": dict(form="der"), "Perowskit": dict(form="wue"),
    "Boracit": dict(form="wue"), "Cristobalit": dict(form="wue"), "Steinsalz": dict(form="wue der nad"),
    "Sylvin": dict(form="wue der"), "Kryolith": dict(form="der wue"),
    "Quarz": dict(farbe="WGYRBL", form="sae der"),   # Farben laut Bemerkung (Citrin, Rauchquarz, Amethyst …) "Chalcedon": dict(form="nie der"), "Opal": dict(form="nie der"),
    "Beryll": dict(form="sae"), "Turmalin": dict(form="sae nad"), "Zirkon": dict(form="sae pyr"),
    "Topas": dict(form="sae"), "Korund": dict(form="der sae pyr"), "Chrysoberyll": dict(form="taf"),
    "Phenakit": dict(form="rh sae"), "Olivin": dict(form="der"), "Cordierit": dict(form="der sae"),
    "Andalusit": dict(form="sae"), "Vesuvian": dict(form="der sae"), "Epidot": dict(form="nad sae der"),
    "Axinit": dict(form="taf"), "Prehnit": dict(form="nad nie"), "Tridymit": dict(form="taf"),
    "Calcit": dict(form="rh der pyr"), "Dolomit": dict(form="der rh"), "Magnesit": dict(form="der rh nad"),
    ("Magnesit", "B 1.3 b"): dict(form="nie der"), "Siderit": dict(form="der rh"), "Rhodochrosit": dict(form="der nie"),
    "Smithsonit": dict(form="nie der rh"), "Aragonit": dict(form="nad sae nie"), "Strontianit": dict(form="nad"),
    "Baryt": dict(form="der sae taf"), "Coelestin": dict(form="sae taf"), "Gips": dict(form="sae der"),
    ("Gips", "B 1.1 b"): dict(form="der nad"), "Wulfenit": dict(form="taf pyr"), "Vanadinit": dict(form="sae"),
    "Pyromorphit": dict(form="nie sae"), "Mimetesit": dict(form="nie sae"), "Apatit": dict(form="sae taf nad"),
    "Scheelit": dict(form="pyr"), "Anatas": dict(form="pyr"), "Brookit": dict(form="taf pyr"),
    "Augit": dict(form="der sae"), "Hornblende": dict(form="der sae nad"), ("Hornblende", "B 2.3"): dict(form="sae"),
    "Diopsid": dict(form="der sae"), "Hedenbergit": dict(form="der sae"), "Omphacit": dict(form="der"),
    "Ägirin": dict(form="sae"), "Jadeit": dict(form="der"), "Spodumen": dict(form="der sae"),
    "Orthoklas": dict(form="der sae taf"), "Mikroklin": dict(form="der sae taf"), "Sanidin": dict(form="taf"),
    "Adular": dict(form="sae"), "Albit": dict(form="taf der"), "Oligoklas": dict(farbe="W", form="taf der"),
    "Andesin": dict(farbe="W", form="taf der"), "Labradorit": dict(form="taf der"), "Bytownit": dict(farbe="W", form="taf der"),
    "Anorthit": dict(form="der sae"), "Petalit": dict(form="der"), "Amblygonit": dict(form="der sae"),
    "Skapolith": dict(form="der sae nad"), "Nephelin": dict(form="der sae"), "Rhodonit": dict(form="der taf"),
    "Kyanit": dict(form="sae nad"), "Sillimanit": dict(form="nad"), "Wollastonit": dict(form="nad sae"),
    "Zoisit": dict(form="sae nad"), "Dumortierit": dict(form="nad"), "Diaspor": dict(form="taf sae"),
    "Chloritoid": dict(form="taf"), "Türkis": dict(form="nie"), "Lazulith": dict(form="der pyr"),
    "Willemit": dict(form="der sae"), "Dioptas": dict(form="sae rh nie"),
    "Hemimorphit": dict(form="nad nie"), "Wavellit": dict(form="nad nie"), "Natrolith": dict(form="nad sae"),
    "Laumontit": dict(form="nad sae der"), "Heulandit": dict(form="taf"), "Stilbit": dict(form="nad taf"),
    "Margarit": dict(form="taf der"), "Kieserit": dict(form="der"), "Epsomit": dict(form="nie nad sae"),
    "Kernit": dict(form="der nad"), "Borax": dict(form="der sae"), "Carnallit": dict(form="der"),
    "Schwefel": dict(form="der pyr"), "Ulexit": dict(form="nad"), "Kaolinit": dict(form="der taf"),
    "Sepiolith": dict(form="nie der"), "Hydrozinkit": dict(form="nie der"),
    "Talk": dict(form="taf der"), ("Talk", "B 1.1 b"): dict(form="der"), "Pyrophyllit": dict(form="taf nad der"),
    ("Pyrophyllit", "B 1.1 b"): dict(form="der"), "Chlorit": dict(form="taf"), "Kämmererit": dict(form="taf"),
    "Brucit": dict(form="taf der"), "Muskovit": dict(form="taf"), "Zinnwaldit": dict(form="taf"),
    "Lepidolith": dict(form="taf nie"), "Phlogopit": dict(form="taf"), "Biotit": dict(form="taf"),
    "Chrysotil": dict(form="nad"), "Antigorit": dict(form="der"), "Annabergit": dict(form="nie"),
    "Erythrin": dict(form="nie nad taf"), "Vivianit": dict(form="nad taf nie"), "Torbernit": dict(form="taf pyr"),
    "Autunit": dict(form="taf"), "Uranocircit": dict(form="taf"), "Realgar": dict(form="der nie sae"),
    "Auripigment": dict(form="nie sae taf"), "Zinnober": dict(form="der nie"), "Krokoit": dict(form="sae nad"),
    "Descloizit": dict(form="nie sae pyr"), "Mottramit": dict(form="nie"), "Olivenit": dict(form="nie nad"),
    "Brochantit": dict(form="der nad"), "Malachit": dict(form="nie nad"), "Azurit": dict(form="nie nad"),
    "Rockbridgeit": dict(form="nad"), "Chrysokoll": dict(form="nie der"), "Goethit": dict(form="nad nie"),
    "Lepidokrokit": dict(form="taf"), "Kryptomelan": dict(form="nie der"), "Psilomelan": dict(form="nie"),
    "Wad": dict(form="nie der"), "Schalenblende": dict(form="nie"), "Phosphorit": dict(form="nie der"),
    "Galmei": dict(form="der nie"), "Arfvedsonit": dict(form="sae"), "Tremolit": dict(form="nad sae"),
    "Aktinolith": dict(form="nad sae"), "Bronzit": dict(form="der"), "Hypersthen": dict(form="der"),
    "Melilith": dict(form="taf"), "Triphylin": dict(form="der"), "Lithiophilit": dict(form="der"),
}


def _codes(regeln, text):
    return [k for k, rx in regeln if re.search(rx, text, re.I)]


def merkmale(r):
    """Gibt die Merkmalsgruppen eines Tabelleneintrags zurück (Dictionary)."""
    farbe = r["farbe"]
    f = "".join(_codes(FARBE, farbe))
    if re.search(ALLE_FARBEN, farbe, re.I):
        f = "WGYRBNLS"
    g = _codes(GLANZ, r["glanz"])
    form = _codes(FORM, r["ausb"] + " " + r["bem"])
    hcl, q = SALZSAEURE.get(r["name"], ("n", "L"))
    korr = dict(KORREKTUR.get(r["name"], {}))
    korr.update(KORREKTUR.get((r["name"], r["tab"]), {}))
    if "farbe" in korr:
        f = korr["farbe"]
    if "form" in korr:
        form = korr["form"].split()
    return {"f": f, "g": g, "form": form, "hcl": hcl, "q": q}
