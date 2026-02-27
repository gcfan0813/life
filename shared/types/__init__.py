"""
类型定义模块 - 用于后端API
与前端 TypeScript 类型定义保持同步
"""

from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from enum import Enum


# ==================== 枚举类型 ====================

class LifeStage(str, Enum):
    """人生阶段"""
    CHILDHOOD = "childhood"
    TEEN = "teen"
    YOUNG_ADULT = "youngAdult"
    ADULT = "adult"
    MIDDLE_AGE = "middleAge"
    SENIOR = "senior"


class EventType(str, Enum):
    """事件类型"""
    MILESTONE = "milestone"
    CRISIS = "crisis"
    OPPORTUNITY = "opportunity"
    RELATIONSHIP = "relationship"
    DAILY = "daily"


class Gender(str, Enum):
    """性别"""
    MALE = "male"
    FEMALE = "female"


# ==================== 五维系统类型 ====================

class PhysicalDimensions:
    """生理系统维度"""
    def __init__(self, health: int = 70, energy: int = 70, 
                 appearance: int = 60, fitness: int = 50):
        self.health = health
        self.energy = energy
        self.appearance = appearance
        self.fitness = fitness
    
    def to_dict(self) -> Dict[str, int]:
        return {
            "health": self.health,
            "energy": self.energy,
            "appearance": self.appearance,
            "fitness": self.fitness
        }


class PsychologicalDimensions:
    """心理系统维度"""
    def __init__(self, openness: int = 50, conscientiousness: int = 50,
                 extraversion: int = 50, agreeableness: int = 50,
                 neuroticism: int = 50, happiness: int = 70,
                 stress: int = 30, resilience: int = 60):
        self.openness = openness
        self.conscientiousness = conscientiousness
        self.extraversion = extraversion
        self.agreeableness = agreeableness
        self.neuroticism = neuroticism
        self.happiness = happiness
        self.stress = stress
        self.resilience = resilience
    
    def to_dict(self) -> Dict[str, int]:
        return {
            "openness": self.openness,
            "conscientiousness": self.conscientiousness,
            "extraversion": self.extraversion,
            "agreeableness": self.agreeableness,
            "neuroticism": self.neuroticism,
            "happiness": self.happiness,
            "stress": self.stress,
            "resilience": self.resilience
        }


class CareerInfo:
    """职业信息"""
    def __init__(self, level: int = 0, title: str = "无", 
                 satisfaction: int = 0, income: int = 0):
        self.level = level
        self.title = title
        self.satisfaction = satisfaction
        self.income = income
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level,
            "title": self.title,
            "satisfaction": self.satisfaction,
            "income": self.income
        }


class EconomicInfo:
    """经济信息"""
    def __init__(self, wealth: int = 0, debt: int = 0, credit: int = 70):
        self.wealth = wealth
        self.debt = debt
        self.credit = credit
    
    def to_dict(self) -> Dict[str, int]:
        return {
            "wealth": self.wealth,
            "debt": self.debt,
            "credit": self.credit
        }


class SocialDimensions:
    """社会系统维度"""
    def __init__(self, social_capital: int = 50, 
                 career: Optional[CareerInfo] = None,
                 economic: Optional[EconomicInfo] = None):
        self.socialCapital = social_capital
        self.career = career if career else CareerInfo()
        self.economic = economic if economic else EconomicInfo()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "socialCapital": self.socialCapital,
            "career": self.career.to_dict(),
            "economic": self.economic.to_dict()
        }


class KnowledgeInfo:
    """知识信息"""
    def __init__(self, academic: int = 40, practical: int = 30, creative: int = 50):
        self.academic = academic
        self.practical = practical
        self.creative = creative
    
    def to_dict(self) -> Dict[str, int]:
        return {
            "academic": self.academic,
            "practical": self.practical,
            "creative": self.creative
        }


class SkillsInfo:
    """技能信息"""
    def __init__(self, communication: int = 30, problem_solving: int = 40,
                 leadership: int = 20):
        self.communication = communication
        self.problemSolving = problem_solving
        self.leadership = leadership
    
    def to_dict(self) -> Dict[str, int]:
        return {
            "communication": self.communication,
            "problemSolving": self.problemSolving,
            "leadership": self.leadership
        }


class MemoryAbilityInfo:
    """记忆能力信息"""
    def __init__(self, short_term: int = 70, long_term: int = 60, emotional: int = 80):
        self.shortTerm = short_term
        self.longTerm = long_term
        self.emotional = emotional
    
    def to_dict(self) -> Dict[str, int]:
        return {
            "shortTerm": self.shortTerm,
            "longTerm": self.longTerm,
            "emotional": self.emotional
        }


class CognitiveDimensions:
    """认知系统维度"""
    def __init__(self, knowledge: Optional[KnowledgeInfo] = None, 
                 skills: Optional[SkillsInfo] = None,
                 memory: Optional[MemoryAbilityInfo] = None):
        self.knowledge = knowledge if knowledge else KnowledgeInfo()
        self.skills = skills if skills else SkillsInfo()
        self.memory = memory if memory else MemoryAbilityInfo()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "knowledge": self.knowledge.to_dict(),
            "skills": self.skills.to_dict(),
            "memory": self.memory.to_dict()
        }


class IntimacyInfo:
    """亲密度信息"""
    def __init__(self, family: int = 80, friends: int = 40, romantic: int = 0):
        self.family = family
        self.friends = friends
        self.romantic = romantic
    
    def to_dict(self) -> Dict[str, int]:
        return {
            "family": self.family,
            "friends": self.friends,
            "romantic": self.romantic
        }


class NetworkInfo:
    """社交网络信息"""
    def __init__(self, size: int = 10, quality: int = 60, diversity: int = 30):
        self.size = size
        self.quality = quality
        self.diversity = diversity
    
    def to_dict(self) -> Dict[str, int]:
        return {
            "size": self.size,
            "quality": self.quality,
            "diversity": self.diversity
        }


class RelationalDimensions:
    """关系系统维度"""
    def __init__(self, intimacy: Optional[IntimacyInfo] = None, 
                 network: Optional[NetworkInfo] = None):
        self.intimacy = intimacy if intimacy else IntimacyInfo()
        self.network = network if network else NetworkInfo()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "intimacy": self.intimacy.to_dict(),
            "network": self.network.to_dict()
        }


class FiveDimensionSystem:
    """五维系统"""
    def __init__(self):
        self.physical = PhysicalDimensions()
        self.psychological = PsychologicalDimensions()
        self.social = SocialDimensions()
        self.cognitive = CognitiveDimensions()
        self.relational = RelationalDimensions()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "physical": self.physical.to_dict(),
            "psychological": self.psychological.to_dict(),
            "social": self.social.to_dict(),
            "cognitive": self.cognitive.to_dict(),
            "relational": self.relational.to_dict()
        }


# ==================== 核心类型 ====================

class LifeProfile:
    """角色档案 - 与前端 TypeScript 类型保持一致"""
    def __init__(self, id: str, name: str, gender: str, birthDate: str, 
                 birthLocation: str, familyBackground: str = "middle",
                 initialPersonality: Optional[Dict[str, float]] = None, 
                 createdAt: Optional[str] = None, startingAge: float = 0.0,
                 era: str = "21世纪", difficulty: str = "normal"):
        self.id = id
        self.name = name
        self.gender = gender
        self.birthDate = birthDate
        self.birthLocation = birthLocation
        self.familyBackground = familyBackground if familyBackground else "middle"
        self.initialPersonality = initialPersonality if initialPersonality else {}
        self.createdAt = createdAt if createdAt else datetime.now().isoformat()
        self.startingAge = startingAge
        self.era = era
        self.difficulty = difficulty
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birthDate": self.birthDate,
            "birthLocation": self.birthLocation,
            "familyBackground": self.familyBackground,
            "initialPersonality": self.initialPersonality,
            "createdAt": self.createdAt,
            "startingAge": self.startingAge,
            "era": self.era,
            "difficulty": self.difficulty
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LifeProfile':
        """从字典创建实例"""
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            gender=data.get("gender", "male"),
            birthDate=data.get("birthDate", data.get("birth_date", "")),
            birthLocation=data.get("birthLocation", data.get("birth_place", "")),
            familyBackground=data.get("familyBackground", data.get("family_background", "middle")),
            initialPersonality=data.get("initialPersonality", data.get("initial_traits", {})),
            createdAt=data.get("createdAt", data.get("created_at")),
            startingAge=data.get("startingAge", data.get("starting_age", 0.0)),
            era=data.get("era", "21世纪"),
            difficulty=data.get("difficulty", "normal")
        )


class CharacterState:
    """角色状态 - 与前端 TypeScript 类型保持一致"""
    def __init__(self, id: str, profileId: str, currentDate: str, age: int,
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
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "profileId": self.profileId,
            "currentDate": self.currentDate,
            "age": self.age,
            "dimensions": self.dimensions,
            "location": self.location,
            "occupation": self.occupation,
            "education": self.education,
            "lifeStage": self.lifeStage,
            "totalEvents": self.totalEvents,
            "totalDecisions": self.totalDecisions,
            "daysSurvived": self.daysSurvived
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CharacterState':
        """从字典创建实例"""
        return cls(
            id=data.get("id", ""),
            profileId=data.get("profileId", data.get("profile_id", "")),
            currentDate=data.get("currentDate", data.get("current_date", "")),
            age=data.get("age", 0),
            dimensions=data.get("dimensions", {}),
            location=data.get("location", ""),
            occupation=data.get("occupation", ""),
            education=data.get("education", ""),
            lifeStage=data.get("lifeStage", data.get("life_stage", "childhood")),
            totalEvents=data.get("totalEvents", data.get("total_events", 0)),
            totalDecisions=data.get("totalDecisions", data.get("total_decisions", 0)),
            daysSurvived=data.get("daysSurvived", data.get("days_survived", 0))
        )


class EventChoice:
    """事件选择项"""
    def __init__(self, id: int, text: str, riskLevel: int = 50,
                 immediateImpacts: Optional[List[Dict[str, Any]]] = None, 
                 longTermEffects: Optional[List[str]] = None,
                 specialConditions: Optional[List[str]] = None):
        self.id = id
        self.text = text
        self.riskLevel = riskLevel
        self.immediateImpacts = immediateImpacts if immediateImpacts else []
        self.longTermEffects = longTermEffects if longTermEffects else []
        self.specialConditions = specialConditions if specialConditions else []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "riskLevel": self.riskLevel,
            "immediateImpacts": self.immediateImpacts,
            "longTermEffects": self.longTermEffects,
            "specialConditions": self.specialConditions
        }


class GameEvent:
    """游戏事件 - 与前端 TypeScript 类型保持一致"""
    def __init__(self, id: str, profileId: str, eventDate: str, eventType: str,
                 title: str, description: str, narrative: str, 
                 choices: Optional[List[Any]] = None,
                 impacts: Optional[List[Any]] = None, 
                 isCompleted: bool = False, 
                 selectedChoice: Optional[int] = None,
                 plausibility: float = 50.0, 
                 emotionalWeight: float = 0.5, 
                 createdAt: Optional[str] = None, 
                 updatedAt: Optional[str] = None):
        self.id = id
        self.profileId = profileId
        self.eventDate = eventDate
        self.eventType = eventType
        self.title = title
        self.description = description
        self.narrative = narrative
        self.choices = choices if choices else []
        self.impacts = impacts if impacts else []
        self.isCompleted = isCompleted
        self.selectedChoice = selectedChoice
        self.plausibility = plausibility
        self.emotionalWeight = emotionalWeight
        self.createdAt = createdAt if createdAt else datetime.now().isoformat()
        self.updatedAt = updatedAt if updatedAt else datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "profileId": self.profileId,
            "eventDate": self.eventDate,
            "eventType": self.eventType,
            "title": self.title,
            "description": self.description,
            "narrative": self.narrative,
            "choices": self.choices,
            "impacts": self.impacts,
            "isCompleted": self.isCompleted,
            "selectedChoice": self.selectedChoice,
            "plausibility": self.plausibility,
            "emotionalWeight": self.emotionalWeight,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameEvent':
        """从字典创建实例"""
        return cls(
            id=data.get("id", ""),
            profileId=data.get("profileId", data.get("profile_id", "")),
            eventDate=data.get("eventDate", data.get("event_date", "")),
            eventType=data.get("eventType", data.get("event_type", "daily")),
            title=data.get("title", ""),
            description=data.get("description", ""),
            narrative=data.get("narrative", ""),
            choices=data.get("choices", []),
            impacts=data.get("impacts", []),
            isCompleted=data.get("isCompleted", data.get("is_completed", False)),
            selectedChoice=data.get("selectedChoice", data.get("selected_choice")),
            plausibility=data.get("plausibility", 50),
            emotionalWeight=data.get("emotionalWeight", data.get("emotional_weight", 0.5)),
            createdAt=data.get("createdAt", data.get("created_at")),
            updatedAt=data.get("updatedAt", data.get("updated_at"))
        )


class Memory:
    """记忆 - 与前端 TypeScript 类型保持一致"""
    def __init__(self, id: str, profileId: str, eventId: str, summary: str,
                 emotionalWeight: float, recallCount: int, 
                 lastRecalled: Optional[str], retention: float, 
                 createdAt: Optional[str] = None, 
                 updatedAt: Optional[str] = None,
                 importance: float = 0.5):
        self.id = id
        self.profileId = profileId
        self.eventId = eventId
        self.summary = summary
        self.emotionalWeight = emotionalWeight
        self.recallCount = recallCount
        self.lastRecalled = lastRecalled
        self.retention = retention
        self.createdAt = createdAt if createdAt else datetime.now().isoformat()
        self.updatedAt = updatedAt if updatedAt else datetime.now().isoformat()
        self.importance = importance
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "profileId": self.profileId,
            "eventId": self.eventId,
            "summary": self.summary,
            "emotionalWeight": self.emotionalWeight,
            "recallCount": self.recallCount,
            "lastRecalled": self.lastRecalled,
            "retention": self.retention,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Memory':
        """从字典创建实例"""
        return cls(
            id=data.get("id", ""),
            profileId=data.get("profileId", data.get("profile_id", "")),
            eventId=data.get("eventId", data.get("event_id", "")),
            summary=data.get("summary", ""),
            emotionalWeight=data.get("emotionalWeight", data.get("emotional_weight", 0.5)),
            recallCount=data.get("recallCount", data.get("recall_count", 0)),
            lastRecalled=data.get("lastRecalled", data.get("last_recalled")),
            retention=data.get("retention", 1.0),
            createdAt=data.get("createdAt", data.get("created_at")),
            updatedAt=data.get("updatedAt", data.get("updated_at")),
            importance=data.get("importance", 0.5)
        )


# ==================== AI设置类型 ====================

class AISettings:
    """AI设置"""
    def __init__(self, use_local_model: bool = True, 
                 local_model_size: str = "1.5B",
                 use_free_api: bool = True,
                 custom_api: Optional[str] = None):
        self.useLocalModel = use_local_model
        self.localModelSize = local_model_size
        self.useFreeAPI = use_free_api
        self.customAPI = custom_api
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "useLocalModel": self.useLocalModel,
            "localModelSize": self.localModelSize,
            "useFreeAPI": self.useFreeAPI,
            "customAPI": self.customAPI
        }


# ==================== 导出所有类型 ====================

__all__ = [
    # 枚举
    'LifeStage',
    'EventType', 
    'Gender',
    # 五维系统
    'PhysicalDimensions',
    'PsychologicalDimensions',
    'CareerInfo',
    'EconomicInfo',
    'SocialDimensions',
    'KnowledgeInfo',
    'SkillsInfo',
    'MemoryAbilityInfo',
    'CognitiveDimensions',
    'IntimacyInfo',
    'NetworkInfo',
    'RelationalDimensions',
    'FiveDimensionSystem',
    # 核心类型
    'LifeProfile',
    'CharacterState',
    'EventChoice',
    'GameEvent',
    'Memory',
    'AISettings',
]
