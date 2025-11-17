***

# Electric Vehicle Data Analysis – Week 1

## Overview

Week 1 focuses on exploratory data analysis (EDA) of the electric vehicle population dataset. This project involves data loading, cleaning, preprocessing, and extracting insights through statistical analysis and visualizations.

## Problem Statement

Electric Vehicles (EVs) are rapidly transforming the automotive industry, but customers still face uncertainty about real-world range and performance. This project aims to analyze EV population data to understand patterns, distributions, and relationships between various features.

## Objectives

- Load and explore the Electric Vehicle Population dataset
- Clean and preprocess data for analysis
- Perform exploratory data analysis (EDA)
- Generate visualizations to understand EV characteristics
- Extract insights about electric vehicle features and distributions

## Dataset

- **Source:** `Electric_Vehicle_Population_Data.csv`
- **Size:** 177,866 records with 17 features
- **Key Features:** VIN, County, City, State, Model Year, Make, Model, Electric Vehicle Type, Electric Range, Base MSRP, and more

## Project Structure

```
Project Week 1/
├── Electric_Vehicle.ipynb              # Main analysis notebook
├── Electric_Vehicle_Population_Data.csv # Raw dataset
└── cleaned_ev_data.csv                 # Cleaned dataset after preprocessing
```

## Key Analysis Steps

### 1. Data Loading
- Imported the EV population dataset using pandas
- Displayed initial rows to understand data structure

### 2. Data Exploration
- Checked dataset dimensions (177,866 rows × 17 columns)
- Analyzed data types and identified missing values
- Generated summary statistics for numerical features

### 3. Data Cleaning & Preprocessing
- Identified missing values across features
- Cleaned categorical columns (Make, Model) using string operations
- Exported cleaned dataset for future use

### 4. Exploratory Data Analysis (EDA)
- **Distribution Analysis:** Visualized the distribution of Electric Vehicle Range
- **Make Distribution:** Analyzed the number of models by manufacturer
- **Correlation Analysis:** Created heatmap showing relationships between numerical features

### 5. Insights Extraction
- Generated correlation heatmap for numerical features
- Identified key relationships between Model Year, Postal Code, and Electric Range

## Technologies Used

- **Python 3.x**
- **pandas** – Data manipulation and analysis
- **numpy** – Numerical computations
- **matplotlib** – Data visualization
- **seaborn** – Statistical visualizations

## Getting Started

### Prerequisites
Ensure you have Python 3.x installed with the required libraries.

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/chandan-911/Electric-Vehicle.git
   ```

2. **Navigate to Week 1 Directory**
   ```bash
   cd Electric-Vehicle/Project\ Week\ 1
   ```

3. **Install Dependencies**
   ```bash
   pip install pandas numpy matplotlib seaborn
   ```

4. **Run the Notebook**
   ```bash
   jupyter notebook Electric_Vehicle.ipynb
   ```

## Key Findings

- Comprehensive data cleaning reduced inconsistencies in the dataset
- Correlation analysis revealed relationships between model year and electric range
- Distribution visualizations provided insights into EV range patterns across different manufacturers

## Output Files

- `cleaned_ev_data.csv` – Preprocessed dataset ready for machine learning (Week 2)

***
