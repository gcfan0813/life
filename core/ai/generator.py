"""
AI推演引擎 - 负责生成未来事件候选项
"""

import asyncio
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

# 本地类型定义
class GameEvent:
    def __init__(self, id, profileId, eventDate, eventType, title, description, narrative, choices, impacts, isCompleted, plausibility, emotionalWeight, createdAt, updatedAt):
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
        self.plausibility = plausibility
        self.emotionalWeight = emotionalWeight
        self.createdAt = createdAt
        self.updatedAt = updatedAt

class CharacterState:
    def __init__(self, profileId, currentDate, age, dimensions):
        self.profileId = profileId
        self.currentDate = currentDate
        self.age = age
        self.dimensions = dimensions

class EventChoice:
    def __init__(self, id, text, immediateImpacts, longTermEffects, riskLevel):
        self.id = id
        self.text = text
        self.immediateImpacts = immediateImpacts
        self.longTermEffects = longTermEffects
        self.riskLevel = riskLevel

# 临时类型定义
class AIReasoningResult:
    def __init__(self, candidateEvents, reasoning, confidence, modelUsed, cost):
        self.candidateEvents = candidateEvents
        self.reasoning = reasoning
        self.confidence = confidence
        self.modelUsed = modelUsed
        self.cost = cost

class EventImpact:
    def __init__(self, dimension, subDimension, change, duration_days=1):
        self.dimension = dimension
        self.subDimension = subDimension
        self.change = change
        self.duration_days = duration_days

class AIGenerator:
    """AI事件生成器"""
    
    def __init__(self):
        self.local_models = {}
        self.api_clients = {}
        self.template_library = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Any]:
        """加载本地模板库"""
        return {
            'daily': [
                {
                    'title': '日常锻炼',
                    'template': '今天你进行了{intensity}的锻炼。',
                    'impacts': [{'dimension': 'physiological', 'subDimension': 'fitness', 'change': 2}]
                },
                {
                    'title': '学习新知识', 
                    'template': '你花时间学习了{subject}相关的知识。',
                    'impacts': [{'dimension': 'cognitive', 'subDimension': 'knowledge', 'change': 3}]
                }
            ],
            'milestone': [
                {
                    'title': '职业晋升',
                    'template': '你在工作中表现出色，获得了{promotion_type}。',
                    'impacts': [{'dimension': 'social', 'subDimension': 'careerLevel', 'change': 10}]
                }
            ]
        }
    
    async def generate_events(
        self, 
        state: CharacterState, 
        days_ahead: int = 30,
        model_level: str = 'L1'
    ) -> AIReasoningResult:
        """生成未来事件候选项"""
        
        # 根据模型级别选择生成策略
        if model_level == 'L0':
            return await self._generate_from_templates(state, days_ahead)
        elif model_level == 'L1':
            return await self._generate_with_local_model(state, days_ahead)
        elif model_level in ['L2', 'L3']:
            return await self._generate_with_api(state, days_ahead, model_level)
        else:
            # 默认降级到模板
            return await self._generate_from_templates(state, days_ahead)
    
    async def _generate_from_templates(self, state: CharacterState, days_ahead: int) -> AIReasoningResult:
        """使用模板库生成事件（L0级别）"""
        candidate_events = []
        
        # 基于当前状态选择模板
        age = state.age
        career_level = state.dimensions.social.careerLevel
        
        # 日常事件模板
        daily_templates = self.template_library['daily']
        for i in range(min(3, days_ahead)):
            template = daily_templates[i % len(daily_templates)]
            
            event_date = self._calculate_future_date(state.currentDate, i + 1)
            
            event = GameEvent(
                id=f"template_{i}_{datetime.now().timestamp()}",
                profileId=state.profileId,
                eventDate=event_date,
                eventType='daily',
                title=template['title'],
                description=template['template'].format(
                    intensity='适度' if age > 40 else '高强度',
                    subject='职业技能' if career_level < 50 else '领导力'
                ),
                narrative=template['template'],
                choices=self._generate_basic_choices(),
                impacts=template['impacts'],
                isCompleted=False,
                plausibility=70,
                emotionalWeight=0.3,
                createdAt=datetime.now().isoformat(),
                updatedAt=datetime.now().isoformat()
            )
            candidate_events.append(event)
        
        return AIReasoningResult(
            candidateEvents=candidate_events,
            reasoning="基于模板库生成的日常事件",
            confidence=60,
            modelUsed="template_library",
            cost=0
        )
    
    async def _generate_with_local_model(self, state: CharacterState, days_ahead: int) -> AIReasoningResult:
        """使用本地模型生成事件（L1级别）"""
        # 简化实现：实际应加载本地量化模型
        
        # 模拟本地模型推理
        await asyncio.sleep(1)  # 模拟推理延迟
        
        candidate_events = []
        
        # 基于角色状态生成更个性化的事件
        personality = state.dimensions.psychological
        social = state.dimensions.social
        
        for i in range(min(5, days_ahead)):
            event_date = self._calculate_future_date(state.currentDate, i + 1)
            
            # 根据人格特质调整事件类型
            if personality.extraversion > 70:
                event_type = 'social'
                title = '社交活动邀请'
                description = f'你收到一个{self._get_social_event_type()}的邀请。'
            elif personality.conscientiousness > 70:
                event_type = 'career' 
                title = '工作机会'
                description = '有一个新的职业发展机会出现在你面前。'
            else:
                event_type = 'daily'
                title = '日常安排'
                description = '今天有一些日常事务需要处理。'
            
            event = GameEvent(
                id=f"local_{i}_{datetime.now().timestamp()}",
                profileId=state.profileId,
                eventDate=event_date,
                eventType=event_type,
                title=title,
                description=description,
                narrative=description,
                choices=self._generate_enhanced_choices(event_type),
                impacts=self._generate_impacts_based_on_personality(personality),
                isCompleted=False,
                plausibility=75,
                emotionalWeight=0.4 if event_type == 'career' else 0.3,
                createdAt=datetime.now().isoformat(),
                updatedAt=datetime.now().isoformat()
            )
            candidate_events.append(event)
        
        return AIReasoningResult(
            candidateEvents=candidate_events,
            reasoning="基于本地模型生成的个性化事件",
            confidence=75,
            modelUsed="local_1.5B",
            cost=0
        )
    
    async def _generate_with_api(self, state: CharacterState, days_ahead: int, model_level: str) -> AIReasoningResult:
        """使用API生成事件（L2/L3级别）"""
        # 简化实现：模拟API调用
        
        await asyncio.sleep(2)  # 模拟API延迟
        
        candidate_events = []
        
        # 生成更复杂、更真实的事件
        for i in range(min(5, days_ahead)):
            event_date = self._calculate_future_date(state.currentDate, i + 1)
            
            event = GameEvent(
                id=f"api_{i}_{datetime.now().timestamp()}",
                profileId=state.profileId,
                eventDate=event_date,
                eventType='milestone',
                title=self._generate_api_event_title(state),
                description=self._generate_api_event_description(state),
                narrative=self._generate_detailed_narrative(state),
                choices=self._generate_complex_choices(),
                impacts=self._generate_api_impacts(),
                isCompleted=False,
                plausibility=85,
                emotionalWeight=0.6,
                createdAt=datetime.now().isoformat(),
                updatedAt=datetime.now().isoformat()
            )
            candidate_events.append(event)
        
        model_used = "siliconflow_deepseek" if model_level == 'L2' else "custom_gpt4"
        
        return AIReasoningResult(
            candidateEvents=candidate_events,
            reasoning="基于API生成的高质量事件",
            confidence=85,
            modelUsed=model_used,
            cost=0.02 if model_level == 'L3' else 0
        )
    
    def _calculate_future_date(self, current_date: str, days: int) -> str:
        """计算未来日期"""
        current = datetime.fromisoformat(current_date)
        future = current + timedelta(days=days)
        return future.isoformat().split('T')[0]
    
    def _generate_basic_choices(self) -> List[EventChoice]:
        """生成基础选择项"""
        return [
            EventChoice(
                id=0,
                text="接受并继续",
                immediateImpacts=[],
                longTermEffects=["推进时间"],
                riskLevel=10
            ),
            EventChoice(
                id=1, 
                text="稍作考虑",
                immediateImpacts=[{"dimension": "psychological", "subDimension": "emotionalState", "change": -5}],
                longTermEffects=["延迟决策"],
                riskLevel=20
            )
        ]
    
    def _generate_enhanced_choices(self, event_type: str) -> List[EventChoice]:
        """生成增强选择项"""
        if event_type == 'social':
            return [
                EventChoice(id=0, text="欣然接受邀请", 
                          immediateImpacts=[{"dimension": "psychological", "subDimension": "emotionalState", "change": 10}],
                          longTermEffects=["扩大社交圈"], riskLevel=15),
                EventChoice(id=1, text="礼貌拒绝",
                          immediateImpacts=[{"dimension": "psychological", "subDimension": "emotionalState", "change": -5}],
                          longTermEffects=["保持现状"], riskLevel=10)
            ]
        else:
            return self._generate_basic_choices()
    
    def _generate_complex_choices(self) -> List[EventChoice]:
        """生成复杂选择项"""
        return [
            EventChoice(id=0, text="积极应对挑战",
                      immediateImpacts=[{"dimension": "psychological", "subDimension": "resilience", "change": 5}],
                      longTermEffects=["潜在重大收益"], riskLevel=40),
            EventChoice(id=1, text="稳妥处理",
                      immediateImpacts=[],
                      longTermEffects=["稳定发展"], riskLevel=20),
            EventChoice(id=2, text="寻求帮助",
                      immediateImpacts=[{"dimension": "relational", "subDimension": "networkSize", "change": 2}],
                      longTermEffects=["建立支持网络"], riskLevel=25)
        ]
    
    def _get_social_event_type(self) -> str:
        """获取社交活动类型"""
        types = ['朋友聚会', '行业交流', '社区活动', '家庭聚餐']
        import random
        return random.choice(types)
    
    def _generate_impacts_based_on_personality(self, personality: Any) -> List[EventImpact]:
        """基于人格生成影响"""
        impacts = []
        
        if personality.extraversion > 70:
            impacts.append(EventImpact("psychological", "emotionalState", 5, 1))
        if personality.neuroticism > 60:
            impacts.append(EventImpact("psychological", "stress", 3, 2))
        
        return impacts
    
    def _generate_api_event_title(self, state: CharacterState) -> str:
        """生成API事件标题"""
        titles = [
            f"职业生涯的转折点",
            f"人际关系的新发展", 
            f"个人成长的机遇",
            f"生活方式的调整"
        ]
        import random
        return random.choice(titles)
    
    def _generate_api_event_description(self, state: CharacterState) -> str:
        """生成API事件描述"""
        return f"在{state.currentDate}这一天，你面临着一个重要的选择，这将影响你未来的发展轨迹。"
    
    def _generate_detailed_narrative(self, state: CharacterState) -> str:
        """生成详细叙事"""
        return """阳光透过窗户洒在桌面上，你坐在那里沉思。这个决定看似简单，却可能改变你的人生方向。
        周围的环境让你回想起过去的经历，那些成功与失败都成为了今天的基石。"""
    
    def _generate_api_impacts(self) -> List[EventImpact]:
        """生成API级别的影响"""
        return [
            EventImpact("social", "careerLevel", 8, 30),
            EventImpact("psychological", "emotionalState", 10, 7),
            EventImpact("cognitive", "knowledge", 5, 15)
        ]

# 全局AI生成器实例
ai_generator = AIGenerator()