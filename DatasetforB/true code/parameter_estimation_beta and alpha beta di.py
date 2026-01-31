import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 定义核心函数
# ==========================================
def get_alpha(t):
    # 电梯效率衰减 (碎片模型)
    t_diff = np.array(t) - 2050
    lambda_t = 0.833 * (1 + 0.015)**t_diff
    repair_t = 14 * (1 - 0.005)**t_diff
    downtime = lambda_t * repair_t + (365 * 0.05)
    return np.maximum(0, 1 - (downtime / 365))

def get_beta_logistic(t):
    # 火箭发射频次 (S型增长)
    return 400 / (1 + np.exp(-0.15 * (t - 2030)))

def get_rocket_cost_curve(n):
    # 莱特学习曲线
    # 初始: $3.75亿, 底线: $1000万
    n_safe = np.maximum(1, n)
    cost = 375 * (n_safe ** np.log2(0.85))
    return np.maximum(10, cost)

# ==========================================
# 2. 绘图 1: 参数估计图
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 子图1: Beta S型曲线
years = np.arange(2020, 2060)
ax1.plot(years, get_beta_logistic(years), 'b-', linewidth=2, label='Forecast')
ax1.scatter([2020, 2022, 2024], [26, 61, 100], color='k', s=20, label='Historical Data')
ax1.set_title(r'Rocket Cadence ($\beta(t)$): Logistic Growth')
ax1.set_xlabel('Year')
ax1.set_ylabel('Launches per Site per Year')
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend()

# 子图2: 成本学习曲线
launches = np.logspace(0, 5, 100)
ax2.semilogx(launches, get_rocket_cost_curve(launches), 'g-', linewidth=2)
ax2.axhline(10, color='r', linestyle='--', label='Physical Floor ($10M)')
ax2.set_title(r'Rocket Cost Learning Curve ($C_R(n)$)')
ax2.set_xlabel('Cumulative Launches (Log Scale)')
ax2.set_ylabel('Cost per Launch ($ Million)')
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend()

plt.tight_layout()
plt.savefig('parameter_estimation_beta.png', dpi=300)
plt.show()

# ==========================================
# 3. 绘图 2: 趋势背离图
# ==========================================
fig, ax1 = plt.subplots(figsize=(10, 6))
years_long = np.arange(2050, 2120)

color = 'tab:red'
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel(r'Elevator Efficiency ($\alpha$)', color=color, fontsize=12)
ax1.plot(years_long, get_alpha(years_long), color=color, linewidth=3, label='Elevator Decay')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim(0, 1.05)

ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel(r'Rocket Cadence Capacity ($\beta$)', color=color, fontsize=12)
ax2.plot(years_long, get_beta_logistic(years_long), color=color, linewidth=3, label='Rocket Maturity')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(350, 410) # 放大显示后期平稳区

plt.title('The Complementary Contradiction: Diverging Trends', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.3)
plt.savefig('alpha_beta_divergence.png', dpi=300)
plt.show()