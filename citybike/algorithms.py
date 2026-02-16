import timeit
from collections.abc import Callable
from typing import Any

# ---------------------------------------------------------------------------
# Sorting — Merge Sort
# ---------------------------------------------------------------------------

def merge_sort(data: list[Any], key: Callable = lambda x: x) -> list[Any]:
    """Merge sort algorithm. Complexity: O(n log n)."""
    if len(data) <= 1:
        return list(data)

    mid = len(data) // 2
    left = merge_sort(data[:mid], key=key)
    right = merge_sort(data[mid:], key=key)

    return _merge(left, right, key=key)


def _merge(left: list[Any], right: list[Any], key: Callable) -> list[Any]:
    """Merge two sorted lists into a single sorted list."""
    result: list[Any] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# ---------------------------------------------------------------------------
# Sorting — Insertion Sort
# ---------------------------------------------------------------------------

def insertion_sort(data: list[Any], key: Callable = lambda x: x) -> list[Any]:
    """
    Insertion sort algorithm.
    Complexity:
        Time  — O(n²) worst/average, O(n) best
        Space — O(n)
    """
    arr = list(data)
    for i in range(1, len(arr)):
        current = arr[i]
        current_key = key(current)  # Виклик key один раз
        j = i - 1
        while j >= 0 and key(arr[j]) > current_key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr

# ---------------------------------------------------------------------------
# Searching — Binary Search
# ---------------------------------------------------------------------------

def binary_search(sorted_data: list[Any], target: Any, key: Callable = lambda x: x) -> int | None:
    """
    Binary search algorithm (for sorted lists only).
    Complexity:
        Time  — O(log n)
        Space — O(1)
    """
    low, high = 0, len(sorted_data) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_val = key(sorted_data[mid])
        if mid_val == target:
            return mid
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
    return None

# ---------------------------------------------------------------------------
# Searching — Linear Search
# ---------------------------------------------------------------------------

def linear_search(data: list[Any], target: Any, key: Callable = lambda x: x) -> int | None:
    """
    Linear search (brute-force).
    Complexity:
        Time  — O(n)
        Space — O(1)
    """
    for index, item in enumerate(data):
        if key(item) == target:
            return index
    return None

# ---------------------------------------------------------------------------
# Benchmarking helpers
# ---------------------------------------------------------------------------

REPEATS_SORT = 5
REPEATS_SEARCH = 10

def benchmark_sort(data: list, key: Callable = lambda x: x, repeats: int = REPEATS_SORT) -> dict:
    """Compare merge_sort, insertion_sort, and built-in sorted()."""
    merge_time = timeit.timeit(lambda: merge_sort(data, key=key), number=repeats)
    insert_time = timeit.timeit(lambda: insertion_sort(data, key=key), number=repeats)
    builtin_time = timeit.timeit(lambda: sorted(data, key=key), number=repeats)

    return {
        "merge_sort_ms": round(merge_time / repeats * 1000, 4),
        "insertion_sort_ms": round(insert_time / repeats * 1000, 4),
        "builtin_sorted_ms": round(builtin_time / repeats * 1000, 4),
    }


def benchmark_search(data_sorted: list, target: Any, key: Callable = lambda x: x, repeats: int = REPEATS_SEARCH) -> dict:
    """Compare binary_search, linear_search, and built-in 'in' operator."""
    binary_time = timeit.timeit(lambda: binary_search(data_sorted, target, key=key), number=repeats)
    linear_time = timeit.timeit(lambda: linear_search(data_sorted, target, key=key), number=repeats)
    builtin_time = timeit.timeit(lambda: any(key(x) == target for x in data_sorted), number=repeats)

    return {
        "binary_search_ms": round(binary_time / repeats * 1000, 4),
        "linear_search_ms": round(linear_time / repeats * 1000, 4),
        "builtin_in_ms": round(builtin_time / repeats * 1000, 4),
    }



