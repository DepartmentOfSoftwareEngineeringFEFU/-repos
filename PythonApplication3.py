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
from PIL import Image, ImageDraw

class Framework:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Parking Space Optimization")
        self.view = View(master=self.root, controller=None)  # Pass None initially
        self.model = Model()
        self.solver = Solver(self.model)  # Pass the model to Solver
        self.visualizer1 = Visualizer1(master=self.root, view=self.view, model=self.model, solver=self.solver)  # Pass the solver here
        self.controller = Controller(self.model, self.view, self.solver, self.visualizer1)
        self.visualizer2 = Visualizer2(master=self.root, view=self.view, model=self.model, controller=self.controller)
        self.connect_modules()
        self.view.controller = self.controller  # Assign the controller after it's defined


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
       
        # Connect Visualizer1's submit button to handle_data_entry method
        self.visualizer1.submit_button.config(command=lambda: self.handle_data_entry(self.visualizer1.preliminary_parking_plan_entry.get(), self.visualizer1.number_of_parking_spaces_entry.get()))

        # Connect View's buttons and entries to corresponding methods


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
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.master.title("Raster Graphics Application")

        # Initialize canvas size and create a new image
        self.canvas_size = (800, 600)
        self.image = Image.new('RGB', self.canvas_size, 'white')
        self.draw = ImageDraw.Draw(self.image)

        # Setup Matplotlib figure
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Control panel setup
        control_frame = ttk.Frame(self.master)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Define buttons
        self.create_button(control_frame, "Clear", self.clear_canvas)
        self.create_button(control_frame, "Save", self.save_image)
        self.create_button(control_frame, "Load", self.load_image)
        self.create_button(control_frame, "Eraser Mode", self.toggle_eraser_mode)
        self.create_button(control_frame, "Line Mode: Off", self.toggle_line_mode)
        self.canvas.mpl_connect('button_press_event', self.on_flood_fill_click)

        # Start, Pause, Stop buttons
        if self.controller:
            self.create_button(control_frame, "Start", self.controller.start_simulation)
            self.create_button(control_frame, "Pause", self.controller.pause_simulation)
            self.create_button(control_frame, "Stop", self.controller.stop_simulation)

        # Bind canvas events
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)

        # Initialize state variables
        self.is_drawing = False
        self.is_eraser_mode = False
        self.is_line_mode = False
        self.color = 'black'
        self.current_shape = None
        self.current_pos = None

        self.is_flood_fill_mode = False
        self.create_button(control_frame, "Flood Fill", self.toggle_flood_fill_mode)

        # Bind left mouse button click event to trigger flood fill
        self.canvas.mpl_connect('button_press_event', self.on_flood_fill_click)
        self.resolution = 100  # 1 meter = 100 pixels

    def create_button(self, parent, text, command):
        ttk.Button(parent, text=text, command=command).pack(side=tk.LEFT)

    def create_label_entry(self, parent, label_text, entry_reference):
        ttk.Label(parent, text=label_text).pack(side=tk.LEFT)
        entry_reference = ttk.Entry(parent, width=10)
        entry_reference.pack(side=tk.LEFT)

    def clear_canvas(self):
        self.image = Image.new('RGB', self.canvas_size, 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.update_image()

    def save_image(self):
        self.image.save('raster_canvas.png')

    def load_image(self):
        self.image = Image.open('raster_canvas.png')
        self.draw = ImageDraw.Draw(self.image)
        self.update_image()

    def toggle_eraser_mode(self):
        self.is_eraser_mode = not self.is_eraser_mode
        mode_text = "On" if self.is_eraser_mode else "Off"
        self.master.children['!frame'].children['!button4'].config(text=f"Eraser Mode: {mode_text}")

    def toggle_line_mode(self):
        self.is_line_mode = not self.is_line_mode
        mode_text = "On" if self.is_line_mode else "Off"
        self.master.children['!frame'].children['!button5'].config(text=f"Line Mode: {mode_text}")

    def update_image(self):
        self.ax.imshow(self.image)
        self.canvas.draw()

    def on_press(self, event):
        if self.is_eraser_mode or self.is_line_mode:
            self.current_pos = (event.xdata, event.ydata)
            self.is_drawing = True
        else:
            self.current_shape = self.draw.rectangle((event.xdata, event.ydata, event.xdata, event.ydata), fill=self.color)
            self.is_drawing = True

    def on_motion(self, event):
        if self.is_drawing:
            if self.current_pos is None:
                self.current_pos = (event.xdata, event.ydata)
            else:
                if self.is_eraser_mode:
                    # Eraser mode logic...
                    pass
                elif self.is_line_mode:
                    # Convert coordinates from meters to pixels
                    x0, y0 = self.current_pos
                    x1, y1 = event.xdata * self.resolution, event.ydata * self.resolution
                
                    # Draw a line
                    self.draw.line([x0, y0, x1, y1], fill=self.color, width=2)
                
                    # Update the current position for continuous line drawing
                    self.current_pos = (x1, y1)
                
                    # Update the image on the canvas
                    self.update_image()
                else:
                    # Convert coordinates from meters to pixels
                    x0, y0 = self.current_pos
                    x1, y1 = event.x * self.resolution, event.y * self.resolution
                    rect_coords = (int(x0), int(y0), int(x1), int(y1))
                    self.draw.rectangle(rect_coords, fill=self.color)
                    # Update the image on the canvas
                    self.update_image()

    def on_release(self, event):
        if self.is_drawing:
            if self.is_eraser_mode:
                # Eraser mode logic for raster graphics
                # Here, we convert the coordinates to integers and then draw a pixel with the background color
                x, y = int(event.xdata), int(event.ydata)
                if 0 <= x < self.canvas_size[0] and 0 <= y < self.canvas_size[1]:
                    self.draw.point((x, y), fill='white')  # Assuming white is the background color
                    self.update_image()

            elif self.is_line_mode:
                # Line mode logic for raster graphics
                # Draw a line between the initial press point and the release point
                x0, y0 = self.current_pos
                x1, y1 = int(event.xdata), int(event.ydata)
                if 0 <= x0 < self.canvas_size[0] and 0 <= y0 < self.canvas_size[1] and \
                   0 <= x1 < self.canvas_size[0] and 0 <= y1 < self.canvas_size[1]:
                    # Draw a line using Bresenham's algorithm or similar for raster graphics
                    # Here, we'll just call the line method of ImageDraw
                    self.draw.line([(x0, y0), (x1, y1)], fill=self.color, width=2)
                    self.update_image()

            else:
                # Drawing mode logic for raster graphics
                # Here, we convert the coordinates to integers and then draw a pixel with the current color
                x, y = int(event.xdata), int(event.ydata)
                if 0 <= x < self.canvas_size[0] and 0 <= y < self.canvas_size[1]:
                    self.draw.point((x, y), fill=self.color)
                    self.update_image()

            # Reset drawing state
            self.is_drawing = False
            self.current_pos = None
            
    def toggle_flood_fill_mode(self):
        self.is_flood_fill_mode = not self.is_flood_fill_mode
        mode_text = "On" if self.is_flood_fill_mode else "Off"
        self.master.children['!frame'].children['!button6'].config(text=f"Flood Fill Mode: {mode_text}")

    def on_flood_fill_click(self, event):
        if self.is_flood_fill_mode:
            self.flood_fill(int(event.xdata), int(event.ydata))

    def flood_fill(self, x, y, target_color='white', replacement_color='black'):
        """Perform a flood fill operation on the canvas."""
        if not (0 <= x < self.canvas_size[0]) or not (0 <= y < self.canvas_size[1]):
            return

        current_color = self.image.getpixel((x, y))

        if current_color != target_color:
            return

        self.draw.point((x, y), fill=replacement_color)

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left

        for dx, dy in directions:
            self.flood_fill(x + dx, y + dy, target_color, replacement_color)

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
    app.root.mainloop()
    

