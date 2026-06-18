import numpy as np
import pandas as pd
import os

raw_data_path = r"C:\visual studio files\data_project\raw\retail_prices.csv"

print("loading the raw colombo retail dataset...")

if not os.path.exists(raw_data_path):
    print(f"error: the file cannot be found at: {raw_data_path}")
    print("please check that the 'raw_data' folder exists inside 'data_project' and contains 'retail_prices.csv'")
else:
    df_raw = pd.read_csv(raw_data_path)
    print(f"dataset loaded successfully! total records: {len(df_raw)}")
    print(f"columns found: {list(df_raw.columns)}\n")
    
    # chronological split using the dataset values
    df_raw['year_extracted'] = df_raw['Week'].str.split('-').str[0].astype(int)
    df_past = df_raw[df_raw['year_extracted'] <= 2023].copy()
    df_future = df_raw[df_raw['year_extracted'] >= 2024].copy()

    print(f"part a ('the past') created with {len(df_past)} rows.")
    print(f"part b ('the future') created with {len(df_future)} rows.")

    future_data_dir = r"C:\visual studio files\data_project\incoming_data"
    os.makedirs(future_data_dir, exist_ok=True)
    df_future.to_csv(os.path.join(future_data_dir, "new_retail_data_2024.csv"), index=False)
    print(f"mock future data saved successfully!\n")
    
    print("starting data cleaning on past records...")

    # 1. drop rows missing items or prices using the exact column name
    initial_rows = len(df_past)
    df_past = df_past.dropna(subset=['Item', 'Avg Price (Rs.)'])
    dropped_rows = initial_rows - len(df_past)
    print(f"cleaned up {dropped_rows} blank or incomplete rows.")

    # 2. force correct numerical data types for calculations
    price_cols = ['Avg Price (Rs.)', 'Price Range - low (Rs.)', 'Price Range - High (Rs.)']
    for col in price_cols:
        if col in df_past.columns:
            df_past[col] = pd.to_numeric(df_past[col], errors='coerce')

    # 3. calculate the gap between high and low retail ranges
    df_past['price_spread_lkr'] = df_past['Price Range - High (Rs.)'] - df_past['Price Range - low (Rs.)']

    # 4. calculate volatility metrics using numpy
    df_past['volatility_index'] = df_past['price_spread_lkr'] / df_past['Avg Price (Rs.)']
    df_past['is_highly_volatile'] = np.where(df_past['volatility_index'] > 0.30, True, False)

    print("cleaning and metric creation complete.")

    # 5. save the baseline output file
    output_master_path = r"C:\visual studio files\data_project\cleaned_master.csv"
    df_past.to_csv(output_master_path, index=False)
    print(f"baseline master file saved to: {output_master_path}\n")

    # print out the highest variances found in colombo markets 
    print("top 5 most volatile item records found in the past dataset:")
    volatile_items = df_past[df_past['is_highly_volatile'] == True]
    print(volatile_items[['Week', 'Item', 'Avg Price (Rs.)', 'price_spread_lkr']].head())