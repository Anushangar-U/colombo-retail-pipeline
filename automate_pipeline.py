import numpy as np
import pandas as pd
import os
import glob

# 1. path configurations
base_path = r"C:\visual studio files\data_project"
master_file_path = os.path.join(base_path, "cleaned_master.csv")
incoming_folder = os.path.join(base_path, "incoming_data")

print("scanning for new retail data entries...")

# 2. look for any new data files in the incoming folder
incoming_files = glob.glob(os.path.join(incoming_folder, "*.csv"))

if not incoming_files:
    print("no new files found to process. pipeline idle.")
elif not os.path.exists(master_file_path):
    print("error: baseline cleaned_master.csv not found. run pipeline.py first.")
else:
    print(f"found {len(incoming_files)} new files to process.")
    
    # load the existing master database
    df_master = pd.read_csv(master_file_path)
    print(f"current master database size: {len(df_master)} rows.")
    
    # 3. process each new incoming file found
    for file in incoming_files:
        print(f"processing streaming file: {os.path.basename(file)}")
        df_new = pd.read_csv(file)
        
        # apply the exact cleaning engine logic to the new data
        df_new = df_new.dropna(subset=['Item', 'Avg Price (Rs.)'])
        
        price_cols = ['Avg Price (Rs.)', 'Price Range - low (Rs.)', 'Price Range - High (Rs.)']
        for col in price_cols:
            if col in df_new.columns:
                df_new[col] = pd.to_numeric(df_new[col], errors='coerce')
                
        # calculate metrics on the new stream
        df_new['price_spread_lkr'] = df_new['Price Range - High (Rs.)'] - df_new['Price Range - low (Rs.)']
        df_new['volatility_index'] = df_new['price_spread_lkr'] / df_new['Avg Price (Rs.)']
        df_new['is_highly_volatile'] = np.where(df_new['volatility_index'] > 0.30, True, False)
        
        # 4. incremental updates: append new clean records into the master dataframe
        df_master = pd.concat([df_master, df_new], ignore_index=True)
        
        # remove the processed file so we do not process it again next time
        os.remove(file)
        print(f"file successfully integrated and archived.")

    # 5. save the updated master database
    df_master.to_csv(master_file_path, index=False)
    print(f"automation run complete. updated master database size: {len(df_master)} rows.")