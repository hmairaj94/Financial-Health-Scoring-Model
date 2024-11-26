# Financial Health Scoring Model

## Overview

This project is a financial health scoring system that takes input from a user (such as income, savings, monthly expenses, etc.) and calculates a financial health score. The system provides recommendations based on the score and displays visualizations of spending distribution.

The project consists of two main components:
- **Flask API**: Handles the backend logic, including calculating the financial score.
- **Streamlit App**: Provides the front-end interface where the user can input their data and receive feedback.

## Setup Instructions

### 1. Install Dependencies

To install the required libraries, run:

```bash
pip install -r requirements.txt
```

### 2. Running the Flask API

The Flask API runs on port `5000` by default. To start the Flask server, run:

```bash
python flask_app.py
```

The API will be available at `http://127.0.0.1:5000`.

### 3. Running the Streamlit App

Once the Flask API is running, start the Streamlit app by running:

```bash
streamlit run app.py
```

The Streamlit app will open in your browser (typically at `http://localhost:8501`).

### 4. How to Use

1. Open the Streamlit app in your browser.
2. Enter the financial data (income, savings, expenses, etc.) in the input form.
3. Click the "Calculate Financial Score" button to receive your financial score and see the recommendations and visualizations.
