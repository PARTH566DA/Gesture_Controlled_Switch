import pandas as pd
import numpy as np

# Load your sensor data from the CSV file
file_path = 'temp.csv'  
df = pd.read_csv(file_path)

X = df.iloc[:, :-1] 
fixed_target = df.iloc[0, -1]

num_new_samples = 500  # Number of new data points you want to generate
X_synthetic = np.zeros((num_new_samples, X.shape[1]))

for i in range(X.shape[1]):
    feature_min = X.iloc[:, i].min()
    feature_max = X.iloc[:, i].max()
    X_synthetic[:, i] = np.random.uniform(feature_min, feature_max, size=num_new_samples)

df_synthetic = pd.DataFrame(X_synthetic, columns=X.columns)

# Add the fixed target column to the synthetic data
df_synthetic['target'] = fixed_target  

# Save the synthetic data to a new CSV file
output_file_path = 'Augmented_data.csv'
df_synthetic.to_csv(output_file_path, index=False)

print(f"Synthetic data with fixed target generated and saved to {output_file_path}")
