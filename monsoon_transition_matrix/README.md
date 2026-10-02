# 🌀 Monsoon Shift Transition Matrix

A dedicated meteorological analysis and interactive visualization package studying atmospheric pressure drops ($\Delta P$), wind vector streamlines ($U, V$), directional reversals, and extreme rainfall surges during the Maldivian monsoon transitions (**Assidha** and **Halha**).

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-blue?style=for-the-badge&logo=github)](https://ajmals.github.io/met-weather-data-analysis/monsoon_transition_matrix/)
[![Static Visuals](https://img.shields.io/badge/Static%20Artifacts-PNG%20%7C%20PDF-success?style=for-the-badge)](./output/)

> **🌐 Live Interactive Dashboard:**  
> **[https://ajmals.github.io/met-weather-data-analysis/monsoon_transition_matrix/](https://ajmals.github.io/met-weather-data-analysis/monsoon_transition_matrix/)**  
> *(Runs 100% client-side in your browser — zero backend required)*

---

## 📖 Meteorological Overview

The Maldivian climate is governed by two opposing monsoon regimes divided into **27 Nakaiys** (traditional 13-to-14 day astronomical calendar sectors):
- **Iruvai (Northeast Monsoon):** Dry, calm trade wind season (Nakaiys 1–9: *Mula* to *Reyva*).
- **Hulhangu (Southwest Monsoon):** Wet, turbulent season with heavy squalls and westerly gusts (Nakaiys 10–27: *Assidha* to *Dosha*).

This package models the two critical seasonal transition inflection points:
1. **Assidha Transition Window (Iruvai $\rightarrow$ Hulhangu Onset):**
   - **Atmospheric Pressure Drop:** Sea-level pressure falls from **1011.32 hPa** (*Huvan*) to **1009.81 hPa** (*Assidha*) and reaches the seasonal minimum of **1009.29 hPa** (*Burunu*), creating a net transition drop of **−2.03 hPa**.
   - **Prevailing Wind Reversal:** Wind direction flips dramatically from Easterly trade winds (**81.6%** NE/E in *Hiyaviha*) to strong Westerlies (**83.6%** W/NW/SW in *Burunu*).
   - **Extreme Rainfall Surge:** 90th percentile daily rainfall surges to **19.47 mm/day** in *Burunu* and **28.31 mm/day** in *Roanu*.

2. **Halha Transition Window (Hulhangu $\rightarrow$ Iruvai Onset):**
   - **Atmospheric Pressure Recovery:** Pressure rebounds to **1011.25 hPa** (+1.5 hPa recovery) in *Furahalha*.
   - **Trade Wind Re-establishment:** Easterly trade winds re-establish rapidly with **77.0%** frequency in *Furahalha*.
   - **Heavy Onset Rain:** 90th percentile daily rainfall reaches **27.44 mm/day** in *Mula*.

---

## 📁 Package Architecture

```
monsoon_transition_matrix/
├── README.md                      # Technical documentation & usage guide
├── index.html                     # Interactive Web Dashboard UI
├── style.css                      # Modern dark theme styles (Glassmorphism & typography)
├── app.js                         # Dynamic visualization controller (Plotly.js / D3.js)
├── monsoon_transition_data.json   # Pre-aggregated transition dataset (used by app.js)
│
├── data_processor.py              # Python data pipeline: parses CSV -> computes U/V & JSON
├── create_transition_matrix.py    # Python plot engine: renders publication PNGs and PDF
│
└── output/                        # Pre-generated publication-quality artifacts
    ├── transition_sankey_flow.png              # Sankey ribbon diagram of wind sector shifts
    ├── pressure_rainfall_transition_profile.png # Dual-axis bar/line chart across all 27 Nakaiys
    ├── wind_streamline_vectors.png             # Polar wind streamline compass plots
    └── monsoon_transition_summary_report.pdf   # Composite multi-panel scientific summary
```

---

## 📊 Core Variables Analyzed

| Variable | Description | Source / Units |
|---|---|---|
| `Monsoon` | Seasonal phase: **Iruvai** (NE), **Hulhangu** (SW), or Transition | Meteorological classification |
| `Nakaiy` | 27 astronomical calendar sectors (13–14 days each) | Traditional Maldivian calendar |
| `pressure_hpa` | Mean and minimum daily sea-level pressure | Daily MET station observations ($hPa$) |
| `clean_wind_sector` | 8-sector cardinal wind compass directions (`N`, `NE`, `E`, `SE`, `S`, `SW`, `W`, `NW`) | Derived from MET compass readings |
| `u_kts`, `v_kts` | East-West ($U$) and North-South ($V$) wind vector components | Meteorological vector decomposition ($kts$) |
| `rainfall_mm` | Daily rainfall: Mean ($R_{\text{mean}}$) and 90th percentile intensity ($R_{p90}$) | Daily rain gauge records ($mm/day$) |

---

## 🚀 Step-by-Step Usage Instructions

### Option 1: Run the Interactive Dashboard Locally (Fastest)

The pre-aggregated data (`monsoon_transition_data.json`) is already generated and included. You only need a local web server (no Python dependencies required):

#### From the project root (`met-weather-analysis/`):
```bash
python3 -m http.server 8000
```
Then open: **[http://localhost:8000/monsoon_transition_matrix/](http://localhost:8000/monsoon_transition_matrix/)**

#### Or from within `monsoon_transition_matrix/`:
```bash
cd monsoon_transition_matrix
python3 -m http.server 8000
```
Then open: **[http://localhost:8000/](http://localhost:8000/)**

---

### Option 2: Re-generate Data & Publication Graphics

If you modify the source data or want to re-run the Python data pipeline and figure generator:

#### 1. Activate the Python Virtual Environment
From the project root:
```bash
source .venv/bin/activate
```
*(If dependencies are not yet installed, run `pip install -r requirements.txt`)*

#### 2. Re-process Raw Data to JSON
Reads `data/hulhule_nakai_mapped.csv` and updates `monsoon_transition_matrix/monsoon_transition_data.json`:
```bash
# From project root:
python monsoon_transition_matrix/data_processor.py

# Or from inside monsoon_transition_matrix/:
cd monsoon_transition_matrix
python data_processor.py
```

#### 3. Render High-Resolution Publication Plots (PNG & PDF)
Generates high-res visual figures in `monsoon_transition_matrix/output/`:
```bash
# From project root:
python monsoon_transition_matrix/create_transition_matrix.py

# Or from inside monsoon_transition_matrix/:
cd monsoon_transition_matrix
python create_transition_matrix.py
```

---

## 🖼️ Pre-Generated Publication Artifacts

The generated artifacts are available in [`output/`](./output/):

1. **[`transition_sankey_flow.png`](./output/transition_sankey_flow.png)**  
   *Sankey flow diagram illustrating the volume and percentage of wind directional transitions across consecutive Nakaiys during the Assidha and Halha inflection periods.*

2. **[`pressure_rainfall_transition_profile.png`](./output/pressure_rainfall_transition_profile.png)**  
   *Dual-axis visualization tracking mean sea-level pressure drop (line) against mean and 90th percentile rainfall surges (bars) across all 27 Nakaiys.*

3. **[`wind_streamline_vectors.png`](./output/wind_streamline_vectors.png)**  
   *Polar streamline vector representations displaying wind directionality and magnitude dynamics.*

4. **[`monsoon_transition_summary_report.pdf`](./output/monsoon_transition_summary_report.pdf)**  
   *Complete multi-panel executive summary report combining key statistics, pressure curves, and vector reversals.*

---

## 🌐 Deploying to GitHub Pages

This web application requires no server-side logic:
1. Ensure `index.html`, `style.css`, `app.js`, and `monsoon_transition_data.json` are committed to your branch.
2. In your GitHub repository, navigate to **Settings** $\rightarrow$ **Pages**.
3. Under **Source**, select **Deploy from a branch** and pick your target branch and root folder.
4. Your dashboard will be live at `https://<username>.github.io/<repo>/monsoon_transition_matrix/`.
