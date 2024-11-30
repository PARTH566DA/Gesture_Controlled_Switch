import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

file_name = 'data.csv'
data = pd.read_csv(file_name, header=None)

# Extracting input features (all columns except the last one)
features = data.iloc[:, :-1]

# Extracting output column (last column with the final output)
output = data.iloc[:, -1]

# Apply PCA to reduce to 2 components
pca = PCA(n_components=2)
features_pca = pca.fit_transform(features)

# Separate the indices for "CLOCKWISE" and "ANTICLOCKWISE"
clockwise_indices = output == 'CLOCKWISE'
anticlockwise_indices = output == 'ANTICLOCKWISE'
notdefined_indices = output == 'Notdefined'


# Create a scatter plot
plt.figure(figsize=(8, 6))

# Scatter plot for "CLOCKWISE" (blue points)
plt.scatter(features_pca[clockwise_indices, 0], features_pca[clockwise_indices, 1], 
            color='blue', label='Clockwise', alpha=0.6)

# Scatter plot for "ANTICLOCKWISE" (red points)
plt.scatter(features_pca[anticlockwise_indices, 0], features_pca[anticlockwise_indices, 1], 
            color='red', label='Anticlockwise', alpha=0.6)

plt.scatter(features_pca[notdefined_indices, 0], features_pca[notdefined_indices, 1], 
            color='green', label='NotDefined', alpha=0.6)


# Add labels and title
plt.title('PCA of Gyroscope and Accelerometer Data (Clockwise vs Anticlockwise)')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')

# Add a legend
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
