# 🇲🇻 Maldives Weather & Climate Analysis

A comprehensive 50-year (1974–2025) empirical analysis of daily meteorological records from **five Maldives weather observation stations**, investigating long-term climate trends, regional rainfall gradients, monsoon dynamics, ENSO impacts, sea level rise, and traditional Maldivian Nakaiy calendar patterns.

[![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-GitHub%20Pages-blue?style=for-the-badge&logo=github)](https://ajmals.github.io/met-weather-data-analysis/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-brightgreen?style=for-the-badge&logo=python)](requirements.txt)
[![Data Period](https://img.shields.io/badge/Data%20Period-1974--2025-orange?style=for-the-badge)](./data/)

> **🌐 Live Interactive Visualization:**  
> Explore the **[Monsoon Shift Transition Matrix Dashboard](https://ajmals.github.io/met-weather-data-analysis/)** hosted on GitHub Pages (runs 100% in your browser, no server required).

---

## ⚡ Quick Start

All cleaned datasets (`data/`) and pre-computed multi-station dashboard payloads (`monsoon_transition_matrix/`) are already provided. You can run notebooks or start the web dashboard immediately.

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
Open **[http://localhost:8000/](http://localhost:8000/)** (or [http://localhost:8000/monsoon_transition_matrix/](http://localhost:8000/monsoon_transition_matrix/)) in your browser.

---

## 📡 Stations Covered

The dataset covers five primary meteorological observation stations maintained by the **Maldives Meteorological Service (MET)**, spanning an 800 km north-to-south latitudinal gradient from 7° N to 1° S (crossing the Equator):

| Station | Region | Latitude | Period | Daily Records | Cleaned Dataset |
|---|---|---|---|---|---|
| **Hanimaadhoo** | Far North | 6.76° N | 1991–2025 | 12,449 | [`hanimaadhoo_cleaned_data.csv`](./data/hanimaadhoo_cleaned_data.csv) |
| **Hulhule** | Central (Capital / Airport) | 4.19° N | 1974–2025 | 18,628 | [`hulhule_cleaned_data.csv`](./data/hulhule_cleaned_data.csv) |
| **Kadhdhoo** | Central-South | 1.86° N | 1991–2025 | 12,450 | [`kadhdhoo_cleaned_data.csv`](./data/kadhdhoo_cleaned_data.csv) |
| **Kaadedhdhoo** | South | 0.49° N | 1994–2025 | 11,552 | [`kaadedhdhoo_cleaned_data.csv`](./data/kaadedhdhoo_cleaned_data.csv) |
| **Gan** | Far South / Equatorial | 0.69° S | 1978–2025 | 17,348 | [`gan_cleaned_data.csv`](./data/gan_cleaned_data.csv) |

*Total observations analyzed: **72,427 station-days**.*

---

## 🔄 End-to-End Analysis Workflow

The repository is structured into an empirical data pipeline:

```
Cleaned MET Station Records (1974–2025)
          │
          ├──► [1] maldives_weather_exploration.ipynb
          │        • Multi-station exploratory analysis
          │        • Latitudinal temperature correlation
          │        • Hulhule seasonal decomposition
          │        • 24-month SARIMAX forecasting
          │
          ├──► [2] maldives_climate_deepdive.ipynb
          │        • Climate Hypotheses (Q1–Q5)
          │        • Sea level rise integration
          │        • Nakaiy calendar mapping (from Maldivian_Nakaiy_Calander_Dataset)
          │
          └──► [3] monsoon_transition_matrix/
                   • data_processor.py ──► monsoon_transition_data.json
                   • index.html (Interactive Multi-Station Dashboard)
```

---

## 🧹 Data Cleaning & Quality Methodology

All raw observation station records underwent systematic data auditing and curation:
- **Header standardization:** Resolved inconsistent column naming and ordering across station exports.
- **Entry typo corrections:** Corrected manual log typos (e.g. pressure values of `10117.0 hPa → 1011.7 hPa` in Gan, `1053.3 hPa → 1013.3 hPa` in Hulhule).
- **Meteorological notation conversion:** Converted trace precipitation (`TR → 0.05 mm`) and dry indicators (`NIL → 0.0 mm`).
- **Physical boundary clipping:** Fixed out-of-range sensor readings (e.g. max humidity `195% → 95%` in Hanimaadhoo, clipping `102% → 100%`).
- **Gap filtering:** Filtered placeholder records from Kadhdhoo's 1990–1991 instrumentation gap.
- *The original audit notebook is preserved in [`archive/maldives_weather_data_quality.ipynb`](./archive/maldives_weather_data_quality.ipynb).*

---

## 🧭 Traditional Nakaiy Calendar Sourcing

The traditional Maldivian calendar divides the solar year into **27 Nakaiys** (13–14 days each), tracking seasonal wind shifts and precipitation.
The calendar reference definitions and Gregorian calendar alignments used across this project are sourced from:
- **[Maldivian Nakaiy Calendar Dataset](https://github.com/ajmals/Maldivian_Nakaiy_Calander_Dataset)** by Ajmal.

The Hulhule 50-year daily sequence is pre-mapped with Nakaiy periods in [`data/hulhule_nakai_mapped.csv`](./data/hulhule_nakai_mapped.csv).

---

## 📓 Notebooks & Core Findings

### 1. [`maldives_weather_exploration.ipynb`](./maldives_weather_exploration.ipynb) — Climate Trends & Time Series
Performs multi-station exploratory data analysis and time-series modeling.
- 📈 **Long-term warming signal:** Detects steady multidecadal upward trends in mean daily temperatures across all stations.
- 🌀 **Monsoon dynamics:** Contrasts the Northeast (Iruvai) and Southwest (Hulhangu) monsoons; Hulhangu brings ~28% higher average wind speeds and higher rainfall variability.
- 🗺️ **Spatial correlation:** Measures high cross-atoll temperature correlation despite the 800 km archipelago length.
- 📉 **Seasonal decomposition:** Deconstructs 50 years of Hulhule monthly records into trend, cyclical seasonal, and residual components.
- 🔮 **SARIMAX modeling:** Validates time-series models against a 2024–2025 test split and projects monthly temperatures through 2026–2027.

---

### 2. [`maldives_climate_deepdive.ipynb`](./maldives_climate_deepdive.ipynb) — Climate Hypotheses

#### Q1 — Regional Rainfall Gradient: Is the South rainier than the North?
**Yes, unequivocally.** Analysis of 1995–2024 records proves a pronounced latitudinal rainfall gradient:
- **Kaadedhdhoo (South):** 2,212.7 mm/yr
- **Gan (Far South):** 2,208.7 mm/yr
- **Kadhdhoo (Central-South):** 2,222.7 mm/yr
- **Hulhule (Central):** 2,009.9 mm/yr
- **Hanimaadhoo (North):** 1,763.9 mm/yr

The South receives **~450 mm/year (+25%) more rain** than the North and experiences a **58% higher frequency** of extreme rain days ($\ge 50\text{ mm}$).

#### Q2 — Nakaiy Transitions & Rainfall Peaks
Evaluates traditional Maldivian folklore that *Nakaiy change* days trigger stormy weather. Empirically compares $\pm 2$-day transition windows against stable mid-Nakaiy days.

#### Q3 — ENSO Impact (El Niño vs. La Niña)
Categorizes historical years using NOAA's Oceanic Niño Index (ONI). Quantifies the impact of El Niño on extreme heat days ($\ge 31.5^\circ\text{C}$), temperature anomalies, and suppressed monsoonal rainfall.

#### Q4 — Climate Change & Sea Level Rise
Fits linear regression trends to 50 years of observations (1975–2024) and joins University of Hawaii Sea Level Center (UHSLC) / IPCC Indian Ocean tide records (`maldives_sealevel_rise.csv`) to compute decadal warming and sea-level rise correlation.

#### Q5 — Tropical Night Acceleration & Heat Index
Finds nighttime minimum temperatures are rising faster than daytime maximums, tracking the surge in **stifling tropical nights** (nights where min temperature does not drop below 27.0°C) and computing the NOAA Heat Index time series to evaluate human heat stress.

---

## 🌐 Interactive Dashboard — Monsoon Shift Transition Matrix

An interactive client-side web application dedicated to analyzing atmospheric pressure drops (&Delta;P), prevailing wind reversals, and extreme rainfall surges during the Maldivian monsoon transitions (**Assidha** and **Halha**) across Northern, Central, and Southern stations.

* **Detailed Docs:** [`monsoon_transition_matrix/README.md`](./monsoon_transition_matrix/README.md)
* **Live Demo:** [https://ajmals.github.io/met-weather-data-analysis/](https://ajmals.github.io/met-weather-data-analysis/)

### Features:
- 🌊 **Sankey Ribbon Diagram:** Interactive flow of directional shifts between wind sectors across consecutive Nakaiys.
- 🧭 **Polar Streamline Compass:** Radial vector plots visualizing wind velocity and angle reversals, filterable by transition phase.
- 📉 **Dual-Axis Transition Profile:** Bar/line chart synchronizing pressure drop against 90th percentile rainfall surges.
- 📡 **Multi-Station Support:** Dynamic switching between Hulhule (Central), Gan (Southern), and Hanimaadhoo (Northern).

### Key Scientific Transition Findings:
- **Assidha Transition (Iruvai &rarr; Hulhangu Onset):** Sea-level pressure drops from **1011.32 hPa** (*Huvan*) to **1009.29 hPa** (*Burunu*), a transition drop of **&minus;2.03 hPa**. Wind direction reverses from **81.6%** Easterly in *Hiyaviha* to **83.6%** Westerly in *Burunu*. 90th percentile rainfall surges to **19.47 mm/day**.
- **Halha Transition (Hulhangu &rarr; Iruvai Onset):** Sea-level pressure recovers by **+1.5 hPa** to **1011.25 hPa** in *Furahalha*. Easterly trade winds establish at **77.0%** frequency, accompanied by heavy onset rainfall of **27.44 mm/day** (p90) in *Mula*.

---

## 🗂️ Project Structure

```
met-weather-analysis/
├── README.md                              # Main project documentation & guide
├── index.html                             # Root gateway (redirects to interactive dashboard)
├── requirements.txt                      # Clean Python dependencies
│
├── data/                                  # Cleaned datasets and external benchmarks
│   ├── hulhule_cleaned_data.csv           # Central/Capital station (1974–2025, 18,628 records)
│   ├── hanimaadhoo_cleaned_data.csv       # North station (1991–2025, 12,449 records)
│   ├── kadhdhoo_cleaned_data.csv          # Central-South station (1991–2025, 12,450 records)
│   ├── kaadedhdhoo_cleaned_data.csv       # South station (1994–2025, 11,552 records)
│   ├── gan_cleaned_data.csv               # Equatorial station (1978–2025, 17,348 records)
│   ├── hulhule_nakai_mapped.csv           # Hulhule daily data with 27-Nakaiy calendar mapping
│   └── maldives_sealevel_rise.csv         # UHSLC/IPCC Indian Ocean sea level benchmark
│
├── monsoon_transition_matrix/             # Interactive dashboard & transition analysis module
│   ├── README.md                          # Dedicated module documentation
│   ├── index.html                         # Dashboard web app interface
│   ├── style.css                          # Modern dark glassmorphism styling
│   ├── app.js                             # Multi-station Plotly.js chart renderer
│   ├── monsoon_transition_data.json       # Pre-aggregated multi-station JSON payload
│   └── data_processor.py                  # Python data pipeline to re-generate JSON
│
├── archive/                               # Archived development notebooks
│   └── maldives_weather_data_quality.ipynb
│
├── maldives_weather_exploration.ipynb    # [Notebook 1] Exploration, trends & SARIMAX
└── maldives_climate_deepdive.ipynb       # [Notebook 2] 5 research hypotheses & Nakaiy mapping
```

---

## 📜 Data Source & Variables

Daily meteorological records courtesy of the **Maldives Meteorological Service (MET)**, spanning 1974 through 2025. Calendar definitions courtesy of the **[Maldivian Nakaiy Calendar Dataset](https://github.com/ajmals/Maldivian_Nakaiy_Calander_Dataset)**.

**Variables included:**
- **Atmospheric Pressure:** Station and Sea-Level Pressure ($hPa$)
- **Temperature:** Maximum, Minimum, and Mean Dry-Bulb Air Temperature ($^\circ\text{C}$)
- **Humidity:** Relative Humidity ($\%$)
- **Wind Dynamics:** Prevailing Direction (16-point compass / 8 cardinal sectors) and Mean Speed ($kts$)
- **Precipitation:** Daily 24-hour Accumulated Rainfall ($mm$)
- **Solar & Atmosphere:** Daily Sunshine Duration ($hours$) and Cloud Cover ($oktas$)
