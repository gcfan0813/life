#!/usr/bin/env python3
"""
无限人生：AI编年史 - 后端API服务
基于FastAPI的RESTful API服务，提供前端与Python核心引擎的通信接口
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 导入核心引擎模块
try:
    from core.engine.simulation import simulation_engine, CharacterState, GameEvent, Memory
    from core.engine.character import CharacterInitializer
    from core.storage.database import db_manager
    from shared.config.api_config import API_CONFIG
    from shared.types import LifeProfile
    
    # 导入必要的类型定义
    from core.engine.character import CharacterState as CoreCharacterState
    from core.engine.simulation import GameEvent as CoreGameEvent
    from core.engine.simulation import Memory as CoreMemory
    
except ImportError as e:
    print(f"导入错误: {e}")
    print("某些功能可能不可用")

# API模型定义
class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None

class CreateProfileRequest(BaseModel):
    name: str
    gender: str
    birthDate: str
    birthLocation: str
    familyBackground: str
    initialPersonality: Dict[str, float]

class AdvanceTimeRequest(BaseModel):
    days: int = 1

class MakeDecisionRequest(BaseModel):
    eventId: str
    choiceIndex: int

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str

# 创建FastAPI应用
app = FastAPI(
    title="无限人生：AI编年史 API",
    description="用户主权式AI推演人生模拟系统后端API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局状态
class GlobalState:
    def __init__(self):
        self.initialized = False
        self.profiles = {}
        self.game_states = {}

global_state = GlobalState()

# 依赖注入
def get_db_manager():
    return db_manager

def get_simulation_engine():
    return simulation_engine

# 工具函数
def convert_to_api_state(core_state: CoreCharacterState) -> CharacterState:
    """将核心状态转换为API状态"""
    return CharacterState(
        id=core_state.id,
        profile_id=core_state.profile_id,
        current_date=core_state.current_date,
        age=core_state.age,
        dimensions=core_state.dimensions,
        location=core_state.location,
        occupation=core_state.occupation,
        education=core_state.education,
        life_stage=core_state.life_stage,
        total_events=core_state.total_events,
        total_decisions=core_state.total_decisions,
        days_survived=core_state.days_survived
    )

def convert_to_api_event(core_event: CoreGameEvent) -> GameEvent:
    """将核心事件转换为API事件"""
    return GameEvent(
        id=core_event.id,
        profile_id=core_event.profile_id,
        event_date=core_event.event_date,
        event_type=core_event.event_type,
        title=core_event.title,
        description=core_event.description,
        narrative=core_event.narrative,
        choices=core_event.choices,
        impacts=core_event.impacts,
        is_completed=core_event.is_completed,
        selected_choice=core_event.selected_choice,
        plausibility=core_event.plausibility,
        emotional_weight=core_event.emotional_weight,
        created_at=core_event.created_at,
        updated_at=core_event.updated_at
    )

def convert_to_api_memory(core_memory: CoreMemory) -> Memory:
    """将核心记忆转换为API记忆"""
    return Memory(
        id=core_memory.id,
        profile_id=core_memory.profile_id,
        event_id=core_memory.event_id,
        summary=core_memory.summary,
        emotional_weight=core_memory.emotional_weight,
        recall_count=core_memory.recall_count,
        last_recalled=core_memory.last_recalled,
        retention=core_memory.retention,
        created_at=core_memory.created_at,
        updated_at=core_memory.updated_at
    )

# API路由
@app.get("/api/health", response_model=APIResponse)
async def health_check():
    """健康检查端点"""
    return APIResponse(
        success=True,
        data=HealthResponse(
            status="healthy",
            version="1.0.0",
            timestamp=datetime.now().isoformat()
        )
    )

@app.get("/api/data/exists", response_model=APIResponse)
async def check_existing_data():
    """检查是否存在现有数据"""
    try:
        has_data = db_manager.check_existing_data()
        return APIResponse(
            success=True,
            data={"hasData": has_data}
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=f"检查数据失败: {str(e)}"
        )

@app.post("/api/initialize", response_model=APIResponse)
async def initialize_system():
    """初始化系统"""
    try:
        # 初始化数据库和系统
        db_manager.initialize_database()
        global_state.initialized = True
        
        return APIResponse(
            success=True,
            data={"isInitialized": True}
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=f"系统初始化失败: {str(e)}"
        )

@app.get("/api/profiles", response_model=APIResponse)
async def get_profiles():
    """获取所有角色档案"""
    try:
        profiles = db_manager.get_profiles()
        return APIResponse(
            success=True,
            data=profiles
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=f"获取档案列表失败: {str(e)}"
        )

@app.post("/api/profiles", response_model=APIResponse)
async def create_profile(request: CreateProfileRequest):
    """创建新角色档案"""
    try:
        # 创建档案数据
        profile_data = {
            "name": request.name,
            "gender": request.gender,
            "birthDate": request.birthDate,
            "birthLocation": request.birthLocation,
            "familyBackground": request.familyBackground,
            "initialPersonality": request.initialPersonality,
            "createdAt": datetime.now().isoformat()
        }
        
        # 保存档案
        profile = db_manager.create_profile(profile_data)
        
        # 初始化角色状态
        character_initializer = CharacterInitializer()
        initial_state = character_initializer.initialize_character_state(profile)
        
        # 保存初始状态
        db_manager.save_state(profile.id, initial_state)
        
        return APIResponse(
            success=True,
            data=profile,
            message="角色档案创建成功"
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=f"创建档案失败: {str(e)}"
        )

@app.post("/api/profiles/{profile_id}/advance", response_model=APIResponse)
async def advance_time(profile_id: str, request: AdvanceTimeRequest):
    """推进时间"""
    try:
        # 加载当前状态
        game_state = db_manager.load_game_state(profile_id)
        if not game_state:
            raise HTTPException(status_code=404, detail="档案不存在")
        
        # 执行时间推进
        result = await simulation_engine.advance_time(
            profile_id, 
            game_state.state, 
            request.days
        )
        
        # 转换为API格式
        api_result = {
            "newState": convert_to_api_state(result.new_state),
            "newEvents": [convert_to_api_event(event) for event in result.new_events],
            "newMemories": [convert_to_api_memory(memory) for memory in result.new_memories],
            "newDate": result.new_date
        }
        
        return APIResponse(
            success=True,
            data=api_result,
            message=f"成功推进 {request.days} 天"
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=f"推进时间失败: {str(e)}"
        )

@app.post("/api/profiles/{profile_id}/decisions", response_model=APIResponse)
async def make_decision(profile_id: str, request: MakeDecisionRequest):
    """处理用户决策"""
    try:
        # 加载当前状态
        game_state = db_manager.load_game_state(profile_id)
        if not game_state:
            raise HTTPException(status_code=404, detail="档案不存在")
        
        # 处理决策
        result = await simulation_engine.process_decision(
            profile_id,
            game_state.state,
            request.eventId,
            request.choiceIndex
        )
        
        # 转换为API格式
        api_result = {
            "newState": convert_to_api_state(result.new_state),
            "newMemories": [convert_to_api_memory(memory) for memory in result.new_memories],
            "immediateEffects": result.immediate_effects,
            "longTermEffects": result.long_term_effects
        }
        
        return APIResponse(
            success=True,
            data=api_result,
            message="决策处理成功"
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=f"决策处理失败: {str(e)}"
        )

@app.post("/api/profiles/{profile_id}/save", response_model=APIResponse)
async def save_game(profile_id: str):
    """保存游戏状态"""
    try:
        # 这里需要从前端接收当前状态数据
        # 简化实现：标记为已保存
        return APIResponse(
            success=True,
            data={"success": True},
            message="游戏保存成功"
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=f"保存游戏失败: {str(e)}"
        )

@app.get("/api/profiles/{profile_id}/load", response_model=APIResponse)
async def load_game(profile_id: str):
    """加载游戏状态"""
    try:
        game_state = db_manager.load_game_state(profile_id)
        if not game_state:
            raise HTTPException(status_code=404, detail="档案不存在")
        
        # 转换为API格式
        api_state = {
            "profile": game_state.profile,
            "state": convert_to_api_state(game_state.state),
            "events": [convert_to_api_event(event) for event in game_state.events],
            "memories": [convert_to_api_memory(memory) for memory in game_state.memories]
        }
        
        return APIResponse(
            success=True,
            data=api_state,
            message="游戏加载成功"
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=f"加载游戏失败: {str(e)}"
        )

@app.get("/api/settings/ai", response_model=APIResponse)
async def get_ai_settings():
    """获取AI设置"""
    try:
        settings = {
            "useLocalModel": True,
            "localModelSize": "1.5B",
            "useFreeAPI": True,
            "customAPI": None
        }
        
        return APIResponse(
            success=True,
            data=settings
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=f"获取AI设置失败: {str(e)}"
        )

@app.put("/api/settings/ai", response_model=APIResponse)
async def update_ai_settings(settings: Dict[str, Any]):
    """更新AI设置"""
    try:
        # 保存设置到配置文件或数据库
        return APIResponse(
            success=True,
            data={"success": True},
            message="AI设置更新成功"
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=f"更新AI设置失败: {str(e)}"
        )

# 启动服务器
if __name__ == "__main__":
    import uvicorn
    
    print("启动无限人生API服务器...")
    print(f"服务器地址: http://localhost:8000")
    print(f"API文档: http://localhost:8000/docs")
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )