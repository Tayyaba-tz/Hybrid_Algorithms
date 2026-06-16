import time
import threading
import customtkinter as ctk
import tkinter as tk
from typing import List, Dict

# Import sorting engines, generator helpers, and reporter
from engines.base_sort import BaseSort
from engines.traditional import InsertionSort, MergeSort, QuickSort, HeapSort
from engines.hybrid import HybridSort
from utils.generator import generate_random_array, generate_sorted_array, generate_reversed_array
from utils.reporter import ComplexityAnalyzer
from visualizer.renderer import CanvasRenderer
from visualizer.controller import SortingController

# Set appearance properties for customtkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Algorithm configuration mapping
ALGORITHMS = {
    "Merge Sort": MergeSort,
    "Quick Sort": QuickSort,
    "Heap Sort": HeapSort,
    "Insertion Sort": InsertionSort,
    "Hybrid Sort": HybridSort
}

# Dataset configuration mapping
DATASETS = {
    "Random": generate_random_array,
    "Sorted": generate_sorted_array,
    "Reversed": generate_reversed_array
}

# Asymptotic time and space complexities mapping for visualization/benchmarking modal
COMPLEXITIES = {
    "Merge Sort": {"Best": "O(N log N)", "Average": "O(N log N)", "Worst": "O(N log N)", "Space": "O(N)"},
    "Quick Sort": {"Best": "O(N log N)", "Average": "O(N log N)", "Worst": "O(N^2)", "Space": "O(log N)"},
    "Heap Sort": {"Best": "O(N log N)", "Average": "O(N log N)", "Worst": "O(N log N)", "Space": "O(1)"},
    "Insertion Sort": {"Best": "O(N)", "Average": "O(N^2)", "Worst": "O(N^2)", "Space": "O(1)"},
    "Hybrid Sort": {"Best": "O(N)", "Average": "O(N log N)", "Worst": "O(N log N)", "Space": "O(N)"}
}


class BenchmarkWindow(ctk.CTkToplevel):
    """
    Stunning modal dialog to show benchmarking stats and asymptotic complexities.
    """
    def __init__(
        self, 
        parent: tk.Misc, 
        algo_name: str, 
        dataset_name: str, 
        size: int, 
        execution_time: float, 
        complexity_info: Dict[str, str]
    ) -> None:
        super().__init__(master=parent)
        self.title("Performance & Complexity Analysis")
        self.geometry("450x440")
        self.resizable(False, False)
        
        # Modal setup
        self.transient(parent)
        self.grab_set()
        
        # Deep slate background
        self.configure(fg_color="#1E293B")
        
        # Header title
        title_label = ctk.CTkLabel(
            master=self, 
            text=f"⚡ {algo_name} Analysis", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FBBF24"
        )
        title_label.pack(pady=(20, 10))
        
        # Execution environment box
        info_frame = ctk.CTkFrame(master=self, fg_color="#334155", corner_radius=8)
        info_frame.pack(pady=10, padx=20, fill="x")
        
        info_rows = [
            ("Dataset Distribution:", f"{dataset_name}"),
            ("Dataset Size:", f"{size} elements"),
            ("Headless Execution Time:", f"{execution_time:.6f} seconds"),
        ]
        
        for label, val in info_rows:
            row_frame = ctk.CTkFrame(master=info_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=15, pady=5)
            
            lbl = ctk.CTkLabel(master=row_frame, text=label, font=ctk.CTkFont(weight="bold", size=12), text_color="#94A3B8")
            lbl.pack(side="left")
            
            v_lbl = ctk.CTkLabel(master=row_frame, text=val, font=ctk.CTkFont(family="Courier", size=12), text_color="#F8FAFC")
            v_lbl.pack(side="right")
            
        # Complexity mapping box
        comp_frame = ctk.CTkFrame(master=self, fg_color="#334155", corner_radius=8)
        comp_frame.pack(pady=10, padx=20, fill="x")
        
        comp_title = ctk.CTkLabel(
            master=comp_frame, 
            text="Theoretical Time & Space Complexity", 
            font=ctk.CTkFont(weight="bold", size=13), 
            text_color="#38BDF8"
        )
        comp_title.pack(pady=(10, 5))
        
        grid_data = [
            ("Best Case Time:", complexity_info["Best"]),
            ("Average Case Time:", complexity_info["Average"]),
            ("Worst Case Time:", complexity_info["Worst"]),
            ("Space Complexity:", complexity_info["Space"]),
        ]
        
        for label, val in grid_data:
            row_frame = ctk.CTkFrame(master=comp_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=15, pady=4)
            
            lbl = ctk.CTkLabel(master=row_frame, text=label, font=ctk.CTkFont(size=12), text_color="#CBD5E1")
            lbl.pack(side="left")
            
            v_lbl = ctk.CTkLabel(master=row_frame, text=val, font=ctk.CTkFont(weight="bold", size=12), text_color="#34D399")
            v_lbl.pack(side="right")
            
        # Close button
        close_btn = ctk.CTkButton(
            master=self, 
            text="Dismiss Report", 
            command=self.destroy,
            fg_color="#3B82F6",
            hover_color="#2563EB",
            font=ctk.CTkFont(weight="bold")
        )
        close_btn.pack(pady=(20, 10))


class SortingVisualizerApp(ctk.CTk):
    """
    Main Application Window of the Sorting Visualizer.
    
    Provides a beautiful Dark Mode controls sidebar on the left,
    a responsive high-performance drawing canvas in the center,
    and complexity analysis tools.
    """
    def __init__(self) -> None:
        super().__init__()
        
        self.title("Hybrid & Traditional Sorting Algorithm Visualizer")
        self.geometry("1100x650")
        self.minimum_size = (900, 550)
        self.minsize(self.minimum_size[0], self.minimum_size[1])
        
        self.current_array: List[int] = []
        
        # Grid layout configurations (2 columns: left sidebar, right main area)
        self.grid_columnconfigure(0, weight=0, minsize=280)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # ------------------- Left Sidebar Layout -------------------
        self.sidebar_frame = ctk.CTkFrame(master=self, width=280, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar_frame.grid_rowconfigure(10, weight=1)  # Bottom spacer
        
        # App Title Logo
        logo_label = ctk.CTkLabel(
            master=self.sidebar_frame, 
            text="SORTING ENGINE", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#60A5FA"
        )
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        # Algorithm Dropdown menu
        algo_title = ctk.CTkLabel(master=self.sidebar_frame, text="Algorithm Select:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#94A3B8")
        algo_title.grid(row=1, column=0, padx=20, pady=(10, 2), sticky="w")
        
        self.algo_menu = ctk.CTkOptionMenu(
            master=self.sidebar_frame, 
            values=list(ALGORITHMS.keys()),
            command=self.on_algo_changed
        )
        self.algo_menu.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        # Dataset Dropdown menu
        dataset_title = ctk.CTkLabel(master=self.sidebar_frame, text="Dataset Type:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#94A3B8")
        dataset_title.grid(row=3, column=0, padx=20, pady=(10, 2), sticky="w")
        
        self.dataset_menu = ctk.CTkOptionMenu(
            master=self.sidebar_frame, 
            values=list(DATASETS.keys()),
            command=self.on_dataset_changed
        )
        self.dataset_menu.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        
        # Array Size Slider
        self.size_label = ctk.CTkLabel(master=self.sidebar_frame, text="Array Size: 100", font=ctk.CTkFont(size=12, weight="bold"), text_color="#94A3B8")
        self.size_label.grid(row=5, column=0, padx=20, pady=(15, 2), sticky="w")
        
        self.size_slider = ctk.CTkSlider(
            master=self.sidebar_frame, 
            from_=10, 
            to=200, 
            number_of_steps=190, 
            command=self.on_size_slider_changed
        )
        self.size_slider.grid(row=6, column=0, padx=20, pady=5, sticky="ew")
        self.size_slider.set(100)
        
        # Animation Speed Slider
        self.speed_label = ctk.CTkLabel(master=self.sidebar_frame, text="Animation Delay: 30 ms", font=ctk.CTkFont(size=12, weight="bold"), text_color="#94A3B8")
        self.speed_label.grid(row=7, column=0, padx=20, pady=(15, 2), sticky="w")
        
        self.speed_slider = ctk.CTkSlider(
            master=self.sidebar_frame, 
            from_=1, 
            to=500, 
            command=self.on_speed_slider_changed
        )
        self.speed_slider.grid(row=8, column=0, padx=20, pady=5, sticky="ew")
        self.speed_slider.set(30)
        
        # Action Buttons
        self.gen_button = ctk.CTkButton(
            master=self.sidebar_frame, 
            text="Generate Data", 
            command=self.generate_data,
            fg_color="#475569",
            hover_color="#334155"
        )
        self.gen_button.grid(row=9, column=0, padx=20, pady=(25, 8), sticky="ew")
        
        self.play_button = ctk.CTkButton(
            master=self.sidebar_frame, 
            text="Start Animation", 
            command=self.toggle_animation,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=ctk.CTkFont(weight="bold")
        )
        self.play_button.grid(row=10, column=0, padx=20, pady=8, sticky="ew")
        
        self.bench_button = ctk.CTkButton(
            master=self.sidebar_frame, 
            text="Run Complexity Analysis", 
            command=self.run_benchmarking,
            fg_color="#059669",
            hover_color="#047857"
        )
        self.bench_button.grid(row=11, column=0, padx=20, pady=(8, 20), sticky="ew")
        
        # ------------------- Main Canvas Layout -------------------
        self.main_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Dark premium background canvas
        self.canvas = tk.Canvas(self.main_frame, bg="#0F172A", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0, 10))
        
        # Status Label bar at the bottom
        self.status_label = ctk.CTkLabel(
            master=self.main_frame, 
            text="Status: Click 'Generate Data' or 'Start Animation' to begin.", 
            font=ctk.CTkFont(size=12, slant="italic"), 
            text_color="#94A3B8"
        )
        self.status_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        # Initialize rendering engine and control bridge
        self.renderer = CanvasRenderer(self.canvas)
        self.controller = SortingController(self.canvas, self.renderer, on_finish_callback=self.on_sorting_finish)
        
        # Bind resize configuration events to scale bars responsively
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        
        # Proactively generate initial default dataset
        self.generate_data()

    def _get_selected_engine(self) -> BaseSort:
        """
        Instantiates and returns the selected sorting engine from GUI state.
        """
        algo_name = self.algo_menu.get()
        engine_cls = ALGORITHMS[algo_name]
        
        if algo_name == "Hybrid Sort":
            # Pass custom run sizes if desired, standard Timsort blocks default to 32
            return engine_cls(run_size=32)
        return engine_cls()

    def generate_data(self) -> None:
        """
        Generates array elements according to dataset and slider specifications,
        then resets the visualizer state.
        """
        size = int(self.size_slider.get())
        dataset_name = self.dataset_menu.get()
        generator_func = DATASETS[dataset_name]
        
        self.current_array = generator_func(size)
        engine = self._get_selected_engine()
        
        # Reset controller and redraw canvas
        self.controller.reset(self.current_array, engine)
        
        # Update play state button representations
        self.play_button.configure(text="Start Animation")
        self.status_label.configure(text=f"Status: Data generated ({dataset_name}, size={size}). Ready to visualize.")

    def toggle_animation(self) -> None:
        """
        Toggles animation play state between sorting and pausing.
        Handles auto-generation of data if clicked with no active array.
        """
        if not self.current_array:
            self.generate_data()
            
        if self.controller.is_playing:
            self.controller.pause()
            self.play_button.configure(text="Resume Animation")
            self.status_label.configure(text="Status: Paused sorting.")
        else:
            self.controller.set_speed(int(self.speed_slider.get()))
            self.controller.play()
            self.play_button.configure(text="Pause Animation")
            self.status_label.configure(text=f"Status: Executing {self.algo_menu.get()} visualization...")

    def on_sorting_finish(self) -> None:
        """
        Callback executed automatically when the sorting generator finishes.
        """
        self.play_button.configure(text="Start Animation")
        self.status_label.configure(text=f"Status: {self.algo_menu.get()} completed successfully!")

    def on_size_slider_changed(self, value: float) -> None:
        """
        Updates size labels in real time and regenerates the array.
        """
        self.size_label.configure(text=f"Array Size: {int(value)}")
        self.generate_data()

    def on_speed_slider_changed(self, value: float) -> None:
        """
        Updates delay labels and changes animation tick interval in real time.
        """
        self.speed_label.configure(text=f"Animation Delay: {int(value)} ms")
        self.controller.set_speed(int(value))

    def on_algo_changed(self, value: str) -> None:
        """
        Swaps sorting engines on the fly. Re-sorts from the current state if possible.
        """
        if self.current_array:
            engine = self._get_selected_engine()
            self.controller.reset(self.current_array, engine)
            self.play_button.configure(text="Start Animation")
            self.status_label.configure(text=f"Status: Loaded algorithm: {value}")

    def on_dataset_changed(self, _: str) -> None:
        """
        Triggers new dataset generation on dropdown state updates.
        """
        self.generate_data()

    def on_canvas_resize(self, _: tk.Event) -> None:
        """
        Handles dynamic canvas resizing to keep elements perfectly scaled in real time.
        """
        if self.controller.current_state:
            self.renderer.update(self.controller.current_state)
        elif self.controller.array:
            self.renderer.setup(self.controller.array)

    def run_benchmarking(self) -> None:
        """
        Runs the benchmark suite on the selected algorithm using a background thread,
        and plots the results in a new Matplotlib window without freezing the main UI.
        """
        algo_name = self.algo_menu.get()
        engine_cls = ALGORITHMS[algo_name]
        
        self.status_label.configure(text=f"Status: Running complexity analysis for {algo_name}...")
        self.bench_button.configure(state="disabled")
        self.update_idletasks()
        
        # Instantiate ComplexityAnalyzer
        analyzer = ComplexityAnalyzer()
        
        # Define target thread function
        def benchmark_thread_target():
            sizes = [50, 100, 200, 500]
            try:
                # Perform calculations headlessly in the background thread
                random_times, sorted_times, reversed_times = analyzer.calculate_times(engine_cls, sizes)
                
                # Safely execute the plotting function on the main GUI thread using self.after
                self.after(0, self.display_benchmark_plot, analyzer, algo_name, sizes, random_times, sorted_times, reversed_times)
            except Exception as e:
                self.after(0, self.on_benchmark_error, e)
                
        # Start daemon thread to prevent blocking on application shutdown
        threading.Thread(target=benchmark_thread_target, daemon=True).start()

    def display_benchmark_plot(
        self, 
        analyzer: ComplexityAnalyzer, 
        algo_name: str, 
        sizes: List[int], 
        random_times: List[float], 
        sorted_times: List[float], 
        reversed_times: List[float]
    ) -> None:
        """
        Renders the complexity plot window and restores the GUI elements.
        Invoked on the main thread for thread-safety.
        """
        self.bench_button.configure(state="normal")
        self.status_label.configure(text=f"Status: Displayed report for {algo_name}.")
        
        # Render the plot on the main thread so that it integrates with Tkinter events
        analyzer.show_plot(algo_name, sizes, random_times, sorted_times, reversed_times)

    def on_benchmark_error(self, error: Exception) -> None:
        """
        Error handler callback invoked on the main thread.
        """
        self.bench_button.configure(state="normal")
        self.status_label.configure(text=f"Status: Complexity Analysis error: {error}")


if __name__ == "__main__":
    app = SortingVisualizerApp()
    app.mainloop()
