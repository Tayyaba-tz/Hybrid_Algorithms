import matplotlib.pyplot as plt
import math
import os

def plot_runtime_comparison(all_results, sizes):
    """
    Plots a line chart of Runtime vs Input Size for all algorithms.
    """
    plt.figure(figsize=(10, 6))
    for algo_name, times in all_results.items():
        plt.plot(sizes, times, marker='o', label=algo_name)
    
    plt.title('Execution Time vs Input Size')
    plt.xlabel('Array Size (n)')
    plt.ylabel('Time (ms)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/runtime_vs_size.png')
    plt.close()

def plot_metrics_bars(results_dict, metric_name):
    """
    Plots a bar chart for a specific metric (Comparisons or Swaps).
    """
    names = list(results_dict.keys())
    values = list(results_dict.values())
    colors = ['#E24B4B', '#4A90D9', '#4CAF50', '#F5A623', '#9B59B6']

    plt.figure(figsize=(10, 5))
    bars = plt.bar(names, values, color=colors[:len(names)], edgecolor='white', linewidth=0.5)

    for bar in bars:
        plt.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height(),
                 f'{int(bar.get_height())}',
                 ha='center', va='bottom', fontsize=10)

    plt.title(f'Number of {metric_name} per Algorithm')
    plt.ylabel(metric_name)
    plt.tight_layout()
    
    filename = f'results/{metric_name.lower()}_chart.png'
    plt.savefig(filename, dpi=150)
    plt.close()

def plot_theoretical_vs_empirical(measured_times, sizes):
    """
    Overlays measured runtime with theoretical O(n^2) and O(n log n) curves.
    """
    plt.figure(figsize=(10, 6))
    
    # Plot measured (take Quick Sort or Merge Sort as representative)
    plt.plot(sizes, measured_times, 'bo-', label='Measured (Empirical)')
    
    # Normalize theoretical curves to match the last measured point
    last_measured = measured_times[-1]
    last_n = sizes[-1]
    
    # O(n log n) curve
    theo_nlogn = [n * math.log2(n) for n in sizes]
    scale_nlogn = last_measured / theo_nlogn[-1]
    plt.plot(sizes, [t * scale_nlogn for t in theo_nlogn], 'g--', label='Theoretical O(n log n)')
    
    # O(n^2) curve
    theo_n2 = [n**2 for n in sizes]
    scale_n2 = last_measured / theo_n2[-1]
    plt.plot(sizes, [t * scale_n2 for t in theo_n2], 'r--', label='Theoretical O(n²)')
    
    plt.title('Theoretical vs Empirical Performance')
    plt.xlabel('Array Size (n)')
    plt.ylabel('Normalized Scale')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.savefig('results/theoretical_vs_empirical.png')
    plt.close()
