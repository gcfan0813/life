"""
模拟引擎测试
"""

import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from core.engine.character import character_initializer
from core.engine.simulation import simulation_engine
from core.storage.database import db_manager

# 测试数据
TEST_PROFILE_DATA = {
    "name": "测试角色",
    "birth_date": "1990-01-01",
    "birth_place": "北京",
    "gender": "male",
    "initial_traits": {
        "familyBackground": "middle",
        "educationLevel": "college",
        "healthStatus": "good",
        "riskTolerance": 60,
        "ambition": 70,
        "empathy": 50
    },
    "era": "现代中国",
    "difficulty": "normal"
}

async def test_character_initialization():
    """测试角色初始化"""
    print("测试角色初始化...")
    
    try:
        # 创建测试档案
        profile = db_manager.create_profile(TEST_PROFILE_DATA)
        print("[OK] 创建档案成功:", profile.name)
        
        # 初始化角色状态
        state = await character_initializer.initialize_character_state(profile)
        print("[OK] 初始化角色状态成功")
        print("   角色年龄:", state.age, "岁")
        print("   人生阶段:", state.life_stage)
        print("   健康值:", state.dimensions['physiological']['health'])
        print("   幸福感:", state.dimensions['psychological']['happiness'])
        
        return profile, state
        
    except Exception as e:
        print("[FAIL] 角色初始化测试失败:", e)
        return None, None

async def test_time_advancement(profile, state):
    """测试时间推进"""
    print("\n测试时间推进...")
    
    try:
        # 推进30天
        result = await simulation_engine.advance_time(profile.id, state, 30)
        
        print("[OK] 时间推进成功")
        print("   新日期:", result.new_date)
        print("   新年龄:", result.new_state.age, "岁")
        print("   生成事件数:", len(result.new_events))
        print("   生成记忆数:", len(result.new_memories))
        print("   AI推理:", result.reasoning)
        
        # 显示生成的事件
        for i, event in enumerate(result.new_events[:3]):  # 只显示前3个事件
            print("   事件" + str(i+1) + ":", event.title, "(可信度:", event.plausibility, "%)")
        
        return result
        
    except Exception as e:
        print("[FAIL] 时间推进测试失败:", e)
        return None

async def test_decision_making(profile, state, event):
    """测试决策处理"""
    print("\n测试决策处理...")
    
    try:
        # 处理第一个选择
        if event.choices:
            result = await simulation_engine.process_decision(
                profile.id, state, event.id, 0
            )
            
            print("[OK] 决策处理成功")
            print("   决策总数:", result.new_state.total_decisions)
            print("   即时影响:", len(result.immediate_effects), "个")
            print("   长期效果:", result.long_term_effects)
            
            return result
        else:
            print("[WARN] 事件无选择项，跳过决策测试")
            return None
            
    except Exception as e:
        print("[FAIL] 决策处理测试失败:", e)
        return None

def test_database_operations():
    """测试数据库操作"""
    print("\n测试数据库操作...")
    
    try:
        # 检查数据存在性
        has_data = db_manager.check_existing_data()
        print("[OK] 数据库检查:", "有数据" if has_data else "无数据")
        
        # 获取档案列表
        profiles = db_manager.get_profiles()
        print("[OK] 档案数量:", len(profiles))
        
        return True
        
    except Exception as e:
        print("[FAIL] 数据库操作测试失败:", e)
        return False

def test_rule_validation():
    """测试规则验证"""
    print("\n测试规则验证...")
    
    try:
        from core.engine.validator import rule_validator
        
        # 创建测试事件
        test_event = type('GameEvent', (), {
            'title': '互联网创业机会',
            'description': '在2020年发现了一个互联网创业机会',
            'emotional_weight': 0.8,
            'impacts': [{'dimension': 'social', 'subDimension': 'careerLevel', 'change': 10}]
        })()
        
        # 创建测试状态
        test_state = type('CharacterState', (), {
            'age': 25,
            'dimensions': {
                'social': {'career': {'level': 50}}
            }
        })()
        
        # 创建测试时代规则
        test_era = type('EraRules', (), {
            'era': '现代中国',
            'historicalEvents': ['科技革命']
        })()
        
        # 计算合理性
        validation_result = rule_validator.calculate_plausibility(test_event, test_state, test_era)
        
        print("[OK] 规则验证成功")
        print("   事件合理性:", validation_result.plausibility, "%")
        print("   冲突数量:", len(validation_result.conflicts))
        print("   警告数量:", len(validation_result.warnings))
        print("   建议:", validation_result.suggestions[0] if validation_result.suggestions else "无")
        
        return True
        
    except Exception as e:
        print("[FAIL] 规则验证测试失败:", e)
        return False

async def run_all_tests():
    """运行所有测试"""
    print("开始模拟引擎综合测试")
    print("=" * 50)
    
    # 测试数据库
    db_test_passed = test_database_operations()
    
    # 测试规则验证
    rule_test_passed = test_rule_validation()
    
    # 测试角色初始化
    profile, state = await test_character_initialization()
    
    if profile and state:
        # 测试时间推进
        time_result = await test_time_advancement(profile, state)
        
        if time_result and time_result.new_events:
            # 测试决策处理
            await test_decision_making(profile, state, time_result.new_events[0])
    
    print("\n" + "=" * 50)
    print("测试结果总结:")
    
    tests_passed = [
        ("数据库操作", db_test_passed),
        ("规则验证", rule_test_passed),
        ("角色初始化", profile is not None),
        ("时间推进", time_result is not None)
    ]
    
    passed_count = sum(1 for _, passed in tests_passed if passed)
    total_count = len(tests_passed)
    
    for test_name, passed in tests_passed:
        status = "[PASS]" if passed else "[FAIL]"
        print("   " + test_name + ": " + status)
    
    print("\n总体结果: " + str(passed_count) + "/" + str(total_count) + " 项测试通过")
    
    if passed_count == total_count:
        print("所有测试通过！模拟引擎功能正常")
    else:
        print("部分测试失败，请检查相关功能")

if __name__ == "__main__":
    # 运行测试
    asyncio.run(run_all_tests())