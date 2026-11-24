"""Download GLAMOS files and keep only the rows of the Rhonegletscher (ID B43-03).

Run from the project folder:  python3 prepare_data.py
Needs only the Python standard library. Requires internet access.

Each output file keeps the full preamble of the original file (license text,
title, column names and units) followed by the rows of the Rhonegletscher.
"""
import os
import re
import urllib.request

GLACIER_ID = "B43-03"

FILES = {
    "glacier_list": "https://doi.glamos.ch/data/glacier_list/glacier_list.csv",
    "lengthchange": "https://doi.glamos.ch/data/lengthchange/lengthchange.csv",
    "massbalance_fixdate": "https://doi.glamos.ch/data/massbalance/massbalance_fixdate.csv",
    "volumechange": "https://doi.glamos.ch/data/volumechange/volumechange.csv",
}

OUT_DIR = "data"

# A data row has a glacier ID like "A10g-05" or "B43-03" in its first or second field.
ID_PATTERN = re.compile(r"^(?:[^,]*,)?[A-Z]\d{2}[a-z]?-\d{2},")


def download(url):
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def filter_lines(text):
    """Keep every line before the first data row (preamble, column names, units),
    then only the data rows of the Rhonegletscher."""
    kept = []
    in_data = False
    for line in text.splitlines():
        if not in_data and ID_PATTERN.match(line):
            in_data = True
        if not in_data:
            kept.append(line)
        elif line.startswith(GLACIER_ID + ",") or ("," + GLACIER_ID + ",") in line[:40]:
            kept.append(line)
    return kept


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, url in FILES.items():
        print(f"Downloading {name} ...")
        text = download(url)
        with open(os.path.join(OUT_DIR, f"{name}_all.csv"), "w", encoding="utf-8") as f:
            f.write(text)
        kept = filter_lines(text)
        out_path = os.path.join(OUT_DIR, f"{name}_rhone.csv")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(kept) + "\n")
        print(f"  {len(kept)} lines -> {out_path}")
    print("Done. Check the *_rhone.csv files (column names, units, years).")


if __name__ == "__main__":
    main()
