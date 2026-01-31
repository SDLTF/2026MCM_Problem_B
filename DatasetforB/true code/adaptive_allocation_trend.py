import numpy as np
import matplotlib.pyplot as plt

# 模拟参数
years = np.linspace(0, 100, 100)
# 1. 电梯性能随时间衰减 (指数衰减)
alpha = 1.0 * np.exp(-0.015 * years) 
# 2. 火箭性能随时间增长 (S型曲线)
beta = 1 / (1 + np.exp(-0.1 * (years - 25)))
# 3. ISRU 贡献率 (平滑增长)
gamma = 0.5 / (1 + np.exp(-0.12 * (years - 50)))

# 计算动态权重 (使用加权倒数模拟成本优势)
# 简化逻辑：权重 = (性能因子) / (需求修正)
w_elevator = alpha * (1 - gamma)
w_rocket = beta

# 归一化比例
total_w = w_elevator + w_rocket
share_elevator = w_elevator / total_w
share_rocket = w_rocket / total_w

# 绘图
plt.figure(figsize=(12, 6))
plt.stackplot(years + 2050, share_elevator * 100, share_rocket * 100, 
              labels=['Space Elevator Share', 'Rocket Fleet Share'],
              colors=['#1f77b4', '#d62728'], alpha=0.7)

plt.title('Time-Varying Adaptive Allocation: Evolutionary Logistics Strategy', fontsize=14, pad=15)
plt.ylabel('Capacity Allocation (%)', fontsize=12)
plt.xlabel('Project Timeline (Year)', fontsize=12)
plt.xlim(2050, 2150)
plt.ylim(0, 100)

# 添加阶段标注
plt.axvline(2075, color='white', linestyle='--', alpha=0.5)
plt.text(2055, 50, 'Phase I:\nElevator Dominant', color='white', fontweight='bold')
plt.text(2080, 50, 'Phase II:\nRocket Transition', color='white', fontweight='bold')
plt.text(2120, 80, 'Phase III:\nISRU Maturation', color='black', fontweight='bold')

plt.legend(loc='lower left', frameon=True)
plt.grid(axis='y', linestyle=':', alpha=0.5)
plt.tight_layout()
plt.savefig('adaptive_allocation_trend.png', dpi=300)
plt.show()