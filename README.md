# 越过天梯：基于动态混合物流网络的月球殖民地优化模型

本仓库包含 **2026 MCM Problem B** 的数学模型实现、数据仿真代码及相关可视化分析。本项目旨在解决 2050 年将 1 亿公吨物资运往月球的物流难题，通过构建多目标动态规划模型，在运输成本、项目工期与环境影响之间寻找最优平衡点。

## 🚀 项目概览

本项目通过对比和整合 **太空电梯 (Space Elevator)** 与 **传统火箭 (Rocket Fleet)** 两种运输方式，提出了一个“混合-60 / 扩容-25”的最优战略。

### 核心亮点

* **动态参数建模**：引入了随轨道碎片增加而衰减的电梯效率因子 ，以及随技术成熟度提升的火箭效能因子 。
* **莱特成本学习曲线**：应用 Wright's Law 模拟了火箭复用技术带来的边际成本指数级下降（从初始 $2500/kg 降至 $66/kg 物理底线）。
* **风险与弹性分析**：利用蒙特卡洛模拟揭示了 10 个现有发射场的运力瓶颈，并提出了扩建至 25 个基地以对冲天气和事故风险的优化方案。
* **环境足迹量化**：量化了混合运输策略对平流层  排放的削减效益（相比纯火箭方案减排 29.2%）。

## 📁 文件夹结构

```text
├── DatasetforB/
│   ├── true code/           # 核心仿真与绘图脚本
│   │   ├── parameter_estimation.py      # 火箭效能与可靠性回归分析
│   │   ├── cost_env_optimization_v2.py  # 包含碳税的成本优化模型
│   │   ├── risk_optimization.py         # 基础设施与风险蒙特卡洛模拟
│   │   └── simulation_csv.py            # 生成最终结果数据集
│   └── old code/            # 早期模型迭代版本
├── pictures/                # 自动生成的分析图表
│   ├── alpha_beta_divergence.png        # 电梯衰减与火箭成熟趋势对比
│   ├── cost_env_optimization_v2.png     # 成本-工期 Pareto 最优曲线
│   ├── environmental_impact.png         # 场景减排效益柱状图
│   └── risk_optimization.png            # 10基地 vs 25基地完工时间分布
└── essay/                   # 论文撰写相关文件（Markdown & TeX）

```

## 📊 核心研究结论

根据校准后的动态模型，我们得出的关键结论如下：

1. **最优工期**：锁定为 **60 年**。这是“火箭学习红利”与“电梯效率衰减”的黄金交叉点。
2. **物流配比**：火箭承担约 **70.8%** 的大宗建设物资运输，太空电梯承担 **29.2%** 的生命维持补给及早期基建材料。
3. **基建扩容**：现有 10 个发射场由于缺乏“浪涌容量”，在天气扰动下极易导致工期滑坡。必须扩建至 **25 个** 基地才能确保 100% 按时完工。
4. **经济可行性**：项目总预算估算为 **17.3 Trillion USD**（含碳税与基建费用），在 60 年的周期内具有显著的工程容错需求和财务合理性。

## 🛠️ 如何使用

1. **环境配置**：
```bash
pip install numpy matplotlib pandas scipy seaborn

```


2. **运行仿真**：
执行 `DatasetforB/true code/simulation_csv.py` 生成详细的数据报表。
3. **可视化分析**：
运行 `DatasetforB/true code/visual csv.py` 可生成完整的经济与物流策略仪表盘。



# 2026 MCM Problem B 解决方案代码库结构说明

以下是仓库中各文件夹及文件的详细用途说明。

## 📂 目录结构详解

### 1. `DatasetforB/` (数据与代码核心目录)

此文件夹包含用于模型构建、参数估计、仿真模拟及绘图的所有 Python 代码。它被细分为两个子文件夹：

* **`true code/` (最终代码)**：包含论文最终采用的、经过校准的核心脚本。
* `simulation_csv.py`: **核心仿真脚本**。基于校准后的参数（如长征9号成本、基建费用等）运行物流模型，生成最终的数据集 `simulation_results_final.csv`。
* `visual csv.py`: **可视化仪表盘脚本**。读取 `simulation_results_final.csv`，生成包含成本权衡、物流配比和碳税分析的综合图表 `csv_visualization_dashboard.png`。
* `parameter_estimation.py` / `parameter_estimation_beta...`: **参数估计算法**。使用 Logistic 回归和 Wright's Law 对 SpaceX 历史数据进行拟合，预测火箭发射频次 () 和成本下降曲线。
* `cost_env_optimization_v2.py`: **多目标优化模型**。计算不同工期下的财务成本与环境成本，绘制 Pareto 最优曲线 `cost_env_optimization_v2.png`，确定 60 年为最优解。
* `risk_optimization.py`: **蒙特卡洛风险分析脚本**。模拟天气延误和碎片撞击等随机变量，对比 10 个基地与 25 个基地的完工时间分布，生成 `risk_optimization.png`。
* `env_impact and true_l_curve.py`: **环境影响分析**。生成环境影响对比柱状图 `environmental_impact.png` 和环境-时间权衡曲线 `true_l_curve.png`。


* **`old code/` (存档代码)**：包含开发过程中的早期版本或实验性代码。这些代码保留用于回溯思路，但在最终论文中未直接使用。

### 2. `pictures/` (图表结果)

此文件夹存放由 `true code/` 中的脚本生成的**高清图片和数据文件**，这些图片被直接插入到最终论文中作为核心论据。

* `alpha_beta_divergence.png`: 展示太空电梯效率衰减 () 与火箭技术成熟 () 的背离趋势图。
* `cost_env_optimization_v2.png`: 经济最优曲线图，展示了 60 年工期是成本最低点。
* `csv_visualization_dashboard.png`: 综合可视化仪表盘，包含成本、物流分担比例和碳税分析。
* `environmental_impact.png`: 环境影响对比柱状图，展示混合方案相比纯火箭方案的减排量。
* `parameter_estimation_beta.png`: 火箭发射频次和可靠性的 S 型增长预测图。
* `risk_optimization.png`: 风险分析直方图，展示了扩建基地前后完工时间的概率分布对比。
* `true_l_curve.png`: 环境-时间权衡的 L 形曲线。
* `simulation_results_final.csv`: 最终仿真输出的数据表格，包含不同工期下的详细成本和可行性评估。

### 3. `essay/` (论文写作)

此文件夹包含论文的写作素材、结构大纲以及最终的排版文件。

* **`tex file/` (LaTeX 排版)**：包含论文的 LaTeX 源代码和编译输出。
* `document.tex`: **论文主源文件**。包含论文的所有文本、公式和排版指令。
* `建立月球殖民地...pdf` / `document.pdf`: **最终生成的论文 PDF**。提交给竞赛的成品文件。
* 其他文件 (`.aux`, `.log`, `.out`, `.synctex` 等): LaTeX 编译过程中的辅助文件。


* **`Final_files/`**:
* `structure.md`: 论文的**最终结构大纲**，定义了各章节的标题和核心逻辑。


* **`already_ok/`**:
* 包含已经撰写完成并核对无误的**文本段落**（Markdown 格式），如参数估计部分的详细描述 (`an estimate for alpha and beta.md`)、CSV 数据描述 (`description for csv.md`) 和图片分析话术 (`description for pictures.md`)。



### 4. `Problems/` (赛题文件)

* `2026_MCM_Problem_B.pdf`: 2026 年 MCM 竞赛 B 题的**官方原版题目描述**。

---

## 🛠️ 快速开始

如果您想重现论文中的数据和图表：

1. 确保安装了必要的 Python 库：`numpy`, `pandas`, `matplotlib`, `scipy`, `seaborn`。
2. 进入 `DatasetforB/true code/` 目录。
3. 运行 `simulation_csv.py` 生成数据。
4. 运行 `visual csv.py` 或其他绘图脚本生成图表。
5. 生成的图片将保存在当前目录或 `pictures/` 目录中（取决于脚本设置）。