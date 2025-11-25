import sys
import os
# 1. Add project root to system path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game
# Import our plotting tools
from utils.monte_carlo_helpers import (
    create_bankroll_path_plot, 
    create_martingale_histogram, 
    get_plot_path
)
import numpy as np
import matplotlib.pyplot as plt

def run_martingale_simulation(wheel_type, num_players, num_spins, table_limit, start_bankroll):
    """
    Runs Martingale simulation using the Game class's built-in limit enforcement.
    """
    all_histories = []
    
    print(f"  ... Simulating {wheel_type.upper()} Martingale (Max Bet ${table_limit})...")
    
    for _ in range(num_players):
        wheel = RouletteWheel(wheel_type)
        
        # Configure Martingale Player
        player = Player(strategy="martingale", initial_bankroll=start_bankroll, base_bet=10)
        player.bet_type = "color"
        player.bet_value = "red"
        
        # *** CRITICAL: Pass the table_limit to the Game ***
        game = Game(wheel, player, table_limit=table_limit)
        
        game.run_simulation(num_spins)
        
        # Extract history for plotting
        player_path = [start_bankroll] + [step['bankroll'] for step in game.history]
        all_histories.append(player_path)
        
    return all_histories

def run_triple_martingale():
    wheel_type = "triple"
    num_players = 1000
    num_spins = 1000
    
    # --- CONFIGURATION ---
    START_BANKROLL = 1000  # Realistic Bankroll
    TABLE_LIMIT = 1000     # Standard Casino Limit ($10-$1000)
    
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    print(f"🎯 EXPERIMENT 4: Martingale with Limits - {wheel_type.upper()}")
    print("=" * 60)
    
    # --- Step 1: Run Simulation ---
    histories = run_martingale_simulation(wheel_type, num_players, num_spins, TABLE_LIMIT, START_BANKROLL)
    
    # --- Step 2: Generate Path Plot (The "Elevator Drops") ---
    print("\nGenerating Path Plot...")
    plt1 = create_bankroll_path_plot(histories, "color", wheel_type, num_spins, strategy_label="Martingale Strategy")
    
    path_plot = get_plot_path(current_folder, "triple_martingale_paths.png")
    plt1.savefig(path_plot, dpi=300, bbox_inches='tight')
    plt1.show()
    print(f"📊 Path plot saved to: {path_plot}")
    
    # --- Step 3: Generate Histogram (Survivors vs. Victims) ---
    print("Generating Histogram...")
    final_bankrolls = [h[-1] for h in histories]
    
    plt2 = create_martingale_histogram(final_bankrolls, num_players, num_spins, wheel_type)
    
    path_hist = get_plot_path(current_folder, "triple_martingale_hist.png")
    plt2.savefig(path_hist, dpi=300, bbox_inches='tight')
    plt2.show()
    print(f"📊 Histogram saved to: {path_hist}")
    
    # --- Step 4: Analytics ---
    print(f"\n--- ANALYTICS ({wheel_type.title()}) ---")
    print(f"Table Limit: ${TABLE_LIMIT}")
    print(f"Avg Final Bankroll: ${np.mean(final_bankrolls):.2f}")
    
    # Survivors vs. Bankrupt
    winners = sum(1 for x in final_bankrolls if x > START_BANKROLL)
    bankrupt = sum(1 for x in final_bankrolls if x <= 0)
    bleeding = sum(1 for x in final_bankrolls if 0 < x <= START_BANKROLL)
    
    print(f"Profitable Players: {winners}/{num_players} ({winners/num_players*100:.1f}%)")
    print(f"Bankrupt Players (<=0): {bankrupt}/{num_players} ({bankrupt/num_players*100:.1f}%)")
    print(f"Losing but Surviving: {bleeding}/{num_players} ({bleeding/num_players*100:.1f}%)")

    # Mathematical Verification
    # Triple House Edge is 7.69% (0.0769)
    expected_loss = (num_spins * 10) * 0.0769
    print(f"\nReference (If Flat Betting): ${START_BANKROLL - expected_loss:.2f}")
    print("Comparison: Martingale players lost significantly more money due to huge wagers.")

if __name__ == "__main__":
    run_triple_martingale()