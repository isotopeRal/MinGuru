# MinGuru

Site to determine minerals based on optical appearance and physical properties.

Interaktive Mineralbestimmung nach äußeren Kennzeichen – im Browser, ohne Installation.

**Zur App:** https://isotoperal.github.io/MinGuru/

## Was die App kann

- **Geführt bestimmen:** Schritt für Schritt durch den Bestimmungsschlüssel (Glanz → Strich → Härte → Spaltbarkeit), mit Praxistipps zu Strichtafel und Ritzprobe, Trefferzahlen vor jeder Antwort, „nicht sicher“ für Grenzfälle und Hinweisen auf Nachbartabellen.
- **Alle Tabellen:** alle 283 Einträge (231 Mineralien) filterbar nach Glanz, Strichfarbe, Mohs-Härte, Spaltbarkeit, Dichte, Glanzart, Kristallsystem und Tabelle, mit Freitextsuche.
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
| `quellen/template.html` | Seitenvorlage (Gestaltung und Logik) |
| `quellen/parse.py`, `quellen/build.py` | Skripte zum Neubau |

## App neu bauen

Nach Änderungen an der Transkription oder der Vorlage:

```bash
python3 quellen/build.py
```

Das Skript erzeugt `index.html` und die CSV neu. Benötigt wird nur Python 3, keine weiteren Pakete.
