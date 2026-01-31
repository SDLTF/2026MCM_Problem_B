import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# 1. 准备数据 (Data Preparation)
# ==========================================
# 场景标签
scenarios = ['Pure Rocket\n(20 Years)', 'Hybrid Strategy\n(60 Years)', 'Pure Elevator\n(100+ Years)']

# 计算排放量 (单位: Million MT CO2e)
# 假设总需求 M_TOTAL = 100 Million MT
# 排放因子 Emission Factor = 2.5
total_demand = 100 

# 场景 B: 纯火箭 (100% 火箭运输)
e_rocket = total_demand * 2.5 

# 场景 C: 混合策略 (约 70.8% 火箭运输 - 基于60年最优解)
e_hybrid = total_demand * 0.708 * 2.5 

# 场景 A: 纯电梯 (近似 0 排放)
e_elevator = 0 

emissions = np.array([e_rocket, e_hybrid, e_elevator])

# ==========================================
# 2. 绘图设置 (Plotting)
# ==========================================
plt.figure(figsize=(10, 6))

# 定义颜色: 红色(高污染), 蓝色(中等), 绿色(环保)
colors = ['#d62728', '#1f77b4', '#2ca02c']

# 绘制柱状图
bars = plt.bar(scenarios, emissions, color=colors, alpha=0.85, edgecolor='black', width=0.6)

# ==========================================
# 3. 装饰与标注 (Decoration & Annotation)
# ==========================================
plt.title('Quantitative Environmental Impact Analysis: Cumulative Emissions', fontsize=14, pad=20)
plt.ylabel('Total Emissions (Million MT $CO_2e$)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.4)

# 在柱子上方添加具体数值标签
for bar in bars:
    height = bar.get_height()
    if height > 0:
        plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                 f'{int(height)} Million MT',
                 ha='center', va='bottom', fontsize=12, fontweight='bold')
    else:
        plt.text(bar.get_x() + bar.get_width()/2., 5,
                 'Near Zero',
                 ha='center', va='bottom', fontsize=12, color='green', fontweight='bold')

# 添加"减排量"标注箭头 (Environmental Savings)
savings = e_rocket - e_hybrid
# 箭头从"混合方案"柱顶指向"纯火箭"高度的差值处，或者简单的文字标注
plt.annotate(f'Environmental Savings:\n{int(savings)} Million MT $CO_2e$\n(-29.2%)',
             xy=(1, e_hybrid), xytext=(1.4, e_hybrid + 40),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
             fontsize=11, bbox=dict(boxstyle="round,pad=0.4", fc="#f0f0f0", ec="gray", lw=1))

# 调整布局以防止标签被截断
plt.ylim(0, 300) # 设置y轴范围，给上方标签留空间
plt.tight_layout()

# ==========================================
# 4. 保存图片
# ==========================================
plt.savefig('environmental_impact.png', dpi=300)
plt.show()

print("Image 'environmental_impact.png' has been generated successfully.")