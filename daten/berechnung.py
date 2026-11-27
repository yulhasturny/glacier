"""Eisverlust von Schweizer Gletschern als Würfel.

Liest die GLAMOS-Datei massbalance_observation.csv (im gleichen Ordner)
und rechnet für die fünf grössten Gletscher dieser Datei, für jedes Messjahr:

1. Massenbilanz (mm w.e. / 1000 = m w.e.) × Gletscherfläche (km² × 1 000 000 = m²)
   = Wasservolumen in m³
2. Wasservolumen × 1000 / 900 = Eisvolumen in m³ (Eis wiegt 900 kg/m³)
3. Dritte Wurzel aus dem Eisvolumen = Kantenlänge des Würfels in m

Ergebnisse (im gleichen Ordner):
- rhone_eisvolumen.csv      nur der Rhonegletscher (wie bisher)
- gletscher_eisvolumen.csv  alle fünf Gletscher, mit einer Spalte für den Gletscher
Positives Volumen = Verlust, negatives Volumen = Zuwachs.

Quelle: GLAMOS (2026). Swiss Glacier Mass Balance, release 2026,
Glacier Monitoring Switzerland, doi:10.18750/massbalance.2026.r2026.

Starten im Terminal:  python3 daten/berechnung.py
"""

import csv
from pathlib import Path

ORDNER = Path(__file__).parent
EINGABE = ORDNER / "massbalance_observation.csv"

# die fünf grössten Gletscher in der Datei (nach heutiger Fläche)
GLETSCHER = {
    "B36-26": "Grosser Aletschgletscher",
    "B83-03": "Glacier de Corbassière",
    "B43-03": "Rhonegletscher",
    "B56-03": "Findelgletscher",
    "B82-27": "Glacier d'Otemma",
}
DICHTE_WASSER = 1000      # kg/m³
DICHTE_EIS = 900          # kg/m³


def rechne(teile):
    beginn, ende = teile[2], teile[4]
    massenbilanz_mm = float(teile[7])
    flaeche_km2 = float(teile[10])
    wasser_m3 = -(massenbilanz_mm / 1000) * (flaeche_km2 * 1_000_000)
    eis_m3 = wasser_m3 * DICHTE_WASSER / DICHTE_EIS
    kante_m = abs(eis_m3) ** (1 / 3)
    return {
        "jahr": int(ende[:4]),
        "beginn": beginn,
        "ende": ende,
        "massenbilanz_mm_we": int(massenbilanz_mm),
        "flaeche_km2": flaeche_km2,
        "wasservolumen_m3": round(wasser_m3),
        "eisvolumen_m3": round(eis_m3),
        "kantenlaenge_m": round(kante_m, 1),
        "zuwachs": "ja" if eis_m3 < 0 else "nein",
    }


alle = []
with open(EINGABE, encoding="utf-8") as f:
    for teile in csv.reader(f):
        # Kopfzeilen und andere Gletscher überspringen
        if len(teile) < 11 or teile[1].strip() not in GLETSCHER:
            continue
        gid = teile[1].strip()
        alle.append({"gletscher": GLETSCHER[gid], "gletscher_id": gid, **rechne(teile)})


def speichere(datei, zeilen, felder):
    with open(ORDNER / datei, "w", encoding="utf-8", newline="") as f:
        schreiber = csv.DictWriter(f, fieldnames=felder)
        schreiber.writeheader()
        schreiber.writerows(zeilen)


felder = list(alle[0].keys())
speichere("gletscher_eisvolumen.csv", alle, felder)
rhone = [{k: v for k, v in z.items() if k not in ("gletscher", "gletscher_id")} for z in alle if z["gletscher_id"] == "B43-03"]
speichere("rhone_eisvolumen.csv", rhone, felder[2:])

for gid, name in GLETSCHER.items():
    zeilen = [z for z in alle if z["gletscher_id"] == gid]
    groesster = max(zeilen, key=lambda z: z["eisvolumen_m3"])
    print(f"{name}: {len(zeilen)} Messjahre ({zeilen[0]['jahr']}–{zeilen[-1]['jahr']}), "
          f"grösster Verlust {groesster['jahr']}: {groesster['eisvolumen_m3'] / 1e6:.1f} Mio. m³ Eis, "
          f"Würfel mit {groesster['kantenlaenge_m']:.0f} m Kante")
print("Gespeichert: gletscher_eisvolumen.csv und rhone_eisvolumen.csv")
