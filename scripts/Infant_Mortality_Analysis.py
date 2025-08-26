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
- data/infant_mortality_data.csv   (cleaned & merged dataset)
- plots/global_trend.png
- plots/who_vs_owid.png
- plots/decade_avg.png
- plots/top10_2023.png
- plots/bottom10_2023.png

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
    response = requests.get(WHO_URL)
    who_data = response.json()['value']
    df = pd.DataFrame(who_data)
    df.to_csv(WHO_FILE, index=False, encoding="utf-8")
    return df

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
    plt.savefig(os.path.join(PLOTS_DIR, "global_trend.png"))
    plt.close()

def plot_who_vs_owid(df):
    trend = df.groupby(["year", "source"])["infant_mortality_rate"].mean().reset_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=trend, x="year", y="infant_mortality_rate", hue="source", marker="o")
    plt.title("WHO vs OWID: Global Infant Mortality Trends")
    plt.ylabel("Infant Mortality Rate")
    plt.xlabel("Year")
    plt.savefig(os.path.join(PLOTS_DIR, "who_vs_owid.png"))
    plt.close()

def plot_decade_avg(df):
    df['decade'] = (df['year'] // 10) * 10
    decade_avg = df.groupby("decade")["infant_mortality_rate"].mean().reset_index()
    plt.figure(figsize=(8, 5))
    sns.barplot(data=decade_avg, x="decade", y="infant_mortality_rate")
    plt.title("Average Infant Mortality by Decade")
    plt.ylabel("Infant Mortality Rate")
    plt.xlabel("Decade")
    plt.savefig(os.path.join(PLOTS_DIR, "decade_avg.png"))
    plt.close()

def plot_top_bottom_countries(df, year=2023):
    latest = df[df["year"] == year].dropna(subset=["infant_mortality_rate"])
    top10 = latest.nlargest(10, "infant_mortality_rate")
    bottom10 = latest.nsmallest(10, "infant_mortality_rate")

    plt.figure(figsize=(10, 6))
    sns.barplot(data=top10, y="country_name", x="infant_mortality_rate", palette="Reds_r")
    plt.title(f"Top 10 Countries by Infant Mortality Rate ({year})")
    plt.xlabel("Infant Mortality Rate")
    plt.ylabel("Country")
    plt.savefig(os.path.join(PLOTS_DIR, f"top10_{year}.png"))
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.barplot(data=bottom10, y="country_name", x="infant_mortality_rate", palette="Greens")
    plt.title(f"Bottom 10 Countries by Infant Mortality Rate ({year})")
    plt.xlabel("Infant Mortality Rate")
    plt.ylabel("Country")
    plt.savefig(os.path.join(PLOTS_DIR, f"bottom10_{year}.png"))
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
    plot_who_vs_owid(df)
    plot_decade_avg(df)
    plot_top_bottom_countries(df, year=2023)

    print("✅ Analysis complete. Results saved in 'plots/' folder.")

if __name__ == "__main__":
    main()
