import tkinter as tk
from typing import List, Dict, Any, Optional, Tuple

class CanvasRenderer:
    """
    Renders the sorting animation on a Tkinter Canvas.
    
    Adheres to high-performance guidelines by creating rectangle objects
    once during setup and modifying their coordinates and colors dynamically
    during update, rather than deleting and recreating elements on each frame.
    """
    
    # Modern HSL-tailored / Tailwind-inspired color palette for dark mode visualizer
    COLOR_DEFAULT = "#60A5FA"   # Light Blue (Default state of elements)
    COLOR_COMPARE = "#FBBF24"   # Yellow (Active comparisons)
    COLOR_SWAP = "#F87171"      # Red (Swaps, shifts, or writes)
    COLOR_SORTED = "#34D399"    # Green (Final fully sorted state)

    def __init__(self, canvas: tk.Canvas) -> None:
        """
        Initializes the CanvasRenderer with a target Tkinter Canvas.
        
        Args:
            canvas (tk.Canvas): The canvas widget where sorting bars are drawn.
        """
        self.canvas = canvas
        self.bar_ids: List[int] = []
        self.array_size = 0
        self.max_value = 1

    def setup(self, array: List[Any]) -> None:
        """
        Sets up the canvas by clearing existing drawings and drawing new bars.
        The rectangle IDs are cached in `self.bar_ids`.
        
        Args:
            array (List[Any]): The array of values to render.
        """
        self.canvas.delete("all")
        self.bar_ids.clear()
        self.array_size = len(array)
        
        if self.array_size == 0:
            return
            
        self.max_value = max(array) if max(array) > 0 else 1
        
        # Get canvas current dimensions. If not laid out yet, get configured size.
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Fallback to configured dimensions if winfo is not yet updated by Tkinter layout engine
        if canvas_width <= 1:
            canvas_width = int(self.canvas.cget("width"))
        if canvas_height <= 1:
            canvas_height = int(self.canvas.cget("height"))

        bar_width = canvas_width / self.array_size
        padding_top = 20
        padding_bottom = 5
        usable_height = canvas_height - padding_top - padding_bottom

        for i, val in enumerate(array):
            # Scale height relative to the maximum value in the array
            height_ratio = val / self.max_value
            bar_height = height_ratio * usable_height
            
            x1 = i * bar_width
            y1 = canvas_height - padding_bottom - bar_height
            x2 = (i + 1) * bar_width
            y2 = canvas_height - padding_bottom

            # Create rectangle bar
            bar_id = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=self.COLOR_DEFAULT,
                outline="",  # No outline for smooth modern look
            )
            self.bar_ids.append(bar_id)

    def update(self, state_dict: Dict[str, Any]) -> None:
        """
        Updates coordinates and colors of existing bars on the canvas.
        
        Args:
            state_dict (Dict[str, Any]): State dict containing:
                "array": List[Any] - Current snapshot of the array.
                "comparing": Optional[Tuple[int, int]] - Indices being compared.
                "swapping": Optional[Tuple[int, int]] - Indices being swapped.
        """
        array = state_dict.get("array", [])
        if len(array) != self.array_size or not self.bar_ids:
            # Re-setup if array size changes dynamically
            self.setup(array)
            return

        comparing = state_dict.get("comparing")
        swapping = state_dict.get("swapping")

        canvas_height = self.canvas.winfo_height()
        canvas_width = self.canvas.winfo_width()
        
        if canvas_width <= 1:
            canvas_width = int(self.canvas.cget("width"))
        if canvas_height <= 1:
            canvas_height = int(self.canvas.cget("height"))

        bar_width = canvas_width / self.array_size
        padding_top = 20
        padding_bottom = 5
        usable_height = canvas_height - padding_top - padding_bottom

        for i, val in enumerate(array):
            height_ratio = val / self.max_value
            bar_height = height_ratio * usable_height
            
            x1 = i * bar_width
            y1 = canvas_height - padding_bottom - bar_height
            x2 = (i + 1) * bar_width
            y2 = canvas_height - padding_bottom

            # Update coordinates dynamically
            self.canvas.coords(self.bar_ids[i], x1, y1, x2, y2)

            # Determine color state
            if swapping and i in swapping:
                color = self.COLOR_SWAP
            elif comparing and i in comparing:
                color = self.COLOR_COMPARE
            else:
                color = self.COLOR_DEFAULT

            # Update item color dynamically
            self.canvas.itemconfig(self.bar_ids[i], fill=color)

    def draw_sorted(self) -> None:
        """
        Turns all bars to the sorted color (green) to signal completion.
        """
        for bar_id in self.bar_ids:
            self.canvas.itemconfig(bar_id, fill=self.COLOR_SORTED)
