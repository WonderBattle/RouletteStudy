import matplotlib.pyplot as plt
import numpy as np
import os

def get_plot_path(folder, filename):
    plots_dir = os.path.join(folder, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    return os.path.join(plots_dir, filename)

def create_bankroll_path_plot(histories, bet_type, wheel_type, num_spins):
    """
    Plots the trajectory of every player and the average trend.
    """
    plt.figure(figsize=(12, 7))
    
    # 1. Convert list of lists to numpy array for easy math
    # Shape: (num_players, num_spins + 1)
    data = np.array(histories)
    
    # 2. Plot individual player paths (The "Spaghetti")
    # We use a very low alpha (transparency) so overlapping lines show density
    # We limit to first 100 players so the plot doesn't get too messy if we run thousands
    players_to_plot = min(len(histories), 200) 
    
    color = 'blue' if bet_type == 'color' else 'orange'
    
    # Plot the individual lines
    for i in range(players_to_plot):
        plt.plot(data[i], color=color, alpha=0.1, linewidth=0.5)
        
    # 3. Calculate and Plot the AVERAGE line (The "Drift")
    # axis=0 calculates the mean down the columns (for each spin step)
    average_path = np.mean(data, axis=0)
    
    plt.plot(average_path, color='black', linewidth=2.5, linestyle='-', 
             label=f'Average (All {len(histories)} Players)')
    
    # 4. Add Reference Line (Starting Bankroll)
    plt.axhline(y=1000, color='red', linestyle='--', linewidth=1.5, label='Start ($1000)')
    
    # Styling
    plt.title(f'Bankroll Trajectories: {bet_type.title()} Bets ({wheel_type.title()})\nVisualizing Volatility vs. House Edge')
    plt.xlabel('Spin Number')
    plt.ylabel('Bankroll ($)')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    
    return plt

def create_distribution_comparison(color_results, number_results, num_players, num_spins, wheel_type):
    """
    Compare distributions of Color Bets vs Number Bets
    This visualizes RISK (Variance).
    """
    plt.figure(figsize=(14, 8))
    
    # Create common bins for the histogram
    all_data = color_results + number_results
    # Limit range to ignore extreme outliers for better visualization if needed
    data_min, data_max = min(all_data), max(all_data)
    bins = np.linspace(data_min, data_max, 50)
    
    # Plot Color Bets (Low Variance)
    plt.hist(color_results, bins=50, alpha=0.6, label='Color Bets (Red)', 
             color='blue', edgecolor='black', density=True)
    
    # Plot Number Bets (High Variance)
    plt.hist(number_results, bins=50, alpha=0.5, label='Number Bets (Single)', 
             color='orange', edgecolor='black', density=True)
    
    # Add vertical line for starting bankroll
    plt.axvline(x=1000, color='red', linestyle='--', linewidth=2, label='Start ($1000)')
    
    plt.xlabel('Final Bankroll ($)')
    plt.ylabel('Frequency (Probability Density)')
    plt.title(f'Risk Profile: Color vs Number Bets ({wheel_type.upper()} Roulette)\n{num_players} Players, {num_spins} Spins Each')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    return plt