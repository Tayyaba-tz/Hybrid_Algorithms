\# Hybrid Sorting Visualizer \& Benchmarking Suite



An advanced, real-time algorithmic visualization and benchmarking tool built in Python. This project demonstrates the execution, performance, and theoretical time complexity of traditional and hybrid sorting algorithms through a modern UI and headless performance profiling.



\## System Overview



This application bridges the gap between pure algorithmic logic and graphical representation. It avoids the common pitfall of tightly coupling UI code with mathematical logic by utilizing \*\*Python Generators (`yield`)\*\*. This architectural decision allows the sorting engines to calculate in a pure environment while independently emitting spatial state data to the visualizer.



\### Core Features

\* \*\*Real-Time Visualization:\*\* Step-by-step graphical rendering of array states (Comparing, Swapping, Sorted) without blocking the main application thread.

\* \*\*Timsort-Inspired Hybridization:\*\* Implements a custom hybrid algorithm combining the recursive divide-and-conquer strategy of Merge Sort with the low-overhead, in-place sorting of Insertion Sort for small subarrays (Runs).

\* \*\*Headless Benchmarking:\*\* A dedicated `ComplexityAnalyzer` that exhausts algorithm generators in memory to measure raw execution time using `time.perf\_counter()`.

\* \*\*Complexity Graphing:\*\* Generates Matplotlib visualizations plotting Execution Time (ms) vs. Input Size (N) across Best, Worst, and Average case datasets.



\---



\## System Architecture



The codebase enforces strict Separation of Concerns (SoC), divided into three primary modules:



\### 1. The Engine Layer (`/engines`)

The pure-logic backend. All algorithms inherit from an abstract `BaseSort` class, ensuring polymorphism. 

\* \*\*Mechanics:\*\* Instead of returning a sorted array, algorithms `yield` a dictionary containing the current state: `{"array": \[...], "comparing": (i, j), "swapping": (x, y)}`.

\* \*\*Algorithms Included:\*\* Merge Sort, Quick Sort, Heap Sort, Insertion Sort, and Hybrid Sort.



\### 2. The Presentation Layer (`/visualizer` \& `main.py`)

The user interface built with `customtkinter` and `tkinter.Canvas`.

\* \*\*`CanvasRenderer`:\*\* Optimized for performance. Instead of destroying and redrawing hundreds of shapes per frame, it initializes objects once and dynamically updates their coordinates (`canvas.coords()`) and colors (`canvas.itemconfig()`) based on the generator's yielded state.

\* \*\*`SortingController`:\*\* Manages the event loop, pulling the `next()` state from the algorithmic engine and pushing it to the renderer using non-blocking Tkinter `after()` loops.



\### 3. The Utility Layer (`/utils`)

Handles data generation and mathematical profiling.

\* \*\*`generator.py`:\*\* Generates Random (Average Case), Ascending (Best Case), and Descending (Worst Case) datasets.

\* \*\*`reporter.py`:\*\* Runs algorithms in a headless state across scaling input sizes (e.g., N=50 to N=500) and plots the asymptotic growth curves to verify Big-O notation.



\---



\## The Hybrid Algorithm (Timsort Architecture)



The flagship algorithm of this suite is the `HybridSort`. It is engineered to overcome the heavy recursive overhead of standard $O(N \\log N)$ algorithms.



1\. \*\*Chunking:\*\* The dataset is divided into small blocks (defined by a `RUN` threshold, typically 32).

2\. \*\*Micro-Sorting:\*\* Each block is sorted using Insertion Sort. While Insertion Sort is $O(N^2)$ macroscopically, it outperforms Merge/Quick Sort on tiny arrays due to its low constant factors and in-place nature.

3\. \*\*Merging:\*\* The sorted runs are then merged together using the standard Merge Sort combination logic.



This approach guarantees an $O(N \\log N)$ worst-case while approaching $O(N)$ for partially sorted data.



\---



\## Installation \& Usage



\### Requirements

\* Python 3.8+

\* `customtkinter`

\* `matplotlib`

\* `numpy` (Optional, depending on dataset generator implementation)



\### Setup

1\. Clone the repository and navigate to the root directory.

2\. Activate your virtual environment (recommended).

3\. Install dependencies:

&#x20;  ```bash

&#x20;  pip install -r requirements.txt

