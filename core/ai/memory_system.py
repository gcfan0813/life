"""
记忆系统 - 艾宾浩斯遗忘曲线实现
"""

import math
from datetime import datetime, timedelta
from typing import Dict, List, Any

class Memory:
    def __init__(self, id, profile_id, event_id, summary, emotional_weight, 
                 recall_count=0, last_recalled=None, retention=1.0, 
                 memory_type="short_term", importance=0.5, created_at=None):
        self.id = id
        self.profile_id = profile_id
        self.event_id = event_id
        self.summary = summary
        self.emotional_weight = emotional_weight
        self.recall_count = recall_count
        self.last_recalled = last_recalled or datetime.now().isoformat()
        self.retention = retention
        self.memory_type = memory_type  # short_term, long_term, epic
        self.importance = importance  # 0-1
        self.created_at = created_at or datetime.now().isoformat()
    
    def calculate_retention(self, current_time=None) -> float:
        """
        艾宾浩斯遗忘曲线计算
        R = e^(-t/S) 其中S为稳定性系数
        """
        if current_time is None:
            current_time = datetime.now()
        
        # 解析记忆创建时间
        created = datetime.fromisoformat(self.created_at)
        
        # 计算经过的天数
        days_elapsed = (current_time - created).days
        
        # 稳定性系数（基于记忆类型和重要性）
        stability = self._get_stability()
        
        # 艾宾浩斯公式: R = e^(-t/S)
        if days_elapsed == 0:
            return 1.0
        
        retention = math.exp(-days_elapsed / stability)
        
        # 考虑情感权重（情感强烈的记忆更不容易遗忘）
        emotional_boost = 1 + (self.emotional_weight * 0.2)
        retention = min(1.0, retention * emotional_boost)
        
        # 考虑重要性
        importance_boost = 1 + (self.importance * 0.3)
        retention = min(1.0, retention * importance_boost)
        
        return max(0.0, retention)
    
    def _get_stability(self) -> float:
        """获取记忆稳定性系数"""
        base_stability = {
            "short_term": 7,    # 短期记忆：7天
            "long_term": 30,    # 长期记忆：30天
            "epic": 365         # 重要记忆：1年
        }.get(self.memory_type, 14)
        
        # 根据重要性调整
        importance_factor = 1 + self.importance
        return base_stability * importance_factor
    
    def recall(self) -> Dict[str, Any]:
        """
        回忆记忆（增强记忆）
        """
        self.recall_count += 1
        self.last_recalled = datetime.now().isoformat()
        
        # 每次回忆都会增强记忆（间隔效应）
        # 最佳复习间隔：1天后、3天后、7天后、14天后、30天后
        retention_boost = 0.1 * (1 + 0.1 * self.recall_count)
        self.retention = min(1.0, self.retention + retention_boost)
        
        return {
            "success": True,
            "retention": self.retention,
            "recall_count": self.recall_count,
            "message": f"第{self.recall_count}次回忆，记忆留存率提升"
        }
    
    def should_forget(self) -> bool:
        """判断是否应该遗忘"""
        return self.retention < 0.2  # 留存率低于20%则遗忘
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "event_id": self.event_id,
            "summary": self.summary,
            "emotional_weight": self.emotional_weight,
            "recall_count": self.recall_count,
            "last_recalled": self.last_recalled,
            "retention": self.retention,
            "memory_type": self.memory_type,
            "importance": self.importance,
            "created_at": self.created_at
        }


class MemorySystem:
    """记忆管理系统"""
    
    # 记忆类型阈值
    MEMORY_TYPE_THRESHOLDS = {
        "epic": 0.9,      # 情感权重 > 0.9 为史诗级记忆
        "long_term": 0.6, # 情感权重 > 0.6 为长期记忆
        "short_term": 0   # 其他为短期记忆
    }
    
    @staticmethod
    def classify_memory(emotional_weight: float, importance: float) -> str:
        """自动分类记忆"""
        if emotional_weight >= MemorySystem.MEMORY_TYPE_THRESHOLDS["epic"]:
            return "epic"
        elif emotional_weight >= MemorySystem.MEMORY_TYPE_THRESHOLDS["long_term"]:
            return "long_term"
        return "short_term"
    
    @staticmethod
    def calculate_importance(event_type: str, emotional_weight: float) -> float:
        """计算记忆重要性"""
        # 事件类型重要性权重
        type_weights = {
            "birth": 1.0,           # 出生
            "death": 0.9,           # 死亡事件
            "marriage": 0.9,        # 婚姻
            "career_change": 0.8,   # 职业变化
            "education": 0.7,       # 教育
            "health": 0.8,          # 健康
            "relationship": 0.7,    # 关系
            "achievement": 0.8,     # 成就
            "trauma": 0.9,         # 创伤
            "daily": 0.3           # 日常
        }
        
        type_weight = type_weights.get(event_type, 0.5)
        
        # 综合计算重要性
        importance = (type_weight + emotional_weight) / 2
        return min(1.0, max(0.0, importance))
    
    @staticmethod
    def process_memory_forgetting(memories: List[Memory]) -> Dict[str, Any]:
        """处理记忆遗忘"""
        stats = {
            "total": len(memories),
            "forgotten": 0,
            "strengthened": 0,
            "decayed": 0
        }
        
        forgotten_memories = []
        
        for memory in memories:
            old_retention = memory.retention
            new_retention = memory.calculate_retention()
            
            if memory.should_forget():
                stats["forgotten"] += 1
                forgotten_memories.append(memory.id)
            elif new_retention > old_retention:
                # 被回忆过，增强了
                stats["strengthened"] += 1
            else:
                stats["decayed"] += 1
        
        return stats


# 全局记忆系统实例
memory_system = MemorySystem()
