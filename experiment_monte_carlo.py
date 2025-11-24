from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game
import matplotlib.pyplot as plt
import numpy as np

def run_monte_carlo_analysis():
    """
    EXPERIMENT 3: Monte Carlo Analysis
    Run many simulations to understand the distribution of outcomes:
    - What percentage of players are ahead after N spins?
    - What does the distribution of final bankrolls look like?
    - How does luck affect short-term vs long-term results?
    """
    print("🎯 EXPERIMENT 3: Monte Carlo Analysis")
    print("=" * 50)
    
    # Monte Carlo parameters
    num_simulations = 1000  # Number of different players
    spins_per_simulation = 1000  # Spins for each player
    
    print(f"Running {num_simulations} simulations of {spins_per_simulation} spins each...")
    print("This may take a moment...")
    
    final_bankrolls = []  # Store final results for all players
    players_ahead = 0     # Count how many players ended with more than they started
    
    # Run all simulations
    for sim in range(num_simulations):
        # Create new wheel and player for each simulation
        wheel = RouletteWheel("european")
        player = Player(strategy="flat", initial_bankroll=1000)
        game = Game(wheel, player)
        
        # Run the simulation
        game.run_simulation(spins_per_simulation)
        
        # Record the final bankroll
        final_bankroll = player.bankroll
        final_bankrolls.append(final_bankroll)
        
        # Count if player is ahead
        if final_bankroll > 1000:
            players_ahead += 1
        
        # Show progress for long runs
        if (sim + 1) % 100 == 0:
            print(f"  Completed {sim + 1}/{num_simulations} simulations...")
    
    # Calculate statistics
    average_final = np.mean(final_bankrolls)
    min_final = min(final_bankrolls)
    max_final = max(final_bankrolls)
    probability_ahead = (players_ahead / num_simulations) * 100
    
    # Theoretical expected value calculation
    theoretical_edge = 2.70  # 2.70% for European roulette
    total_wagered = spins_per_simulation * 10  # $10 per spin
    expected_loss = total_wagered * (theoretical_edge / 100)
    theoretical_final = 1000 - expected_loss
    
    print(f"\n--- MONTE CARLO RESULTS ---")
    print(f"After {spins_per_simulation} spins per player:")
    print(f"  • Average final bankroll: ${average_final:.2f}")
    print(f"  • Theoretical expected: ${theoretical_final:.2f}")
    print(f"  • Best result: ${max_final:,}")
    print(f"  • Worst result: ${min_final:,}")
    print(f"  • Players ahead: {players_ahead}/{num_simulations} ({probability_ahead:.1f}%)")
    
    # Create visualizations
    create_monte_carlo_plots(final_bankrolls, num_simulations, spins_per_simulation)

def create_monte_carlo_plots(final_bankrolls, num_simulations, spins_per_simulation):
    """
    Create histograms and analysis plots for Monte Carlo results
    """
    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Histogram of final bankrolls
    ax1.hist(final_bankrolls, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    ax1.axvline(x=1000, color='red', linestyle='--', linewidth=2, label='Starting Bankroll ($1000)')
    ax1.axvline(x=np.mean(final_bankrolls), color='green', linestyle='--', linewidth=2, label=f'Average (${np.mean(final_bankrolls):.0f})')
    
    ax1.set_xlabel('Final Bankroll ($)')
    ax1.set_ylabel('Number of Players')
    ax1.set_title(f'Distribution of Final Bankrolls\n{num_simulations} Players, {spins_per_simulation} Spins Each')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Cumulative probability
    sorted_bankrolls = np.sort(final_bankrolls)
    cumulative_prob = np.arange(1, len(sorted_bankrolls) + 1) / len(sorted_bankrolls)
    
    ax2.plot(sorted_bankrolls, cumulative_prob * 100, linewidth=2, color='orange')
    ax2.axvline(x=1000, color='red', linestyle='--', linewidth=2, label='Starting Bankroll')
    ax2.axhline(y=50, color='gray', linestyle=':', alpha=0.5, label='50% Probability')
    
    ax2.set_xlabel('Final Bankroll ($)')
    ax2.set_ylabel('Cumulative Probability (%)')
    ax2.set_title('Cumulative Distribution Function\n"What are my chances of having at least X dollars?"')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Add some probability annotations
    players_ahead = len([b for b in final_bankrolls if b > 1000])
    prob_ahead = (players_ahead / len(final_bankrolls)) * 100
    ax2.text(0.05, 0.95, f'Probability of being ahead: {prob_ahead:.1f}%', 
             transform=ax2.transAxes, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('monte_carlo_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"📊 Monte Carlo plots saved as 'monte_carlo_analysis.png'")

if __name__ == "__main__":
    run_monte_carlo_analysis()