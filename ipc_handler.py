# ipc_handler.py
def send_to_log(result):
    txn_id = result["TransactionID"]
    status = "FRAUD" if result["IsFraud"] else "SAFE"
    reasons = ", ".join(result["Reasons"]) if result["Reasons"] else "None"
    print(f"[LOG] Transaction {txn_id} => {status} | Reasons: {reasons}")
    send_otp(txn_id)

def send_otp(txn_id):
    print(f"[OTP] Sending OTP for transaction {txn_id}... [OTP SENT]")