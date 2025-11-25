import matplotlib.pyplot as plt
import numpy as np
import os

# Color schemes for different roulette types in strategy comparisons
STRATEGY_COLORS = {
    "european": {
        "flat": "blue",
        "martingale": "red",
        "martingale_bets": "darkred"
    },
    "american": {
        "flat": "orange", 
        "martingale": "purple",
        "martingale_bets": "darkviolet"
    },
    "triple": {
        "flat": "green",
        "martingale": "brown",
        "martingale_bets": "saddlebrown"
    }
}

def get_plot_path(folder, filename):
    plots_dir = os.path.join(folder, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    return os.path.join(plots_dir, filename)


def create_enhanced_strategy_plot(flat_history, martingale_history, martingale_bets, num_spins, wheel_type):
    """
    Create an enhanced dual-panel plot showing both bankroll and betting patterns
    """
    colors = STRATEGY_COLORS[wheel_type]
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    spins = range(len(flat_history))
    
    # TOP PANEL: Bankroll comparison
    ax1.plot(spins, flat_history, color=colors["flat"], linewidth=2, alpha=0.8,
             label='Flat Betting ($10)')
    ax1.plot(spins, martingale_history, color=colors["martingale"], linewidth=2, alpha=0.8,
             label='Martingale (Base: $10)')
    
    ax1.axhline(y=1000, color='black', linestyle='--', alpha=0.7, label='Starting Bankroll')
    ax1.set_ylabel('Bankroll ($)')
    ax1.set_title(f'Strategy Comparison: {wheel_type.upper()} Roulette\n({num_spins} Spins)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # BOTTOM PANEL: Martingale bet progression
    ax2.plot(spins, martingale_bets, color=colors["martingale_bets"], linewidth=1.5, alpha=0.8,
             label='Martingale Bet Size')
    
    # Add horizontal lines for key bet levels
    bet_levels = [10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120]
    for bet in bet_levels:
        if bet <= max(martingale_bets):
            ax2.axhline(y=bet, color='gray', linestyle=':', alpha=0.3, linewidth=0.5)
    
    ax2.set_xlabel('Spin Number')
    ax2.set_ylabel('Bet Size ($)')
    ax2.set_title('Martingale Bet Progression')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_yscale('log')  # Log scale to see exponential growth clearly
    
    plt.tight_layout()
    return fig

def create_strategy_plot(flat_history, martingale_history, num_spins, wheel_type):
    """
    Original single-panel plot (keep for compatibility)
    """
    colors = STRATEGY_COLORS[wheel_type]
    
    plt.figure(figsize=(12, 8))
    
    # Plot both strategies
    spins = range(len(flat_history))
    plt.plot(spins, flat_history, color=colors["flat"], linewidth=2, alpha=0.8,
             label=f'Flat Betting ($10)')
    plt.plot(spins, martingale_history, color=colors["martingale"], linewidth=2, alpha=0.8,
             label=f'Martingale (Base: $10)')
    
    # Add reference lines and styling
    plt.axhline(y=1000, color='black', linestyle='--', alpha=0.7, label='Starting Bankroll')
    plt.xlabel('Number of Spins')
    plt.ylabel('Bankroll ($)')
    plt.title(f'Strategy Comparison: {wheel_type.upper()} Roulette\n({num_spins} Spins)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return plt

def analyze_martingale_risk(game_martingale):
    """
    Analyze Martingale strategy risk exposure - CORRECTED VERSION
    """
    martingale_bets = [spin['bet_amount'] for spin in game_martingale.history]
    max_bet = max(martingale_bets)
    
    # CORRECTED: Count only UNIQUE bet positions within sequences
    bet_counts = {}
    current_sequence_bets = set()  # Track bets in current sequence
    
    for i, bet in enumerate(martingale_bets):
        if i == 0:
            current_sequence_bets.add(bet)
        elif bet > martingale_bets[i-1]:
            # Continuing losing streak - add to current sequence
            current_sequence_bets.add(bet)
        else:
            # Streak ended - count all unique bets from the sequence
            for sequence_bet in current_sequence_bets:
                bet_counts[sequence_bet] = bet_counts.get(sequence_bet, 0) + 1
            # Start new sequence
            current_sequence_bets = {bet}
    
    # Don't forget the last sequence
    for sequence_bet in current_sequence_bets:
        bet_counts[sequence_bet] = bet_counts.get(sequence_bet, 0) + 1
    
    return max_bet, bet_counts, martingale_bets