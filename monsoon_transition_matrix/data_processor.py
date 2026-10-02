"""
Data Processing Engine for Monsoon Shift Transition Matrix
===========================================================
Processes historical meteorological observations mapped with Maldivian Nakaiy calendars,
deriving wind directional shift transition matrices, atmospheric pressure drop gradients,
wind streamline vector components (U, V), and rainfall intensity profiles across multiple stations
(Hulhule Central, Gan Southern, Hanimaadhoo Northern).
"""

import os
import json
import re
import pandas as pd
import numpy as np

# 27 Nakaiys Reference Definition
NAKAI_DETAILS = [
    {"index": 1, "name": "Mula", "monsoon": "Iruvai", "dates": "Dec 10 - Dec 22", "lore": "Strong winds, rough seas", "is_transition": True, "trans_type": "Halha (Hulhangu->Iruvai)"},
    {"index": 2, "name": "Furahalha", "monsoon": "Iruvai", "dates": "Dec 23 - Jan 05", "lore": "Strong winds, gentle swell", "is_transition": True, "trans_type": "Halha (Hulhangu->Iruvai)"},
    {"index": 3, "name": "Uthurahalha", "monsoon": "Iruvai", "dates": "Jan 06 - Jan 18", "lore": "Clear skies, strong winds", "is_transition": True, "trans_type": "Halha (Hulhangu->Iruvai)"},
    {"index": 4, "name": "Huvan", "monsoon": "Iruvai", "dates": "Jan 19 - Jan 31", "lore": "Calm seas, pleasant sunny days", "is_transition": False, "trans_type": None},
    {"index": 5, "name": "Dhinasha", "monsoon": "Iruvai", "dates": "Feb 01 - Feb 13", "lore": "North-easterly winds, moderate seas", "is_transition": False, "trans_type": None},
    {"index": 6, "name": "Hiyaviha", "monsoon": "Iruvai", "dates": "Feb 14 - Feb 26", "lore": "Calm seas, hot clear days", "is_transition": False, "trans_type": None},
    {"index": 7, "name": "Furabadhuruva", "monsoon": "Iruvai", "dates": "Feb 27 - Mar 11", "lore": "Occasional squalls, moderate wind", "is_transition": False, "trans_type": None},
    {"index": 8, "name": "Fasbadhuruva", "monsoon": "Iruvai", "dates": "Mar 12 - Mar 25", "lore": "Clear skies, light breeze", "is_transition": True, "trans_type": "Pre-Assidha"},
    {"index": 9, "name": "Reyva", "monsoon": "Iruvai", "dates": "Mar 26 - Apr 07", "lore": "Light winds, transition approaching", "is_transition": True, "trans_type": "Pre-Assidha"},
    {"index": 10, "name": "Assidha", "monsoon": "Hulhangu", "dates": "Apr 08 - Apr 21", "lore": "Onset of SW Monsoon, rain & lightning", "is_transition": True, "trans_type": "Assidha Onset (Iruvai->Hulhangu)"},
    {"index": 11, "name": "Burunu", "monsoon": "Hulhangu", "dates": "Apr 22 - May 05", "lore": "Strong winds, stormy rainfall", "is_transition": True, "trans_type": "Assidha Transition"},
    {"index": 12, "name": "Kethi", "monsoon": "Hulhangu", "dates": "May 06 - May 19", "lore": "Continuous dark clouds and rain", "is_transition": False, "trans_type": None},
    {"index": 13, "name": "Roanu", "monsoon": "Hulhangu", "dates": "May 20 - Jun 02", "lore": "Heavy squalls, rough seas", "is_transition": False, "trans_type": None},
    {"index": 14, "name": "Miyahelia", "monsoon": "Hulhangu", "dates": "Jun 03 - Jun 16", "lore": "Rough seas, strong westerly gusts", "is_transition": False, "trans_type": None},
    {"index": 15, "name": "Adha", "monsoon": "Hulhangu", "dates": "Jun 17 - Jun 30", "lore": "Strong winds, heavy rainfall", "is_transition": False, "trans_type": None},
    {"index": 16, "name": "Funoas", "monsoon": "Hulhangu", "dates": "Jul 01 - Jul 14", "lore": "Rough seas, frequent squalls", "is_transition": False, "trans_type": None},
    {"index": 17, "name": "Fus", "monsoon": "Hulhangu", "dates": "Jul 15 - Jul 28", "lore": "Overcast skies, moderate rain", "is_transition": False, "trans_type": None},
    {"index": 18, "name": "Ahulia", "monsoon": "Hulhangu", "dates": "Jul 29 - Aug 10", "lore": "Unsettled weather, gusty winds", "is_transition": False, "trans_type": None},
    {"index": 19, "name": "Maa", "monsoon": "Hulhangu", "dates": "Aug 11 - Aug 23", "lore": "Heavy rain squalls, rough seas", "is_transition": False, "trans_type": None},
    {"index": 20, "name": "Fura", "monsoon": "Hulhangu", "dates": "Aug 24 - Sep 06", "lore": "Frequent showers, moderate wind", "is_transition": False, "trans_type": None},
    {"index": 21, "name": "Uthura", "monsoon": "Hulhangu", "dates": "Sep 07 - Sep 20", "lore": "Strong gusts, heavy rain bursts", "is_transition": False, "trans_type": None},
    {"index": 22, "name": "Atha", "monsoon": "Hulhangu", "dates": "Sep 21 - Oct 03", "lore": "Calmer intervals, isolated rain", "is_transition": False, "trans_type": None},
    {"index": 23, "name": "Hitha", "monsoon": "Hulhangu", "dates": "Oct 04 - Oct 17", "lore": "Light winds, scattered rainfall", "is_transition": False, "trans_type": None},
    {"index": 24, "name": "Hei", "monsoon": "Hulhangu", "dates": "Oct 18 - Oct 31", "lore": "Strong winds, dark squall clouds", "is_transition": False, "trans_type": None},
    {"index": 25, "name": "Viha", "monsoon": "Hulhangu", "dates": "Nov 01 - Nov 13", "lore": "Calm seas, transition preparing", "is_transition": True, "trans_type": "Pre-Halha"},
    {"index": 26, "name": "Nora", "monsoon": "Hulhangu", "dates": "Nov 14 - Nov 26", "lore": "Unsteady breezes, light rain", "is_transition": True, "trans_type": "Pre-Halha"},
    {"index": 27, "name": "Dosha", "monsoon": "Hulhangu", "dates": "Nov 27 - Dec 09", "lore": "Transition to Iruvai, north-easterly winds", "is_transition": True, "trans_type": "Halha Onset (Hulhangu->Iruvai)"}
]

# Compass Direction Mapping & Angles
COMPASS_ANGLES = {
    'N': 0.0, 'NNE': 22.5, 'NE': 45.0, 'ENE': 67.5,
    'E': 90.0, 'ESE': 112.5, 'SE': 135.0, 'SSE': 157.5,
    'S': 180.0, 'SSW': 202.5, 'SW': 225.0, 'WSW': 247.5,
    'W': 270.0, 'WNW': 292.5, 'NW': 315.0, 'NNW': 337.5,
    'CALM': None, 'VRB': None
}

SECTOR_8_MAP = {
    'N': 'N', 'NNE': 'NE', 'NE': 'NE', 'ENE': 'E',
    'E': 'E', 'ESE': 'SE', 'SE': 'SE', 'SSE': 'S',
    'S': 'S', 'SSW': 'SW', 'SW': 'SW', 'WSW': 'W',
    'W': 'W', 'WNW': 'NW', 'NW': 'NW', 'NNW': 'N',
    'CALM': 'CALM', 'VRB': 'VRB'
}


def clean_wind_direction(val):
    if pd.isna(val):
        return 'VRB'
    s = str(val).strip().upper()
    s = s.split(',')[0].split("'")[-1].strip()
    return SECTOR_8_MAP.get(s, 'VRB')


def compass_to_angle(compass):
    if pd.isna(compass):
        return None
    s = str(compass).strip().upper().split(',')[0].split("'")[-1].strip()
    return COMPASS_ANGLES.get(s, None)


def compute_vector_components(speed, compass):
    """
    Computes U (East-West) and V (North-South) wind vector components.
    Meteorological convention: direction is WHERE wind comes FROM.
    U = - speed * sin(deg)
    V = - speed * cos(deg)
    """
    angle_deg = compass_to_angle(compass)
    if angle_deg is None or pd.isna(speed):
        return 0.0, 0.0
    rad = np.radians(angle_deg)
    u = - speed * np.sin(rad)
    v = - speed * np.cos(rad)
    return round(float(u), 3), round(float(v), 3)


def resolve_file_path(rel_path):
    if os.path.exists(rel_path):
        return rel_path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    alt_path = os.path.join(script_dir, "..", rel_path)
    if os.path.exists(alt_path):
        return alt_path
    raise FileNotFoundError(f"File not found: {rel_path} or {alt_path}")


def build_calendar_day_map():
    mapped_csv = resolve_file_path("data/hulhule_nakai_mapped.csv")
    df_nak = pd.read_csv(mapped_csv)
    df_nak["dt"] = pd.to_datetime(df_nak["parsed_date"])
    df_nak["md"] = df_nak["dt"].dt.strftime("%m-%d")
    day_map = df_nak.groupby("md")[["Nakaiy", "Nakaiy_Index", "Monsoon"]].first().to_dict(orient="index")
    return day_map


def process_station_dataframe(df, station_name):
    """
    Processes a station DataFrame that contains 'date', 'pressure_hpa', 'rainfall_mm',
    'mean_wind_speed_kts', 'mean_wind_direction_compass', 'Nakaiy', 'Nakaiy_Index', 'Monsoon'.
    """
    df['clean_wind_sector'] = df['mean_wind_direction_compass'].apply(clean_wind_direction)
    df['wind_angle_deg'] = df['mean_wind_direction_compass'].apply(compass_to_angle)

    # Calculate U, V vector components
    u_v = [compute_vector_components(spd, dir_c) for spd, dir_c in zip(df['mean_wind_speed_kts'], df['mean_wind_direction_compass'])]
    df['u_kts'] = [x[0] for x in u_v]
    df['v_kts'] = [x[1] for x in u_v]

    summary_list = []
    baseline_pressure = df['pressure_hpa'].dropna().mean()

    for item in NAKAI_DETAILS:
        idx = item['index']
        name = item['name']
        sub = df[df['Nakaiy_Index'] == idx] if 'Nakaiy_Index' in df.columns else df[df['Nakaiy'] == name]

        if len(sub) == 0:
            continue

        mean_press = sub['pressure_hpa'].dropna().mean()
        min_press = sub['pressure_hpa'].dropna().min()
        mean_rain = sub['rainfall_mm'].dropna().mean()
        p90_rain = sub['rainfall_mm'].dropna().quantile(0.90)
        max_rain = sub['rainfall_mm'].dropna().max()
        mean_wind_spd = sub['mean_wind_speed_kts'].dropna().mean()
        max_wind_spd = sub['max_wind_speed_kts'].dropna().mean() if 'max_wind_speed_kts' in sub.columns else mean_wind_spd
        u_mean = sub['u_kts'].dropna().mean()
        v_mean = sub['v_kts'].dropna().mean()

        # Dominant wind sector
        sector_counts = sub['clean_wind_sector'].value_counts()
        top_sector = sector_counts.index[0] if len(sector_counts) > 0 else 'VRB'
        top_sector_pct = (sector_counts.iloc[0] / len(sub)) * 100.0 if len(sector_counts) > 0 else 0.0

        # Wind direction distributions (%)
        all_sectors = ['NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N', 'CALM', 'VRB']
        sector_dist = {sec: round(float((sub['clean_wind_sector'] == sec).mean() * 100.0), 2) for sec in all_sectors}

        summary_list.append({
            'index': idx,
            'name': name,
            'monsoon': item['monsoon'],
            'dates': item['dates'],
            'lore': item['lore'],
            'is_transition': item['is_transition'],
            'trans_type': item['trans_type'],
            'mean_pressure_hpa': round(float(mean_press), 2) if not pd.isna(mean_press) else 1010.0,
            'min_pressure_hpa': round(float(min_press), 2) if not pd.isna(min_press) else 1009.0,
            'pressure_anomaly_hpa': round(float(mean_press - baseline_pressure), 2) if not pd.isna(mean_press) else 0.0,
            'mean_rain_mm': round(float(mean_rain), 2) if not pd.isna(mean_rain) else 0.0,
            'p90_rain_mm': round(float(p90_rain), 2) if not pd.isna(p90_rain) else 0.0,
            'max_rain_mm': round(float(max_rain), 2) if not pd.isna(max_rain) else 0.0,
            'mean_wind_speed_kts': round(float(mean_wind_spd), 2) if not pd.isna(mean_wind_spd) else 0.0,
            'max_wind_speed_kts': round(float(max_wind_spd), 2) if not pd.isna(max_wind_spd) else 0.0,
            'u_mean_kts': round(float(u_mean), 2) if not pd.isna(u_mean) else 0.0,
            'v_mean_kts': round(float(v_mean), 2) if not pd.isna(v_mean) else 0.0,
            'dominant_sector': top_sector,
            'dominant_sector_pct': round(float(top_sector_pct), 1),
            'sector_dist_pct': sector_dist,
            'obs_count': int(len(sub))
        })

    summary_df = pd.DataFrame(summary_list)
    # Calculate pressure drop delta relative to previous Nakaiy (positive means drop)
    summary_df['pressure_drop_hpa'] = round(- summary_df['mean_pressure_hpa'].diff().fillna(0.0), 2)

    # Convert all records to dicts so pressure_drop_hpa is present on every item
    all_nakaiy_records = summary_df.to_dict(orient="records")

    # Transition Phase 1: Assidha (Iruvai -> Hulhangu) Analysis
    t1_nakaiys = ['Furabadhuruva', 'Fasbadhuruva', 'Reyva', 'Assidha', 'Burunu', 'Kethi']
    t1_summary = [s for s in all_nakaiy_records if s['name'] in t1_nakaiys]

    # Transition Phase 2: Halha (Hulhangu -> Iruvai) Analysis
    t2_nakaiys = ['Hei', 'Viha', 'Nora', 'Dosha', 'Mula', 'Furahalha', 'Uthurahalha']
    t2_summary = [s for s in all_nakaiy_records if s['name'] in t2_nakaiys]

    # Sankey Flow Link Generation
    sectors = ['NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N', 'VRB/CALM']

    # Sankey Links for Assidha Transition
    sankey_links_t1 = []
    t1_pre = df[df['Nakaiy'].isin(['Hiyaviha', 'Furabadhuruva', 'Fasbadhuruva', 'Reyva'])]
    t1_onset = df[df['Nakaiy'] == 'Assidha']
    t1_post = df[df['Nakaiy'].isin(['Burunu', 'Kethi', 'Roanu'])]

    for sec in sectors:
        sec_filter = sec if sec != 'VRB/CALM' else ['VRB', 'CALM']
        if isinstance(sec_filter, list):
            c_pre = len(t1_pre[t1_pre['clean_wind_sector'].isin(sec_filter)])
            c_onset = len(t1_onset[t1_onset['clean_wind_sector'].isin(sec_filter)])
            c_post = len(t1_post[t1_post['clean_wind_sector'].isin(sec_filter)])
        else:
            c_pre = len(t1_pre[t1_pre['clean_wind_sector'] == sec_filter])
            c_onset = len(t1_onset[t1_onset['clean_wind_sector'] == sec_filter])
            c_post = len(t1_post[t1_post['clean_wind_sector'] == sec_filter])

        if c_pre > 0:
            sankey_links_t1.append({"source": "Late Iruvai (Pre-Assidha)", "target": f"Wind Sector: {sec}", "value": c_pre, "phase": "Pre-Onset"})
        if c_onset > 0:
            sankey_links_t1.append({"source": f"Wind Sector: {sec}", "target": "Assidha Onset (SW Onset)", "value": c_onset, "phase": "Onset"})
        if c_post > 0:
            sankey_links_t1.append({"source": "Assidha Onset (SW Onset)", "target": f"Post-Assidha Sector: {sec}", "value": c_post, "phase": "Established Hulhangu"})

    # Sankey Links for Halha Transition
    sankey_links_t2 = []
    t2_pre = df[df['Nakaiy'].isin(['Viha', 'Nora', 'Dosha'])]
    t2_onset = df[df['Nakaiy'].isin(['Mula', 'Furahalha', 'Uthurahalha'])]
    t2_post = df[df['Nakaiy'].isin(['Huvan', 'Dhinasha'])]

    for sec in sectors:
        sec_filter = sec if sec != 'VRB/CALM' else ['VRB', 'CALM']
        if isinstance(sec_filter, list):
            c_pre = len(t2_pre[t2_pre['clean_wind_sector'].isin(sec_filter)])
            c_onset = len(t2_onset[t2_onset['clean_wind_sector'].isin(sec_filter)])
            c_post = len(t2_post[t2_post['clean_wind_sector'].isin(sec_filter)])
        else:
            c_pre = len(t2_pre[t2_pre['clean_wind_sector'] == sec_filter])
            c_onset = len(t2_onset[t2_onset['clean_wind_sector'] == sec_filter])
            c_post = len(t2_post[t2_post['clean_wind_sector'] == sec_filter])

        if c_pre > 0:
            sankey_links_t2.append({"source": "Late Hulhangu (Pre-Halha)", "target": f"Wind Sector: {sec}", "value": c_pre, "phase": "Pre-Onset"})
        if c_onset > 0:
            sankey_links_t2.append({"source": f"Wind Sector: {sec}", "target": "Halha Onset (NE Onset)", "value": c_onset, "phase": "Onset"})
        if c_post > 0:
            sankey_links_t2.append({"source": "Halha Onset (NE Onset)", "target": f"Post-Halha Sector: {sec}", "value": c_post, "phase": "Established Iruvai"})

    # Key Transition Metrics Summary
    assidha_row = summary_df[summary_df['name'] == 'Assidha'].iloc[0].to_dict()
    burunu_row = summary_df[summary_df['name'] == 'Burunu'].iloc[0].to_dict()
    mula_row = summary_df[summary_df['name'] == 'Mula'].iloc[0].to_dict()
    furahalha_row = summary_df[summary_df['name'] == 'Furahalha'].iloc[0].to_dict()
    huvan_press = summary_df[summary_df['name'] == 'Huvan']['mean_pressure_hpa'].values[0]

    key_stats = {
        "assidha_pressure_hpa": assidha_row['mean_pressure_hpa'],
        "assidha_pressure_drop_from_iruvai": round(float(huvan_press - assidha_row['mean_pressure_hpa']), 2),
        "burunu_min_pressure_hpa": burunu_row['mean_pressure_hpa'],
        "max_transition_pressure_drop_hpa": round(float(huvan_press - burunu_row['mean_pressure_hpa']), 2),
        "assidha_rain_p90_mm": assidha_row['p90_rain_mm'],
        "burunu_rain_p90_mm": burunu_row['p90_rain_mm'],
        "halha_mula_rain_p90_mm": mula_row['p90_rain_mm'],
        "halha_furahalha_pressure_hpa": furahalha_row['mean_pressure_hpa'],
        "iruvai_easterly_shift_pct": round(float(furahalha_row['sector_dist_pct']['E'] + furahalha_row['sector_dist_pct']['NE']), 1),
        "hulhangu_westerly_shift_pct": round(float(burunu_row['sector_dist_pct']['W'] + burunu_row['sector_dist_pct']['NW'] + burunu_row['sector_dist_pct']['SW']), 1)
    }

    return {
        "station_name": station_name,
        "nakaiy_summary": all_nakaiy_records,
        "transition_1_assidha": t1_summary,
        "transition_2_halha": t2_summary,
        "sankey_t1": sankey_links_t1,
        "sankey_t2": sankey_links_t2,
        "key_stats": key_stats
    }


def load_and_process_transition_matrix():
    day_map = build_calendar_day_map()

    stations_cfg = {
        "hulhule": {
            "file": "data/hulhule_nakai_mapped.csv",
            "name": "Hulhule International Airport (Central)",
            "is_mapped": True
        },
        "gan": {
            "file": "data/gan_cleaned_data.csv",
            "name": "Gan International Airport (Southern)",
            "is_mapped": False
        },
        "hanimaadhoo": {
            "file": "data/hanimaadhoo_cleaned_data.csv",
            "name": "Hanimaadhoo Climate Station (Northern)",
            "is_mapped": False
        }
    }

    station_results = {}

    for key, cfg in stations_cfg.items():
        file_path = resolve_file_path(cfg["file"])
        df = pd.read_csv(file_path)
        if not cfg["is_mapped"]:
            df["parsed_date"] = pd.to_datetime(df["date"])
            df["md"] = df["parsed_date"].dt.strftime("%m-%d")
            df["Nakaiy"] = df["md"].map(lambda x: day_map[x]["Nakaiy"])
            df["Nakaiy_Index"] = df["md"].map(lambda x: day_map[x]["Nakaiy_Index"])
            df["Monsoon"] = df["md"].map(lambda x: day_map[x]["Monsoon"])
        else:
            df["parsed_date"] = pd.to_datetime(df["parsed_date"])

        station_results[key] = process_station_dataframe(df, cfg["name"])

    # Base payload on Hulhule for backwards compatibility, with multi-station dictionary
    base = dict(station_results["hulhule"])
    base["stations"] = station_results
    return base


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_json = os.path.join(script_dir, "monsoon_transition_data.json")

    data = load_and_process_transition_matrix()
    json_str = json.dumps(data, indent=2)
    json_str = re.sub(r':\s*NaN\b', ': null', json_str)
    with open(output_json, "w") as f:
        f.write(json_str)

    print("Successfully processed monsoon transition matrix data for all 3 stations!")
    print(f"Stations included: {list(data['stations'].keys())}")
    print(f"JSON export written to: {output_json}")
    print(f"Hulhule Key stats: {data['key_stats']}")
