def send_to_log(result):
    txn_id = result["TransactionID"]
    status = "FRAUD" if result["IsFraud"] else "SAFE"
    reasons = ", ".join(result["Reasons"]) if result["Reasons"] else "None"
    print(f"[LOG] Transaction {txn_id} => {status} | Reasons: {reasons}")

    if result["IsFraud"]:
        confirm = input(f"[ALERT] Transaction {txn_id} is flagged as FRAUD. Do you want to allow it? (yes/no): ")
        if confirm.strip().lower() == "yes":
            print(f"[ACTION] User allowed transaction {txn_id}. Proceeding...")
            send_otp(txn_id)
        else:
            print(f"[ACTION] Transaction {txn_id} BLOCKED by user.")
    else:
        send_otp(txn_id)

def send_otp(txn_id):
    print(f"[OTP] Sending OTP for transaction {txn_id}... [OTP SENT]")
