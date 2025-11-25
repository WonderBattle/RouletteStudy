import sys
import os
sys.path.insert(0, '/home/elenacg/ADA511/Project/roulette_project')

from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game
from utils.plot_helpers import create_comparison_plot, THEORETICAL_EDGES
import numpy as np

def get_plot_path(filename):
    """Get path for saving plots in experiment's plots folder"""
    # Get the directory where THIS script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(current_dir, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    return os.path.join(plots_dir, filename)

def run_comparison_experiment():
    """
    Compare house edges across all three wheel types
    """
    print("🎯 COMPARISON: House Edge Across All Roulette Types")
    print("=" * 60)
    
    wheel_types = ["european", "american", "triple"]
    num_runs = 15
    num_spins = 50000
    
    all_results = {}
    
    for wheel_type in wheel_types:
        print(f"\n--- Testing {wheel_type.upper()} Roulette ---")
        experimental_edges = []
        
        for run in range(num_runs):
            wheel = RouletteWheel(wheel_type)
            player = Player(strategy="flat", initial_bankroll=10000)
            game = Game(wheel, player)
            game.run_simulation(num_spins)
            
            total_wagered = num_spins * player.base_bet
            total_loss = 10000 - player.bankroll
            experimental_edge = (total_loss / total_wagered) * 100
            
            experimental_edges.append(experimental_edge)
            print(f"  Run {run + 1:2d}: {experimental_edge:.2f}%")
        
        all_results[wheel_type] = experimental_edges
        
        # Show summary for this wheel type
        avg_edge = np.mean(experimental_edges)
        print(f"  Average: {avg_edge:.2f}% (Theoretical: {THEORETICAL_EDGES[wheel_type]}%)")
    
    # Create comparison plot
    plt = create_comparison_plot(all_results, num_runs, num_spins)
    path = get_plot_path('all_house_edges_comparison.png')
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\n📊 Comparison plot saved as 'all_house_edges_comparison.png'")

if __name__ == "__main__":
    run_comparison_experiment()