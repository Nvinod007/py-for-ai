# Unsupervised learning: no labels. Find groups and simplify data.
# Each line has a short comment saying WHAT it is.

# numpy: arrays and maths.
import numpy as np
# pandas: tables.
import pandas as pd
# KMeans: k groups around centres; DBSCAN: groups by crowded areas, outliers = noise; AgglomerativeClustering: merges closest points step by step.
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
# Make-up/example datasets: make_blobs, make_moons, load_iris.
from sklearn.datasets import load_iris, make_blobs, make_moons
# PCA: squashes many columns into a few.
from sklearn.decomposition import PCA
# TSNE: squashes data to 2D for pictures.
from sklearn.manifold import TSNE
# silhouette_score: how well separated clusters are; adjusted_rand_score: match with true groups (1 = perfect).
from sklearn.metrics import adjusted_rand_score, silhouette_score
# StandardScaler: rescales columns.
from sklearn.preprocessing import StandardScaler

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% K-means: put points into k groups
# make_blobs(n_samples, centers, cluster_std, random_state): fake points in 4 clumps; cluster_std = how spread out each clump is.
X, true_groups = make_blobs(n_samples=300, centers=4, cluster_std=0.8, random_state=3)
# KMeans(n_clusters=4, n_init=10): 4 groups; n_init = number of restarts, keeps the best; fit(X) finds the groups.
kmeans = KMeans(n_clusters=4, n_init=10, random_state=0).fit(X)
# labels_ = group number of each point; cluster_centers_ = group centres.
print(kmeans.labels_[:10], kmeans.cluster_centers_.round(1))
# np.bincount: counts of each group number.
print("points per cluster:", np.bincount(kmeans.labels_))

# %% How many clusters? Try several and measure
# range(2, 8): try k = 2..7.
for k in range(2, 8):
    # Train a model with k groups.
    model = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    # inertia_ = total distance to centres (smaller = tighter); silhouette_score(X, labels) = separation quality.
    print(f"k={k} inertia={model.inertia_:8.1f} silhouette={silhouette_score(X, model.labels_):.3f}")
# Inertia always falls with bigger k (look for the elbow). Silhouette: higher is better (max 1).

# %% Other algorithms
# AgglomerativeClustering(n_clusters=4): bottom-up clustering.
hier = AgglomerativeClustering(n_clusters=4).fit(X)
# adjusted_rand_score(true, found): 1 = same grouping, ~0 = random.
print("hierarchical agrees with truth:", round(adjusted_rand_score(true_groups, hier.labels_), 2))

# make_moons: two curved half-moons; noise = jitter; _ holds the true groups.
moons, _ = make_moons(n_samples=300, noise=0.07, random_state=0)
# fit_predict(X): fit and return group labels in one step.
print("kmeans on moons ARI:", round(adjusted_rand_score(_, KMeans(2, n_init=10, random_state=0).fit_predict(moons)), 2))
# DBSCAN(eps=0.2, min_samples=5): eps = neighbour distance, min_samples = points needed for a crowd.
db = DBSCAN(eps=0.2, min_samples=5).fit(moons)
# Label -1 means noise (not in any group).
print("dbscan on moons ARI:", round(adjusted_rand_score(_, db.labels_), 2), "(label -1 = noise)")

# %% Customer segmentation example: scale first, then cluster
# np.random.default_rng(0): fixed-seed random maker.
rng = np.random.default_rng(0)
# np.r_[a, b, c] joins arrays; rng.poisson(n, size) makes counts around n; rng.normal(mean, spread, size) makes bell-curve numbers.
customers = pd.DataFrame({
    "orders": np.r_[rng.poisson(2, 100), rng.poisson(12, 60), rng.poisson(30, 20)],
    "avg_basket": np.r_[rng.normal(20, 5, 100), rng.normal(45, 8, 60), rng.normal(90, 15, 20)],
})
# fit_transform(data): learn the scaling and apply it.
scaled = StandardScaler().fit_transform(customers)
# KMeans(3).fit_predict(scaled): assign each customer a group number.
customers["segment"] = KMeans(3, n_init=10, random_state=0).fit_predict(scaled)
# groupby('segment').agg(...): one summary row per group (size = count, mean = average).
print(customers.groupby("segment").agg(people=("orders", "size"), orders=("orders", "mean"), basket=("avg_basket", "mean")).round(1))

# %% PCA: squash many columns into a few that keep most of the information
# load_iris(as_frame=True): famous flower dataset as tables.
iris = load_iris(as_frame=True)
# Scale columns so none dominates.
iris_scaled = StandardScaler().fit_transform(iris.data)
# PCA(n_components=2): keep 2 new columns that hold the most information.
pca = PCA(n_components=2).fit(iris_scaled)
# explained_variance_ratio_: share of information each new column keeps.
print("variance kept:", pca.explained_variance_ratio_.round(3), pca.explained_variance_ratio_.sum().round(3))
# transform(data): apply the squashing.
reduced = pca.transform(iris_scaled)
# shape = (rows, columns).
print(reduced.shape)
# components_: how much each original column feeds each new column.
print(pd.DataFrame(pca.components_, columns=iris.data.columns, index=["PC1", "PC2"]).round(2))
# PCA(0.95): keep as many columns as needed for 95% of the information.
print("components needed for 95%:", PCA(0.95).fit(iris_scaled).n_components_)


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% t-SNE: for pictures only (do not use it as features)
# TSNE(n_components=2, perplexity=20): 2D map where similar points sit close; perplexity ~ neighbours considered.
tsne = TSNE(n_components=2, random_state=0, perplexity=20).fit_transform(iris_scaled)
# shape = (rows, columns).
print(tsne.shape)

# %% Anomaly detection idea: far from every cluster centre = unusual
# transform(X): distance to each centre; np.min(axis=1) keeps the nearest one per row.
distances = np.min(KMeans(3, n_init=10, random_state=0).fit(iris_scaled).transform(iris_scaled), axis=1)
# np.argsort: row numbers ordered by size; [-3:] = the 3 largest.
print("most unusual rows:", np.argsort(distances)[-3:])

# %% Uses in AI work
# Embeddings (folder 10) + clustering = group similar documents or support tickets.
# PCA / t-SNE / UMAP = visualize embeddings.
