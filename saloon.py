import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load cleaned datasets
repeat_customers = pd.read_csv("cleaned_repeat_customers.csv")
daily_sms = pd.read_csv("cleaned_daily_sms.csv")
client_details = pd.read_csv("cleaned_client_details.csv")

# Convert dates if necessary
if 'Date' in repeat_customers.columns:
    repeat_customers['Date'] = pd.to_datetime(repeat_customers['Date'], errors='coerce')
if 'Date' in daily_sms.columns:
    daily_sms['Date'] = pd.to_datetime(daily_sms['Date'], errors='coerce')

st.set_page_config(page_title="Salon Business Dashboard", layout="wide")
st.title("💇‍♀️ Naturals Bhimavaram | Business Intelligence Dashboard")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📅 Total Appointments", len(repeat_customers))
with col2:
    st.metric("🔁 Repeat Customers", repeat_customers['Mobile Number'].nunique())
with col3:
    st.metric("💰 Total Revenue Estimate", f"₹{repeat_customers['Net Revenue - Tax'].sum():,.0f}")
with col4:
    st.metric("📤 Total SMS Sent", len(daily_sms))

# Revenue Trends
st.subheader("📈 Monthly Revenue Trend")
if 'Date' in repeat_customers.columns:
    repeat_customers['Month'] = repeat_customers['Date'].dt.to_period('M')
    monthly_rev = repeat_customers.groupby('Month')['Net Revenue - Tax'].sum().reset_index()
    monthly_rev['Month'] = monthly_rev['Month'].astype(str)

    fig = px.line(
        monthly_rev,
        x='Month',
        y='Net Revenue - Tax',
        title="📊 Revenue Over Time",
        line_shape='spline',
        markers=True,
        color_discrete_sequence=["#3b82f6"]
    )
    fig.update_traces(hovertemplate="Month: %{x}<br>Revenue: ₹%{y:,.0f}")
    fig.update_layout(template='plotly_white', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

# Repeat Customer Trend
st.subheader("🔁 Repeat Visit Trend")
if 'Date' in repeat_customers.columns:
    repeat_customers['Visit Count'] = repeat_customers.groupby('Mobile Number').cumcount() + 1
    visits_over_time = repeat_customers.groupby(repeat_customers['Date'].dt.to_period('M'))['Mobile Number'].nunique().reset_index()
    visits_over_time.columns = ['Month', 'Unique Repeat Customers']
    visits_over_time['Month'] = visits_over_time['Month'].astype(str)

    fig2 = px.bar(
    visits_over_time,
    x='Month',
    y='Unique Repeat Customers',
    color='Unique Repeat Customers',
    color_continuous_scale='viridis',
    title="📈 Unique Repeat Customers Over Time"
)
fig2.update_traces(marker_line_width=1.5)
fig2.update_layout(template='plotly_white', hovermode='x unified')


# SMS Campaign Activity
st.subheader("💬 SMS Campaign Volume")
if 'Date' in daily_sms.columns:
    daily_sms['Month'] = daily_sms['Date'].dt.to_period('M')
    sms_monthly = daily_sms.groupby('Month').size().reset_index(name='SMS Count')
    sms_monthly['Month'] = sms_monthly['Month'].astype(str)

    fig3 = px.area(
        sms_monthly,
        x='Month',
        y='SMS Count',
        title="📨 Monthly SMS Campaign Trend",
        color_discrete_sequence=["#ec4899"]
    )
    fig3.update_layout(template='plotly_dark', hovermode="x unified")
    st.plotly_chart(fig3, use_container_width=True)

# Client Directory
st.subheader("📇 Client Directory")
search = st.text_input("Search by Name or Mobile")
filtered_clients = client_details[
    client_details['Customer Name'].str.contains(search, case=False, na=False) |
    client_details['Phone'].astype(str).str.contains(search)
]
st.dataframe(filtered_clients, use_container_width=True)

st.markdown("---")
st.caption("🚀 Built with ❤️ for Naturals Bhimavaram • Real-Time Business Dashboard • Powered by Streamlit + Plotly")
