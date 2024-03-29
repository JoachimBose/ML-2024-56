import os
import pandas as pd
from core.main.config import PERF_DIR, OUTPUT_DIR
from pathlib import Path

os.chdir(os.path.dirname(os.path.abspath(__file__)))

directory = f"../{PERF_DIR}"
# Initialize an empty dictionary to store unique columns
unique_columns = {}

first = True
# Iterate through all files in the directory
for filename in os.listdir(directory):        
    if filename.endswith('.csv'):
        # Read each CSV file
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        if first:
            first = False
            for column in ["test", "target-size"]:
                unique_columns[column] = df[column]
        df = df.rename(columns={'actual-size': f"{Path(filename).stem}"})
        unique_columns[f"{Path(filename).stem}"] = df[f"{Path(filename).stem}"]

# Concatenate unique columns into a single dataframe
combined_df = pd.concat(unique_columns.values(), axis=1)

# Write the combined dataframe to a new CSV file
combined_df.to_csv(f"../{OUTPUT_DIR}master_perfomance.csv", index=False)

print("Combined CSV file saved successfully.")

target_sizes = combined_df["target-size"]
results = []
alt_results = []
proportions = []
for index, column in enumerate(combined_df.columns):
    if index <= 1:
        continue
    result = 0
    alt_result = 0
    larger = 0
    smaller = 0
    for i, row in combined_df.iterrows():
        if row[column] - target_sizes[i] > 0:
            result += -(row[column] - target_sizes[i]) ** 2
            larger += 1
        else:
            result += (row[column] - target_sizes[i]) ** 2
            smaller += 1
        alt_result += row[column]
    results.append(result)
    alt_results.append(alt_result)
    proportions.append((larger, smaller))
print("Results", results)
print("Larger-Smaller: ",  proportions)
print(f"Best model: {combined_df.columns[results.index(max(results)) + 2]}")
print(f"Alt Best model: {combined_df.columns[alt_results.index(min(alt_results)) + 2]}")

