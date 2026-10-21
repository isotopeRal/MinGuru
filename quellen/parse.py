import json, re, csv
from mindat_ids import M as MINDAT, url as mindat_url

SUB = str.maketrans("0123456789,", "₀₁₂₃₄₅₆₇₈₉,")
BAR = "\u0304"

def formel(s):
    if s.startswith("!"):
        return s[1:]
    # Ziffern (ggf. mit Dezimalkomma) direkt nach Buchstabe oder schließender Klammer -> tiefgestellt
    return re.sub(r"(?<=[A-Za-z\)\]⁺])(\d+(?:,\d+)?)", lambda m: m.group(1).translate(SUB), s)

def miller(s):
    # (10-11) -> (101̄1); nur Klammern mit Ziffern und Minus
    def rep(m):
        inner = re.sub(r"-(\d)", lambda k: k.group(1) + BAR, m.group(1))
        return "(" + inner + ")"
    return re.sub(r"\(([-\d]{3,7})\)", rep, s)

def klasse(s):
    return re.sub(r"(?<![\w.])-(\d)", lambda k: k.group(1) + BAR, s)

def rng(s, kind):
    t = s.replace("½", ".5").replace(",", ".")
    if "n.b" in t:
        return None, None
    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", t)]
    if not nums:
        return None, None
    if t.strip().startswith("<"):
        return nums[0] - 0.5, nums[0]
    if t.strip().startswith(">"):
        return nums[0], nums[0] + 1
    return min(nums), max(nums)

SYS = [("kub", "kubisch"), ("tetrag", "tetragonal"), ("hexag", "hexagonal"), ("trig", "trigonal"),
       ("orthorh", "orthorhombisch"), ("monokl", "monoklin"), ("trikl", "triklin")]

def systeme(s):
    t = s.lower()
    t = re.sub(r"(ps\.-|pseudo-?)[a-zä]+", "", t)
    t = t.replace("morphologisch", "")
    if "amorph" in t:
        return ["amorph"]
    out = [name for key, name in SYS if key in t]
    if not out:
        if "pseudo" in s.lower():
            out = ["pseudo"]
    return out

STRICH = {"A1": "weiß, grau oder schwarz", "A2": "gelb, rot oder braun",
          "B1": "farblos, weiß oder sehr blass", "B2": "gelb, rot, braun (schwarz)", "B3": "grün oder blau"}

rows, tables = [], []
cur = None
for line in open("mineral_daten.txt", encoding="utf-8"):
    line = line.rstrip("\n")
    if not line.strip() or (line.startswith("#") and not line.startswith("#T")):
        continue
    f = [x.strip() for x in line.split(";;")]
    if f[0] == "#T":
        cur = dict(tab=f[1], seite=int(f[2]), glanzgr=f[3], strichgr=f[4], spaltgr=f[5] or "", titel=f[6])
        tables.append(dict(cur, n=0))
        continue
    while len(f) < 14:
        f.append("")
    name, syn, fo, H, D, farbe, strich, glanz, system, ausb, spalt, bem, vork, anm = f[:14]
    hmin, hmax = rng(H, "H")
    dmin, dmax = rng(D, "D")
    r = dict(
        name=name, syn=syn, formel=formel(fo), H=H.replace("-", "–"), D=D.replace("-", "–"),
        hmin=hmin, hmax=hmax, dmin=dmin, dmax=dmax,
        farbe=farbe, strich=strich or STRICH[cur["strichgr"]],
        glanz=glanz or "metallisch / halbmetallisch",
        system=klasse(system), sys=systeme(system), ausb=ausb,
        spalt=miller(spalt), bem=miller(bem), vork=vork, anm=anm,
        tab=cur["tab"], seite=cur["seite"], glanzgr=cur["glanzgr"], strichgr=cur["strichgr"],
        spaltgr=cur["spaltgr"],
    )
    r["mindat"] = mindat_url(name)
    r["mindat_en"] = MINDAT[name][0]
    rows.append(r)
    tables[-1]["n"] += 1

# "auch in": gleiche Namen in anderen Tabellen
for r in rows:
    r["auch"] = sorted({x["tab"] for x in rows if x["name"] == r["name"] and x["tab"] != r["tab"]})

gems = [
    ["Beryll", "gelb", "Goldberyll"], ["Beryll", "grüngelb", "Heliodor"], ["Beryll", "hellblau", "Aquamarin"],
    ["Beryll", "grün", "Smaragd"], ["Beryll", "rosa", "Morganit"],
    ["Chrysoberyll", "Farbwechsel: grün (Tageslicht), rot (Lampenlicht)", "Alexandrit"],
    ["Granat: Pyrop-Almandin", "rot (ohne Braunstich)", "Rhodolith"],
    ["Granat: Grossular mit Fe", "bernsteinfarbig bis gelbrot", "Hessonit"],
    ["Granat: Grossular mit V", "smaragdgrün", "„Tsavorit“ (Handelsname)"],
    ["Granat: Andradit mit Cr", "gelbgrün", "Demantoid"],
    ["Korund", "blau", "Saphir"], ["Korund", "rot", "Rubin"], ["Korund", "gelb", "gelber Saphir, Goldsaphir"],
    ["Korund", "farblos", "Leukosaphir"],
    ["Spodumen", "hellgrün", "Hiddenit"], ["Spodumen", "violettrosa", "Kunzit"],
    ["Turmalin", "grün", "Verdelith"], ["Turmalin", "rot", "Rubellit"], ["Turmalin", "blau", "Indigolith"],
    ["Turmalin", "farblos", "Achroit"],
    ["Zirkon", "gelbrot", "Hyazinth"], ["Zoisit", "blau", "„Tansanit“ (Handelsname)"],
]
effekte = [
    ["Sternrubin, Sternsaphir", "orientierte Rutil-Entmischungen"],
    ["„Katzenaugeneffekt“", "bei Chrysoberyll, Turmalin, Quarz u. a. (orientierte sehr feine Hohlkanäle)"],
    ["Tigerauge, Falkenauge", "„verquarzter“ faseriger Krokydolith"],
    ["„Sonnenstein“", "Oligoklas mit orientierten Hämatitschüppchen"],
    ["Mondstein", "Feldspäte mit submikroskopischen Entmischungslamellen"],
]

json.dump(dict(rows=rows, tables=tables, gems=gems, effekte=effekte),
          open("data.json", "w", encoding="utf-8"), ensure_ascii=False)

with open("Mineralbestimmungstabellen_TU_Berlin.csv", "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.writer(fh, delimiter=";")
    w.writerow(["Tabelle", "Seite", "Glanz-Gruppe", "Strich-Gruppe", "Spaltbarkeit (Tabelle)", "Name", "Synonyme",
                "Formel", "Härte", "H min", "H max", "Dichte", "D min", "D max", "Farbe", "Strich", "Glanz",
                "Kristallsystem/-klasse", "Ausbildung", "Spaltbarkeit/Bruch", "Bemerkungen",
                "Typisches Vorkommen", "Anmerkung Transkription", "mindat-Name", "mindat-Link"])
    for r in rows:
        w.writerow([r["tab"], r["seite"], "metallisch" if r["glanzgr"] == "A" else "nichtmetallisch",
                    STRICH[r["strichgr"]], r["spaltgr"] or "nicht unterschieden", r["name"], r["syn"], r["formel"],
                    r["H"], r["hmin"], r["hmax"], r["D"], r["dmin"], r["dmax"], r["farbe"], r["strich"],
                    r["glanz"], r["system"], r["ausb"], r["spalt"], r["bem"], r["vork"], r["anm"], r["mindat_en"], r["mindat"]])

print(len(rows), "Zeilen,", len({r['name'] for r in rows}), "verschiedene Namen")
for t in tables:
    print(f"{t['tab']:<20} S.{t['seite']:<3} {t['n']}")
probl = [r["name"] + " " + r["tab"] for r in rows if r["hmin"] is None or not r["sys"] and r["system"] not in ("–", "")]
print("Ohne H oder ohne erkanntes System:", probl)
print("Ohne D:", [r["name"] for r in rows if r["dmin"] is None])
