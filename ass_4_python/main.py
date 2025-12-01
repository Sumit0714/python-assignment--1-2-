"""
weather_visualizer.py
Complete implementation for "Weather Data Visualizer" lab assignment.

Outputs produced (in current working directory):
 - cleaned_weather_data.csv
 - daily_temperature.png
 - monthly_rainfall.png
 - humidity_vs_temp.png
 - combined_plots.png
 - monthly_stats.csv
 - summary.txt

Usage:
 - Put CSV(s) in ./data/ with columns: date, temperature, rainfall, humidity
 - Run: python weather_visualizer.py
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

SAMPLE_CSV = DATA_DIR / "sample_weather.csv"


# -------------------------
# Task 1: Data Acquisition
# -------------------------
def ensure_data_folder():
    DATA_DIR.mkdir(exist_ok=True)


def create_sample_data(path=SAMPLE_CSV, n_days=365, seed=0):
    """Create a realistic-looking sample daily weather CSV for demo/testing."""
    np.random.seed(seed)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=n_days, freq="D")
    # Temperature: seasonality + noise (°C)
    day_of_year = dates.dayofyear.values
    temp = 15 + 10 * np.sin(2 * np.pi * (day_of_year / 365.0)) + np.random.normal(0, 2.5, n_days)
    # Rainfall: more random, with some zeros
    rainfall = np.clip(np.random.gamma(0.8, 2.0, n_days) - 1.2, 0, None)
    # Humidity: roughly inverse to temp plus noise (0-100%)
    humidity = np.clip(70 - (temp - temp.mean()) * 1.5 + np.random.normal(0, 6, n_days), 20, 100)
    df = pd.DataFrame({
        "date": dates,
        "temperature": np.round(temp, 2),
        "rainfall": np.round(rainfall, 2),
        "humidity": np.round(humidity, 1)
    })
    df.to_csv(path, index=False)
    print(f"[i] Sample data created at: {path}")


def load_all_csvs(data_folder=DATA_DIR):
    """Load all CSV files from data_folder and combine into a single DataFrame."""
    csv_files = sorted(data_folder.glob("*.csv"))
    if not csv_files:
        return pd.DataFrame()
    dfs = []
    for f in csv_files:
        try:
            df = pd.read_csv(f)
            df["source_file"] = f.name
            dfs.append(df)
        except Exception as e:
            print(f"[!] Failed to read {f.name}: {e}")
    if not dfs:
        return pd.DataFrame()
    combined = pd.concat(dfs, ignore_index=True)
    return combined


# -------------------------
# Task 2: Cleaning & Prep
# -------------------------
def clean_weather_df(df):
    """Standardize column names, parse dates, handle missing values."""
    if df.empty:
        return df

    # lower-case columns for robustness
    df = df.rename(columns={c: c.strip().lower() for c in df.columns})

    # common column name mappings
    col_map = {}
    for c in df.columns:
        if "date" in c:
            col_map[c] = "date"
        if "temp" in c and "temperature" not in df.columns:
            col_map[c] = "temperature"
        if "rain" in c and "rainfall" not in df.columns:
            col_map[c] = "rainfall"
        if "humid" in c and "humidity" not in df.columns:
            col_map[c] = "humidity"
    df = df.rename(columns=col_map)

    # Ensure required columns exist (temperature, rainfall, humidity)
    for req in ("date", "temperature", "rainfall", "humidity"):
        if req not in df.columns:
            df[req] = np.nan

    # Parse date
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Drop rows with invalid date
    df = df.dropna(subset=["date"])

    # Coerce numeric columns
    for col in ["temperature", "rainfall", "humidity"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fill missing numeric values:
    # - temperature/humidity: use forward/backward fill then mean fallback
    # - rainfall: missing -> 0 (assume no rainfall if missing)
    df["temperature"] = df["temperature"].ffill().bfill().fillna(df["temperature"].mean())
    df["humidity"] = df["humidity"].ffill().bfill().fillna(df["humidity"].mean())
    df["rainfall"] = df["rainfall"].fillna(0)

    # Sort by date
    df = df.sort_values("date").reset_index(drop=True)
    return df


# -------------------------
# Task 3: Statistical Analysis
# -------------------------
def compute_daily_stats(df):
    """Daily stats (if multiple entries per day, aggregate)."""
    df_daily = df.set_index("date").resample("D").agg({
        "temperature": "mean",
        "rainfall": "sum",
        "humidity": "mean"
    })
    df_daily = df_daily.rename(columns={
        "temperature": "temp_mean",
        "rainfall": "rain_total",
        "humidity": "humid_mean"
    })
    return df_daily


def compute_monthly_stats(df_daily):
    """Monthly aggregates (mean temperature, total rainfall, mean humidity)."""
    df_month = df_daily.resample("M").agg({
        "temp_mean": ["mean", "min", "max", "std"],
        "rain_total": ["sum", "mean"],
        "humid_mean": ["mean"]
    })
    # Flatten columns
    df_month.columns = ["_".join([c for c in col if c]) for col in df_month.columns.values]
    return df_month


def compute_yearly_stats(df_daily):
    return df_daily.resample("Y").agg({
        "temp_mean": ["mean", "min", "max"],
        "rain_total": "sum",
        "humid_mean": "mean"
    })


# -------------------------
# Task 4: Visualization
# -------------------------
def plot_daily_temperature(df_daily, out_path=OUTPUT_DIR / "daily_temperature.png"):
    plt.figure(figsize=(12, 4))
    plt.plot(df_daily.index, df_daily["temp_mean"], marker=".", linewidth=1)
    plt.title("Daily Mean Temperature")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"[i] Saved: {out_path}")


def plot_monthly_rainfall(df_month, out_path=OUTPUT_DIR / "monthly_rainfall.png"):
    plt.figure(figsize=(10, 4))
    x = df_month.index
    y = df_month["rain_total_sum"] if "rain_total_sum" in df_month.columns else df_month["rain_total_sum"]
    plt.bar(x, y)
    plt.title("Monthly Total Rainfall")
    plt.xlabel("Month")
    plt.ylabel("Rainfall (mm)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"[i] Saved: {out_path}")


def plot_humidity_vs_temp(df_daily, out_path=OUTPUT_DIR / "humidity_vs_temp.png"):
    plt.figure(figsize=(7, 5))
    plt.scatter(df_daily["temp_mean"], df_daily["humid_mean"], alpha=0.6)
    plt.title("Humidity vs Temperature (Daily)")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Humidity (%)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"[i] Saved: {out_path}")


def plot_combined(df_daily, df_month, out_path=OUTPUT_DIR / "combined_plots.png"):
    fig, axs = plt.subplots(2, 1, figsize=(12, 10))

    # Top: daily temp
    axs[0].plot(df_daily.index, df_daily["temp_mean"], marker=".", linewidth=1)
    axs[0].set_title("Daily Mean Temperature")
    axs[0].set_xlabel("Date")
    axs[0].set_ylabel("°C")
    axs[0].grid(alpha=0.3)

    # Bottom: monthly rainfall
    x = df_month.index
    y = df_month["rain_total_sum"]
    axs[1].bar(x, y)
    axs[1].set_title("Monthly Total Rainfall")
    axs[1].set_xlabel("Month")
    axs[1].set_ylabel("Rainfall (mm)")
    axs[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"[i] Saved: {out_path}")


# -------------------------
# Task 5: Export & Summary
# -------------------------
def export_results(clean_df, df_daily, df_monthly):
    cleaned_path = OUTPUT_DIR / "cleaned_weather_data.csv"
    df_daily.to_csv(OUTPUT_DIR / "daily_aggregated.csv")
    df_monthly.to_csv(OUTPUT_DIR / "monthly_stats.csv")
    clean_df.to_csv(cleaned_path, index=False)
    print(f"[i] Exported cleaned data to: {cleaned_path}")


def write_summary(clean_df, df_daily, df_month):
    total_days = df_daily.shape[0]
    overall_mean_temp = df_daily["temp_mean"].mean()
    total_rain = df_daily["rain_total"].sum()
    max_temp = df_daily["temp_mean"].max()
    max_temp_day = df_daily["temp_mean"].idxmax().strftime("%Y-%m-%d")
    max_rain = df_daily["rain_total"].max()
    max_rain_day = df_daily["rain_total"].idxmax().strftime("%Y-%m-%d")

    # Highest monthly rainfall month
    best_month = df_month["rain_total_sum"].idxmax().strftime("%Y-%m")

    summary_txt = (
        "Weather Data Summary\n"
        "====================\n\n"
        f"Total days analyzed: {total_days}\n"
        f"Overall mean daily temperature: {overall_mean_temp:.2f} °C\n"
        f"Total rainfall (period): {total_rain:.2f} mm\n"
        f"Peak daily temperature: {max_temp:.2f} °C on {max_temp_day}\n"
        f"Peak daily rainfall: {max_rain:.2f} mm on {max_rain_day}\n"
        f"Month with highest rainfall (total): {best_month}\n\n"
        "Notes:\n- Temperature is daily mean computed from available entries.\n- Missing numeric values filled using sensible defaults (forward/backward fill).\n"
    )

    with open(OUTPUT_DIR / "summary.txt", "w") as f:
        f.write(summary_txt)
    print(f"[i] Summary written to: {OUTPUT_DIR / 'summary.txt'}")


# -------------------------
# Main pipeline
# -------------------------
def main():
    ensure_data_folder()

    # If no CSV present, create a sample dataset for demo
    if not any(DATA_DIR.glob("*.csv")):
        create_sample_data()

    # 1) Load CSVs
    raw = load_all_csvs()
    if raw.empty:
        print("[!] No data found. Exiting.")
        return

    # 2) Clean
    clean = clean_weather_df(raw)

    # 3) Daily aggregation
    df_daily = compute_daily_stats(clean)

    # 4) Monthly aggregation
    df_month = compute_monthly_stats(df_daily)

    # Ensure columns exist for plotting
    if "rain_total_sum" not in df_month.columns:
        # compute_monthly_stats produced column names like "rain_total_sum" or similar
        # we assume 'rain_total_sum' means total rainfall per month
        # if not present, try to compute:
        if "rain_total_sum" not in df_month.columns and "rain_total_sum" not in df_month.columns:
            df_month["rain_total_sum"] = df_daily["rain_total"].resample("M").sum()

    # 5) Plotting
    plot_daily_temperature(df_daily)
    plot_monthly_rainfall(df_month)
    plot_humidity_vs_temp(df_daily)
    plot_combined(df_daily, df_month)

    # 6) Export
    export_results(clean, df_daily, df_month)
    write_summary(clean, df_daily, df_month)

    print("[✔] All tasks completed. Check the 'output' folder for results.")


if __name__ == "__main__":
    main()
