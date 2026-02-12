"""
API配置设置
"""

API_CONFIG = {
    "host": "localhost",
    "port": 8000,
    "debug": True,
    "cors_origins": [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    "api_prefix": "/api",
    "version": "1.0.0"
}

# AI服务配置
AI_SERVICES = {
    "local_models": {
        "1.5B": "qwen2.5-1.5b-instruct-q4_k_m.gguf",
        "3B": "qwen2.5-3b-instruct-q4_k_m.gguf", 
        "7B": "qwen2.5-7b-instruct-q4_k_m.gguf"
    },
    "free_apis": [
        "https://api.siliconflow.cn/v1",  # 硅基流动
        "https://open.bigmodel.cn/api/paas/v4",  # 智谱AI
        "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat",  # 百度文心
        "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"  # 阿里通义
    ],
    "default_model": "1.5B",
    "max_tokens": 2000,
    "temperature": 0.7
}

# 数据库配置
DATABASE_CONFIG = {
    "path": "life_simulation.db",
    "timeout": 30,
    "check_same_thread": False
}

# 性能配置
PERFORMANCE_CONFIG = {
    "max_events_per_day": 3,
    "max_memories": 1000,
    "auto_save_interval": 300,  # 5分钟
    "cache_ttl": 3600  # 1小时
}