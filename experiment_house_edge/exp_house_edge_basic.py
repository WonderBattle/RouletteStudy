import sys
import os
sys.path.insert(0, '/home/elenacg/ADA511/Project/roulette_project')

from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game

def run_house_edge_experiment():
    """
    EXPERIMENT 1: Verify House Edge
    This experiment tests if our simulation matches theoretical house edges:
    - European: 2.70% theoretical edge
    - American: 5.26% theoretical edge  
    - Triple Zero: 7.69% theoretical edge
    """
    print("🎯 EXPERIMENT 1: House Edge Verification")
    print("=" * 50)
    
    # Test all three wheel types
    wheel_types = ["european", "american", "triple"]
    
    for wheel_type in wheel_types:
        print(f"\n--- Testing {wheel_type.upper()} Roulette ---")
        
        # Create wheel, player, and game for this test
        wheel = RouletteWheel(wheel_type)
        player = Player(strategy="flat", initial_bankroll=10000)  # Start with more money for accuracy
        game = Game(wheel, player)
        
        # Run a large number of spins for statistical significance
        num_spins = 100000
        print(f"Running {num_spins:,} spins...")
        
        # Run the simulation
        game.run_simulation(num_spins)
        
        # Calculate results
        total_wagered = num_spins * player.base_bet
        final_bankroll = player.bankroll
        total_loss = 10000 - final_bankroll  # Since we started with 10,000
        
        # Calculate experimental house edge
        experimental_edge = (total_loss / total_wagered) * 100
        
        # Theoretical house edges (from our mathematical calculations)
        theoretical_edges = {
            "european": 2.70,
            "american": 5.26, 
            "triple": 7.69
        }
        theoretical_edge = theoretical_edges[wheel_type]
        
        # Calculate error (difference between theoretical and experimental)
        error = abs(theoretical_edge - experimental_edge)
        
        # Display results
        print(f"Results for {wheel_type.upper()} roulette:")
        print(f"  • Total amount wagered: ${total_wagered:,}")
        print(f"  • Final bankroll: ${final_bankroll:,}")
        print(f"  • Total loss: ${total_loss:,}")
        print(f"  • Experimental house edge: {experimental_edge:.2f}%")
        print(f"  • Theoretical house edge: {theoretical_edge:.2f}%")
        print(f"  • Error: {error:.2f}%")
        
        # Check if results are reasonable (within 0.2% of theoretical)
        if error < 0.5:
            print("  ✅ PASS: Experimental results match theory!")
        else:
            print("  ⚠️  WARNING: Results differ from theory")

if __name__ == "__main__":
    run_house_edge_experiment()