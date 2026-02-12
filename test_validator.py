#!/usr/bin/env python3
"""
规则校验引擎测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.engine.validator import RuleValidator, GameEvent, CharacterState, EraRules
from datetime import datetime

def test_rule_validator():
    """测试规则校验引擎"""
    print("=== 开始规则校验引擎测试 ===")
    
    # 创建规则校验器
    validator = RuleValidator()
    
    # 测试1: 创建测试数据
    print("\n1. 创建测试数据...")
    
    # 创建时代规则
    era_rules = EraRules("modern", historicalEvents=[
        {"event": "互联网普及", "year": 2000},
        {"event": "智能手机革命", "year": 2010}
    ])
    
    # 创建角色状态
    state = CharacterState(
        id="state_001",
        profile_id="profile_001",
        current_date="2025-01-01",
        age=25,
        dimensions={
            "physical": {"health": 85, "energy": 90, "appearance": 75, "fitness": 80},
            "psychological": {"openness": 70, "conscientiousness": 65, "extraversion": 60, 
                              "agreeableness": 75, "neuroticism": 40, "happiness": 70, 
                              "stress": 30, "resilience": 70},
            "social": {"socialCapital": 60, "career": {"level": 65, "satisfaction": 70, "income": 50}, 
                        "economic": {"wealth": 45, "debt": 20, "credit": 75}},
            "cognitive": {"knowledge": {"academic": 70, "practical": 65, "creative": 75}, 
                           "skills": {"communication": 70, "problemSolving": 75, "leadership": 60}, 
                           "memory": {"shortTerm": 80, "longTerm": 75, "emotional": 70}},
            "relational": {"intimacy": {"family": 80, "friends": 70, "romantic": 65}, 
                           "network": {"size": 50, "quality": 75, "diversity": 70}}
        },
        location="北京",
        occupation="软件工程师",
        education="本科",
        life_stage="youngAdult",
        total_events=100,
        total_decisions=80,
        days_survived=9125
    )
    
    # 创建测试事件
    test_event = GameEvent(
        id="event_001",
        profile_id="profile_001",
        event_date="2025-01-01",
        event_type="opportunity",
        title="职业晋升机会：高级软件工程师",
        description="公司提供高级软件工程师职位，需要承担更多技术领导责任",
        narrative="在一次团队会议上，你的技术总监注意到了你的出色表现，邀请你申请高级工程师职位。",
        choices=[
            {
                "id": 1,
                "text": "接受挑战，申请晋升",
                "riskLevel": 30,
                "immediateImpacts": [{"dimension": "social", "subDimension": "career.level", "change": 5}],
                "longTermEffects": ["职业发展加速", "收入提升"]
            },
            {
                "id": 2,
                "text": "保持现状，继续积累经验",
                "riskLevel": 10,
                "immediateImpacts": [{"dimension": "psychological", "subDimension": "stress", "change": -5}],
                "longTermEffects": ["稳步发展", "减少压力"]
            }
        ],
        impacts=[{"dimension": "social", "subDimension": "career.level", "change": 3}],
        is_completed=False,
        selected_choice=None,
        plausibility=80,
        emotional_weight=0.6,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    print("[OK] 测试数据创建成功")
    
    # 测试2: 合理性评分计算
    print("\n2. 测试合理性评分计算...")
    
    result = validator.calculate_plausibility(test_event, state, era_rules)
    
    print(f"[OK] 合理性评分: {result.plausibility}/100")
    print(f"[INFO] 冲突: {result.conflicts}")
    print(f"[INFO] 警告: {result.warnings}")
    print(f"[INFO] 建议: {result.suggestions}")
    
    # 测试3: 影响计算
    print("\n3. 测试影响计算...")
    
    impacts = validator.calculate_impacts(test_event, state)
    
    print(f"[OK] 计算完成，影响维度: {len(impacts)} 个")
    for key, value in impacts.items():
        print(f"   - {key}: {value:.2f}")
    
    # 测试4: 适用规则获取
    print("\n4. 测试适用规则获取...")
    
    applicable_rules = validator._get_applicable_rules(test_event, state)
    
    print(f"[OK] 找到 {len(applicable_rules)} 条适用规则")
    for rule in applicable_rules:
        print(f"   - {rule.get('id', 'Unknown')}: {rule.get('name', 'Unknown')}")
    
    # 测试5: 不同事件类型测试
    print("\n5. 测试不同事件类型...")
    
    # 创建高情感强度事件
    trauma_event = GameEvent(
        id="event_002",
        profile_id="profile_001",
        event_date="2025-01-02",
        event_type="crisis",
        title="重大交通事故",
        description="遭遇严重交通事故，需要住院治疗",
        narrative="在下班回家的路上，你遭遇了严重的交通事故，车辆严重损坏，需要紧急医疗救治。",
        choices=[
            {
                "id": 1,
                "text": "积极配合治疗，争取早日康复",
                "riskLevel": 20,
                "immediateImpacts": [{"dimension": "physical", "subDimension": "health", "change": -30}],
                "longTermEffects": ["康复过程", "心理恢复"]
            }
        ],
        impacts=[{"dimension": "physical", "subDimension": "health", "change": -25}],
        is_completed=False,
        selected_choice=None,
        plausibility=70,
        emotional_weight=0.9,  # 高情感强度
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    trauma_result = validator.calculate_plausibility(trauma_event, state, era_rules)
    print(f"[OK] 创伤事件合理性评分: {trauma_result.plausibility}/100")
    
    # 测试6: 规则缓存检查
    print("\n6. 测试规则缓存...")
    
    print(f"[INFO] 已加载规则类别: {list(validator.rules_cache.keys())}")
    for category, rules in validator.rules_cache.items():
        print(f"   - {category}: {len(rules)} 条规则")
    
    print("\n=== 规则校验引擎测试完成 ===")
    print("[OK] 所有测试通过！")

if __name__ == "__main__":
    test_rule_validator()