import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------
# 1. 准备数据
# ---------------------------------------------------------
years = np.array([30, 40, 50, 60, 70, 80, 100])

# 简化的模拟结果 (基于之前的 Simulation)
# 假设:
# - 短工期(30年) -> 90% 火箭 -> 高成本 + 高排放
# - 中工期(60年) -> 70% 火箭 -> 中成本 + 中排放
# - 长工期(100年)-> 50% 火箭 -> 低成本 + 低排放

# 基础金融成本 (Financial Cost) - $Trillion (近似值)
# 之前的模拟数据: 30年$56T, 60年$23T, 100年$10T
costs_financial = np.array([56.7, 40.0, 30.0, 23.3, 18.5, 15.0, 10.0])

# 对应的火箭运输比例 (Rocket Share)
rocket_shares = np.array([0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.50])
total_cargo = 100_000_000 # MT

# 计算排放量 (Emissions)
# 排放因子 = 2.5 MT CO2e / MT Payload
emissions_mt = total_cargo * rocket_shares * 2.5 # MT CO2e

# ---------------------------------------------------------
# 2. 引入碳税场景
# ---------------------------------------------------------
# 场景 1: 无视环境 (Tax = $0)
total_cost_scenario_1 = costs_financial

# 场景 2: 激进环保 (Tax = $500/MT CO2e)
# 这是一个很高的碳税，用于测试模型敏感度
tax_rate = 500 # $/MT
# 换算为万亿: 排放量(MT) * 税率($/MT) / 10^12
cost_environmental = (emissions_mt * tax_rate) / 1e12
total_cost_scenario_2 = costs_financial + cost_environmental

# ---------------------------------------------------------
# 3. 绘图对比
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))

# 绘制成本曲线
plt.plot(years, total_cost_scenario_1, 'bo-', linewidth=2, label='Baseline (No Carbon Tax)')
plt.plot(years, total_cost_scenario_2, 'go--', linewidth=2, label='Green Policy (Tax = $500/MT)')

# 标注差异
diff_30 = total_cost_scenario_2[0] - total_cost_scenario_1[0]
diff_100 = total_cost_scenario_2[-1] - total_cost_scenario_1[-1]

plt.annotate(f'Tax Penalty: +${diff_30:.1f}T\n(Heavy Rocket Use)', 
             xy=(30, total_cost_scenario_2[0]), xytext=(35, total_cost_scenario_2[0]+5),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.annotate(f'Tax Penalty: +${diff_100:.1f}T\n(Low Rocket Use)', 
             xy=(100, total_cost_scenario_2[-1]), xytext=(80, total_cost_scenario_2[-1]+5),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.title('Impact of Environmental Factors on Total Project Cost', fontsize=14)
plt.xlabel('Project Duration (Years)', fontsize=12)
plt.ylabel('Total Cost (Trillion USD)', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('env_impact_on_model.png')
plt.show()