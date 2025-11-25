import sys
import os
# 1. Add project root to system path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game
# Use shared path helper
from utils.monte_carlo_helpers import get_plot_path 
import numpy as np
import matplotlib.pyplot as plt

def run_strategy_monte_carlo():
    """
    Runs a Monte Carlo simulation comparing Flat vs Martingale.
    """
    print("🎯 STRATEGY MONTE CARLO: Flat vs Martingale")
    print("=" * 60)
    
    # Configuration
    wheel_type = "european"
    num_players = 100
    num_spins = 1000
    START_BANKROLL = 1000
    
    print(f"Simulating {num_players} players, {num_spins} spins each...")
    print(f"Wheel: {wheel_type.upper()} | Bankroll: ${START_BANKROLL}")
    
    flat_results = []
    martingale_results = []
    
    for i in range(num_players):
        if (i+1) % 20 == 0: print(f"  Simulating player {i+1}/{num_players}...")
        
        # --- 1. Flat Betting Simulation ---
        wheel_f = RouletteWheel(wheel_type)
        
        # FIX: Explicit Configuration for new Game logic
        player_f = Player(strategy="flat", initial_bankroll=START_BANKROLL, base_bet=10)
        player_f.bet_type = "color"
        player_f.bet_value = "red"
        
        game_f = Game(wheel_f, player_f) # Infinite limit (Default)
        game_f.run_simulation(num_spins)
        flat_results.append(player_f.bankroll)
        
        # --- 2. Martingale Simulation ---
        wheel_m = RouletteWheel(wheel_type)
        
        # FIX: Explicit Configuration for new Game logic
        player_m = Player(strategy="martingale", initial_bankroll=START_BANKROLL, base_bet=10)
        player_m.bet_type = "color"
        player_m.bet_value = "red"
        
        game_m = Game(wheel_m, player_m) # Infinite limit (Default)
        game_m.run_simulation(num_spins)
        martingale_results.append(player_m.bankroll)

    # Statistics (Simple format)
    print("\n--- RESULTS ---")
    print(f"FLAT BETTING:")
    print(f"  • Average Final: ${np.mean(flat_results):.2f}")
    print(f"  • Std Dev: ${np.std(flat_results):.2f}")
    print(f"  • Max Win: ${max(flat_results):.2f}")
    print(f"  • Max Loss: ${min(flat_results):.2f}")
    
    print(f"\nMARTINGALE:")
    print(f"  • Average Final: ${np.mean(martingale_results):.2f}")
    print(f"  • Std Dev: ${np.std(martingale_results):.2f}")
    print(f"  • Max Win: ${max(martingale_results):.2f}")
    print(f"  • Max Loss: ${min(martingale_results):.2f}")

    # Plotting
    print("\nGenerating Histogram Comparison...")
    plt.figure(figsize=(12, 6))
    
    # Create bins based on all data
    all_data = flat_results + martingale_results
    bins = np.linspace(min(all_data), max(all_data), 50)
    
    plt.hist(flat_results, bins=bins, alpha=0.6, label='Flat Betting', color='blue', edgecolor='black')
    plt.hist(martingale_results, bins=bins, alpha=0.5, label='Martingale', color='red', edgecolor='black')
    
    plt.axvline(x=START_BANKROLL, color='green', linestyle='--', label='Start ($1000)')
    plt.title(f'Distribution of Outcomes: Flat vs Martingale\n({num_players} Players, {num_spins} Spins, European Wheel)')
    plt.xlabel('Final Bankroll ($)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # FIX: Use shared path helper
    current_folder = os.path.dirname(os.path.abspath(__file__))
    path = get_plot_path(current_folder, 'strategy_monte_carlo.png')
    
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.show()
    print(f"📊 Plot saved to {path}")

if __name__ == "__main__":
    run_strategy_monte_carlo()