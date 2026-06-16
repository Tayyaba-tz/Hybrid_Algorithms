def timsort(arr):
    """
    Sorts an array using a TimSort-inspired hybrid (Insertion Sort + Merge Sort).
    """
    arr = arr.copy()
    n = len(arr)
    min_run = 32
    comparisons = 0
    swaps = 0

    # Step 1: Sort individual subarrays of size min_run
    for start in range(0, n, min_run):
        end = min(start + min_run, n)
        # Insertion sort on the run
        for i in range(start + 1, end):
            key = arr[i]
            j = i - 1
            while j >= start:
                comparisons += 1
                yield arr.copy(), comparisons, swaps, {"red": [j, j+1]}
                if arr[j] > key:
                    arr[j+1] = arr[j]
                    swaps += 1
                    j -= 1
                    yield arr.copy(), comparisons, swaps, {"orange": [j+1]}
                else:
                    break
            arr[j+1] = key
            if j + 1 != i:
                swaps += 1
            yield arr.copy(), comparisons, swaps, {"orange": [j+1]}

    # Step 2: Merge sorted runs
    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n, left + size)
            right = min(n, left + 2 * size)
            
            if mid < right:
                # Merge step
                l_arr = arr[left:mid]
                r_arr = arr[mid:right]
                i = 0
                j = 0
                k = left
                
                while i < len(l_arr) and j < len(r_arr):
                    comparisons += 1
                    yield arr.copy(), comparisons, swaps, {"red": [left + i, mid + j]}
                    if l_arr[i] <= r_arr[j]:
                        arr[k] = l_arr[i]
                        i += 1
                    else:
                        arr[k] = r_arr[j]
                        j += 1
                    swaps += 1
                    k += 1
                    yield arr.copy(), comparisons, swaps, {"orange": [k-1]}
                
                while i < len(l_arr):
                    arr[k] = l_arr[i]
                    i += 1
                    k += 1
                    swaps += 1
                    yield arr.copy(), comparisons, swaps, {"orange": [k-1]}
                
                while j < len(r_arr):
                    arr[k] = r_arr[j]
                    j += 1
                    k += 1
                    swaps += 1
                    yield arr.copy(), comparisons, swaps, {"orange": [k-1]}
        size *= 2

    return arr, comparisons, swaps
