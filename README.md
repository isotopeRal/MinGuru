# MinGuru

Site to determine minerals based on optical appearance and physical properties.

Interaktive Mineralbestimmung nach äußeren Kennzeichen – im Browser, ohne Installation.

**Zur App:** https://isotoperal.github.io/MinGuru/

## Was die App kann

- **Geführt bestimmen:** Schritt für Schritt durch den Bestimmungsschlüssel (Glanz → Strich → Härte → Spaltbarkeit), mit Praxistipps zu Strichtafel und Ritzprobe, Trefferzahlen vor jeder Antwort, „nicht sicher“ für Grenzfälle und Hinweisen auf Nachbartabellen.
- **Feinbestimmung:** Ist die Tabelle erreicht, fragt die App weiter nach Form (mit Symbolbildern), Farbe, Glanzart, Gewicht, genauer Härte und Salzsäuretest – jeweils das Merkmal, das die verbliebenen Kandidaten am besten trennt. Zum Schluss stehen die letzten Kandidaten in einer Vergleichstabelle, die unterscheidenden Merkmale sind markiert; ausgeschiedene Einträge lassen sich mit Begründung nachlesen.
- **Alle Tabellen:** alle 283 Einträge (231 Mineralien) filterbar nach Glanz, Strichfarbe, Mohs-Härte, Spaltbarkeit, Dichte, Glanzart, Kristallsystem und Tabelle, mit Freitextsuche.
- **Kristallmodelle:** zu jedem Mineral ein aus Kristallklasse und typischer Tracht berechnetes Modell der Idealform – klein in der Liste, aufgeklappt groß und drehbar, mit einblendbaren Drehachsen, Spiegelebenen und Symmetriezentrum. Darstellung umschaltbar zwischen Holzmodell und Lehrbuchzeichnung.
- **Silikatstrukturen:** bei Silikaten ein Schema der SiO₄-Tetraeder-Verknüpfung (Insel-, Gruppen-, Ring-, Ketten-, Band-, Schicht-, Gerüstsilikat) mit Vergleich aller sieben Klassen.
- Jeder Mineralname verlinkt auf die passende Seite bei [mindat.org](https://www.mindat.org).
- Funktioniert am Rechner und auf dem Handy, im hellen und dunklen Modus.

## Grundlage

Tennyson, C. (1981): *Tabellen zur Bestimmung der wichtigsten Mineralien nach äußeren Kennzeichen.* Institut für Mineralogie und Kristallographie, Technische Universität Berlin.
Überarbeitet von S. Herting-Agthe & C. Agthe (1998), Institut für Angewandte Geowissenschaften I, Fachgebiet Allgemeine und Angewandte Mineralogie, TU Berlin.

Die Tabellen wurden von Hand aus dem gescannten Original übertragen. Stellen mit Druckfehlern im Original oder ergänzten Werten sind in der App in der Detailansicht markiert.

## Aufbau des Repositorys

| Pfad | Inhalt |
|---|---|
| `index.html` | die fertige App (eine Datei, Daten eingebettet) |
| `daten/Mineralbestimmungstabellen_TU_Berlin.csv` | alle Einträge als CSV (Semikolon, UTF-8) mit Zahlenspalten für Härte und Dichte sowie mindat-Links |
| `quellen/mineral_daten.txt` | die Transkription, Grundlage für alles andere |
| `quellen/mindat_ids.py` | Zuordnung der deutschen Namen zu mindat-Seiten |
| `quellen/template.html` | Seitenvorlage (Gestaltung und Logik); die Formtabelle der Kristallmodelle (`KR`) und die Silikatzuordnung (`SIL_ZU`) stehen im Abschnitt „Kristallmodelle und Silikatstrukturen“ |
| `quellen/merkmale.py` | Merkmalsgruppen für die Feinbestimmung (Farbe, Glanz, Form, Salzsäure), aus den Tabellenangaben abgeleitet und von Hand korrigiert (`KORREKTUR`); die Salzsäurereaktion steht nur bei Calcit, Dolomit und Aragonit in den Tabellen, sonst ist sie nach Lehrbuchwissen ergänzt, Cerussit bleibt ohne Angabe |
| `quellen/parse.py`, `quellen/build.py` | Skripte zum Neubau |

## App neu bauen

Nach Änderungen an der Transkription oder der Vorlage:

```bash
python3 quellen/build.py
```

Das Skript erzeugt `index.html` und die CSV neu. Benötigt wird nur Python 3, keine weiteren Pakete.
