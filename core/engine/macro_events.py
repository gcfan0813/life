"""
宏观事件注入系统
根据年代和历史背景注入影响全社会的重大事件
"""

import json
import random
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum


class MacroEventType(Enum):
    """宏观事件类型"""
    ECONOMIC = "economic"  # 经济事件
    PANDEMIC = "pandemic"  # 疫情
    POLICY = "policy"      # 政策变化
    TECHNOLOGY = "technology"  # 科技革命
    NATURAL_DISASTER = "natural_disaster"  # 自然灾害
    SOCIAL = "social"      # 社会变革


class MacroEvent:
    """宏观事件定义"""
    
    def __init__(
        self,
        event_id: str,
        name: str,
        event_type: MacroEventType,
        year_range: tuple,
        description: str,
        global_impacts: Dict[str, Any],
        affected_groups: List[str],
        probability: float = 0.8
    ):
        self.event_id = event_id
        self.name = name
        self.event_type = event_type
        self.year_range = year_range
        self.description = description
        self.global_impacts = global_impacts
        self.affected_groups = affected_groups
        self.probability = probability
    
    def should_trigger(self, year: int) -> bool:
        """检查是否应该触发此事件"""
        if not (self.year_range[0] <= year <= self.year_range[1]):
            return False
        return random.random() < self.probability
    
    def apply_to_character(self, character_state: Any) -> Dict[str, Any]:
        """将宏观事件应用到角色"""
        # 检查角色是否受影响
        affected = False
        if "all" in self.affected_groups:
            affected = True
        elif hasattr(character_state, 'age'):
            age = character_state.age
            if "youth" in self.affected_groups and 15 <= age <= 30:
                affected = True
            elif "working" in self.affected_groups and 25 <= age <= 60:
                affected = True
            elif "elderly" in self.affected_groups and age > 60:
                affected = True
        
        if not affected:
            return {"affected": False}
        
        return {
            "affected": True,
            "event_name": self.name,
            "impacts": self.global_impacts,
            "narrative": f"【宏观事件】{self.description}"
        }


class MacroEventSystem:
    """宏观事件系统"""
    
    def __init__(self):
        self.events = self._load_historical_events()
        self.triggered_events = set()
    
    def _load_historical_events(self) -> List[MacroEvent]:
        """加载历史宏观事件"""
        events = [
            # 1980年代事件
            MacroEvent(
                event_id="reform_opening",
                name="改革开放",
                event_type=MacroEventType.POLICY,
                year_range=(1978, 1990),
                description="改革开放政策实施，市场经济逐步发展",
                global_impacts={
                    "economic": {"career_opportunity": 10, "economic_growth": 5},
                    "social": {"social_mobility": 8}
                },
                affected_groups=["all"],
                probability=0.95
            ),
            MacroEvent(
                event_id="economic_crisis_1987",
                name="1987股灾",
                event_type=MacroEventType.ECONOMIC,
                year_range=(1987, 1987),
                description="全球股灾波及，金融市场动荡",
                global_impacts={
                    "economic": {"economic": -8},
                    "psychological": {"stress": 5}
                },
                affected_groups=["working"],
                probability=0.7
            ),
            # 1990年代事件
            MacroEvent(
                event_id="asian_financial_crisis",
                name="亚洲金融危机",
                event_type=MacroEventType.ECONOMIC,
                year_range=(1997, 1998),
                description="亚洲金融危机爆发，经济受到冲击",
                global_impacts={
                    "economic": {"economic": -10, "career_stability": -5},
                    "psychological": {"anxiety": 8}
                },
                affected_groups=["working"],
                probability=0.8
            ),
            MacroEvent(
                event_id="internet_bubble",
                name="互联网泡沫",
                event_type=MacroEventType.TECHNOLOGY,
                year_range=(1999, 2001),
                description="互联网产业兴起后泡沫破裂",
                global_impacts={
                    "economic": {"tech_opportunity": 15, "risk": 10},
                    "cognitive": {"digital_literacy": 5}
                },
                affected_groups=["youth", "working"],
                probability=0.75
            ),
            # 2000年代事件
            MacroEvent(
                event_id="sars",
                name="非典疫情",
                event_type=MacroEventType.PANDEMIC,
                year_range=(2003, 2003),
                description="非典疫情爆发，社会生活受影响",
                global_impacts={
                    "physiological": {"health_risk": 5},
                    "psychological": {"anxiety": 10, "resilience": 3},
                    "social": {"social_isolation": 8}
                },
                affected_groups=["all"],
                probability=0.9
            ),
            MacroEvent(
                event_id="financial_crisis_2008",
                name="全球金融危机",
                event_type=MacroEventType.ECONOMIC,
                year_range=(2008, 2009),
                description="次贷危机引发全球金融海啸",
                global_impacts={
                    "economic": {"economic": -15, "career_stability": -10},
                    "psychological": {"stress": 12, "resilience": 5}
                },
                affected_groups=["working"],
                probability=0.85
            ),
            # 2010年代事件
            MacroEvent(
                event_id="mobile_internet",
                name="移动互联网革命",
                event_type=MacroEventType.TECHNOLOGY,
                year_range=(2010, 2015),
                description="智能手机普及，移动互联网改变生活",
                global_impacts={
                    "economic": {"new_industry": 10},
                    "cognitive": {"digital_skills": 8},
                    "social": {"connectivity": 10}
                },
                affected_groups=["youth", "working"],
                probability=0.9
            ),
            MacroEvent(
                event_id="trade_war",
                name="中美贸易摩擦",
                event_type=MacroEventType.ECONOMIC,
                year_range=(2018, 2020),
                description="中美贸易战影响经济格局",
                global_impacts={
                    "economic": {"economic": -5, "career_uncertainty": 8},
                    "psychological": {"anxiety": 5}
                },
                affected_groups=["working"],
                probability=0.7
            ),
            # 2020年代事件
            MacroEvent(
                event_id="covid19",
                name="新冠疫情",
                event_type=MacroEventType.PANDEMIC,
                year_range=(2020, 2023),
                description="全球新冠疫情大流行，深刻改变社会",
                global_impacts={
                    "physiological": {"health_risk": 10},
                    "psychological": {"anxiety": 15, "resilience": 8, "isolation": 10},
                    "economic": {"economic": -8, "remote_work": 10},
                    "social": {"social_distance": 12}
                },
                affected_groups=["all"],
                probability=0.95
            ),
            MacroEvent(
                event_id="ai_revolution",
                name="AI技术革命",
                event_type=MacroEventType.TECHNOLOGY,
                year_range=(2022, 2030),
                description="人工智能技术突破性发展",
                global_impacts={
                    "economic": {"ai_opportunity": 12, "job_displacement": -8},
                    "cognitive": {"ai_skills": 10},
                    "psychological": {"adaptation_stress": 5}
                },
                affected_groups=["youth", "working"],
                probability=0.85
            ),
            # 随机自然灾害
            MacroEvent(
                event_id="earthquake",
                name="大地震",
                event_type=MacroEventType.NATURAL_DISASTER,
                year_range=(1970, 2030),
                description="发生重大地震灾害",
                global_impacts={
                    "physiological": {"health": -5},
                    "psychological": {"trauma": 10, "resilience": 5},
                    "social": {"community_bond": 8}
                },
                affected_groups=["all"],
                probability=0.05
            ),
            MacroEvent(
                event_id="flood",
                name="洪涝灾害",
                event_type=MacroEventType.NATURAL_DISASTER,
                year_range=(1970, 2030),
                description="发生严重洪涝灾害",
                global_impacts={
                    "physiological": {"health": -3},
                    "economic": {"property_loss": -5},
                    "social": {"community_bond": 5}
                },
                affected_groups=["all"],
                probability=0.08
            ),
        ]
        return events
    
    def check_macro_events(self, year: int, character_state: Any) -> List[Dict[str, Any]]:
        """检查并返回当前年份应触发的宏观事件"""
        triggered = []
        
        for event in self.events:
            if event.event_id in self.triggered_events:
                continue
            
            if event.should_trigger(year):
                impact = event.apply_to_character(character_state)
                if impact["affected"]:
                    triggered.append(impact)
                    # 标记为已触发（避免同年重复触发）
                    self.triggered_events.add(f"{event.event_id}_{year}")
        
        return triggered
    
    def get_active_events(self, year: int) -> List[MacroEvent]:
        """获取当前年份可能发生的宏观事件"""
        return [e for e in self.events if e.year_range[0] <= year <= e.year_range[1]]
    
    def force_trigger_event(self, event_id: str, character_state: Any) -> Optional[Dict[str, Any]]:
        """强制触发指定事件（用于剧情或测试）"""
        for event in self.events:
            if event.event_id == event_id:
                return event.apply_to_character(character_state)
        return None


# 全局实例
macro_event_system = MacroEventSystem()
