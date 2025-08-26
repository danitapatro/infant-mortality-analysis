"""
Infant Mortality Analysis
=========================

This script fetches infant mortality data from the World Health Organization (WHO) API 
and combines it with Our World in Data (OWID) datasets. 

Steps performed:
1. Fetch WHO infant mortality data via API and save locally.
2. Load OWID infant mortality dataset from CSV.
3. Clean and merge the datasets:
   - Standardize columns
   - Add country codes/names
   - Handle missing values and duplicates
   - Restrict years to 2000–2024
4. Save the combined dataset as CSV.
5. Generate key visualizations:
   - Global trend of infant mortality rate
   - WHO vs OWID comparison
   - Decade-wise averages
   - Top 10 and Bottom 10 countries by infant mortality (latest year)
6. Save visualizations to the `plots/` folder.

Usage:
------
Run from terminal/anaconda prompt:
    python Infant_Mortality_Analysis.py

Requirements:
-------------
- pandas
- matplotlib
- seaborn
- requests

Inputs:
-------
- data/owid_infant_mortality.csv   (OWID dataset, must be placed in `data/` folder)

Outputs:
--------
- chart1_global_trend_over_time.png
- chart2_difference_WHO_OWID.png
- chart3_average_mortality_by_decade.png
- chart4_global_average.png
- chart5_global_trend.png
- chart6_average_by_decade.png
- chart7_top_10_bottom_10_countries.png
- chart8_global_average_rate_over_time.png
- chart9_country_level_trends.png


Author:
-------
Your Name (GitHub: danitapatro)
"""


import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# Config & Paths
# =========================
DATA_DIR = "data"
PLOTS_DIR = "plots"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

WHO_URL = "https://ghoapi.azureedge.net/api/IMR"
WHO_FILE = os.path.join(DATA_DIR, "who_infant_mortality.csv")
OWID_FILE = os.path.join(DATA_DIR, "owid_infant_mortality.csv")
COMBINED_FILE = os.path.join(DATA_DIR, "infant_mortality_data.csv")

# =========================
# Data Fetch & Save
# =========================
def fetch_who_data():
    try:
        response = requests.get(WHO_URL, timeout=30)
        response.raise_for_status()
        who_data = response.json().get('value', [])
        df = pd.DataFrame(who_data)
        df.to_csv(WHO_FILE, index=False, encoding="utf-8")
        return df
    except Exception as e:
        print(f"⚠️ Failed to fetch WHO data: {e}")
        return pd.DataFrame()


def load_owid_data():
    return pd.read_csv(OWID_FILE)

# =========================
# Data Cleaning
# =========================
def clean_and_merge(who_df, owid_df):
    # WHO clean
    df_who_clean = who_df[['SpatialDim', 'TimeDim', 'NumericValue']].rename(columns={
        'SpatialDim': 'country_code',
        'TimeDim': 'year',
        'NumericValue': 'infant_mortality_rate'
    })
    df_who_clean['source'] = 'WHO'

    # OWID clean
    owid_df = owid_df.rename(columns={
        'Entity': 'country_name',
        'Code': 'country_code',
        'Year': 'year',
        'Infant mortality rate of babies aged under one year, per 100 live births': 'infant_mortality_rate'
    })
    owid_df['source'] = 'OWID'

    # Add country names to WHO data
    code_to_name = owid_df.set_index('country_code')['country_name'].to_dict()
    df_who_clean['country_name'] = df_who_clean['country_code'].map(code_to_name)

    # Merge datasets
    df = pd.concat([df_who_clean, owid_df], ignore_index=True)

    # Drop duplicates & restrict years
    df.drop_duplicates(inplace=True)
    df = df[(df['year'] >= 2000) & (df['year'] <= 2024)]

    # Save combined
    df.to_csv(COMBINED_FILE, index=False, encoding="utf-8")
    return df

# =========================
# Visualization Functions
# =========================
def plot_global_trend(df):
    global_trend = df.groupby("year")["infant_mortality_rate"].mean().reset_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=global_trend, x="year", y="infant_mortality_rate")
    plt.title("Global Average Infant Mortality Rate (2000–2024)")
    plt.ylabel("Infant Mortality Rate")
    plt.xlabel("Year")
    plt.savefig(os.path.join(PLOTS_DIR, "chart1_global_trend_over_time.png"))
    plt.close()

def plot_compare_who_vs_owid(df):
    trend = df.groupby(["year", "source"])["infant_mortality_rate"].mean().unstack()
    trend["Difference"] = trend["WHO"] - trend["OWID"]
    plt.figure(figsize=(10,6))
    sns.barplot(x=trend.index, y=trend["Difference"], color="purple")
    plt.axhline(0, color="black", linestyle="--")
    plt.title("Difference in Infant Mortality Rates: WHO - OWID (2000–2024)", fontsize=14)
    plt.ylabel("Difference (WHO - OWID)")
    plt.xlabel("Year")
    plt.savefig(os.path.join(PLOTS_DIR, "chart2_difference_WHO_OWID.png"), dpi=300, bbox_inches="tight")
    plt.close()

def plot_average_mortality(df):
    df['decade'] = (df['year'] // 10) * 10
    decade_avg = df.groupby("decade")["infant_mortality_rate"].mean().reset_index()
    plt.figure(figsize=(8, 5))
    sns.barplot(data=decade_avg, x="decade", y="infant_mortality_rate")
    plt.title("Average Infant Mortality by Decade")
    plt.ylabel("Infant Mortality Rate")
    plt.xlabel("Decade")
    plt.savefig(os.path.join(PLOTS_DIR, "chart3_average_mortality_by_decade.png"))
    plt.close()

def plot_global_average(df):
    global_trend = df.groupby('year')['infant_mortality_rate'].mean()
    plt.figure(figsize=(10,6))
    sns.lineplot(x=global_trend.index, y=global_trend.values, marker="o")
    plt.title("Global Average Infant Mortality Rate (2000–2024)", fontsize=14)
    plt.xlabel("Year")
    plt.ylabel("Infant Mortality Rate (per 100 live births)")
    plt.grid(True)
    plt.savefig(os.path.join(PLOTS_DIR, "chart4_global_average.png"), dpi=300, bbox_inches="tight")
    plt.close()

def plot_who_vs_owid_global_trend(df):
    who_trend = df[df['source']=="WHO"].groupby('year')['infant_mortality_rate'].mean()
    owid_trend = df[df['source']=="OWID"].groupby('year')['infant_mortality_rate'].mean()

    plt.figure(figsize=(10,6))
    sns.lineplot(x=who_trend.index, y=who_trend.values, label="WHO", marker="o")
    sns.lineplot(x=owid_trend.index, y=owid_trend.values, label="OWID", marker="s")
    plt.title("WHO vs OWID: Global Infant Mortality Trend (2000–2024)", fontsize=14)
    plt.xlabel("Year")
    plt.ylabel("Infant Mortality Rate (per 100 live births)")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(PLOTS_DIR, "chart5_global_trend.png"), dpi=300, bbox_inches="tight")
    plt.close()

def plot_decade_avg(df):
    df['decade'] = (df['year'] // 10) * 10
    decade_trend = df.groupby('decade')['infant_mortality_rate'].mean()

    plt.figure(figsize=(8,6))
    sns.barplot(x=decade_trend.index.astype(str), y=decade_trend.values, palette="coolwarm")
    plt.title("Global Average Infant Mortality by Decade (2000–2020s)", fontsize=14)
    plt.xlabel("Decade")
    plt.ylabel("Infant Mortality Rate (per 100 live births)")
    plt.savefig(os.path.join(PLOTS_DIR, "chart6_average_by_decade.png"), dpi=300, bbox_inches="tight")
    plt.close()

def plot_top_bottom_countries(df, year = None):
    df = df[(df['year'] >= 2000) & (df['year'] <= 2024)]
    latest_year = df['year'].max()
    df_latest = df[df['year'] == latest_year]
    df_sorted = df_latest.sort_values(by='infant_mortality_rate', ascending=False)
    top_10 = df_sorted.head(10)
    bottom_10 = df_sorted.tail(10)
    combined = pd.concat([top_10, bottom_10])

    plt.figure(figsize=(10, 8))
    plt.barh(
        combined['country_name'], combined['infant_mortality_rate'],
        color=['red' if x in top_10['country_name'].values else 'green' for x in combined['country_name']]
    )
    plt.xlabel('Infant Mortality Rate (per 1,000 live births)')
    plt.title(f'Top 10 & Bottom 10 Countries by Infant Mortality Rate ({latest_year})')
    plt.gca().invert_yaxis()
    plt.savefig(os.path.join(PLOTS_DIR, "chart7_top_10_bottom_10_countries.png"), dpi=300, bbox_inches="tight")
    plt.close()

def plot_global_rate(df):
    global_trend = df.groupby("year")["infant_mortality_rate"].mean()
    plt.figure(figsize=(10,6))
    plt.plot(global_trend.index, global_trend.values, marker="o", color="blue", linewidth=2)
    plt.title("Global Average Infant Mortality Rate Over Time", fontsize=14)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Infant Mortality Rate (per 1,000 live births)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig(os.path.join(PLOTS_DIR, "chart8_global_average_rate_over_time.png"), dpi=300, bbox_inches="tight")
    plt.close()

def plot_country_trends(df):
    selected_countries = ["India", "Nigeria", "United States", "Brazil", "China", "Somalia"]
    df_selected = df[df["country_name"].isin(selected_countries)]

    g = sns.relplot(
        data=df_selected,
        x="year", y="infant_mortality_rate",
        kind="line",
        col="country_name", col_wrap=3,
        height=3, aspect=1.2
    )
    g.set_titles("{col_name}")
    g.set_axis_labels("Year", "Infant Mortality Rate")
    plt.suptitle("Infant Mortality Trends by Country", y=1.05, fontsize=14)
    plt.savefig(os.path.join(PLOTS_DIR, "chart9_country_level_trends.png"), dpi=300, bbox_inches="tight")
    plt.close()

# =========================
# Main Function
# =========================
def main():
    print("📥 Fetching WHO Data...")
    who_df = fetch_who_data()

    print("📥 Loading OWID Data...")
    owid_df = load_owid_data()

    print("🧹 Cleaning & Merging...")
    df = clean_and_merge(who_df, owid_df)

    print("📊 Creating Visualizations...")
    plot_global_trend(df)
    plot_compare_who_vs_owid(df)
    plot_average_mortality(df)
    plot_global_average(df)
    plot_who_vs_owid_global_trend(df)
    plot_decade_avg(df)
    plot_top_bottom_countries(df)
    plot_global_rate(df)
    plot_country_trends(df)

    print("✅ Analysis complete. Results saved in 'plots/' folder.")

if __name__ == "__main__":
    main()
