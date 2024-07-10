import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from matplotlib import ticker

class Framework:
    def __init__(self):
        self.root = tk.Tk()
        self.model = Model()
        self.view = View(master=self.root)
        self.solver = Solver(self.model)  # Pass the model to Solver
        # Initialize visualizers after model, view, and solver
        self.visualizer1 = Visualizer1(master=self.root, view=self.view, model=self.model, solver=self.solver)  # Pass the solver here
        self.controller = Controller(self.model, self.view, self.solver, self.visualizer1)
        self.visualizer2 = Visualizer2(master=self.root, view=self.view, model=self.model, controller=self.controller)
        self.connect_modules()

    def connect_modules(self):
        self.visualizer1.controller = self.controller
        self.visualizer1.model = self.model
        self.visualizer2.view = self.view
        self.visualizer2.model = self.model
        self.visualizer2.controller = self.controller
        self.model.controller = self.controller
        self.solver.model = self.model
        self.controller.solver = self.solver
        
class Visualizer1:
    def __init__(self, master, view, model, solver):  # Add master as a parameter
        self.master = master
        self.view = view
        self.model = model
        self.solver = solver

        # Fields
        self.preliminary_parking_plan = None
        self.number_of_parking_spaces = None

        # Create a frame for data entry
        entry_frame = ttk.Frame(self.master)
        entry_frame.pack(padx=20, pady=20)

        # Preliminary Parking Plan Entry
        ttk.Label(entry_frame, text="Enter Preliminary Parking Plan:").grid(row=0, column=0, sticky='w')
        self.preliminary_parking_plan_entry = ttk.Entry(entry_frame, width=40)
        self.preliminary_parking_plan_entry.grid(row=1, column=0, sticky='w')

        # Number of Parking Spaces Entry
        ttk.Label(entry_frame, text="Enter Number of Parking Spaces:").grid(row=2, column=0, sticky='w')
        self.number_of_parking_spaces_entry = ttk.Entry(entry_frame, width=40)
        self.number_of_parking_spaces_entry.grid(row=3, column=0, sticky='w')

        # Submit button for data entry
        self.submit_button = ttk.Button(entry_frame, text="Submit", command=self.data_entry)
        self.submit_button.grid(row=4, column=0, sticky='w', pady=10)

    def data_entry(self):
        # Method to handle data entry and validation
        self.preliminary_parking_plan = self.preliminary_parking_plan_entry.get()
        self.number_of_parking_spaces = self.number_of_parking_spaces_entry.get()

        # Validate data before passing it to the model
        if self.preliminary_parking_plan and self.number_of_parking_spaces:
            # Assuming preliminary_parking_plan is a string representation of a list
            try:
                self.preliminary_parking_plan = eval(self.preliminary_parking_plan)
                self.number_of_parking_spaces = int(self.number_of_parking_spaces)
                # Pass the validated data to the controller for further processing
                self.controller.handle_data_entry(self.preliminary_parking_plan, self.number_of_parking_spaces)
            except Exception as e:
                print(f"Data Entry Error: {e}")
        else:
            print("Both fields must be filled.")

class Visualizer2:
    def __init__(self, master, view, model, controller):  # Add controller as a parameter
        self.master = master
        self.view = view
        self.model = model
        self.controller = controller

        # Fields
        self.preliminary_parking_plan = None
        self.number_of_parking_spaces = None

        # Methods
        self.display_plans()
        self.customize_display()
        self.specify_operations()
        self.frames_per_second()
        self.start_simulation()
        self.pause_simulation()
        self.stop_simulation()

    def display_plans(self):
        # Placeholder for displaying plans
        display_frame = ttk.LabelFrame(self.master, text="Displayed Plans")
        display_frame.pack(fill="both", expand="yes")
        # Add logic to display plans here

    def customize_display(self):
        # Placeholder for customizing display
        customize_frame = ttk.LabelFrame(self.master, text="Customize Display")
        customize_frame.pack(fill="both", expand="yes")
        # Add logic to customize display here

    def specify_operations(self):
        # Placeholder for specifying number of operations
        operations_frame = ttk.LabelFrame(self.master, text="Number of Operations")
        operations_frame.pack(fill="both", expand="yes")
        # Add logic to specify number of operations here

    def frames_per_second(self):
        # Placeholder for setting frames per second
        fps_frame = ttk.LabelFrame(self.master, text="Frames Per Second")
        fps_frame.pack(fill="both", expand="yes")
        # Add logic to set frames per second here

    def start_simulation(self):
        # Placeholder for starting simulation
        start_button = ttk.Button(self.master, text="Start Simulation", command=self._start_simulation)
        start_button.pack()
        # Add logic to start simulation here

    def pause_simulation(self):
        # Placeholder for pausing simulation
        pause_button = ttk.Button(self.master, text="Pause Simulation", command=self._pause_simulation)
        pause_button.pack()
        # Add logic to pause simulation here

    def stop_simulation(self):
        # Placeholder for stopping simulation
        stop_button = ttk.Button(self.master, text="Stop Simulation", command=self._stop_simulation)
        stop_button.pack()
        # Add logic to stop simulation here

    def _start_simulation(self):
        # Logic for starting the simulation
        pass

    def _pause_simulation(self):
        # Logic for pausing the simulation
        pass

    def _stop_simulation(self):
        # Logic for stopping the simulation
        pass

class Controller:
    def __init__(self, model, view, solver, visualizer1=None):  # Add visualizer1 as a parameter
        self.model = model
        self.view = view
        self.solver = solver
        self.visualizer1 = visualizer1  # Store visualizer1
        
        # Connect View's buttons and entries to corresponding methods
        self.view.start_button.config(command=self.start_simulation)
        self.view.pause_button.config(command=self.pause_simulation)
        self.view.stop_button.config(command=self.stop_simulation)
        self.view.operations_entry.bind("<Return>", lambda event: self.handle_operations())
        self.view.fps_entry.bind("<Return>", lambda event: self.handle_fps())
        
        # Connect Visualizer1's submit button to handle_data_entry method
        self.visualizer1.submit_button.config(command=lambda: self.handle_data_entry(self.visualizer1.preliminary_parking_plan_entry.get(), self.visualizer1.number_of_parking_spaces_entry.get()))

    def handle_operations(self):
        # Handle the number of operations specified by the user
        self.model.number_of_parking_spaces = self.view.operations_entry.get()
        if self.model.number_of_parking_spaces.isdigit():
            self.model.number_of_parking_spaces = int(self.model.number_of_parking_spaces)
            # Update the solver with the new number of parking spaces
            self.solver.number_of_parking_spaces = self.model.number_of_parking_spaces
        else:
            print("Invalid input for number of operations.")

    def handle_fps(self):
        # Handle the frames per second specified by the user
        fps = self.view.fps_entry.get()
        if fps.isdigit():
            fps = int(fps)
            # Store the frames per second for future use in the simulation
            self.fps = fps
        else:
            print("Invalid input for frames per second.")

    def start_simulation(self):
        # Logic for starting the simulation
        # Trigger the model to start calculations or any other necessary action
        self.solver.solve_problem()
        self.model.evaluate_equations()

    def pause_simulation(self):
        # Logic for pausing the simulation
        # Implement any necessary actions to pause the simulation
        pass

    def stop_simulation(self):
        # Logic for stopping the simulation
        # Reset any necessary variables or states
        pass

    def display_plans(self):
        for i, space in enumerate(final_plan_data['parking_plan']):
            # Using the imported Rectangle from matplotlib.patches
            rectangle = mpatches.Rectangle((space[0], space[1]), space[2], space[3], facecolor='black')
            ax.add_patch(rectangle)
        new_varnew_var = self.new_method()
        
        # Method to handle displaying plans
        # Retrieve data from the model and update the view
        final_plan_data = self.model.provide_data_for_final_plans()
        if final_plan_data is not None:
            # Update the view with the final plan data
            # This could involve updating labels, charts, or other UI elements
            # For example:
            # self.view.update_labels(final_plan_data)
            self.view.fig.clear()  # Clear previous drawings
            ax = self.view.fig.add_subplot(111)
            for i, space in enumerate(final_plan_data['parking_plan']):
                ax.add_patch(Rectangle((space[0], space[1]), space[2], space[3], facecolor='black'))
            self.view.canvas.draw()
        else:
            print("No data available to display plans.")

    def new_method(self):
        self.view.canvas.draw()

    def customize_display(self):
        # Method to handle customizing display
        # Retrieve customization settings from the view and apply them to the display
        # For example:
        # color = self.view.get_color_setting()
        # self.view.set_plot_color(color)
        pass

    def handle_data_entry(self, preliminary_parking_plan, number_of_parking_spaces):
        # Method to handle data entry and validation
        # Validate data before passing it to the model
        if preliminary_parking_plan and number_of_parking_spaces:
            # Assuming preliminary_parking_plan is a string representation of a list
            try:
                preliminary_parking_plan = eval(preliminary_parking_plan)
                number_of_parking_spaces = int(number_of_parking_spaces)
                # Pass the validated data to the model
                self.model.preliminary_parking_plan = preliminary_parking_plan
                self.model.number_of_parking_spaces = number_of_parking_spaces
                # Update the solver with the new data
                self.solver.preliminary_parking_plan = self.model.preliminary_parking_plan
                self.solver.number_of_parking_spaces = self.model.number_of_parking_spaces
            except Exception as e:
                print(f"Data Entry Error: {e}")
        else:
            print("Both fields must be filled.")

class View:
    def __init__(self, master):
        self.master = master
        self.master.title("Parking Optimization Application")

        # Canvas for drawing parking lot plans
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Variables for drawing
        self.rectangles = []
        self.current_rectangle = None
        self.selected_rectangle = None
        self.zoom_level = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 10.0

        # Bind mouse events to canvas
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('scroll_event', self.on_scroll)

        # Frame for controls
        control_frame = ttk.Frame(self.master)  # Define control_frame here

        # Color selection
        self.color = 'black'
        self.color_button = ttk.Button(control_frame, text="Switch Color", command=self.switch_color)
        self.color_button.pack(side=tk.LEFT)

        # Eraser tool
        self.is_eraser_mode = False
        self.eraser_button = ttk.Button(control_frame, text="Eraser Mode", command=self.toggle_eraser_mode)
        self.eraser_button.pack(side=tk.LEFT)

        # Undo/Redo
        self.undo_stack = []
        self.redo_stack = []
        self.undo_button = ttk.Button(control_frame, text="Undo", command=self.undo)
        self.undo_button.pack(side=tk.LEFT)
        self.redo_button = ttk.Button(control_frame, text="Redo", command=self.redo)
        self.redo_button.pack(side=tk.LEFT)

        control_frame.pack(side=tk.BOTTOM, fill=tk.X)  # Pack control_frame after all its children have been added

        # Bind keyboard events to canvas
        self.canvas.mpl_connect('key_press_event', self.on_key_press)


        # Button for clearing the canvas
        clear_button = ttk.Button(control_frame, text="Clear", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        # Button for saving the current canvas state
        save_button = ttk.Button(control_frame, text="Save", command=lambda: self.save_parking_plan('parking_plan.png'))
        save_button.pack(side=tk.LEFT)

        # Button for loading a canvas state from a file
        load_button = ttk.Button(control_frame, text="Load", command=lambda: self.load_parking_plan('parking_plan.png'))
        load_button.pack(side=tk.LEFT)

        # Bind keyboard events to canvas
        self.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.is_line_mode = False
        self.is_drawing = False  # New flag to track drawing state
        self.line_start = None
        self.current_shape = None
        self.current_rectangle = None
        
        # Control buttons
        control_frame = ttk.Frame(self.master)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.start_button = ttk.Button(control_frame, text="Start")
        self.start_button.pack(side=tk.LEFT)
        
        self.pause_button = ttk.Button(control_frame, text="Pause")
        self.pause_button.pack(side=tk.LEFT)
        
        self.stop_button = ttk.Button(control_frame, text="Stop")
        self.stop_button.pack(side=tk.LEFT)
        
        self.line_mode_button = ttk.Button(control_frame, text="Line Mode: Off", command=self.toggle_line_mode)
        self.line_mode_button.pack(side=tk.LEFT)
        
        # Operations entry
        operations_frame = ttk.Frame(self.master)
        operations_frame.pack(fill="both", expand="yes")
        ttk.Label(operations_frame, text="Operations:").pack(side=tk.LEFT)
        self.operations_entry = ttk.Entry(operations_frame)
        self.operations_entry.pack(side=tk.LEFT)
        
        # FPS entry
        fps_frame = ttk.Frame(self.master)
        fps_frame.pack(fill="both", expand="yes")
        ttk.Label(fps_frame, text="FPS:").pack(side=tk.LEFT)
        self.fps_entry = ttk.Entry(fps_frame)
        self.fps_entry.pack(side=tk.LEFT)        
        
        self.line_start = None  # Initialize line_start here
        
        self.zoom_level = 1.0
        self.pan_position = (0.0, 0.0)

        # Create sliders for zooming and panning
        self.zoom_slider = ttk.Scale(self.master, from_=1, to=10, orient=tk.HORIZONTAL, command=self.update_zoom)
        self.h_slider = ttk.Scale(self.master, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_horizontal_view)
        self.v_slider = ttk.Scale(self.master, from_=0, to=100, orient=tk.VERTICAL, command=self.update_vertical_view)
        
        # Position sliders
        self.zoom_slider.pack(side=tk.BOTTOM, fill=tk.X)
        self.h_slider.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_slider.pack(side=tk.RIGHT, fill=tk.Y)

        # Set initial slider values
        self.zoom_slider.set(5)
        self.h_slider.set(50)
        self.v_slider.set(50)
        self.scale_factor = 1.0  # Define your scale factor here. Adjust as needed.
        self.lines = []  # List to store line objects

    def undo(self):
        if self.undo_stack:
            action = self.undo_stack.pop()
            if action['type'] == 'rectangle':
                # Remove the rectangle from the canvas and rectangles list
                action['patch'].remove()
                self.rectangles.remove(action['patch'])
            elif action['type'] == 'line':
                # Remove the line from the canvas and lines list
                action['line'].remove()
                self.lines.remove(action['line'])
            self.redo_stack.append(action)
            self.canvas.draw()

    def redo(self):
        if self.redo_stack:
            action = self.redo_stack.pop()
            if action['type'] == 'rectangle':
                # Re-add the rectangle to the canvas and rectangles list
                self.ax.add_patch(action['patch'])
                self.rectangles.append(action['patch'])
            elif action['type'] == 'line':
                # Re-add the line to the canvas and lines list
                self.ax.add_line(action['line'])
                self.lines.append(action['line'])
            self.undo_stack.append(action)
            self.canvas.draw()

                        
    def on_press(self, event):
        if event.button == 1 and event.inaxes == self.ax:
            if self.is_eraser_mode:
                self.is_drawing = True
                self.eraser_start = (event.xdata, event.ydata)
            elif self.is_line_mode:
                self.is_drawing = True
                self.line_start = (event.xdata, event.ydata)
                self.ax.plot([], [], color=self.color)
                self.canvas.draw_idle()
            elif not self.is_line_mode:
                self.is_drawing = True
                x_meters = event.xdata * self.scale_factor
                y_meters = event.ydata * self.scale_factor
                self.current_rectangle = Rectangle((x_meters, y_meters), 0, 0, facecolor=self.color)
                self.ax.add_patch(self.current_rectangle)

    def on_motion(self, event):
        if self.is_drawing:
            if self.is_drawing and self.is_eraser_mode and event.inaxes == self.ax:
                if self.eraser_start is not None:
                    # Determine the eraser area (a rectangle around the mouse cursor)
                    eraser_x, eraser_y = self.eraser_start
                    eraser_width = abs(event.xdata - eraser_x)
                    eraser_height = abs(event.ydata - eraser_y)
                    eraser_rect = Rectangle((eraser_x, eraser_y), eraser_width, eraser_height, facecolor='white', alpha=0.0)

                    # Check each rectangle for intersection with the eraser area
                    for rect in self.rectangles[:]:  # Use a copy to avoid modifying the list while iterating
                        if eraser_rect.contains_point((rect.get_x(), rect.get_y())):
                            rect.remove()
                            self.rectangles.remove(rect)
                            self.canvas.draw_idle()
            elif self.is_drawing and self.is_line_mode and event.inaxes == self.ax:
                if self.line_start is not None:
                    self.ax.lines[-1].set_data([self.line_start[0], event.xdata], [self.line_start[1], event.ydata])
                    self.canvas.draw_idle()
            else:
                if self.current_rectangle is not None:
                    x_meters = event.xdata * self.scale_factor
                    y_meters = event.ydata * self.scale_factor
                    width = abs(event.xdata - self.current_rectangle.get_x())
                    height = abs(event.ydata - self.current_rectangle.get_y())
                    if event.xdata < self.current_rectangle.get_x():
                        self.current_rectangle.set_x(event.xdata)
                    if event.ydata < self.current_rectangle.get_y():
                        self.current_rectangle.set_y(event.ydata)
                    self.current_rectangle.set_width(width)
                    self.current_rectangle.set_height(height)
                    self.canvas.draw_idle()
                    
    def on_release(self, event):
            if self.is_drawing and self.is_eraser_mode and event.inaxes == self.ax:
                self.is_drawing = False
                self.eraser_start = None
            if self.is_drawing and self.is_line_mode and event.inaxes == self.ax:
                if self.line_start is not None and event.xdata is not None and event.ydata is not None:
                    line = self.ax.plot([self.line_start[0], event.xdata], [self.line_start[1], event.ydata], color=self.color)[0]
                    self.canvas.draw_idle()
                    self.is_drawing = False
                    # Ensure the line is added to the lines list
                    self.lines.append(line)
                    # Save the line action to the undo stack
                    self.undo_stack.append({'type': 'line', 'line': line})
            else:
                if self.current_rectangle is not None:
                    self.rectangles.append(self.current_rectangle)
                    self.current_rectangle = None
                    self.is_drawing = False
                    self.canvas.draw_idle()
                    # Save the rectangle action to the undo stack
                    self.undo_stack.append({'type': 'rectangle', 'patch': self.rectangles[-1]})

    def clear_canvas(self):
        # Clear rectangles
        for rect in self.rectangles:
            rect.remove()
        self.rectangles = []

        # Clear lines
        for line in self.lines:
            line.remove()
        self.lines = []

        # Redraw the canvas
        self.canvas.draw()

    def find_selected_rectangle(self, x, y):
        for rect in self.rectangles:
            if rect.contains_point((x, y)):
                return rect
        return None

    def on_scroll(self, event):
        if event.button == 'up':
            self.zoom_level *= 1.1
        elif event.button == 'down':
            self.zoom_level /= 1.1
        self.zoom_level = max(min(self.zoom_level, self.max_zoom), self.min_zoom)
        self.ax.set_xlim(self.ax.get_xlim()[0] * self.zoom_level, self.ax.get_xlim()[1] * self.zoom_level)
        self.ax.set_ylim(self.ax.get_ylim()[0] * self.zoom_level, self.ax.get_ylim()[1] * self.zoom_level)
        self.canvas.draw()

    def on_key_press(self, event):
        if event.key == 'delete':
            self.delete_selected_rectangle()

    def delete_selected_rectangle(self):
        if self.selected_rectangle is not None:
            self.selected_rectangle.remove()
            self.rectangles.remove(self.selected_rectangle)
            self.selected_rectangle = None
            self.canvas.draw()
            
    def save_parking_plan(self, filename):
        """
        Saves the current state of the canvas as an image file.
        :param filename: The path and filename to save the image as.
        """
        # Draw the canvas to a PIL Image
        self.canvas.draw()
        canvas_width, canvas_height = self.canvas.get_width_height()
        image = Image.frombytes('RGB', (canvas_width, canvas_height), self.canvas.tostring_rgb())
        image.save(filename)
 
    def switch_color(self):
        """Switches the color used for drawing rectangles."""
        if self.color == 'black':
            self.color = 'red'
        else:
            self.color = 'black'
        # Optionally, you can update the text of the color button to reflect the new color
        self.color_button.config(text=f"Color: {self.color}")
    
    def toggle_eraser_mode(self):
        self.is_eraser_mode = not self.is_eraser_mode
        if self.is_eraser_mode:
            self.eraser_button.config(text="Eraser Mode: On")
            self.is_drawing = False  # Reset drawing state
        else:
            self.eraser_button.config(text="Eraser Mode: Off")
            self.is_drawing = False  # Reset drawing state

        # Add any additional logic for changing behavior based on eraser mode    

        
    def toggle_line_mode(self):
        self.is_line_mode = not self.is_line_mode
        if self.is_line_mode:
            self.line_mode_button.config(text="Line Mode: On")
        else:
            self.line_mode_button.config(text="Line Mode: Off")
            
    def update_zoom(self, value):
        # Update the zoom level based on the slider value
        self.zoom_level = float(value) / 5  # Assuming the mid-point represents the original zoom level

        # Get the current center of the view
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        center = ((xlim[0] + xlim[1]) / 2, (ylim[0] + ylim[1]) / 2)

        # Calculate the new limits based on the zoom factor and center
        new_xlim = (center[0] - (xlim[1] - xlim[0]) * self.zoom_level / 2,
                    center[0] + (xlim[1] - xlim[0]) * self.zoom_level / 2)
        new_ylim = (center[1] - (ylim[1] - ylim[0]) * self.zoom_level / 2,
                    center[1] + (ylim[1] - ylim[0]) * self.zoom_level / 2)

        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.canvas.draw()

    def update_horizontal_view(self, value):
        # Update the horizontal view based on the slider value
        self.pan_position = (float(value) / 100, self.pan_position[1])

        # Get the current center of the view
        xlim = self.ax.get_xlim()
        center = ((xlim[0] + xlim[1]) / 2, (self.ax.get_ylim()[0] + self.ax.get_ylim()[1]) / 2)

        # Calculate the new limits based on the pan position and center
        new_xlim = (center[0] - (xlim[1] - xlim[0]) * (1 - self.pan_position[0]),
                    center[0] + (xlim[1] - xlim[0]) * (self.pan_position[0]))

        self.ax.set_xlim(new_xlim)
        self.canvas.draw()

    def update_vertical_view(self, value):
        # Update the vertical view based on the slider value
        self.pan_position = (self.pan_position[0], float(value) / 100)

        # Get the current center of the view
        ylim = self.ax.get_ylim()
        center = ((self.ax.get_xlim()[0] + self.ax.get_xlim()[1]) / 2, (ylim[0] + ylim[1]) / 2)

        # Calculate the new limits based on the pan position and center
        new_ylim = (center[1] - (ylim[1] - ylim[0]) * (1 - self.pan_position[1]),
                    center[1] + (ylim[1] - ylim[0]) * (self.pan_position[1]))

        self.ax.set_ylim(new_ylim)
        self.canvas.draw()

        
    def update_axis_labels(self):
        # Get the current axis limits in abstract units
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        # Convert limits to meters using the scale factor
        xlim_meters = [lim * self.scale_factor for lim in xlim]
        ylim_meters = [lim * self.scale_factor for lim in ylim]
        # Set the new limits
        self.ax.set_xlim(xlim_meters)
        self.ax.set_ylim(ylim_meters)
        # Update tick labels to show meters
        self.ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{x:.2f}m"))
        self.ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: f"{y:.2f}m"))
        # Redraw the canvas
        self.canvas.draw()     


class Model:
    def __init__(self):
        # Fields
        self.preliminary_parking_plan = None
        self.number_of_parking_spaces = None
        self.results = None

    def evaluate_equations(self):
        """
        Method to calculate equations based on the preliminary parking plan
        and the number of parking spaces. The results of these calculations
        are stored in the 'results' field.
        """
        if self.preliminary_parking_plan is not None and self.number_of_parking_spaces is not None:
            # Example equation evaluation (replace this with your actual calculations)
            # Let's assume we are calculating efficiency based on the number of parking spaces
            efficiency = np.sum(self.preliminary_parking_plan) / self.number_of_parking_spaces
            self.results = {'efficiency': efficiency}
        else:
            print("Preliminary parking plan or number of parking spaces not provided.")

    def provide_data_for_final_plans(self):
        """
        Method to prepare and provide data for generating the final parking plans.
        This method should return the necessary data structures for the final plans.
        """
        if self.results is not None:
            # Example data preparation (replace this with your actual data preparation)
            final_plan_data = {
                'parking_plan': self.preliminary_parking_plan,
                'number_of_spaces': self.number_of_parking_spaces,
                'efficiency': self.results['efficiency']
            }
            return final_plan_data
        else:
            print("No results available to generate final plans.")
            return None
        
class Solver:
    def __init__(self, model):  # Add model as a parameter
        self.model = model
        # Fields
        self.preliminary_parking_plan = None
        self.number_of_parking_spaces = None

    def solve_problem(self):
        """
        Method to solve the parking optimization problem using the preliminary parking plan
        and the number of parking spaces. This method should perform the necessary calculations
        and store the results in the 'results' field of the associated Model instance.
        """
        if self.preliminary_parking_plan is not None and self.number_of_parking_spaces is not None:
            # Call the method to calculate equations
            self.calculate_equations()
        else:
            print("Preliminary parking plan or number of parking spaces not provided.")

    def calculate_equations(self):
        """
        Method to perform calculations based on the preliminary parking plan and the number of parking spaces.
        The results of these calculations are intended to optimize the parking space usage.
        """
        # Example calculation (replace this with your actual calculations)
        # Let's assume we are calculating the average parking space size
        average_space_size = sum(self.preliminary_parking_plan) / self.number_of_parking_spaces
        # Update the results in the Model
        self.model.results = {'average_space_size': average_space_size}

    def provide_results(self):
        """
        Method to provide the results of the calculations to the Model.
        This method should ensure that the results are available for generating the final plans.
        """
        if self.model.results is not None:
            # Example data preparation (replace this with your actual data preparation)
            final_plan_data = {
                'parking_plan': self.preliminary_parking_plan,
                'number_of_spaces': self.number_of_parking_spaces,
                'average_space_size': self.model.results['average_space_size']
            }
            return final_plan_data
        else:
            print("No results available to generate final plans.")
            return None

    def transfer_data(self, model, view, controller):
        """
        Method to transfer data between the Model, View, and Controller.
        This method facilitates the interaction between the different components
        of the MVC architecture.
        """
        # Transfer data from Model to Solver
        if self.preliminary_parking_plan is None:
            self.preliminary_parking_plan = model.preliminary_parking_plan
        if self.number_of_parking_spaces is None:
            self.number_of_parking_spaces = model.number_of_parking_spaces

        # Transfer data from Solver to Model
        if model.preliminary_parking_plan is None:
            model.preliminary_parking_plan = self.preliminary_parking_plan
        if model.number_of_parking_spaces is None:
            model.number_of_parking_spaces = self.number_of_parking_spaces

        # Additional logic for managing the data flow can be added here.

if __name__ == "__main__":
    app = Framework()
    app.view.update_axis_labels()
    app.root.mainloop()
    
