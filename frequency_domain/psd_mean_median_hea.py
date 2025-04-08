import numpy as np
import pandas as pd
import os
from glob import glob

# Define input and output folders
psd_folder = r"C:\Users\USER\Desktop\A_final_data\PSD_Results\Healthy"  # Folder with PSD CSV files
summary_folder = r"C:\Users\USER\Desktop\A_final_data\PSD_Results"   # Folder to save MNF & MDF results

# Ensure output directory exists
os.makedirs(summary_folder, exist_ok=True)

# Get list of all PSD files
psd_files = glob(os.path.join(psd_folder, "*.csv"))

# List to store summary results
summary_data = []

for file_path in psd_files:
    try:
        # Extract filename (e.g., P01M01)
        file_name = os.path.basename(file_path).replace("_psd.csv", "")

        # Load PSD data
        data = pd.read_csv(file_path)
        
        # Check if the file is empty or missing required columns
        if data.empty or 'Frequency (Hz)' not in data.columns or 'PSD' not in data.columns:
            print(f"Skipping {file_name}: Empty file or missing required columns.")
            continue

        freqs = data['Frequency (Hz)'].values
        psd_vals = data['PSD'].values

        # Check if PSD values are all zero or invalid
        if np.sum(psd_vals) == 0:
            print(f"Skipping {file_name}: PSD values are all zero.")
            continue

        # Compute Mean Frequency (MNF)
        mnf = np.sum(freqs * psd_vals) / np.sum(psd_vals)

        # Compute Median Frequency (MDF)
        cumulative_power = np.cumsum(psd_vals)
        total_power = cumulative_power[-1]
        
        if total_power > 0:
            median_freq_index = np.searchsorted(cumulative_power, total_power / 2)
            mdf = freqs[median_freq_index]
        else:
            print(f"Skipping {file_name}: Invalid total power.")
            continue

        # Save summary data
        summary_data.append([file_name, mnf, mdf])

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Create summary DataFrame
summary_df = pd.DataFrame(summary_data, columns=["File", "Mean Frequency (MNF)", "Median Frequency (MDF)"])

# Save the summary CSV
summary_path = os.path.join(summary_folder, "MNF_MDF_Summary_Hea.csv")
summary_df.to_csv(summary_path, index=False)

print(f"MNF & MDF Summary saved at: {summary_path}")