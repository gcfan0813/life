"""
动态规则更新系统
支持运行时规则更新、版本控制和热加载
"""

import json
import os
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import threading

class RuleStatus(Enum):
    """规则状态"""
    ACTIVE = "active"
    DISABLED = "disabled"
    PENDING = "pending"
    DEPRECATED = "deprecated"

class UpdateType(Enum):
    """更新类型"""
    ADD = "add"
    MODIFY = "modify"
    DELETE = "delete"
    ENABLE = "enable"
    DISABLE = "disable"

@dataclass
class RuleChange:
    """规则变更记录"""
    change_id: str
    rule_id: str
    update_type: UpdateType
    old_value: Optional[Dict] = None
    new_value: Optional[Dict] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    reason: str = ""
    author: str = "system"

@dataclass
class RuleVersion:
    """规则版本"""
    version_id: str
    rules_snapshot: Dict[str, List[Dict]]
    timestamp: str
    changes: List[RuleChange]
    checksum: str

class DynamicRuleManager:
    """动态规则管理器"""
    
    def __init__(self, rules_path: str = "shared/rules/"):
        self.rules_path = rules_path
        self.rules: Dict[str, List[Dict]] = {}
        self.rule_status: Dict[str, RuleStatus] = {}
        self.change_history: List[RuleChange] = []
        self.versions: List[RuleVersion] = []
        self.lock = threading.Lock()
        self.update_callbacks: List[Callable] = []
        
        # 加载规则
        self._load_rules()
        
    def _load_rules(self):
        """加载规则库"""
        try:
            comprehensive_file = os.path.join(self.rules_path, "comprehensive_rules.json")
            base_file = os.path.join(self.rules_path, "base_rules.json")
            extended_file = os.path.join(self.rules_path, "extended_rules.json")
            
            total_rules = 0
            self.rules = {}
            
            # 加载全面规则库
            if os.path.exists(comprehensive_file):
                with open(comprehensive_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                categories = data.get('categories', {})
                for cat_name, cat_data in categories.items():
                    if cat_name not in self.rules:
                        self.rules[cat_name] = []
                    
                    if 'subcategories' in cat_data:
                        for subcat_name, subcat_data in cat_data['subcategories'].items():
                            for rule in subcat_data.get('rules', []):
                                rule['category'] = cat_name
                                rule['subcategory'] = subcat_name
                                self.rules[cat_name].append(rule)
                                self.rule_status[rule['id']] = RuleStatus.ACTIVE
                                total_rules += 1
                    elif 'rules' in cat_data:
                        for rule in cat_data['rules']:
                            rule['category'] = cat_name
                            self.rules[cat_name].append(rule)
                            self.rule_status[rule['id']] = RuleStatus.ACTIVE
                            total_rules += 1
                
                # 元规则
                if 'meta_rules' in data:
                    self.rules['meta'] = data['meta_rules'].get('rules', [])
                    for rule in self.rules['meta']:
                        self.rule_status[rule['id']] = RuleStatus.ACTIVE
                        total_rules += 1
                
                # 特殊条件规则
                if 'special_conditions' in data:
                    self.rules['special'] = data['special_conditions'].get('rules', [])
                    for rule in self.rules['special']:
                        self.rule_status[rule['id']] = RuleStatus.ACTIVE
                        total_rules += 1
            
            print(f"[DynamicRuleManager] 加载了 {total_rules} 条规则")
            
            # 创建初始版本
            self._create_version("初始加载")
            
        except Exception as e:
            print(f"[DynamicRuleManager] 规则加载失败: {e}")
            self.rules = {}
    
    def add_rule(self, rule: Dict, category: str, reason: str = "") -> bool:
        """添加新规则"""
        with self.lock:
            try:
                rule_id = rule.get('id')
                if not rule_id:
                    raise ValueError("规则必须有id")
                
                if rule_id in self.rule_status:
                    raise ValueError(f"规则 {rule_id} 已存在")
                
                rule['category'] = category
                rule['created_at'] = datetime.now().isoformat()
                rule['version'] = '1.0'
                
                if category not in self.rules:
                    self.rules[category] = []
                
                self.rules[category].append(rule)
                self.rule_status[rule_id] = RuleStatus.ACTIVE
                
                # 记录变更
                change = RuleChange(
                    change_id=self._generate_change_id(),
                    rule_id=rule_id,
                    update_type=UpdateType.ADD,
                    new_value=rule,
                    reason=reason
                )
                self.change_history.append(change)
                
                # 通知更新
                self._notify_update(change)
                
                return True
                
            except Exception as e:
                print(f"[DynamicRuleManager] 添加规则失败: {e}")
                return False
    
    def modify_rule(self, rule_id: str, updates: Dict, reason: str = "") -> bool:
        """修改规则"""
        with self.lock:
            try:
                old_rule = self._find_rule(rule_id)
                if not old_rule:
                    raise ValueError(f"规则 {rule_id} 不存在")
                
                # 保存旧值
                old_value = old_rule.copy()
                
                # 应用更新
                for key, value in updates.items():
                    old_rule[key] = value
                
                old_rule['updated_at'] = datetime.now().isoformat()
                old_rule['version'] = self._increment_version(old_rule.get('version', '1.0'))
                
                # 记录变更
                change = RuleChange(
                    change_id=self._generate_change_id(),
                    rule_id=rule_id,
                    update_type=UpdateType.MODIFY,
                    old_value=old_value,
                    new_value=old_rule,
                    reason=reason
                )
                self.change_history.append(change)
                
                # 通知更新
                self._notify_update(change)
                
                return True
                
            except Exception as e:
                print(f"[DynamicRuleManager] 修改规则失败: {e}")
                return False
    
    def delete_rule(self, rule_id: str, reason: str = "") -> bool:
        """删除规则"""
        with self.lock:
            try:
                old_rule = self._find_rule(rule_id)
                if not old_rule:
                    raise ValueError(f"规则 {rule_id} 不存在")
                
                category = old_rule.get('category')
                if category and category in self.rules:
                    self.rules[category] = [
                        r for r in self.rules[category] 
                        if r.get('id') != rule_id
                    ]
                
                del self.rule_status[rule_id]
                
                # 记录变更
                change = RuleChange(
                    change_id=self._generate_change_id(),
                    rule_id=rule_id,
                    update_type=UpdateType.DELETE,
                    old_value=old_rule,
                    reason=reason
                )
                self.change_history.append(change)
                
                # 通知更新
                self._notify_update(change)
                
                return True
                
            except Exception as e:
                print(f"[DynamicRuleManager] 删除规则失败: {e}")
                return False
    
    def enable_rule(self, rule_id: str, reason: str = "") -> bool:
        """启用规则"""
        with self.lock:
            if rule_id not in self.rule_status:
                return False
            
            self.rule_status[rule_id] = RuleStatus.ACTIVE
            
            change = RuleChange(
                change_id=self._generate_change_id(),
                rule_id=rule_id,
                update_type=UpdateType.ENABLE,
                reason=reason
            )
            self.change_history.append(change)
            self._notify_update(change)
            
            return True
    
    def disable_rule(self, rule_id: str, reason: str = "") -> bool:
        """禁用规则"""
        with self.lock:
            if rule_id not in self.rule_status:
                return False
            
            self.rule_status[rule_id] = RuleStatus.DISABLED
            
            change = RuleChange(
                change_id=self._generate_change_id(),
                rule_id=rule_id,
                update_type=UpdateType.DISABLE,
                reason=reason
            )
            self.change_history.append(change)
            self._notify_update(change)
            
            return True
    
    def get_active_rules(self) -> Dict[str, List[Dict]]:
        """获取所有活跃规则"""
        active_rules = {}
        
        for category, rules in self.rules.items():
            active_rules[category] = [
                rule for rule in rules
                if self.rule_status.get(rule.get('id')) == RuleStatus.ACTIVE
            ]
        
        return active_rules
    
    def get_rule(self, rule_id: str) -> Optional[Dict]:
        """获取特定规则"""
        rule = self._find_rule(rule_id)
        if rule and self.rule_status.get(rule_id) == RuleStatus.ACTIVE:
            return rule
        return None
    
    def _find_rule(self, rule_id: str) -> Optional[Dict]:
        """查找规则"""
        for rules in self.rules.values():
            for rule in rules:
                if rule.get('id') == rule_id:
                    return rule
        return None
    
    def _generate_change_id(self) -> str:
        """生成变更ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        return f"change_{timestamp}"
    
    def _increment_version(self, version: str) -> str:
        """递增版本号"""
        try:
            parts = version.split('.')
            minor = int(parts[-1]) + 1
            parts[-1] = str(minor)
            return '.'.join(parts)
        except:
            return '1.1'
    
    def _create_version(self, reason: str = "") -> RuleVersion:
        """创建规则版本快照"""
        checksum = self._calculate_checksum()
        
        version = RuleVersion(
            version_id=f"v{len(self.versions) + 1}",
            rules_snapshot=self._deep_copy_rules(),
            timestamp=datetime.now().isoformat(),
            changes=list(self.change_history),
            checksum=checksum
        )
        
        self.versions.append(version)
        return version
    
    def _calculate_checksum(self) -> str:
        """计算规则库校验和"""
        content = json.dumps(self.rules, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def _deep_copy_rules(self) -> Dict[str, List[Dict]]:
        """深拷贝规则"""
        return json.loads(json.dumps(self.rules))
    
    def register_update_callback(self, callback: Callable):
        """注册更新回调"""
        self.update_callbacks.append(callback)
    
    def _notify_update(self, change: RuleChange):
        """通知规则更新"""
        for callback in self.update_callbacks:
            try:
                callback(change)
            except Exception as e:
                print(f"[DynamicRuleManager] 回调执行失败: {e}")
    
    def save_rules(self, filepath: Optional[str] = None) -> bool:
        """保存规则到文件"""
        filepath = filepath or os.path.join(self.rules_path, "user_rules.json")
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    'rules': self.rules,
                    'status': {k: v.value for k, v in self.rule_status.items()},
                    'history': [
                        {
                            'change_id': c.change_id,
                            'rule_id': c.rule_id,
                            'update_type': c.update_type.value,
                            'timestamp': c.timestamp,
                            'reason': c.reason
                        }
                        for c in self.change_history[-100:]  # 只保存最近100条
                    ],
                    'saved_at': datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            
            print(f"[DynamicRuleManager] 规则已保存到 {filepath}")
            return True
            
        except Exception as e:
            print(f"[DynamicRuleManager] 保存规则失败: {e}")
            return False
    
    def load_user_rules(self, filepath: Optional[str] = None) -> bool:
        """加载用户规则"""
        filepath = filepath or os.path.join(self.rules_path, "user_rules.json")
        
        try:
            if not os.path.exists(filepath):
                return False
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 合并用户规则
            for category, rules in data.get('rules', {}).items():
                if category not in self.rules:
                    self.rules[category] = []
                
                for rule in rules:
                    rule_id = rule.get('id')
                    # 不覆盖系统规则
                    if not self._find_rule(rule_id):
                        self.rules[category].append(rule)
                        self.rule_status[rule_id] = RuleStatus(
                            data.get('status', {}).get(rule_id, 'active')
                        )
            
            print(f"[DynamicRuleManager] 已加载用户规则")
            return True
            
        except Exception as e:
            print(f"[DynamicRuleManager] 加载用户规则失败: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取规则统计信息"""
        stats = {
            'total_rules': sum(len(rules) for rules in self.rules.values()),
            'active_rules': sum(1 for s in self.rule_status.values() if s == RuleStatus.ACTIVE),
            'disabled_rules': sum(1 for s in self.rule_status.values() if s == RuleStatus.DISABLED),
            'categories': list(self.rules.keys()),
            'version_count': len(self.versions),
            'change_count': len(self.change_history),
            'last_updated': self.change_history[-1].timestamp if self.change_history else None
        }
        return stats
    
    def rollback_to_version(self, version_id: str) -> bool:
        """回滚到指定版本"""
        for version in self.versions:
            if version.version_id == version_id:
                with self.lock:
                    self.rules = self._deep_copy_rules() if version.rules_snapshot else self.rules
                    self.rule_status = {
                        rule.get('id'): RuleStatus.ACTIVE
                        for rules in self.rules.values()
                        for rule in rules
                    }
                    
                    # 记录回滚
                    change = RuleChange(
                        change_id=self._generate_change_id(),
                        rule_id="all",
                        update_type=UpdateType.MODIFY,
                        reason=f"回滚到版本 {version_id}"
                    )
                    self.change_history.append(change)
                    
                    print(f"[DynamicRuleManager] 已回滚到 {version_id}")
                    return True
        
        return False

# 全局动态规则管理器实例
dynamic_rule_manager = DynamicRuleManager()
