class Player:
    def __init__(self, initial_bankroll=1000, strategy="flat", base_bet=10):
        # Current money the player has
        self.bankroll = initial_bankroll
        # Betting strategy: "flat" or "martingale" 
        self.strategy = strategy
        # The base amount to bet (for flat betting or martingale starting point)
        self.base_bet = base_bet
        # Current bet amount (changes for martingale strategy)
        self.current_bet = base_bet
        # Track how many losses in a row (for martingale)
        self.consecutive_losses = 0
        # What type of bet: "color" or "number"
        self.bet_type = "color"
        # Specific bet value: "red", "black", or a number like 17
        self.bet_value = "red"
    
    def place_bet(self):
        """Determine bet amount based on strategy"""
        # Flat betting: always bet the same amount
        if self.strategy == "flat":
            return self.base_bet
        # Martingale: bet amount depends on previous results
        elif self.strategy == "martingale":
            return self.current_bet
        # Default to flat betting for any unknown strategy
        else:
            return self.base_bet
    
    def process_result(self, won, payout):
        """Update bankroll and strategy state"""
        # Update the player's money (add winnings or subtract losses)
        self.bankroll += payout
        
        # If using martingale strategy, update betting state
        if self.strategy == "martingale":
            if won:
                # Reset to base bet after a win
                self.current_bet = self.base_bet
                self.consecutive_losses = 0
            else:
                # Increase bet after a loss (double each time)
                self.consecutive_losses += 1
                self.current_bet = self.base_bet * (2 ** self.consecutive_losses)