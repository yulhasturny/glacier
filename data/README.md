# Data

All data comes from **GLAMOS** (Glacier Monitoring Switzerland), https://doi.glamos.ch. Cite the source "GLAMOS" in the prototype (footer or info panel).

**Glacier:** Rhonegletscher, glacier ID `B43-03`. Area 13.577 km² (survey year 2023, from `glacier_list.csv`).

## Files

Each GLAMOS file contains all Swiss glaciers. `prepare_data.py` downloads them and writes, for each file, a complete copy (`*_all.csv`) and a copy filtered to `B43-03` (`*_rhone.csv`).

> **Format of all CSV files:** the first lines are a preamble (license, citation, title). Then comes the **column-name line**, then a line with **short names** and a line with **units**. The data rows start after that. A loader must skip the preamble and the two lines below the column names (in `lengthchange` and `massbalance_fixdate`: 9 lines before the first data row; in `volumechange`: 8 lines). Some columns are empty in many rows.

### `lengthchange_rhone.csv`: length change of the glacier tongue

Columns: `glacier name`, `glacier id`, `start date of observation`, `quality of start date`, `end date of observation`, `quality of end date`, `length change` (short name `dL`, **unit m**), `elevation of glacier tongue` (m asl.), `observer`.

- One row per **observation period** (start date to end date, ISO dates `yyyy-mm-dd`). The periods start in 1879. Early periods run from 1 September to 1 September, later periods have irregular dates in summer (for example 2023-08-20 to 2024-08-23).
- `length change` is the **change during that period** (negative = retreat), **not** the cumulative length. Cumulative change since a start year is the sum of the values.
- The last row (as of release 2025) ends on **2024-08-23** (-115.10 m). There is no value for 2025 or 2026.

### `massbalance_fixdate_rhone.csv`: mass balance per hydrological year

Columns: `glacier name`, `glacier id`, `start date of observation`, `end date of winter observation`, `end date of observation`, `winter mass balance` (`Bw`, **mm w.e.**), `summer mass balance` (`Bs`, mm w.e.), `annual mass balance` (`Ba`, mm w.e.), `equilibrium line altitude` (`ELA`, m asl.), `accumulation area ratio` (`AAR`, %), `glacier area` (`area`, **km²**), `minimum elevation of glacier` (m asl.), `maximum elevation of glacier` (m asl.), `observer`.

- One row per **hydrological year** (1 October to 30 September), for example `2024-10-01` to `2025-09-30`.
- "mm w.e." means millimetres of water equivalent.
- The last row (as of release 2025) is the hydrological year **2024/25**, ending 2025-09-30 (annual mass balance -1410 mm w.e., glacier area 13.29875 km²).
- The column `glacier area` gives an area for every year (it changes when the glacier outline is updated). It can drive the size of the glacier body.

### `volumechange_rhone.csv`: geodetic volume change

Columns: `SGI-ID`, `source_start`, `source_end`, `date_start`, `date_end` (format `yyyymmdd`, unknown parts are written as `9999`), `A_start` (km²), `outline_start` (year), `A_end` (km²), `outline_end` (year), `dV` (km³), `dh_mean` (m), `Bgeod` (m w.e. per year), `sigma`, `covered` (%), `rho_dv` (kg m⁻³), `Name`.

- One row per period and per source combination, so the same period can appear several times with different values. Example: 2010 to 2023, `dV` = -0.278963 km³, `dh_mean` = -18.842 m, area 14.7762 km² (outline 2010) to 13.5779 km² (outline 2023).
- This file has only a few periods. It is optional for the prototype (for example for a "volume change since 2010" value).

### `glacier_list_rhone.csv`: glacier list

Columns: `glacier name`, `glacier id`, `coordx`, `coordy` (Swiss coordinates), `glacier area` (km²), `survey year for glacier area`, and three columns (`length change`, `mass balance`, `volume change`) with `1` if data exists. For the Rhonegletscher: area 13.577, survey year 2023, all three data sets available.

## Years and the time slider

| Data | Unit | Last period/year in the data |
|------|------|------------------------------|
| Length change | m | period ending 2024-08-23 |
| Mass balance, glacier area | mm w.e., km² | hydrological year 2024/25 (ends 2025-09-30) |

- The wireframe shows a slider from 2010 to 2026. **With these data use 2010 to 2025.** There are no values for 2026.
- Assign data to a slider year `Y` like this: mass balance and area from the row whose `end date of observation` is in year `Y`; length change from the period whose `end date of observation` is in year `Y`. For a year without a value show "no data" instead of a number.

## Optional

Glacier inventory shapefiles for drawing the real glacier outline, for example https://doi.glamos.ch/data/inventory/inventory_sgi2016_r2020.zip (outline 2016) and https://doi.glamos.ch/data/inventory/inventory_sgi2010_r2010.zip (outline 2010). They need a conversion to GeoJSON; skip this for a first version.

## How to prepare

Run in the project folder (open the terminal from GitHub Desktop: Repository → Open in Terminal):

```bash
python3 prepare_data.py
```

## Rules

- Use only these data. Do not invent values.
- Show the units as given: m, mm w.e., km².
- Check the first and last year before labelling anything.
