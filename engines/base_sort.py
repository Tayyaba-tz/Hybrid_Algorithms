from abc import ABC, abstractmethod
from typing import Generator, Dict, List, Tuple, Any, Optional

class BaseSort(ABC):
    """
    Abstract base class for all sorting algorithms in the visualization engine.
    
    Subclasses must implement the `sort` method as a generator, yielding
    the current state of the array at each critical operational step (e.g.,
    comparing, swapping, or overwriting elements) for frame-by-frame animation.
    """

    @abstractmethod
    def sort(self, array: List[Any]) -> Generator[Dict[str, Any], None, None]:
        """
        Performs the sort operation in-place and yields state frames representing
        the progress of the algorithm.
        
        Args:
            array (List[Any]): The list of elements to be sorted. The array is
                typically mutated in-place.
                
        Yields:
            Dict[str, Any]: A dictionary tracking the current state.
                Expected schema:
                {
                    "array": List[Any],
                        A snapshot copy of the array in its current state.
                    "comparing": Optional[Tuple[int, int]],
                        Indices of the two elements being compared, or None.
                    "swapping": Optional[Tuple[int, int]],
                        Indices of the two elements being swapped or updated, or None.
                }
        """
        pass
