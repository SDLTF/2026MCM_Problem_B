import numpy as np
import matplotlib.pyplot as plt

# 1. Simulation Parameters
years = np.linspace(2050, 2110, 100)
total_demand = 1.0 + 0.015 * (years - 2050) # Normalized total mass demand

# 2. ISRU Contribution Models (Sigmoid Growth)
def isru_sigmoid(t, t_start, k, max_val):
    return max_val / (1 + np.exp(-k * (t - t_start)))

# Water ISRU: Starts early, matures around 2065
water_isru = isru_sigmoid(years, 2065, 0.25, 0.45)
# Material ISRU: Starts later, matures around 2080
material_isru = isru_sigmoid(years, 2080, 0.2, 0.35)

# Earth dependency is the remainder
earth_supply = total_demand - water_isru - material_isru

# 3. Plotting
fig = plt.figure(figsize=(12, 7), dpi=150)
ax = plt.gca()

# Stackplot
plt.stackplot(years, water_isru, material_isru, earth_supply,
              labels=['Water ISRU (Lunar Ice Extraction)',
                      'Material ISRU (3D Printing & Metallurgy)',
                      'Earth-to-Moon Logistical Supply'],
              colors=['#2E91E5', '#2CA02C', '#E1341E'], alpha=0.7)

# Strategic Pivot Lines
plt.axvline(2070, color='black', linestyle='--', alpha=0.6)
plt.text(2071, 1.6, 'Strategic Pivot:\nSelf-Sufficiency > 50%', fontsize=10, fontweight='bold', bbox=dict(facecolor='white', alpha=0.8))

# Annotating specific points
plt.annotate('Water Independence Threshold', xy=(2065, 0.2), xytext=(2052, 0.4),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=8),
             fontsize=9, fontweight='bold')

plt.title('Section 8.2: Decoupling Strategy - ISRU Evolution & Earth Dependency Reduction', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Timeline (Year)', fontsize=12)
plt.ylabel('Normalized Mass Flow (MT/Year)', fontsize=12)
plt.xlim(2050, 2110)
plt.ylim(0, 2.0)
plt.legend(loc='upper left', frameon=True, fontsize=10)
plt.grid(axis='y', linestyle=':', alpha=0.5)

plt.tight_layout()
plt.savefig('isru_water_contribution.png')
plt.show()