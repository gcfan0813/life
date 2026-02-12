"""
简化版AI事件生成器 - 用于演示和测试
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

# 临时类型定义
class AIReasoningResult:
    def __init__(self, candidate_events, reasoning):
        self.candidateEvents = candidate_events
        self.reasoning = reasoning

class SimpleAIGenerator:
    """简化版AI事件生成器"""
    
    def __init__(self):
        self.event_templates = self._load_event_templates()
        self.model_levels = ['L0', 'L1', 'L2']
    
    def _load_event_templates(self) -> Dict[str, List[Dict]]:
        """加载事件模板"""
        return {
            'L0': [
                {
                    'title': '日常学习',
                    'description': '在学校进行日常学习活动',
                    'emotional_weight': 0.2,
                    'choices': [
                        {'text': '认真学习', 'immediateImpacts': [{'dimension': 'cognitive', 'subDimension': 'knowledge', 'change': 2}]},
                        {'text': '玩耍放松', 'immediateImpacts': [{'dimension': 'psychological', 'subDimension': 'happiness', 'change': 3}]}
                    ]
                },
                {
                    'title': '家庭活动', 
                    'description': '与家人共度时光',
                    'emotional_weight': 0.4,
                    'choices': [
                        {'text': '积极互动', 'immediateImpacts': [{'dimension': 'relational', 'subDimension': 'family', 'change': 5}]},
                        {'text': '独自活动', 'immediateImpacts': [{'dimension': 'psychological', 'subDimension': 'happiness', 'change': -1}]}
                    ]
                },
                {
                    'title': '运动锻炼',
                    'description': '参加体育活动锻炼身体',
                    'emotional_weight': 0.3,
                    'choices': [
                        {'text': '坚持锻炼', 'immediateImpacts': [{'dimension': 'physiological', 'subDimension': 'fitness', 'change': 3}]},
                        {'text': '休息一下', 'immediateImpacts': [{'dimension': 'psychological', 'subDimension': 'happiness', 'change': 2}]}
                    ]
                }
            ],
            'L1': [
                {
                    'title': '大学入学',
                    'description': '成功考入理想的大学',
                    'emotional_weight': 0.7,
                    'choices': [
                        {'text': '选择理工科', 'immediateImpacts': [{'dimension': 'cognitive', 'subDimension': 'academic', 'change': 8}]},
                        {'text': '选择文科', 'immediateImpacts': [{'dimension': 'cognitive', 'subDimension': 'creative', 'change': 6}]}
                    ]
                },
                {
                    'title': '第一份工作',
                    'description': '获得人生第一份正式工作',
                    'emotional_weight': 0.6,
                    'choices': [
                        {'text': '接受挑战', 'immediateImpacts': [{'dimension': 'social', 'subDimension': 'careerLevel', 'change': 10}]},
                        {'text': '继续寻找', 'immediateImpacts': [{'dimension': 'social', 'subDimension': 'economic', 'change': -5}]}
                    ]
                },
                {
                    'title': '恋爱关系',
                    'description': '遇到心动的人开始恋爱',
                    'emotional_weight': 0.8,
                    'choices': [
                        {'text': '主动追求', 'immediateImpacts': [{'dimension': 'relational', 'subDimension': 'romantic', 'change': 10}]},
                        {'text': '保持朋友', 'immediateImpacts': [{'dimension': 'psychological', 'subDimension': 'stress', 'change': -2}]}
                    ]
                }
            ],
            'L2': [
                {
                    'title': '职业晋升',
                    'description': '获得重要的职业晋升机会',
                    'emotional_weight': 0.8,
                    'choices': [
                        {'text': '接受晋升', 'immediateImpacts': [{'dimension': 'social', 'subDimension': 'careerLevel', 'change': 15}]},
                        {'text': '保持现状', 'immediateImpacts': [{'dimension': 'psychological', 'subDimension': 'stress', 'change': -5}]}
                    ]
                },
                {
                    'title': '创业机会',
                    'description': '发现一个有潜力的创业机会',
                    'emotional_weight': 0.9,
                    'choices': [
                        {'text': '勇敢尝试', 'immediateImpacts': [{'dimension': 'social', 'subDimension': 'economic', 'change': 20}]},
                        {'text': '谨慎观望', 'immediateImpacts': [{'dimension': 'psychological', 'subDimension': 'stress', 'change': -3}]}
                    ]
                },
                {
                    'title': '家庭建设',
                    'description': '考虑组建家庭的重要决定',
                    'emotional_weight': 0.9,
                    'choices': [
                        {'text': '建立家庭', 'immediateImpacts': [{'dimension': 'relational', 'subDimension': 'family', 'change': 15}]},
                        {'text': '专注事业', 'immediateImpacts': [{'dimension': 'social', 'subDimension': 'careerLevel', 'change': 10}]}
                    ]
                }
            ]
        }
    
    async def generate_events(self, current_state, days: int, model_level: str = 'L1') -> AIReasoningResult:
        """生成事件"""
        
        # 根据模型级别选择模板
        templates = self.event_templates.get(model_level, self.event_templates['L1'])
        
        # 根据天数确定生成事件数量
        event_count = min(days // 7 + 1, 3)  # 每周最多生成3个事件
        
        # 随机选择事件
        selected_events = []
        for _ in range(event_count):
            if templates:
                template = random.choice(templates)
                
                # 创建事件对象
                event = type('GameEvent', (), {
                    'id': f"event_{int(datetime.now().timestamp())}_{random.randint(1000, 9999)}",
                    'profile_id': 'demo_profile_001',
                    'event_date': current_state.current_date,
                    'event_type': 'life_event',
                    'title': template['title'],
                    'description': template['description'],
                    'narrative': '',
                    'choices': template['choices'],
                    'impacts': [{'dimension': 'psychological', 'subDimension': 'happiness', 'change': random.randint(1, 5)}],
                    'is_completed': False,
                    'selected_choice': None,
                    'plausibility': random.randint(70, 95),
                    'emotional_weight': template['emotional_weight'],
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                })()
                
                selected_events.append(event)
        
        # 生成推理说明
        reasoning = f"基于角色当前状态（年龄: {current_state.age}岁，人生阶段: {current_state.life_stage}）生成了 {len(selected_events)} 个事件。使用模型级别: {model_level}"
        
        return AIReasoningResult(
            candidate_events=selected_events,
            reasoning=reasoning
        )

# 全局AI生成器实例
simple_ai_generator = SimpleAIGenerator()