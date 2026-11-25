# Screen 02: Glacier selected

![Screen 02](screen.jpg)

## Description

The user has selected the glacier. The view is zoomed in (zoom indicator "ZOOM ×8"). The orbit rings are no longer shown. The screen has two main areas:

- **Glacier viewport** (left, about 640 x 460 px): a panel with a faint grid (graticule). It shows the terrain image of the glacier with the glacier outline highlighted in cyan. At the bottom of the viewport are the caption "TERRAIN IMAGE + GLACIER OUTLINE" and a "SCALE BAR".
- **Info panel** (right, about 480 px wide): a panel with a cyan border and a close button (×) at the top right. Content from top to bottom:
  - Heading "RHONEGLETSCHER"
  - Rows (label left in small uppercase muted type, value right): **GLACIER ID** (`B43-03`), **AREA (SURVEY 2023)** (13.577 km²), **YEAR** (selected year), **MASS BALANCE** (value), **LENGTH CHANGE** (value)
  - A small **line chart** with the caption "LENGTH CHANGE 2010–2026 · GLAMOS": axes, one cyan line, labels 2010 and 2026 at the x-axis
  - Source line "SOURCE GLAMOS (doi.glamos.ch)"

The common interface elements (title, layers, RESET VIEW, timeline bar) stay visible. The timeline shows the selected year (2016 in the wireframe).

## Trigger

- The user clicks the glacier on screen 01.
- The user moves the time slider while the glacier is selected.
- The user clicks the × button, clicks outside the panels, presses Esc, or clicks RESET VIEW to leave.

## Response

- The view zooms smoothly into the glacier (`d3.zoom` transition). The orbit rings and the other elements fade out.
- The info panel fades in and shows the values for the selected year.
- Moving the time slider updates YEAR, MASS BALANCE, LENGTH CHANGE, the glacier outline (if data allows) and a marker on the line chart that shows the selected year.
- Leaving the state zooms back to screen 01 and the panel fades out.

## Data

- `glacier_list_rhone.csv`: name `Rhonegletscher`, ID `B43-03`, area 13.577 km² (survey year 2023).
- `massbalance_fixdate_rhone.csv`: **MASS BALANCE** = column `annual mass balance` (unit **mm w.e.**, millimetres water equivalent) of the hydrological year (1 Oct to 30 Sep). The same file has `winter mass balance`, `summer mass balance` and `glacier area` (km²).
- `lengthchange_rhone.csv`: **LENGTH CHANGE** = column `length change` (unit **m**) per observation period (start date to end date). Each value is the change in one period, not a cumulative value.
- All files are filtered to ID `B43-03`. The files start with a preamble; see `data/README.md` for the exact format and all columns.

## Remarks

- The wireframe shows "LENGTH CHANGE" because GLAMOS provides **length changes**, not the absolute length. Do not label it "length".
- The line in the wireframe chart is a placeholder curve. Draw the real chart from `length change` (m). Because each value is the change in one observation period, the line shows the **cumulative sum** since the first slider year (2010); label it "cumulative length change since 2010". Alternative: bars per period. [DECIDE]
- Show the units next to the values: length change in m, mass balance in mm w.e.
- For years without data (length change: after 2024; mass balance: after hydrological year 2024/25) show "no data" instead of a number.
- For the glacier outline use the glacier inventory shapefiles from GLAMOS if available (see `data/README.md`); otherwise show a clearly marked placeholder shape.
- The values `[value]` in the wireframe stand for data values. Never show invented numbers.
