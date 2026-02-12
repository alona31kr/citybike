"""
Unit tests for the numerical module.

Covers:
    - trip_duration_stats
    - calculate_fares
    - detect_outliers_zscore
    - station_distance_matrix
"""

import pytest
import numpy as np

from numerical import (
    trip_duration_stats,
    calculate_fares,
    detect_outliers_zscore,
    station_distance_matrix,
)


# ---------------------------------------------------------------------------
# trip_duration_stats
# ---------------------------------------------------------------------------

class TestTripDurationStats:

    def test_basic_stats(self) -> None:
        durations = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
        stats = trip_duration_stats(durations)
        assert stats["mean"] == pytest.approx(30.0)
        assert stats["median"] == pytest.approx(30.0)

    def test_std(self) -> None:
        durations = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
        stats = trip_duration_stats(durations)
        assert stats["std"] == pytest.approx(np.std(durations))

    def test_single_value(self) -> None:
        durations = np.array([42.0])
        stats = trip_duration_stats(durations)
        assert stats["mean"] == pytest.approx(42.0)
        assert stats["median"] == pytest.approx(42.0)
        assert stats["std"] == pytest.approx(0.0)

    def test_percentiles(self) -> None:
        durations = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
        stats = trip_duration_stats(durations)
        assert stats["p25"] == pytest.approx(20.0)
        assert stats["p75"] == pytest.approx(40.0)
        assert stats["p90"] == pytest.approx(46.0)  # 90th percentile

    def test_returns_expected_keys(self) -> None:
        durations = np.array([1.0, 2.0, 3.0])
        stats = trip_duration_stats(durations)
        for key in ["mean", "median", "std", "p25", "p75", "p90"]:
            assert key in stats

    def test_values_are_floats(self) -> None:
        durations = np.array([5.0, 15.0, 25.0])
        stats = trip_duration_stats(durations)
        for val in stats.values():
            assert isinstance(val, float)


# ---------------------------------------------------------------------------
# calculate_fares
# ---------------------------------------------------------------------------

class TestCalculateFares:

    def test_basic_fare_calculation(self) -> None:
        durations = np.array([10, 20, 30])
        distances = np.array([2.0, 5.0, 8.0])
        fares = calculate_fares(durations, distances, per_minute=0.15, per_km=0.10, unlock_fee=1.0)
        expected = np.array([2.7, 4.5, 6.3])
        assert np.allclose(fares, expected)

    def test_no_unlock_fee(self) -> None:
        durations = np.array([10, 20])
        distances = np.array([2.0, 5.0])
        fares = calculate_fares(durations, distances, per_minute=0.1, per_km=0.05)
        expected = np.array([1.1, 2.25])
        assert np.allclose(fares, expected)

    def test_zero_duration_and_distance(self) -> None:
        durations = np.array([0, 0])
        distances = np.array([0.0, 0.0])
        fares = calculate_fares(durations, distances, per_minute=0.1, per_km=0.05, unlock_fee=1.0)
        expected = np.array([1.0, 1.0])
        assert np.allclose(fares, expected)


# ---------------------------------------------------------------------------
# detect_outliers_zscore
# ---------------------------------------------------------------------------

import pytest
import numpy as np
from numerical import detect_outliers_zscore

# ---------------------------------------------------------------------------
# detect_outliers_zscore
# ---------------------------------------------------------------------------

class TestDetectOutliersZscore:

    def test_no_outliers_default_threshold(self) -> None:
        values = np.array([10.0, 12.0, 11.0, 13.0, 12.5])
        outliers = detect_outliers_zscore(values)
        expected = np.array([False, False, False, False, False])
        assert np.array_equal(outliers, expected)

    def test_basic_outliers_lower_threshold(self) -> None:
        values = np.array([10.0, 20.0, 30.0, 100.0, 50.0])
        # Lower threshold to actually detect the 100 as an outlier
        outliers = detect_outliers_zscore(values, threshold=1.5)
        expected = np.array([False, False, False, True, False])
        assert np.array_equal(outliers, expected)

    def test_single_value(self) -> None:
        values = np.array([42.0])
        outliers = detect_outliers_zscore(values)
        expected = np.array([False])  # no outliers
        assert np.array_equal(outliers, expected)

    def test_all_same_values(self) -> None:
        values = np.array([7.0, 7.0, 7.0])
        outliers = detect_outliers_zscore(values)
        expected = np.array([False, False, False])  # std=0 → no outliers
        assert np.array_equal(outliers, expected)

    def test_negative_values_and_outliers(self) -> None:
        values = np.array([-10.0, -20.0, -30.0, -100.0, -50.0])
        outliers = detect_outliers_zscore(values, threshold=1.5)
        expected = np.array([False, False, False, True, False])
        assert np.array_equal(outliers, expected)


# ---------------------------------------------------------------------------
# station_distance_matrix
# ---------------------------------------------------------------------------

class TestStationDistanceMatrix:

    def test_basic_distance_matrix(self) -> None:
        lats = np.array([0.0, 0.0])
        lons = np.array([0.0, 3.0])
        matrix = station_distance_matrix(lats, lons)
        expected = np.array([[0.0, 3.0], [3.0, 0.0]])
        assert np.allclose(matrix, expected)

    def test_square_matrix_shape(self) -> None:
        lats = np.array([0.0, 1.0, 2.0])
        lons = np.array([0.0, 1.0, 2.0])
        matrix = station_distance_matrix(lats, lons)
        assert matrix.shape == (3, 3)

    def test_diagonal_is_zero(self) -> None:
        lats = np.array([1.0, 2.0, 3.0])
        lons = np.array([4.0, 5.0, 6.0])
        matrix = station_distance_matrix(lats, lons)
        assert np.allclose(np.diag(matrix), 0.0)

    def test_empty_input(self) -> None:
        lats = np.array([])
        lons = np.array([])
        matrix = station_distance_matrix(lats, lons)
        assert matrix.shape == (0, 0)
