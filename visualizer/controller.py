from typing import Generator, Dict, List, Any, Optional, Callable
import tkinter as tk
from visualizer.renderer import CanvasRenderer
from engines.base_sort import BaseSort

class SortingController:
    """
    Manages the animation loop and bridges the GUI state with the sorting engine generator.
    
    Uses Tkinter's non-blocking `canvas.after` event loop recursion to pull frames
    from the sorting generator sequentially at a configurable speed.
    """
    
    def __init__(
        self, 
        canvas: tk.Canvas, 
        renderer: CanvasRenderer, 
        on_finish_callback: Optional[Callable[[], None]] = None
    ) -> None:
        """
        Initializes the SortingController.
        
        Args:
            canvas (tk.Canvas): The canvas widget.
            renderer (CanvasRenderer): The renderer responsible for drawing arrays.
            on_finish_callback (Optional[Callable[[], None]]): Function to execute when sorting completes.
        """
        self.canvas = canvas
        self.renderer = renderer
        self.on_finish = on_finish_callback
        
        self.array: List[Any] = []
        self.engine: Optional[BaseSort] = None
        self.generator: Optional[Generator[Dict[str, Any], None, None]] = None
        
        self.is_playing = False
        self.delay_ms = 50
        self.after_id: Optional[str] = None
        self.current_state: Optional[Dict[str, Any]] = None

    def reset(self, array: List[Any], engine: Optional[BaseSort] = None) -> None:
        """
        Resets the controller state with a new/clone array and sorting engine.
        
        Args:
            array (List[Any]): The array to be sorted.
            engine (Optional[BaseSort]): The sorting algorithm engine to use.
        """
        self.pause()
        
        self.array = list(array)
        self.engine = engine
        
        # Setup initial visual presentation
        self.renderer.setup(self.array)
        
        if self.engine is not None and len(self.array) > 0:
            # Instantiate a new generator for sorting this specific array
            self.generator = self.engine.sort(self.array)
        else:
            self.generator = None

        self.current_state = {
            "array": list(self.array),
            "comparing": None,
            "swapping": None
        }

    def play(self) -> None:
        """
        Starts or resumes the sorting animation loop.
        """
        if self.is_playing:
            return
            
        if self.generator is None:
            # Gracefully do nothing if data or engine has not been set up
            return
            
        self.is_playing = True
        self._tick()

    def pause(self) -> None:
        """
        Pauses the sorting animation loop.
        """
        self.is_playing = False
        if self.after_id is not None:
            self.canvas.after_cancel(self.after_id)
            self.after_id = None

    def set_speed(self, ms: int) -> None:
        """
        Sets the animation frame delay in milliseconds.
        
        Args:
            ms (int): Speed delay in milliseconds.
        """
        self.delay_ms = max(1, ms)

    def _tick(self) -> None:
        """
        Executes a single step of the sorting algorithm and schedules the next one.
        """
        if not self.is_playing or self.generator is None:
            return

        try:
            # Retrieve the next frame of state from the sorting engine generator
            state = next(self.generator)
            self.current_state = state
            
            # Render the updated state
            self.renderer.update(state)
            
            # Schedule next frame in delay_ms milliseconds
            self.after_id = self.canvas.after(self.delay_ms, self._tick)
        except StopIteration:
            # Generator exhausted. Sorting is complete.
            self.is_playing = False
            self.after_id = None
            self.renderer.draw_sorted()
            if self.on_finish:
                self.on_finish()
        except Exception as e:
            # Safety fallback for unexpected errors during execution
            self.pause()
            print(f"Error during sorting iteration: {e}")
