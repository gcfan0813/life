"""
统一配置管理器
集中管理所有配置项，提供类型安全的配置访问
"""

import os
from typing import Dict, Any, Optional
from .api_config import API_CONFIG, AI_SERVICES, DATABASE_CONFIG, PERFORMANCE_CONFIG


class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self._configs = {
            'api': API_CONFIG,
            'ai': AI_SERVICES,
            'database': DATABASE_CONFIG,
            'performance': PERFORMANCE_CONFIG
        }
        
        # 环境变量覆盖
        self._load_env_overrides()
    
    def _load_env_overrides(self):
        """从环境变量加载配置覆盖"""
        # API配置覆盖
        if 'API_HOST' in os.environ:
            self._configs['api']['host'] = os.environ['API_HOST']
        if 'API_PORT' in os.environ:
            self._configs['api']['port'] = int(os.environ['API_PORT'])
            
        # 数据库配置覆盖
        if 'DB_PATH' in os.environ:
            self._configs['database']['path'] = os.environ['DB_PATH']
            
        # AI配置覆盖
        if 'DEFAULT_AI_MODEL' in os.environ:
            self._configs['ai']['default_model'] = os.environ['DEFAULT_AI_MODEL']
    
    def get_api_config(self) -> Dict[str, Any]:
        """获取API配置"""
        return self._configs['api']
    
    def get_ai_config(self) -> Dict[str, Any]:
        """获取AI服务配置"""
        return self._configs['ai']
    
    def get_database_config(self) -> Dict[str, Any]:
        """获取数据库配置"""
        return self._configs['database']
    
    def get_performance_config(self) -> Dict[str, Any]:
        """获取性能配置"""
        return self._configs['performance']
    
    def get_host(self) -> str:
        """获取主机地址"""
        return self._configs['api']['host']
    
    def get_port(self) -> int:
        """获取端口号"""
        return self._configs['api']['port']
    
    def get_database_path(self) -> str:
        """获取数据库路径"""
        return self._configs['database']['path']
    
    def get_default_ai_model(self) -> str:
        """获取默认AI模型"""
        return self._configs['ai']['default_model']
    
    def get_max_tokens(self) -> int:
        """获取最大token数"""
        return self._configs['ai']['max_tokens']
    
    def get_temperature(self) -> float:
        """获取温度参数"""
        return self._configs['ai']['temperature']
    
    def get_cors_origins(self) -> list:
        """获取CORS源列表"""
        return self._configs['api']['cors_origins']
    
    def get_api_prefix(self) -> str:
        """获取API前缀"""
        return self._configs['api']['api_prefix']
    
    def is_debug_mode(self) -> bool:
        """检查是否为调试模式"""
        return bool(self._configs['api']['debug'])


# 全局配置管理器实例
config_manager = ConfigManager()