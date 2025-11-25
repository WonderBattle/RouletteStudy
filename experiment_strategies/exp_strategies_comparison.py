import sys
import os
# 1. Add project root to system path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game
# 2. Import the helper we just added
from utils.strategy_helpers import create_strategy_comparison_bar_plot
from utils.monte_carlo_helpers import get_plot_path 
import matplotlib.pyplot as plt

def run_all_strategy_comparison():
    """
    Compares Flat vs Martingale across all 3 wheel types.
    """
    print("🎯 EXPERIMENT 2: Multi-Wheel Strategy Comparison")
    print("=" * 65)
    
    wheel_types = ["european", "american", "triple"]
    START_BANKROLL = 1000
    num_spins = 5000
    
    all_results = {}
    
    for wheel_type in wheel_types:
        print(f"Simulating {wheel_type.upper()}...")
        
        wheel_flat = RouletteWheel(wheel_type)
        wheel_mart = RouletteWheel(wheel_type)
        
        # --- FIX: Explicit Player Configuration ---
        flat_player = Player(strategy="flat", initial_bankroll=START_BANKROLL, base_bet=10)
        flat_player.bet_type = "color"
        flat_player.bet_value = "red"
        
        mart_player = Player(strategy="martingale", initial_bankroll=START_BANKROLL, base_bet=10)
        mart_player.bet_type = "color"
        mart_player.bet_value = "red"
        
        game_flat = Game(wheel_flat, flat_player)
        game_mart = Game(wheel_mart, mart_player)
        
        # Run simulation (Game allows debt, so it runs fully)
        game_flat.run_simulation(num_spins)
        game_mart.run_simulation(num_spins)
        
        # Record results
        mart_bets = [s['bet_amount'] for s in game_mart.history]
        max_bet = max(mart_bets) if mart_bets else 10
        
        all_results[wheel_type] = {
            'flat_final': flat_player.bankroll,
            'martingale_final': mart_player.bankroll,
            'flat_loss': START_BANKROLL - flat_player.bankroll,
            'martingale_loss': START_BANKROLL - mart_player.bankroll,
            'martingale_max_bet': max_bet
        }

    # Print Summary Table
    print("\n" + "="*90)
    print(f"{'Roulette':<12} | {'Strategy':<12} | {'Final ($)':<12} | {'Loss ($)':<12} | {'Max Bet ($)':<12}")
    print("-" * 90)
    
    for wt in wheel_types:
        res = all_results[wt]
        print(f"{wt.title():<12} | Flat         | {res['flat_final']:<12,} | {res['flat_loss']:<12,} | 10")
        print(f"{'':<12} | Martingale   | {res['martingale_final']:<12,} | {res['martingale_loss']:<12,} | {res['martingale_max_bet']:,}")
        print("-" * 90)

    # Plot using the shared helper
    print("\nGenerating Bar Chart Comparison...")
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    fig = create_strategy_comparison_bar_plot(all_results)
    
    path = get_plot_path(current_folder, 'strategy_comparison_all_types.png')
    fig.savefig(path, dpi=300, bbox_inches='tight')
    plt.show()
    print(f"📊 Saved to {path}")

if __name__ == "__main__":
    run_all_strategy_comparison()