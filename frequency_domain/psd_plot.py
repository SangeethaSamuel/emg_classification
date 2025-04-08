import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Folder paths
healthy_folder = r"C:\Users\USER\Desktop\A_final_data\PSD_Results\Healthy"
myopathic_folder = r"C:\Users\USER\Desktop\A_final_data\PSD_Results\Myo"

# Function to load and clean PSD data
def load_psd_data(folder_path):
    psd_data = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            try:
                # Read CSV as strings
                df = pd.read_csv(file_path, header=None, dtype=str)
                
                # Clean and convert all entries
                cleaned_values = []
                for val in df.values.flatten():
                    if pd.notnull(val):
                        try:
                            # Remove apostrophes and convert to float
                            cleaned_val = float(str(val).replace("'", "").strip())
                            cleaned_values.append(cleaned_val)
                        except ValueError:
                            continue  # Skip invalid entries

                if cleaned_values:
                    psd_data.append(np.array(cleaned_values))

            except Exception as e:
                print(f"Skipping file {filename}: {e}")
    return psd_data

# Load data
healthy_psd = load_psd_data(healthy_folder)
myopathic_psd = load_psd_data(myopathic_folder)

# Plot
plt.figure(figsize=(14, 6))

# Healthy PSD
plt.subplot(1, 2, 1)
for psd in healthy_psd:
    plt.plot(psd, alpha=0.3)
plt.title('Healthy Patients - PSD')
plt.xlabel('Frequency Bin')
plt.ylabel('PSD Magnitude')
plt.grid(True)

# Myopathic PSD
plt.subplot(1, 2, 2)
for psd in myopathic_psd:
    plt.plot(psd, alpha=0.3, color='orange')
plt.title('Myopathic Patients - PSD')
plt.xlabel('Frequency Bin')
plt.ylabel('PSD Magnitude')
plt.grid(True)

# Save image
plt.tight_layout()
plt.savefig('psd_comparison.png', dpi=300)
plt.close()

print("✅ PSD comparison image saved as 'psd_comparison.png'")
