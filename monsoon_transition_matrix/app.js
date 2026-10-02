/**
 * Monsoon Shift Transition Matrix Dashboard Controller
 * Handles dynamic rendering of interactive Sankey diagrams, pressure drop matrix profiles,
 * streamline wind vector compass charts, multi-station switching, and dataset tab filtering.
 */

let transitionData = null;
let currentTab = 'all';
let currentStation = 'hulhule';

// Theme Colors
const COLOR_IRUVAI = '#F59E0B';
const COLOR_HULHANGU = '#06B6D4';
const COLOR_ASSIDHA = '#EF4444';
const COLOR_HALHA = '#10B981';
const COLOR_RAIN = '#38BDF8';
const COLOR_BG = '#0B0F19';
const COLOR_CARD = '#111827';
const COLOR_TEXT = '#F9FAFB';
const COLOR_MUTED = '#9CA3AF';

document.addEventListener('DOMContentLoaded', () => {
  fetchData();
});

async function fetchData() {
  try {
    const res = await fetch('monsoon_transition_data.json');
    if (!res.ok) throw new Error(`HTTP ${res.status} — ${res.statusText}`);
    let text = await res.text();
    text = text.replace(/:\s*NaN\b/g, ': null');
    transitionData = JSON.parse(text);
    renderDashboard();
  } catch (err) {
    console.error('Failed to load transition data:', err);
    const banner = document.getElementById('error-banner');
    const msg = document.getElementById('error-msg');
    if (banner && msg) {
      msg.textContent = err.message;
      banner.style.display = 'block';
    }
  }
}

function getActiveData() {
  if (transitionData && transitionData.stations && transitionData.stations[currentStation]) {
    return transitionData.stations[currentStation];
  }
  return transitionData;
}

function switchTab(tabKey) {
  currentTab = tabKey;
  
  // Update button active state
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  const targetBtn = document.getElementById(`tab-${tabKey}`);
  if (targetBtn) targetBtn.classList.add('active');

  renderDashboard();
}

function onStationChange() {
  const select = document.getElementById('station-select');
  if (select) {
    currentStation = select.value;
  }
  renderDashboard();
}

function renderDashboard() {
  if (!transitionData) return;

  renderKeyStats();
  renderSankeyChart();
  renderPressureProfileChart();
  renderCompassChart();
  renderTable();
}

function renderKeyStats() {
  const activeData = getActiveData();
  const stats = activeData.key_stats;
  if (!stats) return;

  const assidhaDropEl = document.getElementById('stat-assidha-press');
  const halhaShiftEl = document.getElementById('stat-halha-shift');
  const peakRainEl = document.getElementById('stat-peak-rain');
  const hulhanguShiftEl = document.getElementById('stat-hulhangu-shift');

  if (assidhaDropEl) assidhaDropEl.textContent = `-${stats.assidha_pressure_drop_from_iruvai} hPa`;
  if (halhaShiftEl) halhaShiftEl.textContent = `${stats.iruvai_easterly_shift_pct}%`;
  if (peakRainEl) peakRainEl.textContent = `${stats.halha_mula_rain_p90_mm} mm/d`;
  if (hulhanguShiftEl) hulhanguShiftEl.textContent = `${stats.hulhangu_westerly_shift_pct}%`;
}

// ------------------------------------------------------------------
// 1. Interactive Sankey Ribbon Diagram
// ------------------------------------------------------------------
function renderSankeyChart() {
  const activeData = getActiveData();
  const isAssidha = currentTab === 'assidha';
  const isHalha = currentTab === 'halha';
  
  let sankeyLinks = activeData.sankey_t1 || [];
  let title = `Assidha Transition Sankey Flow (Iruvai -> Hulhangu Wind Reversal)`;
  
  if (isHalha) {
    sankeyLinks = activeData.sankey_t2 || [];
    title = `Halha Transition Sankey Flow (Hulhangu -> Iruvai Easterly Rebound)`;
  } else if (currentTab === 'all') {
    sankeyLinks = [...(activeData.sankey_t1 || []), ...(activeData.sankey_t2 || [])];
    title = `Annual Monsoon Wind Direction Sankey Ribbon Flow`;
  }

  const titleEl = document.getElementById('sankey-title');
  if (titleEl) {
    const stationSuffix = activeData.station_name ? ` — ${activeData.station_name}` : '';
    titleEl.textContent = `${title}${stationSuffix}`;
  }

  // Build unique node list
  const nodeMap = new Map();
  sankeyLinks.forEach(link => {
    if (!nodeMap.has(link.source)) nodeMap.set(link.source, nodeMap.size);
    if (!nodeMap.has(link.target)) nodeMap.set(link.target, nodeMap.size);
  });

  const nodeLabels = Array.from(nodeMap.keys());
  const nodeColors = nodeLabels.map(label => {
    if (label.includes('Iruvai')) return COLOR_IRUVAI;
    if (label.includes('Hulhangu')) return COLOR_HULHANGU;
    if (label.includes('Assidha')) return COLOR_ASSIDHA;
    if (label.includes('Halha')) return COLOR_HALHA;
    if (label.includes('NE') || label.includes('E')) return COLOR_IRUVAI;
    if (label.includes('SW') || label.includes('W') || label.includes('NW')) return COLOR_HULHANGU;
    return '#A855F7';
  });

  const sources = sankeyLinks.map(l => nodeMap.get(l.source));
  const targets = sankeyLinks.map(l => nodeMap.get(l.target));
  const values = sankeyLinks.map(l => l.value);
  const linkColors = sankeyLinks.map(l => {
    if (l.target.includes('SW') || l.target.includes('W') || l.target.includes('NW')) return 'rgba(6, 182, 212, 0.45)';
    if (l.target.includes('NE') || l.target.includes('E')) return 'rgba(245, 158, 11, 0.45)';
    return 'rgba(168, 85, 247, 0.35)';
  });

  const data = [{
    type: "sankey",
    orientation: "h",
    node: {
      pad: 18,
      thickness: 24,
      line: { color: COLOR_CARD, width: 1 },
      label: nodeLabels,
      color: nodeColors
    },
    link: {
      source: sources,
      target: targets,
      value: values,
      color: linkColors
    }
  }];

  const layout = {
    font: { family: 'Inter, sans-serif', color: COLOR_TEXT, size: 12 },
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    margin: { l: 20, r: 20, t: 20, b: 20 }
  };

  Plotly.newPlot('sankey-chart', data, layout, { responsive: true, displayModeBar: false });
}

// ------------------------------------------------------------------
// 2. Atmospheric Pressure Drop & Rainfall Profile Chart
// ------------------------------------------------------------------
function renderPressureProfileChart() {
  const activeData = getActiveData();
  let summary = activeData.nakaiy_summary || [];

  if (currentTab === 'assidha') {
    summary = activeData.transition_1_assidha || [];
  } else if (currentTab === 'halha') {
    summary = activeData.transition_2_halha || [];
  }

  const xNames = summary.map(s => `${s.index}. ${s.name}`);
  const pressures = summary.map(s => s.mean_pressure_hpa);
  const rainP90 = summary.map(s => s.p90_rain_mm);
  const rainMean = summary.map(s => s.mean_rain_mm);

  const tracePressure = {
    x: xNames,
    y: pressures,
    name: 'Mean Pressure (hPa)',
    type: 'scatter',
    mode: 'lines+markers',
    line: { color: COLOR_IRUVAI, width: 3, shape: 'spline' },
    marker: { size: 8, color: COLOR_IRUVAI },
    yaxis: 'y'
  };

  const traceRainP90 = {
    x: xNames,
    y: rainP90,
    name: '90th Percentile Rain (mm)',
    type: 'bar',
    marker: { color: 'rgba(56, 189, 248, 0.65)' },
    yaxis: 'y2'
  };

  const traceRainMean = {
    x: xNames,
    y: rainMean,
    name: 'Mean Rain (mm)',
    type: 'bar',
    marker: { color: 'rgba(2, 132, 199, 0.85)' },
    yaxis: 'y2'
  };

  const data = [traceRainP90, traceRainMean, tracePressure];

  const layout = {
    font: { family: 'Inter, sans-serif', color: COLOR_TEXT },
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    legend: { orientation: 'h', y: 1.12, x: 0 },
    margin: { l: 60, r: 60, t: 40, b: 80 },
    xaxis: {
      tickangle: -45,
      gridcolor: '#1F2937'
    },
    yaxis: {
      title: 'Atmospheric Pressure (hPa)',
      titlefont: { color: COLOR_IRUVAI },
      tickfont: { color: COLOR_IRUVAI },
      gridcolor: '#1F2937'
    },
    yaxis2: {
      title: 'Daily Rainfall (mm)',
      titlefont: { color: COLOR_RAIN },
      tickfont: { color: COLOR_RAIN },
      overlaying: 'y',
      side: 'right'
    }
  };

  Plotly.newPlot('pressure-chart', data, layout, { responsive: true, displayModeBar: false });
}

// ------------------------------------------------------------------
// 3. Radial Wind Streamline Vector Compass Map (Tab-filtered)
// ------------------------------------------------------------------
function renderCompassChart() {
  const activeData = getActiveData();
  let summary = activeData.nakaiy_summary || [];

  if (currentTab === 'assidha') {
    summary = activeData.transition_1_assidha || [];
  } else if (currentTab === 'halha') {
    summary = activeData.transition_2_halha || [];
  }

  const rValues = summary.map(s => s.mean_wind_speed_kts);
  const secAngles = {'N': 0, 'NE': 45, 'E': 90, 'SE': 135, 'S': 180, 'SW': 225, 'W': 270, 'NW': 315};
  const thetaValues = summary.map(s => secAngles[s.dominant_sector] || 0);
  const textLabels = summary.map(s => `${s.name} (${s.dominant_sector})`);
  const colors = summary.map(s => {
    if (s.name === 'Assidha' || s.name === 'Burunu') return COLOR_ASSIDHA;
    if (s.name === 'Mula' || s.name === 'Furahalha') return COLOR_HALHA;
    return s.monsoon === 'Iruvai' ? COLOR_IRUVAI : COLOR_HULHANGU;
  });

  const maxSpd = Math.max(...rValues, 12);

  const data = [{
    type: 'scatterpolar',
    mode: 'markers+text',
    r: rValues,
    theta: thetaValues,
    text: textLabels,
    textposition: 'top center',
    marker: {
      size: summary.map(s => Math.max(8, s.p90_rain_mm / 2)),
      color: colors,
      line: { color: '#FFFFFF', width: 1.5 }
    }
  }];

  const layout = {
    font: { family: 'Inter, sans-serif', color: COLOR_TEXT },
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    polar: {
      bgcolor: 'transparent',
      radialaxis: {
        visible: true,
        range: [0, Math.ceil(maxSpd + 2)],
        title: 'Wind Speed (kts)',
        gridcolor: '#1F2937'
      },
      angularaxis: {
        direction: 'clockwise',
        period: 360,
        gridcolor: '#1F2937'
      }
    },
    margin: { l: 40, r: 40, t: 40, b: 40 }
  };

  Plotly.newPlot('compass-chart', data, layout, { responsive: true, displayModeBar: false });
}

// ------------------------------------------------------------------
// 4. Data Table Population (Fixed Pressure Drop)
// ------------------------------------------------------------------
function renderTable() {
  const tbody = document.getElementById('table-body');
  if (!tbody) return;
  tbody.innerHTML = '';

  const activeData = getActiveData();
  let list = activeData.nakaiy_summary || [];
  if (currentTab === 'assidha') list = activeData.transition_1_assidha || [];
  if (currentTab === 'halha') list = activeData.transition_2_halha || [];

  list.forEach(row => {
    const tr = document.createElement('tr');
    if (row.name === 'Assidha' || row.name === 'Burunu') tr.classList.add('highlight-assidha');
    if (row.name === 'Mula' || row.name === 'Furahalha' || row.name === 'Uthurahalha') tr.classList.add('highlight-halha');

    // Format pressure drop nicely
    let dropDisplay = '-';
    if (row.pressure_drop_hpa !== undefined && row.pressure_drop_hpa !== null) {
      const val = Number(row.pressure_drop_hpa);
      dropDisplay = val > 0 ? `+${val.toFixed(2)} hPa` : `${val.toFixed(2)} hPa`;
    }

    tr.innerHTML = `
      <td>${row.index}</td>
      <td><strong>${row.name}</strong></td>
      <td><span class="badge ${row.monsoon.toLowerCase()}">${row.monsoon}</span></td>
      <td>${row.dates}</td>
      <td>${row.mean_pressure_hpa} hPa</td>
      <td><strong>${dropDisplay}</strong></td>
      <td>${row.mean_rain_mm} mm</td>
      <td><strong>${row.p90_rain_mm} mm</strong></td>
      <td>${row.mean_wind_speed_kts} kts</td>
      <td><strong>${row.dominant_sector}</strong> (${row.dominant_sector_pct}%)</td>
      <td><em>${row.lore}</em></td>
    `;
    tbody.appendChild(tr);
  });
}
