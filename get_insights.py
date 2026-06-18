import pandas as pd
import os

# Path configuration
base_path = r"C:\visual studio files\data_project"
master_file_path = os.path.join(base_path, "cleaned_master.csv")

if not os.path.exists(master_file_path):
    print("Error: cleaned_master.csv not found. Please run your pipeline first.")
else:
    # Load the updated database containing all data through 2024
    df = pd.read_csv(master_file_path)
    
    print("--- COLOMBO RETAIL MARKET INSIGHTS REPORT ---")
    
    # 1. High-Level Overview
    total_records = len(df)
    volatile_records = df['is_highly_volatile'].sum()
    overall_volatility_rate = (volatile_records / total_records) * 100
    
    print(f"Total Market Records Audited: {total_records:,}")
    print(f"Overall Market Volatility Rate: {overall_volatility_rate:.2f}%")
    print("-" * 50)
    
    # 2. Top 5 Most Volatile Items (Supply Chain Risk)
    # Group by Item and find the average volatility index to see the worst offenders
    item_volatility = df.groupby('Item')['volatility_index'].mean().reset_index()
    top_volatile_items = item_volatility.sort_values(by='volatility_index', ascending=False).head(5)
    
    print("Top 5 Items with the Highest Supply Chain Price Variance:")
    for idx, row in top_volatile_items.iterrows():
        print(f" - {row['Item']}: Avg Volatility Index of {row['volatility_index']:.2f}")
    print("-" * 50)
    
    # 3. Yearly Volatility Trend Analysis
    # See if the market is getting more or less stable over time
    yearly_trends = df.groupby('year_extracted')['is_highly_volatile'].mean() * 100
    print("Percentage of Highly Volatile Prices by Year:")
    for year, rate in yearly_trends.items():
        print(f" - Year {year}: {rate:.2f}% of items experienced severe price spreads")
    print("-" * 50)