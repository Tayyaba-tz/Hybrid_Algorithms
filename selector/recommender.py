def count_inversions(arr):
    """
    Counts the number of inversions in an array.
    An inversion is when a larger element appears before a smaller one.
    """
    count = 0
    n = len(arr)
    # Simple O(n^2) approach, but we cap it to keep it efficient for the recommender
    limit = n * 2
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
                if count > limit:
                    return count
    return count

def select_algorithm(arr):
    """
    Recommends the best sorting algorithm based on the dataset characteristics.
    """
    n = len(arr)

    # Rule 1: Very small arrays
    if n < 32:
        return 'Insertion Sort', 'Array is tiny (n < 32). Insertion Sort is fastest for small arrays.'

    # Rule 2: Check if already sorted
    is_sorted = True
    for i in range(len(arr) - 1):
        if arr[i] > arr[i+1]:
            is_sorted = False
            break
    
    if is_sorted:
        return 'TimSort', 'Array is already sorted. TimSort detects this and runs in O(n).'

    # Rule 3: Count inversions to detect nearly-sorted data
    inversions = count_inversions(arr)
    if inversions < n * 2:
        return 'TimSort', f'Nearly sorted data ({inversions} inversions). TimSort exploits natural runs.'

    # Rule 4: Large random data
    if n > 10000:
        return 'Heap Sort', 'Large dataset. Heap Sort guarantees O(n log n) with O(1) extra space.'

    # Rule 5: Medium random data
    return 'Quick Sort', 'Medium random dataset. Quick Sort has the fastest average-case constants.'
