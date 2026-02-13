"""
简化的优化数据库查询管理器
提供基础的缓存和性能监控功能
"""

import sqlite3
import json
import time
import threading
from typing import Dict, List, Optional, Any
from collections import OrderedDict
from dataclasses import dataclass


@dataclass
class QueryStats:
    """查询统计信息"""
    query: str
    execution_time: float
    hit_count: int
    avg_execution_time: float


class SimpleOptimizedDatabaseManager:
    """简化的优化数据库管理器"""
    
    def __init__(self, db_path: str = "life_simulation.db", max_cache_size: int = 50):
        self.db_path = db_path
        self.max_cache_size = max_cache_size
        self.query_cache = OrderedDict()  # LRU缓存
        self.stats = {}  # 查询统计
        self.lock = threading.Lock()
    
    def _execute_query(self, query: str, params: tuple = (), fetch_method: str = "all") -> Any:
        """执行查询并收集统计信息"""
        start_time = time.time()
        
        # 检查缓存
        cache_key = f"{query}:{params}"
        if cache_key in self.query_cache:
            self.stats.setdefault(query, QueryStats(query, 0, 1, 0))
            self.stats[query].hit_count += 1
            return self.query_cache[cache_key]
        
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            if fetch_method == "one":
                result = cursor.fetchone()
            elif fetch_method == "all":
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.lastrowid
            
            # 缓存结果
            if fetch_method in ["one", "all"] and len(self.query_cache) < self.max_cache_size:
                self.query_cache[cache_key] = result
                # LRU: 移动到末尾
                self.query_cache.move_to_end(cache_key)
                
                # 如果超出缓存大小，删除最旧的
                if len(self.query_cache) > self.max_cache_size:
                    self.query_cache.popitem(last=False)
            
            return result
            
        finally:
            conn.close()
            execution_time = time.time() - start_time
            
            # 更新统计信息
            if query not in self.stats:
                self.stats[query] = QueryStats(query, execution_time, 0, execution_time)
            else:
                stat = self.stats[query]
                stat.execution_time = execution_time
                stat.avg_execution_time = (stat.avg_execution_time * stat.hit_count + execution_time) / (stat.hit_count + 1)
    
    def get_query_stats(self) -> Dict[str, QueryStats]:
        """获取查询统计信息"""
        return self.stats
    
    def clear_cache(self):
        """清空查询缓存"""
        self.query_cache.clear()
    
    # 优化的查询方法
    def get_profile_with_recent_events(self, profile_id: str, limit: int = 10) -> Optional[Dict[str, Any]]:
        """获取角色档案及其最近的事件"""
        # 先获取档案信息
        profile_query = "SELECT * FROM life_profile WHERE id = ?"
        profile_result = self._execute_query(profile_query, (profile_id,), "one")
        
        if not profile_result:
            return None
            
        profile_data = dict(zip(['id', 'name', 'birth_date', 'birth_place', 'gender', 
                               'initial_traits', 'era', 'difficulty', 'created_at', 'updated_at'], 
                              profile_result))
        
        # 获取最近的事件
        events_query = """
            SELECT id, event_date, title, description, is_completed, selected_choice 
            FROM event_log 
            WHERE profile_id = ? 
            ORDER BY event_date DESC 
            LIMIT ?
        """
        events_result = self._execute_query(events_query, (profile_id, limit), "all")
        
        profile_data['events'] = [dict(zip(['id', 'event_date', 'title', 'description', 
                                          'is_completed', 'selected_choice'], row)) 
                                for row in events_result] if events_result else []
        
        return profile_data
    
    def get_events_by_date_range(self, profile_id: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """按日期范围获取事件"""
        query = """
            SELECT * FROM event_log 
            WHERE profile_id = ? AND event_date BETWEEN ? AND ?
            ORDER BY event_date ASC
        """
        results = self._execute_query(query, (profile_id, start_date, end_date), "all")
        columns = ['id', 'profile_id', 'event_date', 'event_type', 'title', 'description', 
                  'narrative', 'choices', 'impacts', 'is_completed', 'selected_choice', 
                  'plausibility', 'emotional_weight', 'created_at']
        return [dict(zip(columns, row)) for row in results] if results else []


# AI模型缓存管理器
class SimpleAIModelCache:
    """简化的AI模型缓存管理器"""
    
    def __init__(self, max_models: int = 3):
        self.max_models = max_models
        self.model_cache = {}
        self.access_times = {}
        self.lock = threading.Lock()
    
    def put_model(self, model_key: str, model: Any):
        """放入模型到缓存"""
        with self.lock:
            # 如果超出限制，清理旧模型
            if len(self.model_cache) >= self.max_models:
                oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
                self.remove_model(oldest_key)
            
            self.model_cache[model_key] = model
            self.access_times[model_key] = time.time()
    
    def get_model(self, model_key: str) -> Optional[Any]:
        """从缓存获取模型"""
        with self.lock:
            if model_key in self.model_cache:
                self.access_times[model_key] = time.time()
                return self.model_cache[model_key]
            return None
    
    def remove_model(self, model_key: str):
        """移除指定模型"""
        with self.lock:
            if model_key in self.model_cache:
                del self.model_cache[model_key]
                del self.access_times[model_key]
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        with self.lock:
            return {
                'cached_models': len(self.model_cache),
                'max_models': self.max_models,
                'usage_percentage': (len(self.model_cache) / self.max_models) * 100
            }


# 全局实例
optimized_db_manager = SimpleOptimizedDatabaseManager()
ai_model_cache = SimpleAIModelCache()