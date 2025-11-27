
# 🎰 Why You Can't Beat the Wheel: A Monte Carlo Simulation

## 📌 Project Overview
This project is a scientific study of **Roulette mathematics, betting strategies, and risk management**. Using Python and Monte Carlo simulations, we analyze why "The House Always Wins" is a mathematical certainty rather than just a saying.

We simulate millions of spins across three different roulette variants (European, American, and Triple Zero) to visualize how the **House Edge**, **Variance**, and **Table Limits** affect player bankrolls over time.

## 🧪 The Experiments

### 1️⃣ Experiment 1: The Mathematical Verification (House Edge)
**Goal:** Verify that the theoretical House Edge matches reality over the long run.
* **Method:** Simulated 100,000 spins per wheel type.
* **Key Finding:** The simulation converged perfectly to the theoretical values:
    * European (1 Zero): **2.70%**
    * American (2 Zeros): **5.26%**
    * Triple Zero (3 Zeros): **7.69%**

### 2️⃣ Experiment 2: The Illusion of Winning (Strategy Comparison)
**Goal:** Compare Flat Betting vs. Martingale Strategy under "Infinite Money" conditions and no Table Limit.
* **Method:** Simulated 5,000 spins allowing deep debt (no bankruptcy).
* **Key Finding:** Martingale creates an illusion of constant winning (slow upward trend) but hides massive risks. We observed specific sequences where a player risked over 600,000 just to win $10, proving the strategy is unsustainable without infinite wealth.

### 3️⃣ Experiment 3: The Volatility Trap (Flat Betting Monte Carlo)
**Goal:** Prove that "Risk" (Variance) is different from "Edge" (Expected Value).
* **Method:** Compared 1,000 players betting on **Color (Low Risk)** vs. **Numbers (High Risk)**.
* **Key Finding:**
    * **Color Bets:** Produces a "thick rope" graph (low variance).
    * **Number Bets:** Produces a "diagonal slide" graph (high variance).
    * **The Trap:** Despite the different shapes, the **Average Final Bankroll** was identical (~$730). You cannot outrun the House Edge by taking higher risks.

### 4️⃣ Experiment 4: The Reality Check (Martingale Monte Carlo with Limits)
**Goal:** Test the Martingale strategy against real-world Casino Table Limits.
* **Method:** Enforced a standard table limit (10 - 1,000) on 1,000 players.
* **Key Finding:** The "Elevator Effect." Players climb slowly but suffer catastrophic vertical drops when they hit the table limit. The survival rate drops significantly as more Zeros are added to the wheel.

---

## 📂 Project Structure

The project is designed with a modular Object-Oriented architecture:

```text
roulette_project/
│
├── components/                  # Core Simulation Engine
│   ├── roulette_wheel.py        # Logic for 3 wheel types
│   ├── player.py                # Betting strategies (Flat/Martingale)
│   └── game.py                  # Game engine & rule enforcement
│
├── utils/                       # Shared Utilities
│   ├── monte_carlo_helpers.py   # Plotting & Analysis tools
│   └── strategy_helpers.py      # Comparison tools
│
├── experiment_house_edge/             # Exp 1: Math Verification
├── experiment_strategies/             # Exp 2: Strategy Comparison
├── experiment_monte_carlo_flat/       # Exp 3: Variance Analysis
└── experiment_monte_carlo_martingale/ # Exp 4: Table Limits
````

-----

## 🚀 How to Run

### Prerequisites

You need Python 3 installed along with the following scientific libraries:

```bash
pip install numpy matplotlib
```

### Running the Experiments

**1. Verify the House Edge:**

```bash
python3 experiment_house_edge/exp_house_edge_comparison.py
```

**2. Compare Strategies (Infinite Money):**

```bash
python3 experiment_strategies/exp_strategies_european.py
```

**3. Analyze Risk (Flat Betting Monte Carlo):**

```bash
python3 experiment_monte_carlo_flat/exp_mc_flat_european.py
```

**4. Test Survival (Martingale with Limits):**

```bash
python3 experiment_monte_carlo_martingale/exp_mc_mart_comparison.py
```

*Note: All plots are automatically saved in a `plots/` subfolder within each experiment directory.*

-----

## 📊 Key Takeaways

1.  **The Zero is the Tax:** The House Edge is unavoidable. Adding zeros (American/Triple) drastically accelerates player ruin.
2.  **Martingale is a Trap:** It trades frequent small wins for rare, catastrophic losses.
3.  **Table Limits Kill Strategies:** Casinos use table limits specifically to break progressive betting systems like Martingale.
4.  **Variance \!= Profit:** Changing your bet type (Color vs. Number) changes the volatility of your ride, but the destination (Expected Loss) remains exactly the same.

-----

### 👤 Author

Developed by **Elena Cancho González** as a study on probability, simulation, and data analysis. Final project for ADA511: Data science and AI-prototyping 

