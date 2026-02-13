"""
优化模块测试套件
验证各项优化功能的正确性和性能提升
"""

import unittest
import time
import tempfile
import os
import sys
from unittest.mock import Mock, patch

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.storage.simple_optimized_db import SimpleOptimizedDatabaseManager, SimpleAIModelCache
from shared.config.config_manager import config_manager


class TestOptimizedDatabaseManager(unittest.TestCase):
    """测试优化的数据库管理器"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        self.db_manager = SimpleOptimizedDatabaseManager(self.temp_db.name, max_cache_size=10)
    
    def tearDown(self):
        """测试后清理"""
        os.unlink(self.temp_db.name)
    
    def test_query_caching(self):
        """测试查询缓存功能"""
        # 执行相同查询两次
        query = "SELECT 1"
        result1 = self.db_manager._execute_query(query, (), "one")
        result2 = self.db_manager._execute_query(query, (), "one")
        
        # 检查第二次查询应该是缓存命中
        stats = self.db_manager.get_query_stats()
        self.assertIn(query, stats)
        self.assertEqual(stats[query].hit_count, 1)
    
    def test_cache_eviction(self):
        """测试缓存驱逐机制"""
        # 执行超过缓存大小的不同查询
        for i in range(15):
            query = f"SELECT {i}"
            self.db_manager._execute_query(query, (), "one")
        
        # 检查缓存大小限制
        self.assertLessEqual(len(self.db_manager.query_cache), 10)
    
    def test_get_profile_with_events(self):
        """测试获取角色和事件的组合查询"""
        # 这个测试需要真实的数据库表结构
        # 在实际环境中可以测试完整的功能
        pass
    
    def test_clear_cache(self):
        """测试清空缓存功能"""
        # 添加一些缓存项
        self.db_manager._execute_query("SELECT 1", (), "one")
        self.db_manager._execute_query("SELECT 2", (), "one")
        
        # 清空缓存
        self.db_manager.clear_cache()
        
        # 检查缓存是否清空
        self.assertEqual(len(self.db_manager.query_cache), 0)


class TestAIModelCache(unittest.TestCase):
    """测试AI模型缓存"""
    
    def setUp(self):
        """测试前准备"""
        self.cache = SimpleAIModelCache(max_models=3)
    
    def test_model_caching(self):
        """测试模型缓存功能"""
        model1 = Mock()
        model2 = Mock()
        
        # 添加模型到缓存
        self.cache.put_model("model1", model1)
        self.cache.put_model("model2", model2)
        
        # 验证可以从缓存获取
        retrieved_model1 = self.cache.get_model("model1")
        self.assertIs(retrieved_model1, model1)
        
        retrieved_model2 = self.cache.get_model("model2")
        self.assertIs(retrieved_model2, model2)
    
    def test_cache_eviction_lru(self):
        """测试LRU缓存驱逐"""
        # 添加3个模型（达到上限）
        for i in range(3):
            self.cache.put_model(f"model{i}", Mock())
        
        # 访问第一个模型使其变为最近使用
        self.cache.get_model("model0")
        
        # 添加第4个模型，应该驱逐model1（最久未使用）
        self.cache.put_model("model3", Mock())
        
        # 验证model1被驱逐，model0仍在缓存中
        self.assertIsNone(self.cache.get_model("model1"))
        self.assertIsNotNone(self.cache.get_model("model0"))
    
    def test_cache_stats(self):
        """测试缓存统计功能"""
        # 添加一些模型
        self.cache.put_model("model1", Mock())
        self.cache.put_model("model2", Mock())
        
        stats = self.cache.get_cache_stats()
        self.assertEqual(stats['cached_models'], 2)
        self.assertEqual(stats['max_models'], 3)
        self.assertAlmostEqual(stats['usage_percentage'], 66.67, places=2)


class TestConfigManager(unittest.TestCase):
    """测试配置管理器"""
    
    def test_default_values(self):
        """测试默认配置值"""
        self.assertEqual(config_manager.get_host(), "localhost")
        self.assertEqual(config_manager.get_port(), 8000)
        self.assertEqual(config_manager.get_database_path(), "life_simulation.db")
    
    def test_environment_override(self):
        """测试环境变量覆盖"""
        with patch.dict(os.environ, {'API_PORT': '3000', 'DB_PATH': '/tmp/test.db'}):
            # 重新创建配置管理器以获取环境变量
            from importlib import reload
            import shared.config.config_manager
            reload(shared.config.config_manager)
            from shared.config.config_manager import config_manager
            
            self.assertEqual(config_manager.get_port(), 3000)
            self.assertEqual(config_manager.get_database_path(), "/tmp/test.db")


class TestPerformanceImprovements(unittest.TestCase):
    """性能改进测试"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        self.db_manager = SimpleOptimizedDatabaseManager(self.temp_db.name)
    
    def tearDown(self):
        """测试后清理"""
        os.unlink(self.temp_db.name)
    
    def test_cache_performance(self):
        """测试缓存带来的性能提升"""
        query = "SELECT sqlite_version()"
        
        # 首次查询（无缓存）
        start_time = time.time()
        result1 = self.db_manager._execute_query(query, (), "one")
        first_time = time.time() - start_time
        
        # 第二次查询（使用缓存）
        start_time = time.time()
        result2 = self.db_manager._execute_query(query, (), "one")
        second_time = time.time() - start_time
        
        # 缓存查询应该更快
        self.assertLess(second_time, first_time)
        
        # 结果应该相同
        self.assertEqual(result1, result2)


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)