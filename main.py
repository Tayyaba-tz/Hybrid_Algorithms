import tkinter as tk
from tkinter import ttk, messagebox
import random
import os

# Import modules
from generator import (
    generate_random, generate_sorted, generate_reversed, 
    generate_nearly_sorted, generate_repeated
)
from selector.recommender import select_algorithm
from visualizer.bar_chart import BarChartVisualizer

# Import algorithms
from algorithms.insertion_sort import insertion_sort
from algorithms.merge_sort import merge_sort
from algorithms.quick_sort import quick_sort
from algorithms.heap_sort import heap_sort
from algorithms.timsort import timsort

class HybridSortApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hybrid Sorting Visualizer")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0D1117")

        # State
        self.original_array = []
        self.current_array = []
        self.generator_obj = None
        self.is_paused = True
        self.animation_speed = 50
        self.comparisons = 0
        self.swaps = 0
        self.step_count = 0
        
        self.setup_ui()
        self.generate_new_dataset()

    def setup_ui(self):
        # Top Bar
        top_bar = tk.Frame(self.root, bg="#1A1F2E", height=50)
        top_bar.pack(side="top", fill="x")
        
        title_label = tk.Label(
            top_bar, text="Hybrid Sorting Visualizer", 
            fg="#E8EAF0", bg="#1A1F2E", font=("Arial", 16, "bold")
        )
        title_label.pack(side="left", padx=20)

        # Complexity Strip
        self.complexity_frame = tk.Frame(self.root, bg="#22283A", height=40)
        self.complexity_frame.pack(side="top", fill="x")
        
        self.complexity_labels = {}
        metrics = ["Best Case", "Average Case", "Worst Case", "Space", "Stable?"]
        for m in metrics:
            lbl = tk.Label(
                self.complexity_frame, text=f"{m}: -", 
                fg="#6B7099", bg="#22283A", font=("Arial", 10)
            )
            lbl.pack(side="left", padx=20, expand=True)
            self.complexity_labels[m] = lbl

        # Main Canvas Area
        self.canvas = tk.Canvas(self.root, bg="#0D1117", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.visualizer = BarChartVisualizer(self.canvas, 1160, 500)

        # Info Labels
        self.info_frame = tk.Frame(self.root, bg="#0D1117")
        self.info_frame.pack(fill="x", padx=20)
        
        self.algo_name_lbl = tk.Label(self.info_frame, text="Algorithm: -", fg="#4A90D9", bg="#0D1117", font=("Arial", 12))
        self.algo_name_lbl.pack(side="left")
        
        self.stats_lbl = tk.Label(self.info_frame, text="Comparisons: 0 | Swaps: 0", fg="#E8EAF0", bg="#0D1117", font=("Arial", 12))
        self.stats_lbl.pack(side="right")

        self.recommendation_lbl = tk.Label(self.root, text="", fg="#4CAF50", bg="#0D1117", font=("Arial", 10, "italic"))
        self.recommendation_lbl.pack(pady=5)

        # Bottom Toolbar
        toolbar = tk.Frame(self.root, bg="#1A1F2E", height=60)
        toolbar.pack(side="bottom", fill="x")

        # Controls
        tk.Label(toolbar, text="Algorithm:", fg="white", bg="#1A1F2E").pack(side="left", padx=5)
        self.algo_var = tk.StringVar(value="Quick Sort")
        self.algo_menu = ttk.Combobox(toolbar, textvariable=self.algo_var, values=[
            "Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort", "TimSort"
        ], width=15)
        self.algo_menu.pack(side="left", padx=5)
        self.algo_menu.bind("<<ComboboxSelected>>", self.update_complexity_info)

        tk.Label(toolbar, text="Type:", fg="white", bg="#1A1F2E").pack(side="left", padx=5)
        self.type_var = tk.StringVar(value="Random")
        self.type_menu = ttk.Combobox(toolbar, textvariable=self.type_var, values=[
            "Random", "Sorted", "Reversed", "Nearly Sorted", "Repeated"
        ], width=12)
        self.type_menu.pack(side="left", padx=5)

        tk.Label(toolbar, text="Size:", fg="white", bg="#1A1F2E").pack(side="left", padx=5)
        self.size_var = tk.StringVar(value="100")
        self.size_entry = tk.Entry(toolbar, textvariable=self.size_var, width=5)
        self.size_entry.pack(side="left", padx=5)

        tk.Label(toolbar, text="Speed:", fg="white", bg="#1A1F2E").pack(side="left", padx=5)
        self.speed_scale = tk.Scale(toolbar, from_=1, to=100, orient="horizontal", bg="#1A1F2E", fg="white", highlightthickness=0)
        self.speed_scale.set(50)
        self.speed_scale.pack(side="left", padx=5)

        # Buttons
        self.btn_reset = tk.Button(toolbar, text="⏮ Reset", command=self.reset_animation)
        self.btn_reset.pack(side="left", padx=5)
        
        self.btn_play = tk.Button(toolbar, text="▶ Play", command=self.toggle_play)
        self.btn_play.pack(side="left", padx=5)
        
        self.btn_step = tk.Button(toolbar, text="⏭ Step", command=self.step_animation)
        self.btn_step.pack(side="left", padx=5)
        
        self.btn_new = tk.Button(toolbar, text="↺ New Dataset", command=self.generate_new_dataset)
        self.btn_new.pack(side="left", padx=5)

    def update_complexity_info(self, event=None):
        complexities = {
            "Insertion Sort": ["O(n)", "O(n²)", "O(n²)", "O(1)", "Yes"],
            "Merge Sort": ["O(n log n)", "O(n log n)", "O(n log n)", "O(n)", "Yes"],
            "Quick Sort": ["O(n log n)", "O(n log n)", "O(n²)", "O(log n)", "No"],
            "Heap Sort": ["O(n log n)", "O(n log n)", "O(n log n)", "O(1)", "No"],
            "TimSort": ["O(n)", "O(n log n)", "O(n log n)", "O(n)", "Yes"]
        }
        algo = self.algo_var.get()
        if algo in complexities:
            vals = complexities[algo]
            metrics = ["Best Case", "Average Case", "Worst Case", "Space", "Stable?"]
            for i, m in enumerate(metrics):
                self.complexity_labels[m].config(text=f"{m}: {vals[i]}", fg="#E8EAF0")

    def generate_new_dataset(self):
        try:
            n = int(self.size_var.get())
        except ValueError:
            n = 100
            self.size_var.set("100")
        
        dtype = self.type_var.get()
        if dtype == "Random": self.original_array = generate_random(n)
        elif dtype == "Sorted": self.original_array = generate_sorted(n)
        elif dtype == "Reversed": self.original_array = generate_reversed(n)
        elif dtype == "Nearly Sorted": self.original_array = generate_nearly_sorted(n)
        elif dtype == "Repeated": self.original_array = generate_repeated(n)
        
        self.reset_animation()
        
        # Update recommendation
        rec_algo, reason = select_algorithm(self.original_array)
        self.recommendation_lbl.config(text=f"Recommended: {rec_algo} — {reason}")

    def reset_animation(self):
        self.is_paused = True
        self.btn_play.config(text="▶ Play")
        self.current_array = self.original_array.copy()
        self.comparisons = 0
        self.swaps = 0
        self.step_count = 0
        self.generator_obj = None
        self.visualizer.draw(self.current_array)
        self.update_stats()
        self.update_complexity_info()

    def update_stats(self):
        self.stats_lbl.config(text=f"Comparisons: {self.comparisons} | Swaps: {self.swaps}")
        self.algo_name_lbl.config(text=f"Algorithm: {self.algo_var.get()}")

    def toggle_play(self):
        if not self.generator_obj:
            algo = self.algo_var.get()
            funcs = {
                "Insertion Sort": insertion_sort,
                "Merge Sort": merge_sort,
                "Quick Sort": quick_sort,
                "Heap Sort": heap_sort,
                "TimSort": timsort
            }
            self.generator_obj = funcs[algo](self.current_array)

        self.is_paused = not self.is_paused
        self.btn_play.config(text="⏸ Pause" if not self.is_paused else "▶ Play")
        if not self.is_paused:
            self.animate()

    def step_animation(self):
        if not self.generator_obj:
            algo = self.algo_var.get()
            funcs = {
                "Insertion Sort": insertion_sort,
                "Merge Sort": merge_sort,
                "Quick Sort": quick_sort,
                "Heap Sort": heap_sort,
                "TimSort": timsort
            }
            self.generator_obj = funcs[algo](self.current_array)
        
        self.is_paused = True
        self.btn_play.config(text="▶ Play")
        self.next_frame()

    def next_frame(self):
        if not self.generator_obj:
            return False
            
        try:
            frame = next(self.generator_obj)
            self.current_array, self.comparisons, self.swaps, highlights = frame
            self.visualizer.draw(self.current_array, highlights)
            self.update_stats()
            return True
        except StopIteration:
            self.is_paused = True
            self.btn_play.config(text="▶ Play")
            self.generator_obj = None
            # Final draw with all green
            self.visualizer.draw(self.current_array, {"sorted": list(range(len(self.current_array)))})
            return False

    def animate(self):
        if not self.is_paused:
            if self.next_frame():
                # Speed slider: 1 (slow, 500ms) to 100 (fast, 5ms)
                delay = max(5, 500 - (self.speed_scale.get() * 5))
                self.root.after(delay, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = HybridSortApp(root)
    root.mainloop()
