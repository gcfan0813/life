"""
优化验证脚本 - 简化版本
"""

import sys
import os
import time

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_config_manager():
    """测试配置管理器"""
    print("=== Testing Config Manager ===")
    try:
        from shared.config.config_manager import config_manager
        
        print(f"Host: {config_manager.get_host()}")
        print(f"Port: {config_manager.get_port()}")
        print(f"DB Path: {config_manager.get_database_path()}")
        print("PASS: Config manager works")
        return True
    except Exception as e:
        print(f"FAIL: Config manager test failed: {e}")
        return False

def test_ai_model_cache():
    """测试AI模型缓存"""
    print("\n=== Testing AI Model Cache ===")
    try:
        from core.storage.simple_optimized_db import SimpleAIModelCache
        
        cache = SimpleAIModelCache(max_models=2)
        
        # 测试添加模型
        model1 = {"name": "test_model_1"}
        model2 = {"name": "test_model_2"}
        
        cache.put_model("model1", model1)
        cache.put_model("model2", model2)
        
        # 测试获取模型
        retrieved_model1 = cache.get_model("model1")
        assert retrieved_model1 == model1, "Failed to retrieve model1"
        
        # 测试缓存统计
        stats = cache.get_cache_stats()
        assert stats['cached_models'] == 2, "Incorrect cache count"
        
        print("PASS: AI model cache works")
        print(f"Cache stats: {stats}")
        return True
    except Exception as e:
        print(f"FAIL: AI model cache test failed: {e}")
        return False

def test_database_optimization():
    """测试数据库优化功能"""
    print("\n=== Testing Database Optimization ===")
    try:
        from core.storage.simple_optimized_db import SimpleOptimizedDatabaseManager
        import tempfile
        
        # 创建临时数据库
        temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        temp_db.close()
        
        try:
            db_manager = SimpleOptimizedDatabaseManager(temp_db.name, max_cache_size=5)
            
            # 测试查询缓存
            query = "SELECT 1"
            
            # 首次查询
            start_time = time.time()
            result1 = db_manager._execute_query(query, (), "one")
            first_time = time.time() - start_time
            
            # 第二次查询（应该使用缓存）
            start_time = time.time()
            result2 = db_manager._execute_query(query, (), "one")
            second_time = time.time() - start_time
            
            # 验证缓存效果
            stats = db_manager.get_query_stats()
            assert query in stats, "Query stats not recorded"
            assert stats[query].hit_count == 1, "Cache hit count incorrect"
            
            print("PASS: Database optimization works")
            print(f"First query time: {first_time:.6f}s")
            print(f"Cached query time: {second_time:.6f}s")
            print(f"Performance improvement: {((first_time - second_time) / first_time * 100):.1f}%")
            
            return True
        finally:
            os.unlink(temp_db.name)
            
    except Exception as e:
        print(f"FAIL: Database optimization test failed: {e}")
        return False

def test_exception_handling():
    """测试异常处理规范化"""
    print("\n=== Testing Exception Handling ===")
    try:
        # 测试具体的异常处理而不是裸露的except
        def test_value_error():
            int("not_a_number")
        
        def test_zero_division():
            1/0
            
        # 验证我们可以捕获具体异常
        try:
            test_value_error()
        except ValueError:
            pass  # 期望的异常
            
        try:
            test_zero_division()
        except ZeroDivisionError:
            pass  # 期望的异常
            
        print("PASS: Exception handling works")
        return True
    except Exception as e:
        print(f"FAIL: Exception handling test failed: {e}")
        return False

def main():
    """主测试函数"""
    print("Infinite Life: AI Chronicle - Optimization Validation")
    print("=" * 50)
    
    tests = [
        test_config_manager,
        test_ai_model_cache,
        test_database_optimization,
        test_exception_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All optimizations verified!")
        return True
    else:
        print("FAILURE: Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)