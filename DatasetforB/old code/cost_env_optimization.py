import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ==========================================
# 1. 核心参数与函数 (与之前保持一致)
# ==========================================
M_TOTAL = 100_000_000
START_YEAR = 2050
KE_NOMINAL = 537_000
PAYLOAD = 150
EMISSION_FACTOR = 2.5 # MT CO2e / MT Payload

def get_alpha(t):
    # 简化的 alpha 衰减 (碎片影响)
    baseline_lambda = 0.833
    baseline_repair = 14
    growth_debris = 0.015
    improve_repair = 0.005
    lambda_t = baseline_lambda * (1 + growth_debris)**(t - 2050)
    repair_t = baseline_repair * (1 - improve_repair)**(t - 2050)
    downtime = lambda_t * repair_t + (365 * 0.05)
    return max(0, 1 - (downtime / 365))

# ==========================================
# 2. 模拟全范围数据 (20年 到 120年)
# ==========================================
durations = range(20, 125, 5) # 每5年一个点
emissions_list = []
durations_list = []

for T in durations:
    annual_demand = M_TOTAL / T
    total_rocket_cargo = 0
    
    for i in range(T):
        year = START_YEAR + i
        cap_e = KE_NOMINAL * get_alpha(year)
        cargo_e = min(annual_demand, cap_e)
        cargo_r = max(0, annual_demand - cargo_e)
        total_rocket_cargo += cargo_r
        
    total_emissions = total_rocket_cargo * EMISSION_FACTOR / 1e6 # 换算为 Million MT
    emissions_list.append(total_emissions)
    durations_list.append(T)

# ==========================================
# 3. 绘制 L 形曲线 (Pareto Frontier)
# ==========================================
plt.figure(figsize=(10, 6))

# 绘制曲线
plt.plot(durations_list, emissions_list, 'o-', color='#d62728', linewidth=2, markersize=8, label='Trade-off Curve')

# 标注关键点
# 20年 (高污染)
plt.annotate(f'Pure Rocket (20Y)\n{int(emissions_list[0])}M MT $CO_2e$', 
             xy=(20, emissions_list[0]), xytext=(30, emissions_list[0]),
             arrowprops=dict(facecolor='black', arrowstyle='->'))

# 60年 (推荐点)
idx_60 = durations_list.index(60)
plt.plot(60, emissions_list[idx_60], 's', color='blue', markersize=12, label='Recommended (60Y)')
plt.annotate(f'Hybrid Optimal (60Y)\n{int(emissions_list[idx_60])}M MT', 
             xy=(60, emissions_list[idx_60]), xytext=(65, emissions_list[idx_60]+40),
             arrowprops=dict(facecolor='black', arrowstyle='->'),
             bbox=dict(boxstyle="round,pad=0.3", fc="#e6f2ff", ec="blue", lw=1))

# 100年 (低污染)
plt.annotate(f'Pure Elevator\nNear Zero', 
             xy=(100, 5), xytext=(90, 40),
             arrowprops=dict(facecolor='black', arrowstyle='->'))

# 装饰
plt.title('The "L-Curve": Trade-off between Project Duration and Emissions', fontsize=14)
plt.xlabel('Project Duration (Years)', fontsize=12)
plt.ylabel('Cumulative Emissions (Million MT $CO_2e$)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

# 填充区域表示"不可接受区"
plt.fill_between(durations_list, emissions_list, color='red', alpha=0.05)

plt.tight_layout()
plt.savefig('environmental_tradeoff_curve.png', dpi=300)
plt.show()