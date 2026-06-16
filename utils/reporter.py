import time
from collections import deque
from typing import List, Any, Type, Dict, Tuple, Union, Callable, Optional
import matplotlib.pyplot as plt
from engines.base_sort import BaseSort

class ComplexityAnalyzer:
    """
    Engine responsible for executing headless benchmarks of sorting algorithms
    and graphing their execution times relative to array size.
    """

    def run_benchmark(
        self, 
        algorithm_class: Type[BaseSort], 
        dataset_generator: Union[List[Any], Callable[[int], List[Any]]],
        size: Optional[int] = None
    ) -> float:
        """
        Instantiates the algorithm, generates/prepares the dataset, and fully consumes
        the sorting generator headlessly for maximum performance.
        
        Args:
            algorithm_class (Type[BaseSort]): The class of the sorting algorithm.
            dataset_generator (Union[List[Any], Callable[[int], List[Any]]]): 
                Either a pre-generated list of data, or a callable function (e.g., from generator.py)
                that accepts a size integer and returns a list.
            size (Optional[int]): The array size, required only if `dataset_generator` is a callable.
            
        Returns:
            float: The exact time taken to exhaust the sorting generator in milliseconds.
        """
        # Prepare the data array
        if isinstance(dataset_generator, list):
            data = list(dataset_generator)
        elif callable(dataset_generator):
            if size is None:
                raise ValueError("Size parameter must be specified when dataset_generator is a callable.")
            data = dataset_generator(size)
        else:
            # Fallback for general iterables
            data = list(dataset_generator)

        # Instantiate sorting engine
        algo_instance = algorithm_class()
        
        # Instantiate sorting generator
        generator = algo_instance.sort(data)
        
        # Profile using high-precision performance counter
        start_time = time.perf_counter()
        
        # Exhaust the generator without rendering frames.
        # deque(..., maxlen=0) consumes the generator at C-speed in Python.
        deque(generator, maxlen=0)
        
        end_time = time.perf_counter()
        
        # Calculate execution duration in milliseconds
        duration_ms = (end_time - start_time) * 1000.0
        return duration_ms

    def calculate_times(
        self, 
        algorithm_class: Type[BaseSort], 
        sizes: List[int]
    ) -> Tuple[List[float], List[float], List[float]]:
        """
        Helper method to collect benchmark runtimes across different array sizes.
        
        Args:
            algorithm_class (Type[BaseSort]): The algorithm class to run.
            sizes (List[int]): List of array sizes to test.
            
        Returns:
            Tuple of lists: (random_times, sorted_times, reversed_times) in milliseconds.
        """
        from utils.generator import generate_random_array, generate_sorted_array, generate_reversed_array
        
        random_times: List[float] = []
        sorted_times: List[float] = []
        reversed_times: List[float] = []
        
        for size in sizes:
            # Average Case (Random)
            random_times.append(self.run_benchmark(algorithm_class, generate_random_array, size))
            # Best Case (Sorted)
            sorted_times.append(self.run_benchmark(algorithm_class, generate_sorted_array, size))
            # Worst Case (Reversed)
            reversed_times.append(self.run_benchmark(algorithm_class, generate_reversed_array, size))
            
        return random_times, sorted_times, reversed_times

    def show_plot(
        self, 
        algo_name: str, 
        sizes: List[int], 
        random_times: List[float], 
        sorted_times: List[float], 
        reversed_times: List[float]
    ) -> None:
        """
        Builds and displays a Matplotlib plot showing execution time vs size.
        Must be invoked from the main thread if sharing a Tkinter event loop.
        """
        plt.figure(figsize=(8, 5))
        plt.plot(sizes, random_times, marker='o', linestyle='-', color='#3B82F6', linewidth=2, label='Random (Average Case)')
        plt.plot(sizes, sorted_times, marker='s', linestyle='--', color='#10B981', linewidth=2, label='Sorted (Best Case)')
        plt.plot(sizes, reversed_times, marker='^', linestyle='-.', color='#EF4444', linewidth=2, label='Reversed (Worst Case)')
        
        plt.title(f"Complexity Analysis: {algo_name}", fontsize=14, fontweight='bold', pad=15)
        plt.xlabel("Array Size (N)", fontsize=12)
        plt.ylabel("Execution Time (milliseconds)", fontsize=12)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#E2E8F0')
        plt.tight_layout()
        plt.show()

    def generate_report(self, algorithm_class: Type[BaseSort]) -> None:
        """
        Synchronously runs the full benchmark suite on the selected algorithm and plots results.
        """
        sizes = [50, 100, 200, 500]
        random_times, sorted_times, reversed_times = self.calculate_times(algorithm_class, sizes)
        self.show_plot(algorithm_class.__name__, sizes, random_times, sorted_times, reversed_times)
