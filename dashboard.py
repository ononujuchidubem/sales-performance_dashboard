import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")

st.title("📊 Sales Performance Dashboard")
st.markdown("### Interactive Dashboard - Superstore Sales Data")

# Load cleaned data
df = pd.read_csv(r"C:\Users\Lenovo E14\Desktop\Sales_Performance_Dashboard\data\Cleaned_Superstore_Data.csv")

# Sidebar filters
st.sidebar.header("Filters")
selected_region = st.sidebar.multiselect(
    "Select Region(s)",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

# Filter data
df_filtered = df[df['Region'].isin(selected_region)]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${df_filtered['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${df_filtered['Profit'].sum():,.0f}")
col3.metric("Total Orders", df_filtered['Order ID'].nunique())
col4.metric("Avg Profit Margin", f"{df_filtered['Profit Margin (%)'].mean():.2f}%")

st.markdown("---")

# Charts
st.subheader("Sales by Region")
fig1, ax1 = plt.subplots()
sns.barplot(data=df_filtered.groupby('Region')['Sales'].sum().reset_index(),
            x='Region', y='Sales', ax=ax1, palette='viridis')
st.pyplot(fig1)

st.subheader("Sales by Category")
fig2, ax2 = plt.subplots()
sns.barplot(data=df_filtered.groupby('Category')['Sales'].sum().reset_index(),
            x='Category', y='Sales', ax=ax2, palette='coolwarm')
st.pyplot(fig2)

st.subheader("Monthly Sales Trend")
monthly = df_filtered.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
fig3, ax3 = plt.subplots(figsize=(12, 5))
sns.lineplot(data=monthly, x='Month', y='Sales', hue='Year', marker='o', ax=ax3)
st.pyplot(fig3)

# Show filtered data
st.subheader("Filtered Data Sample")
st.dataframe(df_filtered.head(20))