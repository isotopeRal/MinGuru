"""Baut die App neu: liest die Transkription, erzeugt Daten und CSV und schreibt ../index.html.

Aufruf aus dem Repository-Wurzelverzeichnis:  python3 quellen/build.py
"""
import os, runpy, shutil

hier = os.path.dirname(os.path.abspath(__file__))
os.chdir(hier)                      # parse.py arbeitet mit Pfaden relativ zu diesem Ordner
runpy.run_path("parse.py")          # erzeugt data.json und die CSV im Ordner quellen/

with open("template.html", encoding="utf-8") as f:
    vorlage = f.read()
with open("data.json", encoding="utf-8") as f:
    daten = f.read()

# Daten in die Seite einsetzen; "</" maskieren, damit kein "</script>" im JSON das Skript beendet
seite = vorlage.replace("__DATA__", daten.replace("</", "<\\/"))
with open(os.path.join("..", "index.html"), "w", encoding="utf-8") as f:
    f.write(seite)

shutil.move("Mineralbestimmungstabellen_TU_Berlin.csv",
            os.path.join("..", "daten", "Mineralbestimmungstabellen_TU_Berlin.csv"))
os.remove("data.json")
print("index.html und daten/ aktualisiert.")
