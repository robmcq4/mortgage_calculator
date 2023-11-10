import streamlit as st
import pandas as pd
import math
import locale
import plotly.express as px
import seaborn as sns

locale.setlocale(locale.LC_ALL, "")


st.title("McHugh Mortgage Calculator")

home_price = float(
    st.text_input("Input Home Price", value="785000", placeholder="$1,000,0000")
)
down_payment = float(
    st.text_input("Input Downpayment Amount", value="100000", placeholder="$100,000")
)
if home_price * 0.2 > down_payment:
    down_twenty = "No"
    st.subheader(f" Downpayment is 20% : :red[{down_twenty}]")
    st.caption(f"Downpayment needed is ${int(home_price*0.2):n}")
elif home_price * 0.2 <= down_payment:
    down_twenty = "Yes"
    st.subheader(f" Downpayment is 20% : :green[{down_twenty}]")
else:
    down_twenty = "No Downpayment Input"
    # st.subheader(f" Downpayment is 20% : :red[{down_twenty}]")
realtor_fee = 0.025 * home_price
st.metric("Realtor Fee", f"${realtor_fee:n}")
st.metric("Initial Downpayment", f"${int(down_payment)+int(realtor_fee):n}")
# st.subheader(f" Downpayment is 20% : {down_twenty}")

total_loan_amount = home_price - down_payment
# st.write(total_loan_amount)
interest_rate = float(
    st.text_input("Input Interest Rate %", value="7", placeholder="7%")
)
interest = (interest_rate / 100) / 12
years = st.text_input("Mortgage length (years)", value=30)
months = float(years) * 12
# st.write(total_loan_amount, interest_rate, interest, months)
# st.write(total_loan_amount * (interest * (1 + interest) ** months))

# st.write((((1 + interest) ** months) - 1))
monthly_payment = (
    (total_loan_amount)
    * (interest * (1 + interest) ** months)
    // (((1 + interest) ** months) - 1)
)
total_mortgage_price = monthly_payment * months
total_interest = total_mortgage_price - total_loan_amount
# st.write(monthly_payment)
#### Total Monthly Payment
hoa = st.selectbox("Does this home have an HOA?", ("no", "yes"))
if hoa == "yes":
    HOA = float(
        st.text_input("Home Owners Association (HOA)", value="25", placeholder="$0")
    )
else:
    HOA = 0
# st.metric("HOA fees", f"${int(HOA):n}")
property_taxes = st.text_input(
    label="Property Taxes", value="12695", placeholder="$1,000"
)


col1, col2, col3, col4 = st.columns(4)

col1.metric("Monthly Mortgage", f"${int(monthly_payment):n}")
col2.metric("Total Loan Amount", f"${int(total_loan_amount):n}")
col3.metric("Total Interest", f"${int(total_interest):n}")
col4.metric("Total Mortgage Price", f"${int(total_mortgage_price):n}")

rates = [1, 2, 3, 4, 5, 6, 7, 8]
monthly_mortgage = []
show_rates = []
for x in rates:
    applied_rate = (float(x) / 100) / 12
    payments = (
        (total_loan_amount)
        * (applied_rate * (1 + applied_rate) ** months)
        // (((1 + applied_rate) ** months) - 1)
    )
    monthly_mortgage.append(f"${int(payments):n}")
    show_rates.append(f"{int(x)} %")

cm = sns.light_palette("green", as_cmap=True)
show = pd.DataFrame({"Interest Rate": show_rates, "Monthly Mortgage": monthly_mortgage})
show.set_index("Interest Rate", inplace=True)

st.dataframe(show.style.background_gradient(cmap=cm), width=600)
# prices = [total_interest, total_loan_amount]
# df = pd.DataFrame(prices)
# fig = px.pie(df, values="prices")
# st.plotly_chart(fig)
# col3.metric(
#     "Total Mortgage Price", f"{locale.currency(total_mortgage_price, grouping=True)}"
# )
homeowners_insurance = monthly_payment * (0.095)
total_monthly_payment = (
    monthly_payment + HOA + (int(property_taxes) // 12) + homeowners_insurance
)
col1, col2, col3 = st.columns(3)
col2.metric("Total Monthly Payment", f"${int(total_monthly_payment):n}")
