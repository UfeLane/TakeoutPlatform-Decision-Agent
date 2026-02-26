import pandas as pd
import json
import os
from core import Agent
from personas import AGENTS_CONFIG


# ================= 1. 数据加载与抽样函数 =================
def load_sampled_data(csv_filename, samples_per_class=5):
    """
    读取 CSV，只取 'content' 和 'cluster_label' 两列
    从每个类别中随机抽取 5 条，并按类别顺序排列。
    """
    # 获取当前脚本所在的文件夹路径，确保一定能找到文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, csv_filename)

    print(f"📂 正在尝试读取文件: {csv_path}")

    try:
        # 1. 读取 CSV (尝试不同编码防止乱码)
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
        except UnicodeDecodeError:
            print("⚠️ UTF-8 读取失败，尝试 GBK 编码...")
            df = pd.read_csv(csv_path, encoding='gbk')

        # 2. 检查列名是否正确
        # 你截图里的列名是 'content' 和 'cluster_label'
        required_cols = ['content', 'cluster_label']
        if not set(required_cols).issubset(df.columns):
            print(f"❌ 列名错误！你的CSV必须包含: {required_cols}")
            print(f"   你当前的列名是: {df.columns.tolist()}")
            return []

        # 3. 只保留需要的两列，去除空值
        df = df[required_cols].dropna()

        # 4. 分层抽样 (Stratified Sampling)
        # 从每个 cluster_label 里抽 5 条
        # 如果某类不足 5 条，就全部取出来
        sampled_df = df.groupby('cluster_label', group_keys=False).apply(
            lambda x: x.sample(min(len(x), samples_per_class), random_state=42)
        )

        # 5. 【关键】按 cluster_label 排序
        # 这样喂给智能体时，评论是按话题分块的（比如先全是价格类，再全是服务类...）
        # 这会让折线图出现漂亮的“阶段性波动”
        sampled_df = sampled_df.sort_values('cluster_label')

        print(f"✅ 成功抽取数据：共 {len(sampled_df)} 条")
        print(f"   包含话题类别: {sampled_df['cluster_label'].unique()}")

        # 只返回评论内容的列表给智能体
        return sampled_df['content'].tolist()

    except FileNotFoundError:
        print(f"❌ 找不到文件！请确认文件名是否为: {csv_filename}")
        return []
    except Exception as e:
        print(f"❌ 发生未知错误: {e}")
        return []


# ================= 2. 仿真主逻辑 =================
def run_simulation(comment_list):
    """
    接收评论列表，让所有智能体阅读并反应
    """
    # 初始化智能体
    agents = [Agent(cfg["name"], cfg["desc"]) for cfg in AGENTS_CONFIG]

    full_logs = []
    line_chart_data = {a.name: [] for a in agents}

    print(f"\n🚀 开始仿真：{len(agents)} 个智能体 x {len(comment_list)} 条评论")
    print("-" * 50)

    # 循环交互
    for i, comment in enumerate(comment_list):
        # 简单的进度展示，避免刷屏
        print(f"[{i + 1}/{len(comment_list)}] 正在阅读: {comment[:20]}...")

        for agent in agents:
            # 调用核心模块 (core.py)
            res = agent.perceive(comment)
            if res:
                full_logs.append(res)
                line_chart_data[agent.name].append(res['cumulative_score'])

    return {
        "raw_logs": full_logs,  # 详细日志 (给热力图/桑基图)
        "line_chart": line_chart_data  # 趋势数据 (给折线图)
    }


# ================= 3. 程序入口 =================
if __name__ == "__main__":
    # 请确保这个名字和你截图里的完全一样
    CSV_FILENAME = "allcomments_with_label_processed.csv"

    # 1. 加载并抽样数据
    comments_input = load_sampled_data(CSV_FILENAME, samples_per_class=5)

    # 2. 如果有数据，开始仿真
    if comments_input:
        result = run_simulation(comments_input)

        # 3. 打印第一条结果验证
        if result["raw_logs"]:
            print("\n✅ 仿真完成！输出示例 (第一条日志):")
            print(json.dumps(result["raw_logs"][0], indent=4, ensure_ascii=False))

            # (可选) 保存结果文件，方便以后分析或给前端用
            with open("simulation_result.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
            print("\n💾 完整结果已保存到: simulation_result.json")
    else:
        print("\n⚠️ 无法获取评论数据，程序终止。")