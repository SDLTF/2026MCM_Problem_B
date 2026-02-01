import numpy as np
import matplotlib.pyplot as plt

# 1. 参数设定
cumulative_mass = np.linspace(1, 100, 500)  # 累计运输量 (百万吨)
time_frames = [20, 40, 60, 80, 100]        # 不同工期方案

# 2. 莱特定律导致的单位成本下降 (Wright's Law)
f = 0.85  # 学习率
b = -np.log2(f)
c_initial = 500  # 初始单价 ($/kg)
unit_cost_learning = c_initial * (cumulative_mass)**(-b)

# 3. 环境惩罚成本 (随工期缩短而剧增)
# 工期越短，年均发射频率越高，环境惩罚 p=2
def env_penalty(duration):
    frequency = 100 / duration # 简化为：总量/工期
    return 20 * (frequency**2.2)

# 计算不同工期下的综合单价
total_costs = []
for d in time_frames:
    penalty = env_penalty(d)
    total_costs.append(unit_cost_learning + penalty)

# --- 绘图 ---
plt.figure(figsize=(10, 6), dpi=150)
plt.plot(cumulative_mass, unit_cost_learning, 'k--', label="Learning Curve (Wright's Law)", linewidth=2)

colors = plt.cm.RdYlGn(np.linspace(0, 1, len(time_frames)))
for i, d in enumerate(time_frames):
    plt.plot(cumulative_mass, total_costs[i], label=f'Total Cost ({d}-Year Plan)', color=colors[i], linewidth=1.5)

# 标注：帕累托前沿
plt.annotate('Environmental Penalty Overcomes\nLearning Dividends (Short Durations)', 
             xy=(40, 350), xytext=(50, 450),
             arrowprops=dict(facecolor='black', shrink=0.05), fontsize=9)

plt.title('Section 3.2: Economic Dynamics - Learning Dividends vs. Environmental Penalty', fontsize=13, fontweight='bold')
plt.xlabel('Cumulative Transported Mass (Million Tons)', fontsize=11)
plt.ylabel('Effective Unit Cost ($/kg)', fontsize=11)
plt.legend(title="Duration Scenarios", loc='upper right')
plt.grid(True, alpha=0.3)
plt.ylim(0, 600)

plt.tight_layout()
plt.savefig('cost_dynamics_intersection.png')
plt.show()