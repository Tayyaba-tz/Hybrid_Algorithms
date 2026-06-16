def heap_sort(arr):
    """
    Sorts an array using Heap Sort and yields state for visualization.
    """
    arr = arr.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        gen = heapify(arr, n, i, comparisons, swaps)
        try:
            while True:
                val = next(gen)
                yield val[:3] + (val[3],)
                comparisons, swaps = val[1], val[2]
        except StopIteration as e:
            comparisons, swaps = e.value

    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        swaps += 1
        yield arr.copy(), comparisons, swaps, {"green": list(range(i, n))}
        
        gen = heapify(arr, i, 0, comparisons, swaps)
        try:
            while True:
                val = next(gen)
                yield val[:3] + (val[3],)
                comparisons, swaps = val[1], val[2]
        except StopIteration as e:
            comparisons, swaps = e.value

    return arr, comparisons, swaps

def heapify(arr, n, i, comparisons, swaps):
    """
    Heapifies a subtree rooted at index i.
    """
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n:
        comparisons += 1
        yield arr.copy(), comparisons, swaps, {"red": [l, largest]}
        if arr[l] > arr[largest]:
            largest = l

    if r < n:
        comparisons += 1
        yield arr.copy(), comparisons, swaps, {"red": [r, largest]}
        if arr[r] > arr[largest]:
            largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        swaps += 1
        yield arr.copy(), comparisons, swaps, {"orange": [i, largest]}
        
        gen = heapify(arr, n, largest, comparisons, swaps)
        try:
            while True:
                val = next(gen)
                yield val
                comparisons, swaps = val[1], val[2]
        except StopIteration as e:
            comparisons, swaps = e.value

    return comparisons, swaps
