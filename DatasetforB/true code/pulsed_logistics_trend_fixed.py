import numpy as np
import matplotlib.pyplot as plt

# 1. 模拟宏观趋势 (2050 - 2150)
years_long = np.linspace(2050, 2150, 500)
# 电梯与火箭的基本份额演化逻辑
alpha = 1.0 * np.exp(-0.015 * (years_long - 2050))
beta = 1 / (1 + np.exp(-0.1 * (years_long - 2050 - 25)))
total = alpha + beta
share_e_long = alpha / total
share_r_long = beta / total

# 2. 模拟微观脉冲 (选取 2070-2071 年作为典型展示)
years_micro = np.linspace(2070, 2071, 1500)
window_period = 28 / 365.25  # 约28天一个发射窗口
window_width = 3 / 365.25    # 假设窗口持续3天

# 太空电梯流量 (Base Load)
e_flow = 0.4 * np.ones_like(years_micro)

# 火箭流量 (Pulse Load): 模拟离散轨道窗口
r_flow = np.zeros_like(years_micro)
for i in range(14):
    center = 2070.05 + i * window_period
    # 使用更窄的高斯函数模拟脉冲
    r_flow += 3.5 * np.exp(-((years_micro - center)**2) / (2 * (window_width/2.5)**2))

# --- 开始绘图 ---
fig = plt.figure(figsize=(12, 9), dpi=200)

# 子图 1: 宏观趋势分析 (100年视角)
ax1 = plt.subplot2grid((2, 1), (0, 0))
ax1.stackplot(years_long, share_e_long * 100, share_r_long * 100, 
              labels=['Space Elevator (Base Load)', 'Rocket Fleet (Pulse Load)'],
              colors=['#2878B5', '#C82423'], alpha=0.7)
ax1.set_title('Macro-Scale: Adaptive Capacity Allocation (2050-2150)', fontsize=15, fontweight='bold', pad=12)
ax1.set_ylabel('Allocation Percentage (%)', fontsize=12)
ax1.set_xlim(2050, 2150)
ax1.set_ylim(0, 100)
ax1.legend(loc='upper right', frameon=True, fontsize=10)
ax1.grid(True, linestyle='--', alpha=0.5)

# 子图 2: 微观窗口分析 (1年脉冲细节)
ax2 = plt.subplot2grid((2, 1), (1, 0))
ax2.fill_between(years_micro, e_flow, color='#2878B5', alpha=0.3, label='Continuous Elevator Supply')
ax2.plot(years_micro, e_flow + r_flow, color='#C82423', linewidth=1.2, label='Total Dynamic Logistics Flow')
ax2.fill_between(years_micro, e_flow, e_flow + r_flow, color='#C82423', alpha=0.2)

ax2.set_title('Micro-Scale: Pulsed Logistics & Orbital Windows (Discrete Constraints)', fontsize=15, fontweight='bold', pad=12)
ax2.set_xlabel('Project Timeline (Year)', fontsize=12)
ax2.set_ylabel('Instantaneous Throughput (MT/Day)', fontsize=12)
ax2.set_xlim(2070, 2071)
ax2.set_ylim(0, 5.5) # 提高上限，给标注留出空间
ax2.legend(loc='upper right', frameon=True, fontsize=10)
ax2.grid(True, linestyle='--', alpha=0.5)

# --- 重新设计的非重叠标注 ---

# 1. 峰值需求标注：移向右上方，并增加白色背景背景框
ax2.annotate('Peak Surge Demand\n(Requires 25 Launchpads)', 
             xy=(2070.36, 3.9), xytext=(2070.52, 4.6),
             arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=8),
             fontsize=11, fontweight='bold', 
             bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#C82423", alpha=0.9))

# 2. 稳定基准标注：移向左上方，避免与脉冲重叠
ax2.annotate('Steady Baseline Supply', 
             xy=(2070.15, 0.4), xytext=(2070.15, 2.5),
             arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=8),
             fontsize=11, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#2878B5", alpha=0.9))

plt.tight_layout(pad=3.0)
plt.savefig('pulsed_logistics_trend_fixed.png', bbox_inches='tight')
plt.show()