import sys
import os
# Ensure we can find the components folder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game
# Import all necessary plotting functions from our shared utility
from utils.monte_carlo_helpers import (
    create_distribution_comparison, 
    create_bankroll_path_plot, 
    get_plot_path
)
import numpy as np
import matplotlib.pyplot as plt

def run_simulation_paths(wheel_type, bet_type, num_players, num_spins):
    """
    Runs simulation and returns the FULL history for every player.
    This history is needed for the Path Plots (full trajectory) 
    and the Histogram (final value).
    """
    all_histories = []
    
    print(f"  ... Simulating {bet_type} bets ({num_players} players)...")
    
    for _ in range(num_players):
        wheel = RouletteWheel(wheel_type)
        player = Player(strategy="flat", initial_bankroll=1000, base_bet=10)
        player.bet_type = bet_type 
        
        # Configure specific bet
        if bet_type == "color":
            player.bet_value = "red"  # Payout 1:1 [cite: 172]
        else:
            player.bet_value = 17     # Payout 35:1 [cite: 191]
            
        game = Game(wheel, player)
        game.run_simulation(num_spins)
        
        # Extract the bankroll at every step for this specific player
        # We start with 1000, then append the result of every spin
        player_path = [1000] + [step['bankroll'] for step in game.history]
        all_histories.append(player_path)
        
    return all_histories

def run_triple_experiment():
    wheel_type = "triple"
    num_players = 1000  # High sample size for good histograms
    num_spins = 1000    # Duration of play
    
    print(f"🎯 EXPERIMENT 3: Triple Zero Roulette Monte Carlo Analysis")
    print("=" * 60)
    
    # --- STEP 1: Run Simulations ---
    # We run the simulations first to gather all data
    print("\n[1/4] Running Simulations...")
    color_histories = run_simulation_paths(wheel_type, "color", num_players, num_spins)
    number_histories = run_simulation_paths(wheel_type, "number", num_players, num_spins)
    
    # Get the folder where THIS script is located (for saving plots)
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    # --- STEP 2: Generate Path Plots (The "Journey") ---
    print("\n[2/4] Generating Path Plots...")
    
    # Plot 1: Color Bet Paths
    plt1 = create_bankroll_path_plot(color_histories, "color", wheel_type, num_spins)
    
    # Save using the shared utility + current folder
    path_color = get_plot_path(current_folder, "triple_paths_color.png")
    plt1.savefig(path_color, dpi=300, bbox_inches='tight')
    plt1.show() # Display the plot
    print(f"📊 Color path plot saved to: {path_color}")

    # Plot 2: Number Bet Paths
    plt2 = create_bankroll_path_plot(number_histories, "number", wheel_type, num_spins)
    path_number = get_plot_path(current_folder, "triple_paths_number.png")
    plt2.savefig(path_number, dpi=300, bbox_inches='tight')
    plt2.show() # Display the plot
    print(f"📊 Number path plot saved to: {path_number}")
    
    # --- STEP 3: Display Detailed Analytics ---
    # We extract the final bankroll (the last item in the history list) for stats
    color_finals = [h[-1] for h in color_histories]
    number_finals = [h[-1] for h in number_histories]
    
    print(f"\n[3/4] --- ANALYTICS RESULTS ({num_players} Players) ---")
    
    # Stats for Color Bets
    print(f"\nCOLOR BETS (Low Volatility):")
    print(f"  • Average Bankroll: ${np.mean(color_finals):.2f}")
    print(f"  • Standard Deviation: ${np.std(color_finals):.2f} (Low Risk)")
    print(f"  • Best Winner: ${max(color_finals):,}")
    print(f"  • Worst Loser: ${min(color_finals):,}")
    print(f"  • Players Profitable: {sum(1 for x in color_finals if x > 1000)}/{num_players}")
    
    # Stats for Number Bets
    print(f"\nNUMBER BETS (High Volatility):")
    print(f"  • Average Bankroll: ${np.mean(number_finals):.2f}")
    print(f"  • Standard Deviation: ${np.std(number_finals):.2f} (High Risk)")
    print(f"  • Best Winner: ${max(number_finals):,}")
    print(f"  • Worst Loser: ${min(number_finals):,}")
    print(f"  • Players Profitable: {sum(1 for x in number_finals if x > 1000)}/{num_players}")

    # Mathematical Verification
    total_bet = num_spins * 10
    house_edge = 0.0769 # 7.69% for Triple Zero Roulette 
    expected_loss = total_bet * house_edge
    expected_final = 1000 - expected_loss
    
    print(f"\n--- MATHEMATICAL VERIFICATION ---")
    print(f"Theoretical Expected Final Bankroll: ${expected_final:.2f}")
    print(f"Observation: Both averages should be close to ${expected_final:.2f}, proving the House Edge is constant.")

    # --- STEP 4: Generate Comparison Histogram (The "Result") ---
    print("\n[4/4] Generating Comparison Histogram...")
    
    # Plot 3: Distribution Comparison
    plt3 = create_distribution_comparison(color_finals, number_finals, num_players, num_spins, wheel_type)
    path_hist = get_plot_path(current_folder, "triple_histogram_comparison.png")
    plt3.savefig(path_hist, dpi=300, bbox_inches='tight')
    plt3.show() 
    print(f"📊 Comparison histogram saved to: {path_hist}")

if __name__ == "__main__":
    run_triple_experiment()