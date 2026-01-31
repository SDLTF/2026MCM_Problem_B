import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 参数设置
M_TOTAL = 100_000_000
START_YEAR = 2050
KE_NOMINAL = 537_000
COST_R_INIT = 375_000_000
COST_R_FLOOR = 10_000_000
INFRA_COST = 75_000_000_000 # $75B
CARBON_TAX = 150 
EMISSION_FACTOR = 2.5

def get_alpha(t):
    t_diff = t - 2050
    # 简化版衰减公式
    downtime = (0.833 * 1.015**t_diff) * (14 * 0.995**t_diff) + 18.25
    return max(0, 1 - downtime/365)

def get_rocket_cost(n_start, n_new):
    if n_new <= 0: return 0
    n_mid = n_start + n_new/2
    unit_cost = max(COST_R_FLOOR, COST_R_INIT * (n_mid ** np.log2(0.85)))
    return n_new * unit_cost

durations = range(20, 125, 5)
results = []

for T in durations:
    total_fin = INFRA_COST
    n_launches = 0
    total_rocket_cargo = 0
    demand = M_TOTAL / T
    
    for i in range(T):
        yr = START_YEAR + i
        cap_e = KE_NOMINAL * get_alpha(yr)
        cargo_e = min(demand, cap_e)
        cargo_r = max(0, demand - cargo_e)
        
        launches = cargo_r / 150
        cost_r = get_rocket_cost(n_launches, launches)
        cost_e = cargo_e * 220_000
        
        total_fin += (cost_e + cost_r)
        n_launches += launches
        total_rocket_cargo += cargo_r
        
    green_cost = total_fin + (total_rocket_cargo * EMISSION_FACTOR * CARBON_TAX)
    results.append({'T': T, 'Fin': total_fin/1e12, 'Green': green_cost/1e12})

df = pd.DataFrame(results)

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(df['T'], df['Fin'], 'b-o', label='Financial Cost', linewidth=2)
plt.plot(df['T'], df['Green'], 'g--s', label='With Carbon Tax', linewidth=2)

# 标注最优
best = df.loc[df['Green'].idxmin()]
plt.annotate(f"Optimum: ~{int(best['T'])} Years\n${best['Green']:.1f}T", 
             xy=(best['T'], best['Green']), xytext=(best['T']+10, best['Green']+5),
             arrowprops=dict(facecolor='black', shrink=0.05),
             bbox=dict(boxstyle="round", fc="#e6f2ff", ec="blue"))

plt.title('Cost Optimization Analysis (Calibrated)', fontsize=14)
plt.xlabel('Project Duration (Years)')
plt.ylabel('Total Cost (Trillion USD)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('cost_env_optimization_v2.png', dpi=300)
plt.show()