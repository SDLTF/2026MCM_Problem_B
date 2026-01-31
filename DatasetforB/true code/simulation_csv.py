import numpy as np
import pandas as pd

# ==========================================
# 1. 最终校准参数 (Calibrated Parameters)
# ==========================================
# 请确保你的代码中这些数值与此处完全一致
M_TOTAL = 100_000_000         # 总需求 1亿吨
START_YEAR = 2050

# 太空电梯
KE_NOMINAL = 537_000          # 年运力 (MT)
COST_E_PER_MT = 220_000       # $220/kg

# 火箭 (基于长征9号/Starship校准)
PAYLOAD = 150                 # MT
COST_R_INIT_LAUNCH = 375_000_000 # $3.75亿/次 (关键参数!)
COST_R_FLOOR_LAUNCH = 10_000_000  # $1000万/次
LEARNING_RATE = 0.85
B_EXPONENT = np.log2(LEARNING_RATE)

# 基建 (容易被遗漏的参数!)
INFRASTRUCTURE_COST = 75_000_000_000 # $750亿

# 环境
EMISSION_FACTOR = 2.5
CARBON_TAX = 150

# ==========================================
# 2. 核心计算逻辑
# ==========================================
def get_alpha(t):
    """电梯效率衰减"""
    t_diff = t - 2050
    lambda_t = 0.833 * (1 + 0.015)**t_diff
    repair_t = 14 * (1 - 0.005)**t_diff
    downtime = lambda_t * repair_t + (365 * 0.05)
    return max(0, 1 - (downtime / 365))

def calculate_rocket_cost_batch(n_start, n_new):
    """火箭批次成本计算"""
    if n_new <= 0: return 0
    # 使用中点近似法积分
    n_mid = n_start + (n_new / 2)
    # 防止 n_mid < 1 导致计算错误
    if n_mid < 1: n_mid = 1
    
    unit_cost = max(COST_R_FLOOR_LAUNCH, COST_R_INIT_LAUNCH * (n_mid ** B_EXPONENT))
    return n_new * unit_cost

# ==========================================
# 3. 运行验证
# ==========================================
def verify_results():
    durations = [20, 30, 40, 50, 60, 70, 80, 100]
    results = []

    print(f"{'Duration':<10} | {'Fin Cost($T)':<15} | {'Green Cost($T)':<15} | {'Rocket Share(%)':<15}")
    print("-" * 65)

    for T in durations:
        total_financial = 0
        total_launches = 0
        total_rocket_cargo = 0
        annual_demand = M_TOTAL / T
        
        for i in range(T):
            year = START_YEAR + i
            
            # 1. 计算电梯
            alpha = get_alpha(year)
            cap_e = KE_NOMINAL * alpha 
            cargo_e = min(annual_demand, cap_e)
            cost_e = cargo_e * COST_E_PER_MT
            
            # 2. 计算火箭
            cargo_r = max(0, annual_demand - cargo_e)
            launches = cargo_r / PAYLOAD
            cost_r = calculate_rocket_cost_batch(total_launches, launches)
            
            # 3. 累加
            total_financial += (cost_e + cost_r)
            total_launches += launches
            total_rocket_cargo += cargo_r
            
        # 4. 加上基建费 (关键!)
        total_financial += INFRASTRUCTURE_COST
        
        # 5. 加上环境税
        total_emissions = total_rocket_cargo * EMISSION_FACTOR
        env_cost = total_emissions * CARBON_TAX
        green_cost = total_financial + env_cost
        
        # 格式化输出
        fin_t = total_financial / 1e12
        green_t = green_cost / 1e12
        share = 100 * total_rocket_cargo / M_TOTAL
        
        print(f"{T:<10} | {fin_t:<15.2f} | {green_t:<15.2f} | {share:<15.1f}")
        
        results.append({
            "Duration": T,
            "Financial Cost ($T)": round(fin_t, 2),
            "Green Cost ($T)": round(green_t, 2),
            "Rocket Share (%)": round(share, 1)
        })

    # 保存 CSV
    df = pd.DataFrame(results)
    df.to_csv('simulation_results_final.csv', index=False)
    print("\n[Success] Verified data saved to 'simulation_results_final.csv'")

if __name__ == "__main__":
    verify_results()