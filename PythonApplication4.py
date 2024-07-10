import math

class ParkingLotCalculator:
    def __init__(self, length, width, shape):
        self.length = length
        self.width = width
        self.shape = shape
        self.car_size = (4.5, 2.0)
        self.truck_size = (6.0, 2.5)

    def rectangle_area(self):
        return self.length * self.width

    def ellipse_area(self):
        return math.pi * (self.length / 2) * (self.width / 2)
    
    def cars_fit(self):
        if self.shape == 'rectangle':
            area = self.rectangle_area()
        else:
            area = self.ellipse_area()
        car_area = self.car_size[0] * self.car_size[1]
        return area // car_area

    def trucks_fit(self):
        if self.shape == 'rectangle':
            area = self.rectangle_area()
        else:
            area = self.ellipse_area()
        truck_area = self.truck_size[0] * self.truck_size[1]
        return area // truck_area

    def staggered_parking(self, vehicle_type='car'):
        if self.shape == 'rectangle':
            area = self.rectangle_area()
        else:
            area = self.ellipse_area()

        if vehicle_type == 'car':
            vehicle_length, vehicle_width = self.car_size
        elif vehicle_type == 'truck':
            vehicle_length, vehicle_width = self.truck_size

        # For simplicity, let's assume vehicles are staggered at a 45 degree angle
        staggered_vehicle_length = vehicle_length * 0.7071  # cos(45 degrees)
        staggered_vehicle_width = vehicle_width * 1.4142  # sqrt(2) because of the staggered arrangement
        staggered_vehicle_area = staggered_vehicle_length * staggered_vehicle_width
        return area // staggered_vehicle_area
    

    # Diagonal parking algorithm
    def diagonal_parking(self, vehicle_type='car'):
        if self.shape == 'rectangle':
            area = self.rectangle_area()
        else:
            area = self.ellipse_area()

        if vehicle_type == 'car':
            vehicle_length, vehicle_width = self.car_size
        elif vehicle_type == 'truck':
            vehicle_length, vehicle_width = self.truck_size

        diagonal_area = ((vehicle_length**2 + vehicle_width**2)**0.5) * vehicle_width
        return area // diagonal_area

    # Compact car parking algorithm
    def compact_cars_fit(self):
        compact_car_size = (4, 1.8)  # Assuming compact cars are smaller
        if self.shape == 'rectangle':
            area = self.rectangle_area()
        else:
            area = self.ellipse_area()
        compact_car_area = compact_car_size[0] * compact_car_size[1]
        return area // compact_car_area

    # Efficient truck parking algorithm
    def efficient_trucks_fit(self):
        if self.shape == 'rectangle':
            area = self.rectangle_area()
        else:
            area = self.ellipse_area()
        
        # Assume efficient layout reduces wasted space by 20%
        adjusted_truck_area = self.truck_size[0] * self.truck_size[1] * 0.8
        return area // adjusted_truck_area

def main():
    print("Welcome to the Enhanced Parking Lot Calculator!")
    length = float(input("Enter the length of the parking lot: "))
    width = float(input("Enter the width of the parking lot: "))
    shape = input("Is the parking lot a rectangle? Press Y for yes, any other key for ellipse: ").lower()
    
    if shape == 'y':
        shape = 'rectangle'
    else:
        shape = 'ellipse'

    calculator = ParkingLotCalculator(length, width, shape)
    
    cars = int(input("Guess how many cars can fit: "))
    trucks = int(input("Guess how many trucks can fit: "))
    
    cars_fit = calculator.cars_fit()
    trucks_fit = calculator.trucks_fit()
    
    diagonal_cars_fit = calculator.diagonal_parking('car')
    diagonal_trucks_fit = calculator.diagonal_parking('truck')
    
    compact_cars_fit = calculator.compact_cars_fit()
    
    efficient_trucks_fit = calculator.efficient_trucks_fit()
    
    # Elaborating on the results for better understanding and user experience
    print(f"Based on the dimensions provided and assuming an optimal arrangement,")
    print(f"the actual number of standard-sized cars that can fit in your parking lot is: {cars_fit}.")
    print(f"For trucks, taking into account their larger size, the number that could potentially fit is: {trucks_fit}.")

    # Explaining diagonal parking benefits
    print("\nDiagonal parking can often increase the number of vehicles that can be accommodated.")
    print(f"With diagonal parking, the number of cars that can fit increases to: {diagonal_cars_fit}.")
    print(f"Similarly, the number of trucks that can be parked diagonally increases to: {diagonal_trucks_fit}.")
    print("This increase is due to the more efficient use of space when vehicles are parked at an angle.")

    # Highlighting compact car advantages
    print("\nFor compact cars, which are smaller than standard cars,")
    print(f"the parking lot can accommodate up to: {compact_cars_fit} vehicles.")
    print("Compact cars benefit from their smaller size, allowing more vehicles to be parked within the same area.")

    # Discussing efficient truck parking strategies
    print("\nEfficient layouts for trucks can significantly improve the utilization of space.")
    print(f"With an optimized layout reducing wasted space by 20%, the number of trucks that can fit increases to: {efficient_trucks_fit}.")
    print("This improvement comes from better planning and minimizing the unused areas between parked trucks.")

    # Comparing user guesses with calculated values
    print("\nComparing your guesses with the calculated values:")
    if cars != cars_fit:
        print(f"Your guess for the number of cars was off by {abs(cars - cars_fit)}.")
    else:
        print("Your guess for the number of cars was spot on!")

    if trucks != trucks_fit:
        print(f"Your guess for the number of trucks was off by {abs(trucks - trucks_fit)}.")
    else:
        print("Your guess for the number of trucks was spot on!")

if __name__ == "__main__":
    main()



