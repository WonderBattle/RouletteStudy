import sys
import os
# 1. Add project root to system path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game
from utils.monte_carlo_helpers import (
    create_martingale_comparison, # The shared comparison helper
    get_plot_path
)
import numpy as np
import matplotlib.pyplot as plt

def run_simulation_batch(wheel_type, num_players, num_spins, table_limit, start_bankroll):
    """
    Helper to run a batch of Martingale sims for comparison.
    Returns the list of final bankrolls.
    """
    final_bankrolls = []
    print(f"  ... Simulating {wheel_type.upper()} Martingale...")
    
    for _ in range(num_players):
        wheel = RouletteWheel(wheel_type)
        
        # Configure Player
        player = Player(strategy="martingale", initial_bankroll=start_bankroll, base_bet=10)
        player.bet_type = "color"
        player.bet_value = "red"
        
        # Configure Game with Limit
        game = Game(wheel, player, table_limit=table_limit)
        
        game.run_simulation(num_spins)
        final_bankrolls.append(player.bankroll)
        
    return final_bankrolls

def run_martingale_comparison():
    num_players = 1000
    num_spins = 1000
    
    # --- CONFIGURATION ---
    TABLE_LIMIT = 1000
    START_BANKROLL = 1000
    
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    print(f"🎯 EXPERIMENT 4: Martingale Comparison (The Limits of Survival)")
    print("=" * 60)
    print(f"Comparing all wheels with Max Bet ${TABLE_LIMIT}")

    # --- Step 1: Run Simulations ---
    euro_results = run_simulation_batch("european", num_players, num_spins, TABLE_LIMIT, START_BANKROLL)
    amer_results = run_simulation_batch("american", num_players, num_spins, TABLE_LIMIT, START_BANKROLL)
    trip_results = run_simulation_batch("triple", num_players, num_spins, TABLE_LIMIT, START_BANKROLL)
    
    # --- Step 2: Print Survival Analytics ---
    print("\n" + "="*90)
    print(f"SUMMARY: MARTINGALE SURVIVAL (1000 Spins, Max Bet $1000)")
    print("-" * 90)
    print(f"{'METRIC':<20} | {'EUROPEAN':<15} | {'AMERICAN':<15} | {'TRIPLE':<15}")
    print("-" * 90)
    
    # Average Final Bankroll (Net Wealth)
    print(f"{'Avg End Bankroll':<20} | ${np.mean(euro_results):<14.0f} | ${np.mean(amer_results):<14.0f} | ${np.mean(trip_results):<14.0f}")
    
    # Winners (Survivors > Start)
    euro_wins = sum(1 for x in euro_results if x > START_BANKROLL)
    amer_wins = sum(1 for x in amer_results if x > START_BANKROLL)
    trip_wins = sum(1 for x in trip_results if x > START_BANKROLL)
    
    print(f"{'Survivors':<20} | {euro_wins:<15} | {amer_wins:<15} | {trip_wins:<15}")
    
    # Bankrupt (Lost everything <= 0)
    euro_crash = sum(1 for x in euro_results if x <= 0)
    amer_crash = sum(1 for x in amer_results if x <= 0)
    trip_crash = sum(1 for x in trip_results if x <= 0)
    
    print(f"{'Bankrupt (<=0)':<20} | {euro_crash:<15} | {amer_crash:<15} | {trip_crash:<15}")
    print("="*90)

    # --- Step 3: Generate Comparison Plot ---
    print("\nGenerating Comparison Plot...")
    
    # Use the helper function to overlay the 3 histograms
    plt = create_martingale_comparison(euro_results, amer_results, trip_results, num_players)
    
    save_path = get_plot_path(current_folder, "comparison_martingale_survival.png")
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"📊 Comparison plot saved to: {save_path}")

if __name__ == "__main__":
    run_martingale_comparison()