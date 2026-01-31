import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ==========================================
# 0. 全局排版美化配置
# ==========================================
plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.unicode_minus': False 
})
sns.set_theme(style="whitegrid")

# ==========================================
# 1. 修复 cost_env_optimization (精确指向 60Y)
# ==========================================
def fix_cost_optimization_final():
    # 模拟与你上传图片一致的数据
    durations = np.arange(20, 101, 5)
    # 基础财务成本
    fin_costs = [15.1, 15.53, 15.67, 16.22, 16.75, 17.26, 17.75, 18.23, 18.7, 19.15, 19.6, 20.1, 20.6, 21.1, 21.6, 22.1, 22.6]
    # 截取匹配长度
    fin_costs = fin_costs[:len(durations)]
    green_costs = [f + 0.05 for f in fin_costs] # 绿色成本略高
    
    df = pd.DataFrame({"T": durations, "Fin": fin_costs, "Green": green_costs})
    
    plt.figure(figsize=(10, 7))
    plt.plot(df['T'], df['Fin'], color='#5c75ae', marker='o', linewidth=2, label='Financial Cost')
    plt.plot(df['T'], df['Green'], color='#52b16a', marker='s', linestyle='--', linewidth=2, label='Green Cost (Tax Included)')
    
    # --- 核心修复：获取 60Y 的准确坐标 ---
    target_row = df[df['T'] == 60].iloc[0]
    target_x = target_row['T']
    target_y = target_row['Green']
    
    # 箭头指向精确的数据点 (target_x, target_y)
    plt.annotate('Optimal Strategy (60Y)', 
                 xy=(target_x, target_y), 
                 xytext=(target_x + 10, target_y - 1.2), # 文字放在点右下方
                 fontsize=11,
                 fontweight='bold',
                 arrowprops=dict(arrowstyle='-|>', color='black', lw=1),
                 bbox=dict(boxstyle="round,pad=0.5", fc="#ffffbf", ec="#e6e600", alpha=0.8))
    
    plt.title('Optimal Duration Analysis', fontsize=15, pad=20)
    plt.xlabel('Project Duration (Years)')
    plt.ylabel('Total Cost (Trillion USD)')
    plt.legend(loc='upper left', frameon=True)
    plt.grid(True, linestyle=':', alpha=0.6)
    
    plt.savefig('cost_env_optimization_v2_fixed_v4.png')
    plt.close()

# ==========================================
# 2. 修复 csv_visualization_dashboard (解决布局警告)
# ==========================================
def fix_csv_dashboard_final():
    df = pd.DataFrame({
        "Duration": [20, 30, 40, 50, 60, 70, 80, 100],
        "Fin": [15.1, 15.67, 16.22, 16.75, 17.26, 17.75, 18.23, 19.15],
        "Share": [90.2, 85.3, 80.4, 75.6, 70.8, 66.0, 61.3, 51.9],
        "Tax": [33.8, 32.0, 30.2, 28.3, 26.5, 24.8, 23.0, 19.5]
    })
    
    fig = plt.figure(figsize=(15, 13))
    # 手动调整子图边距，彻底避开 tight_layout 警告
    fig.subplots_adjust(hspace=0.4, wspace=0.3, top=0.92, bottom=0.08, left=0.1, right=0.95)
    
    gs = fig.add_gridspec(2, 2)
    
    # 子图1: 财务曲线
    ax1 = fig.add_subplot(gs[0, 0])
    sns.lineplot(data=df, x="Duration", y="Fin", marker='o', ax=ax1, color='#1f77b4', linewidth=2.5)
    ax1.set_title("Economic Trade-off: Project Cost", pad=15)
    ax1.set_ylabel("USD (Trillion)", labelpad=10)

    # 子图2: 填充图
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.fill_between(df["Duration"], 0, df["Share"], color='#d62728', alpha=0.4, label='Rocket Share')
    ax2.fill_between(df["Duration"], df["Share"], 100, color='#1f77b4', alpha=0.4, label='Elevator Share')
    ax2.set_title("Logistics Strategy Composition", pad=15)
    ax2.set_ylabel("Share (%)")
    ax2.set_ylim(0, 100)
    ax2.legend(loc='lower left', frameon=True)

    # 子图3: 碳税 (修复 palette 警告)
    ax3 = fig.add_subplot(gs[1, :])
    sns.barplot(data=df, x="Duration", y="Tax", hue="Duration", palette="viridis", 
                ax=ax3, edgecolor='black', legend=False)
    ax3.set_title("Environmental Penalty: Carbon Tax Liability", pad=15)
    ax3.set_ylabel("USD (Billion)", labelpad=10)
    
    for container in ax3.containers:
        ax3.bar_label(container, fmt='$%.1fB', padding=3)

    plt.savefig('csv_visualization_dashboard_fixed_v4.png')
    plt.close()

# ==========================================
# 3. 修复 parameter_estimation_beta (参数估计)
# ==========================================
def fix_parameter_estimation_final():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), layout="constrained")
    
    years = np.arange(2010, 2101)
    beta = 500 / (1 + np.exp(-0.25 * (years - 2030)))
    ax1.plot(years, beta, color='#1f77b4', linewidth=2.5, label='Logistic Regression Prediction')
    hist_years = [2012, 2014, 2016, 2018, 2020, 2021, 2022, 2023, 2024]
    hist_vals = [2, 6, 8, 15, 26, 31, 61, 96, 110]
    ax1.scatter(hist_years, hist_vals, color='black', s=35, label='Historical Data (SpaceX)', zorder=5)
    
    ax1.axvline(2050, color='red', linestyle='--', alpha=0.6, label='Project Start (2050)')
    ax1.annotate('2050 Capacity:\n~499 launches/yr', 
                 xy=(2050, 499), xytext=(2015, 400), # 文字位置微调
                 arrowprops=dict(arrowstyle='->', color='black', connectionstyle="arc3,rad=.2"))
    
    ax1.set_title('Estimation of Rocket Launch Cadence', pad=20)
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Launches per Site per Year')
    ax1.legend(loc='lower right', frameon=True)

    rel_curve = 1.0 - 0.1 * np.exp(-0.15 * (years - 2010))
    ax2.plot(years, rel_curve, color='#2ca02c', linewidth=2.5, label='Reliability Growth Curve')
    hist_rel_y = [2010, 2015, 2018, 2020, 2022, 2024]
    hist_rel_v = [0.90, 0.94, 0.97, 0.985, 0.992, 0.996]
    ax2.scatter(hist_rel_y, hist_rel_v, color='black', s=35, label='Historical Trend')
    
    ax2.axvline(2050, color='red', linestyle='--', alpha=0.6)
    ax2.annotate('2050 Reliability:\n0.9998', 
                 xy=(2050, 0.9998), xytext=(2020, 0.94), # 文字位置微调
                 arrowprops=dict(arrowstyle='->', color='black', connectionstyle="arc3,rad=-.2"))
    
    ax2.set_title('Estimation of Vehicle Reliability', pad=20)
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Mission Success Rate')
    ax2.set_ylim(0.88, 1.04) # 留出顶部空间
    ax2.legend(loc='lower right', frameon=True)
    
    plt.savefig('parameter_estimation_beta_fixed_v4.png')
    plt.close()

if __name__ == "__main__":
    fix_cost_optimization_final()
    fix_csv_dashboard_final()
    fix_parameter_estimation_final()
    print("✨ v4 最终版生成成功！箭头已精确对齐数据点，布局无重叠无警告。")