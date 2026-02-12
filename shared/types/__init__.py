"""
类型定义模块 - 用于后端API
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

# 角色档案类型
class LifeProfile:
    def __init__(self, id: str, name: str, gender: str, birthDate: str, birthLocation: str, 
                 familyBackground: str, initialPersonality: Dict[str, float], createdAt: str):
        self.id = id
        self.name = name
        self.gender = gender
        self.birthDate = birthDate
        self.birthLocation = birthLocation
        self.familyBackground = familyBackground
        self.initialPersonality = initialPersonality
        self.createdAt = createdAt

# 角色状态类型  
class CharacterState:
    def __init__(self, id: str, profileId: str, currentDate: str, age: float, 
                 dimensions: Dict[str, Any], location: str, occupation: str, 
                 education: str, lifeStage: str, totalEvents: int, 
                 totalDecisions: int, daysSurvived: int):
        self.id = id
        self.profileId = profileId
        self.currentDate = currentDate
        self.age = age
        self.dimensions = dimensions
        self.location = location
        self.occupation = occupation
        self.education = education
        self.lifeStage = lifeStage
        self.totalEvents = totalEvents
        self.totalDecisions = totalDecisions
        self.daysSurvived = daysSurvived

# 游戏事件类型
class GameEvent:
    def __init__(self, id: str, profileId: str, eventDate: str, eventType: str,
                 title: str, description: str, narrative: str, choices: List[Dict],
                 impacts: Dict[str, Any], isCompleted: bool, selectedChoice: Optional[int],
                 plausibility: float, emotionalWeight: float, createdAt: str, updatedAt: str):
        self.id = id
        self.profileId = profileId
        self.eventDate = eventDate
        self.eventType = eventType
        self.title = title
        self.description = description
        self.narrative = narrative
        self.choices = choices
        self.impacts = impacts
        self.isCompleted = isCompleted
        self.selectedChoice = selectedChoice
        self.plausibility = plausibility
        self.emotionalWeight = emotionalWeight
        self.createdAt = createdAt
        self.updatedAt = updatedAt

# 记忆类型
class Memory:
    def __init__(self, id: str, profileId: str, eventId: str, summary: str,
                 emotionalWeight: float, recallCount: int, lastRecalled: Optional[str],
                 retention: float, createdAt: str, updatedAt: str):
        self.id = id
        self.profileId = profileId
        self.eventId = eventId
        self.summary = summary
        self.emotionalWeight = emotionalWeight
        self.recallCount = recallCount
        self.lastRecalled = lastRecalled
        self.retention = retention
        self.createdAt = createdAt
        self.updatedAt = updatedAt
