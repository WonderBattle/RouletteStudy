import sys
import os
sys.path.insert(0, '/home/elenacg/ADA511/Project/roulette_project')

from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game
import matplotlib.pyplot as plt
import numpy as np

def run_strategy_monte_carlo():
    """
    MONTE CARLO ANALYSIS: Strategy Comparison with Multiple Players
    Run many players with each strategy to see the distribution of outcomes
    """
    print("🎯 MONTE CARLO: Strategy Comparison with Multiple Players")
    print("=" * 70)
    
    wheel_type = "european"
    num_players = 100  # Test 100 players for each strategy
    num_spins = 1000   # Fewer spins per player for faster execution
    
    print(f"Testing {num_players} players for each strategy on {wheel_type.upper()} roulette")
    print(f"Each player plays {num_spins} spins")
    
    # Store results for all players
    flat_finals = []
    martingale_finals = []
    martingale_max_bets = []
    
    for player_num in range(num_players):
        if (player_num + 1) % 20 == 0:
            print(f"  Completed {player_num + 1}/{num_players} players...")
        
        # Flat betting player
        wheel_flat = RouletteWheel(wheel_type)
        flat_player = Player(strategy="flat", initial_bankroll=1000, base_bet=10)
        game_flat = Game(wheel_flat, flat_player)
        game_flat.run_simulation(num_spins)
        flat_finals.append(flat_player.bankroll)
        
        # Martingale player  
        wheel_martingale = RouletteWheel(wheel_type)
        martingale_player = Player(strategy="martingale", initial_bankroll=1000, base_bet=10)
        game_martingale = Game(wheel_martingale, martingale_player)
        game_martingale.run_simulation(num_spins)
        martingale_finals.append(martingale_player.bankroll)
        martingale_max_bets.append(max([spin['bet_amount'] for spin in game_martingale.history]))
    
    # Calculate statistics
    flat_avg = np.mean(flat_finals)
    martingale_avg = np.mean(martingale_finals)
    flat_std = np.std(flat_finals)
    martingale_std = np.std(martingale_finals)
    
    # Players who ended ahead
    flat_ahead = len([b for b in flat_finals if b > 1000])
    martingale_ahead = len([b for b in martingale_finals if b > 1000])
    
    print(f"\n--- MONTE CARLO RESULTS ({num_players} PLAYERS) ---")
    print(f"FLAT BETTING:")
    print(f"  • Average final bankroll: ${flat_avg:.0f}")
    print(f"  • Standard deviation: ${flat_std:.0f}")
    print(f"  • Players ahead: {flat_ahead}/{num_players} ({flat_ahead/num_players*100:.1f}%)")
    
    print(f"\nMARTINGALE:")
    print(f"  • Average final bankroll: ${martingale_avg:.0f}") 
    print(f"  • Standard deviation: ${martingale_std:.0f}")
    print(f"  • Players ahead: {martingale_ahead}/{num_players} ({martingale_ahead/num_players*100:.1f}%)")
    print(f"  • Average max bet: ${np.mean(martingale_max_bets):.0f}")
    print(f"  • Highest max bet: ${max(martingale_max_bets):,}")
    
    # Create distribution plot
    create_monte_carlo_plot(flat_finals, martingale_finals, num_players, num_spins, wheel_type)

def create_monte_carlo_plot(flat_finals, martingale_finals, num_players, num_spins, wheel_type):
    """
    Create histogram showing distribution of outcomes for both strategies
    """
    plt.figure(figsize=(12, 8))
    
    # Create histograms
    bins = np.linspace(min(flat_finals + martingale_finals), 
                      max(flat_finals + martingale_finals), 30)
    
    plt.hist(flat_finals, bins=bins, alpha=0.7, label='Flat Betting', 
             color='blue', edgecolor='black')
    plt.hist(martingale_finals, bins=bins, alpha=0.7, label='Martingale',
             color='red', edgecolor='black')
    
    plt.axvline(x=1000, color='black', linestyle='--', linewidth=2, 
                label='Starting Bankroll ($1000)')
    plt.xlabel('Final Bankroll ($)')
    plt.ylabel('Number of Players')
    plt.title(f'Strategy Outcome Distribution: {wheel_type.upper()} Roulette\n'
              f'({num_players} players, {num_spins} spins each)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('strategy_monte_carlo.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\n📊 Monte Carlo plot saved as 'strategy_monte_carlo.png'")

if __name__ == "__main__":
    run_strategy_monte_carlo()