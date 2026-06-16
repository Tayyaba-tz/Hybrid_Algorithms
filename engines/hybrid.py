from typing import Generator, Dict, List, Tuple, Any, Optional
from engines.base_sort import BaseSort

class HybridSort(BaseSort):
    """
    Hybrid Sort (Timsort-inspired) implementation.
    
    Divides the array into small blocks of size RUN (default 32),
    sorts them using Insertion Sort, and then merges them iteratively using Merge Sort.
    
    Every step of both phases yields a state dictionary for frame-by-frame animation.
    """

    def __init__(self, run_size: int = 32):
        """
        Initializes the HybridSort engine.
        
        Args:
            run_size (int): The size of sub-arrays/runs to sort via insertion sort before merging.
        """
        self.run_size = run_size

    def sort(self, array: List[Any]) -> Generator[Dict[str, Any], None, None]:
        n = len(array)
        if n <= 1:
            return

        # Phase 1: Sort individual sub-arrays/runs of size RUN using Insertion Sort
        for start in range(0, n, self.run_size):
            end = min(start + self.run_size - 1, n - 1)
            yield from self._insertion_sort(array, start, end)

        # Phase 2: Merge sorted sub-arrays iteratively (bottom-up merge)
        curr_size = self.run_size
        while curr_size < n:
            for left in range(0, n, 2 * curr_size):
                mid = min(left + curr_size - 1, n - 1)
                right = min(left + 2 * curr_size - 1, n - 1)

                # Merge sub-arrays array[left...mid] and array[mid+1...right] if they exist
                if mid < right:
                    yield from self._merge(array, left, mid, right)
            curr_size *= 2

    def _insertion_sort(self, array: List[Any], start: int, end: int) -> Generator[Dict[str, Any], None, None]:
        """
        Insertion Sort helper for sorting a specific sub-array range in-place.
        """
        for i in range(start + 1, end + 1):
            key = array[i]
            j = i - 1
            while j >= start:
                yield {
                    "array": list(array),
                    "comparing": (j, j + 1),
                    "swapping": None
                }
                if array[j] > key:
                    array[j + 1] = array[j]
                    yield {
                        "array": list(array),
                        "comparing": None,
                        "swapping": (j, j + 1)
                    }
                    j -= 1
                else:
                    break
            array[j + 1] = key
            yield {
                "array": list(array),
                "comparing": None,
                "swapping": (j + 1, j + 1)
            }

    def _merge(self, array: List[Any], l: int, mid: int, r: int) -> Generator[Dict[str, Any], None, None]:
        """
        Merge Sort merge helper for merging two sorted contiguous sub-arrays in-place.
        """
        # Create a copy of the active subarray segment to act as reference
        aux = list(array)
        i = l
        j = mid + 1
        k = l

        while i <= mid and j <= r:
            yield {
                "array": list(array),
                "comparing": (i, j),
                "swapping": None
            }
            if aux[i] <= aux[j]:
                array[k] = aux[i]
                yield {
                    "array": list(array),
                    "comparing": None,
                    "swapping": (k, i)
                }
                i += 1
            else:
                array[k] = aux[j]
                yield {
                    "array": list(array),
                    "comparing": None,
                    "swapping": (k, j)
                }
                j += 1
            k += 1

        # Copy any remaining elements from the left sub-array
        while i <= mid:
            array[k] = aux[i]
            yield {
                "array": list(array),
                "comparing": None,
                "swapping": (k, i)
            }
            i += 1
            k += 1

        # Copy any remaining elements from the right sub-array
        while j <= r:
            array[k] = aux[j]
            yield {
                "array": list(array),
                "comparing": None,
                "swapping": (k, j)
            }
            j += 1
            k += 1
