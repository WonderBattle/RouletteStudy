import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game
from utils.plot_helpers import create_single_wheel_plot, THEORETICAL_EDGES
from utils.monte_carlo_helpers import get_plot_path
import numpy as np
import matplotlib.pyplot as plt

def run_american_experiment():
    """Detailed analysis for American Roulette"""
    print("🚀 AMERICAN ROULETTE: House Edge Distribution Analysis")
    print("=" * 60)
    
    wheel_type = "american"
    num_runs = 20
    num_spins = 100000
    START_BANKROLL = 10000
    
    print(f"Running {num_runs} experiments of {num_spins:,} spins each...")
    print(f"Theoretical house edge: {THEORETICAL_EDGES[wheel_type]}%")
    
    experimental_edges = []
    
    for run in range(num_runs):
        wheel = RouletteWheel(wheel_type)
        
        player = Player(strategy="flat", initial_bankroll=START_BANKROLL, base_bet=10)
        player.bet_type = "color"
        player.bet_value = "red"
        
        game = Game(wheel, player)
        game.run_simulation(num_spins)
        
        total_wagered = num_spins * player.base_bet
        total_loss = START_BANKROLL - player.bankroll
        
        experimental_edge = (total_loss / total_wagered) * 100
        experimental_edges.append(experimental_edge)
        print(f"Run {run + 1:2d}: Experimental edge = {experimental_edge:.2f}%")

    average_edge = np.mean(experimental_edges)
    std_dev = np.std(experimental_edges)
    
    print(f"\n--- STATISTICAL SUMMARY ---")
    print(f"Average experimental edge: {average_edge:.2f}%")
    print(f"Theoretical edge: {THEORETICAL_EDGES[wheel_type]}%")
    print(f"Standard deviation: {std_dev:.2f}%")
    print(f"Range: {min(experimental_edges):.2f}% to {max(experimental_edges):.2f}%")
    
    plt = create_single_wheel_plot(experimental_edges, wheel_type, num_runs, num_spins)
    
    current_folder = os.path.dirname(os.path.abspath(__file__))
    save_path = get_plot_path(current_folder, 'american_house_edge.png')
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    print(f"📊 Plot saved to: {save_path}")

if __name__ == "__main__":
    run_american_experiment()