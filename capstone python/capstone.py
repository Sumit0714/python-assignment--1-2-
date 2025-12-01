import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt



class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, reading: MeterReading):
        self.meter_readings.append(reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)

    def generate_report(self):
        total = self.calculate_total_consumption()
        return f"Building: {self.name}, Total Consumption: {total:.2f} kWh"


class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def add_reading(self, building_name, reading: MeterReading):
        if building_name not in self.buildings:
            self.buildings[building_name] = Building(building_name)
        self.buildings[building_name].add_reading(reading)

    def get_buildings(self):
        return self.buildings.values()

    def generate_all_reports(self):
        return [b.generate_report() for b in self.get_buildings()]





def load_energy_data(data_folder="data"):
    folder = Path(data_folder)
    all_files = list(folder.glob("*.csv"))

    if not all_files:
        print("⚠ No CSV files found in /data/")
        return pd.DataFrame()

    df_list = []

    for file in all_files:
        try:
            df = pd.read_csv(file, on_bad_lines='skip')
            df['building'] = file.stem
            df_list.append(df)
        except Exception as e:
            print(f"⚠ Error reading {file}: {e}")

    if not df_list:
        return pd.DataFrame()

    df_combined = pd.concat(df_list, ignore_index=True)

    df_combined['timestamp'] = pd.to_datetime(df_combined['timestamp'], errors='coerce')
    df_combined = df_combined.dropna(subset=['timestamp', 'kwh'])

    return df_combined



def calculate_daily_totals(df):
    return df.resample('D', on='timestamp').kwh.sum()


def calculate_weekly_aggregates(df):
    return df.resample('W', on='timestamp').kwh.sum()


def building_wise_summary(df):
    return df.groupby("building")['kwh'].agg(['mean', 'min', 'max', 'sum'])




def create_dashboard(df, daily, weekly, output_file="dashboard.png"):
    fig, axs = plt.subplots(3, 1, figsize=(12, 14))

    # Line Chart — Daily Trend
    axs[0].plot(daily.index, daily.values, marker='o')
    axs[0].set_title("Daily Electricity Consumption (Campus Total)")
    axs[0].set_xlabel("Date")
    axs[0].set_ylabel("kWh")

    # Bar Chart — Weekly Totals
    axs[1].bar(weekly.index, weekly.values)
    axs[1].set_title("Weekly Electricity Usage")
    axs[1].set_xlabel("Week")
    axs[1].set_ylabel("kWh")

    # Scatter Plot — Building Peaks
    peak_df = df.groupby("building")['kwh'].max()
    axs[2].scatter(peak_df.index, peak_df.values)
    axs[2].set_title("Peak Load per Building")
    axs[2].set_xlabel("Building")
    axs[2].set_ylabel("Peak kWh")

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()



def save_outputs(df, summary_df):
    df.to_csv("cleaned_energy_data.csv", index=False)
    summary_df.to_csv("building_summary.csv")

    total_consumption = df['kwh'].sum()
    highest_building = summary_df['sum'].idxmax()
    peak_load = df['kwh'].max()

    with open("summary.txt", "w") as f:
        f.write(
            "Campus Energy Consumption Summary\n"
            "------------------------------------------\n"
            f"Total Campus Consumption: {total_consumption:.2f} kWh\n"
            f"Highest Consuming Building: {highest_building}\n"
            f"Peak Load Recorded: {peak_load:.2f} kWh\n"
        )



def main():
    print(" Loading Data...")
    df = load_energy_data()

    if df.empty:
        print(" No data to process. Exiting.")
        return

    print("Performing Aggregations...")
    daily = calculate_daily_totals(df)
    weekly = calculate_weekly_aggregates(df)
    summary = building_wise_summary(df)

    print("🧱 Building OOP Models...")
    manager = BuildingManager()
    for _, row in df.iterrows():
        manager.add_reading(row['building'], MeterReading(row['timestamp'], row['kwh']))

    print(" Creating Dashboard...")
    create_dashboard(df, daily, weekly)

    print(" Saving Outputs...")
    save_outputs(df, summary)

    print(" Capstone Project Completed!")
    print(" Files generated:\n - dashboard.png\n - cleaned_energy_data.csv\n - building_summary.csv\n - summary.txt")


if __name__ == "__main__":
    main()
