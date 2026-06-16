from typing import Generator, Dict, List, Tuple, Any, Optional
from engines.base_sort import BaseSort

class InsertionSort(BaseSort):
    """
    Insertion Sort implementation.
    
    Iterates through the array, consuming one input element each repetition,
    and growing a sorted output list.
    """
    
    def sort(self, array: List[Any]) -> Generator[Dict[str, Any], None, None]:
        n = len(array)
        for i in range(1, n):
            key = array[i]
            j = i - 1
            # Shift elements of array[0..i-1] that are greater than key
            while j >= 0:
                # Yield comparison frame
                yield {
                    "array": list(array),
                    "comparing": (j, j + 1),
                    "swapping": None
                }
                if array[j] > key:
                    array[j + 1] = array[j]
                    # Yield shift (overwrite) frame
                    yield {
                        "array": list(array),
                        "comparing": None,
                        "swapping": (j, j + 1)
                    }
                    j -= 1
                else:
                    break
            array[j + 1] = key
            # Yield placement of the key
            yield {
                "array": list(array),
                "comparing": None,
                "swapping": (j + 1, j + 1)
            }


class MergeSort(BaseSort):
    """
    Merge Sort implementation.
    
    A divide-and-conquer algorithm that divides the input array into two halves,
    calls itself for the two halves, and then merges the two sorted halves.
    """
    
    def sort(self, array: List[Any]) -> Generator[Dict[str, Any], None, None]:
        yield from self._merge_sort(array, 0, len(array) - 1)

    def _merge_sort(self, array: List[Any], l: int, r: int) -> Generator[Dict[str, Any], None, None]:
        if l < r:
            mid = (l + r) // 2
            # Recursively sort first and second halves
            yield from self._merge_sort(array, l, mid)
            yield from self._merge_sort(array, mid + 1, r)
            # Merge the sorted halves
            yield from self._merge(array, l, mid, r)

    def _merge(self, array: List[Any], l: int, mid: int, r: int) -> Generator[Dict[str, Any], None, None]:
        # Create a copy of the subarray to serve as our comparison reference
        aux = list(array)
        i = l
        j = mid + 1
        k = l

        while i <= mid and j <= r:
            # Compare elements from the auxiliary snapshot
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

        # Copy any remaining elements from the left subarray
        while i <= mid:
            array[k] = aux[i]
            yield {
                "array": list(array),
                "comparing": None,
                "swapping": (k, i)
            }
            i += 1
            k += 1

        # Copy any remaining elements from the right subarray
        while j <= r:
            array[k] = aux[j]
            yield {
                "array": list(array),
                "comparing": None,
                "swapping": (k, j)
            }
            j += 1
            k += 1


class QuickSort(BaseSort):
    """
    Quick Sort implementation (Lomuto partitioning).
    
    A divide-and-conquer algorithm that picks an element as a pivot and partitions
    the given array around the picked pivot.
    """
    
    def sort(self, array: List[Any]) -> Generator[Dict[str, Any], None, None]:
        yield from self._quick_sort(array, 0, len(array) - 1)

    def _quick_sort(self, array: List[Any], low: int, high: int) -> Generator[Dict[str, Any], None, None]:
        if low < high:
            # Partition the array and get pivot index
            pivot_idx = yield from self._partition(array, low, high)
            # Recursively sort elements before and after partition
            yield from self._quick_sort(array, low, pivot_idx - 1)
            yield from self._quick_sort(array, pivot_idx + 1, high)

    def _partition(self, array: List[Any], low: int, high: int) -> Generator[Dict[str, Any], None, int]:
        pivot = array[high]
        i = low - 1

        for j in range(low, high):
            # Yield comparison with pivot
            yield {
                "array": list(array),
                "comparing": (j, high),
                "swapping": None
            }
            if array[j] < pivot:
                i += 1
                array[i], array[j] = array[j], array[i]
                yield {
                    "array": list(array),
                    "comparing": None,
                    "swapping": (i, j)
                }

        # Swap pivot to its correct final place
        array[i + 1], array[high] = array[high], array[i + 1]
        yield {
            "array": list(array),
            "comparing": None,
            "swapping": (i + 1, high)
        }
        return i + 1


class HeapSort(BaseSort):
    """
    Heap Sort implementation.
    
    Comparison-based sorting technique based on Binary Heap data structure.
    Uses recursive heapify to showcase nested generator delegation.
    """
    
    def sort(self, array: List[Any]) -> Generator[Dict[str, Any], None, None]:
        n = len(array)

        def heapify(size: int, i: int) -> Generator[Dict[str, Any], None, None]:
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2

            # Check if left child exists and is greater than root
            if left < size:
                yield {
                    "array": list(array),
                    "comparing": (left, largest),
                    "swapping": None
                }
                if array[left] > array[largest]:
                    largest = left

            # Check if right child exists and is greater than the current largest
            if right < size:
                yield {
                    "array": list(array),
                    "comparing": (right, largest),
                    "swapping": None
                }
                if array[right] > array[largest]:
                    largest = right

            # If largest is not root, swap and continue heapifying
            if largest != i:
                array[i], array[largest] = array[largest], array[i]
                yield {
                    "array": list(array),
                    "comparing": None,
                    "swapping": (i, largest)
                }
                # Recursive call on the affected sub-tree using yield from
                yield from heapify(size, largest)

        # Build a maxheap
        for i in range(n // 2 - 1, -1, -1):
            yield from heapify(n, i)

        # Extract elements one by one from the heap
        for i in range(n - 1, 0, -1):
            array[0], array[i] = array[i], array[0]
            yield {
                "array": list(array),
                "comparing": None,
                "swapping": (0, i)
            }
            # Heapify the root element to get the highest element at 0 again
            yield from heapify(i, 0)
