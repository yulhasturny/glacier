# Prototype Specification: Swiss Glaciers

## General

- **Project:** An interactive, science-style visualization of the **Rhonegletscher** (Rhone Glacier, Switzerland) and everything that depends on it. Inspired by NASA Eyes on the Solar System: the glacier is the "sun" in the center, and the things that depend on the glacier orbit around it on rings like planets. The further out a ring, the less direct and the more distant the dependency. The user starts at the glacier, zooms and pans, moves a time slider (2010 to 2026) and clicks elements to learn about their relationship to the glacier.
- **Guiding question:** What are the direct effects of the disappearing of the Swiss glaciers on their ecosystems and on the surrounding and distant environment?
- **Goals:** Make the consequences of glacier loss visible, raise awareness, and show how far the influence of a single glacier reaches.
- **Technology:** Web prototype using **d3.js** (plain HTML, CSS and JavaScript, no build tools). Use `d3.zoom` for zooming and panning. Must run locally, for example with `python3 -m http.server` in the project folder and opening `http://localhost:8000`.
- **Data:** All data files are in the `data/` folder. Use only this data; do not invent values. Where a statement is qualitative (no number in the data), write it as text, never as a made-up figure. See `data/README.md` for the files and how they are filtered to the Rhonegletscher (ID `B43-03`).
- **Wireframes:** The wireframes are in Figma, file "Data Sketches A1 presentation", section "Wireframes v2: scientific style (Rhonegletscher one-pager)". Exported images are in the screen folders. Frame size 1440 x 900.

## One page, several states

The prototype is a **single page** (one pager). The user can pan and zoom freely. The "screens" in this specification are **snapshots (states) of this one page**, not separate pages:

- `01_overview`: the whole system with the glacier in the center and the elements on the orbit rings (start state, year 2010; a second state shows the year 2026)
- `02_glacier_selected`: the same page, zoomed to the glacier with an info panel
- `03_element_popup`: the same page, zoomed to one element (forest, Rhone river, animals or Lake Geneva) with a pop-up

Moving between the states happens through zooming, panning and clicking, with smooth transitions. The pictures show the key states; everything in between is the continuous zoom and pan.

## Visual style (NASA Eyes inspired, scientific, not illustrative)

- **Background:** very dark blue `#0B0F15`.
- **Panels** (layers, info panel, pop-up, timeline bar): `#121A24` with a thin 1 px border (cyan at about 50 % opacity for info panel and pop-up, grey at about 35 % for the layers panel), small corner radius (6 px).
- **Text:** primary `#E6EDF5`, secondary/muted `#8C9EB3`. Font: Inter (or a similar clean sans-serif). Labels are **uppercase, small (9 to 12 px) with letter spacing**. Headings uppercase, 18 to 20 px.
- **Objects** are simple glowing circles (a core circle plus two translucent halos), no icons or illustrations:
  - Glacier: cyan `#66D9FF`
  - Rhone river and Lake Geneva: blue `#5999FF`
  - Forest: green `#73D18C`
  - Animals: amber `#F2B859`
- **Orbit rings:** thin 1 px circles in muted grey at about 35 % opacity, concentric around the glacier. The ring of a selected element is highlighted in cyan.
- **Annotations** in orange in the wireframes are notes for the team and are **not part of the interface**.

## Elements and orbit rings

| Ring | Level | Element | Color |
|------|-------|---------|-------|
| 1 (innermost) | LEVEL 1 · DIRECT | Rhone river | blue |
| 2 | LEVEL 2 | Forest | green |
| 3 | LEVEL 3 | Animals | amber |
| 4 (outermost) | LEVEL 4 · DISTANT | Lake Geneva | blue |

The glacier is at the center. Each ring has a small tag (L1 to L4) on its right side. More elements (for example hydropower dams, meltwater lakes, agriculture downstream) can be added as further dots on the rings later.

## Common interface elements (on every state)

- **Top left:** title "RHONEGLETSCHER" and subtitle "What depends on this glacier?".
- **Top right:** zoom indicator ("ZOOM ×1", "ZOOM ×4", "ZOOM ×8") and a **RESET VIEW** button.
- **Left:** a **LAYERS** panel with a checkbox for each element (Rhone river, Forest, Animals, Lake Geneva). Unchecking hides the element and its label.
- **Bottom:** a **timeline bar** with the current YEAR in large type, a PLAY button, and a slider with a tick for every year (labels at 2010, 2015, 2020 and the last year). The wireframe shows 2010 to 2026; with the current data the range is **2010 to 2025** (see `data/README.md`).

## How this specification is organized

- Every screen of the prototype has its own folder in `screens/`, numbered in the order a user sees them (`01_overview`, `02_glacier_selected`, `03_element_popup`).
- Each screen folder contains a `README.md` with the description of that screen, plus one or more pictures of the wireframe.
- **All images in a screen folder belong to that screen.** `screen.jpg` is the main picture; additional pictures show other states of the same screen (for example `state_2026.jpg`).

## Open points (to fill in by the team)

- [ ] Wireframe images exported from Figma into the screen folders
- [ ] Data files from GLAMOS in `data/` (see `data/README.md`)
- [ ] Final pop-up texts for each element (`data/elements.json`) with sources
- [ ] Confirm the size of the glacier body: proposal is the glacier area (km²) per year from `massbalance_fixdate`
