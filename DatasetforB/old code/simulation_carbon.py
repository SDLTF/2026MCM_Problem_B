import numpy as np
import pandas as pd

# ==========================================
# 1. 全局参数 (修正版)
# ==========================================
M_TOTAL = 100_000_000   # 1亿吨
START_YEAR = 2050

# 太空电梯
KE_NOMINAL = 537_000    # MT/yr
COST_E_PER_MT = 220_000 # $220/kg

# 火箭 (Calibration Applied)
PAYLOAD = 150           # MT (Effective Lunar Payload)
# 修正1: 初始成本上调至队友调研值 ($2500/kg -> $375M/launch)
COST_R_INIT_LAUNCH = 375_000_000 
# 修正2: 底线成本上调以包含加油燃料 ($66/kg -> $10M/launch)
COST_R_FLOOR_LAUNCH = 10_000_000  
LEARNING_RATE = 0.85
B_EXPONENT = np.log2(LEARNING_RATE)

# 基建
# 修正3: 新增 15 个发射场的建设费 ($5B each)
INFRASTRUCTURE_COST = 15 * 5_000_000_000 

# 环境
EMISSION_FACTOR = 2.5   # MT CO2e / MT Payload
CARBON_TAX = 150        # $/MT

# ==========================================
# 2. 核心函数
# ==========================================
def get_alpha(t):
    """电梯效率 (碎片影响)"""
    baseline_lambda = 0.833
    baseline_repair = 14
    growth_debris = 0.015
    improve_repair = 0.005
    lambda_t = baseline_lambda * (1 + growth_debris)**(t - 2050)
    repair_t = baseline_repair * (1 - improve_repair)**(t - 2050)
    downtime = lambda_t * repair_t + (365 * 0.05)
    return max(0, 1 - (downtime / 365))

def calculate_rocket_cost_batch(n_start, n_new):
    """学习曲线积分"""
    if n_new <= 0: return 0
    n_mid = n_start + (n_new / 2)
    unit_cost = max(COST_R_FLOOR_LAUNCH, COST_R_INIT_LAUNCH * (n_mid ** B_EXPONENT))
    return n_new * unit_cost

def generate_calibrated_results():
    durations = [20, 30, 40, 50, 60, 70, 80, 100, 120]
    results = []

    for T in durations:
        total_financial = 0
        total_launches = 0
        total_rocket_cargo = 0
        annual_demand = M_TOTAL / T
        
        for i in range(T):
            year = START_YEAR + i
            
            # 电梯
            alpha = get_alpha(year)
            cap_e = KE_NOMINAL * alpha 
            cargo_e = min(annual_demand, cap_e)
            cost_e = cargo_e * COST_E_PER_MT
            
            # 火箭
            cargo_r = max(0, annual_demand - cargo_e)
            launches = cargo_r / PAYLOAD
            cost_r = calculate_rocket_cost_batch(total_launches, launches)
            
            total_financial += (cost_e + cost_r)
            total_launches += launches
            total_rocket_cargo += cargo_r
            
        # 加上基建固定成本 (Infrastructure Cost)
        total_financial += INFRASTRUCTURE_COST
        
        # 环境成本
        total_emissions = total_rocket_cargo * EMISSION_FACTOR
        env_cost = total_emissions * CARBON_TAX
        
        results.append({
            "Target Years": T,
            "Total Cost ($T)": round(total_financial / 1e12, 2),
            "Green Cost ($T)": round((total_financial + env_cost) / 1e12, 2),
            "Rocket Share (%)": round(100 * total_rocket_cargo / M_TOTAL, 1),
            "Infra Cost Included": "Yes"
        })
        
    df = pd.DataFrame(results)
    
    # 保存 CSV
    df.to_csv('simulation_results_calibrated.csv', index=False)
    
    print("CALIBRATION COMPLETE.")
    print("---------------------")
    print(f"Updated Parameters:")
    print(f" - Rocket Init Cost: ${COST_R_INIT_LAUNCH/1e6}M (was $150M)")
    print(f" - Rocket Floor Cost: ${COST_R_FLOOR_LAUNCH/1e6}M (was $2M)")
    print(f" - Fixed Infra Cost: ${INFRASTRUCTURE_COST/1e9}B added")
    print("\nNew Results Snapshot:")
    print(df)

if __name__ == "__main__":
    generate_calibrated_results()