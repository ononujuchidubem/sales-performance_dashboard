import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Set style for better visuals
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

print("Libraries imported successfully!")

# ====================== STEP 1: LOAD DATA ======================
df = pd.read_csv(
    r"C:\Users\Lenovo E14\Desktop\Sales_Performance_Dashboard\data\Sample - Superstore.csv",
    encoding='latin1'
)

print("Dataset loaded successfully!")
print(f"Shape of data: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())
# ====================== DATA CLEANING ======================

print("\n" + "="*50)
print("STEP 2: DATA CLEANING")
print("="*50)

# Check for missing values
print("\nMissing values per column:")
print(df.isnull().sum())

# Drop unnecessary columns
df = df.drop(['Row ID', 'Postal Code'], axis=1, errors='ignore')

# Convert date columns to datetime format
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Create useful new columns
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
df['Month Name'] = df['Order Date'].dt.strftime('%B')
df['Profit Margin (%)'] = (df['Profit'] / df['Sales']) * 100

print("\nData cleaning completed successfully!")
print(f"New shape of data: {df.shape}")
print("\nFirst 5 rows after cleaning:")
print(df.head())
# ====================== KEY METRICS & ANALYSIS ======================

print("\n" + "="*50)
print("STEP 3: KEY METRICS & ANALYSIS")
print("="*50)

# Total Sales and Profit
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
avg_profit_margin = df['Profit Margin (%)'].mean()

print(f"\n=== OVERALL PERFORMANCE ===")
print(f"Total Sales:          ${total_sales:,.2f}")
print(f"Total Profit:         ${total_profit:,.2f}")
print(f"Total Orders:         {total_orders}")
print(f"Average Profit Margin: {avg_profit_margin:.2f}%")

# Sales and Profit by Region
print("\n=== SALES BY REGION ===")
region_analysis = df.groupby('Region').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Profit Margin (%)': 'mean'
}).sort_values('Sales', ascending=False).round(2)

print(region_analysis)

# Sales by Category
print("\n=== SALES BY CATEGORY ===")
category_analysis = df.groupby('Category').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Profit Margin (%)': 'mean'
}).sort_values('Sales', ascending=False).round(2)

print(category_analysis)
# ====================== VISUALIZATIONS ======================

print("\n" + "="*50)
print("STEP 4: CREATING VISUALIZATIONS")
print("="*50)

# 1. Sales by Region
plt.figure(figsize=(8, 5))
sns.barplot(data=region_analysis.reset_index(), x='Region', y='Sales', hue='Region', palette='viridis', legend=False)
plt.title('Total Sales by Region', fontsize=14)
plt.ylabel('Sales ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Sales by Category
plt.figure(figsize=(8, 5))
sns.barplot(data=category_analysis.reset_index(), x='Category', y='Sales', hue='Category', palette='coolwarm', legend=False)
plt.title('Total Sales by Category', fontsize=14)
plt.ylabel('Sales ($)')
plt.tight_layout()
plt.show()

# 3. Monthly Sales Trend
monthly_sales = df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_sales, x='Month', y='Sales', hue='Year', marker='o', palette='tab10')
plt.title('Monthly Sales Trend Over Years', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Sales ($)')
plt.xticks(range(1, 13))
plt.tight_layout()
plt.show()

print("\nVisualizations created successfully!")
# ====================== SAVE CLEANED DATA ======================

print("\n" + "="*50)
print("STEP 5: SAVING CLEANED DATA")
print("="*50)

# Use full path to save (same style as loading)
save_path = r"C:\Users\Lenovo E14\Desktop\Sales_Performance_Dashboard\data\Cleaned_Superstore_Data.csv"
df.to_csv(save_path, index=False)

print("\nCleaned data saved successfully!")
print(f"File saved at: {save_path}")
print(f"Total rows saved: {len(df)}")
