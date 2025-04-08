import numpy as np
import pandas as pd
import os
from glob import glob

# Define input and output folders
psd_folder = r"C:\Users\USER\Desktop\A_final_data\PSD_Results\Healthy"  # Folder with PSD CSV files
summary_folder = r"C:\Users\USER\Desktop\A_final_data\PSD_Results"   # Folder to save summary CSVs

# Ensure output directory exists
os.makedirs(summary_folder, exist_ok=True)

# Get list of all PSD files
psd_files = glob(os.path.join(psd_folder, "*.csv"))

# List to store summary results
summary_data = []

for file_path in psd_files:
    try:
        # Extract filename without extension (keeping P01M01 format)
        file_name = os.path.basename(file_path).replace("_psd.csv", "")

        # Load PSD data
        data = pd.read_csv(file_path)
        freqs = data['Frequency (Hz)'].values
        psd_vals = data['PSD'].values

        # Compute required statistics
        max_psd = np.max(psd_vals)
        min_psd = np.min(psd_vals)
        mean_psd = np.mean(psd_vals)
        std_psd = np.std(psd_vals)

        # Get corresponding frequencies
        freq_max_psd = freqs[np.argmax(psd_vals)]
        freq_min_psd = freqs[np.argmin(psd_vals)]

        # Save summary data
        summary_data.append([file_name, max_psd, freq_max_psd, min_psd, freq_min_psd, mean_psd, std_psd])

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Create summary DataFrame
summary_df = pd.DataFrame(summary_data, columns=[
    "File", "Max PSD", "Freq Max PSD (Hz)", "Min PSD", "Freq Min PSD (Hz)", "Mean PSD", "Std PSD"
])

# Save the summary CSV
summary_path = os.path.join(summary_folder, "Hea_Summary.csv")
summary_df.to_csv(summary_path, index=False)

print(f"PSD Summary saved at: {summary_path}")
