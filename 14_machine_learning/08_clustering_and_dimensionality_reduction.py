# Unsupervised learning: no labels. Find groups and simplify data.

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.datasets import load_iris, make_blobs, make_moons
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler

# %% K-means: put points into k groups
X, true_groups = make_blobs(n_samples=300, centers=4, cluster_std=0.8, random_state=3)
kmeans = KMeans(n_clusters=4, n_init=10, random_state=0).fit(X)
print(kmeans.labels_[:10], kmeans.cluster_centers_.round(1))
print("points per cluster:", np.bincount(kmeans.labels_))

# %% How many clusters? Try several and measure
for k in range(2, 8):
    model = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    print(f"k={k} inertia={model.inertia_:8.1f} silhouette={silhouette_score(X, model.labels_):.3f}")
# Inertia always falls with bigger k (look for the elbow). Silhouette: higher is better (max 1).

# %% Other algorithms
hier = AgglomerativeClustering(n_clusters=4).fit(X)
print("hierarchical agrees with truth:", round(adjusted_rand_score(true_groups, hier.labels_), 2))

moons, _ = make_moons(n_samples=300, noise=0.07, random_state=0)
print("kmeans on moons ARI:", round(adjusted_rand_score(_, KMeans(2, n_init=10, random_state=0).fit_predict(moons)), 2))
db = DBSCAN(eps=0.2, min_samples=5).fit(moons)
print("dbscan on moons ARI:", round(adjusted_rand_score(_, db.labels_), 2), "(label -1 = noise)")

# %% Customer segmentation example: scale first, then cluster
rng = np.random.default_rng(0)
customers = pd.DataFrame({
    "orders": np.r_[rng.poisson(2, 100), rng.poisson(12, 60), rng.poisson(30, 20)],
    "avg_basket": np.r_[rng.normal(20, 5, 100), rng.normal(45, 8, 60), rng.normal(90, 15, 20)],
})
scaled = StandardScaler().fit_transform(customers)
customers["segment"] = KMeans(3, n_init=10, random_state=0).fit_predict(scaled)
print(customers.groupby("segment").agg(people=("orders", "size"), orders=("orders", "mean"), basket=("avg_basket", "mean")).round(1))

# %% PCA: squash many columns into a few that keep most of the information
iris = load_iris(as_frame=True)
iris_scaled = StandardScaler().fit_transform(iris.data)
pca = PCA(n_components=2).fit(iris_scaled)
print("variance kept:", pca.explained_variance_ratio_.round(3), pca.explained_variance_ratio_.sum().round(3))
reduced = pca.transform(iris_scaled)
print(reduced.shape)
print(pd.DataFrame(pca.components_, columns=iris.data.columns, index=["PC1", "PC2"]).round(2))
print("components needed for 95%:", PCA(0.95).fit(iris_scaled).n_components_)

# %% t-SNE: for pictures only (do not use it as features)
tsne = TSNE(n_components=2, random_state=0, perplexity=20).fit_transform(iris_scaled)
print(tsne.shape)

# %% Anomaly detection idea: far from every cluster centre = unusual
distances = np.min(KMeans(3, n_init=10, random_state=0).fit(iris_scaled).transform(iris_scaled), axis=1)
print("most unusual rows:", np.argsort(distances)[-3:])

# %% Uses in AI work
# Embeddings (folder 10) + clustering = group similar documents or support tickets.
# PCA / t-SNE / UMAP = visualize embeddings.
