import unittest
from typing import List, Any
from utils.generator import generate_random_array, generate_sorted_array, generate_reversed_array
from utils.reporter import ComplexityAnalyzer
from engines.traditional import InsertionSort, MergeSort, QuickSort, HeapSort
from engines.hybrid import HybridSort

class TestSortingEngines(unittest.TestCase):
    
    def setUp(self) -> None:
        self.sizes = [0, 1, 5, 33, 64]  # Test small sizes, edge cases, and run-boundary sizes
        self.algorithms = [
            InsertionSort(),
            MergeSort(),
            QuickSort(),
            HeapSort(),
            HybridSort(run_size=16)  # Use smaller run size for testing smaller array sizes
        ]

    def test_sorting_correctness(self) -> None:
        """
        Verifies that all sorting engines correctly sort random arrays and yield
        valid frame state dicts containing copy arrays, comparing indices, and swapping indices.
        """
        for algo in self.algorithms:
            for size in self.sizes:
                with self.subTest(algorithm=algo.__class__.__name__, size=size):
                    arr = generate_random_array(size)
                    expected = sorted(arr)
                    
                    # Track frame counts and state correctness
                    frames_count = 0
                    last_frame = None
                    
                    generator = algo.sort(arr)
                    for frame in generator:
                        frames_count += 1
                        last_frame = frame
                        
                        # Check frame schema
                        self.assertIn("array", frame)
                        self.assertIn("comparing", frame)
                        self.assertIn("swapping", frame)
                        
                        # Verify array in the frame has the correct length
                        self.assertEqual(len(frame["array"]), size)
                        
                        # Verify comparing elements are valid indices
                        comp = frame["comparing"]
                        if comp is not None:
                            self.assertIsInstance(comp, tuple)
                            self.assertEqual(len(comp), 2)
                            self.assertTrue(0 <= comp[0] < size, f"Invalid comparing index {comp[0]} for size {size}")
                            self.assertTrue(0 <= comp[1] < size, f"Invalid comparing index {comp[1]} for size {size}")
                        
                        # Verify swapping elements are valid indices
                        swap = frame["swapping"]
                        if swap is not None:
                            self.assertIsInstance(swap, tuple)
                            self.assertEqual(len(swap), 2)
                            self.assertTrue(0 <= swap[0] < size, f"Invalid swapping index {swap[0]} for size {size}")
                            self.assertTrue(0 <= swap[1] < size, f"Invalid swapping index {swap[1]} for size {size}")
                    
                    # The original array should be sorted in-place
                    self.assertEqual(arr, expected)
                    
                    # If elements were sorted (size > 1), the last frame's array should also be sorted
                    if size > 1:
                        self.assertTrue(frames_count > 0)
                        self.assertIsNotNone(last_frame)
                        self.assertEqual(last_frame["array"], expected)

    def test_already_sorted_arrays(self) -> None:
        """
        Tests behavior when sorting arrays that are already sorted.
        """
        for algo in self.algorithms:
            for size in [10, 32]:
                with self.subTest(algorithm=algo.__class__.__name__, size=size):
                    arr = generate_sorted_array(size)
                    expected = list(arr)
                    
                    generator = algo.sort(arr)
                    for _ in generator:
                        pass
                    
                    self.assertEqual(arr, expected)

    def test_reversed_arrays(self) -> None:
        """
        Tests behavior when sorting reverse-sorted arrays.
        """
        for algo in self.algorithms:
            for size in [10, 32]:
                with self.subTest(algorithm=algo.__class__.__name__, size=size):
                    arr = generate_reversed_array(size)
                    expected = sorted(arr)
                    
                    generator = algo.sort(arr)
                    for _ in generator:
                        pass
                    
                    self.assertEqual(arr, expected)


class TestComplexityAnalyzer(unittest.TestCase):
    def test_analyzer_benchmarking(self) -> None:
        analyzer = ComplexityAnalyzer()
        
        # Test run_benchmark with a list generator
        rand_arr = generate_random_array(10)
        t_rand = analyzer.run_benchmark(InsertionSort, rand_arr)
        self.assertIsInstance(t_rand, float)
        self.assertTrue(t_rand >= 0.0)
        
        # Test run_benchmark with a callable generator
        t_callable = analyzer.run_benchmark(MergeSort, generate_random_array, size=10)
        self.assertIsInstance(t_callable, float)
        self.assertTrue(t_callable >= 0.0)
        
        # Test calculate_times
        sizes = [10, 20]
        random_times, sorted_times, reversed_times = analyzer.calculate_times(QuickSort, sizes)
        self.assertEqual(len(random_times), len(sizes))
        self.assertEqual(len(sorted_times), len(sizes))
        self.assertEqual(len(reversed_times), len(sizes))
        
        for t in random_times + sorted_times + reversed_times:
            self.assertIsInstance(t, float)
            self.assertTrue(t >= 0.0)


if __name__ == "__main__":
    unittest.main()
