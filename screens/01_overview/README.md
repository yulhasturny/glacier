# Screen 01: Overview

![Screen 01](screen.jpg)

Additional state: `state_2026.jpg` (the same screen at the year 2026).

## Description

The start state shows the whole system on a dark background. The **Rhonegletscher** is at the center as a glowing cyan body. Four thin concentric orbit rings surround it. On the rings sit the elements that depend on the glacier, each shown as a small colored dot with a label and a level text:

- **Rhone river** on ring 1 (LEVEL 1 · DIRECT), blue
- **Forest** on ring 2 (LEVEL 2), green
- **Animals** on ring 3 (LEVEL 3), amber
- **Lake Geneva** on ring 4 (LEVEL 4 · DISTANT), blue

Next to the glacier body are the label "RHONEGLETSCHER" and the glacier ID "B43-03". Each ring has a small tag (L1 to L4) on its right side.

Interface elements (see main README): title top left, zoom indicator and RESET VIEW top right, LAYERS panel on the left, timeline bar at the bottom with the YEAR readout (2010 in this state), PLAY button and slider with the handle at the first year.

**State 2026:** identical layout. The year readout shows 2026, the slider handle is at the end, and the glacier body is smaller.

## Trigger

- Page load.
- The user drags the time slider, presses PLAY, or clicks on the slider track.
- The user toggles a layer in the LAYERS panel.
- The user zooms or pans (scroll, pinch, drag).
- The user hovers over an element or the glacier.
- The user clicks the glacier (leads to screen 02) or another element (leads to screen 03).

## Response

- On page load the whole system is shown centered, with the slider at the first year (2010).
- Moving the slider updates the year readout and the glacier body. The size of the glacier body is derived from the data of the selected year (see Data).
- PLAY advances the year step by step and stops at the last year. The button then returns to PLAY.
- Unchecking a layer hides that element and its label. Checking it shows it again.
- Hovering over an element highlights it (brighter halo, brighter label) and shows a pointer cursor to signal that it is clickable.
- Clicking the glacier zooms smoothly to screen 02. Clicking another element zooms smoothly to screen 03.
- RESET VIEW returns to this state.

## Data

- `massbalance_fixdate_rhone.csv`: column `glacier area` (km²) for each hydrological year. Use it for the size of the glacier body.
- `lengthchange_rhone.csv` and `massbalance_fixdate_rhone.csv` for the values shown on screen 02. See `data/README.md` for all columns and units.
- **Slider range:** the wireframe shows 2010 to 2026, but the data ends earlier (mass balance and area: hydrological year ending 2025-09-30; length change: period ending 2024-08-23). Use **2010 to 2025** as the slider range. For a year without a value show "no data" instead of a number.

## Remarks

- Only the glacier changes with the data. The other elements stay in place; they only change if there is data in `data/` to support it.
- In the wireframe the glacier radius is 26 px (2010) and 18 px (2026). These are placeholders. Proposal for the real size: compute it from `glacier area` (km²) of the selected year so that the drawn **area** is proportional to the glacier area (radius proportional to the square root of the area). [DECIDE]
- The wireframe labels the last year "2026". With the current data the last year is 2025; adapt the slider labels to the data.
- If a year has no value, do not silently invent one; show the nearest available value and mark it, or skip that year.
- The orange annotations in the wireframe are team notes and are not part of the interface.
