"""
角色状态初始化引擎
"""

import json
from datetime import datetime
from typing import Dict, Any

# 临时类型定义
class LifeProfile:
    def __init__(self, id, name, birth_date, birth_place, gender, initial_traits, era, difficulty, created_at, updated_at):
        self.id = id
        self.name = name
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.gender = gender
        self.initial_traits = initial_traits
        self.era = era
        self.difficulty = difficulty
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

class CharacterInitializer:
    """角色状态初始化器"""
    
    def __init__(self):
        self.base_attributes = self._load_base_attributes()
    
    def _load_base_attributes(self) -> Dict[str, Any]:
        """加载基础属性配置"""
        return {
            'physiological': {
                'health': 80,
                'energy': 70,
                'appearance': 50,
                'fitness': 60
            },
            'psychological': {
                'openness': 50,
                'conscientiousness': 50,
                'extraversion': 50,
                'agreeableness': 50,
                'neuroticism': 50,
                'happiness': 60,
                'stress': 30,
                'resilience': 50
            },
            'social': {
                'socialCapital': 30,
                'career': {
                    'level': 0,
                    'satisfaction': 50,
                    'income': 0
                },
                'economic': {
                    'wealth': 0,
                    'debt': 0,
                    'credit': 50
                }
            },
            'cognitive': {
                'knowledge': {
                    'academic': 0,
                    'practical': 0,
                    'creative': 50
                },
                'skills': {
                    'communication': 50,
                    'problemSolving': 50,
                    'leadership': 30
                },
                'memory': {
                    'shortTerm': 70,
                    'longTerm': 60,
                    'emotional': 60
                }
            },
            'relational': {
                'intimacy': {
                    'family': 70,
                    'friends': 40,
                    'romantic': 0
                },
                'network': {
                    'size': 10,
                    'quality': 50,
                    'diversity': 30
                }
            }
        }
    
    async def initialize_character_state(self, profile: LifeProfile) -> CharacterState:
        """初始化角色状态"""
        
        # 计算初始年龄
        birth_date = datetime.fromisoformat(profile.birth_date)
        current_date = datetime.fromisoformat(profile.birth_date)
        age = 0  # 从出生开始
        
        # 创建基础状态
        base_dimensions = self.base_attributes.copy()
        
        # 根据初始特质调整属性
        self._adjust_by_family_background(base_dimensions, profile.initial_traits.get('familyBackground', 'middle'))
        self._adjust_by_education(base_dimensions, profile.initial_traits.get('educationLevel', 'none'))
        self._adjust_by_health(base_dimensions, profile.initial_traits.get('healthStatus', 'average'))
        self._adjust_by_personality_traits(base_dimensions, profile.initial_traits)
        
        # 根据难度调整
        self._adjust_by_difficulty(base_dimensions, profile.difficulty)
        
        # 根据时代背景调整
        self._adjust_by_era(base_dimensions, profile.era)
        
        # 创建初始状态
        character_state = CharacterState(
            id=f"state_{profile.id}",
            profile_id=profile.id,
            current_date=profile.birth_date,
            age=age,
            dimensions=base_dimensions,
            location=profile.birth_place,
            occupation="无",
            education="未开始",
            life_stage=self._determine_life_stage(age),
            total_events=0,
            total_decisions=0,
            days_survived=0
        )
        
        return character_state
    
    def _adjust_by_family_background(self, dimensions: Dict[str, Any], background: str):
        """根据家庭背景调整属性"""
        adjustments = {
            'poor': {
                'social': {'socialCapital': -20, 'economic': {'wealth': -30, 'debt': 20}},
                'psychological': {'stress': 10, 'resilience': 5}
            },
            'middle': {
                'social': {'socialCapital': 0, 'economic': {'wealth': 0, 'debt': 0}}
            },
            'wealthy': {
                'social': {'socialCapital': 20, 'economic': {'wealth': 30, 'debt': -10}},
                'psychological': {'happiness': 5, 'stress': -5}
            }
        }
        
        if background in adjustments:
            self._apply_adjustments(dimensions, adjustments[background])
    
    def _adjust_by_education(self, dimensions: Dict[str, Any], education: str):
        """根据教育背景调整属性"""
        adjustments = {
            'none': {
                'cognitive': {'knowledge': {'academic': -20, 'practical': 0}},
                'social': {'career': {'level': -10}}
            },
            'primary': {
                'cognitive': {'knowledge': {'academic': -10, 'practical': 5}}
            },
            'secondary': {
                'cognitive': {'knowledge': {'academic': 0, 'practical': 10}}
            },
            'college': {
                'cognitive': {'knowledge': {'academic': 15, 'practical': 10}},
                'social': {'career': {'level': 5}}
            },
            'graduate': {
                'cognitive': {'knowledge': {'academic': 25, 'practical': 15}},
                'social': {'career': {'level': 10}}
            }
        }
        
        if education in adjustments:
            self._apply_adjustments(dimensions, adjustments[education])
    
    def _adjust_by_health(self, dimensions: Dict[str, Any], health: str):
        """根据健康状况调整属性"""
        adjustments = {
            'poor': {
                'physiological': {'health': -30, 'energy': -20, 'fitness': -25}
            },
            'average': {
                'physiological': {'health': 0, 'energy': 0}
            },
            'good': {
                'physiological': {'health': 10, 'energy': 10, 'fitness': 5}
            },
            'excellent': {
                'physiological': {'health': 20, 'energy': 15, 'fitness': 10}
            }
        }
        
        if health in adjustments:
            self._apply_adjustments(dimensions, adjustments[health])
    
    def _adjust_by_personality_traits(self, dimensions: Dict[str, Any], traits: Dict[str, Any]):
        """根据人格特质调整属性"""
        # 风险承受度
        risk_tolerance = traits.get('riskTolerance', 50)
        if risk_tolerance > 70:
            dimensions['psychological']['neuroticism'] -= 5
            dimensions['cognitive']['skills']['problemSolving'] += 5
        elif risk_tolerance < 30:
            dimensions['psychological']['conscientiousness'] += 5
            dimensions['psychological']['neuroticism'] += 5
        
        # 野心
        ambition = traits.get('ambition', 50)
        if ambition > 70:
            dimensions['psychological']['conscientiousness'] += 10
            dimensions['social']['career']['level'] += 5
        
        # 同理心
        empathy = traits.get('empathy', 50)
        if empathy > 70:
            dimensions['psychological']['agreeableness'] += 10
            dimensions['relational']['intimacy']['friends'] += 10
    
    def _adjust_by_difficulty(self, dimensions: Dict[str, Any], difficulty: str):
        """根据难度调整属性"""
        adjustments = {
            'easy': {
                'physiological': {'health': 10, 'energy': 10},
                'social': {'economic': {'wealth': 20}}
            },
            'normal': {
                # 默认属性，无调整
            },
            'hard': {
                'physiological': {'health': -10, 'energy': -10},
                'social': {'economic': {'wealth': -20, 'debt': 10}}
            },
            'nightmare': {
                'physiological': {'health': -30, 'energy': -20},
                'psychological': {'stress': 20, 'happiness': -15},
                'social': {'economic': {'wealth': -50, 'debt': 30}}
            }
        }
        
        if difficulty in adjustments:
            self._apply_adjustments(dimensions, adjustments[difficulty])
    
    def _adjust_by_era(self, dimensions: Dict[str, Any], era: str):
        """根据时代背景调整属性"""
        # 简化实现：根据时代关键词调整
        if '古代' in era or '封建' in era:
            dimensions['social']['career']['level'] -= 10
            dimensions['cognitive']['knowledge']['academic'] -= 15
        elif '现代' in era or '当代' in era:
            dimensions['cognitive']['knowledge']['academic'] += 10
            dimensions['social']['socialCapital'] += 5
    
    def _apply_adjustments(self, dimensions: Dict[str, Any], adjustments: Dict[str, Any]):
        """应用属性调整"""
        for dimension, sub_adjustments in adjustments.items():
            if dimension in dimensions:
                if isinstance(sub_adjustments, dict):
                    for sub_dimension, value in sub_adjustments.items():
                        if isinstance(value, dict):
                            # 嵌套属性
                            for nested_key, nested_value in value.items():
                                if sub_dimension in dimensions[dimension]:
                                    if nested_key in dimensions[dimension][sub_dimension]:
                                        # 确保目标值是数值类型
                                        if isinstance(dimensions[dimension][sub_dimension][nested_key], (int, float)):
                                            dimensions[dimension][sub_dimension][nested_key] += nested_value
                        else:
                            # 直接属性
                            if sub_dimension in dimensions[dimension]:
                                # 确保目标值是数值类型
                                if isinstance(dimensions[dimension][sub_dimension], (int, float)):
                                    dimensions[dimension][sub_dimension] += value
    
    def _determine_life_stage(self, age: float) -> str:
        """确定人生阶段"""
        if age < 1:
            return 'infant'
        elif age < 3:
            return 'toddler'
        elif age < 13:
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

# 全局角色初始化器实例
character_initializer = CharacterInitializer()