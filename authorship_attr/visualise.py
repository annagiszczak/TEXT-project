import pandas as pd
import seaborn as sns
from sklearn.manifold import MDS
from matplotlib import pyplot as plt
import numpy as np

def show_distance_heatmap(distances, authors):
    distance_matrix = pd.DataFrame(index=authors, columns=authors, dtype=float)

    # Fill matrix with given distances
    for (a1, a2), dist in distances.items():
        distance_matrix.loc[a1, a2] = dist
        distance_matrix.loc[a2, a1] = dist  # Symmetric
    # Plot heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(distance_matrix, cmap="coolwarm", annot=True, fmt=".2f", annot_kws={'fontsize':6})
    plt.title("Heatmap of Pairwise Distances")
    plt.show()

def show_mds_embedding(distances, authors):
    distance_matrix = pd.DataFrame(index=authors, columns=authors, dtype=float)

    for (a1, a2), dist in distances.items():
        distance_matrix.loc[a1, a2] = dist
        distance_matrix.loc[a2, a1] = dist  # Symmetric


    np.fill_diagonal(distance_matrix.values, 0)

    mds = MDS(n_components=2, dissimilarity="precomputed")
    coords = mds.fit_transform(distance_matrix)

    mds_df = pd.DataFrame(coords, index=authors, columns=["x", "y"])

    plt.figure(figsize=(8, 6))
    plt.scatter(mds_df["x"], mds_df["y"], color="red")

    for author, (x, y) in mds_df.iterrows():
        plt.text(x, y, author, fontsize=12, ha='right', va='bottom')

    plt.title("MDS Representation of Author Distances")
    plt.xlabel("MDS Dimension 1")
    plt.ylabel("MDS Dimension 2")
    plt.grid(True)
    plt.show()