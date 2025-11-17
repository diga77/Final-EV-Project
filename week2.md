***

# Electric Vehicle Project – Week 2

## Overview

This project focuses on predicting the driving range of electric vehicles using machine learning techniques. It includes data preprocessing, model building, performance evaluation, and the deployment of a user-friendly Streamlit web application.

## Features

- **EV Range Prediction:** Predicts the driving range of an electric vehicle based on model year, price, type, and manufacturer.
- **Data Preprocessing:** Cleans and prepares the electric vehicle population dataset for modeling.
- **Performance Evaluation:** Assesses model accuracy using MAE, RMSE, and $$R^2$$ metrics.
- **Streamlit App:** Interactive web application allowing users to input EV details and receive predicted range estimates.
- **Deployment Ready:** Includes all necessary artifacts for reproducibility and deployment.

## File Structure

- `Electric_Vehicle.ipynb` – Main notebook with data exploration, preprocessing, and modeling steps.
- `streamlit_app.py` – Streamlit web application source code.
- `metrics.json` – Model performance summary.
- `requirements.txt` – Project dependencies.
- Other supporting files as needed.

## Getting Started

1. **Clone the Repository**
   ```bash
   git clone https://github.com/chandan-911/Electric-Vehicle.git
   ```
2. **Navigate to the Project Directory**
   ```bash
   cd Electric-Vehicle/Project\ Week\ 1\ and\ 2
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Streamlit App**
   ```bash
   streamlit run streamlit_app.py
   ```

## Usage

- Enter EV specifications in the web app.
- View the predicted driving range instantly.

***