import sys
import os
sys.path.insert(0, '/home/elenacg/ADA511/Project/roulette_project')

from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game
import matplotlib.pyplot as plt
import numpy as np

def get_plot_path(filename):
    """Get path for saving plots in experiment's plots folder"""
    # Get the directory where THIS script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(current_dir, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    return os.path.join(plots_dir, filename)

def run_all_strategy_comparison():
    """
    EXPERIMENT 2: Strategy Comparison Across All Roulette Types
    Compare how strategies perform differently across European, American, and Triple Zero roulette
    """
    print("🎯 EXPERIMENT 2: Strategy Comparison - ALL Roulette Types")
    print("=" * 70)
    
    wheel_types = ["european", "american", "triple"]
    num_spins = 3000  # Fewer spins for faster execution
    
    # Store results for all combinations
    all_results = {}
    
    for wheel_type in wheel_types:
        print(f"\n--- Testing {wheel_type.upper()} Roulette ---")
        
        # Create setups for both strategies
        wheel_flat = RouletteWheel(wheel_type)
        wheel_martingale = RouletteWheel(wheel_type)
        
        flat_player = Player(strategy="flat", initial_bankroll=1000, base_bet=10)
        martingale_player = Player(strategy="martingale", initial_bankroll=1000, base_bet=10)
        
        game_flat = Game(wheel_flat, flat_player)
        game_martingale = Game(wheel_martingale, martingale_player)
        
        # Run simulations
        print(f"Running {num_spins} spins...")
        game_flat.run_simulation(num_spins)
        game_martingale.run_simulation(num_spins)
        
        # Store results
        all_results[wheel_type] = {
            'flat_final': flat_player.bankroll,
            'martingale_final': martingale_player.bankroll,
            'flat_loss': 1000 - flat_player.bankroll,
            'martingale_loss': 1000 - martingale_player.bankroll,
            'martingale_max_bet': max([spin['bet_amount'] for spin in game_martingale.history])
        }
        
        # Show immediate results
        print(f"  Flat betting: ${flat_player.bankroll:,} (Loss: ${all_results[wheel_type]['flat_loss']:,})")
        print(f"  Martingale: ${martingale_player.bankroll:,} (Loss: ${all_results[wheel_type]['martingale_loss']:,})")
        print(f"  Martingale max bet: ${all_results[wheel_type]['martingale_max_bet']:,}")
    
    # Create comprehensive comparison
    create_comprehensive_comparison_plot(all_results, num_spins)
    
    # Print summary table
    print_summary_table(all_results, num_spins)

def create_comprehensive_comparison_plot(all_results, num_spins):
    """
    Create a plot comparing strategy performance across all wheel types
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    wheel_types = list(all_results.keys())
    colors = {'european': 'blue', 'american': 'orange', 'triple': 'green'}
    
    # Plot 1: Final bankrolls
    flat_finals = [all_results[wt]['flat_final'] for wt in wheel_types]
    martingale_finals = [all_results[wt]['martingale_final'] for wt in wheel_types]
    
    x_pos = np.arange(len(wheel_types))
    width = 0.35
    
    ax1.bar(x_pos - width/2, flat_finals, width, label='Flat Betting', alpha=0.8)
    ax1.bar(x_pos + width/2, martingale_finals, width, label='Martingale', alpha=0.8)
    
    ax1.axhline(y=1000, color='red', linestyle='--', alpha=0.7, label='Starting Bankroll')
    ax1.set_xlabel('Roulette Type')
    ax1.set_ylabel('Final Bankroll ($)')
    ax1.set_title('Final Bankroll by Strategy and Roulette Type')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels([wt.upper() for wt in wheel_types])
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Loss percentages
    flat_loss_pct = [(all_results[wt]['flat_loss'] / 1000) * 100 for wt in wheel_types]
    martingale_loss_pct = [(all_results[wt]['martingale_loss'] / 1000) * 100 for wt in wheel_types]
    
    ax2.bar(x_pos - width/2, flat_loss_pct, width, label='Flat Betting', alpha=0.8)
    ax2.bar(x_pos + width/2, martingale_loss_pct, width, label='Martingale', alpha=0.8)
    
    ax2.set_xlabel('Roulette Type')
    ax2.set_ylabel('Loss Percentage (%)')
    ax2.set_title('Loss Percentage by Strategy and Roulette Type')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([wt.upper() for wt in wheel_types])
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    original_path = get_plot_path('strategy_comparison_all_types.png')
    plt.savefig(original_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\n📊 Comprehensive comparison plot saved as 'strategy_comparison_all_types.png'")

def print_summary_table(all_results, num_spins):
    """
    Print a formatted summary table of all results
    """
    print(f"\n{'='*80}")
    print(f"SUMMARY TABLE: Strategy Performance Across {num_spins} Spins")
    print(f"{'='*80}")
    print(f"{'Roulette Type':<12} {'Strategy':<12} {'Final Bankroll':<15} {'Total Loss':<12} {'Loss %':<8} {'Max Bet':<10}")
    print(f"{'-'*80}")
    
    for wheel_type in all_results.keys():
        results = all_results[wheel_type]
        print(f"{wheel_type.upper():<12} {'Flat':<12} ${results['flat_final']:<14,} ${results['flat_loss']:<11,} {results['flat_loss']/10:.1f}%{'':<9}")
        print(f"{'':<12} {'Martingale':<12} ${results['martingale_final']:<14,} ${results['martingale_loss']:<11,} {results['martingale_loss']/10:.1f}%{'':<7}${results['martingale_max_bet']:,}")
        print(f"{'-'*80}")

if __name__ == "__main__":
    run_all_strategy_comparison()