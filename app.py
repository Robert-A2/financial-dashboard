import streamlit as st
import pandas as pd
import datetime

# ----- Get The Config -----
st.set_page_config(page_title="My APP (MVP)", layout="wide")
if "history" not in st.session_state: st.session_state.history = []

st.warning("This is an MVP (test version). Features may change and bugs may exist.")
st.title("My Dashboard Beta Version")
st.subheader("Know in 30 seconds if you're actually making money (not just earning).")
st.sidebar.info("MVP version production is not ready yet")
st.text("Feel free to share your thoughts.")

# ----- Put Mode Example-----
mode = st.radio("Select how you want to start it:",
                ["⚡ Try Demo (Instant)", "📂 Upload CSV", "✍️ Manual Input"])

if mode == "⚡ Try Demo (Instant)":
    mode = "⚡ Try Demo (Instantly)"

st.write("Current mode:", mode)

# ----- Core Bacis Function -----
def get_results(income, df):
    total = df["amount"].sum()
    net = income - total
    savings_ratio = (net / income * 100) if income > 0 else 0
    expense_ratio = (total / income * 100) if income > 0 else 0

    st.subheader("Financial Stability")
    status = "No income data found." if income==0 else \
             "⚠️ You have to be careful because you are losing money!" if net<0 else \
             "⚠️You have a Low savings." if savings_ratio<10 else \
             "You have a decent savings." if savings_ratio<30 else \
             "✅ Your are doing good on your savings."
    st.success(status)

# ----- Display Metrics -----
    c1,c2,c3 = st.columns(3)
    c1.metric("Income", f"£{income:.2f}")
    c2.metric("Expenses", f"£{total:.2f}")
    c3.metric("Left Over", f"£{net:.2f}")

    ratio1,ratio2 = st.columns(2)
    ratio1.metric("Savings Ratio", f"{savings_ratio:.1f}%")
    ratio2.metric("Expense Ratio", f"{expense_ratio:.1f}%")

    # ----- Breakdown the category -----
    st.subheader("Spending Breakdown")
    cat_summary = df.groupby("category")["amount"].sum()
    st.bar_chart(cat_summary)

    st.write("Breakdown Table:", cat_summary)

    top = cat_summary.idxmax() if not df.empty else None
    if top: st.info(f"Top spending: {top}")

    if st.button("Save Result"):
        st.session_state.history.append({"date": datetime.date.today(), "income": income, "expense": total})
        st.success("Saved.")

# ----- Display Demo -----
if mode =="⚡ Try Demo (Instantly)":
    df = pd.DataFrame({"category":["Rent","Food","Transport"],"amount":[500,200,150]})
    st.dataframe(df)
    get_results(1200, df)

# ----- Function to Upload CSV -----
elif mode=="📂 Upload CSV":
    st.caption("CSV: income, category, amount")
    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        try:
            df = pd.read_csv(file, sep=None, engine="python")
            income = df["income"].iloc[0] if "income" in df.columns else st.number_input("Enter income (£)",0.0)
            if income>0 and "category" in df.columns and "amount" in df.columns:
                get_results(income, df)
            else: st.error("CSV must contain'category' and 'amount'.")
        except Exception as e: st.error(f"Error: {e}")
    else: st.info("Upload a CSV file to analyze your income ane expenses.")

# -----Get the Manual Input-----
elif mode=="✍️ Manual Input":
    st.subheader("Enter Your Data Here")
    income = st.number_input("Income (£)",0.0)

    st.subheader("Expenses by Category")
    
# -----categories -----
    if "manual_categories" not in st.session_state: st.session_state.manual_categories = ["Rent","Food","Transport"]
    new_cat = st.text_input("Add new category", key="new_cat")
    if st.button("Add Category") and new_cat.strip():
        st.session_state.manual_categories.append(new_cat.strip())

    expense_data = []
    for cat in st.session_state.manual_categories:
        amt = st.number_input(f"{cat} (£)",0.0,key=cat)
        if amt>0: expense_data.append({"category":cat,"amount":amt})

    if st.button("Analyze"):
        if expense_data:
            df_expense = pd.DataFrame(expense_data)
            get_results(income, df_expense)
        else:
            st.warning("Please enter at least one expense.")

# ----- Result History -----
st.divider()
st.subheader("Below Is Your Progress")
if st.session_state.history:
    df_hist = pd.DataFrame(st.session_state.history)
    st.line_chart(df_hist.set_index("date")[["income","expense"]])
else:
    st.info("No saved data yet.")

# ----- Run Feedback -----
st.divider()
st.subheader("Share Your Feedback")
fb = st.text_area("What can be improved? Would you use this weekly?")
if st.button("Submit Feedback"):
    if fb.strip(): st.success("Thank you for your feedback!")
    else: st.warning("Please enter some feedback.")