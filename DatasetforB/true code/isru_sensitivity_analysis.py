import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. 仿真函数：计算不同 ISRU 水平下的表现
# ==========================================
def simulate_isru_scenario(gamma_max, T=60):
    # 基础参数
    M_TOTAL = 1e8
    KE_NOMINAL = 537_000
    COST_E = 220_000
    annual_base_demand = M_TOTAL / T
    
    total_cost = 75e9 # 初始基建
    total_launches = 0
    costs_history = []
    demand_history = []

    for i in range(T):
        # 计算第 i 年的自给率 (Logistic Growth)
        gamma = gamma_max / (1 + np.exp(-0.12 * (i - 25)))
        net_demand = annual_base_demand * (1 - gamma)
        
        # 模拟电梯衰减
        alpha = max(0, 1 - ((0.833 * 1.015**i * 14 * 0.995**i + 18)/365))
        cap_e = KE_NOMINAL * alpha
        
        # 分配运量
        cargo_e = min(net_demand, cap_e)
        cargo_r = max(0, net_demand - cargo_e)
        
        # 计算火箭学习成本
        launches = cargo_r / 150
        n_mid = total_launches + (launches / 2)
        unit_cost = max(10e6, 375e6 * (max(1, n_mid)**np.log2(0.85)))
        
        total_cost += (cargo_e * COST_E + launches * unit_cost)
        total_launches += launches
        
        costs_history.append(total_cost / 1e12) # Trillion
        demand_history.append(net_demand / 1e6) # Million MT
        
    return costs_history, demand_history

# ==========================================
# 2. 执行对比并绘图
# ==========================================
# 运行 50% vs 20%
c50, d50 = simulate_isru_scenario(0.5)
c20, d20 = simulate_isru_scenario(0.2)
years = np.arange(2050, 2110)

plt.figure(figsize=(12, 5))

# 子图 1: 运输需求
plt.subplot(1, 2, 1)
plt.plot(years, d50, 'g-', label='Scenario A: 50% ISRU')
plt.plot(years, d20, 'r--', label='Scenario B: 20% ISRU')
plt.title('Earth-to-Moon Demand Comparison')
plt.ylabel('Million MT / Year')
plt.legend()
plt.grid(True, alpha=0.3)

# 子图 2: 累计成本
plt.subplot(1, 2, 2)
plt.plot(years, c50, 'g-', label='50% ISRU (Optimistic)')
plt.plot(years, c20, 'r--', label='20% ISRU (Bottleneck)')
plt.title('Cumulative Financial Impact')
plt.ylabel('Trillion USD')
gap = c20[-1] - c50[-1]
plt.annotate(f'Gap: ${gap:.2f}T', xy=(2110, c20[-1]), xytext=(2085, c20[-1]+1),
             arrowprops=dict(arrowstyle='->'))
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('isru_sensitivity_analysis.png')