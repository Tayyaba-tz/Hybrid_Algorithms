import random
from typing import List

def generate_random_array(size: int) -> List[int]:
    """
    Generates a list of random integers of a given size.
    
    The values generated are in the range [1, size] and may contain duplicates.
    This is suitable for testing average-case sorting performance and stability.
    
    Args:
        size (int): The number of elements to generate.
        
    Returns:
        List[int]: A list of random integers.
    """
    if size < 0:
        raise ValueError("Size of the array must be non-negative.")
    return [random.randint(1, max(1, size)) for _ in range(size)]

def generate_sorted_array(size: int) -> List[int]:
    """
    Generates a sorted list of integers of a given size.
    
    The values range from 1 to size, in ascending order.
    This represents the best-case scenario for some algorithms (e.g., Insertion Sort).
    
    Args:
        size (int): The number of elements to generate.
        
    Returns:
        List[int]: A sorted list of integers.
    """
    if size < 0:
        raise ValueError("Size of the array must be non-negative.")
    return list(range(1, size + 1))

def generate_reversed_array(size: int) -> List[int]:
    """
    Generates a reversed sorted list of integers of a given size.
    
    The values range from size down to 1, in descending order.
    This represents the worst-case scenario for many traditional algorithms.
    
    Args:
        size (int): The number of elements to generate.
        
    Returns:
        List[int]: A reversed sorted list of integers.
    """
    if size < 0:
        raise ValueError("Size of the array must be non-negative.")
    return list(range(size, 0, -1))
