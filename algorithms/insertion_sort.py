def insertion_sort(arr):
    """
    Sorts an array using Insertion Sort and yields state for visualization.
    """
    arr = arr.copy()
    comparisons = 0
    swaps = 0

    for j in range(1, len(arr)):
        key = arr[j]
        i = j - 1
        
        # Highlight the key being placed
        yield arr.copy(), comparisons, swaps, {"orange": [j]}

        while i >= 0:
            comparisons += 1
            # Highlight elements being compared
            yield arr.copy(), comparisons, swaps, {"red": [i, i+1]}
            
            if arr[i] > key:
                arr[i + 1] = arr[i]
                swaps += 1
                i -= 1
                yield arr.copy(), comparisons, swaps, {"orange": [i+1]}
            else:
                break
        
        arr[i + 1] = key
        # One swap for the final placement if it moved
        if i + 1 != j:
            swaps += 1
        yield arr.copy(), comparisons, swaps, {"green": list(range(j + 1))}

    return arr, comparisons, swaps
