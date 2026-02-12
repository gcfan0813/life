"""
规则校验引擎 - 负责验证AI生成事件的合理性
"""

import json
import math
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Any, Tuple
from datetime import datetime

from typing import List, Dict, Any, Tuple
import json
from datetime import datetime

# 临时类型定义
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

class EraRules:
    def __init__(self, era, historicalEvents=None):
        self.era = era
        self.historicalEvents = historicalEvents or []

class RuleValidationResult:
    def __init__(self, plausibility, conflicts, warnings, suggestions):
        self.plausibility = plausibility
        self.conflicts = conflicts
        self.warnings = warnings
        self.suggestions = suggestions

class RuleValidator:
    """规则校验引擎"""
    
    def __init__(self, rules_path: str = "shared/rules/"):
        self.rules_path = rules_path
        self.rules_cache = {}
        self._load_rules()
    
    def _load_rules(self):
        """加载规则库"""
        try:
            # 尝试加载全面规则库
            comprehensive_file = "shared/rules/comprehensive_rules.json"
            base_file = "shared/rules/base_rules.json"
            extended_file = "shared/rules/extended_rules.json"
            
            total_rules = 0
            self.rules_cache = {}
            
            # 加载全面规则库
            try:
                with open(comprehensive_file, 'r', encoding='utf-8') as f:
                    comprehensive_data = json.load(f)
                
                # 解析全面规则库结构
                categories = comprehensive_data.get('categories', {})
                for cat_name, cat_data in categories.items():
                    if cat_name not in self.rules_cache:
                        self.rules_cache[cat_name] = []
                    
                    # 处理子类别
                    if 'subcategories' in cat_data:
                        for subcat_name, subcat_data in cat_data['subcategories'].items():
                            rules = subcat_data.get('rules', [])
                            for rule in rules:
                                rule['category'] = cat_name
                                rule['subcategory'] = subcat_name
                                self.rules_cache[cat_name].append(rule)
                                total_rules += 1
                    elif 'rules' in cat_data:
                        rules = cat_data['rules']
                        for rule in rules:
                            rule['category'] = cat_name
                            self.rules_cache[cat_name].append(rule)
                            total_rules += 1
                
                # 加载元规则
                meta_rules = comprehensive_data.get('meta_rules', {})
                if meta_rules:
                    self.rules_cache['meta'] = meta_rules.get('rules', [])
                    total_rules += len(self.rules_cache['meta'])
                
                # 加载特殊条件规则
                special_rules = comprehensive_data.get('special_conditions', {})
                if special_rules:
                    self.rules_cache['special'] = special_rules.get('rules', [])
                    total_rules += len(self.rules_cache['special'])
                
                print(f"[OK] 成功加载 {total_rules} 条规则 (全面规则库)")
                return
                
            except FileNotFoundError:
                pass
            
            # 回退到基础规则库
            with open(base_file, 'r', encoding='utf-8') as f:
                rules_data = json.load(f)
            
            for rule in rules_data.get('rules', []):
                category = rule.get('category', 'other')
                if category not in self.rules_cache:
                    self.rules_cache[category] = []
                self.rules_cache[category].append(rule)
                total_rules += 1
            
            # 加载扩展规则库
            try:
                with open(extended_file, 'r', encoding='utf-8') as f:
                    extended_data = json.load(f)
                
                categories = extended_data.get('categories', {})
                for cat_name, cat_data in categories.items():
                    if cat_name not in self.rules_cache:
                        self.rules_cache[cat_name] = []
                    for rule in cat_data.get('rules', []):
                        rule['category'] = cat_name
                        self.rules_cache[cat_name].append(rule)
                        total_rules += 1
                
                # 元规则
                for rule in extended_data.get('meta_rules', []):
                    if 'meta' not in self.rules_cache:
                        self.rules_cache['meta'] = []
                    self.rules_cache['meta'].append(rule)
                    total_rules += 1
            except FileNotFoundError:
                pass
                
            print(f"[OK] 成功加载 {total_rules} 条规则")
            
        except Exception as e:
            print(f"[WARN] 规则加载失败，使用默认规则: {e}")
            # 使用默认规则
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
    
    def _check_era_compatibility(self, event: GameEvent, era_rules) -> float:
        """检查时代合规性"""
        try:
            era = era_rules.get('era', '') if isinstance(era_rules, dict) else era_rules.era
        except:
            era = '现代'
        
        # 简化实现：检查事件类型是否与时代匹配
        if '19' in era or '古代' in era:
            # 19世纪事件限制
            if '互联网' in event.title or '智能手机' in event.description:
                return 0.1
            return 0.9
        elif '20' in era:
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
        try:
            career_level = 0
            if 'social' in state.dimensions:
                social_dim = state.dimensions['social']
                if 'career' in social_dim and isinstance(social_dim['career'], dict):
                    career_level = social_dim['career'].get('level', 0)
            
            if career_level < 30 and '高级' in event.title:
                score *= 0.3
            elif career_level > 70 and '初级' in event.title:
                score *= 0.5
        except:
            pass
        
        # 检查年龄适宜性
        age = state.age
        if age < 18 and '工作' in event.title:
            score *= 0.2
        elif age > 65 and '高强度' in event.description:
            score *= 0.4
        
        return score
    
    def _check_memory_coherence(self, event: GameEvent, state: CharacterState) -> float:
        """检查历史记忆连贯性"""
        # 简化实现：基于角色状态检查连贯性
        
        try:
            # 检查事件情感连续性
            emotional_state = 50
            if 'psychological' in state.dimensions:
                psych_dim = state.dimensions['psychological']
                if 'happiness' in psych_dim:
                    emotional_state = psych_dim['happiness']
            
            if event.emotional_weight > 0.7 and emotional_state > 50:
                # 高情绪事件出现在积极情绪状态下
                return 0.9
            elif event.emotional_weight < 0.3 and emotional_state < 30:
                # 低情绪事件出现在消极情绪状态下  
                return 0.9
            else:
                return 0.7
        except:
            return 0.7
    
    def _check_macro_influence(self, event: GameEvent, era_rules) -> float:
        """检查宏观事件影响"""
        # 简化实现：检查事件是否与历史大事相关
        try:
            if isinstance(era_rules, dict):
                historical_events = era_rules.get('historicalEvents', [])
            else:
                historical_events = era_rules.historicalEvents
            
            for he in historical_events:
                if isinstance(he, dict):
                    event_name = he.get('event', '')
                else:
                    event_name = str(he)
                
                if event_name and (event_name in event.description or event_name in event.title):
                    return 1.0  # 与历史事件相关，加分
            
            return 0.5
        except:
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
            try:
                dimension = impact.get('dimension', '')
                sub_dimension = impact.get('subDimension', '')
                change = impact.get('change', 0)
                
                if dimension and sub_dimension:
                    # 累积影响
                    key = f"{dimension}.{sub_dimension}"
                    impacts[key] = impacts.get(key, 0) + change
            except:
                continue
        
        # 应用规则约束的影响
        for rule in self._get_applicable_rules(event, state):
            rule_effects = rule.get('effects', [])
            for effect in rule_effects:
                try:
                    dimension = effect.get('dimension', '')
                    sub_dimension = effect.get('subDimension', '')
                    change = effect.get('change', 0)
                    probability = effect.get('probability', 100)
                    
                    if dimension and sub_dimension and probability >= 50:
                        # 按概率应用影响
                        key = f"{dimension}.{sub_dimension}"
                        impacts[key] = impacts.get(key, 0) + change
                except:
                    continue
        
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