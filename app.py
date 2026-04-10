import streamlit as st
import pandas as pd

st.set_page_config(page_title="Freelancer Survival Tool", layout="centered")

st.title("💸 Freelancer Survival Tool")

st.markdown("Understand your financial situation in seconds.")

# ----- INPUTS -----
st.subheader("📥 Your Data")

income = st.number_input("💰 Monthly Income (€)", min_value=0.0)
savings = st.number_input("🏦 Current Savings (€)", min_value=0.0)

st.markdown("### 💸 Expenses")

expense_data = []

num_expenses = st.number_input("Number of expense items", min_value=1, step=1)

for i in range(int(num_expenses)):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(f"Expense {i+1} name", key=f"name_{i}")
    with col2:
        amount = st.number_input(f"€", min_value=0.0, key=f"amount_{i}")

if amount > 0:
    expense_data.append({"name": name, "amount": amount})

# ----- CALCULATION -----
if st.button("Analyze my situation"):

   if not expense_data:
       st.warning("Please enter at least one expense.")
       st.stop()

   df_expense = pd.DataFrame(expense_data)
   total_expense = df_expense["amount"].sum()
   monthly_balance = income - total_expense

   st.divider()
   st.subheader("📊 Your Situation")

# ----- SAFE TO SPEND -----
if monthly_balance >= 0:
    st.success(f"🟢 You are stable. You can save about €{monthly_balance:.0f}/month.")
else:
    st.error(f"🔴 You are losing €{abs(monthly_balance):.0f}/month.")

# ----- SURVIVAL -----
if monthly_balance < 0:
    if savings > 0:
        months_survival = savings / abs(monthly_balance)
        st.error(f"⏳ You will run out of money in {months_survival:.1f} months.")
    else:
        st.error("🚨 You have no savings and are losing money. Immediate action needed.")
else:
    st.success("🟢 You are not at immediate risk.")

# ----- DECISION ENGINE -----
st.divider()
st.subheader("🚀 What to do now")

if monthly_balance < 0:
    needed_income = abs(monthly_balance)
    weekly_gap = needed_income / 4

    st.markdown(f"""
👉 You need **€{needed_income:.0f} more per month** to break even
👉 That’s about **€{weekly_gap:.0f} per week**
""")

    if savings > 0:
        if months_survival < 1:
            st.error("🚨 Critical: Less than 1 month left. Act immediately.")
        elif months_survival < 3:
            st.warning("⚠️ You have limited time. Focus on getting income now.")
        else:
            st.info("🟡 You have some buffer, but don’t wait too long.")

    st.markdown("""
### 📌 Action Plan:
- Get at least **1 paying client this week**
- Pause non-essential spending
- Focus only on paid work (no free tasks)
""")
    
else:
    st.markdown("""
### ✅ You are in a good position:
- Keep saving consistently
- Prepare for slow months
- Invest in better clients or skills
""")

# ----- SUMMARY -----
    st.divider()
    st.subheader("🧠 Quick Summary")

    if monthly_balance < 0:
        st.error("You are currently at risk. Focus on increasing income immediately.")
    else:
        st.success("You are financially stable. Maintain and grow this position.")
