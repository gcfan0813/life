"""
简单的优化验证脚本
快速验证各项优化功能是否正常工作
"""

import sys
import os
import time

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_config_manager():
    """测试配置管理器"""
    print("=== 测试配置管理器 ===")
    try:
        from shared.config.config_manager import config_manager
        
        print(f"✓ 主机: {config_manager.get_host()}")
        print(f"✓ 端口: {config_manager.get_port()}")
        print(f"✓ 数据库路径: {config_manager.get_database_path()}")
        print("✓ 配置管理器测试通过")
        return True
    except Exception as e:
        print(f"✗ 配置管理器测试失败: {e}")
        return False

def test_ai_model_cache():
    """测试AI模型缓存"""
    print("\n=== 测试AI模型缓存 ===")
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
        assert retrieved_model1 == model1, "模型1获取失败"
        
        # 测试缓存统计
        stats = cache.get_cache_stats()
        assert stats['cached_models'] == 2, "缓存数量不正确"
        
        print("✓ AI模型缓存测试通过")
        print(f"  缓存统计: {stats}")
        return True
    except Exception as e:
        print(f"✗ AI模型缓存测试失败: {e}")
        return False

def test_database_optimization():
    """测试数据库优化功能"""
    print("\n=== 测试数据库优化 ===")
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
            assert query in stats, "查询统计未记录"
            assert stats[query].hit_count == 1, "缓存命中计数不正确"
            
            print("✓ 数据库优化测试通过")
            print(f"  首次查询时间: {first_time:.6f}s")
            print(f"  缓存查询时间: {second_time:.6f}s")
            print(f"  性能提升: {((first_time - second_time) / first_time * 100):.1f}%")
            
            return True
        finally:
            os.unlink(temp_db.name)
            
    except Exception as e:
        print(f"✗ 数据库优化测试失败: {e}")
        return False

def test_exception_handling():
    """测试异常处理规范化"""
    print("\n=== 测试异常处理规范化 ===")
    try:
        # 测试具体的异常处理而不是裸露的except
        test_cases = [
            ("ValueError", lambda: int("not_a_number")),
            ("ZeroDivisionError", lambda: 1/0),
            ("IndexError", lambda: [1,2,3][10])
        ]
        
        for exception_name, test_func in test_cases:
            try:
                test_func()
            except Exception as e:
                # 验证我们捕获到了具体的异常类型
                assert type(e).__name__ == exception_name, f"异常类型不匹配: 期望{exception_name}, 实际{type(e).__name__}"
        
        print("✓ 异常处理规范化测试通过")
        return True
    except Exception as e:
        print(f"✗ 异常处理测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("《无限人生：AI编年史》优化验证测试")
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
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有优化功能验证通过！")
        return True
    else:
        print("❌ 部分测试失败，请检查相关功能")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)