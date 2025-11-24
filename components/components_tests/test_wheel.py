import sys
import os
sys.path.insert(0, '/home/elenacg/ADA511/Project/roulette_project')

from components.roulette_wheel import RouletteWheel

print("=== Testing Roulette Wheel Class ===")

# Test European wheel
print("\n1. Testing European Wheel:")
european = RouletteWheel("european")
print(f"   European wheel has {european.get_total_pockets()} pockets")

# Test a few spins
print("   Test spins:")
for i in range(5):
    spin_result = european.spin()
    print(f"   Spin {i+1}: {spin_result}")

# Test American wheel  
print("\n2. Testing American Wheel:")
american = RouletteWheel("american")
print(f"   American wheel has {american.get_total_pockets()} pockets")

# Test Triple Zero wheel
print("\n3. Testing Triple Zero Wheel:")
triple = RouletteWheel("triple")
print(f"   Triple zero wheel has {triple.get_total_pockets()} pockets")

print("\n=== Wheel Testing Complete! ===")