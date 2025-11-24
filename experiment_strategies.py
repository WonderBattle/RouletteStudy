from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game
import matplotlib.pyplot as plt

def run_strategy_comparison():
    """
    EXPERIMENT 2: Strategy Comparison
    Compare Flat Betting vs Martingale strategy to demonstrate that:
    - Martingale creates the illusion of winning with frequent small gains
    - But eventually hits catastrophic losses
    - Both strategies have the same long-term expected loss
    """
    print("🎯 EXPERIMENT 2: Strategy Comparison - Flat vs Martingale")
    print("=" * 60)
    
    # Create two identical setups except for strategy
    wheel_flat = RouletteWheel("european")
    wheel_martingale = RouletteWheel("european")
    
    # Create players with different strategies but same starting conditions
    flat_player = Player(strategy="flat", initial_bankroll=1000, base_bet=10)
    martingale_player = Player(strategy="martingale", initial_bankroll=1000, base_bet=10)
    
    # Create games for each player
    game_flat = Game(wheel_flat, flat_player)
    game_martingale = Game(wheel_martingale, martingale_player)
    
    # Run simulation for both players
    num_spins = 5000
    print(f"Running {num_spins} spins for both strategies...")
    
    game_flat.run_simulation(num_spins)
    game_martingale.run_simulation(num_spins)
    
    # Extract bankroll history for plotting
    flat_bankrolls = [spin['bankroll'] for spin in game_flat.history]
    martingale_bankrolls = [spin['bankroll'] for spin in game_martingale.history]
    
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
    martingale_bets = [spin['bet_amount'] for spin in game_martingale.history]
    max_bet = max(martingale_bets)
    print(f"  • Maximum bet placed: ${max_bet:,}")
    
    # Create comparison plot
    create_strategy_plot(flat_bankrolls, martingale_bankrolls, num_spins)

def create_strategy_plot(flat_history, martingale_history, num_spins):
    """
    Create a visual comparison of the two strategies over time
    """
    # Set up the plot
    plt.figure(figsize=(12, 8))
    
    # Plot both strategies
    spins = range(len(flat_history))
    plt.plot(spins, flat_history, label='Flat Betting ($10)', linewidth=2, alpha=0.8)
    plt.plot(spins, martingale_history, label='Martingale (Base: $10)', linewidth=2, alpha=0.8)
    
    # Add reference lines and styling
    plt.axhline(y=1000, color='red', linestyle='--', alpha=0.7, label='Starting Bankroll')
    plt.xlabel('Number of Spins')
    plt.ylabel('Bankroll ($)')
    plt.title(f'Strategy Comparison: Flat Betting vs Martingale\n({num_spins} Spins on European Roulette)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('strategy_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\n📊 Plot saved as 'strategy_comparison.png'")

if __name__ == "__main__":
    run_strategy_comparison()