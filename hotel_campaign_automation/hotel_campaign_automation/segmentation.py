import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def load_customer_data():
    # TODO: Replace this with actual data loading from a database or CSV file
    # For now, we'll create a sample dataset
    np.random.seed(42)
    n_customers = 1000
    data = {
        'recency': np.random.randint(1, 365, n_customers),
        'frequency': np.random.randint(1, 20, n_customers),
        'monetary': np.random.randint(100, 10000, n_customers),
        'age': np.random.randint(18, 80, n_customers),
        'loyalty_score': np.random.randint(1, 100, n_customers)
    }
    return pd.DataFrame(data)

def preprocess_data(df):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)
    return scaled_data

def apply_kmeans(data, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(data)
    return clusters

def apply_dbscan(data, eps=0.5, min_samples=5):
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    clusters = dbscan.fit_predict(data)
    return clusters

def visualize_clusters(data, clusters, method):
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(data)

    plt.figure(figsize=(10, 8))
    plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=clusters, cmap='viridis')
    plt.title(f'Customer Segments using {method}')
    plt.xlabel('First Principal Component')
    plt.ylabel('Second Principal Component')
    plt.colorbar(label='Cluster')
    plt.savefig(f'{method.lower()}_clusters.png')
    plt.close()

def segment_customers():
    # Load customer data
    df = load_customer_data()

    # Preprocess data
    scaled_data = preprocess_data(df)

    # Apply K-Means
    kmeans_clusters = apply_kmeans(scaled_data)
    visualize_clusters(scaled_data, kmeans_clusters, 'K-Means')

    # Apply DBSCAN
    dbscan_clusters = apply_dbscan(scaled_data)
    visualize_clusters(scaled_data, dbscan_clusters, 'DBSCAN')

    # Add cluster labels to the original dataframe
    df['kmeans_cluster'] = kmeans_clusters
    df['dbscan_cluster'] = dbscan_clusters

    return df

def analyze_segments(df):
    kmeans_analysis = df.groupby('kmeans_cluster').mean()
    dbscan_analysis = df.groupby('dbscan_cluster').mean()

    return {
        'kmeans_segments': kmeans_analysis.to_dict(),
        'dbscan_segments': dbscan_analysis.to_dict()
    }

if __name__ == "__main__":
    segmented_data = segment_customers()
    segment_analysis = analyze_segments(segmented_data)
    print("K-Means Segments:")
    print(segment_analysis['kmeans_segments'])
    print("\nDBSCAN Segments:")
    print(segment_analysis['dbscan_segments'])
