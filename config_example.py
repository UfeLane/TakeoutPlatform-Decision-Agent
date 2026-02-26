
# ================= API 设置 =================
# 填入您的 API 密钥（切勿上传包含真实密钥的文件到 GitHub！）
API_KEY = "YOUR_DEEPSEEK_API_KEY_HERE"
BASE_URL = "https://api.deepseek.com"
MODEL_NAME = "deepseek-chat"

# ================= 仿真参数 =================
# 记忆衰退系数 (0.8表示每次保留 80% 的旧情绪)
MEMORY_DECAY = 0.8

# 单次情感冲击的归一化系数 (防止分数溢出)
IMPACT_SCALE = 10.0