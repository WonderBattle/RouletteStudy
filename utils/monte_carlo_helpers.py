import matplotlib.pyplot as plt
import numpy as np
import os

def get_plot_path(folder, filename):
    plots_dir = os.path.join(folder, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    return os.path.join(plots_dir, filename)

# Update the definition line:
def create_bankroll_path_plot(histories, bet_type, wheel_type, num_spins, strategy_label=None):
    """
    Plots the trajectory of every player and the average trend.
    """
    plt.figure(figsize=(12, 7))
    
    data = np.array(histories)
    players_to_plot = min(len(histories), 200) 
    
    color = 'blue' if bet_type == 'color' else 'orange'
    
    # Plot lines
    for i in range(players_to_plot):
        plt.plot(data[i], color=color, alpha=0.1, linewidth=0.5)
        
    average_path = np.mean(data, axis=0)
    
    plt.plot(average_path, color='black', linewidth=2.5, linestyle='-', 
             label=f'Average (All {len(histories)} Players)')
    
    plt.axhline(y=1000, color='red', linestyle='--', linewidth=1.5, label='Start ($1000)')
    
    # --- FIX: DYNAMIC TITLE LOGIC ---
    if strategy_label:
        title_text = f'Bankroll Trajectories: {strategy_label} ({wheel_type.title()})'
    else:
        title_text = f'Bankroll Trajectories: {bet_type.title()} Bets ({wheel_type.title()})'
        
    plt.title(f'{title_text}\nVisualizing Volatility vs. House Edge')
    # --------------------------------
    
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

def create_three_wheel_comparison(euro_data, amer_data, trip_data, num_players, num_spins, bet_type="Color"):
    """
    Overlays histograms of all 3 wheels to show the 'Shift' in expected value.
    """
    plt.figure(figsize=(12, 7))
    
    # Create common bins so the bars align perfectly
    all_data = euro_data + amer_data + trip_data
    bins = np.linspace(min(all_data), max(all_data), 60)
    
    # Plot European (Best Odds)
    plt.hist(euro_data, bins=bins, alpha=0.5, label='European (1 Zero)', 
             color='blue', edgecolor='black', density=True)
    
    # Plot American (Medium Odds)
    plt.hist(amer_data, bins=bins, alpha=0.5, label='American (2 Zeros)', 
             color='orange', edgecolor='black', density=True)
    
    # Plot Triple (Worst Odds)
    plt.hist(trip_data, bins=bins, alpha=0.5, label='Triple Zero (3 Zeros)', 
             color='green', edgecolor='black', density=True)
    
    # Add Reference Line (Start)
    plt.axvline(x=1000, color='red', linestyle='--', linewidth=2, label='Start ($1000)')
    
    # Add Average Lines (The "Drift")
    plt.axvline(x=np.mean(euro_data), color='blue', linestyle=':', linewidth=2)
    plt.axvline(x=np.mean(amer_data), color='orange', linestyle=':', linewidth=2)
    plt.axvline(x=np.mean(trip_data), color='green', linestyle=':', linewidth=2)
    
    plt.xlabel('Final Bankroll ($)')
    plt.ylabel('Probability Density')
    #plt.title(f'The Cost of Zeros: Wheel Comparison\n(Flat Betting on Color, {num_players} Players, {num_spins} Spins)')
    plt.title(f'The Cost of Zeros: Wheel Comparison\n(Flat Betting on {bet_type}, {num_players} Players, {num_spins} Spins)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    return plt


def create_martingale_histogram(final_bankrolls, num_players, num_spins, wheel_type):
    """
    Special histogram for Martingale.
    Highlights the split between 'Small Winners' and 'Big Losers'.
    """
    plt.figure(figsize=(12, 7))
    
    # Martingale creates a wide range of negative values, so we need dynamic bins
    data_min = min(final_bankrolls)
    data_max = max(final_bankrolls)
    bins = np.linspace(data_min, data_max, 60)
    
    plt.hist(final_bankrolls, bins=bins, alpha=0.7, label='Martingale Outcomes', 
             color='purple', edgecolor='black')
    
    # Reference Line (Start)
    plt.axvline(x=1000, color='red', linestyle='--', linewidth=2, label='Start ($1000)')
    
    plt.xlabel('Final Bankroll ($)')
    plt.ylabel('Number of Players')
    plt.title(f'Martingale with Limits ({wheel_type.title()})\nMax Bet $1000 | {num_players} Players | {num_spins} Spins')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    return plt

def create_martingale_comparison(euro_data, amer_data, trip_data, num_players):
    """
    Overlays histograms of all 3 wheels for Martingale.
    Shows how the 'Bankrupt' pile grows as House Edge increases.
    """
    plt.figure(figsize=(12, 7))
    
    # Determine range based on all data (some players lose $5000+, some win $1000)
    all_data = euro_data + amer_data + trip_data
    data_min = max(min(all_data), -5000) # Cap min visualization at -5000 for readability
    data_max = max(all_data)
    bins = np.linspace(data_min, data_max, 60)
    
    # Plot with transparency
    plt.hist(euro_data, bins=bins, alpha=0.5, label='European (1 Zero)', color='blue', edgecolor='black', density=True)
    plt.hist(amer_data, bins=bins, alpha=0.5, label='American (2 Zeros)', color='orange', edgecolor='black', density=True)
    plt.hist(trip_data, bins=bins, alpha=0.5, label='Triple Zero (3 Zeros)', color='green', edgecolor='black', density=True)
    
    # Reference Line (Start)
    plt.axvline(x=1000, color='red', linestyle='--', linewidth=2, label='Start ($1000)')
    
    plt.xlabel('Final Bankroll ($)')
    plt.ylabel('Number of Players')
    plt.title(f'Martingale Survival Comparison\n(Max Bet $1000, {num_players} Players)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    return plt