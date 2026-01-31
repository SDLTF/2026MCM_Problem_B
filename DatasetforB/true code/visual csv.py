import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Reconstruct the final calibrated data (Single Source of Truth)
data = {
    "Duration": [20, 30, 40, 50, 60, 70, 80, 100],
    "Financial Cost ($T)": [15.10, 15.67, 16.22, 16.75, 17.26, 17.75, 18.23, 19.15],
    "Green Cost ($T)": [15.14, 15.71, 16.25, 16.77, 17.28, 17.78, 18.26, 19.17],
    "Rocket Share (%)": [90.2, 85.3, 80.4, 75.6, 70.8, 66.0, 61.3, 51.9],
    "Carbon Tax ($B)": [33.8, 32.0, 30.2, 28.3, 26.5, 24.8, 23.0, 19.5]
}
df = pd.DataFrame(data)

# Set visual style
plt.style.use('seaborn-v0_8-whitegrid')
fig = plt.figure(figsize=(14, 10))

# --- Plot 1: Cost Optimization Curve (Financial vs Green) ---
ax1 = plt.subplot(2, 2, 1)
# Plot Lines
sns.lineplot(data=df, x="Duration", y="Financial Cost ($T)", marker='o', label="Financial Cost", linewidth=2, color='#1f77b4', ax=ax1)
sns.lineplot(data=df, x="Duration", y="Green Cost ($T)", marker='s', label="Green Cost (w/ Tax)", linewidth=2, linestyle='--', color='#2ca02c', ax=ax1)

# Highlight Optimal Point (60 Years)
opt_row = df[df["Duration"] == 60].iloc[0]
ax1.plot(60, opt_row["Green Cost ($T)"], 'r*', markersize=15, label="Optimal (60y)")
ax1.annotate(f"${opt_row['Green Cost ($T)']:.2f}T", 
             xy=(60, opt_row["Green Cost ($T)"]), xytext=(65, opt_row["Green Cost ($T)"]-0.5),
             arrowprops=dict(facecolor='black', arrowstyle='->'), fontsize=10, fontweight='bold')

ax1.set_title("Economic Trade-off: Project Cost vs. Duration", fontsize=12, fontweight='bold')
ax1.set_ylabel("Total Cost (Trillion USD)")
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.6)

# --- Plot 2: Logistics Composition (Rocket vs Elevator) ---
ax2 = plt.subplot(2, 2, 2)
# Create Stacked Area-like visual using bars for clarity at discrete points
# Rocket Share
sns.barplot(data=df, x="Duration", y="Rocket Share (%)", color='#d62728', alpha=0.7, label="Rocket Fleet", ax=ax2)
# Elevator Share (Complement)
# We can't easily stack seaborn barplots directly without melt, let's just plot Rocket Share line + Area
ax2.clear()
ax2.fill_between(df["Duration"], df["Rocket Share (%)"], color='#d62728', alpha=0.5, label="Rocket Share")
ax2.fill_between(df["Duration"], df["Rocket Share (%)"], 100, color='#1f77b4', alpha=0.5, label="Elevator Share")
ax2.plot(df["Duration"], df["Rocket Share (%)"], 'k--', linewidth=1)

ax2.set_title("Logistics Strategy Composition", fontsize=12, fontweight='bold')
ax2.set_ylabel("Transport Share (%)")
ax2.set_ylim(0, 100)
ax2.legend(loc="lower left")
ax2.grid(True, linestyle='--', alpha=0.6)
# Annotate 60y split
split_60 = df[df["Duration"] == 60].iloc[0]["Rocket Share (%)"]
ax2.text(60, split_60, f"Rocket: {split_60}%", ha='center', va='bottom', fontweight='bold', color='white')

# --- Plot 3: Environmental Penalty (Carbon Tax) ---
ax3 = plt.subplot(2, 1, 2)
# Bar chart for Tax
bars = sns.barplot(data=df, x="Duration", y="Carbon Tax ($B)", color='gray', edgecolor='black', ax=ax3)

ax3.set_title("Environmental Penalty: Carbon Tax Burden", fontsize=12, fontweight='bold')
ax3.set_ylabel("Carbon Tax Bill (Billion USD)")
ax3.set_xlabel("Project Duration (Years)")

# Add values on top
for container in ax3.containers:
    ax3.bar_label(container, fmt='$%.1fB', padding=3)

# Highlight 60y bar
bars.patches[4].set_color('#2ca02c') # 60 years is index 4
bars.patches[4].set_edgecolor('black')
bars.patches[4].set_linewidth(2)
ax3.annotate("Optimal Balance", xy=(4, 26.5), xytext=(4, 30),
             arrowprops=dict(facecolor='black', arrowstyle='->'), ha='center')

plt.tight_layout()
plt.savefig('csv_visualization_dashboard.png', dpi=300)
plt.show()