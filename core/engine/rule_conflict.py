"""
规则冲突检测与解决系统
负责检测规则间的冲突并提供解决方案
"""

import json
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ConflictType(Enum):
    """冲突类型"""
    CONTRADICTORY = "contradictory"  # 矛盾冲突
    REDUNDANT = "redundant"          # 冗余
    OVERLAPPING = "overlapping"      # 重叠
    CONDITIONAL = "conditional"      # 条件冲突

class ConflictSeverity(Enum):
    """冲突严重程度"""
    CRITICAL = "critical"    # 严重冲突，必须解决
    MODERATE = "moderate"    # 中等冲突，建议解决
    MINOR = "minor"          # 轻微冲突，可忽略

@dataclass
class RuleConflict:
    """规则冲突"""
    rule1_id: str
    rule2_id: str
    conflict_type: ConflictType
    severity: ConflictSeverity
    description: str
    affected_dimensions: List[str]
    resolution_suggestion: str
    auto_resolvable: bool

class RuleConflictDetector:
    """规则冲突检测器"""
    
    def __init__(self, rules: Dict[str, List[Dict]] = None):
        self.rules = rules or {}
        self.conflict_cache = {}
        
    def load_rules(self, rules: Dict[str, List[Dict]]):
        """加载规则"""
        self.rules = rules
        self.conflict_cache = {}
    
    def detect_all_conflicts(self) -> List[RuleConflict]:
        """检测所有规则冲突"""
        conflicts = []
        all_rules = self._flatten_rules()
        
        # 两两比较规则
        for i, rule1 in enumerate(all_rules):
            for rule2 in all_rules[i+1:]:
                conflict = self._detect_pair_conflict(rule1, rule2)
                if conflict:
                    conflicts.append(conflict)
        
        return conflicts
    
    def detect_conflicts_for_rule(self, rule: Dict) -> List[RuleConflict]:
        """检测特定规则的冲突"""
        conflicts = []
        all_rules = self._flatten_rules()
        
        for other_rule in all_rules:
            if other_rule.get('id') == rule.get('id'):
                continue
            conflict = self._detect_pair_conflict(rule, other_rule)
            if conflict:
                conflicts.append(conflict)
        
        return conflicts
    
    def _detect_pair_conflict(self, rule1: Dict, rule2: Dict) -> Optional[RuleConflict]:
        """检测两个规则间的冲突"""
        # 1. 检查条件重叠
        condition_overlap = self._check_condition_overlap(rule1, rule2)
        
        # 2. 检查效果冲突
        effect_conflict = self._check_effect_conflict(rule1, rule2)
        
        if effect_conflict and condition_overlap:
            # 条件重叠且效果冲突 = 矛盾冲突
            return RuleConflict(
                rule1_id=rule1.get('id', 'unknown'),
                rule2_id=rule2.get('id', 'unknown'),
                conflict_type=ConflictType.CONTRADICTORY,
                severity=ConflictSeverity.CRITICAL,
                description=f"规则 {rule1.get('id')} 和 {rule2.get('id')} 在相同条件下产生矛盾效果",
                affected_dimensions=effect_conflict,
                resolution_suggestion="修改其中一条规则的条件或效果，确保不会在相同情境下产生矛盾",
                auto_resolvable=True
            )
        
        elif effect_conflict and not condition_overlap:
            # 效果冲突但条件不重叠 = 条件冲突
            return RuleConflict(
                rule1_id=rule1.get('id', 'unknown'),
                rule2_id=rule2.get('id', 'unknown'),
                conflict_type=ConflictType.CONDITIONAL,
                severity=ConflictSeverity.MODERATE,
                description=f"规则 {rule1.get('id')} 和 {rule2.get('id')} 效果相反但条件不同",
                affected_dimensions=effect_conflict,
                resolution_suggestion="确保条件能正确区分两种情况，或添加优先级",
                auto_resolvable=False
            )
        
        elif condition_overlap and not effect_conflict:
            # 条件重叠但效果不冲突 = 冗余或重叠
            if self._check_redundancy(rule1, rule2):
                return RuleConflict(
                    rule1_id=rule1.get('id', 'unknown'),
                    rule2_id=rule2.get('id', 'unknown'),
                    conflict_type=ConflictType.REDUNDANT,
                    severity=ConflictSeverity.MINOR,
                    description=f"规则 {rule1.get('id')} 可能与 {rule2.get('id')} 冗余",
                    affected_dimensions=[],
                    resolution_suggestion="考虑合并或删除冗余规则",
                    auto_resolvable=False
                )
        
        return None
    
    def _check_condition_overlap(self, rule1: Dict, rule2: Dict) -> bool:
        """检查两个规则的条件是否重叠"""
        cond1 = rule1.get('condition', '')
        cond2 = rule2.get('condition', '')
        
        # 简化实现：检查关键条件词
        key_terms1 = self._extract_key_terms(cond1)
        key_terms2 = self._extract_key_terms(cond2)
        
        # 如果都涉及相同的维度
        common_dimensions = set(key_terms1) & set(key_terms2)
        
        if common_dimensions:
            return True
        
        return False
    
    def _check_effect_conflict(self, rule1: Dict, rule2: Dict) -> List[str]:
        """检查两个规则的效果是否冲突"""
        effect1 = rule1.get('effect', {})
        effect2 = rule2.get('effect', {})
        
        conflicting_dimensions = []
        
        # 检查每个维度
        all_keys = set(effect1.keys()) | set(effect2.keys())
        
        for key in all_keys:
            val1 = effect1.get(key, 0)
            val2 = effect2.get(key, 0)
            
            # 如果一个正向一个负向，则冲突
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                if val1 * val2 < 0:  # 异号
                    conflicting_dimensions.append(key)
        
        return conflicting_dimensions
    
    def _check_redundancy(self, rule1: Dict, rule2: Dict) -> bool:
        """检查两个规则是否冗余"""
        # 简化实现：如果条件相似且效果相同方向
        effect1 = rule1.get('effect', {})
        effect2 = rule2.get('effect', {})
        
        same_direction = all(
            (effect1.get(k, 0) >= 0) == (effect2.get(k, 0) >= 0)
            for k in set(effect1.keys()) & set(effect2.keys())
        )
        
        return same_direction
    
    def _extract_key_terms(self, condition: str) -> List[str]:
        """从条件中提取关键术语"""
        if not condition:
            return []
        
        # 关键维度术语
        dimension_terms = [
            'age', 'health', 'energy', 'happiness', 'stress',
            'career', 'income', 'relationship', 'education',
            'skill', 'knowledge', 'fitness', 'appearance'
        ]
        
        found_terms = []
        condition_lower = condition.lower()
        
        for term in dimension_terms:
            if term in condition_lower:
                found_terms.append(term)
        
        return found_terms
    
    def _flatten_rules(self) -> List[Dict]:
        """扁平化规则列表"""
        all_rules = []
        for category_rules in self.rules.values():
            if isinstance(category_rules, list):
                all_rules.extend(category_rules)
            elif isinstance(category_rules, dict):
                # 处理子类别
                if 'rules' in category_rules:
                    all_rules.extend(category_rules['rules'])
                elif 'subcategories' in category_rules:
                    for subcat in category_rules['subcategories'].values():
                        if 'rules' in subcat:
                            all_rules.extend(subcat['rules'])
        return all_rules
    
    def resolve_conflict(self, conflict: RuleConflict) -> Dict[str, Any]:
        """解决规则冲突"""
        if conflict.conflict_type == ConflictType.CONTRADICTORY:
            return self._resolve_contradictory(conflict)
        elif conflict.conflict_type == ConflictType.REDUNDANT:
            return self._resolve_redundant(conflict)
        elif conflict.conflict_type == ConflictType.CONDITIONAL:
            return self._resolve_conditional(conflict)
        
        return {'resolved': False, 'reason': 'Unknown conflict type'}
    
    def _resolve_contradictory(self, conflict: RuleConflict) -> Dict[str, Any]:
        """解决矛盾冲突"""
        # 自动解决策略：保留概率更高的规则
        rule1 = self._find_rule(conflict.rule1_id)
        rule2 = self._find_rule(conflict.rule2_id)
        
        if rule1 and rule2:
            prob1 = rule1.get('probability', 50)
            prob2 = rule2.get('probability', 50)
            
            if prob1 > prob2:
                return {
                    'resolved': True,
                    'action': 'disable',
                    'rule_id': conflict.rule2_id,
                    'reason': f'规则 {conflict.rule1_id} 可信度更高 ({prob1}% > {prob2}%)'
                }
            else:
                return {
                    'resolved': True,
                    'action': 'disable',
                    'rule_id': conflict.rule1_id,
                    'reason': f'规则 {conflict.rule2_id} 可信度更高 ({prob2}% > {prob1}%)'
                }
        
        return {'resolved': False, 'reason': 'Cannot find rules'}
    
    def _resolve_redundant(self, conflict: RuleConflict) -> Dict[str, Any]:
        """解决冗余冲突"""
        # 建议合并规则
        return {
            'resolved': False,
            'action': 'suggest_merge',
            'rule_ids': [conflict.rule1_id, conflict.rule2_id],
            'reason': '建议合并这两条冗余规则'
        }
    
    def _resolve_conditional(self, conflict: RuleConflict) -> Dict[str, Any]:
        """解决条件冲突"""
        # 建议添加优先级
        return {
            'resolved': False,
            'action': 'suggest_priority',
            'rule_ids': [conflict.rule1_id, conflict.rule2_id],
            'reason': '建议为这两条规则设置优先级'
        }
    
    def _find_rule(self, rule_id: str) -> Optional[Dict]:
        """查找规则"""
        for rule in self._flatten_rules():
            if rule.get('id') == rule_id:
                return rule
        return None
    
    def get_conflict_statistics(self) -> Dict[str, Any]:
        """获取冲突统计信息"""
        conflicts = self.detect_all_conflicts()
        
        stats = {
            'total_conflicts': len(conflicts),
            'by_severity': {
                'critical': 0,
                'moderate': 0,
                'minor': 0
            },
            'by_type': {
                'contradictory': 0,
                'redundant': 0,
                'overlapping': 0,
                'conditional': 0
            },
            'auto_resolvable': 0
        }
        
        for conflict in conflicts:
            stats['by_severity'][conflict.severity.value] += 1
            stats['by_type'][conflict.conflict_type.value] += 1
            if conflict.auto_resolvable:
                stats['auto_resolvable'] += 1
        
        return stats

# 全局冲突检测器实例
conflict_detector = RuleConflictDetector()
