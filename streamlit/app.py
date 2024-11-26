import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

FLASK_API_URL = "http://127.0.0.1:5000/score"

# Streamlit UI
st.title('Financial Health Scoring Model')

# Add some debug prints
st.write("Streamlit app is running...")

# Create an input form for user data
st.subheader('Enter Family Financial Data')

# Collect inputs
family_id = st.text_input("Family ID", "1")
income = st.number_input("Income", min_value=0)
savings = st.number_input("Savings", min_value=0)
monthly_expenses = st.number_input("Monthly Expenses", min_value=0)
loan_payments = st.number_input("Loan Payments", min_value=0)
credit_card_spending = st.number_input("Credit Card Spending", min_value=0)
savings_ratio = st.number_input("Savings Ratio", min_value=0.0, max_value=1.0, value=0.5)
expenses_ratio = st.number_input("Expenses Ratio", min_value=0.0, max_value=1.0, value=0.3)
loan_ratio = st.number_input("Loan Ratio", min_value=0.0, max_value=1.0, value=0.05)
credit_card_usage = st.number_input("Credit Card Usage", min_value=0.0, max_value=1.0, value=0.2)

# Create a DataFrame from the input
input_data = {
    'Family ID': [family_id],
    'Savings': [savings],
    'Income': [income],
    'Monthly Expenses': [monthly_expenses],
    'Loan Payments': [loan_payments],
    'Credit Card Spending': [credit_card_spending],
    'SavingsToIncomeRatio': [savings / income if income != 0 else 0],
    'ExpensesPercentOfIncome': [monthly_expenses / income if income != 0 else 0],
    'Savings_Ratio': [savings_ratio],
    'Expenses_Ratio': [expenses_ratio],
    'Loan_Ratio': [loan_ratio],
    'Credit_Card_Usage': [credit_card_usage]
}

df_input = pd.DataFrame(input_data)

st.write("Input data created:", df_input)

# Send a POST request to Flask API
if st.button('Calculate Financial Score'):
    try:
        st.write("Sending request to Flask API...")

        # Make the POST request to Flask API
        response = requests.post(FLASK_API_URL, json=input_data)
        
        # Debugging: print the response
        st.write("Response from Flask API:", response.json())

        # Check if the response was successful
        if response.status_code == 200:
            result = response.json()
            financial_score = result['financial_score']

            # Display the financial score
            st.subheader(f"Your Financial Score is: {financial_score:.2f}")

            # Provide recommendations based on the score
            st.subheader('Recommendations')
            if financial_score < 50:
                st.write("Your financial score is below 50. Consider reducing your monthly expenses and increasing savings.")
            elif 50 <= financial_score < 75:
                st.write("Your financial score is moderate. Try to reduce your discretionary spending to improve your score.")
            else:
                st.write("Your financial score is great! Keep up the good work by maintaining savings and controlling expenses.")

            # Visualization for Spending Distribution
            st.subheader('Spending Distribution')
            category_spending = pd.DataFrame({
                'Category': ['Savings', 'Expenses', 'Loan Payments', 'Credit Card Spending'],
                'Amount': [savings, monthly_expenses, loan_payments, credit_card_spending]
            })

            # Plot for spending distribution
            fig, ax = plt.subplots()
            sns.barplot(x='Category', y='Amount', data=category_spending, ax=ax)
            ax.set_title('Spending Distribution Across Categories')
            st.pyplot(fig)

        else:
            st.write("Error: Unable to get a response from the Flask API.")
    except Exception as e:
        st.write(f"Error: {e}")
