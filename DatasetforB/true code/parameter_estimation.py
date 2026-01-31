import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# --- 1. 准备历史数据 (SpaceX History) ---
# 年份
years_hist = np.array([2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])
# 年发射总次数
launches_hist = np.array([2, 3, 6, 7, 9, 18, 21, 13, 26, 31, 61, 96, 138])
# 假设活跃发射场数量 (用于计算单场效率)
active_sites = 3
cadence_hist = launches_hist / active_sites

# --- 2. 定义回归模型 ---
# Logistic Growth for Cadence (S型增长)
def logistic_model(t, L, k, t0):
    return L / (1 + np.exp(-k * (t - t0)))

# Exponential Decay for Failure Rate (可靠性增长)
def reliability_model(t, a, b):
    # Base failure rate decays over time
    return 1 - a * np.exp(-b * (t - 2010))

# --- 3. 执行回归拟合 ---
# 拟合发射频率
popt_cadence, _ = curve_fit(logistic_model, years_hist, cadence_hist, 
                            bounds=([50, 0.1, 2015], [500, 1.0, 2035]))

# 拟合可靠性 (使用合成的行业趋势数据)
years_rel = np.array([2010, 2015, 2018, 2021, 2024])
rel_data = np.array([0.90, 0.94, 0.97, 0.99, 0.995]) # 成功率
popt_rel, _ = curve_fit(reliability_model, years_rel, rel_data,
                        bounds=([0.01, 0.01], [0.5, 0.5]))

# --- 4. 生成预测数据 ---
future_years = np.arange(2012, 2100)
pred_cadence = logistic_model(future_years, *popt_cadence)
pred_reliability = reliability_model(future_years, *popt_rel)

# --- 5. 绘图 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 图1: 发射频率预测
ax1.scatter(years_hist, cadence_hist, color='black', label='Historical Data (SpaceX)', zorder=5)
ax1.plot(future_years, pred_cadence, color='#1f77b4', linewidth=3, label='Logistic Regression Prediction')
ax1.axvline(2050, color='r', linestyle='--', alpha=0.8, label='Project Start (2050)')
ax1.set_title('Estimation of Rocket Launch Cadence (beta_cadence)', fontsize=14)
ax1.set_ylabel('Launches per Site per Year', fontsize=12)
ax1.set_xlabel('Year', fontsize=12)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend()
# 标注 2050 年的值
val_2050 = logistic_model(2050, *popt_cadence)
ax1.annotate(f'2050 Capacity:\n~{int(val_2050)} launches/yr', (2050, val_2050), 
             xytext=(2015, val_2050+50), arrowprops=dict(arrowstyle='->', color='black'))

# 图2: 可靠性预测
ax2.scatter(years_rel, rel_data, color='black', label='Historical Trend')
ax2.plot(future_years, pred_reliability, color='#2ca02c', linewidth=3, label='Reliability Growth Curve')
ax2.axvline(2050, color='r', linestyle='--', alpha=0.8)
ax2.set_title('Estimation of Vehicle Reliability (beta_reliability)', fontsize=14)
ax2.set_ylabel('Mission Success Rate', fontsize=12)
ax2.set_xlabel('Year', fontsize=12)
ax2.set_ylim(0.90, 1.01)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(loc='lower right')
# 标注 2050 年的值
val_rel_2050 = reliability_model(2050, *popt_rel)
ax2.annotate(f'2050 Reliability:\n{val_rel_2050:.4f}', (2050, val_rel_2050), 
             xytext=(2020, 0.96), arrowprops=dict(arrowstyle='->', color='black'))

plt.tight_layout()
plt.savefig('parameter_estimation_beta.png', dpi=300)
plt.show()