import sys
import os
sys.path.insert(0, '/home/elenacg/ADA511/Project/roulette_project')

from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game
from utils.strategy_helpers import create_strategy_plot, create_enhanced_strategy_plot, analyze_martingale_risk
import matplotlib.pyplot as plt

def run_triple_strategy_comparison():
    """
    EXPERIMENT 2: Strategy Comparison on TRIPLE Roulette
    Compare Flat Betting vs Martingale strategy on Triple roulette
    """
    print("🎯 EXPERIMENT 2: Strategy Comparison - TRIPLE Roulette")
    print("=" * 65)
    
    # Use Triple roulette
    wheel_type = "triple"
    
    # Create two identical setups except for strategy
    wheel_flat = RouletteWheel(wheel_type)
    wheel_martingale = RouletteWheel(wheel_type)
    
    # Create players with different strategies but same starting conditions
    flat_player = Player(strategy="flat", initial_bankroll=1000, base_bet=10)
    martingale_player = Player(strategy="martingale", initial_bankroll=1000, base_bet=10)
    
    # Create games for each player
    game_flat = Game(wheel_flat, flat_player)
    game_martingale = Game(wheel_martingale, martingale_player)
    
    # Run simulation for both players
    num_spins = 5000
    print(f"Running {num_spins} spins for both strategies on {wheel_type.upper()} roulette...")
    
    game_flat.run_simulation(num_spins)
    game_martingale.run_simulation(num_spins)
    
    # Extract bankroll history for plotting
    flat_bankrolls = [spin['bankroll'] for spin in game_flat.history]
    martingale_bankrolls = [spin['bankroll'] for spin in game_martingale.history]
    
    # Extract Martingale bet history
    martingale_bets = [spin['bet_amount'] for spin in game_martingale.history]
    
    # Calculate final results
    flat_final = flat_player.bankroll
    martingale_final = martingale_player.bankroll
    
    flat_loss = 1000 - flat_final
    martingale_loss = 1000 - martingale_final
    
    print(f"\n--- FINAL RESULTS AFTER {num_spins} SPINS ---")
    print(f"FLAT BETTING:")
    print(f"  • Final bankroll: ${flat_final:,}")
    print(f"  • Total loss: ${flat_loss:,}")
    print(f"  • Loss percentage: {(flat_loss/1000)*100:.1f}%")
    
    print(f"\nMARTINGALE:")
    print(f"  • Final bankroll: ${martingale_final:,}")
    print(f"  • Total loss: ${martingale_loss:,}") 
    print(f"  • Loss percentage: {(martingale_loss/1000)*100:.1f}%")
    
    # Analyze Martingale behavior
    max_bet, bet_counts, _ = analyze_martingale_risk(game_martingale)
    print(f"  • Maximum bet placed: ${max_bet:,}")
    print(f"  • Bet distribution: {bet_counts}")
    
    # Find interesting sequences for annotation
    interesting_sequences = find_interesting_sequences(martingale_bets, martingale_bankrolls)
    print_sequence_analysis(interesting_sequences)
    
    # Create ENHANCED comparison plot (dual panel)
    fig = create_enhanced_strategy_plot(flat_bankrolls, martingale_bankrolls, martingale_bets, num_spins, wheel_type)
    fig.savefig('strategy_comparison_triple_enhanced.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Also create original plot for comparison
    plt_original = create_strategy_plot(flat_bankrolls, martingale_bankrolls, num_spins, wheel_type)
    plt_original.savefig('strategy_comparison_triple_original.png', dpi=300, bbox_inches='tight')
    plt_original.show()
    
    print(f"\n📊 Enhanced plot saved as 'strategy_comparison_triple_enhanced.png'")
    print(f"📊 Original plot saved as 'strategy_comparison_triple_original.png'")
def find_interesting_sequences(martingale_bets, martingale_bankrolls):
    """
    Find interesting sequences in Martingale betting pattern
    """
    sequences = []
    current_sequence = []
    
    for i, bet in enumerate(martingale_bets):
        if not current_sequence:
            current_sequence.append((i, bet))
        elif bet > current_sequence[-1][1]:
            # Bet increased - continuing losing streak
            current_sequence.append((i, bet))
        else:
            # Bet reset - streak ended
            if len(current_sequence) >= 4:  # Only care about sequences of 4+ losses
                sequences.append(current_sequence)
            current_sequence = [(i, bet)]
    
    # Don't forget the last sequence
    if len(current_sequence) >= 4:
        sequences.append(current_sequence)
    
    return sequences

def print_sequence_analysis(sequences):
    """
    Print analysis of interesting Martingale sequences
    """
    if sequences:
        print(f"\n--- MARTINGALE SEQUENCE ANALYSIS ---")
        for i, seq in enumerate(sequences[:5]):  # Show first 5 sequences
            start_spin, start_bet = seq[0]
            end_spin, max_bet = seq[-1]
            losses = len(seq) - 1  # Number of consecutive losses
            
            print(f"Sequence {i+1}:")
            print(f"  • Spins {start_spin}-{end_spin} ({losses} consecutive losses)")
            print(f"  • Bet progression: ${seq[0][1]} → ${max_bet}")
            print(f"  • Total risked: ${sum(bet for _, bet in seq):,}")

if __name__ == "__main__":
    run_triple_strategy_comparison()