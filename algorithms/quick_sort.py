def quick_sort(arr, low=0, high=None):
    """
    Sorts an array using Quick Sort and yields state for visualization.
    """
    if high is None:
        high = len(arr) - 1
        arr = arr.copy()
        quick_sort.comparisons = 0
        quick_sort.swaps = 0

    if low < high:
        # Partition and get pivot index
        pivot_gen = partition(arr, low, high)
        pivot_idx = None
        try:
            while True:
                val = next(pivot_gen)
                if isinstance(val, tuple):
                    yield val
                else:
                    pivot_idx = val
                    break
        except StopIteration as e:
            pivot_idx = e.value

        yield from quick_sort(arr, low, pivot_idx - 1)
        yield from quick_sort(arr, pivot_idx + 1, high)

    if low == 0 and high == len(arr) - 1:
        return arr, quick_sort.comparisons, quick_sort.swaps

def partition(arr, low, high):
    """
    Partitions the array using the last element as pivot.
    """
    pivot = arr[high]
    i = low - 1
    
    # Highlight pivot
    yield arr.copy(), quick_sort.comparisons, quick_sort.swaps, {"orange": [high]}
    
    for j in range(low, high):
        quick_sort.comparisons += 1
        # Highlight elements being compared
        yield arr.copy(), quick_sort.comparisons, quick_sort.swaps, {"red": [j, high]}
        
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            quick_sort.swaps += 1
            yield arr.copy(), quick_sort.comparisons, quick_sort.swaps, {"red": [i, j]}

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    quick_sort.swaps += 1
    yield arr.copy(), quick_sort.comparisons, quick_sort.swaps, {"green": [i + 1]}
    
    return i + 1
