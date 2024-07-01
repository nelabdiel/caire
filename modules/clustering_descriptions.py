from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
#import numpy as np

def cluster_descriptions(descriptions):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(descriptions)
    
    # Experiment with different eps and min_samples values
    dbscan = DBSCAN(eps=0.3, min_samples=2, metric='cosine')
    clusters = dbscan.fit_predict(X)
    
    # Check the number of clusters found (excluding noise points)
    n_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
    print(f'Estimated number of clusters: {n_clusters}')
    
    return clusters
