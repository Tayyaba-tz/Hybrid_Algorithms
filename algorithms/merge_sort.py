def merge_sort(arr, start=0, end=None):
    """
    Sorts an array using Merge Sort and yields state for visualization.
    """
    if end is None:
        end = len(arr)
        arr = arr.copy()
        # Initialize stats for the recursive calls
        merge_sort.comparisons = 0
        merge_sort.swaps = 0

    if end - start > 1:
        mid = (start + end) // 2
        yield from merge_sort(arr, start, mid)
        yield from merge_sort(arr, mid, end)
        yield from merge(arr, start, mid, end)

    if start == 0 and end == len(arr):
        return arr, merge_sort.comparisons, merge_sort.swaps

def merge(arr, start, mid, end):
    """
    Merges two sorted sub-arrays and yields state.
    """
    left = arr[start:mid]
    right = arr[mid:end]
    
    i = 0
    j = 0
    k = start
    
    while i < len(left) and j < len(right):
        merge_sort.comparisons += 1
        # Highlight elements being compared
        yield arr.copy(), merge_sort.comparisons, merge_sort.swaps, {"red": [start + i, mid + j]}
        
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        merge_sort.swaps += 1
        k += 1
        yield arr.copy(), merge_sort.comparisons, merge_sort.swaps, {"orange": [k-1]}

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
        merge_sort.swaps += 1
        yield arr.copy(), merge_sort.comparisons, merge_sort.swaps, {"orange": [k-1]}

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
        merge_sort.swaps += 1
        yield arr.copy(), merge_sort.comparisons, merge_sort.swaps, {"orange": [k-1]}
