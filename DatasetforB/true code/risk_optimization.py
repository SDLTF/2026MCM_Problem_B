import numpy as np
import matplotlib.pyplot as plt
def get_alpha(t):
    t_diff = t - 2050
    # 简化版衰减公式
    downtime = (0.833 * 1.015**t_diff) * (14 * 0.995**t_diff) + 18.25
    return max(0, 1 - downtime/365)
# 蒙特卡洛参数
N_SIMS = 1000
TARGET = 1e8
START_YR = 2050

def run_mc(n_sites):
    results = []
    for _ in range(N_SIMS):
        rem = TARGET
        yr = 0
        while rem > 0:
            # 随机天气 (均值 0.16, 波动 0.05)
            weather = max(0, np.random.normal(0.16, 0.05))
            # 随机电梯 (均值 alpha, 波动 0.05)
            alpha_base = get_alpha(START_YR + yr)
            alpha = max(0, np.random.normal(alpha_base, 0.05))
            
            # 计算运力
            cap_e = 537_000 * alpha
            # 火箭能力: 400次/年 * (1-天气) * 150吨 * 基地数
            cap_r = 400 * (1 - weather) * 150 * n_sites
            
            # 假设全力运输
            rem -= (cap_e + cap_r)
            yr += 1
            if yr > 150: break
        results.append(yr)
    return results

# 运行模拟
res_10 = run_mc(10)
res_25 = run_mc(25)

# 绘图
plt.figure(figsize=(10, 6))
plt.hist(res_10, bins=30, alpha=0.6, color='r', density=True, label='10 Sites (Baseline)')
plt.hist(res_25, bins=30, alpha=0.6, color='g', density=True, label='25 Sites (Optimized)')

# 标注均值
plt.axvline(np.mean(res_10), color='darkred', linestyle='--', label=f'Mean: {np.mean(res_10):.1f} Yrs')
plt.axvline(np.mean(res_25), color='darkgreen', linestyle='--', label=f'Mean: {np.mean(res_25):.1f} Yrs')
plt.axvline(60, color='k', linewidth=2, label='Target (60 Yrs)')

plt.xlabel('Completion Time (Years)')
plt.ylabel('Probability Density')
plt.title('Risk Analysis & Infrastructure Optimization')
plt.legend()
plt.savefig('risk_optimization.png', dpi=300)
plt.show()