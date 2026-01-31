import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ==============================================================================
# 0. 全局参数设定 (Global Parameters)
# ==============================================================================
# 物资需求
M_TOTAL = 100_000_000   # 1亿吨
START_YEAR = 2050

# 太空电梯参数 (Space Elevator)
KE_NOMINAL = 537_000    # 年名义运力 (MT)
COST_E_PER_MT = 220_000 # $220/kg -> $220k/MT

# 火箭参数 (Rocket)
PAYLOAD = 150           # 单次载重 (MT)
COST_R_INIT_LAUNCH = 150_000_000 # 初始 $1.5亿/次
COST_R_FLOOR_LAUNCH = 2_000_000  # 底线 $200万/次
LEARNING_RATE = 0.85
B_EXPONENT = np.log2(LEARNING_RATE)

# 环境参数 (Environment)
EMISSION_FACTOR = 2.5   # 2.5 MT CO2e / MT Payload
CARBON_TAX = 150        # $150 / MT CO2e

# 绘图风格设置
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'

# ==============================================================================
# 1. 动态核心函数 (Dynamic Functions)
# ==============================================================================

def get_alpha(t):
    """太空电梯效率因子: 随碎片增长衰减"""
    # t 是绝对年份 (e.g., 2055)
    baseline_lambda = 0.833
    baseline_repair = 14
    growth_debris = 0.015
    improve_repair = 0.005
    
    lambda_t = baseline_lambda * (1 + growth_debris)**(t - 2050)
    repair_t = baseline_repair * (1 - improve_repair)**(t - 2050)
    
    downtime = lambda_t * repair_t + (365 * 0.05) # +5% 常规维护
    return max(0, 1 - (downtime / 365))

def get_beta_capacity(t, num_sites=10):
    """火箭物理运力上限 (MT/yr): S型增长"""
    # 假设单发射场饱和能力为 400次/年
    L = 400 
    k = 0.15
    t0 = 2030
    cadence = L / (1 + np.exp(-k * (t - t0)))
    return cadence * num_sites * PAYLOAD

def calculate_rocket_cost(n_start, n_new):
    """计算一批火箭发射的总成本 (Wright's Law积分近似)"""
    if n_new <= 0: return 0
    n_mid = n_start + (n_new / 2)
    unit_cost = max(COST_R_FLOOR_LAUNCH, COST_R_INIT_LAUNCH * (n_mid ** B_EXPONENT))
    return n_new * unit_cost

# ==============================================================================
# 2. Section 4.2 & 6.1: 经济最优与环境反馈 (Economic & Environmental)
# ==============================================================================
def run_deterministic_analysis():
    durations = range(20, 121, 5) # 模拟 20年 到 120年
    results = []

    for T in durations:
        # 重置累计变量
        total_financial_cost = 0
        total_launches = 0
        total_rocket_cargo = 0
        annual_demand = M_TOTAL / T
        
        # 逐年模拟
        for i in range(T):
            year = START_YEAR + i
            
            # 电梯优先
            alpha = get_alpha(year)
            cap_e = KE_NOMINAL * alpha
            cargo_e = min(annual_demand, cap_e)
            cost_e = cargo_e * COST_E_PER_MT
            
            # 火箭补充
            cargo_r = max(0, annual_demand - cargo_e)
            launches = cargo_r / PAYLOAD
            
            # 火箭成本 (学习曲线)
            cost_r = calculate_rocket_cost(total_launches, launches)
            
            # 更新累计
            total_financial_cost += (cost_e + cost_r)
            total_launches += launches
            total_rocket_cargo += cargo_r
            
        # 计算环境成本 (Section 6.1 Refinement)
        total_emissions = total_rocket_cargo * EMISSION_FACTOR # MT CO2e
        env_tax_cost = total_emissions * CARBON_TAX
        
        results.append({
            "Duration": T,
            "Financial_Cost": total_financial_cost / 1e12, # Trillion
            "Green_Cost": (total_financial_cost + env_tax_cost) / 1e12, # Trillion
            "Rocket_Share": total_rocket_cargo / M_TOTAL
        })
    
    df = pd.DataFrame(results)
    
    # --- 绘图: 经济最优与环境修正 ---
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # 绘制基础金融成本
    ax1.plot(df['Duration'], df['Financial_Cost'], 'b-o', label='Base Financial Cost ($Z_{fin}$)', linewidth=2)
    # 绘制含碳税成本
    ax1.plot(df['Duration'], df['Green_Cost'], 'g--s', label='With Carbon Tax ($Z_{green}$)', linewidth=2)
    
    # 标注最优解
    min_idx = df['Financial_Cost'].idxmin()
    best_T = df.loc[min_idx, 'Duration']
    best_Cost = df.loc[min_idx, 'Financial_Cost']
    
    ax1.annotate(f'Economic Optimum\n~{best_T} Years (${best_Cost:.1f}T)',
                 xy=(best_T, best_Cost), xytext=(best_T+10, best_Cost+10),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    
    ax1.set_xlabel("Project Duration (Years)", fontsize=12)
    ax1.set_ylabel("Total Cost (Trillion USD)", fontsize=12)
    ax1.set_title("Sec 4.2 & 6.1: Cost Optimization with Environmental Feedback", fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    plt.savefig('cost_env_optimization.png')
    print(f"[Done] Generated 'cost_env_optimization.png' for Sec 4.2 & 6.1")
    return df

# ==============================================================================
# 3. Section 6.2: 风险与基建优化 (Risk & Infrastructure Monte Carlo)
# ==============================================================================
def run_monte_carlo():
    n_sims = 1000
    scenarios = [10, 25] # 比较 10个基地 vs 25个基地
    results_mc = {}
    
    print(f"Running Monte Carlo Simulation ({n_sims} runs)...")
    
    for sites in scenarios:
        years_to_complete = []
        for _ in range(n_sims):
            cargo_rem = M_TOTAL
            year_idx = 0
            
            while cargo_rem > 0:
                curr_year = START_YEAR + year_idx
                year_idx += 1
                
                # 随机扰动
                # 1. 电梯: 随机 alpha (Normal dist around trend)
                alpha_trend = get_alpha(curr_year)
                alpha_rnd = max(0, np.random.normal(alpha_trend, 0.05))
                lift_e = KE_NOMINAL * alpha_rnd
                
                # 2. 火箭: 随机天气 (Scrub rate mean 0.16, std 0.05)
                # Beta_cadence 已经是物理极限，乘以 (1 - weather) 得到实际可用
                weather_loss = max(0, np.random.normal(0.16, 0.05))
                beta_eff = (1 - weather_loss)
                
                # 物理运力上限 (Bottleneck Check)
                max_rocket_cap = get_beta_capacity(curr_year, num_sites=sites) * beta_eff
                
                # 实际运力: 假设全力运输 (Max Effort Strategy)
                lift_r = max_rocket_cap
                
                cargo_rem -= (lift_e + lift_r)
                
                # 防止死循环 (设置一个极大值)
                if year_idx > 200: break
            
            years_to_complete.append(year_idx)
        results_mc[sites] = years_to_complete

    # --- 绘图: 风险直方图 ---
    plt.figure(figsize=(10, 6))
    
    # 10 Sites
    plt.hist(results_mc[10], bins=30, alpha=0.6, color='red', density=True, label='10 Sites (Baseline)')
    mu_10 = np.mean(results_mc[10])
    plt.axvline(mu_10, color='darkred', linestyle='--', linewidth=2, label=f'Mean: {mu_10:.1f} Yrs')
    
    # 25 Sites
    plt.hist(results_mc[25], bins=30, alpha=0.6, color='green', density=True, label='25 Sites (Optimized)')
    mu_25 = np.mean(results_mc[25])
    plt.axvline(mu_25, color='darkgreen', linestyle='--', linewidth=2, label=f'Mean: {mu_25:.1f} Yrs')
    
    # Target Line
    plt.axvline(60, color='black', linewidth=3, label='Target (60 Years)')
    
    plt.xlabel("Actual Completion Time (Years)", fontsize=12)
    plt.ylabel("Probability Density", fontsize=12)
    plt.title("Sec 6.2: Risk Analysis & Infrastructure Optimization", fontsize=14)
    plt.legend()
    
    plt.savefig('risk_optimization.png')
    print(f"[Done] Generated 'risk_optimization.png' for Sec 6.2")
    return results_mc

# ==============================================================================
# 4. Section 7: 最终结论数据 (Final Conclusion)
# ==============================================================================
def print_final_conclusion(df_det, res_mc):
    # 提取 60年方案的确定性数据
    row_60 = df_det[df_det['Duration'] == 60].iloc[0]
    
    # 提取 25基地方案的概率数据
    sims_25 = np.array(res_mc[25])
    prob_success = np.mean(sims_25 <= 60) * 100
    
    print("\n" + "="*60)
    print("SECTION 7: FINAL CONCLUSION DATA (RECOMMENDED STRATEGY)")
    print("="*60)
    print(f"Strategy Profile:        Hybrid Transport (60 Years) + Infrastructure Expansion")
    print("-" * 60)
    print(f"[Economic Feasibility]")
    print(f"  - Total Budget:        ${row_60['Financial_Cost']:.2f} Trillion")
    print(f"  - Rocket Cargo Share:  {row_60['Rocket_Share']*100:.1f}%")
    print(f"  - With Carbon Tax:     ${row_60['Green_Cost']:.2f} Trillion (Tax penalty included)")
    print("-" * 60)
    print(f"[Risk & Reliability (w/ 25 Sites)]")
    print(f"  - Expected Duration:   {np.mean(sims_25):.1f} Years")
    print(f"  - On-Time Probability: {prob_success:.1f}% (<= 60 Years)")
    print(f"  - Worst Case:          {np.max(sims_25):.1f} Years")
    print("="*60)

# ==============================================================================
# Main Execution
# ==============================================================================
if __name__ == "__main__":
    # 1. 运行确定性分析 (Sec 4.2 & 6.1)
    df_results = run_deterministic_analysis()
    
    # 2. 运行蒙特卡洛风险分析 (Sec 6.2)
    mc_results = run_monte_carlo()
    
    # 3. 输出最终结论 (Sec 7)
    print_final_conclusion(df_results, mc_results)