import sys
import os
# 1. Add the project root to the system path so we can import our components
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game
# Import the plotting function for comparing 3 wheels and the path helper
from utils.monte_carlo_helpers import create_three_wheel_comparison, get_plot_path
import numpy as np
import matplotlib.pyplot as plt

def run_color_simulation(wheel_type, num_players, num_spins):
    """
    Runs a batch of simulations specifically for COLOR bets on a specific wheel.
    """
    final_bankrolls = []
    print(f"  ... Simulating {wheel_type.upper()} (Color Bets)...")
    
    for _ in range(num_players):
        wheel = RouletteWheel(wheel_type)
        # Strategy: Flat betting $10 on Red
        player = Player(strategy="flat", initial_bankroll=1000, base_bet=10)
        player.bet_type = "color"
        player.bet_value = "red" # Payout 1:1
        
        game = Game(wheel, player)
        game.run_simulation(num_spins)
        final_bankrolls.append(player.bankroll)
        
    return final_bankrolls

def run_color_comparison():
    """
    Main execution for the Color Bet Comparison Experiment.
    """
    num_players = 1000
    num_spins = 1000
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    print(f"🎯 EXPERIMENT 3A: Comparison of COLOR Bets (Low Variance)")
    print(f"Comparing: European vs American vs Triple Zero")
    print("=" * 60)

    # --- Step 1: Run Simulations for all 3 wheels ---
    euro_results = run_color_simulation("european", num_players, num_spins)
    amer_results = run_color_simulation("american", num_players, num_spins)
    trip_results = run_color_simulation("triple", num_players, num_spins)
    
    # --- Step 2: Print Comparative Analytics Table ---
    print("\n" + "="*80)
    print(f"SUMMARY: COLOR BETS (Starting Bankroll: $1000)")
    print("-" * 80)
    print(f"{'METRIC':<20} | {'EUROPEAN':<15} | {'AMERICAN':<15} | {'TRIPLE':<15}")
    print("-" * 80)
    
    # Average Final Bankroll (Shows the House Edge 'Drift')
    print(f"{'Avg End Bankroll':<20} | ${np.mean(euro_results):<14.2f} | ${np.mean(amer_results):<14.2f} | ${np.mean(trip_results):<14.2f}")
    
    # House Edge Verification
    print(f"{'Theoretical Edge':<20} | {'2.70%':<15} | {'5.26%':<15} | {'7.69%':<15}")
    
    # Winners (Survivors)
    euro_wins = sum(1 for x in euro_results if x > 1000)
    amer_wins = sum(1 for x in amer_results if x > 1000)
    trip_wins = sum(1 for x in trip_results if x > 1000)
    
    print(f"{'Profitable Players':<20} | {euro_wins:<15} | {amer_wins:<15} | {trip_wins:<15}")
    print(f"{'Win Probability':<20} | {euro_wins/num_players*100:<14.1f}% | {amer_wins/num_players*100:<14.1f}% | {trip_wins/num_players*100:<14.1f}%")
    print("="*80)

    # --- Step 3: Generate and Save the Comparison Plot ---
    print("\nGenerating Color Comparison Plot...")
    
    # Uses the shared helper to overlay the 3 histograms
    plt = create_three_wheel_comparison(euro_results, amer_results, trip_results, num_players, num_spins, bet_type="Color")
    
    # Save to the 'plots' subfolder
    save_path = get_plot_path(current_folder, "comparison_all_wheels_color.png")
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"📊 Color comparison plot saved to: {save_path}")

if __name__ == "__main__":
    run_color_comparison()