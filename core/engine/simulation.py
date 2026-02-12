"""
核心模拟引擎 - 整合AI推演和规则校验
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ai.generator import ai_generator, AIReasoningResult
from core.engine.validator import rule_validator, RuleValidationResult
from core.storage.database import db_manager

# 临时类型定义
class CharacterState:
    def __init__(self, id, profile_id, current_date, age, dimensions, location, occupation, education, life_stage, total_events, total_decisions, days_survived):
        self.id = id
        self.profile_id = profile_id
        self.current_date = current_date
        self.age = age
        self.dimensions = dimensions
        self.location = location
        self.occupation = occupation
        self.education = education
        self.life_stage = life_stage
        self.total_events = total_events
        self.total_decisions = total_decisions
        self.days_survived = days_survived

class GameEvent:
    def __init__(self, id, profile_id, event_date, event_type, title, description, narrative, choices, impacts, is_completed, selected_choice, plausibility, emotional_weight, created_at, updated_at):
        self.id = id
        self.profile_id = profile_id
        self.event_date = event_date
        self.event_type = event_type
        self.title = title
        self.description = description
        self.narrative = narrative
        self.choices = choices
        self.impacts = impacts
        self.is_completed = is_completed
        self.selected_choice = selected_choice
        self.plausibility = plausibility
        self.emotional_weight = emotional_weight
        self.created_at = created_at
        self.updated_at = updated_at

class Memory:
    def __init__(self, id, profile_id, event_id, summary, emotional_weight, recall_count, last_recalled, retention, created_at, updated_at):
        self.id = id
        self.profile_id = profile_id
        self.event_id = event_id
        self.summary = summary
        self.emotional_weight = emotional_weight
        self.recall_count = recall_count
        self.last_recalled = last_recalled
        self.retention = retention
        self.created_at = created_at
        self.updated_at = updated_at

class SimulationResult:
    def __init__(self, new_state, new_events, new_memories, new_date, reasoning=None):
        self.new_state = new_state
        self.new_events = new_events
        self.new_memories = new_memories
        self.new_date = new_date
        self.reasoning = reasoning

class DecisionResult:
    def __init__(self, new_state, new_memories, immediate_effects, long_term_effects):
        self.new_state = new_state
        self.new_memories = new_memories
        self.immediate_effects = immediate_effects
        self.long_term_effects = long_term_effects

class SimulationEngine:
    """核心模拟引擎"""
    
    def __init__(self):
        self.ai_generator = ai_generator
        self.rule_validator = rule_validator
        self.db_manager = db_manager
        
    async def advance_time(self, profile_id: str, current_state: CharacterState, days: int = 1) -> SimulationResult:
        """推进时间模拟"""
        
        # 1. 使用AI生成未来事件
        model_level = self._determine_model_level(current_state)
        ai_result = await self.ai_generator.generate_events(current_state, days, model_level)
        
        # 2. 使用规则校验优化事件
        validated_events = []
        for event in ai_result.candidateEvents:
            # 检查事件合理性
            validation_result = self.rule_validator.calculate_plausibility(event, current_state, self._get_era_rules(current_state))
            
            # 如果事件可信度足够高，则采用
            if validation_result.plausibility >= 60:
                # 调整事件可信度
                event.plausibility = validation_result.plausibility
                validated_events.append(event)
        
        # 3. 更新角色状态
        new_state = self._update_character_state(current_state, validated_events, days)
        
        # 4. 生成记忆
        new_memories = self._generate_memories(profile_id, validated_events)
        
        # 5. 更新日期
        new_date = self._calculate_new_date(current_state.current_date, days)
        
        # 6. 保存事件和状态
        for event in validated_events:
            self.db_manager.save_event(profile_id, event)
        
        self.db_manager.save_snapshot(profile_id, new_date, new_state, len(validated_events))
        
        return SimulationResult(
            new_state=new_state,
            new_events=validated_events,
            new_memories=new_memories,
            new_date=new_date,
            reasoning=ai_result.reasoning
        )
    
    async def process_decision(self, profile_id: str, current_state: CharacterState, event_id: str, choice_index: int) -> DecisionResult:
        """处理用户决策"""
        
        # 1. 获取事件
        event = self._get_event_by_id(profile_id, event_id)
        if not event:
            raise ValueError(f"事件 {event_id} 不存在")
        
        # 2. 验证选择有效性
        if choice_index < 0 or choice_index >= len(event.choices):
            raise ValueError("无效的选择索引")
        
        selected_choice = event.choices[choice_index]
        
        # 3. 应用即时影响
        immediate_effects = self._apply_immediate_effects(current_state, selected_choice)
        
        # 4. 更新角色状态
        new_state = self._update_state_with_effects(current_state, immediate_effects)
        
        # 5. 生成记忆
        new_memories = self._generate_decision_memory(profile_id, event, choice_index)
        
        # 6. 标记事件为已完成
        event.is_completed = True
        event.selected_choice = choice_index
        
        # 7. 保存更新
        self.db_manager.save_event(profile_id, event)
        
        return DecisionResult(
            new_state=new_state,
            new_memories=new_memories,
            immediate_effects=immediate_effects,
            long_term_effects=selected_choice.longTermEffects
        )
    
    def _determine_model_level(self, state: CharacterState) -> str:
        """确定AI模型级别"""
        # 基于角色状态和设置确定模型级别
        # 简化实现：根据年龄和职业等级决定
        
        if state.age < 18:
            return 'L0'  # 青少年使用模板
        elif state.dimensions.get('social', {}).get('career', {}).get('level', 0) > 70:
            return 'L2'  # 高职业等级使用API
        else:
            return 'L1'  # 默认使用本地模型
    
    def _get_era_rules(self, state: CharacterState) -> Dict[str, Any]:
        """获取时代规则"""
        # 简化实现：根据出生年份确定时代
        birth_year = int(state.current_date.split('-')[0]) - state.age
        
        if birth_year < 1900:
            return {'era': '19世纪', 'historicalEvents': ['工业革命', '辛亥革命']}
        elif birth_year < 1950:
            return {'era': '20世纪上半叶', 'historicalEvents': ['二战', '新中国成立']}
        elif birth_year < 1980:
            return {'era': '20世纪下半叶', 'historicalEvents': ['改革开放', '互联网兴起']}
        else:
            return {'era': '21世纪', 'historicalEvents': ['科技革命', '全球化']}
    
    def _update_character_state(self, current_state: CharacterState, events: List[GameEvent], days: int) -> CharacterState:
        """更新角色状态"""
        new_state = CharacterState(
            id=current_state.id,
            profile_id=current_state.profile_id,
            current_date=self._calculate_new_date(current_state.current_date, days),
            age=current_state.age + days/365.25,  # 更新年龄
            dimensions=current_state.dimensions.copy(),
            location=current_state.location,
            occupation=current_state.occupation,
            education=current_state.education,
            life_stage=self._determine_life_stage(current_state.age + days/365.25),
            total_events=current_state.total_events + len(events),
            total_decisions=current_state.total_decisions,
            days_survived=current_state.days_survived + days
        )
        
        # 应用事件影响
        for event in events:
            impacts = self.rule_validator.calculate_impacts(event, current_state)
            for key, change in impacts.items():
                dimension, sub_dimension = key.split('.')
                if dimension in new_state.dimensions:
                    if sub_dimension in new_state.dimensions[dimension]:
                        new_state.dimensions[dimension][sub_dimension] += change
        
        # 确保数值在合理范围内
        self._normalize_dimensions(new_state.dimensions)
        
        return new_state
    
    def _generate_memories(self, profile_id: str, events: List[GameEvent]) -> List[Memory]:
        """生成记忆"""
        memories = []
        now = datetime.now().isoformat()
        
        for event in events:
            if event.emotional_weight > 0.3:  # 只保存情感权重较高的记忆
                memory = Memory(
                    id=f"memory_{event.id}",
                    profile_id=profile_id,
                    event_id=event.id,
                    summary=f"关于{event.title}的记忆",
                    emotional_weight=event.emotional_weight,
                    recall_count=0,
                    last_recalled=None,
                    retention=1.0,
                    created_at=now,
                    updated_at=now
                )
                memories.append(memory)
        
        return memories
    
    def _calculate_new_date(self, current_date: str, days: int) -> str:
        """计算新日期"""
        current = datetime.fromisoformat(current_date)
        new_date = current + timedelta(days=days)
        return new_date.isoformat().split('T')[0]
    
    def _determine_life_stage(self, age: float) -> str:
        """确定人生阶段"""
        if age < 13:
            return 'childhood'
        elif age < 20:
            return 'teen'
        elif age < 35:
            return 'youngAdult'
        elif age < 50:
            return 'adult'
        elif age < 65:
            return 'middleAge'
        else:
            return 'senior'
    
    def _normalize_dimensions(self, dimensions: Dict[str, Any]):
        """规范化维度数值"""
        for dimension, sub_dimensions in dimensions.items():
            if isinstance(sub_dimensions, dict):
                for key, value in sub_dimensions.items():
                    if isinstance(value, (int, float)):
                        # 确保数值在0-100范围内
                        dimensions[dimension][key] = max(0, min(100, value))
    
    def _get_event_by_id(self, profile_id: str, event_id: str) -> GameEvent:
        """根据ID获取事件"""
        # 简化实现：从数据库获取
        # 实际应该查询数据库
        return None
    
    def _apply_immediate_effects(self, state: CharacterState, choice) -> Dict[str, float]:
        """应用即时影响"""
        effects = {}
        
        for impact in choice.immediateImpacts:
            try:
                dimension = impact.get('dimension', '')
                sub_dimension = impact.get('subDimension', '')
                change = impact.get('change', 0)
                
                if dimension and sub_dimension:
                    key = f"{dimension}.{sub_dimension}"
                    effects[key] = change
            except:
                continue
        
        return effects
    
    def _update_state_with_effects(self, state: CharacterState, effects: Dict[str, float]) -> CharacterState:
        """使用效果更新状态"""
        new_state = CharacterState(
            id=state.id,
            profile_id=state.profile_id,
            current_date=state.current_date,
            age=state.age,
            dimensions=state.dimensions.copy(),
            location=state.location,
            occupation=state.occupation,
            education=state.education,
            life_stage=state.life_stage,
            total_events=state.total_events,
            total_decisions=state.total_decisions + 1,
            days_survived=state.days_survived
        )
        
        for key, change in effects.items():
            dimension, sub_dimension = key.split('.')
            if dimension in new_state.dimensions:
                if sub_dimension in new_state.dimensions[dimension]:
                    new_state.dimensions[dimension][sub_dimension] += change
        
        self._normalize_dimensions(new_state.dimensions)
        return new_state
    
    def _generate_decision_memory(self, profile_id: str, event: GameEvent, choice_index: int) -> List[Memory]:
        """生成决策记忆"""
        now = datetime.now().isoformat()
        
        memory = Memory(
            id=f"decision_{event.id}_{choice_index}",
            profile_id=profile_id,
            event_id=event.id,
            summary=f"在{event.title}中选择了{event.choices[choice_index].text}",
            emotional_weight=event.emotional_weight * 1.2,  # 决策记忆更深刻
            recall_count=0,
            last_recalled=None,
            retention=1.0,
            created_at=now,
            updated_at=now
        )
        
        return [memory]

# 全局模拟引擎实例
simulation_engine = SimulationEngine()