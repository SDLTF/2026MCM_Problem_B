import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
def get_alpha(t):
    t_diff = t - 2050
    # 简化版衰减公式
    downtime = (0.833 * 1.015**t_diff) * (14 * 0.995**t_diff) + 18.25
    return max(0, 1 - downtime/365)
# --- 图片 4: 柱状图 ---
plt.figure(figsize=(8, 5))
scenarios = ['Pure Rocket\n(20Y)', 'Hybrid Optimal\n(60Y)', 'Pure Elevator\n(100Y)']
emissions = [250, 177, 0] # Million MT
bars = plt.bar(scenarios, emissions, color=['#d62728', '#1f77b4', '#2ca02c'], edgecolor='k')

plt.title('Environmental Impact Comparison')
plt.ylabel('Emissions (Million MT $CO_2e$)')
plt.annotate('Savings: -29.2%', xy=(1, 177), xytext=(1.5, 220),
             arrowprops=dict(facecolor='black', arrowstyle='->'),
             bbox=dict(boxstyle="round", fc="white"))
for bar in bars:
    plt.text(bar.get_x()+bar.get_width()/2, bar.get_height()+5, f"{int(bar.get_height())}", ha='center')
plt.savefig('environmental_impact.png', dpi=300)
plt.show()

# --- 图片 5: L形曲线 ---
# 假设电梯每年扩容 4%
def get_expanded_capacity(t):
    base = 537_000 * get_alpha(2050 + t) # 复用上面的 get_alpha
    return base * (1.04 ** t)

durations = range(20, 100)
l_curve_data = []
for T in durations:
    demand = 1e8 / T
    rocket_cargo = 0
    for i in range(T):
        cap = get_expanded_capacity(i)
        rocket_cargo += max(0, demand - cap)
    l_curve_data.append(rocket_cargo * 2.5 / 1e6)

plt.figure(figsize=(10, 6))
plt.plot(durations, l_curve_data, 'r-', linewidth=3, label='With Capacity Expansion')
plt.plot(60, l_curve_data[40], 'bo', markersize=10) # 60年点
plt.annotate('Knee Point (60Y)', xy=(60, l_curve_data[40]), xytext=(70, l_curve_data[40]+50),
             arrowprops=dict(facecolor='black', shrink=0.05),
             bbox=dict(boxstyle="round", fc="white"))
plt.title('The True L-Curve: Environment vs Time')
plt.xlabel('Duration (Years)')
plt.ylabel('Emissions (Million MT)')
plt.grid(True, alpha=0.3)
plt.savefig('true_l_curve.png', dpi=300)
plt.show()