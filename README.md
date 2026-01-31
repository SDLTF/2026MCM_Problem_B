

# 🚀 地月物流网络优化模型 (2026 MCM Problem B)

本项目为 **2026年美国大学生数学建模竞赛 (MCM) B题** 的特等奖候选方案。我们开发了一个动态混合物流网络模型，旨在解决 2050 年将 1 亿公吨物资运往月球的全球战略难题。

## 🌟 核心模型亮点

* **三位一体创新**：整合了 **ISRU（就地资源利用）自给模型**、**轨道碎片动力学反馈回路** 以及 **冗余度灾难恢复模型**。
* **1-2-6 战略**：通过数学仿真确立了 **1 亿吨** 物资、**25 个** 全球发射基地、**60 年** 项目工期的最优执行路径。
* **动态策略演化**：物流配比随技术成熟度（Wright's Law）和环境风险自动调整，实现从“电梯主导”到“火箭/ISRU协同”的平滑范式转移。

---

## 📂 目录结构与功能详解

### 1. `DatasetforB/` (算法与仿真核心)

此文件夹包含所有数学模型的实现脚本，是项目的“发动机”。

* **`true code/` (最终校准脚本)**
* `final_.py`: **集成化仿真引擎**。一键生成包含 ISRU 灵敏度、韧性压力测试、全局优化及动态分配在内的全套核心图表。
* `parameter_estimation.py`: 基于 SpaceX 历史数据，利用 **Logistic 回归** 预测 2050 年后的火箭发射频次上限及任务可靠性。
* `global_optimum_analysis.py`: 计算 **综合压力指数 (GSSI)**，通过权衡财务支出、窗口拥堵和电梯风险，锁定 60 年为黄金平衡点。
* `isru_sensitivity_analysis.py`: 量化月球自给自足能力对地球物流负荷的削减效应。
* `risk_optimization.py`: 蒙特卡洛随机模拟，论证 25 个基地相比 10 个基地在应对突发干扰时的概率优势。
* `adaptive_allocation_trend.py`: 绘制运力分配随时间进化的堆叠面积图。



### 2. `pictures/` (可视化证据链)

存放模型输出的高清图表（v4 校准版），直接支撑论文的每一个核心论点。

* `resilience_test_survival.png`: **核心图表**。展示电梯失效后，25 个基地如何保障月球基地的生存水位。
* `global_optimum_analysis_fixed_v4.png`: 展示“U型”总压力曲线及 60 年最优工期。
* `adaptive_allocation_trend.png`: 展示地月物流系统从 2050 到 2150 年的模式演变。
* `isru_sensitivity_analysis_fixed_v4.png`: 展示 20% 与 50% 自给率下的成本敏感度对比。

### 3. `essay/` (论文与文档)

* **`Final_files/structure.md`**: 定义了整篇论文的学术框架，涵盖从引言到韧性分析的完整逻辑。
* **`already_ok/`**: 包含经过校准的学术描述片段，如：
* `ending.md`: 给决策者的**战略备忘录 (Memorandum)**。
* `description for pictures.md`: 专业的图注与图表分析话术。


* **`tex file/`**: 包含符合竞赛格式要求的 LaTeX 源代码及最终生成的 PDF 论文。

---

## 🛠️ 快速复现指南

1. **环境依赖**：
```bash
pip install numpy matplotlib pandas seaborn scipy

```


2. **生成全套图表**：
直接运行 `python "DatasetforB/true code/final_.py"`。该脚本会自动在 `pictures/` 目录下更新所有校准后的可视化结果。
3. **查看数据报表**：
运行 `simulation_csv.py` 以获取不同工期场景下的详细成本与风险量化表格。

---

## 🏆 团队贡献

本项目由 2026 MCM 战略建模小组开发。模型不仅解决了“物资搬运”问题，更为人类在月球的**永久性、韧性生存**提供了数学证明。
