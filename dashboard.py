# app.py
import streamlit as st
from datetime import date
import pandas as pd
import os

# -----------------------
# Part 1: Page Layout
# -----------------------
st.title("💰 Personal Finance Dashboard")
st.header("Track your Income & Expenses")
st.write("Yahaan aap apni income aur expenses add karke apna balance track kar sakte hain.")

# -----------------------
# Part 2: Transaction Form
# -----------------------
st.subheader("Add a New Transaction")

# Form Fields
transaction_date = st.date_input("Transaction Date", date.today())
transaction_type = st.selectbox("Type", ["Income", "Expense"])
category = st.text_input("Category (e.g., Salary, Food, Investment)")
amount = st.number_input("Amount", min_value=0.0, step=0.01)
description = st.text_area("Description (Optional)")

# -----------------------
# Part 3: CSV Storage & Display
# -----------------------
file_name = "transactions.csv"

if st.button("Add Transaction"):
    # Save transaction as dictionary
    transaction = {
        "Date": str(transaction_date),
        "Type": transaction_type,
        "Category": category,
        "Amount": amount,
        "Description": description
    }

    # Check if CSV exists
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        new_row = pd.DataFrame([transaction])
        df = pd.concat([df, new_row], ignore_index=True)  # append safely
    else:
        df = pd.DataFrame([transaction])

    # Save DataFrame to CSV
    df.to_csv(file_name, index=False)

    # Success message
    st.success(f"✅ Transaction Added: {transaction_type} of ₹{amount} in {category} on {transaction_date}")

    # Display updated table
    st.subheader("All Transactions")
    st.dataframe(df)

# -----------------------
# Display all transactions on page load
# -----------------------
if os.path.exists(file_name):
    df = pd.read_csv(file_name)
    st.subheader("All Transactions")
    st.dataframe(df)

# -----------------------
# Part 4: Summary Section
# -----------------------
if os.path.exists(file_name):
    df = pd.read_csv(file_name)

    # Calculate totals
    total_income = df[df['Type'] == 'Income']['Amount'].sum()
    total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
    balance = total_income - total_expense

    # Display Summary
    st.subheader("💡 Summary")
    st.write(f"**Total Income:** ₹{total_income}")
    st.write(f"**Total Expense:** ₹{total_expense}")
    st.write(f"**Balance:** ₹{balance}")
