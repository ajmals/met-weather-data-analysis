# 🌀 Monsoon Shift Transition Matrix

A dedicated meteorological analysis and interactive visualization package studying atmospheric pressure drops (&Delta;P), wind vector streamlines ($U, V$), directional reversals, and extreme rainfall surges during the Maldivian monsoon transitions (**Assidha** and **Halha**) across Northern, Central, and Southern atolls.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-blue?style=for-the-badge&logo=github)](https://ajmals.github.io/met-weather-data-analysis/monsoon_transition_matrix/)

> **🌐 Live Interactive Dashboard:**  
> **[https://ajmals.github.io/met-weather-data-analysis/monsoon_transition_matrix/](https://ajmals.github.io/met-weather-data-analysis/monsoon_transition_matrix/)**  
> *(Runs 100% client-side in your browser — zero backend required)*

---

## 📖 Meteorological Overview

The Maldivian climate is governed by two opposing monsoon regimes divided into **27 Nakaiys** (traditional 13-to-14 day astronomical calendar sectors):
- **Iruvai (Northeast Monsoon):** Dry, calm trade wind season (Nakaiys 1–9: *Mula* to *Reyva*).
- **Hulhangu (Southwest Monsoon):** Wet, turbulent season with heavy squalls and westerly gusts (Nakaiys 10–27: *Assidha* to *Dosha*).

The calendar mapping standardizing the 27 Nakaiy periods and their alignment with the Gregorian calendar is sourced from the **[Maldivian Nakaiy Calendar Dataset](https://github.com/ajmals/Maldivian_Nakaiy_Calander_Dataset)**.

This package models the two critical seasonal transition inflection points:
1. **Assidha Transition Window (Iruvai &rarr; Hulhangu Onset):**
   - **Atmospheric Pressure Drop:** Sea-level pressure falls from **1011.32 hPa** (*Huvan*) to **1009.81 hPa** (*Assidha*) and reaches the seasonal minimum of **1009.29 hPa** (*Burunu*), creating a net transition drop of **&minus;2.03 hPa**.
   - **Prevailing Wind Reversal:** Wind direction flips dramatically from Easterly trade winds (**81.6%** NE/E in *Hiyaviha*) to strong Westerlies (**83.6%** W/NW/SW in *Burunu*).
   - **Extreme Rainfall Surge:** 90th percentile daily rainfall surges to **19.47 mm/day** in *Burunu* and **28.31 mm/day** in *Roanu*.

2. **Halha Transition Window (Hulhangu &rarr; Iruvai Onset):**
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
├── app.js                         # Dynamic visualization controller (Plotly.js)
├── monsoon_transition_data.json   # Multi-station aggregated transition dataset (used by app.js)
└── data_processor.py              # Python data pipeline: parses station CSVs -> computes U/V & JSON
```

---

## 📊 Core Variables Analyzed

| Variable | Description | Source / Units |
|---|---|---|
| `Monsoon` | Seasonal phase: **Iruvai** (NE), **Hulhangu** (SW), or Transition | Meteorological classification |
| `Nakaiy` | 27 astronomical calendar sectors (13–14 days each) | [Maldivian Nakaiy Calendar Dataset](https://github.com/ajmals/Maldivian_Nakaiy_Calander_Dataset) |
| `pressure_hpa` | Mean and minimum daily sea-level pressure | Daily MET station observations ($hPa$) |
| `clean_wind_sector` | 8-sector cardinal wind compass directions (`N`, `NE`, `E`, `SE`, `S`, `SW`, `W`, `NW`) | Derived from MET compass readings |
| `u_kts`, `v_kts` | East-West ($U$) and North-South ($V$) wind vector components | Meteorological vector decomposition ($kts$) |
| `rainfall_mm` | Daily rainfall: Mean ($R_{\text{mean}}$) and 90th percentile intensity ($R_{p90}$) | Daily rain gauge records ($mm/day$) |

---

## 🚀 Step-by-Step Usage Instructions

### Option 1: Run the Interactive Dashboard Locally (Fastest)

The pre-aggregated data (`monsoon_transition_data.json`) covering Hulhule (Central), Gan (Southern), and Hanimaadhoo (Northern) is already generated and included. You only need a local web server (no Python dependencies required):

#### From the project root (`met-weather-analysis/`):
```bash
python3 -m http.server 8000
```
Then open: **[http://localhost:8000/monsoon_transition_matrix/](http://localhost:8000/monsoon_transition_matrix/)** (or simply [http://localhost:8000/](http://localhost:8000/))

#### Or from within `monsoon_transition_matrix/`:
```bash
cd monsoon_transition_matrix
python3 -m http.server 8000
```
Then open: **[http://localhost:8000/](http://localhost:8000/)**

---

### Option 2: Re-generate Multi-Station JSON Payload

If you modify the source data or want to re-run the Python data pipeline:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run pipeline from project root:
python monsoon_transition_matrix/data_processor.py
```
This reads station records from `data/` and updates `monsoon_transition_matrix/monsoon_transition_data.json`.

---

## 🌐 Deploying to GitHub Pages

This web application requires no build steps or backend servers:
1. Ensure `index.html`, `style.css`, `app.js`, and `monsoon_transition_data.json` are committed to your branch.
2. In your GitHub repository, navigate to **Settings** &rarr; **Pages**.
3. Under **Source**, select **Deploy from a branch** and choose `/ (root)`.
4. The dashboard will be live at `https://<username>.github.io/<repo>/` (automatically forwarding to `monsoon_transition_matrix/`).
