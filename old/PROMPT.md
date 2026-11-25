# Prompt for Claude Code / Codex

Copy the text below into your AI coding tool after you have opened the project folder.

---

Read `README.md`, `data/README.md` and all files in `screens/` (every `README.md` and every image in each screen folder). They are the specification for an interactive web prototype. Then look at the files in `data/`.

Build the prototype with **d3.js** in plain HTML, CSS and JavaScript (no build tools). It must run locally with `python3 -m http.server`.

Important:
- This is a **one-pager**. The three screens in `screens/` are snapshots (states) of **one single page** that the user can pan and zoom (`d3.zoom`). Clicking the glacier zooms to screen 02, clicking another element zooms to screen 03. Transitions are smooth.
- The look is **scientific, in the style of NASA Eyes on the Solar System**: dark background, thin orbit rings, simple glowing circles for the elements, uppercase small labels, panels with thin borders. No illustrations or icons. The exact colors, sizes and layout are in `README.md` and in the wireframe images.

Requirements:
1. Follow the specification and the wireframe images closely (layout, colors, labels, positions, panels, timeline bar).
2. Use only the data in `data/` (Rhonegletscher, ID `B43-03`). Do not invent values. If a column name, unit or year range is unclear, look at the CSV first and tell me what you found.
3. Create these files: `index.html`, `style.css`, `main.js`. Load data with `d3.csv` / `d3.json` from `data/`.
4. Work step by step. First build the **overview** (dark page, orbit rings, glacier and elements, layers panel, timeline bar with year readout and slider) and tell me how to run it. Wait for my feedback before continuing with the zoom and the glacier info panel, then the element pop-ups.
5. If something in the specification is unclear or the data does not match, ask me instead of guessing.

---

## Follow-up prompts (use one at a time)

- "Add zoom and pan with `d3.zoom`, the zoom indicator, RESET VIEW, and the transition to the glacier info panel (screen 02)."
- "Connect the time slider and the PLAY button to the GLAMOS data. Show YEAR, MASS BALANCE and LENGTH CHANGE in the info panel and draw the line chart from the real data."
- "Add the layer toggles and the element pop-ups with the dependency line, from `data/elements.json` (screen 03)."
- "Make the zoom transitions smoother and add hover states for the elements."
- "Compare the page with the wireframe images and fix differences in spacing, colors and typography."
