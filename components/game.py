class Game:
    def __init__(self, wheel, player):
        # Store the wheel and player objects
        self.wheel = wheel
        self.player = player
        # List to store history of all spins and results
        self.history = []
        # Define which numbers are red on the roulette wheel
        self.red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    
    def determine_win(self, spin_result, bet_type, bet_value):
        # Handle color bets (red/black)
        if bet_type == "color":
            # Check for red win
            if bet_value == "red" and spin_result in self.red_numbers:
                return True
            # Check for black win (not red and not zero)
            elif bet_value == "black" and spin_result not in self.red_numbers and spin_result != 0:
                return True
            # Otherwise lose (including zeros)
            return False
        # Handle straight-up number bets
        elif bet_type == "number":
            # Win only if the specific number matches
            return spin_result == bet_value
        # Default case for unknown bet types
        return False
    
    def run_spin(self):
        # Player decides how much to bet
        bet_amount = self.player.place_bet()
        # Wheel generates a random result
        spin_result = self.wheel.spin()
        # Determine if the player won based on their bet
        won = self.determine_win(spin_result, self.player.bet_type, self.player.bet_value)
        
        # Calculate payout amount
        if won:
            if self.player.bet_type == "color":
                payout = bet_amount  # 1:1 payout for color bets
            else:  # number bet
                payout = bet_amount * 35  # 35:1 payout for straight-up bets
        else:
            payout = -bet_amount  # Player loses their bet
        
        # Update player's bankroll and strategy state
        self.player.process_result(won, payout)
        
        # Create a record of this spin for history
        spin_record = {
            'spin_number': len(self.history) + 1,
            'spin_result': spin_result,
            'bet_amount': bet_amount,
            'bet_type': self.player.bet_type,
            'bet_value': self.player.bet_value,
            'result': 'win' if won else 'lose',
            'payout': payout,
            'bankroll': self.player.bankroll
        }
        # Add this spin to history
        self.history.append(spin_record)
        
        return spin_record
    
    def run_simulation(self, num_spins):
        # Run the specified number of spins
        for _ in range(num_spins):
            self.run_spin()
        # Return the complete history
        return self.history