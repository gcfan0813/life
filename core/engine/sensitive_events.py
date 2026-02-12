"""
高敏事件处理协议
实现对用户心理有重大影响事件的温和处理机制

高敏事件定义：
- 死亡相关：角色死亡、亲人离世
- 重大疾病：癌症、重大事故
- 家庭变故：离婚、家庭破裂
- 心理创伤：抑郁、自杀倾向

处理原则：
1. 预警原则：提前告知可能的高敏内容
2. 选择原则：提供三选一的温和处理方式
3. 支持原则：提供心理支持和资源
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from datetime import datetime


class SensitivityLevel(Enum):
    """敏感度等级"""
    LOW = "low"          # 低敏感：普通挫折
    MEDIUM = "medium"    # 中敏感：重大变故
    HIGH = "high"        # 高敏感：死亡、重病
    CRITICAL = "critical"  # 极高敏感：自杀、极端事件


class HighSensitivityEventType(Enum):
    """高敏事件类型"""
    DEATH = "death"                    # 死亡
    SERIOUS_ILLNESS = "serious_illness" # 重病
    FAMILY_BREAKDOWN = "family_breakdown" # 家庭破裂
    DIVORCE = "divorce"                 # 离婚
    JOB_LOSS = "job_loss"              # 失业
    BANKRUPTCY = "bankruptcy"          # 破产
    TRAUMA = "trauma"                   # 心理创伤
    ADDICTION = "addiction"             # 成瘾
    CRIME = "crime"                     # 犯罪（受害者或加害者）
    SUICIDE_IDEOLOGY = "suicide_ideology"  # 自杀倾向


class HandlingMode(Enum):
    """处理模式"""
    SKIP = "skip"           # 跳过此事件
    SOFTEN = "soften"       # 温和处理（降低影响）
    FULL = "full"           # 完整体验


class HighSensitivityEvent:
    """高敏事件定义"""
    
    def __init__(
        self,
        event_type: HighSensitivityEventType,
        sensitivity_level: SensitivityLevel,
        title: str,
        description: str,
        normal_narrative: str,
        softened_narrative: str,
        impacts: Dict[str, Any],
        support_resources: List[str]
    ):
        self.event_type = event_type
        self.sensitivity_level = sensitivity_level
        self.title = title
        self.description = description
        self.normal_narrative = normal_narrative
        self.softened_narrative = softened_narrative
        self.impacts = impacts
        self.support_resources = support_resources


class HighSensitivityHandler:
    """高敏事件处理器"""
    
    def __init__(self):
        self.events = self._load_sensitive_events()
        self.user_preferences = {}  # 用户处理偏好
    
    def _load_sensitive_events(self) -> Dict[str, HighSensitivityEvent]:
        """加载高敏事件定义"""
        events = {
            # 死亡相关
            "character_death": HighSensitivityEvent(
                event_type=HighSensitivityEventType.DEATH,
                sensitivity_level=SensitivityLevel.CRITICAL,
                title="生命终结",
                description="角色生命的最后时刻",
                normal_narrative="生命的旅程走到了尽头。回顾这一生，有欢笑有泪水，有遗憾也有圆满。在亲人的陪伴下，安详地闭上了眼睛。",
                softened_narrative="这是一个庄严而温暖的告别时刻。生命的轮回是自然的一部分，重要的是这一生留下的美好回忆。",
                impacts={"physiological": {"health": -100}},
                support_resources=[
                    "生命热线：400-161-9995",
                    "心理咨询：当地心理健康中心"
                ]
            ),
            "family_member_death": HighSensitivityEvent(
                event_type=HighSensitivityEventType.DEATH,
                sensitivity_level=SensitivityLevel.HIGH,
                title="亲人离世",
                description="挚爱的亲人离开了",
                normal_narrative="亲人永远地离开了。悲痛之余，也记得他们留下的爱与美好回忆。生命的意义在于珍惜当下。",
                softened_narrative="这是一段关于爱与告别的旅程。逝者已矣，生者如斯。让我们怀着感恩的心，铭记那些美好的时光。",
                impacts={"psychological": {"resilience": -10, "emotional": -15}},
                support_resources=[
                    "哀伤辅导：当地社工服务中心",
                    "心理支持热线"
                ]
            ),
            
            # 疾病相关
            "serious_illness": HighSensitivityEvent(
                event_type=HighSensitivityEventType.SERIOUS_ILLNESS,
                sensitivity_level=SensitivityLevel.HIGH,
                title="重大疾病",
                description="被诊断出重大疾病",
                normal_narrative="医院传来沉重的诊断结果。这是一个艰难的时刻，但现代医学不断进步，希望永远存在。",
                softened_narrative="健康是人生的重要财富。面对挑战时，积极的心态是最好的良药。医疗团队会全力帮助您。",
                impacts={"physiological": {"health": -30}, "psychological": {"stress": 20}},
                support_resources=[
                    "医疗咨询：专业医疗机构",
                    "患者互助团体"
                ]
            ),
            
            # 家庭变故
            "divorce": HighSensitivityEvent(
                event_type=HighSensitivityEventType.DIVORCE,
                sensitivity_level=SensitivityLevel.MEDIUM,
                title="婚姻结束",
                description="婚姻走到了尽头",
                normal_narrative="经过深思熟虑，决定结束这段婚姻。虽然痛苦，但有时分开也是一种解脱。人生还有新的可能。",
                softened_narrative="人生的不同阶段有时需要不同的选择。这是一个新的开始，未来依然充满希望。",
                impacts={"relational": {"family": -20}, "psychological": {"emotional": -10}},
                support_resources=[
                    "婚姻家庭咨询热线",
                    "法律援助服务"
                ]
            ),
            "family_breakdown": HighSensitivityEvent(
                event_type=HighSensitivityEventType.FAMILY_BREAKDOWN,
                sensitivity_level=SensitivityLevel.HIGH,
                title="家庭破裂",
                description="家庭关系严重破裂",
                normal_narrative="家庭关系陷入深深的裂痕。每个人的选择都有其原因，也许时间和沟通能够弥合伤口。",
                softened_narrative="家庭关系有时会经历风雨。这是一个需要时间和理解的过程，每个人都有自己的道路。",
                impacts={"relational": {"family": -30}, "psychological": {"emotional": -15}},
                support_resources=[
                    "家庭治疗服务",
                    "社区支持中心"
                ]
            ),
            
            # 心理健康
            "depression": HighSensitivityEvent(
                event_type=HighSensitivityEventType.TRAUMA,
                sensitivity_level=SensitivityLevel.HIGH,
                title="情绪低落",
                description="经历持续的情绪低落",
                normal_narrative="最近感到心情沉重，什么都不想做。这是正常的情绪波动，但也值得关注。",
                softened_narrative="每个人都会有低落的时候，这并不代表软弱。适当的休息和寻求帮助是勇敢的选择。",
                impacts={"psychological": {"emotional": -20, "resilience": -5}},
                support_resources=[
                    "心理援助热线：400-161-9995",
                    "在线心理咨询平台",
                    "身边的亲友可以提供支持"
                ]
            ),
            "suicide_ideology": HighSensitivityEvent(
                event_type=HighSensitivityEventType.SUICIDE_IDEOLOGY,
                sensitivity_level=SensitivityLevel.CRITICAL,
                title="绝望时刻",
                description="经历极度的绝望感",
                normal_narrative="（此内容已做保护性处理）",
                softened_narrative="生命中有时会有极其艰难的时刻。请记住，您并不孤单，总有人愿意倾听和帮助。",
                impacts={},
                support_resources=[
                    "【重要】24小时心理危机干预热线：400-161-9995",
                    "北京心理危机研究与干预中心：010-82951332",
                    "生命热线：400-821-1215",
                    "请立即联系专业人士或信任的人"
                ]
            ),
            
            # 经济危机
            "bankruptcy": HighSensitivityEvent(
                event_type=HighSensitivityEventType.BANKRUPTCY,
                sensitivity_level=SensitivityLevel.MEDIUM,
                title="经济危机",
                description="遭遇严重的经济困境",
                normal_narrative="面临严峻的经济挑战。这是人生的低谷，但历史上很多人从更艰难的处境中重新站起。",
                softened_narrative="经济困难是暂时的。许多成功人士都经历过这样的挑战，这是重新开始的机会。",
                impacts={"social": {"economic": -40}},
                support_resources=[
                    "金融咨询服务",
                    "就业援助中心"
                ]
            ),
            "job_loss": HighSensitivityEvent(
                event_type=HighSensitivityEventType.JOB_LOSS,
                sensitivity_level=SensitivityLevel.MEDIUM,
                title="失业",
                description="失去了工作",
                normal_narrative="工作结束了。这是一个转折点，也是重新审视职业道路的机会。新的可能性正在等待。",
                softened_narrative="职业生涯中的变动是常态。这可能是通向更好机会的转折点。",
                impacts={"social": {"career": -20, "economic": -15}},
                support_resources=[
                    "就业服务中心",
                    "职业培训项目"
                ]
            ),
        }
        return events
    
    def check_sensitivity(self, event_data: Dict[str, Any]) -> Optional[SensitivityLevel]:
        """检查事件的敏感度"""
        event_type = event_data.get("eventType", "")
        title = event_data.get("title", "")
        description = event_data.get("description", "")
        
        # 检查是否为高敏事件
        sensitive_keywords = {
            SensitivityLevel.CRITICAL: ["死亡", "自杀", "绝症", "临终"],
            SensitivityLevel.HIGH: ["癌症", "离婚", "破产", "抑郁症", "亲人离世"],
            SensitivityLevel.MEDIUM: ["失业", "分手", "疾病", "经济困难"]
        }
        
        full_text = f"{event_type} {title} {description}"
        
        for level, keywords in sensitive_keywords.items():
            for keyword in keywords:
                if keyword in full_text:
                    return level
        
        return None
    
    def get_handling_options(self, event_id: str) -> Dict[str, Any]:
        """获取事件的处理选项"""
        event = self.events.get(event_id)
        if not event:
            return {
                "is_sensitive": False,
                "options": []
            }
        
        return {
            "is_sensitive": True,
            "sensitivity_level": event.sensitivity_level.value,
            "event_type": event.event_type.value,
            "title": event.title,
            "description": event.description,
            "options": [
                {
                    "id": "skip",
                    "label": "跳过此事件",
                    "description": "不经历这个事件，选择其他人生路径"
                },
                {
                    "id": "soften",
                    "label": "温和处理",
                    "description": "以更温和的方式体验这个事件"
                },
                {
                    "id": "full",
                    "label": "完整体验",
                    "description": "完整经历这个事件的所有内容"
                }
            ],
            "support_resources": event.support_resources,
            "warning": "这个事件可能对您的情绪产生影响，请选择最适合您的处理方式。"
        }
    
    def process_event(
        self,
        event_id: str,
        handling_mode: HandlingMode,
        character_state: Any = None
    ) -> Dict[str, Any]:
        """处理高敏事件"""
        event = self.events.get(event_id)
        if not event:
            return {"success": False, "error": "事件不存在"}
        
        result = {
            "success": True,
            "event_id": event_id,
            "handling_mode": handling_mode.value,
            "processed_at": datetime.now().isoformat()
        }
        
        if handling_mode == HandlingMode.SKIP:
            result["narrative"] = "您选择跳过了这个事件。人生有很多可能，这是您的选择。"
            result["impacts"] = {}
            result["skipped"] = True
            
        elif handling_mode == HandlingMode.SOFTEN:
            result["narrative"] = event.softened_narrative
            # 降低影响
            softened_impacts = {}
            for dim, changes in event.impacts.items():
                softened_impacts[dim] = {k: v * 0.3 for k, v in changes.items()}
            result["impacts"] = softened_impacts
            result["softened"] = True
            
        else:  # FULL
            result["narrative"] = event.normal_narrative
            result["impacts"] = event.impacts
        
        # 始终提供支持资源
        result["support_resources"] = event.support_resources
        result["sensitivity_level"] = event.sensitivity_level.value
        
        return result
    
    def get_event_by_type(self, event_type: HighSensitivityEventType) -> List[HighSensitivityEvent]:
        """按类型获取高敏事件"""
        return [e for e in self.events.values() if e.event_type == event_type]
    
    def set_user_preference(self, user_id: str, preference: Dict[str, HandlingMode]):
        """设置用户的高敏事件处理偏好"""
        self.user_preferences[user_id] = preference
    
    def get_user_preference(self, user_id: str, event_type: str) -> Optional[HandlingMode]:
        """获取用户的事件处理偏好"""
        prefs = self.user_preferences.get(user_id, {})
        return prefs.get(event_type)


# 全局实例
hs_handler = HighSensitivityHandler()
