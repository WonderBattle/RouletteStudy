import sys
import os
sys.path.insert(0, '/home/elenacg/ADA511/Project/roulette_project')

from components.player import Player

print("=== Testing Player Class ===")

# Test flat betting player
print("\n1. Testing Flat Betting Player:")
flat_player = Player(strategy="flat")
print(f"   Bankroll: ${flat_player.bankroll}")
print(f"   Next bet: ${flat_player.place_bet()}")

# Test martingale player  
print("\n2. Testing Martingale Player:")
martingale_player = Player(strategy="martingale")
print(f"   Starting bankroll: ${martingale_player.bankroll}")
print(f"   Starting bet: ${martingale_player.place_bet()}")

# Simulate a loss for martingale player
print("\n3. Simulating Martingale after losses:")
martingale_player.process_result(won=False, payout=-10)
print(f"   After 1st loss - Bankroll: ${martingale_player.bankroll}")
print(f"   Next bet: ${martingale_player.place_bet()}")
print(f"   Consecutive losses: {martingale_player.consecutive_losses}")

# Simulate another loss
martingale_player.process_result(won=False, payout=-20)  
print(f"   After 2nd loss - Bankroll: ${martingale_player.bankroll}")
print(f"   Next bet: ${martingale_player.place_bet()}")
print(f"   Consecutive losses: {martingale_player.consecutive_losses}")

# Simulate a win
martingale_player.process_result(won=True, payout=40)
print(f"   After win - Bankroll: ${martingale_player.bankroll}")
print(f"   Next bet: ${martingale_player.place_bet()}")
print(f"   Consecutive losses: {martingale_player.consecutive_losses}")

print("\n=== Player Testing Complete! ===")