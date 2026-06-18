import pandas as pd
import os

# path configurations
base_path = r"C:\visual studio files\data_project"
master_file_path = os.path.join(base_path, "cleaned_master.csv")
readme_output_path = os.path.join(base_path, "project_summary.md")

if not os.path.exists(master_file_path):
    print("error: cleaned_master.csv not found. please run the pipeline first.")
else:
    # load the master dataset
    df = pd.read_csv(master_file_path)
    
    # 1. calculate high-level metrics
    total_records = len(df)
    volatile_records = df['is_highly_volatile'].sum()
    overall_volatility_rate = (volatile_records / total_records) * 100
    
    # 2. calculate top volatile items for a markdown table
    item_volatility = df.groupby('Item')['volatility_index'].mean().reset_index()
    top_volatile_items = item_volatility.sort_values(by='volatility_index', ascending=False).head(5)
    
    # 3. calculate yearly trends
    yearly_trends = df.groupby('year_extracted')['is_highly_volatile'].mean() * 100
    
    # 4. build the markdown string
    markdown_content = f"""# colombo retail market data pipeline: automated audit summary

## executive overview
> **key finding:** an analysis of {total_records:,} weekly retail price data points across colombo districts reveals an overall supply chain price volatility rate of **{overall_volatility_rate:.2f}%**. static procurement contracts face significant risk from localized price spreads.

---

## core metrics and risk analysis

### top 5 items with highest market price variance
the table below shows the average volatility index (price spread divided by average price) for the most unstable commodities in the dataset.

| commodity item | average volatility index | risk classification |
| :--- | :---: | :--- |
"""
    
    # append table rows dynamically using a loop
    for idx, row in top_volatile_items.iterrows():
        markdown_content += f"| {row['Item']} | {row['volatility_index']:.2f} | high risk supply variance |\n"
        
    markdown_content += """
---

### structural stability trends over time
the percentage of items experiencing severe price spreads (above 30% variance between maximum and minimum market rates) tracked by year:

"""
    # append yearly trends as a markdown bullet list
    for year, rate in yearly_trends.items():
        markdown_content += f"* **year {year}:** {rate:.2f}% of monitored items showed extreme volatility\n"
        
    markdown_content += """
---
## pipeline operational status
* **ingestion mode:** automated batch processing via glob
* **transformation engine:** pandas and numpy vectorized arrays
* **target storage:** incremental updates to centralized master repository
"""

    # 5. write the string directly to a markdown file
    with open(readme_output_path, "w") as f:
        f.write(markdown_content)
        
    print(f"success: summary metrics exported directly to markdown at: {readme_output_path}")