import sys
import os
sys.path.insert(0, '/home/elenacg/ADA511/Project/roulette_project')

from components.roulette_wheel import RouletteWheel
from components.player import Player
from components.game import Game

print("=== Testing Complete Game ===")

# Create a European wheel and a flat betting player
wheel = RouletteWheel("european")
player = Player(strategy="flat", initial_bankroll=1000)
game = Game(wheel, player)

print(f"Starting bankroll: ${player.bankroll}")

# Run 10 spins
print("\nRunning 10 spins:")
game.run_simulation(10)

# Show results
print(f"Final bankroll: ${player.bankroll}")
print(f"Number of spins recorded: {len(game.history)}")

# Show first 10 spins in detail
print("\nFirst 10 spins details:")
for i in range(10):
    spin = game.history[i]
    print(f"Spin {spin['spin_number']}: {spin['spin_result']} - {spin['result']} - Bankroll: ${spin['bankroll']}")

print("\n=== Game Testing Complete! ===")