import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle, Circle
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageTk
from matplotlib import ticker
from tkinter import Canvas, filedialog
import cv2
from scipy.ndimage.measurements import label




class Framework:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Parking Space Optimization")
        # Apply ttk theme
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
        self.width_of_parking_lot = None
        self.vehicle_type_var = tk.BooleanVar()
        self.vehicle_type = 'car' if self.vehicle_type_var.get() else 'truck'

        # Create a frame for data entry
        entry_frame = ttk.Frame(self.master)
        entry_frame.pack(padx=20, pady=20)

        # Preliminary Parking Plan Entry
        ttk.Label(entry_frame, text="Upload Preliminary Parking Plan Image:").grid(row=0, column=0, sticky='w')
        self.preliminary_parking_plan_button = ttk.Button(entry_frame, text="Select Image", command=self.select_image)
        self.preliminary_parking_plan_button.grid(row=1, column=0, sticky='w')

        # Number of Parking Spaces Entry
        ttk.Label(entry_frame, text="Enter Number of Parking Spaces:").grid(row=2, column=0, sticky='w')
        self.number_of_parking_spaces_entry = ttk.Entry(entry_frame, width=40)
        self.number_of_parking_spaces_entry.grid(row=3, column=0, sticky='w')

        # Width of Parking Lot Entry
        ttk.Label(entry_frame, text="Enter Width of Parking Lot (meters):").grid(row=4, column=0, sticky='w')
        self.width_of_parking_lot_entry = ttk.Entry(entry_frame, width=40)
        self.width_of_parking_lot_entry.grid(row=5, column=0, sticky='w')

        # Vehicle Type Checkbox
        self.vehicle_type_var = tk.BooleanVar()
        ttk.Checkbutton(entry_frame, text="Vehicles are Cars", variable=self.vehicle_type_var).grid(row=6, column=0, sticky='w')

        # Submit button for data entry
        self.submit_button = ttk.Button(entry_frame, text="Submit", command=self.data_entry)
        self.submit_button.grid(row=7, column=0, sticky='w', pady=10)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            self.preliminary_parking_plan = file_path
            # You might want to display the image in the GUI here using the View module

    def data_entry(self):
        # Method to handle data entry and validation
        if self.preliminary_parking_plan and self.number_of_parking_spaces_entry.get() and self.width_of_parking_lot_entry.get():
            try:
                self.number_of_parking_spaces = int(self.number_of_parking_spaces_entry.get())
                self.width_of_parking_lot = float(self.width_of_parking_lot_entry.get())
                self.vehicle_type = 'car' if self.vehicle_type_var.get() else 'truck'
                # Pass the validated data to the controller for further processing
                self.controller.handle_data_entry(self.preliminary_parking_plan, self.number_of_parking_spaces, self.width_of_parking_lot, self.vehicle_type)
            except Exception as e:
                print(f"Data Entry Error: {e}")
        else:
            print("All fields must be filled.")


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

    def data_entry(self):
        # Method to handle data entry and validation
        if self.preliminary_parking_plan and self.number_of_parking_spaces_entry.get() and self.width_of_parking_lot_entry.get():
            try:
                number_of_parking_spaces = int(self.number_of_parking_spaces_entry.get())
                width_of_parking_lot = float(self.width_of_parking_lot_entry.get())
                vehicle_type = self.vehicle_type_var.get()  # Already a boolean
                # Pass the validated data to the controller for further processing
                self.controller.handle_data_entry(self.preliminary_parking_plan, number_of_parking_spaces, width_of_parking_lot, vehicle_type)
            except ValueError as ve:
                # Handle ValueError which occurs if conversion fails
                print(f"Data Entry Error: {ve}")
        else:
            print("All fields must be filled.")

class Controller:
    def __init__(self, model, view, solver, visualizer1):
        self.model = model
        self.view = view
        self.solver = solver
        self.visualizer1 = visualizer1  # Store visualizer1

        # Connect Visualizer1's submit button to handle_data_entry method
        self.visualizer1.submit_button.config(command=self.handle_data_entry)
        
        # Connect View's buttons and entries to corresponding methods
       
        # Connect Visualizer1's submit button to handle_data_entry method
        self.visualizer1.submit_button.config(command=self.handle_data_entry)
        
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

    def handle_data_entry(self):
        # Method to handle data entry and validation
        if self.visualizer1.preliminary_parking_plan and \
           self.visualizer1.number_of_parking_spaces_entry.get() and \
           self.visualizer1.width_of_parking_lot_entry.get():

            try:
                number_of_parking_spaces = int(self.visualizer1.number_of_parking_spaces_entry.get())
                width_of_parking_lot = float(self.visualizer1.width_of_parking_lot_entry.get())
                vehicle_type = self.visualizer1.vehicle_type_var.get()  # Already a boolean

                # Pass the validated data to the model and solver for further processing
                self.model.preliminary_parking_plan = self.visualizer1.preliminary_parking_plan
                self.model.number_of_parking_spaces = number_of_parking_spaces
                self.model.width_of_parking_lot = width_of_parking_lot
                self.model.vehicle_type = vehicle_type

                self.solver.preliminary_parking_plan = self.model.preliminary_parking_plan
                self.solver.number_of_parking_spaces = self.model.number_of_parking_spaces
                self.solver.width_of_parking_lot = self.model.width_of_parking_lot
                self.solver.vehicle_type = self.model.vehicle_type

                # Further processing or triggering the solver can be done here
                self.solver.solve_problem()

            except ValueError as ve:
                print(f"Data Entry Error: {ve}")
        else:
            print("All fields must be filled.")
    def process_data(self, image_path, number_of_parking_spaces, width_of_parking_lot, vehicle_type):
        # Load the image from the provided path
        image = Image.open(image_path)
        self.model.preliminary_parking_plan = image
        self.model.number_of_parking_spaces = number_of_parking_spaces
        self.model.width_of_parking_lot = width_of_parking_lot
        self.model.vehicle_type = vehicle_type
        # Update the solver with the new data
        self.solver.preliminary_parking_plan = self.model.preliminary_parking_plan
        self.solver.number_of_parking_spaces = self.model.number_of_parking_spaces
        self.solver.width_of_parking_lot = self.model.width_of_parking_lot
        self.solver.vehicle_type = self.model.vehicle_type

class View:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.master.title("Raster Graphics Application")

        # Setup Raster Image and Draw object
        self.image = Image.new('RGB', (800, 600), 'white')  # Default size
        self.draw = ImageDraw.Draw(self.image)
        self.canvas_size = self.image.size

        # Create a frame to hold the Tkinter canvas
        self.canvas_frame = ttk.Frame(self.master)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a Tkinter canvas for displaying the raster image
        self.canvas = tk.Canvas(self.canvas_frame, bg='white', width=self.canvas_size[0], height=self.canvas_size[1])
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Bind canvas events
        self.canvas.bind('<Button-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_motion)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)

        # Create a frame for controls (buttons, etc.)
        self.control_frame = ttk.Frame(self.master)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Define buttons
        self.create_button(self.control_frame, "Clear", self.clear_canvas)
        self.create_button(self.control_frame, "Undo", self.undo_action)
        self.create_button(self.control_frame, "Fill", self.fill_area)
        self.create_button(self.control_frame, "Eraser", self.erase_mode)
        self.create_button(self.control_frame, "Line", self.line_mode)
        self.create_button(self.control_frame, "Rectangle", self.rectangle_mode)
        self.create_button(self.control_frame, "Save", self.save_canvas)  # New save button
        self.create_button(self.control_frame, "Load", self.load_canvas)  # New load button

        # Initialize state variables
        self.is_drawing = False
        self.is_erasing = False
        self.is_filling = False
        self.is_line_mode = False
        self.is_rectangle_mode = False
        self.current_shape = None
        self.current_pos = None
        self.undo_stack = []

        # Update the canvas with the initial image
        self.update_image()

    def create_button(self, parent, text, command):
        button = ttk.Button(parent, text=text, command=command)
        button.pack(side=tk.LEFT)
        return button

    def clear_canvas(self):
        self.image = Image.new('RGB', self.canvas_size, 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.undo_stack = []  # Clear undo stack when clearing the canvas
        self.update_image()

    def undo_action(self):
        if self.undo_stack:
            self.image, self.draw = self.undo_stack.pop()
            self.update_image()
            
    def line_mode(self):
        self.is_line_mode = True
        self.is_rectangle_mode = False
        self.is_erasing = False
        self.is_filling = False


    def fill_area(self):
        self.is_filling = True

    def erase_mode(self):
        self.is_erasing = True
        self.is_line_mode = False
        self.is_rectangle_mode = False
        self.is_filling = False


    def fill_area(self):
        self.is_filling = True
        self.is_line_mode = False  # Add this line
        self.is_rectangle_mode = False  # And this line

    def rectangle_mode(self):
        self.is_rectangle_mode = True
        self.is_line_mode = False  # Add this line


    def update_image(self):
        self.canvas.delete("all")
        # Convert PIL Image to PhotoImage
        photo_image = ImageTk.PhotoImage(self.image)
        # Ensure the PhotoImage is not garbage collected by keeping a reference
        self.canvas.image = photo_image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)

    def on_press(self, event):
        self.undo_stack.append((self.image.copy(), self.draw))
        if self.is_line_mode:
            self.current_pos = (event.x, event.y)
            self.is_drawing = True
        elif self.is_rectangle_mode:
            self.current_shape = (event.x, event.y, event.x, event.y)
            self.is_drawing = True
        elif self.is_erasing:
            self.draw.point((event.x, event.y), fill='white')
            self.update_image()

    def on_motion(self, event):
        if self.is_drawing:
            if self.is_line_mode:
                self.draw.line([self.current_pos, (event.x, event.y)], fill='black', width=5)
                self.current_pos = (event.x, event.y)
                self.update_image()
            elif self.is_rectangle_mode:
                self.draw.rectangle([self.current_shape[0], self.current_shape[1], event.x, event.y], outline='black', width=5)
                self.current_shape.extend([event.x, event.y])
                self.update_image()
        elif self.is_erasing:
            self.draw.rectangle([event.x-5, event.y-5, event.x+5, event.y+5], fill='white')
            self.update_image()

    def on_release(self, event):
        if self.is_drawing:
            if self.is_line_mode:
                # Draw the line when the mouse button is released
                if self.current_pos is not None:
                    self.draw.line([self.current_pos, (event.x, event.y)], fill='black', width=5)
                    self.update_image()
                self.current_pos = None
                self.is_drawing = False
                self.is_line_mode = False  # Add this line
                self.is_rectangle_mode = False  # And this line
            else:
                self.draw.rectangle(self.current_shape, outline='black', width=5)
                self.current_shape = None
                self.is_drawing = False
                self.update_image()
        elif self.is_filling:
            self.flood_fill(event.x, event.y)
            self.is_filling = False
        self.is_erasing = False  # Add this line

    def flood_fill(self, x, y, target_color=(255, 255, 255), replacement_color=(0, 0, 0)):
        # Check if the starting pixel is the target color
        current_color = self.image.getpixel((x, y))
        if current_color == target_color:
            # Replace the color at the starting point
            self.draw.point((x, y), replacement_color)
            # Recursive calls on adjacent pixels
            if x > 0:
                self.flood_fill(x - 1, y, target_color, replacement_color)
            if x < self.canvas_size[0] - 1:
                self.flood_fill(x + 1, y, target_color, replacement_color)
            if y > 0:
                self.flood_fill(x, y - 1, target_color, replacement_color)
            if y < self.canvas_size[1] - 1:
                self.flood_fill(x, y + 1, target_color, replacement_color)
            self.update_image()
    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.image.save(file_path)
            print(f"Image saved to {file_path}")

    def load_canvas(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            self.image = Image.open(file_path)
            self.update_image()

class Model:
    def __init__(self):
        # Fields
        self.preliminary_parking_plan = None  # Now an image
        self.number_of_parking_spaces = None
        self.results = None

    def load_parking_plan(self, file_path):
        self.preliminary_parking_plan = Image.open(file_path)

    def save_parking_plan(self, file_path):
        self.preliminary_parking_plan.save(file_path)

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
        self.preliminary_parking_plan = None
        self.number_of_parking_spaces = None
        self.width_of_parking_lot = None
        self.vehicle_type = None
        self.vehicle_dimensions = {'car': (4.5, 2.0), 'truck': (6.0, 2.5)}  # Length, Width

    def solve_problem(self):
        if self.preliminary_parking_plan is not None and self.width_of_parking_lot is not None and self.vehicle_type is not None:
            # Ensure preliminary_parking_plan is an Image object
            if isinstance(self.preliminary_parking_plan, str):
                self.preliminary_parking_plan = Image.open(self.preliminary_parking_plan)
        
            # Now you can use .size to get the image dimensions
            image_width, image_height = self.preliminary_parking_plan.size
            # Assuming the longer dimension represents the length
            parking_lot_length = max(image_width, image_height)
            img_gray = np.array(self.preliminary_parking_plan.convert('L'))
            img_binary = (img_gray < 255).astype(np.uint8)
            labeled_img, num_features = label(img_binary)
            max_area = 0
            max_label = 0
            for label_id in range(1, num_features + 1):
                mask = labeled_img == label_id
                area = np.sum(mask)
                if area > max_area:
                    max_area = area
                    max_label = label_id

            # Calculate the area of the largest non-white space
            largest_non_white_area = np.sum(labeled_img == max_label)

            # Calculate the area of the parking lot
            parking_lot_area = self.width_of_parking_lot * parking_lot_length

            # Scale the vehicle dimensions
            if self.vehicle_type is True:
                vehicle_length, vehicle_width = 4.5, 2.0
            else:
                vehicle_length, vehicle_width = 6.0, 2.5    

            # Calculate the number of vehicles fitting in various orientations
            # Calculate the number of vehicles that can fit based on the selected orientation
            orientations = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # North, South, East, West
            vehicle_counts = []
            for orientation in orientations:
                # Calculate the number of vehicles that can fit vertically and horizontally
                vertical_fit = parking_lot_length // vehicle_length
                horizontal_fit = self.width_of_parking_lot // vehicle_width  # Use self.width_of_parking_lot instead of parking_lot_width
                vehicle_counts.append(vertical_fit * horizontal_fit)


            # Select the first orientation and create a visualization
            selected_orientation = orientations[0]

            # Print the number of vehicles calculated for each orientation
            for count in vehicle_counts:
                print(f"Number of {self.vehicle_type}s that can fit: {count}")

        else:
            print("Preliminary parking plan, width of parking lot, or vehicle type not provided.")

    def calculate_equations(self):
        # Assuming the goal is to calculate additional metrics based on the parking plan and vehicle type
        occupied_area = self.number_of_parking_spaces * self.vehicle_dimensions[self.vehicle_type][0] * self.vehicle_dimensions[self.vehicle_type][1]
        total_area = self.parking_lot_length * self.width_of_parking_lot
        occupancy_percentage = (occupied_area / total_area) * 100

        # Update the results in the Model
        self.model.results = {'occupancy_percentage': occupancy_percentage}

    def provide_results(self):
        if self.model.results is not None:
            final_plan_data = {
                'parking_plan': self.preliminary_parking_plan,
                'number_of_spaces': self.number_of_parking_spaces,
                'occupancy_percentage': self.model.results.get('occupancy_percentage')
            }
            return final_plan_data
        else:
            return {}

    def transfer_data(self, model, view, controller):
        # Transfer data from Model to Solver
        self.preliminary_parking_plan = model.preliminary_parking_plan
        self.number_of_parking_spaces = model.number_of_parking_spaces
        self.width_of_parking_lot = model.width_of_parking_lot
        self.vehicle_type = model.vehicle_type

        # Transfer data from Solver to Model
        model.preliminary_parking_plan = self.preliminary_parking_plan
        model.number_of_parking_spaces = self.number_of_parking_spaces
        model.width_of_parking_lot = self.width_of_parking_lot
        model.vehicle_type = self.vehicle_type

    def analyze_parking_plan(self):
        # Convert the image to grayscale for easier processing
        gray = cv2.cvtColor(np.array(self.preliminary_parking_plan), cv2.COLOR_RGB2GRAY)
        print("Converted image to grayscale.")

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        print("Applied Gaussian blur to reduce noise.")

        # Apply adaptive thresholding to binarize the image
        binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        print("Applied adaptive thresholding to binarize the image.")

        # Apply morphological opening (erosion followed by dilation) to remove small objects
        kernel = np.ones((3, 3), np.uint8)
        opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
        print("Applied morphological opening to remove small objects.")

        # Find contours in the processed binary image
        contours, _ = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print(f"Found {len(contours)} contours in the binary image.")

        # Analyze each contour to find parking spaces
        parking_spaces = []
        min_area = 500  # Minimum area for a contour to be considered a parking space
        for contour in contours:
            # Approximate the contour to a polygon
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Calculate the area of the contour
            area = cv2.contourArea(contour)
            print(f"Contour area: {area}")

            # If the area is too small, skip this contour
            if area < min_area:
                print("Contour area is too small. Skipping...")
                continue

            # If the polygon has four points and is nearly rectangular, it might be a parking space
            if len(approx) == 4:
                # Calculate the bounding rectangle around the contour
                x, y, w, h = cv2.boundingRect(approx)
                print(f"Bounding rectangle: x={x}, y={y}, w={w}, h={h}")

                # Calculate the aspect ratio of the bounding rectangle
                aspect_ratio = w / float(h)
                print(f"Aspect ratio: {aspect_ratio}")

                # If the aspect ratio is too far from 1 (square-like), it might not be a parking space
                if aspect_ratio < 0.5 or aspect_ratio > 2:
                    print("Aspect ratio is too far from 1. Skipping...")
                    continue

                # Add the potential parking space to the list
                parking_spaces.append({'x': x, 'y': y, 'width': w, 'height': h})
                print("Potential parking space added to the list.")

        print(f"Total potential parking spaces found: {len(parking_spaces)}")

        # Store the results in self.model.results
        self.model.results = {'parking_spaces': parking_spaces}


if __name__ == "__main__":
    app = Framework()
    app.root.mainloop()
    


