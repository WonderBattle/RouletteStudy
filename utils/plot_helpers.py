import os
import matplotlib.pyplot as plt
import numpy as np

# Define color schemes for different roulette types
COLOR_SCHEMES = {
    "european": {
        "primary": "blue",
        "secondary": "lightblue", 
        "theoretical": "darkblue"
    },
    "american": {
        "primary": "red", 
        "secondary": "lightcoral",
        "theoretical": "darkred"
    },
    "triple": {
        "primary": "green",
        "secondary": "lightgreen",
        "theoretical": "darkgreen"
    }
}

# Theoretical house edges
THEORETICAL_EDGES = {
    "european": 2.70,
    "american": 5.26,
    "triple": 7.69
}

def get_plot_path(folder, filename):
    plots_dir = os.path.join(folder, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    return os.path.join(plots_dir, filename)

def create_single_wheel_plot(experimental_edges, wheel_type, num_runs, num_spins):
    """
    Create a distribution plot for a single wheel type with custom colors
    """
    colors = COLOR_SCHEMES[wheel_type]
    theoretical_edge = THEORETICAL_EDGES[wheel_type]
    
    # Set up the plot
    plt.figure(figsize=(12, 8))
    
    # Create x positions
    runs = range(1, len(experimental_edges) + 1)
    
    # Plot individual results with wheel-specific colors
    plt.scatter(runs, experimental_edges, color=colors["primary"], s=80, alpha=0.8,
                label=f'Experimental House Edge (Individual Runs)')
    
    # Connecting line
    plt.plot(runs, experimental_edges, color=colors["primary"], alpha=0.4, linewidth=1.5)
    
    # Theoretical house edge line
    plt.axhline(y=theoretical_edge, color=colors["theoretical"], linestyle='--', 
                linewidth=3, label=f'Theoretical House Edge ({theoretical_edge}%)')
    
    # Average experimental edge
    average_edge = np.mean(experimental_edges)
    plt.axhline(y=average_edge, color=colors["secondary"], linestyle='-.', linewidth=2,
                label=f'Average Experimental Edge ({average_edge:.2f}%)')
    
    # Standard deviation region
    std_dev = np.std(experimental_edges)
    plt.fill_between(runs, average_edge - std_dev, average_edge + std_dev,
                     color=colors["secondary"], alpha=0.3, label='±1 Standard Deviation')
    
    # Customize plot
    plt.xlabel('Experiment Run Number')
    plt.ylabel('House Edge (%)')
    plt.title(f'House Edge Distribution: {wheel_type.upper()} Roulette\n'
              f'({num_runs} runs of {num_spins:,} spins each)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Set dynamic y-axis limits
    y_margin = max(1.0, std_dev * 2.5)
    plt.ylim(theoretical_edge - y_margin, theoretical_edge + y_margin)
    
    # Statistical annotation
    plt.text(0.02, 0.98, f'Standard Deviation: {std_dev:.2f}%', 
             transform=plt.gca().transAxes, bbox=dict(boxstyle="round,pad=0.3", 
             facecolor="white", alpha=0.9))
    
    plt.tight_layout()
    return plt

def create_comparison_plot(all_results, num_runs, num_spins):
    """
    Create a comparison plot for all three wheel types
    """
    plt.figure(figsize=(14, 8))
    
    # Plot each wheel type
    for i, (wheel_type, edges) in enumerate(all_results.items()):
        colors = COLOR_SCHEMES[wheel_type]
        theoretical_edge = THEORETICAL_EDGES[wheel_type]
        
        # Create positions with slight offset
        positions = np.arange(len(edges)) + 1 + (i - 1) * 0.25
        
        # Plot experimental points
        plt.scatter(positions, edges, color=colors["primary"], s=60, alpha=0.8,
                   label=f'{wheel_type.upper()} (Experimental)', marker='o' if wheel_type == "european" else 's' if wheel_type == "american" else '^')
        
        # Plot theoretical line
        plt.axhline(y=theoretical_edge, color=colors["theoretical"], 
                   linestyle='--', alpha=0.8, linewidth=2.5,
                   label=f'{wheel_type.upper()} (Theoretical: {theoretical_edge}%)')
    
    plt.xlabel('Experiment Run Number')
    plt.ylabel('House Edge (%)')
    plt.title(f'House Edge Comparison: All Roulette Types\n'
              f'({num_runs} runs of {num_spins:,} spins each)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Legend outside plot
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return plt