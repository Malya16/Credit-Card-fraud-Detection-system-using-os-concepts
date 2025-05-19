from flask import Flask, render_template, request, redirect, url_for
import os
import csv
from fraud_detector import detect_fraud

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []

    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.csv'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            results = run_detection(filepath)

    return render_template('index.html', results=results)

def run_detection(csv_file):
    transactions = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            transaction = {
                "TransactionID": int(row["TransactionID"]),
                "Timestamp": row["Timestamp"],
                "Amount": float(row["Amount"]),
                "Location": row["Location"],
                "CardHolderID": int(row["CardHolderID"]),
                "MerchantID": int(row["MerchantID"]),
                "TransactionType": row["TransactionType"],
                "IsFraud": int(row["IsFraud"])
            }
            result = detect_fraud(transaction)
            result["Status"] = "FRAUD" if result["IsFraud"] else "SAFE"
            transactions.append(result)
    return transactions

if __name__ == '__main__':
    app.run(debug=True)
