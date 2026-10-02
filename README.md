# 🇲🇻 Maldives Weather & Climate Analysis

A comprehensive 50-year (1974–2025) empirical analysis of daily meteorological records from **five Maldives weather observation stations**, investigating long-term climate trends, regional rainfall gradients, monsoon dynamics, ENSO impacts, sea level rise, and traditional Maldivian Nakaiy calendar patterns.

[![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-GitHub%20Pages-blue?style=for-the-badge&logo=github)](https://ajmals.github.io/met-weather-data-analysis/monsoon_transition_matrix/)
[![Python](https://img.shields.io/badge/Python-3.12%2B-brightgreen?style=for-the-badge&logo=python)](requirements.txt)
[![Data Period](https://img.shields.io/badge/Data%20Period-1974--2025-orange?style=for-the-badge)](./data/)

> **🌐 Live Interactive Visualization:**  
> Explore the **[Monsoon Shift Transition Matrix Dashboard](https://ajmals.github.io/met-weather-data-analysis/monsoon_transition_matrix/)** hosted on GitHub Pages (runs 100% in your browser, no server required).

---

## ⚡ Quick Start

All cleaned datasets (`data/`) and pre-computed dashboard payloads (`monsoon_transition_matrix/`) are already provided. You can run notebooks or start the web dashboard immediately.

```bash
# 1. Clone the repository
git clone https://github.com/ajmals/met-weather-data-analysis.git
cd met-weather-data-analysis

# 2. Set up virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Launch JupyterLab to inspect analysis notebooks
jupyter lab
```

### To Launch the Interactive Dashboard Locally:
```bash
# From the project root:
python3 -m http.server 8000
```
Open **[http://localhost:8000/monsoon_transition_matrix/](http://localhost:8000/monsoon_transition_matrix/)** in your browser.

---

## 📡 Stations Covered

The dataset covers five primary meteorological observation stations maintained by the **Maldives Meteorological Service (MET)**, spanning an 800 km north-to-south latitudinal gradient from 7° N to 1° S (crossing the Equator):

| Station | Region | Latitude | Period | Daily Records | Cleaned Dataset |
|---|---|---|---|---|---|
| **Hanimaadhoo** | Far North | 6.76° N | 1991–2025 | 12,449 | [`hanimaadhoo_cleaned_data.csv`](./data/hanimaadhoo_cleaned_data.csv) |
| **Hulhule** | Central (Capital / Airport) | 4.19° N | 1974–2025 | 18,809 | [`hulhule_cleaned_data.csv`](./data/hulhule_cleaned_data.csv) |
| **Kadhdhoo** | Central-South | 1.86° N | 1991–2025 | 12,449 | [`kadhdhoo_cleaned_data.csv`](./data/kadhdhoo_cleaned_data.csv) |
| **Kaadedhdhoo** | South | 0.49° N | 1994–2025 | 11,353 | [`kaadedhdhoo_cleaned_data.csv`](./data/kaadedhdhoo_cleaned_data.csv) |
| **Gan** | Far South / Equatorial | 0.69° S | 1978–2025 | 17,350 | [`gan_cleaned_data.csv`](./data/gan_cleaned_data.csv) |

---

## 🔄 End-to-End Analysis Workflow

The repository is structured into a modular four-stage analytical pipeline:

```
Raw MET Station Records (1974–2025)
                │
                ▼
  [1] maldives_weather_data_quality.ipynb
      • Systematic audit, typo corrections & outlier clipping
      • Outputs: 5 cleaned CSVs in data/
                │
        ┌───────┴────────────────────────────────────────┐
        ▼                                                ▼
  [2] maldives_weather_exploration.ipynb        [3] maldives_climate_deepdive.ipynb
      • Multi-station exploratory analysis          • 5 Core Climate Hypotheses (Q1–Q5)
      • Latitudinal temperature correlation         • Sea level rise integration
      • Hulhule seasonal decomposition              • Nakaiy calendar mapping
      • 24-month SARIMAX forecasting                • Outputs: data/hulhule_nakai_mapped.csv
                                                         │
                                                         ▼
                                            [4] monsoon_transition_matrix/
                                                • data_processor.py ──► monsoon_transition_data.json
                                                • create_transition_matrix.py ──► output/ (PNG & PDF)
                                                • index.html (Interactive Dashboard)
```

> **Note:** All output files from each stage are already committed to the repository, so you can execute or modify any stage independently without running earlier stages first.

---

## 📓 Notebooks & Findings

### 1. [`maldives_weather_data_quality.ipynb`](./maldives_weather_data_quality.ipynb) — Data Cleaning Pipeline
Audits raw meteorological daily records across all five stations and builds reproducible cleaned datasets.
- **Header standardization:** Resolves inconsistent column names and variable orders across stations.
- **Entry error corrections:** Fixes transcription typos (e.g. pressure values of `10117.0 hPa → 1011.7 hPa`, `1053.3 hPa → 1013.3 hPa`).
- **Meteorological notation conversion:** Converts trace precipitation (`TR → 0.05 mm`) and dry indicators (`NIL → 0.0 mm`).
- **Physical boundary clipping:** Adjusts impossible humidity readings (e.g. `195% → 95%`, `102% → 100%`).
- **Placeholder filtering:** Removes zero-filled and placeholder records from Kadhdhoo's 1990–1991 instrumentation gap.

---

### 2. [`maldives_weather_exploration.ipynb`](./maldives_weather_exploration.ipynb) — Climate Trends & Time Series
Performs multi-station exploratory data analysis and time-series modeling.
- 📈 **Long-term warming signal:** Detects steady multidecadal upward trends in mean daily temperatures across all stations.
- 🌀 **Monsoon dynamics:** Contrasts the Northeast (Iruvai) and Southwest (Hulhangu) monsoons; Hulhangu brings ~28% higher average wind speeds and higher rainfall variability.
- 🗺️ **Spatial correlation:** Measures high cross-atoll temperature correlation despite the 800 km archipelago length.
- 📉 **Seasonal decomposition:** Deconstructs 50 years of Hulhule monthly records into trend, cyclical seasonal, and residual components.
- 🔮 **SARIMAX modeling:** Validates time-series models against a 2024–2025 test split and projects monthly temperatures through 2026–2027.

---

### 3. [`maldives_climate_deepdive.ipynb`](./maldives_climate_deepdive.ipynb) — Five Core Climate Hypotheses

#### Q1 — Regional Rainfall Gradient: Is the South rainier than the North?
**Yes, unequivocally.** Analysis of 1995–2024 records proves a pronounced latitudinal rainfall gradient:
- **Kaadedhdhoo (South):** 2,212.7 mm/yr
- **Kadhdhoo (Central-South):** 2,222.7 mm/yr
- **Hulhule (Central):** 2,009.9 mm/yr
- **Hanimaadhoo (North):** 1,763.9 mm/yr

The South receives **~450 mm/year (+25%) more rain** than the North and experiences a **58% higher frequency** of extreme rain days ($\ge 50\text{ mm}$).

#### Q2 — Nakaiy Transitions & Rainfall Peaks
Evaluates traditional Maldivian folklore that *Nakaiy change* days (the transition boundaries between the 27 traditional 13-day astronomical calendar periods) trigger stormy weather. Empirically compares $\pm 2$-day transition windows against stable mid-Nakaiy days.

#### Q3 — ENSO Impact (El Niño vs. La Niña)
Categorizes historical years using NOAA's Oceanic Niño Index (ONI). Quantifies the impact of El Niño on extreme heat days ($\ge 31.5^\circ\text{C}$), temperature anomalies, and suppressed monsoonal rainfall.

#### Q4 — Climate Change & Sea Level Rise
Fits linear regression trends to 50 years of observations (1975–2024) and joins University of Hawaii Sea Level Center (UHSLC) / IPCC Indian Ocean tide records (`maldives_sealevel_rise.csv`) to compute decadal warming and seal-level rise correlation.

#### Q5 — Tropical Night Acceleration & Heat Index
Finds nighttime minimum temperatures are rising faster than daytime maximums, tracking the surge in **stifling tropical nights** (nights where min temperature does not drop below 27.0°C) and computing the NOAA Heat Index time series to evaluate human heat stress.

---

## 🌐 Interactive Dashboard — Monsoon Shift Transition Matrix

An interactive client-side web application dedicated to analyzing atmospheric pressure drops ($\Delta P$), prevailing wind reversals, and extreme rainfall surges during the Maldivian monsoon transitions (**Assidha** and **Halha**).

* **Detailed Docs:** [`monsoon_transition_matrix/README.md`](./monsoon_transition_matrix/README.md)
* **Live Demo:** [https://ajmals.github.io/met-weather-data-analysis/monsoon_transition_matrix/](https://ajmals.github.io/met-weather-data-analysis/monsoon_transition_matrix/)

### Features:
- 🌊 **Sankey Ribbon Diagram:** Interactive flow of directional shifts between wind sectors across consecutive Nakaiys.
- 🧭 **Polar Streamline Compass:** Radial vector plots visualizing wind velocity and angle reversals.
- 📉 **Dual-Axis Transition Profile:** Bar/line chart synchronizing pressure drop against 90th percentile rainfall surges.
- 📑 **Publication Graphics & PDF Report:** Pre-rendered figures located in [`monsoon_transition_matrix/output/`](./monsoon_transition_matrix/output/).

### Key Scientific Transition Findings:
- **Assidha Transition (Iruvai $\rightarrow$ Hulhangu Onset):** Sea-level pressure drops from **1011.32 hPa** (*Huvan*) to **1009.29 hPa** (*Burunu*), a transition drop of **−2.03 hPa**. Wind direction reverses from **81.6%** Easterly in *Hiyaviha* to **83.6%** Westerly in *Burunu*. 90th percentile rainfall surges to **19.47 mm/day**.
- **Halha Transition (Hulhangu $\rightarrow$ Iruvai Onset):** Sea-level pressure recovers by **+1.5 hPa** to **1011.25 hPa** in *Furahalha*. Easterly trade winds establish at **77.0%** frequency, accompanied by heavy onset rainfall of **27.44 mm/day** (p90) in *Mula*.

---

## 🗂️ Project Structure

```
met-weather-analysis/
├── README.md                              # Main project documentation & guide
├── requirements.txt                      # Python dependencies (pandas, matplotlib, statsmodels, etc.)
├── mindblowing_weather_questions.md      # Advanced research hypotheses on archipelagic dynamics
│
├── data/                                  # Cleaned datasets and external benchmarks
│   ├── hulhule_cleaned_data.csv           # Central/Capital station (1974–2025)
│   ├── hanimaadhoo_cleaned_data.csv       # North station (1991–2025)
│   ├── kadhdhoo_cleaned_data.csv          # Central-South station (1991–2025)
│   ├── kaadedhdhoo_cleaned_data.csv       # South station (1994–2025)
│   ├── gan_cleaned_data.csv               # Equatorial station (1978–2025)
│   ├── hulhule_nakai_mapped.csv           # Hulhule daily data with 27-Nakaiy calendar mapping
│   └── maldives_sealevel_rise.csv         # UHSLC/IPCC Indian Ocean sea level benchmark
│
├── monsoon_transition_matrix/             # Interactive dashboard & transition analysis module
│   ├── README.md                          # Dedicated module documentation
│   ├── index.html                         # Dashboard web app interface
│   ├── style.css                          # Modern dark glassmorphism styling
│   ├── app.js                             # Plotly.js / D3.js chart renderer
│   ├── monsoon_transition_data.json       # Aggregated JSON payload consumed by app.js
│   ├── data_processor.py                  # Python data pipeline to re-generate JSON
│   ├── create_transition_matrix.py        # Python script to render static PNG & PDF figures
│   └── output/                            # Generated publication figures
│       ├── transition_sankey_flow.png
│       ├── pressure_rainfall_transition_profile.png
│       ├── wind_streamline_vectors.png
│       └── monsoon_transition_summary_report.pdf
│
├── maldives_weather_data_quality.ipynb   # [Pipeline Step 1] Cleaning & auditing raw data
├── maldives_weather_exploration.ipynb    # [Pipeline Step 2] Exploration, trends & SARIMAX
└── maldives_climate_deepdive.ipynb       # [Pipeline Step 3] 5 research hypotheses & Nakaiy mapping
```

---

## 📜 Data Source & Variables

Daily meteorological records courtesy of the **Maldives Meteorological Service (MET)**, spanning 1974 through 2025.

**Variables included:**
- **Atmospheric Pressure:** Station and Sea-Level Pressure ($hPa$)
- **Temperature:** Maximum, Minimum, and Mean Dry-Bulb Air Temperature ($^\circ\text{C}$)
- **Humidity:** Relative Humidity ($\%$)
- **Wind Dynamics:** Prevailing Direction (16-point compass / 8 cardinal sectors) and Mean Speed ($kts$)
- **Precipitation:** Daily 24-hour Accumulated Rainfall ($mm$)
- **Solar & Atmosphere:** Daily Sunshine Duration ($hours$) and Cloud Cover ($oktas$)
