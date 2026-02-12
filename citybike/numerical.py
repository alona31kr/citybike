"""
NumPy-based numerical computations for the CityBike platform.

Students should implement:
    - Station distance matrix using Euclidean distance
    - Vectorized trip statistics (mean, median, std, percentiles)
    - Outlier detection using z-scores
    - Vectorized fare calculation across all trips
"""

import numpy as np


# ---------------------------------------------------------------------------
# Distance calculations
# ---------------------------------------------------------------------------

def station_distance_matrix(
    latitudes: np.ndarray, longitudes: np.ndarray
) -> np.ndarray:
    # Ensure arrays
    latitudes = np.asarray(latitudes)
    longitudes = np.asarray(longitudes)

    # Pairwise differences using broadcasting
    lat_diff = latitudes[:, np.newaxis] - latitudes[np.newaxis, :]
    lon_diff = longitudes[:, np.newaxis] - longitudes[np.newaxis, :]

    # Euclidean distance formula
    distances = np.sqrt(lat_diff**2 + lon_diff**2)

    return distances


# ---------------------------------------------------------------------------
# Trip statistics
# ---------------------------------------------------------------------------

def trip_duration_stats(durations: np.ndarray) -> dict[str, float]:
    durations = np.asarray(durations)

    return {
        "mean": float(np.mean(durations)),
        "median": float(np.median(durations)),
        "std": float(np.std(durations)),
        "p25": float(np.percentile(durations, 25)),
        "p75": float(np.percentile(durations, 75)),
        "p90": float(np.percentile(durations, 90)),
    }


# ---------------------------------------------------------------------------
# Outlier detection
# ---------------------------------------------------------------------------
def detect_outliers_zscore(
    values: np.ndarray, threshold: float = 3.0
) -> np.ndarray:
    values = np.asarray(values)

    mean = np.mean(values)
    std = np.std(values)

    if std == 0:
        return np.zeros_like(values, dtype=bool)

    z_scores = (values - mean) / std

    return np.abs(z_scores) > threshold


# ---------------------------------------------------------------------------
# Vectorized fare calculation
# ---------------------------------------------------------------------------

def calculate_fares(
    durations: np.ndarray,
    distances: np.ndarray,
    per_minute: float,
    per_km: float,
    unlock_fee: float = 0.0,
) -> np.ndarray:
    durations = np.asarray(durations)
    distances = np.asarray(distances)

    return unlock_fee + per_minute * durations + per_km * distances
