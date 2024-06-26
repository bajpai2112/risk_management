import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import numpy as np

# Example transaction data
transaction_data = pd.DataFrame({
    'Account_Number': ['1234567890'] * 12 + ['2345678901'] * 12,
    'Name': ['Alice'] * 12 + ['Bob'] * 12,
    'Transaction_Date': pd.date_range(start='2024-06-01', periods=24, freq='D').tolist(),
    'Amount': [10000, 500000, 700000, 150000, 200000, 600000, 100000, 800000, 900000, 100000, 400000, 250000,
               30000, 45000, 100000, 700000, 800000, 120000, 300000, 150000, 600000, 700000, 900000, 200000],
    'Location': ['Local', 'Local', 'International', 'Local', 'Local', 'International', 'Local', 'Local', 'International', 'Local', 'Local', 'International',
                 'Local', 'International', 'Local', 'Local', 'International', 'Local', 'Local', 'International', 'Local', 'Local', 'Local', 'International'],
    'Is_Fraud': [0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Fraudulent flag
})

# Example account credentials
accounts = {
    '1234567890': '1234',
    '2345678901': '2345'
}

# Bank contact details
bank_contact_details = "Contact your branch:\nPhone: +1 234 567 890\nEmail: support@bank.com"

# Function to simulate fraud detection and notification
def detect_fraud(transactions):
    fraudulent_transactions = transactions[transactions['Is_Fraud'] == 1]
    if len(fraudulent_transactions) > 3:
        user_notification = "Your account is locked due to suspicious activity. Please contact your branch."
        messagebox.showwarning("Account Locked", f"{user_notification}\n{bank_contact_details}")
        print("FRAUD DETECTED. Account locked. Details:\n", fraudulent_transactions)
        return True, fraudulent_transactions
    elif not fraudulent_transactions.empty:
        user_notification = "Security Alert: Possible fraudulent activity detected on your account."
        messagebox.showwarning("Fraud Detected", user_notification)
        print("FRAUD DETECTED. Details:\n", fraudulent_transactions)
        return False, fraudulent_transactions
    return False, None

# Function to handle submit button click
def handle_submit():
    account_number = account_number_entry.get()
    pin = pin_entry.get()

    # Validate account number and PIN
    if account_number in accounts and accounts[account_number] == pin:
        # Display user details
        user_details = transaction_data[transaction_data['Account_Number'] == account_number].iloc[0]
        user_name = user_details['Name']
        user_details_label.config(text=f"Account Holder: {user_name}\nAccount Number: {account_number}")

        # Display last 10 transactions
        transactions = transaction_data[transaction_data['Account_Number'] == account_number].tail(10)
        transaction_history_text.config(state=tk.NORMAL)
        transaction_history_text.delete('1.0', tk.END)
        
        for idx, transaction in transactions.iterrows():
            line = f"{transaction['Transaction_Date']} | {transaction['Amount']} | {transaction['Location']}\n"
            transaction_history_text.insert(tk.END, line)
            if transaction['Amount'] > 500000:
                transaction_history_text.tag_add("high_amount", f"{float(idx)+1}.0", f"{float(idx)+1}.end")
            if transaction['Location'] == 'International':
                transaction_history_text.tag_add("international", f"{float(idx)+1}.0", f"{float(idx)+1}.end")
        
        transaction_history_text.config(state=tk.DISABLED)
        transaction_history_text.tag_config("high_amount", foreground="red")
        transaction_history_text.tag_config("international", background="yellow")

        # Simulate fraud detection
        account_locked, suspicious_transactions = detect_fraud(transaction_data[transaction_data['Account_Number'] == account_number])
        if account_locked and suspicious_transactions is not None:
            suspicious_text.config(state=tk.NORMAL)
            suspicious_text.delete('1.0', tk.END)
            suspicious_text.insert(tk.END, "Suspicious Transactions:\n")
            suspicious_text.insert(tk.END, suspicious_transactions.to_string(index=False))
            suspicious_text.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "Invalid account number or PIN.")

# GUI setup
root = tk.Tk()
root.title("Account History and Fraud Detection")

# Account Number entry
account_number_label = ttk.Label(root, text="Account Number:")
account_number_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
account_number_entry = ttk.Entry(root)
account_number_entry.grid(row=0, column=1, padx=10, pady=10)

# PIN entry
pin_label = ttk.Label(root, text="Security PIN:")
pin_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
pin_entry = ttk.Entry(root, show='*')
pin_entry.grid(row=1, column=1, padx=10, pady=10)

# Submit button
submit_button = ttk.Button(root, text="Submit", command=handle_submit)
submit_button.grid(row=2, column=0, columnspan=2, pady=10)

# User details display
user_details_label = ttk.Label(root, text="")
user_details_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Transaction history display
transaction_history_label = ttk.Label(root, text="Transaction History:")
transaction_history_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)

transaction_history_text = tk.Text(root, height=15, width=50, wrap=tk.WORD)
transaction_history_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
transaction_history_text.config(state=tk.DISABLED)

# Suspicious transactions display
suspicious_label = ttk.Label(root, text="Suspicious Transactions (if any):")
suspicious_label.grid(row=6, column=0, padx=10, pady=10, sticky=tk.W)

suspicious_text = tk.Text(root, height=10, width=50, wrap=tk.WORD)
suspicious_text.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
suspicious_text.config(state=tk.DISABLED)

# Run the GUI event loop
root.mainloop()
