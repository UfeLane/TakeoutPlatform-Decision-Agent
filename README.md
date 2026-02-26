# TakeoutPlatform-Decision-Agent
A high-fidelity LLM agent simulating user mental evolution and platform switching decisions amidst the  "Food Delivery War" driven by social media opinions.
> **2025年外卖大战背景下，基于大模型智能体的用户决策演化仿真实验。**

本项目利用 LLM 构建高保真虚拟用户，模拟其在社交媒体（微博、小红书）舆论冲击下的心理变化，量化“杀熟”、“补贴”、“超时”等话题对平台决策的杀伤力。

## 📂 项目结构 (Project Structure)

* `main.py`: 实验启动入口，协调仿真流程。
* `core.py`: 核心仿真逻辑，处理舆论刺激与智能体认知更新。
* `personas.py`: 虚拟受试者（智能体）画像定义，包含价格/公平敏感度等参数。
* `config.py`: 环境与 API 全局配置。
* `export.py`: 实验结果分析与数据导出工具。
* `allcomments_with_label_processed.csv`: 预处理后的社交媒体舆论输入源。
* `simulation_result.json`: 记录智能体心路演变与决策轨迹的实验结果。

##  快速开始

1. **环境准备**：
   ```bash
   pip install -r requirements.txt
