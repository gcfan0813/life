"""
角色状态初始化引擎
"""

import json
from datetime import datetime, timedelta
from typing import Dict, Any

from shared.types import LifeProfile, CharacterState

class CharacterInitializer:
    """角色状态初始化器"""
    
    def __init__(self):
        self.base_attributes = self._load_base_attributes()
    
    def _load_base_attributes(self) -> Dict[str, Any]:
        """加载基础属性配置"""
        return {
            'physiological': {
                'health': 85,
                'energy': 75,
                'appearance': 55,
                'fitness': 65
            },
            'psychological': {
                'openness': 55,
                'conscientiousness': 55,
                'extraversion': 55,
                'agreeableness': 55,
                'neuroticism': 45,
                'happiness': 65,
                'stress': 25,
                'resilience': 55
            },
            'social': {
                'socialCapital': 35,
                'career': {
                    'level': 0,
                    'satisfaction': 0,
                    'income': 0
                },
                'economic': {
                    'wealth': 0,
                    'debt': 0,
                    'credit': 0
                }
            },
            'cognitive': {
                'knowledge': {
                    'academic': 0,
                    'practical': 0,
                    'creative': 0
                },
                'skills': {
                    'communication': 0,
                    'problemSolving': 0,
                    'leadership': 0
                },
                'memory': {
                    'shortTerm': 70,
                    'longTerm': 60,
                    'emotional': 60
                }
            },
            'relational': {
                'intimacy': {
                    'family': 75,
                    'friends': 15,
                    'romantic': 0
                },
                'network': {
                    'size': 5,
                    'quality': 25,
                    'diversity': 10
                }
            }
        }
    
    async def initialize_character_state(self, profile: LifeProfile) -> CharacterState:
        """初始化角色状态"""
        
        # 计算初始日期（出生日期 + 起始年龄）
        birth_date = datetime.fromisoformat(profile.birthDate)
        starting_age_val = getattr(profile, 'startingAge', 0.0)
        
        # 计算当前游戏日期
        current_date_obj = birth_date + timedelta(days=int(starting_age_val * 365.25))
        current_date_str = current_date_obj.isoformat().split('T')[0]
        
        # 计算整数年龄
        age = current_date_obj.year - birth_date.year
        if (current_date_obj.month, current_date_obj.day) < (birth_date.month, birth_date.day):
            age -= 1
        
        # 创建基础状态
        base_dimensions = self.base_attributes.copy()
        
        # 根据初始特质调整属性
        self._adjust_by_family_background(base_dimensions, getattr(profile, 'familyBackground', 'middle'))
        
        # 如果起始年龄大于0，进行额外的人生历练调整（模拟成长过程）
        if starting_age_val > 0:
            self._apply_growth_simulation(base_dimensions, starting_age_val)
        
        # 创建初始状态
        character_state = CharacterState(
            id=f"state_{profile.id}",
            profileId=profile.id,
            currentDate=current_date_str,
            age=age,
            dimensions=base_dimensions,
            location=profile.birthLocation,
            occupation="无" if age < 18 else "待业",
            education="未开始" if age < 6 else "基础教育",
            lifeStage=self._determine_life_stage(age),
            totalEvents=0,
            totalDecisions=0,
            daysSurvived=(current_date_obj - birth_date).days
        )
        
        return character_state

    def _apply_growth_simulation(self, dimensions: Dict[str, Any], age: float):
        """模拟成长过程中的属性变化"""
        # 简单模拟：随着年龄增长，认知和社会属性会提升
        growth_factor = min(age / 20.0, 1.0) # 20岁达到一个基础峰值
        
        dimensions['cognitive']['knowledge']['practical'] += 20 * growth_factor
        dimensions['social']['socialCapital'] += 10 * growth_factor
        dimensions['physiological']['fitness'] += 10 * growth_factor
        
        if age >= 18:
            dimensions['social']['career']['level'] = 10
            dimensions['cognitive']['knowledge']['academic'] += 30
    
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