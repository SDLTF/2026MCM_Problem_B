import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------
# Part 1: Cost Learning Curve & Sensitivity Analysis
# ---------------------------------------------------------
def calculate_cost_curve(years, total_mass, lr):
    # Parameters
    payload = 150 # MT
    c_initial = 40_000_000 # $40M
    c_floor = 2_000_000    # $2M
    b = np.log2(lr)
    
    # Simple simulation of cumulative launches
    total_launches = total_mass / payload
    launches_per_year = total_launches / years
    
    cumulative = 0
    total_cost = 0
    
    # Integrate cost
    # Approximate by batches
    batches = 100
    batch_size = total_launches / batches
    
    for i in range(batches):
        n_mid = cumulative + batch_size/2
        unit_cost = max(c_floor, c_initial * (n_mid ** b))
        total_cost += unit_cost * batch_size
        cumulative += batch_size
        
    return total_cost

# Plotting Sensitivity
years_range = np.arange(20, 101, 5)
lrs = [0.80, 0.85, 0.90, 0.95]
results = {lr: [] for lr in lrs}

for y in years_range:
    # Assume 67% of cargo goes by Rocket (Hybrid Scenario)
    rocket_cargo = 100_000_000 * 0.67 
    for lr in lrs:
        cost = calculate_cost_curve(y, rocket_cargo, lr)
        # Add fixed Elevator cost (approx $3T for 60 years)
        # Simplified for visualization trend
        total = cost + (3e12 * (y/60)) 
        results[lr].append(total / 1e12) # Trillions

plt.figure(figsize=(14, 5))

# Subplot 1: Sensitivity Analysis
plt.subplot(1, 2, 1)
colors = ['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728']
for i, lr in enumerate(lrs):
    plt.plot(years_range, results[lr], color=colors[i], linewidth=2.5, label=f'LR = {int(lr*100)}%')

plt.title('Sensitivity Analysis: Total Cost vs. Learning Rate', fontsize=12)
plt.xlabel('Project Duration (Years)', fontsize=10)
plt.ylabel('Total Cost (Trillion USD)', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.axvline(60, color='gray', linestyle=':', alpha=0.8)

# ---------------------------------------------------------
# Part 2: Wait/Risk Monte Carlo Analysis
# ---------------------------------------------------------
# Stochastic Params
n_sims = 1000
target_years = 60
base_capacity = 1.66e6 # MT/yr needed (100M / 60)

sim_years = []

for _ in range(n_sims):
    cargo_rem = 100_000_000
    year = 0
    while cargo_rem > 0:
        year += 1
        # Random disruptions
        # Elevator: Debris (Poisson) -> Downtime
        events = np.random.poisson(0.833)
        down_days = events * np.random.normal(14, 3) + (365*0.05)
        alpha_sim = max(0, 1 - down_days/365)
        
        # Rocket: Weather (Normal)
        beta_weather_sim = 1 - max(0.05, np.random.normal(0.16, 0.05))
        
        # Capacity this year
        # Elevator: 537k * alpha
        cap_e = 537_000 * alpha_sim
        
        # Rocket: Max capacity constraints (Launchpad Limit)
        # Assume mature pads: 400 launches/yr/site * 10 sites * 150T
        # But constrained by "Planned Schedule" + Weather
        # We can't use 100% of theoretical max, only what was planned/prepped
        # "Bottleneck": Real output = Planned * Beta
        planned_r = (base_capacity - 537_000) # Base plan
        real_r = planned_r * beta_weather_sim
        
        # Total Realized
        total_lift = cap_e + real_r
        
        # "Catch up" logic: Can we surge?
        # Assume max surge is +10% of planned
        if total_lift < base_capacity:
             # We fell behind. Next year we try harder?
             # But here we just count how long it takes at this rate.
             pass
        
        cargo_rem -= total_lift

    sim_years.append(year)

# Subplot 2: Risk Histogram
plt.subplot(1, 2, 2)
plt.hist(sim_years, bins=20, color='#d62728', alpha=0.7, edgecolor='black')
plt.axvline(60, color='g', linewidth=3, label='Target (60 Yrs)')
plt.axvline(np.mean(sim_years), color='k', linestyle='--', linewidth=2, label=f'Real Mean ({int(np.mean(sim_years))} Yrs)')
plt.title('Risk Analysis: Actual Completion Time Distribution', fontsize=12)
plt.xlabel('Years to Complete', fontsize=10)
plt.ylabel('Frequency', fontsize=10)
plt.legend()
plt.grid(axis='y', alpha=0.5)

plt.tight_layout()
plt.savefig('refinement_analysis.png')
plt.show()