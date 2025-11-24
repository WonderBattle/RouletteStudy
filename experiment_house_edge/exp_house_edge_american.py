import sys
import os
sys.path.insert(0, '/home/elenacg/ADA511/Project/roulette_project')

from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game
from utils.plot_helpers import create_single_wheel_plot, THEORETICAL_EDGES
import numpy as np

def run_american_experiment():
    """
    Detailed house edge analysis for American roulette
    """
    print("🎯 AMERICAN ROULETTE: House Edge Distribution Analysis")
    print("=" * 60)
    
    wheel_type = "american"
    num_runs = 20
    num_spins = 100000
    
    print(f"Running {num_runs} experiments of {num_spins:,} spins each...")
    print(f"Theoretical house edge: {THEORETICAL_EDGES[wheel_type]}%")
    
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
        print(f"Run {run + 1:2d}: Experimental edge = {experimental_edge:.2f}%")
    
    # Statistics
    average_edge = np.mean(experimental_edges)
    std_dev = np.std(experimental_edges)
    
    print(f"\n--- STATISTICAL SUMMARY ---")
    print(f"Average experimental edge: {average_edge:.2f}%")
    print(f"Theoretical edge: {THEORETICAL_EDGES[wheel_type]}%")
    print(f"Standard deviation: {std_dev:.2f}%")
    print(f"Range: {min(experimental_edges):.2f}% to {max(experimental_edges):.2f}%")
    
    # Create and save plot
    plt = create_single_wheel_plot(experimental_edges, wheel_type, num_runs, num_spins)
    plt.savefig('american_house_edge.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"📊 Plot saved as 'american_house_edge.png'")

if __name__ == "__main__":
    run_american_experiment()