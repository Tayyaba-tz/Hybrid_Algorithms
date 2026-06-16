# Hybrid Sorting Visualizer and Benchmarking Suite

An educational tool built in Python to visualize sorting algorithms and benchmark their performance across different dataset types.

## Core Features

The Hybrid Sorting Visualizer provides a comprehensive suite of tools for understanding and comparing sorting performance. It implements five distinct sorting algorithms—**Insertion Sort**, **Merge Sort**, **Quick Sort**, **Heap Sort**, and a **TimSort-inspired Hybrid**—allowing users to see how they handle different data distributions.

Users can generate five unique dataset types, including **Random**, **Sorted**, **Reversed**, **Nearly Sorted**, and **Repeated** values. The application features an interactive visualization engine with full playback controls, an adaptive recommender that suggests the optimal algorithm for any given dataset, and a benchmarking suite that exports detailed performance metrics to CSV files.

## Project Structure

The application is organized into modular components to ensure clarity and maintainability. Each module handles a specific aspect of the system, from data generation to the final visualization.

| Module | Description |
| :--- | :--- |
| `main.py` | The primary entry point that initializes the Tkinter GUI and coordinates all modules. |
| `generator.py` | Contains logic for creating various numerical datasets (random, sorted, etc.). |
| `algorithms/` | A directory containing self-contained implementations of each sorting algorithm. |
| `visualizer/` | Handles the rendering of the array as an interactive bar chart on the canvas. |
| `selector/` | Implements the adaptive logic for recommending the best algorithm. |
| `benchmarking/` | Manages precise performance timing and data collection for all algorithms. |
| `dashboard/` | Generates visual charts using Matplotlib for performance comparison. |
| `results/` | A dedicated folder for storing generated benchmark reports and analysis images. |

## Setup Instructions
1. Ensure you have Python 3.7+ installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## How it Works
- **Instrumentation**: Each algorithm is a Python generator using `yield` to send its state (array, comparisons, swaps) to the GUI after every operation.
- **Visualization**: The GUI uses a Tkinter Canvas to draw bars representing array elements, using colors to highlight comparisons, pivots, and sorted sections.
- **Benchmarking**: The suite runs each algorithm multiple times to calculate stable averages, then exports data for further analysis.
