import sys
import os
# 1. Add project root to system path to find 'components'
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game

def run_house_edge_experiment():
    """
    EXPERIMENT 1: Verify House Edge (Basic Text Output)
    Tests if our simulation matches theoretical math using a long run of spins.
    """
    print("🎯 EXPERIMENT 1: House Edge Verification")
    print("=" * 50)
    
    wheel_types = ["european", "american", "triple"]
    
    # We can use a realistic bankroll because the Game allows debt!
    START_BANKROLL = 10000
    
    for wheel_type in wheel_types:
        print(f"\n--- Testing {wheel_type.upper()} Roulette ---")
        
        wheel = RouletteWheel(wheel_type)
        
        # Configure Player
        player = Player(strategy="flat", initial_bankroll=START_BANKROLL, base_bet=10)
        
        # We must explicitly tell the new Game logic what we are betting on.
        player.bet_type = "color"
        player.bet_value = "red"
        
        game = Game(wheel, player)
        
        # Run 100,000 spins to let the Law of Large Numbers work
        # Since 'Game' allows debt, this loop will finish completely.
        num_spins = 100000
        print(f"Running {num_spins:,} spins...")
        
        game.run_simulation(num_spins)
        
        # Calculate Results
        total_wagered = num_spins * player.base_bet
        final_bankroll = player.bankroll
        
        # Calculate Total Loss (Start - End)
        # This works even if final_bankroll is negative!
        total_loss = START_BANKROLL - final_bankroll
        
        # Calculate House Edge: (Loss / Total Wagered) * 100
        experimental_edge = (total_loss / total_wagered) * 100
        
        # Theoretical values for comparison
        theoretical_edges = {
            "european": 2.70,
            "american": 5.26, 
            "triple": 7.69
        }
        theoretical_edge = theoretical_edges[wheel_type]
        
        error = abs(theoretical_edge - experimental_edge)
        
        print(f"Results for {wheel_type.upper()} roulette:")
        print(f"  • Total amount wagered: ${total_wagered:,}")
        print(f"  • Final bankroll: ${final_bankroll:,}")
        print(f"  • Total loss: ${total_loss:,}")
        print(f"  • Experimental house edge: {experimental_edge:.2f}%")
        print(f"  • Theoretical house edge: {theoretical_edge:.2f}%")
        print(f"  • Error: {error:.2f}%")
        
        if error < 0.5:
            print("  ✅ PASS: Experimental results match theory!")
        else:
            print("  ⚠️  WARNING: Results differ from theory")

if __name__ == "__main__":
    run_house_edge_experiment()