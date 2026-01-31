import numpy as np
import matplotlib.pyplot as plt

# 1. 定义时间轴
years = np.arange(2050, 2151)

# 2. Alpha 模型 (太空电梯: 环境恶化主导)
# 参数源自 IAA 报告与 ESA 碎片模型
baseline_lambda = 0.833 # 初始撞击率 (次/年)
baseline_repair = 14    # 初始维修时间 (天)
growth_debris = 0.015   # 碎片年增长率 1.5%
improve_repair = 0.005  # 技术年进步率 0.5%

# 计算动态 Alpha
lambda_t = baseline_lambda * (1 + growth_debris)**(years - 2050)
repair_t = baseline_repair * (1 - improve_repair)**(years - 2050)
downtime = lambda_t * repair_t + (365 * 0.05) # +5% 常规维护
alpha_trend = 1 - (downtime / 365)

# 3. Beta 模型 (火箭: 技术成熟主导)
# 参数源自 SpaceX 历史数据回归 (指数衰减模型)
def reliability_forecast(t):
    # 故障率从 2010 年开始指数下降
    return 1 - 0.1 * np.exp(-0.15 * (t - 2010))

beta_trend = reliability_forecast(years)

# 4. 绘图
plt.figure(figsize=(10, 6))
plt.plot(years, alpha_trend, 'r-', linewidth=3, label='Elevator Efficiency alpha(t) (Degrading)')
plt.plot(years, beta_trend, 'g-', linewidth=3, label='Rocket Reliability beta(t) (Improving)')

plt.title('Divergent Trends: Environmental Degradation vs. Technological Maturation')
plt.xlabel('Year')
plt.ylabel('Efficiency Index')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.savefig('alpha_beta_divergence.png')