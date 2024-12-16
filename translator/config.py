"""
Anthropic
"""

# 柏拉图AI注册链接
link = "https://api.bltcy.ai/register?aff=q3ue"

# 柏拉图AI转发地址
BLT_BASE_URL_1 = "https://api.bltcy.cn/v1"  # 国内请求地址，屏蔽海外流量
BLT_BASE_URL_2 = "https://api.bltcy.ai/v1"  # 主站 (美国集群 国内极速访问)

# 模型名称
CLAUDE_3_5_HAIKU = "claude-3-5-haiku-20241022"
CLAUDE_3_5_SONNET = "claude-3-5-sonnet-20241022"
CLAUDE_3_5_LATEST = "claude-3-5-sonnet-latest"
GPT_4O_MINI = "gpt-4o-mini"
GPT_4O = "gpt-4o"

PRICE_PER_1K_TOKENS_BLT = {
    GPT_4O_MINI: {"prompt": 0.000375, "completion": 0.0015},
    GPT_4O: {"prompt": 0.00625, "completion": 0.025},
    CLAUDE_3_5_LATEST: {
        "prompt": 0.015 * 1.1,
        "completion": 0.075 * 1.1,
    },
    CLAUDE_3_5_HAIKU: {"prompt": 0.0002 * 1.1, "completion": 0.01 * 1.1},
}
