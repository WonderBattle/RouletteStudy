class Game:
    def __init__(self, wheel, player, table_limit=float('inf')):
        # Store the wheel and player objects
        self.wheel = wheel
        self.player = player
        
        # Store the table limit
        self.table_limit = table_limit
        
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
            elif bet_value == "black" and spin_result not in self.red_numbers and spin_result != 0 and spin_result != '0' and spin_result != '00' and spin_result != '000':
                return True
            # Otherwise lose (including zeros)
            return False
            
        # Handle straight-up number bets
        elif bet_type == "number":
            # Win only if the specific number matches
            # Ensure types match (int vs string issues)
            return str(spin_result) == str(bet_value)
            
        # Default case for unknown bet types
        return False

    def run_spin(self):
        # 1. Player decides how much they WANT to bet
        intended_bet = self.player.place_bet()
        
        # 2. The Game enforces the Table Limit
        actual_bet = min(intended_bet, self.table_limit)
        
        # 3. Wheel spins
        spin_result = self.wheel.spin()
        
        # 4. Determine win/loss
        won = self.determine_win(spin_result, self.player.bet_type, self.player.bet_value)
        
        # 5. Calculate payout
        if won:
            if self.player.bet_type == "color":
                payout = actual_bet  # 1:1 payout
            else:
                payout = actual_bet * 35  # 35:1 payout
        else:
            payout = -actual_bet  # Lose the bet
            
        # 6. Update player
        self.player.process_result(won, payout)
        
        # 7. Record history
        spin_record = {
            'spin_number': len(self.history) + 1,
            'spin_result': spin_result,
            'bet_amount': actual_bet,
            'intended_bet': intended_bet,
            'bet_type': self.player.bet_type,
            'bet_value': self.player.bet_value,
            'result': 'win' if won else 'lose',
            'payout': payout,
            'bankroll': self.player.bankroll
        }
        
        self.history.append(spin_record)
        return spin_record

    def run_simulation(self, num_spins):
        # Run the specified number of spins
        for _ in range(num_spins):
            # --- FIX: REMOVED THE BANKRUPTCY CHECK ---
            # We allow the simulation to continue even if bankroll is negative.
            # This lets us see the full mathematical trend and prevents plotting errors.
            self.run_spin()
            
        return self.history