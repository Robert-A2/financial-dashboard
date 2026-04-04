import streamlit as st
import pandas as pd

st.set_page_config(page_title="My APP (MVP)", layout="wide")
st.warning("This is an MVP(test version). Features may change, as well as bugs may also exist.")
st.title ("My Dashboard Beta Version")
st.markdown("""This is an early prototype which is built for testing and to get feedback.""")

st.sidebar.info("MVP version the production is not ready yet")
st.text ("Feel free to share your thought.")

st.subheader("Upload Your Financial Data")
st.markdown("""
***Required CSV Format:*** 
income,expense
  500,200
  400,200""")

# Title
st.title('Freelancers Dashboard')

# Uploade a file
uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])


# Function to analyze financial stability
def analyze_financial_stability(income, expenses):
    if income == 0:
        return "No income data found"

    net_income= income - expenses
    savings_rate = net_income / income

    if net_income < 0:
        return "You are spending more than what you earn!  Reduce your expenses."
    elif savings_rate < 0.1:
        return "Your savings is low! You are close to Risk."
    elif savings_rate < 0.3:
        return "You are finanacially stable but can you still improve your savings."
    
    else:
        return "Based on the analyses You are on a right angle. You are financially stable."

# Function the uploaded file
if uploaded_file is not None:
 try:
        df_user = pd.read_csv(uploaded_file)

        # Validate the neccessary columns
        look_for_cols = {"income", "expense"}
        if not look_for_cols.issubset(df_user.columns):
            st.error("CSV needs to contain 'income' and 'expenses' columns.")

        else:
            # Do the Calculations
            money_in = df_user["income"].sum()
            money_out = df_user["expense"].sum()
            net_income = money_in - money_out

            savings_rate = net_income/ money_in if money_in > 0 else 0
            expense_ratio = money_out / money_in if money_in > 0 else 0

            the_status = analyze_financial_stability(money_in, money_out)

            # Display the results
            st.subheader("Financial Stability")
            st.write(the_status)

            # Show metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Income", f"£{money_in:.2f}")
            col2.metric("Expense", f"£{money_out:.2f}")
            col3.metric("Profit", f"£{net_income:.2f}")

            st.write(f"Savings Rate: {round(savings_rate * 100, 2)}%")
            st.write(f"Expense Ratio: {round(expense_ratio * 100, 2)}%")

 except Exception as e:
  st.error(f"Error processing file:{e}")
else:
    st.info("Please update a CSV file to get started.")

# Process feedback
    st.subheader("Share Your Feedback")
    feedback = st.text_area("What can be improved? What did you like?")

    if st.button("Submit Feedback"):
        if feedback.strip():
            st.success(" Thank You very much for your feedback!")
            # Future: connect to database /Google Sheets
        else:
            ("Please enter some feedback before sumbmitting.")