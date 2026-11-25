const YEAR_MIN = 2010;
const YEAR_MAX = 2025;
const GLACIER_RADIUS_2010 = 26;
const ELEMENT_RADIUS = 7;
const RING_RADII = [108, 176, 248, 324];

const ELEMENT_LAYOUT = {
  rhone: { angle: 188 },
  forest: { angle: 148 },
  animals: { angle: 52 },
  lake: { angle: -28 },
};

const state = {
  year: YEAR_MIN,
  playing: false,
  playTimer: null,
  areaByYear: new Map(),
  area2010: null,
  elements: [],
  visible: {},
};

function parseGlamosCsv(text) {
  const lines = text.split(/\r?\n/).filter((line) => line.length > 0);
  const headerIndex = lines.findIndex((line) => line.startsWith("glacier name,"));
  if (headerIndex < 0) return [];
  const headers = lines[headerIndex].split(",");
  const rows = [];
  for (let i = headerIndex + 3; i < lines.length; i += 1) {
    const cols = lines[i].split(",");
    if (cols.length < 3) continue;
    const row = {};
    headers.forEach((header, index) => {
      row[header] = cols[index];
    });
    rows.push(row);
  }
  return rows;
}

function yearFromIsoDate(value) {
  if (!value) return null;
  const year = Number(String(value).slice(0, 4));
  return Number.isFinite(year) ? year : null;
}

function polar(cx, cy, radius, angleDeg) {
  const rad = (angleDeg * Math.PI) / 180;
  return {
    x: cx + radius * Math.cos(rad),
    y: cy - radius * Math.sin(rad),
  };
}

function glacierRadius(area) {
  const baseArea = state.area2010;
  if (!area || !baseArea) return GLACIER_RADIUS_2010;
  return GLACIER_RADIUS_2010 * Math.sqrt(area / baseArea);
}

function addGlow(selection, radius, color) {
  selection
    .append("circle")
    .attr("class", "halo-outer")
    .attr("r", radius * 2.35)
    .attr("fill", color)
    .attr("opacity", 0.08);
  selection
    .append("circle")
    .attr("class", "halo-inner")
    .attr("r", radius * 1.55)
    .attr("fill", color)
    .attr("opacity", 0.2);
  selection
    .append("circle")
    .attr("class", "core")
    .attr("r", radius)
    .attr("fill", color);
}

function stageSize() {
  const svg = document.getElementById("stage");
  return { width: svg.clientWidth, height: svg.clientHeight };
}

function drawSystem() {
  const svg = d3.select("#stage");
  svg.selectAll("*").remove();

  const { width, height } = stageSize();
  const cx = width * 0.54;
  const cy = height * 0.46;

  const system = svg.append("g").attr("class", "system");

  RING_RADII.forEach((radius, index) => {
    system
      .append("circle")
      .attr("class", "orbit-ring")
      .attr("cx", cx)
      .attr("cy", cy)
      .attr("r", radius);

    const tagAngle = index === 0 ? -12 : -2;
    const tag = polar(cx, cy, radius + 8, tagAngle);
    system
      .append("text")
      .attr("class", "ring-tag")
      .attr("x", tag.x)
      .attr("y", tag.y)
      .attr("text-anchor", "start")
      .text(`L${index + 1}`);
  });

  const glacier = system.append("g").attr("class", "glacier").attr("transform", `translate(${cx},${cy})`);
  const area = state.areaByYear.get(state.year);
  const radius = glacierRadius(area);
  addGlow(glacier, radius, "#66D9FF");
  glacier
    .append("text")
    .attr("class", "glacier-label")
    .attr("x", radius + 16)
    .attr("y", 2)
    .text("RHONEGLETSCHER");
  glacier
    .append("text")
    .attr("class", "glacier-id")
    .attr("x", radius + 16)
    .attr("y", 16)
    .text("B43-03");

  state.elements.forEach((element) => {
    const layout = ELEMENT_LAYOUT[element.id];
    if (!layout) return;
    const ringRadius = RING_RADII[element.level - 1];
    const pos = polar(cx, cy, ringRadius, layout.angle);
    const group = system
      .append("g")
      .attr("class", "element")
      .attr("data-id", element.id)
      .attr("transform", `translate(${pos.x},${pos.y})`)
      .style("display", state.visible[element.id] === false ? "none" : null);

    addGlow(group, ELEMENT_RADIUS, element.color);
    group
      .append("text")
      .attr("class", "element-label")
      .attr("x", 16)
      .attr("y", 3)
      .text(element.title.toUpperCase());
    group
      .append("text")
      .attr("class", "level-label")
      .attr("x", 16)
      .attr("y", 16)
      .text(element.levelLabel);
  });
}

function setYear(year) {
  const next = Math.min(YEAR_MAX, Math.max(YEAR_MIN, year));
  state.year = next;
  document.getElementById("year-value").textContent = String(next);
  document.getElementById("year-slider").value = String(next);
  drawSystem();
}

function stopPlayback() {
  state.playing = false;
  if (state.playTimer) {
    window.clearInterval(state.playTimer);
    state.playTimer = null;
  }
  document.getElementById("play-button").textContent = "PLAY";
  document.getElementById("play-button").classList.remove("is-playing");
}

function startPlayback() {
  if (state.year >= YEAR_MAX) setYear(YEAR_MIN);
  state.playing = true;
  document.getElementById("play-button").textContent = "PAUSE";
  document.getElementById("play-button").classList.add("is-playing");
  state.playTimer = window.setInterval(() => {
    if (state.year >= YEAR_MAX) {
      stopPlayback();
      return;
    }
    setYear(state.year + 1);
  }, 650);
}

function renderLayerControls() {
  const form = d3.select("#layers-form");
  form.selectAll("*").remove();
  state.elements.forEach((element) => {
    const row = form.append("label").attr("class", "layer-row");
    row
      .append("span")
      .attr("class", "layer-swatch")
      .style("background", element.color)
      .style("color", element.color);
    row.append("span").attr("class", "layer-name").text(element.title.toUpperCase());
    row
      .append("input")
      .attr("type", "checkbox")
      .property("checked", true)
      .attr("data-id", element.id)
      .on("change", (event) => {
        state.visible[element.id] = event.target.checked;
        drawSystem();
      });
  });
}

function renderSliderTicks() {
  const ticks = document.getElementById("slider-ticks");
  ticks.innerHTML = "";
  const labeled = new Set([YEAR_MIN, 2015, 2020, YEAR_MAX]);
  for (let year = YEAR_MIN; year <= YEAR_MAX; year += 1) {
    const pct = ((year - YEAR_MIN) / (YEAR_MAX - YEAR_MIN)) * 100;
    const tick = document.createElement("div");
    tick.className = "tick";
    tick.style.left = `${pct}%`;
    if (labeled.has(year)) {
      const label = document.createElement("span");
      label.textContent = String(year);
      tick.appendChild(label);
    }
    ticks.appendChild(tick);
  }
}

function fitApp() {
  const scale = Math.min(window.innerWidth / 1440, window.innerHeight / 900, 1);
  const app = document.getElementById("app");
  app.style.transform = `scale(${scale})`;
  document.body.style.height = `${900 * scale}px`;
}

function bindControls() {
  const slider = document.getElementById("year-slider");
  slider.min = String(YEAR_MIN);
  slider.max = String(YEAR_MAX);
  slider.addEventListener("input", (event) => {
    stopPlayback();
    setYear(Number(event.target.value));
  });

  document.getElementById("play-button").addEventListener("click", () => {
    if (state.playing) stopPlayback();
    else startPlayback();
  });

  document.getElementById("reset-view").addEventListener("click", () => {
    stopPlayback();
    Object.keys(state.visible).forEach((id) => {
      state.visible[id] = true;
    });
    document.querySelectorAll("#layers-form input").forEach((input) => {
      input.checked = true;
    });
    setYear(YEAR_MIN);
  });

  window.addEventListener("resize", () => {
    fitApp();
    drawSystem();
  });
}

async function loadData() {
  const [massText, elements] = await Promise.all([
    d3.text("data/massbalance_fixdate_rhone.csv"),
    d3.json("data/elements.json"),
  ]);
  const massRows = parseGlamosCsv(massText);
  massRows.forEach((row) => {
    const year = yearFromIsoDate(row["end date of observation"]);
    const area = Number(row["glacier area"]);
    if (year && Number.isFinite(area)) state.areaByYear.set(year, area);
  });
  state.area2010 = state.areaByYear.get(YEAR_MIN) ?? null;
  state.elements = elements;
  elements.forEach((element) => {
    state.visible[element.id] = true;
  });
}

async function init() {
  await loadData();
  renderLayerControls();
  renderSliderTicks();
  bindControls();
  fitApp();
  setYear(YEAR_MIN);
}

init().catch((error) => {
  console.error(error);
});
