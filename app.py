import streamlit as st
import pandas as pd
import datetime

   # Page config 
st.set_page_config(page_title="My APP (MVP)", layout="wide")

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

   # MVP Header 
st.warning("This is an MVP (test version). Features may change and bugs may exist.")

st.title("My Dashboard Beta Version")
st.subheader("Know in 30 seconds if you're actually making money (not just earning).")

st.sidebar.info("MVP version production is not ready yet")
st.text("Feel free to share your thoughts.")

  # Mode selector 
mode = st.radio(
    "Selsect how you want to start:",
    ["⚡ Try Demo (Instant)", "📂 Upload CSV", "✍️ Manual Input"]
)

     # Analyse financial stability
def analyze_financial_stability(income, expenses):
    if income == 0:
        return "No income data found"

    net_income = income - expenses
    savings_rate = net_income / income

    if net_income < 0:
        return "You are spending more than what you earn! Reduce your expenses."
    elif savings_rate < 0.1:
        return "Your savings are low! You are close to risk."
    elif savings_rate < 0.3:
        return "You are financially stable, but you can still improve your savings."
    else:
        return "You are on the right track. You are financially stable."

     # Main logic to analises
def analyze(income, expense):
    net = income - expense
    savings_rate = net / income if income > 0 else 0
    return net, savings_rate

def get_top_category(df):
    if not df.empty:
        return df.groupby("category")["amount"].sum().idxmax()
    return None

    # Display the function
def display_results(income, df_expense):
    total_expense = df_expense["amount"].sum()
    net, savings_rate = analyze(income, total_expense)

    
    status = analyze_financial_stability(income, total_expense)

    st.subheader("Financial Stability")

     # Show metrics
    st.success(status)

    col1, col2, col3 = st.columns(3)
    col1.metric("Income", f"£{income:.2f}")
    col2.metric("Expense", f"£{total_expense:.2f}")
    col3.metric("left over", f"£{net:.2f}")

     # Category breakdown
    st.subheader("Spending Breakdown")
    cat_summary = df_expense.groupby("category")["amount"].sum()
    st.bar_chart(cat_summary)

     # Top category insight
    top_cat = get_top_category(df_expense)
    if top_cat:
        st.info(f"You spend the most on: {top_cat}")

     # Yearly projection (simple but powerful)
    if net >= 0:
        st.write(f"You save about £{round(net*12,2)} per year.")
    else:
        st.write(f"You lose about £{round(abs(net*12),2)} per year.")

      # Save result
    if st.button("Save Result"):
        st.session_state.history.append({
            "date": datetime.date.today(),
            "income": income,
            "expense": total_expense
        })
        st.success("Saved.")

     # display the demonstration
if mode == "⚡ Try Demo (Instant)":
    st.subheader("Instant Demo")

    demo_data = pd.DataFrame({
        "category": ["Rent", "Food", "Transport"],
        "amount": [500, 200, 150]
    })

    income = 1200

    st.write("Sample Data:")
    st.dataframe(demo_data)

    display_results(income, demo_data)

  # Function to upload file
elif mode == "Upload CSV":
    st.subheader("Upload Your Financial Data")

    st.markdown("""
    **Required CSV Format:**  
    income,category,amount  
    2000,Rent,800  
    2000,Food,300  
    """)

    uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            df_user = pd.read_csv(uploaded_file)

            required_cols = {"income", "category", "amount"}
            if not required_cols.issubset(df_user.columns):
                st.error("CSV must contain 'income', 'category', 'amount'.")
            else:
                income = df_user["income"].iloc[0]
                display_results(income, df_user)

        except Exception as e:
            st.error(f"Error processing file: {e}")
    else:
        st.info("Upload a CSV file to analyze your finances.")

     # Get the manual input 
elif mode == "✍️ Manual Input":
    st.subheader("Enter Your Data Here")

    income = st.number_input("Income (£)", min_value=0.0)

    st.subheader("Expenses by Category")

    categories = ["Rent", "Food", "Transport", "Fun", "Other"]
    expense_data = []

    for cat in categories:
        value = st.number_input(f"{cat} (£)", min_value=0.0, key=cat)
        if value > 0:
            expense_data.append({"category": cat, "amount": value})

    if st.button("Analyze"):
        if expense_data:
            df_expense = pd.DataFrame(expense_data)
            display_results(income, df_expense)
        else:
            st.warning("Please enter at least one expense.")

     # Finalize data
st.divider()
st.subheader("Below Is Your Progress")

if st.session_state.history:
    df_hist = pd.DataFrame(st.session_state.history)
    st.line_chart(df_hist.set_index("date")[["income", "expense"]])
else:
    st.info("No saved data yet.")

# Get the feedback
st.divider()
st.subheader("Share Your Feedback")

feedback = st.text_area("What can be improved? Would you use this weekly?")

if st.button("Submit Feedback"):
    if feedback.strip():
        st.success("Thank you very much for your feedback!")
    else:
        st.warning("Please enter some feedback before submitting.")