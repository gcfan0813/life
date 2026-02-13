"""
优化的数据库查询管理器
提供缓存、批处理和性能监控功能
"""

import sqlite3
import json
import time
import threading
from typing import Dict, List, Optional, Any, Callable
from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class QueryStats:
    """查询统计信息"""
    query: str
    execution_time: float
    hit_count: int
    avg_execution_time: float


class OptimizedDatabaseManager:
    """优化的数据库管理器"""
    
    def __init__(self, db_path: str = "life_simulation.db", max_cache_size: int = 100):
        self.db_path = db_path
        self.max_cache_size = max_cache_size
        self.query_cache = OrderedDict()  # LRU缓存
        self.stats = {}  # 查询统计
        self.connection_pool = []  # 连接池
        self.lock = threading.Lock()
        
        # 初始化数据库
        self._init_database()
        
    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接（带连接池）"""
        with self.lock:
            if self.connection_pool:
                return self.connection_pool.pop()
            else:
                conn = sqlite3.connect(self.db_path, check_same_thread=False)
                conn.row_factory = sqlite3.Row  # 使用字典形式访问结果
                return conn
    
    def _return_connection(self, conn: sqlite3.Connection):
        """归还数据库连接到池中"""
        with self.lock:
            if len(self.connection_pool) < 5:  # 最多保持5个连接
                self.connection_pool.append(conn)
            else:
                conn.close()
    
    def _execute_with_stats(self, query: str, params: tuple = (), fetch_method: str = "all") -> Any:
        """执行查询并收集统计信息"""
        start_time = time.time()
        
        # 检查缓存
        cache_key = f"{query}:{params}"
        if cache_key in self.query_cache:
            self.stats.setdefault(query, QueryStats(query, 0, 0, 0))
            self.stats[query].hit_count += 1
            return self.query_cache[cache_key]
        
        conn = self._get_connection()
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
            self._return_connection(conn)
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
    
    def batch_execute(self, queries: List[tuple]) -> List[Any]:
        """批量执行查询"""
        results = []
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            for query, params in queries:
                cursor.execute(query, params)
                if query.strip().upper().startswith('SELECT'):
                    results.append(cursor.fetchall())
                else:
                    results.append(cursor.lastrowid)
            conn.commit()
            return results
        finally:
            self._return_connection(conn)
    
    # 优化的查询方法
    def get_profile_with_events(self, profile_id: str, limit: int = 50) -> Dict[str, Any]:
        """获取角色档案及其最近的事件（单次查询）"""
        query = """
            SELECT p.*, 
                   json_group_array(
                       json_object(
                           'id', e.id,
                           'event_date', e.event_date,
                           'title', e.title,
                           'description', e.description,
                           'is_completed', e.is_completed,
                           'selected_choice', e.selected_choice
                       )
                   ) as events
            FROM life_profile p
            LEFT JOIN (
                SELECT * FROM event_log 
                WHERE profile_id = ? 
                ORDER BY event_date DESC 
                LIMIT ?
            ) e ON p.id = e.profile_id
            WHERE p.id = ?
            GROUP BY p.id
        """
        
        result = self._execute_with_stats(query, (profile_id, limit, profile_id), "one")
        if result:
            profile_data = dict(result)
            # 解析事件数组
            try:
                profile_data['events'] = json.loads(profile_data['events']) if profile_data['events'] else []
            except:
                profile_data['events'] = []
            return profile_data
        return None
    
    def get_events_by_date_range(self, profile_id: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """按日期范围获取事件"""
        query = """
            SELECT * FROM event_log 
            WHERE profile_id = ? AND event_date BETWEEN ? AND ?
            ORDER BY event_date ASC
        """
        results = self._execute_with_stats(query, (profile_id, start_date, end_date), "all")
        return [dict(row) for row in results] if results else []
    
    def get_statistics_summary(self, profile_id: str) -> Dict[str, Any]:
        """获取统计数据摘要"""
        query = """
            SELECT 
                COUNT(*) as total_events,
                SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) as completed_events,
                AVG(emotional_weight) as avg_emotional_weight,
                MAX(event_date) as last_event_date,
                MIN(event_date) as first_event_date
            FROM event_log 
            WHERE profile_id = ?
        """
        result = self._execute_with_stats(query, (profile_id,), "one")
        return dict(result) if result else {}


# AI模型缓存管理器
class AIModelCache:
    """AI模型缓存管理器"""
    
    def __init__(self, max_memory_mb: int = 2048):
        self.max_memory_mb = max_memory_mb
        self.model_cache = {}
        self.access_times = {}
        self.memory_usage = {}
        self.lock = threading.Lock()
    
    def put_model(self, model_key: str, model: Any, memory_mb: int):
        """放入模型到缓存"""
        with self.lock:
            # 如果超出内存限制，清理旧模型
            if sum(self.memory_usage.values()) + memory_mb > self.max_memory_mb:
                self._evict_models()
            
            self.model_cache[model_key] = model
            self.access_times[model_key] = time.time()
            self.memory_usage[model_key] = memory_mb
    
    def get_model(self, model_key: str) -> Optional[Any]:
        """从缓存获取模型"""
        with self.lock:
            if model_key in self.model_cache:
                self.access_times[model_key] = time.time()
                return self.model_cache[model_key]
            return None
    
    def _evict_models(self):
        """驱逐最少使用的模型"""
        if not self.access_times:
            return
            
        # 按访问时间排序，驱逐最旧的
        oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
        self.remove_model(oldest_key)
    
    def remove_model(self, model_key: str):
        """移除指定模型"""
        with self.lock:
            if model_key in self.model_cache:
                del self.model_cache[model_key]
                del self.access_times[model_key]
                del self.memory_usage[model_key]
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        with self.lock:
            return {
                'cached_models': len(self.model_cache),
                'total_memory_mb': sum(self.memory_usage.values()),
                'max_memory_mb': self.max_memory_mb,
                'usage_percentage': (sum(self.memory_usage.values()) / self.max_memory_mb) * 100
            }


# 全局实例
db_manager_optimized = OptimizedDatabaseManager()
ai_model_cache = AIModelCache()


def _init_database(self):
    """初始化数据库表结构（简化版本）"""
    conn = self._get_connection()
    try:
        cursor = conn.cursor()
        
        # 确保必要的表存在
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS life_profile (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                birth_place TEXT NOT NULL,
                gender TEXT NOT NULL,
                initial_traits TEXT NOT NULL,
                era TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS event_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id TEXT NOT NULL,
                event_date TEXT NOT NULL,
                event_type TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                narrative TEXT NOT NULL,
                choices TEXT NOT NULL,
                impacts TEXT NOT NULL,
                is_completed INTEGER DEFAULT 0,
                selected_choice INTEGER,
                plausibility INTEGER DEFAULT 60,
                emotional_weight REAL DEFAULT 0.5,
                created_at TEXT NOT NULL
            )
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_event_log_profile_date ON event_log(profile_id, event_date)")
        
        conn.commit()
    finally:
        self._return_connection(conn)


# 为类添加方法
OptimizedDatabaseManager._init_database = _init_database