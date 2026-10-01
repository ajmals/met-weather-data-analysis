# 🇲🇻 Maldives Weather & Climate Analysis

A comprehensive 50-year (1974–2025) empirical analysis of daily meteorological records from **five Maldives weather stations**, exploring long-term climate trends, monsoon dynamics, ENSO impacts, sea level rise, and traditional Nakaiy calendar patterns.

> **🌐 Interactive Dashboard →** [Monsoon Shift Transition Matrix](./monsoon_transition_matrix/index.html)  
> *(Open locally or deploy via GitHub Pages — no backend required)*

---

## 📡 Stations Covered

| Station | Region | Lat/Lon | Period |
|---|---|---|---|
| **Hanimaadhoo** | Far North | 6.76° N | 1991–2025 |
| **Hulhule** | Central (Capital) | 4.19° N | 1974–2025 |
| **Kadhdhoo** | Central-South | 1.86° N | 1991–2025 |
| **Kaadedhdhoo** | South | 0.49° N | 1994–2025 |
| **Gan** | Far South / Equatorial | 0.69° S | 1978–2025 |

---

## 📓 Notebooks

### 1. [`maldives_weather_data_quality.ipynb`](./maldives_weather_data_quality.ipynb) — Data Cleaning Pipeline

A systematic data quality audit and cleaning pipeline on the raw daily weather datasets from all five stations.

**What it does:**
- Loads raw CSV files, standardizes column names and ordering across stations
- Detects and corrects data entry errors (e.g. `10117.0 hPa → 1011.7 hPa`, `1053.3 hPa → 1013.3 hPa`)
- Converts meteorological shorthand (`TR` → `0.05 mm`, `NIL` → `0.0 mm`)
- Clips humidity outliers (e.g. `195%` → `95%`, `102%` → `100%`)
- Drops placeholder rows from Kadhdhoo (1990–1991 gap period)
- Exports clean CSVs to `data/`

**Output:** 5 cleaned station CSV files in [`data/`](./data/)

---

### 2. [`maldives_weather_exploration.ipynb`](./maldives_weather_exploration.ipynb) — Climate Trends & Time Series

Exploratory data analysis and time-series modeling across all five stations.

**What it covers:**
- 📈 **Annual temperature trends** — long-term warming signal across stations
- 🌀 **Monsoon season analysis** — Northeast (Iruvai) vs Southwest (Hulhangu) wind speed and rainfall patterns
- 🗺️ **Spatial correlation matrix** — latitudinal temperature divergence across the 800 km archipelago
- 📉 **Seasonal decomposition** — trend, seasonal, and residual components of Hulhule monthly temperatures
- 🧮 **Stationarity testing** — Augmented Dickey-Fuller (ADF) test
- 🔮 **SARIMAX forecasting** — train/test split (2024–2025) and 24-month projection (2026–2027)

**Key Finding:** A clear warming trend is visible in the long-term Hulhule temperature decomposition, with Southwest monsoon average wind speeds ~28% higher than the Northeast dry season.

---

### 3. [`maldives_climate_deepdive.ipynb`](./maldives_climate_deepdive.ipynb) — Deep Dive: 5 Core Climate Questions

Comprehensive empirical investigation of five advanced climate hypotheses.

#### Q1 — Regional Rainfall Gradient: Is the South rainier than the North?
**Yes.** Empirical data from 1995–2024 across all stations confirms a strong latitudinal rainfall gradient:
- South (Kaadedhdhoo): **2,212.7 mm/yr**
- Central-South (Kadhdhoo): **2,222.7 mm/yr**
- Central (Hulhule): **2,009.9 mm/yr**
- North (Hanimaadhoo): **1,763.9 mm/yr**

The South receives **~450 mm/year (+25%) more rain** than the North, with **58% higher frequency** of extreme rain events.

#### Q2 — Nakaiy Transitions & Rainfall Peaks
Tests the traditional Maldivian folklore hypothesis that *Nakaiy change* days (transition windows between the 27 traditional 13-day calendar sectors) bring more intense rainfall and storm activity. Empirically evaluates ±2 day transition windows vs. stable mid-Nakaiy days across all stations.

#### Q3 — ENSO Impact (El Niño vs. La Niña)
Classifies historical years by NOAA ONI index into El Niño, La Niña, and Neutral phases. Analyses impacts on Hulhule temperature anomalies, extreme heat days (≥31.5°C), and seasonal rainfall totals.

#### Q4 — Climate Change & Sea Level Rise
Fits an OLS linear regression model to the 50-year temperature record (1975–2024). Integrates UHSLC/IPCC Indian Ocean sea level rise data (`maldives_sealevel_rise.csv`) to compute decadal warming rate (°C/decade) and Pearson correlation between temperature rise and sea level rise.

#### Q5 — Tropical Night Acceleration & Heat Index
Investigates whether nighttime minimum temperatures are warming faster than daytime maximums. Tracks **stifling tropical nights** (nights where min temp fails to drop below 27.0°C) and computes the NOAA Heat Index time series to quantify the felt-temperature surge beyond raw thermometer readings.

---

## 🌐 Interactive Dashboard — Monsoon Shift Transition Matrix

An interactive web application visualizing atmospheric pressure drops (ΔP), prevailing wind directional reversals, and extreme rainfall surges during the Maldivian monsoon transitions (**Assidha** and **Halha**).

**📂 Location:** [`monsoon_transition_matrix/`](./monsoon_transition_matrix/)

**Features:**
- 🌊 **Sankey ribbon flow diagram** — wind sector transitions across all 27 Nakaiys
- 🧭 **Polar wind streamline compass** — U/V vector components during monsoon phases
- 📉 **Pressure drop matrix profiles** — sea-level pressure change across Nakaiy transitions

**🔬 Key Scientific Findings:**
- **Assidha Transition (Iruvai → Hulhangu):** Pressure drops from 1011.32 hPa → 1009.29 hPa (max ΔP: **−2.03 hPa**), wind direction flips from 81.6% NE/E → 83.6% W/NW/SW, rainfall surges to 19.47 mm/day (p90)
- **Halha Transition (Hulhangu → Iruvai):** Pressure recovers to 1011.25 hPa (+1.5 hPa), easterly trade winds re-establish at 77.0%, extreme rainfall peaks at 27.44 mm/day (p90) in Mula

**To run locally:**
```bash
source .venv/bin/activate
python -m http.server 8000
# Open: http://localhost:8000/monsoon_transition_matrix/
```

**To deploy on GitHub Pages:** Commit all files in `monsoon_transition_matrix/` (including `monsoon_transition_data.json`) and enable GitHub Pages in repo settings. The app runs entirely in the browser — no backend required.

---

## 🗂️ Project Structure

```
met-weather-analysis/
├── data/                              # Cleaned station datasets
│   ├── hulhule_cleaned_data.csv       # Capital station (1974–2025)
│   ├── hanimaadhoo_cleaned_data.csv   # North (1991–2025)
│   ├── kadhdhoo_cleaned_data.csv      # Central-South (1991–2025)
│   ├── kaadedhdhoo_cleaned_data.csv   # South (1994–2025)
│   ├── gan_cleaned_data.csv           # Far South / Equatorial (1978–2025)
│   ├── hulhule_nakai_mapped.csv       # Hulhule with Nakaiy calendar mapping
│   └── maldives_sealevel_rise.csv     # UHSLC Indian Ocean sea level data
│
├── monsoon_transition_matrix/         # Interactive web dashboard
│   ├── index.html                     # Dashboard UI
│   ├── app.js                         # Chart rendering (Plotly.js / D3.js)
│   ├── style.css                      # Glassmorphism dark UI
│   ├── monsoon_transition_data.json   # Pre-generated data payload
│   ├── data_processor.py              # Python data engine & JSON exporter
│   └── create_transition_matrix.py    # Static plot generator (PNG/PDF)
│
├── maldives_weather_data_quality.ipynb   # Data cleaning pipeline
├── maldives_weather_exploration.ipynb    # EDA & time series
├── maldives_climate_deepdive.ipynb       # 5-question deep dive
├── mindblowing_weather_questions.md      # Research hypotheses & ideas
├── requirements.txt                      # Python dependencies
└── .venv/                                # Local virtual environment (not tracked)
```

---

## ⚙️ Setup

**Requirements:** Python 3.12+

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch JupyterLab
jupyter lab
```

---

## 📜 Data Source

Daily meteorological records sourced from the **Maldives Meteorological Service (MET)** covering five primary weather observation stations across the Maldives archipelago, spanning **1974–2025**.

Variables include: atmospheric pressure (hPa), maximum/minimum/mean temperature (°C), relative humidity (%), wind direction (compass), wind speed (kts), daily rainfall (mm), sunshine hours, and cloud cover (oktas).
