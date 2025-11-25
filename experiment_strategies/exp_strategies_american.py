import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game
from utils.strategy_helpers import (
    create_strategy_plot, 
    create_enhanced_strategy_plot, 
    analyze_martingale_risk
)
from utils.monte_carlo_helpers import get_plot_path 
import matplotlib.pyplot as plt

# (Helpers included below main function to match structure)

def run_american_strategy_comparison():
    print("🎯 EXPERIMENT 2: Strategy Comparison - AMERICAN Roulette")
    print("=" * 65)
    
    wheel_type = "american"
    wheel_flat = RouletteWheel(wheel_type)
    wheel_martingale = RouletteWheel(wheel_type)
    
    START_BANKROLL = 1000
    
    # FIX: Explicit configuration
    flat_player = Player(strategy="flat", initial_bankroll=START_BANKROLL, base_bet=10)
    flat_player.bet_type = "color"
    flat_player.bet_value = "red"
    
    martingale_player = Player(strategy="martingale", initial_bankroll=START_BANKROLL, base_bet=10)
    martingale_player.bet_type = "color"
    martingale_player.bet_value = "red"
    
    game_flat = Game(wheel_flat, flat_player)
    game_martingale = Game(wheel_martingale, martingale_player)
    
    num_spins = 5000
    print(f"Running {num_spins} spins for both strategies on {wheel_type.upper()} roulette...")
    
    game_flat.run_simulation(num_spins)
    game_martingale.run_simulation(num_spins)
    
    flat_bankrolls = [spin['bankroll'] for spin in game_flat.history]
    martingale_bankrolls = [spin['bankroll'] for spin in game_martingale.history]
    martingale_bets = [spin['bet_amount'] for spin in game_martingale.history]
    
    flat_final = flat_player.bankroll
    martingale_final = martingale_player.bankroll
    
    flat_loss = START_BANKROLL - flat_final
    martingale_loss = START_BANKROLL - martingale_final
    
    print(f"\n--- FINAL RESULTS AFTER {num_spins} SPINS ---")
    print(f"FLAT BETTING:")
    print(f"  • Final bankroll: ${flat_final:,}")
    print(f"  • Total loss: ${flat_loss:,}")
    print(f"  • Loss percentage: {(flat_loss/START_BANKROLL)*100:.1f}%")
    
    print(f"\nMARTINGALE:")
    print(f"  • Final bankroll: ${martingale_final:,}")
    print(f"  • Total loss: ${martingale_loss:,}") 
    print(f"  • Loss percentage: {(martingale_loss/START_BANKROLL)*100:.1f}%")
    
    max_bet, bet_counts, _ = analyze_martingale_risk(game_martingale)
    print(f"  • Maximum bet placed: ${max_bet:,}")
    
    interesting_sequences = find_interesting_sequences(martingale_bets, martingale_bankrolls)
    print_sequence_analysis(interesting_sequences)
    
    sequence_max_bets = {}
    for seq in interesting_sequences:
        max_bet_in_seq = max(bet for _, bet, _ in seq)
        sequence_max_bets[max_bet_in_seq] = sequence_max_bets.get(max_bet_in_seq, 0) + 1
    
    print(f"\n  • Sequences reaching each bet level: {sequence_max_bets}")

    # FIX: Shared path helper
    current_folder = os.path.dirname(os.path.abspath(__file__))

    fig = create_enhanced_strategy_plot(flat_bankrolls, martingale_bankrolls, martingale_bets, num_spins, wheel_type)
    enhanced_path = get_plot_path(current_folder, 'strategy_comparison_american_enhanced.png')
    fig.savefig(enhanced_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    plt_original = create_strategy_plot(flat_bankrolls, martingale_bankrolls, num_spins, wheel_type)
    original_path = get_plot_path(current_folder, 'strategy_comparison_american_original.png')
    plt_original.savefig(original_path, dpi=300, bbox_inches='tight')
    plt_original.show()
    
    print(f"\n📊 Enhanced plot saved as 'strategy_comparison_american_enhanced.png'")
    print(f"📊 Original plot saved as 'strategy_comparison_american_original.png'")

def find_interesting_sequences(martingale_bets, martingale_bankrolls):
    sequences = []
    current_sequence = []
    for i, bet in enumerate(martingale_bets):
        if not current_sequence:
            current_sequence.append((i, bet, martingale_bankrolls[i]))
        elif bet > current_sequence[-1][1]:
            current_sequence.append((i, bet, martingale_bankrolls[i]))
        else:
            if len(current_sequence) >= 3: sequences.append(current_sequence)
            current_sequence = [(i, bet, martingale_bankrolls[i])]
    if len(current_sequence) >= 3: sequences.append(current_sequence)
    return sequences

def print_sequence_analysis(sequences):
    if sequences:
        print(f"\n--- MARTINGALE SEQUENCE ANALYSIS ---")
        sequences.sort(key=lambda seq: max(bet for _, bet, _ in seq), reverse=True)
        for i, seq in enumerate(sequences[:8]):
            start_spin, start_bet, start_br = seq[0]
            end_spin, max_bet, end_br = seq[-1]
            losses = len(seq) - 1
            total_risked = sum(bet for _, bet, _ in seq)
            sequence_result = "WON" if end_br > start_br else "LOST"
            profit_loss = end_br - start_br
            print(f"Sequence {i+1} ({sequence_result}):")
            print(f"  • Spins {start_spin}-{end_spin} ({losses} consecutive losses)")
            print(f"  • Bet progression: ${start_bet} → ${max_bet}")
            print(f"  • Total risked: ${total_risked:,}")
            print(f"  • Result: {sequence_result} ${abs(profit_loss):,}")

if __name__ == "__main__":
    run_american_strategy_comparison()