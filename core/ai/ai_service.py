"""
AI服务层 - 支持多API智能路由
实现L0-L3 AI推演分级和免费API集成
"""

import os
import json
import asyncio
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

# AI推演级别
class AILevel(Enum):
    L0_LOCAL = "L0"  # 本地规则引擎（免费）
    L1_LOCAL_MODEL = "L1"  # 本地量化模型（免费）
    L2_FREE_API = "L2"  # 免费API（有限额）
    L3_ADVANCED = "L3"  # 高级API（付费）

class APIProvider(Enum):
    LOCAL = "local"  # 本地生成
    LOCAL_MODEL = "local_model"  # 本地量化模型
    SILICON_FLOW = "silicon_flow"  # 硅基流动
    ZHIPU = "zhipu"  # 智谱AI
    BAIDU = "baidu"  # 百度
    ALIBABA = "alibaba"  # 阿里

class AIService:
    """AI服务管理器"""
    
    def __init__(self):
        self.current_level = AILevel.L0_LOCAL
        self.current_provider = APIProvider.LOCAL
        self.api_keys = self._load_api_keys()
        # 硅基流动默认模型
        self.silicon_flow_model = "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B"
        self.fallback_chain = [
            APIProvider.LOCAL,
            APIProvider.LOCAL_MODEL,
            APIProvider.SILICON_FLOW,
            APIProvider.ZHIPU,
            APIProvider.BAIDU
        ]
        
        # 本地模型管理器
        self.local_model = None
        self._init_local_model()
        
        # 检查本地模型系统状态
        self._check_local_model_system()
    
    def _init_local_model(self):
        """初始化本地模型管理器"""
        try:
            from core.ai.local_model_loader import local_model_manager
            self.local_model = local_model_manager
            print("[AI] 本地模型管理器已初始化")
        except ImportError as e:
            print(f"[AI] 本地模型管理器初始化失败: {e}")
    
    def _check_local_model_system(self):
        """检查本地模型系统状态"""
        if not self.local_model:
            print("[AI] WARNING: 本地模型系统不可用")
            return
        
        try:
            # 检查依赖状态
            deps = self.local_model.get_dependency_status()
            if deps["missing_required"]:
                print(f"[AI] WARNING: 缺少必需依赖: {', '.join(deps['missing_required'])}")
            
            # 检查兼容性
            compat = self.local_model.get_compatibility_report()
            if not compat["can_run_local_models"]:
                print("[AI] WARNING: 设备不完全兼容本地模型运行")
            
            # 显示可用模型
            available = self.local_model.get_available_models()
            ready_models = [m for m in available if m["available"]]
            downloadable = [m for m in available if m.get("downloadable") and not m["available"]]
            
            print(f"[AI] 本地模型状态: {len(ready_models)} 个就绪, {len(downloadable)} 个可下载")
            
            if ready_models:
                print(f"[AI] 就绪模型: {', '.join([m['name'] for m in ready_models[:3]])}")
            
        except Exception as e:
            print(f"[AI] 本地模型系统检查失败: {e}")
        
    def _load_api_keys(self) -> Dict[str, str]:
        """加载API密钥"""
        # 默认API密钥（用户提供的）
        default_keys = {
            'silicon_flow': 'sk-ecjqmtjapqgboinnulycfbsbyxcpfcatkjqaifirlxrgpiih',
            'zhipu': '',
            'baidu': '',
            'alibaba': ''
        }
        
        return {
            'silicon_flow': os.environ.get('SILICON_FLOW_API_KEY', default_keys['silicon_flow']),
            'zhipu': os.environ.get('ZHIPU_API_KEY', default_keys['zhipu']),
            'baidu': os.environ.get('BAIDU_API_KEY', default_keys['baidu']),
            'alibaba': os.environ.get('ALIBABA_API_KEY', default_keys['alibaba'])
        }
    
    def set_level(self, level: AILevel):
        """设置AI推演级别"""
        self.current_level = level
        print(f"[AI] 推演级别已切换到: {level.value}")
    
    def set_provider(self, provider: APIProvider):
        """设置API提供商"""
        self.current_provider = provider
        print(f"[AI] 当前API提供商: {provider.value}")
    
    async def generate_events(
        self,
        state: Any,
        num_events: int = 3,
        force_level: Optional[AILevel] = None
    ) -> Dict[str, Any]:
        """生成事件候选（自动路由）"""
        level = force_level or self.current_level
        
        try:
            if level == AILevel.L0_LOCAL:
                return await self._generate_local(state, num_events)
            elif level == AILevel.L1_LOCAL_MODEL:
                return await self._generate_local_model(state, num_events)
            elif level == AILevel.L2_FREE_API:
                return await self._generate_with_api(state, num_events)
            elif level == AILevel.L3_ADVANCED:
                return await self._generate_advanced(state, num_events)
        except Exception as e:
            print(f"[AI] 生成失败，尝试降级: {e}")
            # 降级到本地
            return await self._generate_local(state, num_events)
    
    async def _generate_local(self, state: Any, num_events: int) -> Dict[str, Any]:
        """L0: 本地规则引擎生成"""
        events = []
        age = getattr(state, 'age', 25)
        life_stage = getattr(state, 'life_stage', '青年')
        
        # 基于年龄和人生阶段生成事件模板
        templates = self._get_event_templates(age, life_stage)
        
        for i, template in enumerate(templates[:num_events]):
            event = {
                "id": f"local_{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]}_{i}",
                "eventType": template["type"],
                "title": template["title"],
                "description": template["description"],
                "narrative": template["narrative"],
                "choices": template["choices"],
                "impacts": template["impacts"],
                "plausibility": 75,
                "emotionalWeight": template.get("emotional_weight", 0.5)
            }
            events.append(event)
        
        return {
            "events": events,
            "reasoning": "基于本地规则引擎生成",
            "confidence": 0.75,
            "level": "L0_LOCAL",
            "provider": "local",
            "cost": 0
        }
    
    async def _generate_template(self, state: Any, num_events: int) -> Dict[str, Any]:
        """L1: 模板增强生成（已弃用，使用本地模型）"""
        return await self._generate_local_model(state, num_events)
    
    async def _generate_local_model(self, state: Any, num_events: int) -> Dict[str, Any]:
        """L1: 本地量化模型生成"""
        if not self.local_model:
            # 回退到本地规则
            print("[AI] 本地模型不可用，使用规则引擎")
            return await self._generate_local(state, num_events)
        
        try:
            # 检查模型状态
            status = self.local_model.get_status()
            if status["status"] != "ready":
                # 尝试加载模型
                print("[AI] 正在加载本地模型...")
                if not self.local_model.load_model():
                    print("[AI] 本地模型加载失败，使用规则引擎")
                    return await self._generate_local(state, num_events)
            
            # 使用本地模型生成
            result = self.local_model.generate_events(state, num_events)
            
            if result.get("events"):
                return result
            else:
                print("[AI] 本地模型生成失败，使用规则引擎")
                return await self._generate_local(state, num_events)
                
        except Exception as e:
            print(f"[AI] 本地模型出错: {e}")
            return await self._generate_local(state, num_events)
    
    async def _generate_with_api(self, state: Any, num_events: int) -> Dict[str, Any]:
        """L2: 使用免费API生成"""
        # 尝试硅基流动API
        if self.api_keys.get('silicon_flow'):
            try:
                return await self._call_silicon_flow(state, num_events)
            except Exception as e:
                print(f"[AI] 硅基流动API失败: {e}")
        
        # 回退到智谱AI
        if self.api_keys.get('zhipu'):
            try:
                return await self._call_zhipu(state, num_events)
            except Exception as e:
                print(f"[AI] 智谱AI失败: {e}")
        
        # 降级到本地
        print("[AI] API不可用，降级到本地生成")
        return await self._generate_local(state, num_events)
    
    async def _generate_advanced(self, state: Any, num_events: int) -> Dict[str, Any]:
        """L3: 高级API生成"""
        # 尝试所有可用API
        for provider in self.fallback_chain:
            if provider == APIProvider.LOCAL:
                continue
            try:
                if provider == APIProvider.LOCAL_MODEL and self.local_model:
                    result = await self._generate_local_model(state, num_events)
                    if result.get("events"):
                        return result
                elif provider == APIProvider.SILICON_FLOW and self.api_keys.get('silicon_flow'):
                    return await self._call_silicon_flow(state, num_events)
                elif provider == APIProvider.ZHIPU and self.api_keys.get('zhipu'):
                    return await self._call_zhipu(state, num_events)
            except:
                continue
        
        return await self._generate_local(state, num_events)
    
    async def _call_silicon_flow(self, state: Any, num_events: int) -> Dict[str, Any]:
        """调用硅基流动API"""
        import aiohttp
        
        age = getattr(state, 'age', 25)
        life_stage = getattr(state, 'life_stage', '青年')
        
        prompt = f"""请为以下角色生成{num_events}个人生事件：
- 年龄：{age}岁
- 人生阶段：{life_stage}
- 当前状态：{state.dimensions if hasattr(state, 'dimensions') else '正常'}

请生成JSON格式的事件列表，包含：title, description, eventType, choices, impacts"""
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://api.siliconflow.cn/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.api_keys["silicon_flow"]}',
                    'Content-Type': 'application/json'
                },
                json={
                    "model": self.silicon_flow_model,  # deepseek-ai/DeepSeek-R1-0528-Qwen3-8B
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1000
                }
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    content = data['choices'][0]['message']['content']
                    # 解析JSON
                    try:
                        events = json.loads(content)
                        return {
                            "events": events if isinstance(events, list) else [events],
                            "reasoning": "AI智能生成",
                            "confidence": 0.95,
                            "level": "L2_FREE_API",
                            "provider": "silicon_flow",
                            "cost": 0.001
                        }
                    except:
                        pass
        
        raise Exception("API响应解析失败")
    
    async def _call_zhipu(self, state: Any, num_events: int) -> Dict[str, Any]:
        """调用智谱AI API"""
        import aiohttp
        
        age = getattr(state, 'age', 25)
        life_stage = getattr(state, 'life_stage', '青年')
        
        prompt = f"""请为以下角色生成{num_events}个人生事件：
- 年龄：{age}岁
- 人生阶段：{life_stage}
- 当前状态：{state.dimensions if hasattr(state, 'dimensions') else '正常'}

请生成JSON格式的事件列表，包含：title, description, eventType, choices, impacts"""
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://open.bigmodel.cn/api/paas/v4/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.api_keys["zhipu"]}',
                    'Content-Type': 'application/json'
                },
                json={
                    "model": "glm-4-flash",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1000
                }
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    content = data['choices'][0]['message']['content']
                    try:
                        events = json.loads(content)
                        return {
                            "events": events if isinstance(events, list) else [events],
                            "reasoning": "智谱AI智能生成",
                            "confidence": 0.93,
                            "level": "L2_FREE_API",
                            "provider": "zhipu",
                            "cost": 0.0005
                        }
                    except:
                        pass
        
        raise Exception("智谱AI响应解析失败")
    
    def _get_event_templates(self, age: int, life_stage: str) -> List[Dict]:
        """获取事件模板"""
        templates = []
        
        if life_stage == "童年":
            templates = [
                {"type": "education", "title": "上小学", "description": "开始接受义务教育", 
                 "narrative": "背着书包走进校园，开启了人生的新篇章",
                 "choices": ["努力学习", "快乐玩耍", "两者兼顾"],
                 "impacts": {"cognitive": {"knowledge": 5}},
                 "emotional_weight": 0.6},
                {"type": "health", "title": "健康成长", "description": "身体发育良好", 
                 "narrative": "在父母的呵护下健康成长",
                 "choices": ["加强锻炼", "注意营养", "顺其自然"],
                 "impacts": {"physiological": {"health": 3, "energy": 2}},
                 "emotional_weight": 0.4}
            ]
        elif life_stage == "青年":
            templates = [
                {"type": "career", "title": "职业选择", "description": "面临职业发展的重要抉择", 
                 "narrative": "站在人生的十字路口，需要做出重要选择",
                 "choices": ["追求梦想", "稳定工作", "继续深造"],
                 "impacts": {"social": {"career": 10, "economic": 5}},
                 "emotional_weight": 0.8},
                {"type": "relationship", "title": "恋爱经历", "description": "遇到心动的对象", 
                 "narrative": "爱情悄然来临，心动的感觉令人难忘",
                 "choices": ["主动追求", "顺其自然", "专注于事业"],
                 "impacts": {"relational": {"intimacy": 10}},
                 "emotional_weight": 0.7}
            ]
        elif life_stage == "中年":
            templates = [
                {"type": "family", "title": "家庭建设", "description": "组建家庭的决定", 
                 "narrative": "家庭是人生的港湾",
                 "choices": ["结婚生子", "专注事业", "享受单身"],
                 "impacts": {"relational": {"family": 15}, "social": {"economic": -5}},
                 "emotional_weight": 0.8},
                {"type": "career", "title": "职业晋升", "description": "事业进入上升期", 
                 "narrative": "多年的努力终于得到回报",
                 "choices": ["接受挑战", "保持现状", "创业发展"],
                 "impacts": {"social": {"career": 15, "economic": 10}},
                 "emotional_weight": 0.6}
            ]
        else:  # 老年
            templates = [
                {"type": "health", "title": "健康保养", "description": "开始关注身体健康", 
                 "narrative": "健康是最大的财富",
                 "choices": ["坚持锻炼", "定期体检", "顺其自然"],
                 "impacts": {"physiological": {"health": 5}},
                 "emotional_weight": 0.5},
                {"type": "retirement", "title": "退休生活", "description": "开启退休生活", 
                 "narrative": "辛苦了一辈子，现在是享受生活的时候",
                 "choices": ["旅游度假", "含饴弄孙", "发挥余热"],
                 "impacts": {"psychological": {"satisfaction": 10}},
                 "emotional_weight": 0.4}
            ]
        
        return templates
    
    def get_status(self) -> Dict[str, Any]:
        """获取AI服务状态"""
        return {
            "current_level": self.current_level.value,
            "current_provider": self.current_provider.value,
            "available_apis": {
                "silicon_flow": bool(self.api_keys.get('silicon_flow')),
                "zhipu": bool(self.api_keys.get('zhipu')),
                "baidu": bool(self.api_keys.get('baidu')),
                "alibaba": bool(self.api_keys.get('alibaba'))
            },
            "fallback_chain": [p.value for p in self.fallback_chain]
        }

# 全局AI服务实例
ai_service = AIService()
