import streamlit as st
import pandas as pd

st.set_page_config(page_title="My APP (MVP)", layout="wide")
st.warning("This is an MVP(test version). Features may change, as well as bugs may also exist.")
st.title ("My Dashboard Beta Version")
st.markdown("""This is an early prototype which is built for testing and to get feedback.""")

st.sidebar.info("MVP version the production is not ready yet")
st.text ("Feel free to share your thought. What do you think?")
st.button("submit")


st.text(" Get the clarity of your income and expenses")

# Title
st.title('Financial Freelancers Dashboard')

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
            col1.metric("Income", f"{money_in:.1f}")
            col2.metric("Expense", f"{money_out:.1f}")
            col3.metric("Profit", f"{net_income:.1f}")

            st.write(f"Savings Rate: {round(savings_rate * 100, 2)}%")
            st.write(f"Expense Ratio: {round(expense_ratio * 100, 2)}%")

            # Show the Line chart
            st.subheader("Your Financial Insight")
            st.line_chart({
                "Income": [money_in],
                "Expense": [money_out],
                "Profit": [net_income ]
            })

else:
    st.info("Welcome please upload a CSV file to get started.")
