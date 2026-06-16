import time
import csv
import os
from algorithms.insertion_sort import insertion_sort
from algorithms.merge_sort import merge_sort
from algorithms.quick_sort import quick_sort
from algorithms.heap_sort import heap_sort
from algorithms.timsort import timsort

def time_one_run(sort_function, arr):
    """
    Measures the execution time and metrics for a single run of a sorting algorithm.
    """
    arr_copy = arr.copy()
    start = time.perf_counter()
    
    # Consume the generator to get the final result
    generator = sort_function(arr_copy)
    final_result = None
    try:
        while True:
            final_result = next(generator)
    except StopIteration as e:
        final_result = e.value
    
    end = time.perf_counter()
    elapsed_ms = (end - start) * 1000
    
    # If final_result is still None, it might be that the function returned directly (no yields)
    # This shouldn't happen with our instrumented code, but good to handle
    if final_result is None:
        # Re-run if it wasn't a generator or failed to return via StopIteration
        return 0, 0, 0 

    _, comparisons, swaps = final_result
    return elapsed_ms, comparisons, swaps

def benchmark_algorithm(name, sort_function, arr, runs=5):
    """
    Runs an algorithm multiple times and returns averaged benchmarks.
    """
    results = []
    for _ in range(runs):
        results.append(time_one_run(sort_function, arr))
    
    avg_time = sum(r[0] for r in results) / runs
    avg_comps = sum(r[1] for r in results) / runs
    avg_swaps = sum(r[2] for r in results) / runs
    
    return {
        'name': name,
        'avg_time_ms': avg_time,
        'avg_comparisons': avg_comps,
        'avg_swaps': avg_swaps
    }

def run_full_benchmark(dataset, dataset_name):
    """
    Benchmarks all algorithms on a given dataset and saves to CSV.
    """
    algorithms = {
        'Insertion Sort': insertion_sort,
        'Merge Sort': merge_sort,
        'Quick Sort': quick_sort,
        'Heap Sort': heap_sort,
        'TimSort': timsort
    }
    
    benchmark_results = []
    for name, func in algorithms.items():
        res = benchmark_algorithm(name, func, dataset)
        benchmark_results.append(res)
    
    # Save to CSV
    os.makedirs('results', exist_ok=True)
    filename = f'results/benchmark_{dataset_name}.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'avg_time_ms', 'avg_comparisons', 'avg_swaps'])
        writer.writeheader()
        writer.writerows(benchmark_results)
        
    return benchmark_results
