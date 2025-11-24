import random

class RouletteWheel:
    def __init__(self, wheel_type="european"):
        # Store the type of wheel (european, american, triple)
        self.wheel_type = wheel_type
        # Initialize the numbers based on wheel type
        self.numbers = self._initialize_numbers()
        
    def _initialize_numbers(self):
        # European roulette: numbers 0-36 (37 total)
        if self.wheel_type == "european":
            return list(range(0, 37))  # Creates [0, 1, 2, ..., 36]
        # American roulette: 0, 00, and 1-36 (38 total)  
        elif self.wheel_type == "american":
            return ['0', '00'] + list(range(1, 37))
        # Triple zero roulette: 0, 00, 000, and 1-36 (39 total)
        elif self.wheel_type == "triple":
            return ['0', '00', '000'] + list(range(1, 37))
        # If invalid wheel type provided, raise an error
        else:
            raise ValueError("Invalid wheel type")
    
    def spin(self):
        # Return a random number from the wheel's numbers
        return random.choice(self.numbers)
    
    def get_total_pockets(self):
        # Return the total number of pockets on this wheel
        return len(self.numbers)