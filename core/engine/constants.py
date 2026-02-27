"""
游戏常量定义 - 统一管理游戏中的魔法数字和字符串
"""

# ============================================
# 规则校验相关常量
# ============================================

class ValidationConstants:
    """规则校验常量"""
    
    # 基础分数
    BASE_PLAUSIBILITY_SCORE = 50
    
    # 分数范围
    MIN_SCORE = 0
    MAX_SCORE = 100
    
    # 各项检查权重（总和应为100）
    ERA_COMPATIBILITY_WEIGHT = 30
    CHARACTER_CONSISTENCY_WEIGHT = 20
    MEMORY_COHERENCE_WEIGHT = 15
    MACRO_INFLUENCE_WEIGHT = 15
    COMMON_SENSE_WEIGHT = 10
    
    # 时代合规性阈值
    ERA_COMPATIBILITY_LOW_THRESHOLD = 0.5
    
    # 人物属性一致性阈值
    CHARACTER_CONSISTENCY_LOW_THRESHOLD = 0.6
    
    # 记忆连贯性阈值
    MEMORY_COHERENCE_THRESHOLD = 0.7
    
    # 常识检查阈值
    COMMON_SENSE_THRESHOLD = 0.8
    
    # 可信度等级阈值
    HIGH_CREDIBILITY_THRESHOLD = 80
    MEDIUM_CREDIBILITY_THRESHOLD = 60
    
    # 职业等级阈值
    CAREER_LEVEL_LOW = 30
    CAREER_LEVEL_HIGH = 70
    
    # 年龄阈值
    WORKING_AGE_MIN = 18
    RETIREMENT_AGE = 65


# ============================================
# 角色状态相关常量
# ============================================

class CharacterConstants:
    """角色状态常量"""
    
    # 初始属性值
    DEFAULT_HEALTH = 80
    DEFAULT_ENERGY = 70
    DEFAULT_APPEARANCE = 60
    DEFAULT_FITNESS = 50
    
    # 心理属性默认值
    DEFAULT_HAPPINESS = 80
    DEFAULT_STRESS = 20
    DEFAULT_RESILIENCE = 60
    
    # 五维人格默认值
    DEFAULT_PERSONALITY_TRAIT = 50
    
    # 社会属性默认值
    DEFAULT_SOCIAL_CAPITAL = 50
    DEFAULT_CREDIT = 70
    
    # 认知属性默认值
    DEFAULT_ACADEMIC_KNOWLEDGE = 40
    DEFAULT_PRACTICAL_KNOWLEDGE = 30
    DEFAULT_CREATIVE_KNOWLEDGE = 50
    DEFAULT_COMMUNICATION_SKILL = 30
    DEFAULT_PROBLEM_SOLVING_SKILL = 40
    DEFAULT_LEADERSHIP_SKILL = 20
    DEFAULT_SHORT_TERM_MEMORY = 70
    DEFAULT_LONG_TERM_MEMORY = 60
    DEFAULT_EMOTIONAL_MEMORY = 80
    
    # 关系属性默认值
    DEFAULT_FAMILY_INTIMACY = 80
    DEFAULT_FRIEND_INTIMACY = 40
    DEFAULT_ROMANTIC_INTIMACY = 0
    DEFAULT_NETWORK_SIZE = 10
    DEFAULT_NETWORK_QUALITY = 60
    DEFAULT_NETWORK_DIVERSITY = 30


# ============================================
# 事件相关常量
# ============================================

class EventConstants:
    """事件相关常量"""
    
    # 默认可信度
    DEFAULT_PLAUSIBILITY = 60
    
    # 默认情感权重
    DEFAULT_EMOTIONAL_WEIGHT = 0.5
    
    # 情感权重阈值
    HIGH_EMOTIONAL_WEIGHT = 0.7
    LOW_EMOTIONAL_WEIGHT = 0.3
    TRAUMA_WEIGHT_THRESHOLD = 0.8
    
    # 事件类型
    EVENT_TYPE_CAREER = "career"
    EVENT_TYPE_RELATIONSHIP = "relationship"
    EVENT_TYPE_HEALTH = "health"
    EVENT_TYPE_EDUCATION = "education"
    EVENT_TYPE_FINANCE = "finance"
    EVENT_TYPE_LIFE = "life"
    
    # 人生阶段
    STAGE_CHILDHOOD = "childhood"
    STAGE_TEEN = "teen"
    STAGE_YOUNG_ADULT = "youngAdult"
    STAGE_ADULT = "adult"
    STAGE_MIDDLE_AGE = "middleAge"
    STAGE_ELDERLY = "elderly"


# ============================================
# 记忆系统相关常量
# ============================================

class MemoryConstants:
    """记忆系统常量"""
    
    # 默认保留度
    DEFAULT_RETENTION = 1.0
    
    # 最小保留度阈值
    MIN_RETENTION_THRESHOLD = 0.3
    
    # 记忆容量限制
    MAX_MEMORIES = 500
    
    # 情感权重阈值（用于记忆巩固）
    IMPORTANT_MEMORY_WEIGHT = 0.7
    
    # 召回次数衰减因子
    RECALL_DECAY_FACTOR = 0.95


# ============================================
# 数据库相关常量
# ============================================

class DatabaseConstants:
    """数据库常量"""
    
    # 连接池大小
    CONNECTION_POOL_SIZE = 5
    
    # 查询缓存大小
    QUERY_CACHE_SIZE = 100
    
    # 缓存过期时间（毫秒）
    CACHE_EXPIRY_MS = 5 * 60 * 1000  # 5分钟
    
    # 批量操作大小
    BATCH_SIZE = 100
    
    # 事件查询默认限制
    DEFAULT_EVENT_LIMIT = 100


# ============================================
# AI模型相关常量
# ============================================

class AIConstants:
    """AI模型常量"""
    
    # 模型缓存最大内存（MB）
    MAX_MODEL_CACHE_MEMORY_MB = 2048
    
    # 本地模型大小选项
    MODEL_SIZE_1_5B = "1.5B"
    MODEL_SIZE_3B = "3B"
    MODEL_SIZE_7B = "7B"
    
    # API超时时间（秒）
    API_TIMEOUT_SECONDS = 30
    
    # 重试次数
    MAX_RETRY_COUNT = 3
    
    # 温度参数
    DEFAULT_TEMPERATURE = 0.7
    CREATIVE_TEMPERATURE = 0.9
    DETERMINISTIC_TEMPERATURE = 0.3


# ============================================
# 游戏设置相关常量
# ============================================

class GameConstants:
    """游戏设置常量"""
    
    # 时代选项
    ERA_21ST_CENTURY = "21世纪"
    ERA_20TH_CENTURY = "20世纪"
    ERA_19TH_CENTURY = "19世纪"
    ERA_MODERN = "现代"
    ERA_ANCIENT = "古代"
    
    # 难度选项
    DIFFICULTY_EASY = "easy"
    DIFFICULTY_NORMAL = "normal"
    DIFFICULTY_HARD = "hard"
    
    # 家庭背景选项
    BACKGROUND_POOR = "poor"
    BACKGROUND_MIDDLE = "middle"
    BACKGROUND_WEALTHY = "wealthy"
    
    # 性别选项
    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    
    # 时间推进默认天数
    DEFAULT_TIME_ADVANCE_DAYS = 1
    
    # 自动保存防抖时间（毫秒）
    AUTO_SAVE_DEBOUNCE_MS = 2000


# ============================================
# 错误消息常量
# ============================================

class ErrorMessages:
    """错误消息常量"""
    
    # API错误
    API_KEY_NOT_CONFIGURED = "未配置API密钥，请在环境变量中设置"
    API_CONNECTION_FAILED = "API连接失败，请检查网络连接"
    API_TIMEOUT = "API请求超时，请稍后重试"
    
    # 数据错误
    DATA_LOAD_FAILED = "数据加载失败"
    DATA_SAVE_FAILED = "数据保存失败"
    PROFILE_NOT_FOUND = "未找到角色档案"
    
    # 验证错误
    INVALID_AGE = "年龄无效，请输入有效年龄"
    INVALID_DATE = "日期格式无效"
    INVALID_GENDER = "性别选项无效"
    
    # 游戏错误
    GAME_NOT_INITIALIZED = "游戏未初始化，请先创建角色"
    EVENT_GENERATION_FAILED = "事件生成失败，请重试"


# ============================================
# 日志消息常量
# ============================================

class LogMessages:
    """日志消息常量"""
    
    # 系统启动
    SYSTEM_INITIALIZING = "开始初始化无限人生系统..."
    SYSTEM_INITIALIZED = "系统初始化完成"
    
    # API配置
    API_CONFIGURED = "[AI] 已配置的API: {}"
    API_NOT_CONFIGURED = "[AI] 警告: 未配置任何API密钥，请在环境变量中设置"
    
    # 规则加载
    RULES_LOADED = "[OK] 成功加载 {} 条规则"
    RULES_LOAD_FAILED = "[WARN] 规则加载失败，使用默认规则: {}"
    
    # 游戏操作
    PROFILE_CREATED = "创建角色档案: {}"
    GAME_SAVED = "游戏已保存"
    GAME_LOADED = "游戏已加载: {}"