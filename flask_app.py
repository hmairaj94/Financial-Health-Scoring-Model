from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Normalize a series to a 0-1 range
def normalize(series):
    
    if series.max() - series.min() == 0:
        return series  
    return (series - series.min()) / (series.max() - series.min())

@app.route('/score', methods=['POST'])
def get_financial_score():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
       
        df = pd.DataFrame(data)

        print("Input DataFrame:")
        print(df)

        # Check for missing values
        if df.isnull().sum().any():
            return jsonify({'error': 'Missing values in input data'}), 400

        df['Savings_Ratio'] = pd.to_numeric(df['Savings_Ratio'], errors='coerce')
        df['Expenses_Ratio'] = pd.to_numeric(df['Expenses_Ratio'], errors='coerce')
        df['Loan_Ratio'] = pd.to_numeric(df['Loan_Ratio'], errors='coerce')
        df['Credit_Card_Usage'] = pd.to_numeric(df['Credit_Card_Usage'], errors='coerce')

        # Handle missing values after conversion
        if df.isnull().sum().any():
            return jsonify({'error': 'Invalid or missing data after conversion'}), 400
        
        print("Data before normalization:")
        print(df[['Savings_Ratio', 'Expenses_Ratio', 'Loan_Ratio', 'Credit_Card_Usage']])

        # Normalize the columns
        df['Norm_Savings_Ratio'] = normalize(df['Savings_Ratio'])
        df['Norm_Expenses_Ratio'] = normalize(1 - df['Expenses_Ratio'])  # Inverse: lower is better
        df['Norm_Loan_Ratio'] = normalize(1 - df['Loan_Ratio'])  # Inverse: lower is better
        df['Norm_Credit_Card_Usage'] = normalize(1 - df['Credit_Card_Usage'])  # Inverse
        
        print("Normalized Columns:")
        print(df[['Norm_Savings_Ratio', 'Norm_Expenses_Ratio', 'Norm_Loan_Ratio', 'Norm_Credit_Card_Usage']])

        weights = {
            'Norm_Savings_Ratio': 0.35,
            'Norm_Expenses_Ratio': 0.3,
            'Norm_Loan_Ratio': 0.15,
            'Norm_Credit_Card_Usage': 0.2
        }

        if df[['Norm_Savings_Ratio', 'Norm_Expenses_Ratio', 'Norm_Loan_Ratio', 'Norm_Credit_Card_Usage']].isnull().sum().any():
            return jsonify({'error': 'NaN values in normalized columns'}), 400

        # Final score calculation
        df['Financial_Score'] = (
            df['Norm_Savings_Ratio'] * weights['Norm_Savings_Ratio'] +
            df['Norm_Expenses_Ratio'] * weights['Norm_Expenses_Ratio'] +
            df['Norm_Loan_Ratio'] * weights['Norm_Loan_Ratio'] +
            df['Norm_Credit_Card_Usage'] * weights['Norm_Credit_Card_Usage']
        ) * 100  # Scale to 0-100

        #Print final financial score
        print("Calculated Financial Score:")
        print(df['Financial_Score'])

        return jsonify({'financial_score': df['Financial_Score'].iloc[0]}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)