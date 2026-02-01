### 1. 火箭发射频率与可靠性数据 (Section 3.1 & 3.2)

这些数据主要源于 **SpaceX 的历史发射记录**。你代码中使用的 2012-2024 年发射数据和 99.8% 的可靠性数据可引用：

* **SpaceX 官方统计 (ElonX)**: 提供详细的发射频次、周转时间和成功率。
* [SpaceX Statistics - ElonX.net](https://www.elonx.net/spacex-statistics/)


* **Wikipedia (List of Falcon 9 launches)**: 包含每次发射的详细载荷和结果，适合作为时间序列回归的原始数据。
* [List of Falcon 9 and Falcon Heavy launches](https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches)


* **CSIS 航天安全数据**: 包含 Falcon 9 的交互式发射历史图表。
* [Launch History: SpaceX Falcon 9 - CSIS](https://aerospace.csis.org/data/launch-history-spacex-falcon-9/)



### 2. 星舰 (Starship) 的运力与未来预测 (Section 4)

由于题目背景是 2050 年，你需要基于当前 Starship 的设计参数进行外推：

* **SpaceX Starship 官方页面**: 确认了 **100-150 MT** (吨) 的全重复使用有效载荷。
* [Starship - SpaceX Official](https://www.spacex.com/vehicles/starship)


* **芝加哥大学 Starship 报告**: 探讨了星舰的大规模部署能力（如 100 艘星舰每年可运输百万吨级物资）。
* [Starship Report - SSEH UChicago](https://sseh.uchicago.edu/doc/Starship_Report.pdf)



### 3. 成本学习曲线 (Wright's Law) 数据 (Section 3.3)

你模型中使用的 **85% 学习率** 和成本下降逻辑，在以下研究中可以找到实证支持：

* **Human Progress**: 详细描述了 SpaceX 如何遵循“莱特定律”降低成本，预测到 2028 年成本将进一步下降 40 倍。
* [Starlink Is Riding Down the Wright's Law Cost Curve](https://humanprogress.org/starlink-is-riding-down-the-wrights-law-cost/)


* **ScanX News**: 提到 Elon Musk 设想通过全重复使用将发射成本降低 **100 倍**。
* [SpaceX Targets 100x Cost Reduction](https://scanx.trade/stock-market-news/global/spacex-targets-100x-cost-reduction-in-satellite-launches-through-full-rocket-reusability/30688735)



### 4. 太空碎片与电梯退化风险 (Section 3.4)

太空电梯的可用性  下降是基于 **ESA (欧洲空间局)** 对凯斯勒效应的预测：

* **ESA 年度年度环境报告**: 提供了轨道碎片增长率的权威预测（约 1.2M 大于 1cm 的碎片）。
* [ESA Space Environment Report 2025](https://www.esa.int/Space_Safety/Space_Debris/ESA_Space_Environment_Report_2025)


* **国际太空电梯联盟 (ISEC)**: 讨论了电梯面临的碎片撞击概率及防御策略。
* [Space Elevator Survivability - ISEC](https://space-elevator.squarespace.com/s/2010StudyReport_SpaceElevatorSpaceDebris.pdf)
