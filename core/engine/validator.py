"""
规则校验引擎 - 负责验证AI生成事件的合理性
"""

import json
import math
from typing import List, Dict, Any, Tuple
from datetime import datetime

from ..shared.types import GameEvent, CharacterState, EraRules, RuleValidationResult

class RuleValidator:
    """规则校验引擎"""
    
    def __init__(self, rules_path: str = "shared/rules/"):
        self.rules_path = rules_path
        self.rules_cache = {}
        self._load_rules()
    
    def _load_rules(self):
        """加载规则库"""
        # 这里简化实现，实际应从文件系统加载
        self.rules_cache = {
            'physiological': self._load_physiological_rules(),
            'psychological': self._load_psychological_rules(),
            'social': self._load_social_rules(),
            'cognitive': self._load_cognitive_rules(),
            'relational': self._load_relational_rules()
        }
    
    def _load_physiological_rules(self) -> List[Dict]:
        """加载生理规则"""
        return [
            {
                "id": "PHY-AGING-01",
                "name": "基础衰老曲线",
                "condition": "age >= 30",
                "impact": {"physiological": {"health": -0.1, "energy": -0.05}}
            }
        ]
    
    def _load_psychological_rules(self) -> List[Dict]:
        """加载心理规则"""
        return [
            {
                "id": "PSY-TRAUMA-01", 
                "name": "创伤事件影响",
                "condition": "event.emotional_weight > 0.8",
                "impact": {"psychological": {"neuroticism": 0.1, "resilience": -0.05}}
            }
        ]
    
    def _load_social_rules(self) -> List[Dict]:
        """加载社会规则"""
        return [
            {
                "id": "SOC-CAREER-01",
                "name": "职业晋升条件",
                "condition": "state.dimensions.social.careerLevel > 70 and state.age > 25",
                "impact": {"social": {"careerLevel": 0.05, "economicStatus": 0.1}}
            }
        ]
    
    def _load_cognitive_rules(self) -> List[Dict]:
        """加载认知规则"""
        return []
    
    def _load_relational_rules(self) -> List[Dict]:
        """加载关系规则"""
        return []
    
    def calculate_plausibility(self, event: GameEvent, state: CharacterState, era_rules: EraRules) -> RuleValidationResult:
        """计算事件合理性评分"""
        score = 50  # 基础分
        conflicts = []
        warnings = []
        suggestions = []
        
        # 1. 时代合规性检查 (±30)
        era_score = self._check_era_compatibility(event, era_rules)
        score += era_score * 30
        
        if era_score < 0.5:
            conflicts.append(f"事件与{era_rules.era}时代背景不符")
        
        # 2. 人物属性一致性检查 (±20)
        character_score = self._check_character_consistency(event, state)
        score += character_score * 20
        
        if character_score < 0.6:
            warnings.append("事件与角色当前状态存在较大偏差")
        
        # 3. 历史记忆连贯性检查 (±15)
        memory_score = self._check_memory_coherence(event, state)
        score -= (1 - memory_score) * 15
        
        if memory_score < 0.7:
            warnings.append("事件与近期记忆存在冲突")
        
        # 4. 宏观事件影响检查 (±15)
        macro_score = self._check_macro_influence(event, era_rules)
        score += macro_score * 15
        
        # 5. 基础常识检查 (±10)
        common_sense_score = self._check_common_sense(event)
        score += common_sense_score * 10
        
        if common_sense_score < 0.8:
            conflicts.append("事件存在基本常识性错误")
        
        # 确保分数在0-100范围内
        score = max(0, min(100, score))
        
        # 根据分数提供建议
        if score >= 80:
            suggestions.append("事件高度可信，可直接采用")
        elif score >= 60:
            suggestions.append("事件基本可信，建议微调")
        else:
            suggestions.append("事件可信度较低，建议重新生成")
        
        return RuleValidationResult(
            plausibility=score,
            conflicts=conflicts,
            warnings=warnings,
            suggestions=suggestions
        )
    
    def _check_era_compatibility(self, event: GameEvent, era_rules: EraRules) -> float:
        """检查时代合规性"""
        era = era_rules.era
        
        # 简化实现：检查事件类型是否与时代匹配
        if era.startswith('19'):
            # 19世纪事件限制
            if '互联网' in event.title or '智能手机' in event.description:
                return 0.1
            return 0.9
        elif era.startswith('20'):
            # 20世纪事件限制  
            if '人工智能' in event.title and '2020' not in era:
                return 0.3
            return 0.8
        else:
            # 21世纪及以后
            return 1.0
    
    def _check_character_consistency(self, event: GameEvent, state: CharacterState) -> float:
        """检查人物属性一致性"""
        score = 1.0
        
        # 检查职业相关性
        if hasattr(event, 'career_related') and event.career_related:
            career_level = state.dimensions.social.careerLevel
            if career_level < 30 and '高级职位' in event.title:
                score *= 0.3
            elif career_level > 70 and '初级职位' in event.title:
                score *= 0.5
        
        # 检查年龄适宜性
        age = state.age
        if age < 18 and '工作' in event.title:
            score *= 0.2
        elif age > 65 and '高强度' in event.description:
            score *= 0.4
        
        return score
    
    def _check_memory_coherence(self, event: GameEvent, state: CharacterState) -> float:
        """检查历史记忆连贯性"""
        # 简化实现：基于近期事件检查连贯性
        recent_events = state.recentEvents
        
        if len(recent_events) == 0:
            return 1.0
        
        # 检查事件情感连续性
        emotional_state = state.dimensions.psychological.emotionalState
        
        if event.emotional_weight > 0.7 and emotional_state > 50:
            # 高情绪事件出现在积极情绪状态下
            return 0.9
        elif event.emotional_weight < 0.3 and emotional_state < -30:
            # 低情绪事件出现在消极情绪状态下  
            return 0.9
        else:
            return 0.7
    
    def _check_macro_influence(self, event: GameEvent, era_rules: EraRules) -> float:
        """检查宏观事件影响"""
        # 简化实现：检查事件是否与历史大事相关
        historical_events = era_rules.historicalEvents
        
        for he in historical_events:
            if he.event in event.description or he.event in event.title:
                return 1.0  # 与历史事件相关，加分
        
        return 0.5
    
    def _check_common_sense(self, event: GameEvent) -> float:
        """基础常识检查"""
        score = 1.0
        
        # 检查明显矛盾
        contradictions = [
            ('健康', '生病'),
            ('富有', '贫穷'), 
            ('年轻', '年老'),
            ('成功', '失败')
        ]
        
        for positive, negative in contradictions:
            if positive in event.title and negative in event.description:
                score *= 0.1
        
        # 检查时间逻辑
        if '未来' in event.title and '回忆' in event.description:
            score *= 0.3
        
        return score
    
    def calculate_impacts(self, event: GameEvent, state: CharacterState) -> Dict[str, float]:
        """精确计算AI预测的影响"""
        impacts = {}
        
        # 应用事件本身的影响
        for impact in event.impacts:
            dimension = impact.dimension
            sub_dimension = impact.subDimension
            change = impact.change
            
            # 累积影响
            key = f"{dimension}.{sub_dimension}"
            impacts[key] = impacts.get(key, 0) + change
        
        # 应用规则约束的影响
        for rule in self._get_applicable_rules(event, state):
            rule_impacts = rule.get('impact', {})
            for dimension, changes in rule_impacts.items():
                for sub_dimension, change in changes.items():
                    key = f"{dimension}.{sub_dimension}"
                    impacts[key] = impacts.get(key, 0) + change
        
        return impacts
    
    def _get_applicable_rules(self, event: GameEvent, state: CharacterState) -> List[Dict]:
        """获取适用的规则"""
        applicable_rules = []
        
        for dimension_rules in self.rules_cache.values():
            for rule in dimension_rules:
                if self._evaluate_condition(rule.get('condition', ''), event, state):
                    applicable_rules.append(rule)
        
        return applicable_rules
    
    def _evaluate_condition(self, condition: str, event: GameEvent, state: CharacterState) -> bool:
        """评估规则条件"""
        if not condition:
            return True
        
        # 简化实现：实际应使用安全的表达式求值
        try:
            # 这里使用简单的字符串匹配
            if 'age >' in condition:
                age_threshold = int(condition.split('age >')[1].strip())
                return state.age > age_threshold
            elif 'emotional_weight >' in condition:
                weight_threshold = float(condition.split('emotional_weight >')[1].strip())
                return event.emotional_weight > weight_threshold
            
            return True
        except:
            return False

# 全局规则校验器实例
rule_validator = RuleValidator()