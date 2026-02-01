import numpy as np
import matplotlib.pyplot as plt

# Simulate Window Quota Optimization
windows = np.arange(1, 13) # 12 windows (~1 year)
q_env = 3.0 # Environmental threshold
target_base = 2.5 # Normal target

# Weights (wc: logistics, we: environment)
# Scenario 1: Steady State
q_steady = np.full_like(windows, 2.6, dtype=float) + np.random.normal(0, 0.1, len(windows))

# Scenario 2: Recovery (Elevator failure at window 4)
q_recovery = np.copy(q_steady)
q_recovery[4:] = 0 # Initial drop in elevator part (handled by total flow)
# Surge response: wc increases, allowing Qk > Qenv
# Surge starts at window 5
q_recovery[4:9] = np.array([4.2, 4.8, 4.5, 3.8, 3.2]) # Pulse超频
q_recovery[9:] = target_base + 0.2

# Logistics Deficit (Backlog)
backlog = np.zeros_like(windows, dtype=float)
deficit = 0
for i in range(len(windows)):
    if i == 4: # Fail
        deficit += 3.0 # Accumulated loss
    if i >= 4:
        # Net change = target - supply
        # If Q_recovery[i] > target_base, we reduce deficit
        net = q_recovery[i] - target_base
        deficit -= net
    backlog[i] = max(0, deficit)

# Plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# Plot 1: Quota Optimization
ax1.step(windows, q_steady, where='mid', label='Steady State Allocation (w_e > w_c)', color='#2878B5', alpha=0.6, linestyle='--')
ax1.step(windows, q_recovery, where='mid', label='Adaptive Surge Recovery (w_c > w_e)', color='#C82423', linewidth=2)
ax1.axhline(q_env, color='gray', linestyle=':', label='Environmental Self-cleaning Threshold ($Q_{env}$)')

ax1.fill_between(windows, q_env, q_recovery, where=(q_recovery > q_env), color='#C82423', alpha=0.2, step='mid', label='Environmental Debt (Overshoot)')

ax1.set_title('Section 6.1.3: Window Quota Optimization & Penalty Trade-off', fontsize=14, fontweight='bold')
ax1.set_ylabel('Launch Quota $Q_k$ (MT/Window)', fontsize=12)
ax1.legend(loc='upper right', frameon=True)
ax1.grid(True, alpha=0.3)

# Plot 2: Logistics Deficit (Backlog)
ax2.bar(windows, backlog, color='#FFBB44', alpha=0.7, label='Logistics Backlog (Supply Deficit)')
ax2.set_title('Backlog Resolution through Adaptive Throttling', fontsize=14, fontweight='bold')
ax2.set_ylabel('Cumulative Backlog (MT)', fontsize=12)
ax2.set_xlabel('Launch Window Index (k)', fontsize=12)
ax2.axvline(5, color='black', linestyle='--', alpha=0.5)
ax2.text(5.2, 2.5, 'Emergency Surge Triggered', fontsize=10, fontweight='bold')

ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('window_quota_optimization.png', dpi=300)
plt.show()