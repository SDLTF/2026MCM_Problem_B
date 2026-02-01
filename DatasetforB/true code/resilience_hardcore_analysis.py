import numpy as np
import matplotlib.pyplot as plt

def generate_section_7_resilience_plots():
    # 1. 时间参数定义 (单位: 天)
    t_max = 180
    t = np.linspace(0, t_max, 1000)
    t_fail = 30  # 假设在第 30 天电梯发生失效

    # 2. 物理参数设定 (单位: MT/day)
    omega = 3500           # 月球基地日消耗率 (Omega)
    phi_isru = 500         # 月球 ISRU 日产出 (Phi_ISRU)
    phi_elevator = 2000    # 电梯日运力 (失效前)
    phi_rocket_base = 1200 # 火箭常态日运力

    # 3. 25 个发射场的“浪涌动员”参数 (Heaviside Step Function)
    n_pads = 25
    cap_per_pad = 180      # 单个场站全功率增量
    # 设定场站激活延迟: 5天到45天不等，模拟地勤动员时间
    delays = np.linspace(5, 45, n_pads) 

    # 4. 计算运力流 (Flows)
    flow_elevator = np.where(t < t_fail, phi_elevator, 0)
    flow_isru = np.full_like(t, phi_isru)
    flow_rocket_base = np.full_like(t, phi_rocket_base)

    # 核心：基于单位阶跃函数的浪涌叠加
    surge_flow = np.zeros_like(t)
    for d in delays:
        # H(t - t_fail - Delta_t_i)
        surge_flow += np.where(t > (t_fail + d), cap_per_pad, 0)

    total_inflow = flow_elevator + flow_isru + flow_rocket_base + surge_flow
    net_flow = total_inflow - omega

    # 5. 数值积分得到物资储备 S(t)
    dt = t[1] - t[0]
    S = np.zeros_like(t)
    S_initial = 100000     # 初始储备
    S_crit = 30000        # 生存红线
    S[0] = S_initial
    for i in range(1, len(t)):
        S[i] = S[i-1] + net_flow[i] * dt

    # 寻找转折点 t* (储备量止跌回升的时刻)
    pivot_idx = np.where((net_flow >= 0) & (t > t_fail))[0]
    t_star = t[pivot_idx[0]] if len(pivot_idx) > 0 else None

    # --- 绘图逻辑 ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, dpi=150)

    # Plot 1: 物资储备动力学 (Resilience Test)
    ax1.plot(t, S, color='#2878B5', linewidth=3, label='Lunar Supply Inventory $S(t)$')
    ax1.axhline(S_crit, color='#D62728', linestyle='--', alpha=0.8, label='Survival Threshold $S_{crit}$')
    ax1.axvline(t_fail, color='black', linestyle=':', label='Elevator Failure Event')
    
    # 标注生存窗口
    ax1.fill_between(t, 0, S_crit, color='#D62728', alpha=0.1)
    
    if t_star:
        ax1.scatter(t_star, S[pivot_idx[0]], color='green', s=100, zorder=5)
        ax1.annotate(f'Pivot Point: Day {int(t_star-t_fail)} Post-Failure',
                     xy=(t_star, S[pivot_idx[0]]), xytext=(t_star+15, S[pivot_idx[0]]-10000),
                     arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
                     fontsize=11, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="green", alpha=0.9))

    ax1.set_title('Section 7.1: Dynamics of Supply Depletion & Recovery', fontsize=15, fontweight='bold')
    ax1.set_ylabel('Material Inventory (MT)', fontsize=12)
    ax1.set_ylim(0, S_initial * 1.2)
    ax1.legend(loc='upper right', frameon=True)
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Plot 2: 运力流响应 (Heaviside Surge)
    ax2.fill_between(t, flow_elevator, color='#2878B5', alpha=0.2, label='Lost Elevator Flow')
    ax2.plot(t, total_inflow, color='#C82423', linewidth=2.5, label='Total Supply Inflow $\Phi_{total}(t)$')
    ax2.axhline(omega, color='#FF7F0E', linestyle='--', linewidth=2, label='Consumption Rate $\Omega(t)$')
    
    # 填充浪涌部分
    ax2.fill_between(t, flow_isru + flow_rocket_base, total_inflow, where=(t > t_fail), 
                     color='#C82423', alpha=0.1, label='Rocket Surge (25 Pads)')

    ax2.set_title('Section 7.2: Staggered Surge Response (Heaviside Activation)', fontsize=15, fontweight='bold')
    ax2.set_ylabel('Mass Flow Rate (MT/Day)', fontsize=12)
    ax2.set_xlabel('Time Since Project Launch (Days)', fontsize=12)
    ax2.set_ylim(0, total_inflow.max() * 1.2)
    ax2.legend(loc='upper right', frameon=True)
    ax2.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout(pad=3.0)
    plt.savefig('resilience_hardcore_analysis.png')
    plt.show()

if __name__ == "__main__":
    generate_section_7_resilience_plots()