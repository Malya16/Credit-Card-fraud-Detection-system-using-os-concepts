from flask import Flask, request, render_template, redirect, url_for
import csv
from fraud_detector import detect_fraud

app = Flask(__name__)
flagged_transactions = []  # Store fraud transactions

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    global flagged_transactions
    file = request.files["csvfile"]
    if not file:
        return "No file uploaded", 400

    transactions = []
    reader = csv.DictReader(file.stream.read().decode("utf-8").splitlines())
    for row in reader:
        txn = {
            "TransactionID": int(row["TransactionID"]),
            "Timestamp": row["Timestamp"],
            "Amount": float(row["Amount"]),
            "Location": row["Location"],
            "CardHolderID": int(row["CardHolderID"]),
            "MerchantID": int(row["MerchantID"]),
            "TransactionType": row["TransactionType"],
            "IsFraud": int(row["IsFraud"])
        }
        result = detect_fraud(txn)
        if result["IsFraud"]:
            flagged_transactions.append(result)

    return redirect(url_for("alerts"))

@app.route("/alerts")
def alerts():
    return render_template("alerts.html", transactions=flagged_transactions)

@app.route("/approve/<int:txn_id>")
def approve(txn_id):
    print(f"[ACTION] Transaction {txn_id} approved by user.")
    return redirect(url_for("alerts"))

@app.route("/block/<int:txn_id>")
def block(txn_id):
    print(f"[ACTION] Transaction {txn_id} BLOCKED by user.")
    return redirect(url_for("alerts"))

if __name__ == "__main__":
    app.run(debug=True)
