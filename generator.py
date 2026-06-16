import random

def generate_random(n, lo=1, hi=1000):
    """
    Generates an array of n random integers between lo and hi.
    """
    return [random.randint(lo, hi) for _ in range(n)]

def generate_sorted(n):
    """
    Generates a sorted array of n integers from 1 to n.
    """
    return list(range(1, n + 1))

def generate_reversed(n):
    """
    Generates a reversed array of n integers from n down to 1.
    """
    return list(range(n, 0, -1))

def generate_nearly_sorted(n):
    """
    Generates a nearly sorted array by taking a sorted array and performing 5% random swaps.
    """
    arr = list(range(1, n + 1))
    # Perform approximately 5% swaps
    num_swaps = max(1, n // 20)
    for _ in range(num_swaps):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def generate_repeated(n):
    """
    Generates an array of n integers where only 10 unique values exist, repeated many times.
    """
    unique_values = [random.randint(1, 100) for _ in range(10)]
    return [random.choice(unique_values) for _ in range(n)]
