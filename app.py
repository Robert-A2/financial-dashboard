
import streamlit as st
import pandas as pd
import datetime

# ----- CONFIG -----
st.set_page_config(page_title="Freelancer Survival Dashboard", layout="wide")

if "history" not in st.session_state:
   st.session_state.history = []

# ----- HEADER -----
st.warning("This is an MVP (test version). Results are indicative, not financial advice.")
st.title("🚀 Freelancer Survival Dashboard")
st.subheader("Know in 30 seconds if you're financially safe or at risk.")

st.sidebar.info("MVP version - built for testing real freelancer pain points")

# ----- CURRENCY -----
currency = st.sidebar.selectbox(
    "Select Currency",
    ["EUR (€)", "USD ($)", "GBP (£)", "GHS (₵)"]
)

currency_symbol = (
     "€" if "EUR" in currency else
     "$" if "USD" in currency else
     "£" if "GBP" in currency else
     "₵"
)

# ----- GOAL INPUT (KEY FEATURE) -----
st.subheader("💰 Your Income Goal")
goal = st.number_input(
f"What is your monthly income goal? ({currency_symbol})",
min_value=0.0
)

# ----- MODE -----
mode = st.radio(
"How do you want to start?",
["⚡ Try Demo", "📂 Upload CSV", "✍️ Manual Input"]
)

# ----- CORE FUNCTION -----
def get_results(income, df, goal):
 total = df["amount"].sum()
  net = income - total

savings_ratio = (net / income * 100) if income > 0 else 0

st.subheader("💡 Your Financial Reality")

# ---- RISK LEVEL ----
if income == 0:
risk = "danger"
msg = "🚨 No income. You are in survival mode."
elif net < 0:
risk = "danger"
msg = "🚨 You are losing money. This is not sustainable."
elif income < goal:
risk = "warning"
msg = "⚠️ You are below your income target."
elif savings_ratio < 20:
risk = "warning"
msg = "⚠️ Your safety margin is low."
else:
risk = "safe"
msg = "✅ You are financially stable."

if risk == "danger":
st.error(msg)
elif risk == "warning":
st.warning(msg)
else:
st.success(msg)

# ---- METRICS ----
c1, c2, c3 = st.columns(3)
c1.metric("Income", f"{currency_symbol}{income:.2f}")
c2.metric("Expenses", f"{currency_symbol}{total:.2f}")
c3.metric("Left Over", f"{currency_symbol}{net:.2f}")

# ---- RATIOS ----
r1, r2 = st.columns(2)
r1.metric("Savings Ratio", f"{savings_ratio:.1f}%")
expense_ratio = (total / income * 100) if income > 0 else 0
r2.metric("Expense Ratio", f"{expense_ratio:.1f}%")

# ---- RUNWAY ----
st.subheader("🧠 Survival Runway")
if total > 0:
runway = income / total
st.info(f"You can survive **{runway:.1f} months** at this spending level.")
else:
st.info("No expenses recorded.")

# ---- GOAL GAP ----
gap = goal - income
if gap > 0:
st.warning(f"You need {currency_symbol}{gap:.2f} more to reach your goal.")
else:
st.success("You reached your income goal.")

# ---- ACTION ADVICE ----
st.subheader("🎯 What You Should Do Next")

if risk == "danger":
st.write("- Cut unnecessary expenses immediately")
st.write("- Find at least 1 paying client this week")
st.write("- Avoid unpaid work")
elif risk == "warning":
st.write("- Increase your rates or get 1 extra client")
st.write("- Reduce your top spending category")
else:
st.write("- Maintain current strategy")
st.write("- Consider saving or reinvesting")

# ---- BREAKDOWN ----
st.subheader("📊 Spending Breakdown")
cat_summary = df.groupby("category")["amount"].sum()
st.bar_chart(cat_summary)

top = cat_summary.idxmax() if not df.empty else None
if top:
st.info(f"Top Spending Category: {top}")

# ---- SAVE ----
if st.button("Save Result"):
st.session_state.history.append({
"date": datetime.date.today(),
"income": income,
"expense": total
})
st.success("Saved.")

# ----- DEMO MODE -----
if mode == "⚡ Try Demo":
df = pd.DataFrame({
"category": ["Rent", "Food", "Transport"],
"amount": [500, 200, 150]
})
st.dataframe(df)
get_results(1200, df, goal)

# ----- CSV MODE -----
elif mode == "📂 Upload CSV":
st.caption("CSV format: income, category, amount")

file = st.file_uploader("Upload CSV", type=["csv"])

if file:
try:
df = pd.read_csv(file, sep=None, engine="python")

income = df["income"].iloc[0] if "income" in df.columns else st.number_input(
f"Enter income ({currency_symbol})", 0.0
)

if income > 0 and "category" in df.columns and "amount" in df.columns:
get_results(income, df, goal)
else:
st.error("CSV must contain 'category' and 'amount' columns.")

except Exception as e:
st.error(f"Error: {e}")
else:
st.info("Upload a CSV file to analyze your finances.")

# ----- MANUAL INPUT -----
elif mode == "✍️ Manual Input":
st.subheader("Enter Your Data")

income = st.number_input(f"Income ({currency_symbol})", 0.0)

st.subheader("Expenses by Category")

if "manual_categories" not in st.session_state:
st.session_state.manual_categories = ["Rent", "Food", "Transport"]

new_cat = st.text_input("Add new category")

if st.button("Add Category") and new_cat.strip():
st.session_state.manual_categories.append(new_cat.strip())

expense_data = []

for cat in st.session_state.manual_categories:
amt = st.number_input(f"{cat} ({currency_symbol})", 0.0, key=cat)
if amt > 0:
expense_data.append({"category": cat, "amount": amt})

if st.button("Analyze"):
if expense_data:
df_expense = pd.DataFrame(expense_data)
get_results(income, df_expense, goal)
else:
st.warning("Please enter at least one expense.")

# ----- HISTORY -----
st.divider()
st.subheader("📈 Your Progress")

if st.session_state.history:
df_hist = pd.DataFrame(st.session_state.history)
st.line_chart(df_hist.set_index("date")[["income", "expense"]])
else:
st.info("No saved data yet.")

# ----- SMART FEEDBACK -----
st.divider()
st.subheader("💬 Help Improve This Tool")

fb_type = st.radio(
"What is your biggest problem as a freelancer?",
[
"I don't earn enough",
"My expenses are too high",
"Income is unstable",
"I don't know where my money goes"
]
)

fb = st.text_area("What should we improve? Would you use this weekly?")

if st.button("Submit Feedback"):
if fb.strip():
st.success("Thank you for your feedback!")
else:
st.warning("Please enter some feedback.")