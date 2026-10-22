#!/usr/bin/env python3
"""
scripts/sync_data.py
--------------------
Manages synchronization and update tracking between met-weather-analysis and
the upstream dataset repository: https://github.com/ajmals/maldives-met-weather-dataset

Features:
  - Check for new upstream data updates on GitHub or local sibling repo
  - Synchronize latest cleaned CSV datasets into data/cleaned/
  - Display detailed status and notifications
  - Helper functions for notebooks to load station data and dynamically map Nakaiy periods
"""

import os
import sys
import json
import hashlib
import urllib.request
import urllib.error
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CLEANED_DIR = os.path.join(DATA_DIR, "cleaned")
VERSION_FILE = os.path.join(DATA_DIR, ".dataset_version.json")

GITHUB_OWNER = "ajmals"
GITHUB_REPO = "maldives-met-weather-dataset"
GITHUB_API_COMMITS = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/commits?path=data/cleaned&page=1&per_page=1"
GITHUB_RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_OWNER}/{GITHUB_REPO}/main/data/cleaned"

DATA_FILES = [
    "gan.csv",
    "hanimaadhoo.csv",
    "hulhule.csv",
    "kaadedhdhoo.csv",
    "kadhdhoo.csv",
    "maldives_national_weather_daily.csv"
]

# Traditional 27 Nakaiys Reference Definition (Hassan Ahmed Maniku, 1989)
NAKAI_PERIODS = [
    (1, "Mula", "Iruvai", (12, 10), (12, 22)),
    (2, "Furahalha", "Iruvai", (12, 23), (1, 5)),
    (3, "Uthurahalha", "Iruvai", (1, 6), (1, 18)),
    (4, "Huvan", "Iruvai", (1, 19), (1, 31)),
    (5, "Dhinasha", "Iruvai", (2, 1), (2, 13)),
    (6, "Hiyaviha", "Iruvai", (2, 14), (2, 26)),
    (7, "Furabadhuruva", "Iruvai", (2, 27), (3, 11)),
    (8, "Fasbadhuruva", "Iruvai", (3, 12), (3, 25)),
    (9, "Reyva", "Iruvai", (3, 26), (4, 7)),
    (10, "Assidha", "Hulhangu", (4, 8), (4, 21)),
    (11, "Burunu", "Hulhangu", (4, 22), (5, 5)),
    (12, "Kethi", "Hulhangu", (5, 6), (5, 19)),
    (13, "Roanu", "Hulhangu", (5, 20), (6, 2)),
    (14, "Miyahelia", "Hulhangu", (6, 3), (6, 16)),
    (15, "Adha", "Hulhangu", (6, 17), (6, 30)),
    (16, "Funoas", "Hulhangu", (7, 1), (7, 14)),
    (17, "Fus", "Hulhangu", (7, 15), (7, 28)),
    (18, "Ahulia", "Hulhangu", (7, 29), (8, 10)),
    (19, "Maa", "Hulhangu", (8, 11), (8, 23)),
    (20, "Fura", "Hulhangu", (8, 24), (9, 6)),
    (21, "Uthura", "Hulhangu", (9, 7), (9, 20)),
    (22, "Atha", "Hulhangu", (9, 21), (10, 3)),
    (23, "Hitha", "Hulhangu", (10, 4), (10, 17)),
    (24, "Hei", "Hulhangu", (10, 18), (10, 31)),
    (25, "Viha", "Hulhangu", (11, 1), (11, 13)),
    (26, "Nora", "Hulhangu", (11, 14), (11, 26)),
    (27, "Dosha", "Hulhangu", (11, 27), (12, 9)),
]


def compute_file_sha256(filepath):
    if not os.path.exists(filepath):
        return None
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()


def count_file_rows(filepath):
    if not os.path.exists(filepath):
        return 0
    count = 0
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for _ in f:
            count += 1
    return count


def load_version_metadata():
    if os.path.exists(VERSION_FILE):
        try:
            with open(VERSION_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "repo": f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}",
        "last_synced_commit": None,
        "last_synced_date": None,
        "last_checked_date": None,
        "files": {}
    }


def save_version_metadata(meta):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(VERSION_FILE, "w") as f:
        json.dump(meta, f, indent=2)


def get_local_sibling_repo():
    candidates = [
        os.path.join(os.path.dirname(BASE_DIR), GITHUB_REPO),
        os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), GITHUB_REPO),
        f"/Users/ajmal/Documents/Projects/{GITHUB_REPO}"
    ]
    for path in candidates:
        if os.path.exists(os.path.join(path, "data", "cleaned")):
            return path
    return None


def fetch_latest_upstream_commit():
    """Fetches latest commit info touching data/cleaned from GitHub API or local git."""
    # 1. Try local sibling repo first if available
    local_repo = get_local_sibling_repo()
    local_commit = None
    if local_repo and os.path.exists(os.path.join(local_repo, ".git")):
        try:
            import subprocess
            out = subprocess.check_output(
                ["git", "log", "-n", "1", "--format=%H|%cI|%s", "--", "data/cleaned"],
                cwd=local_repo,
                stderr=subprocess.DEVNULL
            ).decode().strip()
            if out:
                sha, date_str, msg = out.split("|", 2)
                local_commit = {
                    "sha": sha,
                    "date": date_str,
                    "message": msg,
                    "source": "local_repo",
                    "repo_path": local_repo
                }
        except Exception:
            pass

    # 2. Query GitHub API
    req = urllib.request.Request(
        GITHUB_API_COMMITS,
        headers={"User-Agent": "met-weather-analysis-updater"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            if data and len(data) > 0:
                remote_commit = data[0]
                return {
                    "sha": remote_commit["sha"],
                    "date": remote_commit["commit"]["committer"]["date"],
                    "message": remote_commit["commit"]["message"].split("\n")[0],
                    "source": "github_api"
                }
    except Exception as e:
        if local_commit:
            return local_commit
        return {"error": f"Failed to check GitHub API: {str(e)}"}

    if local_commit:
        return local_commit
    return {"error": "Could not determine upstream commit"}


def check_dataset_update(notify=False):
    """
    Checks if upstream maldives-met-weather-dataset has new data.
    Returns: dict(update_available=bool, ...)
    """
    meta = load_version_metadata()
    current_commit = meta.get("last_synced_commit")
    upstream = fetch_latest_upstream_commit()

    if "error" in upstream:
        if notify:
            print(f"[Dataset Sync] Note: {upstream['error']} (using cached local data)")
        return {"update_available": False, "error": upstream["error"]}

    latest_sha = upstream.get("sha")
    latest_date = upstream.get("date")
    latest_msg = upstream.get("message")

    meta["last_checked_date"] = datetime.now().isoformat()
    save_version_metadata(meta)

    # Check if commit differs or if any file is missing
    missing_files = [f for f in DATA_FILES if not os.path.exists(os.path.join(CLEANED_DIR, f))]
    has_update = (current_commit != latest_sha) or (len(missing_files) > 0)

    result = {
        "update_available": has_update,
        "current_commit": current_commit[:7] if current_commit else "None",
        "latest_commit": latest_sha[:7] if latest_sha else "Unknown",
        "latest_date": latest_date,
        "message": latest_msg,
        "missing_files": missing_files
    }

    if notify:
        if has_update:
            print("\n" + "=" * 68)
            print("🔔 NEW DATASET UPDATE AVAILABLE!")
            print(f"   Repository : https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}")
            print(f"   Current    : {result['current_commit']}")
            print(f"   Latest     : {result['latest_commit']} ({latest_date})")
            print(f"   Note       : {latest_msg}")
            if missing_files:
                print(f"   Missing    : {', '.join(missing_files)}")
            print("   👉 Run 'python scripts/sync_data.py --sync' to update.")
            print("=" * 68 + "\n")
        else:
            print(f"[Dataset Sync] ✅ Dataset is up-to-date with upstream (Commit: {result['latest_commit']})")

    return result


def sync_dataset():
    """Downloads or copies latest cleaned datasets from upstream repo."""
    os.makedirs(CLEANED_DIR, exist_ok=True)
    meta = load_version_metadata()
    upstream = fetch_latest_upstream_commit()

    local_repo = get_local_sibling_repo()
    used_source = "local" if local_repo else "github"

    print("=" * 68)
    print("🔄 Synchronizing dataset from maldives-met-weather-dataset...")
    if local_repo:
        print(f"   Source: Local sibling repo ({local_repo})")
    else:
        print(f"   Source: GitHub ({GITHUB_RAW_BASE})")

    synced_files = {}

    for filename in DATA_FILES:
        target_path = os.path.join(CLEANED_DIR, filename)

        if local_repo:
            source_path = os.path.join(local_repo, "data", "cleaned", filename)
            if os.path.exists(source_path):
                with open(source_path, "rb") as sf, open(target_path, "wb") as tf:
                    tf.write(sf.read())
            else:
                print(f"   Warning: {source_path} not found locally, falling back to GitHub...")
                download_from_github(filename, target_path)
        else:
            download_from_github(filename, target_path)

        rows = count_file_rows(target_path) - 1 # exclude header
        sha = compute_file_sha256(target_path)
        synced_files[filename] = {"rows": max(0, rows), "sha256": sha}
        print(f"   ✓ {filename:<36} : {rows:,} daily records")

    meta["last_synced_commit"] = upstream.get("sha") if "error" not in upstream else "synced_local"
    meta["last_synced_date"] = datetime.now().isoformat()
    meta["last_checked_date"] = datetime.now().isoformat()
    meta["files"] = synced_files
    save_version_metadata(meta)

    print("\n✅ Synchronization complete!")
    print(f"   Synced at : {meta['last_synced_date']}")
    print(f"   Commit    : {meta['last_synced_commit'][:7] if meta['last_synced_commit'] else 'local'}")
    print("=" * 68)


def download_from_github(filename, target_path):
    url = f"{GITHUB_RAW_BASE}/{filename}"
    req = urllib.request.Request(url, headers={"User-Agent": "met-weather-analysis-updater"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        with open(target_path, "wb") as f:
            f.write(resp.read())


def print_status():
    meta = load_version_metadata()
    print("=" * 68)
    print("📊 DATASET STATUS IN MET-WEATHER-ANALYSIS")
    print("=" * 68)
    print(f"Upstream Repo   : {meta.get('repo')}")
    print(f"Synced Commit   : {meta.get('last_synced_commit', 'None')}")
    print(f"Last Synced     : {meta.get('last_synced_date', 'Never')}")
    print(f"Last Checked    : {meta.get('last_checked_date', 'Never')}")
    print("\nLocal Cleaned Files (data/cleaned/):")
    total_records = 0
    for filename in DATA_FILES:
        path = os.path.join(CLEANED_DIR, filename)
        if os.path.exists(path):
            rows = count_file_rows(path) - 1
            if filename != "maldives_national_weather_daily.csv":
                total_records += max(0, rows)
            print(f"  • {filename:<36} : {rows:,} rows")
        else:
            print(f"  • {filename:<36} : [MISSING]")
    print(f"\nTotal Station Daily Records : {total_records:,}")
    print("=" * 68)


# ---------------------------------------------------------------------------
# Data Loading & Nakaiy Calendar Helper Utilities for Notebooks & Scripts
# ---------------------------------------------------------------------------

def get_nakaiy(month, day):
    """Maps month and day integers to (Nakaiy_Index, Nakaiy_Name, Monsoon)."""
    for idx, name, monsoon, (sm, sd), (em, ed) in NAKAI_PERIODS:
        if sm == em:
            if sm == month and sd <= day <= ed:
                return idx, name, monsoon
        else:
            if (month == sm and day >= sd) or (month == em and day <= ed):
                return idx, name, monsoon
    return None, None, None


def map_nakaiy(df, date_col="date"):
    """
    Appends 'Nakaiy_Index', 'Nakaiy', and 'Monsoon' columns to a DataFrame.
    """
    import pandas as pd
    df = df.copy()
    dt = pd.to_datetime(df[date_col])
    indices = []
    names = []
    monsoons = []
    for d in dt:
        idx, name, mon = get_nakaiy(d.month, d.day)
        indices.append(idx)
        names.append(name)
        monsoons.append(mon)
    df["Nakaiy_Index"] = indices
    df["Nakaiy"] = names
    df["Monsoon"] = monsoons
    return df


def load_station(station_name, with_nakaiy=False):
    """
    Loads a station CSV from data/cleaned/ and standardizes columns:
      - parses 'date' into datetime64
      - computes derived 'mean_temp_c' = (temp_max_c + temp_min_c) / 2
      - computes 'dtr_c' (diurnal temperature range) = temp_max_c - temp_min_c
    """
    import pandas as pd
    filename = f"{station_name.lower().strip()}.csv"
    filepath = os.path.join(CLEANED_DIR, filename)
    if not os.path.exists(filepath):
        # Auto-sync if file is missing
        print(f"File {filepath} not found. Attempting auto-sync from upstream...")
        sync_dataset()
    df = pd.read_csv(filepath)
    df["date"] = pd.to_datetime(df["date"])
    df["mean_temp_c"] = (df["temp_max_c"] + df["temp_min_c"]) / 2.0
    df["dtr_c"] = df["temp_max_c"] - df["temp_min_c"]
    if with_nakaiy:
        df = map_nakaiy(df, "date")
    return df


def load_national_dataset(with_nakaiy=False):
    """Loads the unified 5-station dataset data/cleaned/maldives_national_weather_daily.csv."""
    import pandas as pd
    filepath = os.path.join(CLEANED_DIR, "maldives_national_weather_daily.csv")
    if not os.path.exists(filepath):
        sync_dataset()
    df = pd.read_csv(filepath)
    df["date"] = pd.to_datetime(df["date"])
    df["mean_temp_c"] = (df["temp_max_c"] + df["temp_min_c"]) / 2.0
    df["dtr_c"] = df["temp_max_c"] - df["temp_min_c"]
    if with_nakaiy:
        df = map_nakaiy(df, "date")
    return df


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--sync" in args or "-s" in args:
        sync_dataset()
    elif "--check" in args or "-c" in args:
        check_dataset_update(notify=True)
    elif "--status" in args:
        print_status()
    else:
        # Default behavior: run status and check
        print_status()
        print()
        check_dataset_update(notify=True)
