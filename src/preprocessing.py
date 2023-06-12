from sklearn.cluster import DBSCAN
import numpy as np


def process_subset(subset, eps, min_samples):
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(subset)
    return np.where(labels == -1)[0]


def merge_results(results):
    merged_labels = []
    current_index = 0
    for subset_labels in results:
        merged_labels.extend(subset_labels + current_index)
        current_index += len(np.unique(subset_labels))
    return merged_labels


def preprocessing(points, colors, eps, min_samples, subset_size):
    print("Started Preprocessing!")
    num_subsets = len(points) // subset_size
    subsets = np.array_split(points, num_subsets)
    subset_results = []
    i = 0
    for subset in subsets:
        subset_labels = process_subset(subset, eps, min_samples)
        subset_results.append(subset_labels)
        i += 1
        print(i, "/", num_subsets, " Batches done.")
    merged_labels = merge_results(subset_results)
    points = np.delete(points, merged_labels, axis=0)
    colors = np.delete(colors, merged_labels, axis=0)
    print("Preprocessing done!")
    return points, colors
