"""
家族传承系统
实现角色家族关系、遗产传递和代际传承

功能：
1. 家族树结构 - 记录家族成员关系
2. 遗产传递 - 物质遗产和精神遗产
3. 家族特性 - 可继承的性格、天赋、财富
4. 下一代创建 - 基于上一代创建新角色
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import json
import uuid


class FamilyRelation(Enum):
    """家族关系类型"""
    PARENT = "parent"          # 父母
    CHILD = "child"            # 子女
    SPOUSE = "spouse"          # 配偶
    SIBLING = "sibling"        # 兄弟姐妹
    GRANDPARENT = "grandparent" # 祖父母
    GRANDCHILD = "grandchild"  # 孙辈


class LegacyType(Enum):
    """遗产类型"""
    MATERIAL = "material"      # 物质遗产：财富、资产
    SOCIAL = "social"          # 社会遗产：人脉、声誉
    COGNITIVE = "cognitive"    # 认知遗产：知识、技能
    PSYCHOLOGICAL = "psychological"  # 心理遗产：性格、价值观
    RELATIONAL = "relational"  # 关系遗产：家族纽带


class FamilyMember:
    """家族成员"""
    
    def __init__(
        self,
        member_id: str,
        name: str,
        gender: str,
        birth_year: int,
        death_year: Optional[int] = None,
        profile_id: Optional[str] = None,
        generation: int = 0
    ):
        self.member_id = member_id
        self.name = name
        self.gender = gender
        self.birth_year = birth_year
        self.death_year = death_year
        self.profile_id = profile_id  # 关联的角色档案ID
        self.generation = generation
        self.relations: Dict[str, FamilyRelation] = {}  # 关系列表
        self.legacy: Dict[str, Any] = {}  # 遗产


class FamilyLegacy:
    """家族遗产"""
    
    def __init__(
        self,
        legacy_type: LegacyType,
        name: str,
        value: Any,
        inherit_probability: float = 0.5,
        decay_rate: float = 0.1
    ):
        self.legacy_type = legacy_type
        self.name = name
        self.value = value
        self.inherit_probability = inherit_probability  # 继承概率
        self.decay_rate = decay_rate  # 代际衰减率


class FamilyTree:
    """家族树"""
    
    def __init__(self, family_id: str, founder_name: str):
        self.family_id = family_id
        self.founder_name = founder_name
        self.members: Dict[str, FamilyMember] = {}
        self.legacies: List[FamilyLegacy] = []
        self.family_stats = {
            "total_generations": 1,
            "total_members": 1,
            "total_wealth": 0,
            "family_reputation": 50,
            "notable_achievements": []
        }
        self.created_at = datetime.now().isoformat()
    
    def add_member(self, member: FamilyMember):
        """添加家族成员"""
        self.members[member.member_id] = member
        self.family_stats["total_members"] = len(self.members)
        self.family_stats["total_generations"] = max(
            self.family_stats["total_generations"],
            member.generation + 1
        )
    
    def add_relation(self, member1_id: str, member2_id: str, relation: FamilyRelation):
        """添加家族关系"""
        if member1_id in self.members and member2_id in self.members:
            self.members[member1_id].relations[member2_id] = relation
    
    def add_legacy(self, legacy: FamilyLegacy):
        """添加家族遗产"""
        self.legacies.append(legacy)


class FamilySystem:
    """家族系统管理器"""
    
    def __init__(self):
        self.families: Dict[str, FamilyTree] = {}
    
    def create_family(self, founder_name: str, founder_profile: Dict[str, Any]) -> FamilyTree:
        """创建新家族"""
        family_id = f"family_{uuid.uuid4().hex[:8]}"
        family = FamilyTree(family_id, founder_name)
        
        # 添加创始人
        founder = FamilyMember(
            member_id=f"member_{uuid.uuid4().hex[:8]}",
            name=founder_name,
            gender=founder_profile.get("gender", "male"),
            birth_year=founder_profile.get("birth_year", 2000),
            profile_id=founder_profile.get("profile_id"),
            generation=0
        )
        family.add_member(founder)
        
        # 初始化家族遗产
        self._initialize_legacy(family, founder_profile)
        
        self.families[family_id] = family
        return family
    
    def _initialize_legacy(self, family: FamilyTree, profile: Dict[str, Any]):
        """初始化家族遗产"""
        # 物质遗产
        economic = profile.get("dimensions", {}).get("social", {}).get("economic", 50)
        family.add_legacy(FamilyLegacy(
            legacy_type=LegacyType.MATERIAL,
            name="初始财富",
            value=economic,
            inherit_probability=0.7,
            decay_rate=0.1
        ))
        
        # 社会遗产
        career = profile.get("dimensions", {}).get("social", {}).get("career", 50)
        family.add_legacy(FamilyLegacy(
            legacy_type=LegacyType.SOCIAL,
            name="社会地位",
            value=career,
            inherit_probability=0.5,
            decay_rate=0.15
        ))
        
        # 心理遗产（性格）
        personality = profile.get("personality", {})
        if personality:
            family.add_legacy(FamilyLegacy(
                legacy_type=LegacyType.PSYCHOLOGICAL,
                name="家族性格",
                value=personality,
                inherit_probability=0.4,
                decay_rate=0.05
            ))
    
    def add_child(
        self,
        family_id: str,
        parent_id: str,
        child_name: str,
        child_gender: str,
        birth_year: int
    ) -> Optional[FamilyMember]:
        """添加子女"""
        family = self.families.get(family_id)
        if not family:
            return None
        
        parent = family.members.get(parent_id)
        if not parent:
            return None
        
        # 创建子女
        child = FamilyMember(
            member_id=f"member_{uuid.uuid4().hex[:8]}",
            name=child_name,
            gender=child_gender,
            birth_year=birth_year,
            generation=parent.generation + 1
        )
        
        # 添加关系
        child.relations[parent_id] = FamilyRelation.PARENT
        parent.relations[child.member_id] = FamilyRelation.CHILD
        
        family.add_member(child)
        
        return child
    
    def add_spouse(
        self,
        family_id: str,
        member_id: str,
        spouse_name: str,
        spouse_gender: str
    ) -> Optional[FamilyMember]:
        """添加配偶"""
        family = self.families.get(family_id)
        if not family:
            return None
        
        member = family.members.get(member_id)
        if not member:
            return None
        
        # 创建配偶
        spouse = FamilyMember(
            member_id=f"member_{uuid.uuid4().hex[:8]}",
            name=spouse_name,
            gender=spouse_gender,
            birth_year=member.birth_year,
            generation=member.generation
        )
        
        # 添加关系
        spouse.relations[member_id] = FamilyRelation.SPOUSE
        member.relations[spouse.member_id] = FamilyRelation.SPOUSE
        
        family.add_member(spouse)
        
        return spouse
    
    def calculate_inheritance(self, family_id: str, child_id: str) -> Dict[str, Any]:
        """计算子女继承的遗产"""
        family = self.families.get(family_id)
        if not family:
            return {}
        
        child = family.members.get(child_id)
        if not child:
            return {}
        
        inheritance = {}
        
        for legacy in family.legacies:
            # 根据继承概率和衰减率计算
            import random
            if random.random() < legacy.inherit_probability:
                inherited_value = legacy.value
                if isinstance(inherited_value, (int, float)):
                    # 数值型遗产按代际衰减
                    decay_factor = (1 - legacy.decay_rate) ** child.generation
                    inherited_value = inherited_value * decay_factor
                
                legacy_type = legacy.legacy_type.value
                if legacy_type not in inheritance:
                    inheritance[legacy_type] = {}
                inheritance[legacy_type][legacy.name] = {
                    "original_value": legacy.value,
                    "inherited_value": inherited_value,
                    "decay_factor": (1 - legacy.decay_rate) ** child.generation
                }
        
        return inheritance
    
    def create_next_generation_profile(
        self,
        family_id: str,
        child_name: str,
        child_gender: str,
        birth_year: int,
        parent_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """创建下一代角色档案"""
        family = self.families.get(family_id)
        if not family:
            return {}
        
        # 添加子女到家族树
        parent_id = None
        for member_id, member in family.members.items():
            if member.profile_id == parent_profile.get("id"):
                parent_id = member_id
                break
        
        if not parent_id:
            # 如果父辈不在家族树中，使用第一个成员作为父辈
            parent_id = list(family.members.keys())[0]
        
        child = self.add_child(family_id, parent_id, child_name, child_gender, birth_year)
        if not child:
            return {}
        
        # 计算继承
        inheritance = self.calculate_inheritance(family_id, child.member_id)
        
        # 创建新角色档案
        new_profile = {
            "id": f"profile_{uuid.uuid4().hex[:8]}",
            "name": child_name,
            "gender": child_gender,
            "birthDate": f"{birth_year}-01-01",
            "birthLocation": parent_profile.get("birthLocation", "北京"),
            "familyBackground": f"{family.founder_name}家族第{child.generation + 1}代",
            "family_id": family_id,
            "generation": child.generation,
            "parent_profile_id": parent_profile.get("id"),
            "initialPersonality": self._inherit_personality(parent_profile, inheritance),
            "initial_conditions": self._calculate_initial_conditions(inheritance),
            "inheritance": inheritance
        }
        
        child.profile_id = new_profile["id"]
        
        return new_profile
    
    def _inherit_personality(self, parent_profile: Dict[str, Any], inheritance: Dict[str, Any]) -> Dict[str, int]:
        """继承性格特征"""
        import random
        
        parent_personality = parent_profile.get("personality", {
            "openness": 50,
            "conscientiousness": 50,
            "extraversion": 50,
            "agreeableness": 50,
            "neuroticism": 50
        })
        
        # 基础继承 + 随机变异
        child_personality = {}
        for trait, value in parent_personality.items():
            # 继承40-60%的父母特征
            inherited = value * random.uniform(0.4, 0.6)
            # 添加随机变异
            variation = random.uniform(-15, 15)
            child_value = inherited + variation
            # 限制在0-100范围
            child_personality[trait] = max(0, min(100, int(child_value)))
        
        return child_personality
    
    def _calculate_initial_conditions(self, inheritance: Dict[str, Any]) -> Dict[str, Any]:
        """计算初始条件"""
        conditions = {
            "economic": 50,
            "social_status": 50,
            "education_bonus": 0
        }
        
        # 应用物质遗产
        if "material" in inheritance:
            for item in inheritance["material"].values():
                if isinstance(item.get("inherited_value"), (int, float)):
                    conditions["economic"] = min(100, 50 + item["inherited_value"] * 0.5)
        
        # 应用社会遗产
        if "social" in inheritance:
            for item in inheritance["social"].values():
                if isinstance(item.get("inherited_value"), (int, float)):
                    conditions["social_status"] = min(100, 50 + item["inherited_value"] * 0.3)
        
        return conditions
    
    def get_family_tree(self, family_id: str) -> Dict[str, Any]:
        """获取家族树结构"""
        family = self.families.get(family_id)
        if not family:
            return {}
        
        nodes = []
        links = []
        
        for member_id, member in family.members.items():
            nodes.append({
                "id": member.member_id,
                "name": member.name,
                "gender": member.gender,
                "birth_year": member.birth_year,
                "death_year": member.death_year,
                "generation": member.generation,
                "profile_id": member.profile_id
            })
            
            for related_id, relation in member.relations.items():
                # 避免重复添加关系
                if member_id < related_id:
                    links.append({
                        "source": member_id,
                        "target": related_id,
                        "type": relation.value
                    })
        
        return {
            "family_id": family.family_id,
            "founder_name": family.founder_name,
            "nodes": nodes,
            "links": links,
            "stats": family.family_stats,
            "legacies": [
                {
                    "type": l.legacy_type.value,
                    "name": l.name,
                    "value": l.value,
                    "inherit_probability": l.inherit_probability
                }
                for l in family.legacies
            ]
        }
    
    def get_family_summary(self, family_id: str) -> Dict[str, Any]:
        """获取家族总结"""
        family = self.families.get(family_id)
        if not family:
            return {}
        
        # 统计家族信息
        generations = {}
        for member in family.members.values():
            gen = member.generation
            if gen not in generations:
                generations[gen] = []
            generations[gen].append(member.name)
        
        return {
            "family_id": family.family_id,
            "founder_name": family.founder_name,
            "total_generations": family.family_stats["total_generations"],
            "total_members": family.family_stats["total_members"],
            "generation_details": generations,
            "family_reputation": family.family_stats["family_reputation"],
            "notable_achievements": family.family_stats["notable_achievements"],
            "created_at": family.created_at
        }


# 全局实例
family_system = FamilySystem()
