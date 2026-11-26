"""Eisverlust des Rhonegletschers als Würfel.

Liest die GLAMOS-Datei massbalance_observation.csv (im gleichen Ordner),
nimmt nur den Rhonegletscher (B43-03) und rechnet für jedes Messjahr:

1. Massenbilanz (mm w.e. / 1000 = m w.e.) × Gletscherfläche (km² × 1 000 000 = m²)
   = Wasservolumen in m³
2. Wasservolumen × 1000 / 900 = Eisvolumen in m³ (Eis wiegt 900 kg/m³)
3. Dritte Wurzel aus dem Eisvolumen = Kantenlänge des Würfels in m

Ergebnis: rhone_eisvolumen.csv (im gleichen Ordner).
Positives Volumen = Verlust, negatives Volumen = Zuwachs.

Quelle: GLAMOS (2026). Swiss Glacier Mass Balance, release 2026,
Glacier Monitoring Switzerland, doi:10.18750/massbalance.2026.r2026.

Starten im Terminal:  python3 daten/berechnung.py
"""

import csv
from pathlib import Path

ORDNER = Path(__file__).parent
EINGABE = ORDNER / "massbalance_observation.csv"
AUSGABE = ORDNER / "rhone_eisvolumen.csv"

GLETSCHER_ID = "B43-03"   # Rhonegletscher
DICHTE_WASSER = 1000      # kg/m³
DICHTE_EIS = 900          # kg/m³

zeilen = []
with open(EINGABE, encoding="utf-8") as f:
    for teile in csv.reader(f):
        # Kopfzeilen und andere Gletscher überspringen
        if len(teile) < 11 or teile[1].strip() != GLETSCHER_ID:
            continue
        beginn, ende = teile[2], teile[4]
        massenbilanz_mm = float(teile[7])
        flaeche_km2 = float(teile[10])

        wasser_m3 = -(massenbilanz_mm / 1000) * (flaeche_km2 * 1_000_000)
        eis_m3 = wasser_m3 * DICHTE_WASSER / DICHTE_EIS
        kante_m = abs(eis_m3) ** (1 / 3)

        zeilen.append({
            "jahr": int(ende[:4]),
            "beginn": beginn,
            "ende": ende,
            "massenbilanz_mm_we": int(massenbilanz_mm),
            "flaeche_km2": flaeche_km2,
            "wasservolumen_m3": round(wasser_m3),
            "eisvolumen_m3": round(eis_m3),
            "kantenlaenge_m": round(kante_m, 1),
            "zuwachs": "ja" if eis_m3 < 0 else "nein",
        })

with open(AUSGABE, "w", encoding="utf-8", newline="") as f:
    schreiber = csv.DictWriter(f, fieldnames=list(zeilen[0].keys()))
    schreiber.writeheader()
    schreiber.writerows(zeilen)

groesster = max(zeilen, key=lambda z: z["eisvolumen_m3"])
zuwachs = [z["jahr"] for z in zeilen if z["zuwachs"] == "ja"]
print(f"{len(zeilen)} Messjahre gespeichert in {AUSGABE.name}")
print(f"Grösster Verlust: {groesster['jahr']}, "
      f"{groesster['eisvolumen_m3'] / 1e6:.1f} Mio. m³ Eis, "
      f"Würfel mit {groesster['kantenlaenge_m']:.0f} m Kante")
print("Jahre mit Zuwachs:", ", ".join(map(str, zuwachs)))
