"""
Anthropic
"""

# CloseAI转发地址
ANTHROPIC_BASE_URL_1 = "https://api.openai-proxy.org/anthropic"  # 【主力域名】推荐线上服务使用，全球CDN加速
ANTHROPIC_BASE_URL_2 = "https://api.openai-proxy.live/anthropic"  # 【备用域名】基于Cloudflare的备用域名，有100秒超时限制，建议仅供首选域名无法访问时使用
ANTHROPIC_BASE_URL_3 = "https://api.closeai-proxy.xyz/anthropic"  # 【国内专用】针对国内做过全链路优化，但承载力较低，推荐个人客户端使用

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
        "prompt": 0.015 * 1.4055,
        "completion": 0.075 * 1.4055,
    },
    CLAUDE_3_5_HAIKU: {"prompt": 0.0002 * 1.4055, "completion": 0.01 * 1.4055},
}
