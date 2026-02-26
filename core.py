# agent_system/core.py
import json
import re
from openai import OpenAI
from config import API_KEY, BASE_URL, MODEL_NAME, MEMORY_DECAY, IMPACT_SCALE

# 初始化 API 客户端
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


class Agent:
    def __init__(self, name, persona_desc):
        self.name = name
        self.persona_desc = persona_desc
        self.current_score = 0.0  # 初始好感度

    def _build_system_prompt(self):
        """构建给 AI 看的系统指令"""
        return f"""
        你现在进行一场社会学仿真实验。
        【你的人设】：你叫{self.name}。{self.persona_desc}

        【当前状态】：你对XX外卖的好感度是 {self.current_score:.2f} (范围 -1.0讨厌 ~ 1.0喜欢)。

        【任务】：
        你将阅读一条关于外卖平台的真实用户评论。
        请代入人设，输出 JSON 格式（不要包含Markdown代码块），包含字段：
        1. topic_category: 话题类型 ("价格", "时效", "服务", "杀熟", "其他")
        2. reaction: 内心独白 (30字内)
        3. sentiment_shift: 好感度变化值 (-5 到 +5)
        4. action: 行为 ("A"=下载/切换, "B"=观望, "C"=放弃/坚守)
        5. reason: 决策理由
        """

    def _parse_json(self, text):
        """清洗 AI 返回的脏数据"""
        try:
            # 1. 尝试直接解析
            return json.loads(text)
        except:
            # 2. 如果 AI 加了 ```json，用正则提取大括号里的内容
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return None  # 解析失败

    def perceive(self, comment):
        """阅读评论并产生反应"""
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": self._build_system_prompt()},
                    {"role": "user", "content": f"评论内容：【{comment}】"}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}  # 强制 JSON
            )

            content = response.choices[0].message.content
            result = self._parse_json(content)

            if not result: return None

            # 数值计算逻辑
            shift = result.get("sentiment_shift", 0)
            normalized_shift = shift / IMPACT_SCALE

            # 记忆更新公式
            self.current_score = self.current_score * MEMORY_DECAY + normalized_shift
            self.current_score = max(-1.0, min(1.0, self.current_score))

            # 组装返回数据
            return {
                "agent_name": self.name,
                "topic_category": result.get("topic_category", "其他"),
                "reaction": result.get("reaction", ""),
                "sentiment_shift": shift,
                "action": result.get("action", "B"),
                "reason": result.get("reason", ""),
                "cumulative_score": round(self.current_score, 2)
            }

        except Exception as e:
            print(f"⚠️ [{self.name}] API调用失败: {e}")
            return None