import sys
import os
sys.path.insert(0, '/home/elenacg/ADA511/Project/roulette_project')

from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game
from utils.strategy_helpers import create_strategy_plot, create_enhanced_strategy_plot, analyze_martingale_risk
import matplotlib.pyplot as plt

def get_plot_path(filename):
    """Get path for saving plots in experiment's plots folder"""
    # Get the directory where THIS script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(current_dir, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    return os.path.join(plots_dir, filename)

def run_american_strategy_comparison():
    """
    EXPERIMENT 2: Strategy Comparison on AMERICAN Roulette
    Compare Flat Betting vs Martingale strategy on American roulette
    """
    print("🎯 EXPERIMENT 2: Strategy Comparison - AMERICAN Roulette")
    print("=" * 65)
    
    # Use American roulette
    wheel_type = "american"
    
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
    #print(f"  • Bet distribution: {bet_counts}")
    print(f"  • Number of bets at each level: {bet_counts}")
    
    # Find interesting sequences for annotation
    interesting_sequences = find_interesting_sequences(martingale_bets, martingale_bankrolls)
    print_sequence_analysis(interesting_sequences)
    
    # Calculate how many sequences reached each bet level
    sequence_max_bets = {}
    for seq in interesting_sequences:
        max_bet_in_seq = max(bet for _, bet, _ in seq)
        sequence_max_bets[max_bet_in_seq] = sequence_max_bets.get(max_bet_in_seq, 0) + 1
    
    print(f"\n  • Sequences reaching each bet level: {sequence_max_bets}")

    # Create ENHANCED comparison plot (dual panel)
    fig = create_enhanced_strategy_plot(flat_bankrolls, martingale_bankrolls, martingale_bets, num_spins, wheel_type)
    enhanced_path = get_plot_path('strategy_comparison_american_enhanced.png')  # ← USE FUNCTION
    fig.savefig(enhanced_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    # Also create original plot for comparison
    plt_original = create_strategy_plot(flat_bankrolls, martingale_bankrolls, num_spins, wheel_type)
    original_path = get_plot_path('strategy_comparison_american_original.png')  # ← USE FUNCTION
    plt_original.savefig(original_path, dpi=300, bbox_inches='tight')
    plt_original.show()
    
    print(f"\n📊 Enhanced plot saved as '{enhanced_path}'")
    print(f"📊 Original plot saved as '{original_path}'")


def find_interesting_sequences(martingale_bets, martingale_bankrolls):
    """
    Find interesting sequences in Martingale betting pattern
    """
    sequences = []
    current_sequence = []
    
    for i, bet in enumerate(martingale_bets):
        if not current_sequence:
            current_sequence.append((i, bet, martingale_bankrolls[i]))
        elif bet > current_sequence[-1][1]:
            # Bet increased - continuing losing streak
            current_sequence.append((i, bet, martingale_bankrolls[i]))
        else:
            # Bet reset - streak ended (either win or new sequence)
            if len(current_sequence) >= 3:  # Sequences of 3+ losses
                sequences.append(current_sequence)
            current_sequence = [(i, bet, martingale_bankrolls[i])]
    
    # Don't forget the last sequence
    if len(current_sequence) >= 3:
        sequences.append(current_sequence)
    
    return sequences


def print_sequence_analysis(sequences):
    """
    Print analysis of interesting Martingale sequences
    """
    if sequences:
        print(f"\n--- MARTINGALE SEQUENCE ANALYSIS ---")
        
        # Sort sequences by maximum bet (highest risk first)
        sequences.sort(key=lambda seq: max(bet for _, bet, _ in seq), reverse=True)
        
        for i, seq in enumerate(sequences[:8]):  # Show top 8 sequences
            start_spin, start_bet, start_br = seq[0]
            end_spin, max_bet, end_br = seq[-1]
            losses = len(seq) - 1  # Number of consecutive losses
            
            # Calculate total risked in this sequence
            total_risked = sum(bet for _, bet, _ in seq)
            
            # Determine if the sequence ended with a win or loss
            # If bet reset after this sequence, it means the last spin was a WIN
            sequence_result = "WON" if end_br > start_br else "LOST"
            profit_loss = end_br - start_br
            
            print(f"Sequence {i+1} ({sequence_result}):")
            print(f"  • Spins {start_spin}-{end_spin} ({losses} consecutive losses)")
            print(f"  • Bet progression: ${start_bet} → ${max_bet}")
            print(f"  • Total risked: ${total_risked:,}")
            print(f"  • Result: {sequence_result} ${abs(profit_loss):,}")
            
            # Show the actual bet sequence for long streaks
            if losses >= 5:
                bet_sequence = [bet for _, bet, _ in seq]
                print(f"  • Bet sequence: {bet_sequence}")


if __name__ == "__main__":
    run_american_strategy_comparison()