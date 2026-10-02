# Monsoon Shift Transition Matrix

A dedicated meteorological modeling and visual analysis package for studying atmospheric pressure drops ($\Delta P$), wind vector streamlines ($U, V$), prevailing wind directional reversals, and extreme rainfall surges during the Maldivian monsoon transition periods (**Assidha** and **Halha**).

---

## 📌 Features & Variables

- **Required Variables**:
  - `Monsoon`: Monsoon Phase (**Iruvai** [Northeast Trade Winds], **Hulhangu** [Southwest Monsoon], and Transition windows).
  - `Nakaiy`: 27 traditional Maldivian Nakaiys (13-day astronomical calendar sectors).
  - `pressure_hpa`: Mean and minimum sea level atmospheric pressure ($P_{\text{hPa}}$).
  - `mean_wind_direction_compass`: 8-sector cardinal wind compass directions (`NE`, `E`, `SE`, `S`, `SW`, `W`, `NW`, `N`) & transition matrices.
  - `rainfall_mm`: Mean ($R_{\text{mean}}$) and 90th percentile extreme daily rainfall intensity ($R_{p90}$).

---

## 📁 Folder Structure

```
monsoon_transition_matrix/
├── README.md                              # Technical documentation
├── data_processor.py                      # Python data engine & JSON exporter
├── create_transition_matrix.py            # Static high-resolution publication plot generator (PNG/PDF)
├── index.html                             # Interactive Web Dashboard Application
├── style.css                              # Modern UI styling (Glassmorphism / Inter & Outfit typography)
├── app.js                                 # Client-side dynamic chart controller (Plotly.js / D3.js)
├── monsoon_transition_data.json           # Aggregated transition data payload
└── output/                                # Generated visual artifacts
    ├── transition_sankey_flow.png
    ├── pressure_rainfall_transition_profile.png
    ├── wind_streamline_vectors.png
    └── monsoon_transition_summary_report.pdf
```

---

## 🔬 Scientific & Meteorological Key Findings

1. **Assidha Transition Window (Iruvai $\rightarrow$ Hulhangu Onset)**:
   - **Atmospheric Pressure Drop**: Sea-level pressure drops from **1011.32 hPa** (in Huvan) to **1009.81 hPa** (in Assidha) and bottoms out at **1009.29 hPa** (in Burunu), registering a maximum transition pressure drop of **2.03 hPa**.
   - **Wind Direction Shift**: Wind direction flips from Easterly trade winds (**81.6%** NE/E in Hiyaviha) to strong Westerlies (**83.6%** W/NW/SW in Burunu).
   - **Rainfall Intensity Surge**: 90th percentile daily rainfall surges to **19.47 mm/day** in Burunu and **28.31 mm/day** in Roanu.

2. **Halha Transition Window (Hulhangu $\rightarrow$ Iruvai Onset)**:
   - **Pressure Recovery**: Sea-level pressure rebounds to **1011.25 hPa** (+1.5 hPa recovery) in Furahalha & Uthurahalha.
   - **Trade Wind Re-establishment**: Easterly trade winds establish rapidly with **77.0%** frequency in Furahalha.
   - **Heavy Onset Rain**: 90th percentile daily rainfall reaches **27.44 mm/day** in Mula.

---

## 🚀 Usage Instructions

### 1. Run Data Processor
To re-process raw observations and export `monsoon_transition_data.json`:
```bash
python3 monsoon_transition_matrix/data_processor.py
```

### 2. Generate Publication Graphics (PNG & PDF)
To render high-resolution static vector plots:
```bash
python3 monsoon_transition_matrix/create_transition_matrix.py
```

### 3. Open Interactive Web Dashboard
Open `monsoon_transition_matrix/index.html` in any browser or launch via local web server:
```bash
python3 -m http.server 8000
```
Navigate to `http://localhost:8000/monsoon_transition_matrix/` to explore interactive Sankey ribbon flow diagrams, polar wind streamline compasses, and pressure drop matrix profiles.

---

## 🌐 Live Demo

The interactive dashboard is publicly hosted on GitHub Pages:

**🔗 [https://ajmals.github.io/met-weather-data-analysis/monsoon_transition_matrix/](https://ajmals.github.io/met-weather-data-analysis/monsoon_transition_matrix/)**
