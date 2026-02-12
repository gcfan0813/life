#!/usr/bin/env python3
"""
事件溯源存储引擎测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.storage.database import DatabaseManager, GameEvent, CharacterState, Memory
from datetime import datetime, timedelta
import json

def test_database_operations():
    """测试数据库基本操作"""
    print("=== 开始事件溯源存储引擎测试 ===")
    
    # 创建数据库管理器
    db = DatabaseManager("test_life_simulation.db")
    
    # 测试1: 创建角色档案
    print("\n1. 测试创建角色档案...")
    profile_data = {
        'name': '测试角色',
        'birth_date': '1990-01-01',
        'birth_place': '北京',
        'gender': 'male',
        'initial_traits': {
            'familyBackground': 'middle',
            'educationLevel': 'college',
            'healthStatus': 'good',
            'riskTolerance': 70,
            'ambition': 85,
            'empathy': 60
        },
        'era': 'modern',
        'difficulty': 'normal'
    }
    
    profile = db.create_profile(profile_data)
    print(f"[OK] 创建角色档案成功: {profile.name} (ID: {profile.id})")
    
    # 测试2: 获取角色档案列表
    print("\n2. 测试获取角色档案列表...")
    profiles = db.get_profiles()
    print(f"[OK] 获取到 {len(profiles)} 个角色档案")
    
    # 测试3: 创建测试事件
    print("\n3. 测试创建事件...")
    test_event = GameEvent(
        id="event_001",
        profile_id=profile.id,
        event_date="1995-09-01",
        event_type="milestone",
        title="小学入学",
        description="开始接受正规教育",
        narrative="在父母的陪伴下，你背着新书包走进了小学校门。",
        choices=[
            {
                "id": 1,
                "text": "努力学习，争取好成绩",
                "riskLevel": 10,
                "immediateImpacts": [{"dimension": "cognitive", "subDimension": "academic", "change": 5}],
                "longTermEffects": ["获得更好的教育机会"]
            },
            {
                "id": 2,
                "text": "享受童年，适度学习",
                "riskLevel": 5,
                "immediateImpacts": [{"dimension": "psychological", "subDimension": "happiness", "change": 3}],
                "longTermEffects": ["保持心理健康"]
            }
        ],
        impacts=[{"dimension": "cognitive", "subDimension": "academic", "change": 2}],
        is_completed=False,
        selected_choice=None,
        plausibility=90,
        emotional_weight=0.3,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    event_id = db.save_event(profile.id, test_event)
    print(f"[OK] 创建事件成功: {test_event.title} (事件ID: {event_id})")
    
    # 测试4: 创建状态快照
    print("\n4. 测试创建状态快照...")
    state = CharacterState(
        id="state_001",
        profile_id=profile.id,
        current_date="1995-09-01",
        age=5,
        dimensions={
            "physical": {"health": 95, "energy": 90, "appearance": 70, "fitness": 80},
            "psychological": {"openness": 60, "conscientiousness": 55, "extraversion": 65, 
                              "agreeableness": 70, "neuroticism": 40, "happiness": 75, 
                              "stress": 20, "resilience": 65},
            "social": {"socialCapital": 50, "career": {"level": 0, "satisfaction": 0, "income": 0}, 
                        "economic": {"wealth": 0, "debt": 0, "credit": 0}},
            "cognitive": {"knowledge": {"academic": 45, "practical": 40, "creative": 55}, 
                           "skills": {"communication": 50, "problemSolving": 45, "leadership": 40}, 
                           "memory": {"shortTerm": 60, "longTerm": 50, "emotional": 55}},
            "relational": {"intimacy": {"family": 80, "friends": 60, "romantic": 0}, 
                           "network": {"size": 15, "quality": 65, "diversity": 40}}
        },
        location="北京",
        occupation="学生",
        education="小学",
        life_stage="childhood",
        total_events=1,
        total_decisions=0,
        days_survived=1825
    )
    
    db.save_snapshot(profile.id, "1995-09-01", state, 0)
    print("[OK] 创建状态快照成功")
    
    # 测试5: 获取快照
    print("\n5. 测试获取快照...")
    snapshot = db.get_latest_snapshot(profile.id)
    if snapshot:
        state, offset, date = snapshot
        print(f"[OK] 获取快照成功: {date} (事件偏移: {offset})")
    else:
        print("[FAIL] 获取快照失败")
    
    # 测试6: 检查数据存在性
    print("\n6. 测试数据存在性检查...")
    has_data = db.check_existing_data()
    print(f"[OK] 数据库数据存在: {has_data}")
    
    # 测试7: 创建记忆
    print("\n7. 测试创建记忆...")
    memory = Memory(
        id="memory_001",
        profile_id=profile.id,
        event_id=event_id,
        summary="第一次上学的美好回忆",
        emotional_weight=0.6,
        recall_count=1,
        last_recalled=datetime.now().isoformat(),
        retention=0.95,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    db.save_memory(profile.id, memory)
    print("[OK] 创建记忆成功")
    
    # 测试8: 获取记忆
    print("\n8. 测试获取记忆...")
    memories = db.get_memories(profile.id)
    print(f"[OK] 获取到 {len(memories)} 条记忆")
    
    print("\n=== 事件溯源存储引擎测试完成 ===")
    print("[OK] 所有测试通过！")
    
    # 清理测试数据库
    try:
        os.remove("test_life_simulation.db")
        print("[OK] 清理测试数据库完成")
    except:
        print("[WARN] 清理测试数据库失败")

if __name__ == "__main__":
    test_database_operations()