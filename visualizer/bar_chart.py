import tkinter as tk
from tkinter import ttk
import random

class BarChartVisualizer:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.colors = {
            "default": "#4A90D9",  # Steel blue
            "compare": "#E24B4B",  # Red
            "pivot": "#F5A623",    # Orange
            "sorted": "#4CAF50",   # Green
            "temp": "#888888"      # Gray
        }

    def draw(self, arr, highlights=None):
        """
        Draws the array as bars on the canvas.
        highlights: dict mapping color names to lists of indices
        """
        self.canvas.delete("all")
        if not arr:
            return

        n = len(arr)
        bar_width = (self.width - 20) / n
        max_val = max(arr) if arr else 1
        
        # Pre-calculate highlight mapping
        idx_colors = {}
        if highlights:
            for color_name, indices in highlights.items():
                hex_color = self.colors.get(color_name, self.colors["default"])
                for idx in indices:
                    idx_colors[idx] = hex_color

        for i, val in enumerate(arr):
            x0 = 10 + i * bar_width
            x1 = 10 + (i + 1) * bar_width - 1
            
            # Normalize height
            bar_height = (val / max_val) * (self.height - 40)
            y0 = self.height - bar_height - 10
            y1 = self.height - 10
            
            color = idx_colors.get(i, self.colors["default"])
            
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=color,
                outline=""
            )

    def clear(self):
        self.canvas.delete("all")
