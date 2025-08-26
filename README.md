# Infant Mortality Analysis: Data-Driven Insights on Fatal Causes Despite Healthcare Advances

Infant mortality remains one of the most critical indicators of public health and social development worldwide. Despite significant advancements in healthcare technology and prenatal care, many regions still face high rates of infant deaths due to various preventable causes.

This project analyzes infant mortality trends from **2000 to 2024** across different countries and regions, focusing on:

- **Time-based trends:** How infant mortality rates have changed globally and regionally over the last two decades  
- **Cause-based analysis:** Leading fatal causes such as respiratory diseases, infections, and birth complications  
- **Healthcare access impact:** Correlating infant death rates with healthcare infrastructure and prenatal care availability  
- **Demographic factors:** Insights based on maternal age, birth weight, and premature birth prevalence

Using publicly available datasets from trusted sources like the **World Health Organization (WHO)** and **Our World in Data (OWID)**, this project demonstrates:

- Data cleaning and preprocessing techniques  
- Exploratory Data Analysis (EDA) with rich visualizations  
- Potential clustering or grouping of countries based on infant mortality characteristics  
- Storytelling through data to highlight ongoing challenges and opportunities for improving infant health outcomes  

The project is built using Python libraries including **pandas**, **matplotlib**, **seaborn**, and interactive tools like **plotly**.

---

## 📂 Repository Structure
```
Infant-Mortality-Analysis/
│
├── data/ # Raw and processed data files
│ ├── owid_infant_mortality.csv
│ ├── who_infant_mortality.csv
│ └── infant_mortality_data.csv
│
├── plots/ # Saved visualization outputs
│ ├── global_trend.png
│ ├── who_vs_owid.png
│ ├── decade_avg.png
│ ├── top10_2023.png
│ └── bottom10_2023.png
│
├── notebooks/ # Jupyter notebooks
│ └── infant_mortality.ipynb
│
├── Infant_Mortality_Analysis.py # Main analysis script
├── requirements.txt # Dependencies
└── README.md # Project documentation
```

## ⚙️ Installation & Setup
1. **Clone the repository**  
```bash
git clone https://github.com/your-username/infant-mortality-analysis.git
cd infant-mortality-analysis
```

2. **Create a virtual environment (recommended)**  
```bash
python -m venv venv
```
Activate it:  
- Windows: `venv\Scripts\activate`  
- Mac/Linux: `source venv/bin/activate`  

3. **Install dependencies**  
```bash
pip install -r requirements.txt
```

4. **Download datasets**  
   - WHO dataset → fetched automatically by the script  
   - OWID dataset → place in `data/` folder as `owid_infant_mortality.csv`  

---

## 🚀 Usage  

- **Run the main script (analysis + plots):**  
```bash
python Infant_Mortality_Analysis.py
```
➡️ Outputs: all charts saved in the `plots/` folder.  

- **Explore interactively with Jupyter Notebook:**  
Open `notebooks/infant_mortality.ipynb` in Jupyter.  

---

## 📊 Visualizations  

The project generates multiple insights through charts:  

1. **Global Trends** – Average infant mortality rate (2000–2024)  
2. **WHO vs OWID Comparison** – Global trend differences by source  
3. **Decade-wise Averages** – Mortality grouped by decades  
4. **Top & Bottom 10 Countries (2023)** – Highest and lowest infant mortality rates  
5. **Distribution** – Histogram of mortality rates  
6. **Heatmap** – Country vs year (if multiple countries available)  
7. *(Optional)* Interactive country-level trends with Streamlit  

---

## 🛠️ Requirements
(…requirements.txt…)

## 👩‍💻 Author
Anita


