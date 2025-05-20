import csv
from multiprocessing import Process
from fraud_detector import detect_fraud
from ipc_handler import send_to_log

# Load transactions from CSV
def load_transactions(filename):
    transactions = []
    with open(filename, mode='r') as file:
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
            transactions.append(transaction)
    return transactions

# Transaction handler run by each process
def handle_transaction(transaction):
    result = detect_fraud(transaction)
    send_to_log(result)

# Multiprocessing logic
def handle_transactions(transactions):
    processes = []

    for txn in transactions:
        p = Process(target=handle_transaction, args=(txn,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

# Entry point
if __name__ == "__main__":
    print("[SYSTEM] Starting Fraud Shield...")
    transactions = load_transactions("data/transactions.csv")
    print(f"[SYSTEM] Loaded {len(transactions)} transactions.")

    handle_transactions(transactions)
    print("[SYSTEM] All transactions processed.")
