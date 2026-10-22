# 🇲🇻 Maldives Weather & Climate Analysis

A comprehensive 51-year (1975–2026) empirical analysis of daily meteorological records from **five Maldives weather observation stations**, investigating long-term climate trends, regional rainfall gradients, monsoon dynamics, ENSO impacts, sea level rise, and traditional Maldivian Nakaiy calendar patterns.

[![Dataset: maldives-met-weather-dataset](https://img.shields.io/badge/Dataset-maldives--met--weather--dataset-blue?style=for-the-badge&logo=github)](https://github.com/ajmals/maldives-met-weather-dataset)
[![Python](https://img.shields.io/badge/Python-3.11%2B-brightgreen?style=for-the-badge&logo=python)](requirements.txt)
[![Data Period](https://img.shields.io/badge/Data%20Period-1975--2026-orange?style=for-the-badge)](https://github.com/ajmals/maldives-met-weather-dataset)

---

## ⚡ Quick Start

Cleaned observation datasets (`data/cleaned/`) are synchronized from the upstream **[maldives-met-weather-dataset](https://github.com/ajmals/maldives-met-weather-dataset)** repository. You can launch and execute the analysis notebooks immediately.

```bash
# 1. Clone the repository
git clone https://github.com/ajmals/met-weather-data-analysis.git
cd met-weather-data-analysis

# 2. Set up virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Check for dataset updates or synchronize latest data
python scripts/sync_data.py --check   # Check if upstream dataset has new commits
python scripts/sync_data.py --sync    # Pull latest cleaned CSVs into data/cleaned/

# 4. Launch JupyterLab to run analysis notebooks
jupyter lab
```

---

## 🔄 Upstream Dataset Synchronization

The meteorological dataset for this analysis is maintained and published in a dedicated repository:
👉 **[github.com/ajmals/maldives-met-weather-dataset](https://github.com/ajmals/maldives-met-weather-dataset)**

This project keeps a local synchronized copy of the cleaned datasets in `data/cleaned/`. A built-in updater utility tracks upstream updates:

| Command | Action |
|---|---|
| `python scripts/sync_data.py --check` | Queries GitHub API / local sibling repo to check if newer observations or cleaning updates are available. |
| `python scripts/sync_data.py --sync` | Downloads and refreshes all CSV files in `data/cleaned/` and updates `.dataset_version.json`. |
| `python scripts/sync_data.py --status` | Displays currently synchronized commit SHA, timestamp, row counts, and file health. |

*Note: Notebooks automatically run `check_dataset_update(notify=True)` on startup and will notify you inline if an update is available.*

---

## 📡 Stations Covered

The dataset covers five primary meteorological observation stations maintained by the **Maldives Meteorological Service (MMS)**, spanning an 800 km north-to-south latitudinal gradient from 7° N to 1° S (crossing the Equator):

| Station | Atoll | Region | Latitude | Period | Daily Records | Cleaned Dataset |
|---|---|---|---|---|---|---|
| **Hanimaadhoo** | HDh. | Far North | 06°45' N | 1991–2026 | 12,906 | [`hanimaadhoo.csv`](./data/cleaned/hanimaadhoo.csv) |
| **Hulhulé** *(Male' Airport)* | K. | Central (Capital) | 04°11' N | 1975–2026 | 18,901 | [`hulhule.csv`](./data/cleaned/hulhule.csv) |
| **Kadhdhoo** | L. | Central-South | 01°51' N | 1990–2026 | 13,422 | [`kadhdhoo.csv`](./data/cleaned/kadhdhoo.csv) |
| **Kaadedhdhoo** | GDh. | South | 00°29' N | 1994–2026 | 11,961 | [`kaadedhdhoo.csv`](./data/cleaned/kaadedhdhoo.csv) |
| **Gan** *(Addu)* | S. | Far South / Equatorial | 00°41' S | 1978–2026 | 17,805 | [`gan.csv`](./data/cleaned/gan.csv) |

*Total observations analyzed: **74,995 station-days**.*

---

## 🔄 End-to-End Analysis Workflow

The repository is structured into an empirical data pipeline:

```
Cleaned MET Station Records (1975–2026)
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
          ├──► [3] maldives_monsoon_transitions.ipynb
          │        • Atmospheric pressure drops (ΔP) & barometric plunge
          │        • Wind vector streamline decomposition (U, V) & directional reversal
          │        • Extreme rainfall surges (P90) across 27 Nakaiys
          │        • Interactive Plotly Sankey diagram & polar vector compass
          │        • Multi-station latitudinal gradient & folklore testing
          │
          └──► [4] maldives_weather_factcheck.ipynb & MALDIVES_WEATHER_FACTCHECK_REPORT.md
                   • Social Media & Viral Claim Fact-Check Desk
                   • Fact-Check #001: October Malé Rainfall & 100mm Spells (Mohamed Nasheed)
                   • Fact-Check #002: Does South have more rain than North? (Fasy Ibrahim)
                   • Modular template for appending future public inquiries
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

The daily station observation sequences are mapped dynamically with Nakaiy calendar periods via `scripts/sync_data.py` (`map_nakaiy`).

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

### 3. [`maldives_monsoon_transitions.ipynb`](./maldives_monsoon_transitions.ipynb) — Monsoon Shift Transition Analysis
A comprehensive dedicated meteorological analysis examining atmospheric pressure drops ($\Delta P$), prevailing wind streamline vector reversals ($U, V$), and extreme rainfall surges during the Maldivian monsoon transitions (**Assidha** and **Halha**) across Northern, Central, and Southern stations.

- 📉 **Coupled Pressure-Rainfall Dynamics:** Maps the barometric plunge ($\Delta P = -2.03\text{ hPa}$) from late Iruvai (*Huvan*: 1011.32 hPa) to *Burunu* (1009.29 hPa) and synchronizes it with 90th percentile daily rainfall surges ($R_{p90}$ jumping from 0.0 mm/day to 19.47 mm/day in *Burunu* and 28.31 mm/day in *Roanu*).
- 🧭 **Prevailing Wind Direction Reversal:** Quantifies the abrupt transition from Easterly trade winds (81.6% in *Hiyaviha*) to roaring Westerlies (83.6% in *Burunu*), decomposing wind velocity into $U$ (East-West) and $V$ (North-South) vector streamlines.
- 🌊 **Halha Pressure Recovery:** Measures the barometric recovery ($+1.65\text{ hPa}$ to 1011.25 hPa in *Furahalha*) and the rapid re-establishment of trade winds (77.0% easterly in *Furahalha*), accompanied by retreat squall rainfall of 27.44 mm/day (P90) in *Mula*.
- 🗺️ **Multi-Station Latitudinal Transect:** Contrasts transition behavior between Hanimaadhoo (Far North), Hulhulé (Central), and Gan (Equatorial South).
- 📊 **Interactive Plotly Visualizations:** Features interactive Sankey directional ribbon flow diagrams and radial streamline vector compass plots embedded directly within the notebook.
- 🧪 **Empirical Folklore Testing:** Uses two-sample $t$-tests and Mann-Whitney $U$ tests to evaluate whether Nakaiy changeover days are significantly stormier than mid-period days.

---

### 4. [`maldives_weather_factcheck.ipynb`](./maldives_weather_factcheck.ipynb) & [`MALDIVES_WEATHER_FACTCHECK_REPORT.md`](./MALDIVES_WEATHER_FACTCHECK_REPORT.md) — Weather Fact-Check & FAQ Desk
A dedicated, living desk and empirical verification notebook testing viral social media posts and community questions against 50+ years of official MMS records.
- 🔍 **Fact-Check #001 (Mohamed Nasheed):** Evaluates claims regarding October normal rainfall in Malé, rainy days, consecutive 25–35 mm days, 100 mm 5-day spells, and climate change attribution.
  - *Verdict:* Baseline math is accurate (mean 237.7 mm; WMO normal 203.5–245.4 mm; ~15 rain days), but 100 mm in 5 days is routine (experienced in 54.9% of all Octobers).
- 🔍 **Fact-Check #002 (Fasy Ibrahim):** Answers whether the South has more rainfall than the North across an 800 km transect.
  - *Verdict:* Confirmed (+26.1% more rain in the South; ~2,216 mm/yr vs ~1,758 mm/yr). Crucially discovers that SW monsoon rainfall is nearly identical nationwide, and the disparity is generated entirely during the NE monsoon (*Iruvai*) because the South avoids the continental dry season.
- 🔍 **Fact-Check #003 (Community Lore / Anonymous):** Tests whether rainfall increases or weather changes during Nakaiy transitions.
  - *Verdict:* Busted for routine transitions (5.47 vs 5.51 mm/day, $p = 0.81$); Confirmed for macro monsoon shifts (*Assidha/Burunu* and *Dosha/Mula*) where barometric pressure drops by 2.0 hPa, winds reverse 180°, and rain surges +24% to +64%.
- 🛠️ **Expandable Architecture:** Features standardized Verdict Cards and a modular template to easily append new questions.

---

## 🗂️ Project Structure

```
met-weather-analysis/
├── README.md                              # Main project documentation & guide
├── MALDIVES_WEATHER_FACTCHECK_REPORT.md   # [Living Report] Social media fact-check desk
├── requirements.txt                      # Clean Python dependencies
│
├── assets/
│   └── factcheck/                         # Tweet screenshots & verification plots
│       ├── tweet_mohamed_nasheed_october_rainfall.png
│       ├── tweet_fasy_south_north_rainfall.png
│       ├── october_male_rainfall_distribution.png
│       ├── maldives_north_vs_south_rainfall.png
│       └── nakaiy_transitions_rainfall_weather_change.png
│
├── scripts/
│   └── sync_data.py                       # Sync & check updates from maldives-met-weather-dataset
│
├── data/
│   ├── .dataset_version.json              # Version tracking & SHA hash stamp of upstream data
│   │
│   ├── cleaned/                           # Cleaned station records (synced from dataset repo)
│   │   ├── gan.csv                        # Equatorial station (1978–2026, 17,805 records)
│   │   ├── hanimaadhoo.csv                # North station (1991–2026, 12,906 records)
│   │   ├── hulhule.csv                    # Central/Capital station (1975–2026, 18,901 records)
│   │   ├── kaadedhdhoo.csv                # South station (1994–2026, 11,961 records)
│   │   ├── kadhdhoo.csv                   # Central-South station (1990–2026, 13,422 records)
│   │   └── maldives_national_weather_daily.csv  # Unified master national dataset (74,995 records)
│   │
│   └── benchmarks/
│       ├── maldives_sealevel_rise.csv     # UHSLC/IPCC Indian Ocean sea level benchmark (1975–2024)
│       └── monsoon_transition_data.json   # Multi-station synoptic transition benchmark dataset
│
├── archive/                               # Archived development notebooks
│   ├── maldives_weather_data_quality.ipynb
│   └── mindblowing_weather_questions.md
│
├── maldives_weather_exploration.ipynb    # [Notebook 1] Exploration, trends, DTR & SARIMAX
├── maldives_climate_deepdive.ipynb       # [Notebook 2] 5 research hypotheses & Nakaiy mapping
├── maldives_monsoon_transitions.ipynb     # [Notebook 3] Barometric plunge, wind vector reversals & Nakaiy transitions
└── maldives_weather_factcheck.ipynb       # [Notebook 4] Social media & public questions fact-check desk
```

---

## 📜 Data Source & Variables

**Sources:**
- **Meteorological Records:** Sourced from **[maldives-met-weather-dataset](https://github.com/ajmals/maldives-met-weather-dataset)** (original synoptic observations from the [Maldives Meteorological Service](https://www.meteorology.gov.mv/)) — daily station observations, 1975–2026.
- **Nakaiy Calendar:** Digitised from *Hassan Ahmed Maniku (1989)* and dynamically mapped via `scripts/sync_data.py`.
- **Sea Level Rise:** [University of Hawaii Sea Level Center (UHSLC)](https://uhslc.soest.hawaii.edu/) — Hulhule Tide Gauge Station 1475, supplemented with IPCC Indian Ocean estimates (`data/benchmarks/maldives_sealevel_rise.csv`).

**Variables in Synced Cleaned Records (`data/cleaned/`):**
- `date`: ISO-8601 observation date (`YYYY-MM-DD`)
- `rainfall_mm`: Daily 24-hour accumulated precipitation ($mm$)
- `is_trace_rain`: Boolean flag for trace precipitation events ($< 0.1\text{ mm}$)
- `temp_max_c`: Daily maximum air temperature ($^\circ\text{C}$)
- `temp_min_c`: Daily minimum air temperature ($^\circ\text{C}$)
- *Derived in analysis:* `mean_temp_c` ($[T_{max} + T_{min}] / 2$), `dtr_c` ($T_{max} - T_{min}$), and Nakaiy periods.
