import numpy as np


def sample_indices_along_distance(distance_m, interval_m=500):
    total = distance_m[-1]
    if total <= 0:
        return [0]
    targets = np.arange(0, total + 1, interval_m)
    indices = [int(np.searchsorted(distance_m, t, side='left')) for t in targets]
    # clamp
    indices = [min(max(0, idx), len(distance_m) - 1) for idx in indices]
    # unique and ordered
    indices = sorted(set(indices))
    return indices