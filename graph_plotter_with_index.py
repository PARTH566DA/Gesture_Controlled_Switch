import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

file_name = 'data.csv'
data = pd.read_csv(file_name, header=None)

features = data.iloc[:, :-1]

output = data.iloc[:, -1]

# Apply PCA to reduce to 2 components
pca = PCA(n_components=2)
features_pca = pca.fit_transform(features)

clockwise_indices = output == 'CLOCKWISE'
anticlockwise_indices = output == 'ANTICLOCKWISE'
notdefined_indices = output == 'Notdefined'

# Create a scatter plot
plt.figure(figsize=(8, 6))

# Scatter plot for "CLOCKWISE" (blue points)
for idx in range(len(features_pca)):
    if clockwise_indices[idx]:
        plt.scatter(features_pca[idx, 0], features_pca[idx, 1], color='blue', label='Clockwise' if idx == 0 else "", alpha=0.6)
        plt.annotate(idx, (features_pca[idx, 0], features_pca[idx, 1]), fontsize=8, color='blue')

# Scatter plot for "ANTICLOCKWISE" (red points)
for idx in range(len(features_pca)):
    if anticlockwise_indices[idx]:
        plt.scatter(features_pca[idx, 0], features_pca[idx, 1], color='red', label='Anticlockwise' if idx == 0 else "", alpha=0.6)
        plt.annotate(idx, (features_pca[idx, 0], features_pca[idx, 1]), fontsize=8, color='red')
       
# Scatter plot for "NotDefiened" (green points) 
for idx in range(len(features_pca)):
    if notdefined_indices[idx]:
        plt.scatter(features_pca[idx, 0], features_pca[idx, 1], color='green', label='Notdefined' if idx == 0 else "", alpha=0.6)
        plt.annotate(idx, (features_pca[idx, 0], features_pca[idx, 1]), fontsize=8, color='green')

# Add labels and title
plt.title('PCA of Gyroscope and Accelerometer Data (Clockwise vs Anticlockwise)')

# Add a legend
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
