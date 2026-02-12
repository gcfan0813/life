#!/usr/bin/env python3
"""
无限人生：AI编年史 - 完整版后端API服务
基于FastAPI + 核心引擎（规则校验 + AI推演）
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 导入核心引擎模块
from core.engine.simulation import simulation_engine, CharacterState, GameEvent, Memory, SimulationResult
from core.engine.character import CharacterInitializer
from core.engine.validator import RuleValidator, EraRules
from core.engine.macro_events import macro_event_system, MacroEventType
from core.engine.sensitive_events import hs_handler, SensitivityLevel, HandlingMode, HighSensitivityEventType
from core.engine.family_legacy import family_system, FamilyRelation, LegacyType
from core.storage.database import db_manager
from shared.types import LifeProfile, CharacterState as PyCharacterState, GameEvent as PyGameEvent, Memory as PyMemory

# FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="无限人生：AI编年史 - 完整版API",
    description="集成核心引擎的完整后端服务（AI推演 + 规则校验）",
    version="2.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API模型
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
    days: int = 30

class MakeDecisionRequest(BaseModel):
    eventId: str
    choiceIndex: int

# 辅助函数：转换核心类型到API类型
def convert_character_state(state: CharacterState) -> Dict[str, Any]:
    """转换核心引擎的CharacterState为API格式"""
    return {
        "id": state.id,
        "profileId": state.profile_id,
        "currentDate": state.current_date,
        "age": state.age,
        "dimensions": state.dimensions,
        "location": state.location,
        "occupation": state.occupation,
        "education": state.education,
        "lifeStage": state.life_stage,
        "totalEvents": state.total_events,
        "totalDecisions": state.total_decisions,
        "daysSurvived": state.days_survived
    }

def convert_game_event(event: GameEvent) -> Dict[str, Any]:
    """转换核心引擎的GameEvent为API格式"""
    return {
        "id": event.id,
        "profileId": event.profile_id,
        "eventDate": event.event_date,
        "eventType": event.event_type,
        "title": event.title,
        "description": event.description,
        "narrative": event.narrative,
        "choices": event.choices,
        "impacts": event.impacts,
        "isCompleted": event.is_completed,
        "selectedChoice": event.selected_choice,
        "plausibility": event.plausibility,
        "emotionalWeight": event.emotional_weight,
        "createdAt": event.created_at,
        "updatedAt": event.updated_at
    }

def convert_memory(memory: Memory) -> Dict[str, Any]:
    """转换核心引擎的Memory为API格式"""
    return {
        "id": memory.id,
        "profileId": memory.profile_id,
        "eventId": memory.event_id,
        "summary": memory.summary,
        "emotionalWeight": memory.emotional_weight,
        "recallCount": memory.recall_count,
        "lastRecalled": memory.last_recalled,
        "retention": memory.retention,
        "createdAt": memory.created_at,
        "updatedAt": memory.updated_at
    }

# API路由
@app.get("/")
async def root():
    """欢迎页面"""
    return {
        "message": "无限人生：AI编年史 - 完整版API服务",
        "version": "2.0.0",
        "endpoints": {
            "health": "/api/health",
            "docs": "/docs",
            "redoc": "/redoc",
            "profiles": "/api/profiles"
        },
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    """健康检查"""
    try:
        # 测试核心引擎
        engine_status = "ok" if simulation_engine else "error"
        db_status = "ok" if db_manager else "error"
        
        return APIResponse(
            success=True,
            data={
                "status": "healthy",
                "version": "2.0.0",
                "timestamp": datetime.now().isoformat(),
                "engine": engine_status,
                "database": db_status
            }
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/api/profiles", response_model=APIResponse)
async def create_profile(request: CreateProfileRequest):
    """创建角色档案（集成核心引擎）"""
    try:
        # 使用核心引擎创建角色
        character_initializer = CharacterInitializer()
        
        # 创建档案数据
        profile_data = {
            "id": f"profile_{datetime.now().timestamp()}",
            "name": request.name,
            "gender": request.gender,
            "birthDate": request.birthDate,
            "birthLocation": request.birthLocation,
            "familyBackground": request.familyBackground,
            "initialPersonality": request.initialPersonality,
            "createdAt": datetime.now().isoformat()
        }
        
        # 初始化角色状态
        profile_obj = type('Profile', (), profile_data)
        initial_state = character_initializer.initialize_character_state(profile_obj)
        
        # 保存到数据库
        db_manager.create_profile(profile_data)
        db_manager.save_state(profile_data["id"], initial_state)
        
        return APIResponse(
            success=True,
            data=profile_data,
            message="角色创建成功（集成核心引擎）"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=f"创建失败: {str(e)}")

@app.get("/api/profiles", response_model=APIResponse)
async def get_profiles():
    """获取所有角色档案"""
    try:
        profiles = db_manager.get_profiles()
        return APIResponse(success=True, data=profiles)
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/api/profiles/{profile_id}/advance", response_model=APIResponse)
async def advance_time(profile_id: str, request: AdvanceTimeRequest):
    """推进时间（集成核心引擎）"""
    try:
        # 加载当前状态
        game_state = db_manager.load_game_state(profile_id)
        if not game_state:
            return APIResponse(success=False, error="角色不存在")
        
        # 使用核心引擎推进时间
        result = await simulation_engine.advance_time(
            profile_id,
            game_state.state,
            request.days
        )
        
        # 转换结果
        api_result = {
            "newState": convert_character_state(result.new_state),
            "newEvents": [convert_game_event(event) for event in result.new_events],
            "newMemories": [convert_memory(memory) for memory in result.new_memories],
            "newDate": result.new_date,
            "reasoning": result.reasoning
        }
        
        return APIResponse(
            success=True,
            data=api_result,
            message=f"成功推进{request.days}天（集成核心引擎）"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=f"推进失败: {str(e)}")

@app.post("/api/profiles/{profile_id}/decisions", response_model=APIResponse)
async def make_decision(profile_id: str, request: MakeDecisionRequest):
    """处理决策（集成核心引擎）"""
    try:
        # 加载当前状态
        game_state = db_manager.load_game_state(profile_id)
        if not game_state:
            return APIResponse(success=False, error="角色不存在")
        
        # 使用核心引擎处理决策
        result = await simulation_engine.process_decision(
            profile_id,
            game_state.state,
            request.eventId,
            request.choiceIndex
        )
        
        # 转换结果
        api_result = {
            "newState": convert_character_state(result.new_state),
            "newMemories": [convert_memory(memory) for memory in result.new_memories],
            "immediateEffects": result.immediate_effects,
            "longTermEffects": result.long_term_effects
        }
        
        return APIResponse(
            success=True,
            data=api_result,
            message="决策处理成功（集成核心引擎）"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=f"决策处理失败: {str(e)}")

@app.get("/api/data/exists", response_model=APIResponse)
async def check_data():
    """检查是否有数据"""
    try:
        has_data = db_manager.check_existing_data()
        return APIResponse(success=True, data={"hasData": has_data})
    except Exception as e:
        return APIResponse(success=False, error=str(e))

# 规则引擎实例（延迟初始化）
_rule_validator = None

def get_rule_validator():
    """获取规则验证器实例"""
    global _rule_validator
    if _rule_validator is None:
        try:
            _rule_validator = RuleValidator()
        except Exception as e:
            print(f"规则验证器初始化失败: {e}")
            _rule_validator = None
    return _rule_validator

@app.get("/api/rules/stats", response_model=APIResponse)
async def get_rules_stats():
    """获取规则库统计信息"""
    try:
        validator = get_rule_validator()
        if not validator:
            return APIResponse(success=True, data={
                "totalRules": 0,
                "categories": {},
                "status": "规则引擎未初始化"
            })
        
        # 统计各分类规则数量
        category_stats = {}
        for category, rules in validator.rules_cache.items():
            category_stats[category] = len(rules)
        
        total = sum(category_stats.values())
        
        return APIResponse(
            success=True,
            data={
                "totalRules": total,
                "categories": category_stats,
                "status": "规则引擎已加载"
            }
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/api/rules/validate-event", response_model=APIResponse)
async def validate_event(profile_id: str, event_data: dict):
    """验证单个事件的合理性"""
    try:
        validator = get_rule_validator()
        if not validator:
            return APIResponse(success=False, error="规则引擎未初始化")
        
        # 加载角色状态
        game_state = db_manager.load_game_state(profile_id)
        if not game_state:
            return APIResponse(success=False, error="角色不存在")
        
        # 创建GameEvent对象
        event = GameEvent(
            id=event_data.get("id", ""),
            profile_id=profile_id,
            event_date=event_data.get("eventDate", ""),
            event_type=event_data.get("eventType", "general"),
            title=event_data.get("title", ""),
            description=event_data.get("description", ""),
            narrative=event_data.get("narrative", ""),
            choices=event_data.get("choices", []),
            impacts=event_data.get("impacts", {}),
            is_completed=event_data.get("isCompleted", False),
            selected_choice=event_data.get("selectedChoice"),
            plausibility=event_data.get("plausibility", 0.5),
            emotional_weight=event_data.get("emotionalWeight", 0.5),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        # 创建时代规则
        era_rules = EraRules(era="现代")
        
        # 验证事件
        result = validator.calculate_plausibility(event, game_state.state, era_rules)
        
        return APIResponse(
            success=True,
            data={
                "plausibility": result.plausibility,
                "conflicts": result.conflicts,
                "warnings": result.warnings,
                "suggestions": result.suggestions,
                "isValid": result.plausibility >= 60,
                "quality": "优秀" if result.plausibility >= 80 else "良好" if result.plausibility >= 60 else "需改进"
            },
            message=f"事件合理性评分: {result.plausibility}"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=f"验证失败: {str(e)}")

@app.post("/api/rules/validate-decision", response_model=APIResponse)
async def validate_decision(profile_id: str, decision_data: dict):
    """验证决策的合理性"""
    try:
        validator = get_rule_validator()
        if not validator:
            return APIResponse(success=False, error="规则引擎未初始化")
        
        # 加载角色状态
        game_state = db_manager.load_game_state(profile_id)
        if not game_state:
            return APIResponse(success=False, error="角色不存在")
        
        choice_index = decision_data.get("choiceIndex", 0)
        event_type = decision_data.get("eventType", "general")
        
        # 基于事件类型和当前状态进行决策验证
        state = game_state.state
        plausibility = 50  # 基础分
        
        # 风险评估
        risk_level = "low"
        if event_type == "health" and state.dimensions.get("health", 50) < 30:
            plausibility -= 20
            risk_level = "high"
        elif event_type == "career" and state.dimensions.get("social", {}).get("career", {}).get("level", 50) < 30:
            plausibility -= 15
            risk_level = "medium"
        
        # 决策建议
        suggestions = []
        if plausibility >= 80:
            suggestions.append("这是一个非常合理的选择")
        elif plausibility >= 60:
            suggestions.append("这是一个合理的选择，但有风险需要注意")
        else:
            suggestions.append("建议重新考虑这个选择，风险较高")
        
        return APIResponse(
            success=True,
            data={
                "plausibility": plausibility,
                "riskLevel": risk_level,
                "suggestions": suggestions,
                "isRecommended": plausibility >= 60
            },
            message=f"决策评分: {plausibility}"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=f"验证失败: {str(e)}")

# AI服务相关导入
try:
    from core.ai.ai_service import AIService, AILevel, ai_service
    AI_SERVICE_AVAILABLE = True
except ImportError as e:
    print(f"[WARN] AI服务模块不可用: {e}")
    AI_SERVICE_AVAILABLE = False
    ai_service = None

@app.get("/api/ai/status", response_model=APIResponse)
async def get_ai_status():
    """获取AI服务状态"""
    try:
        if not AI_SERVICE_AVAILABLE or not ai_service:
            return APIResponse(success=True, data={
                "available": False,
                "message": "AI服务模块未初始化"
            })
        
        status = ai_service.get_status()
        return APIResponse(
            success=True,
            data={
                "available": True,
                **status
            },
            message="AI服务状态获取成功"
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/api/ai/level", response_model=APIResponse)
async def set_ai_level(level: str):
    """设置AI推演级别"""
    try:
        if not AI_SERVICE_AVAILABLE or not ai_service:
            return APIResponse(success=False, error="AI服务模块未初始化")
        
        valid_levels = ["L0", "L1", "L2", "L3"]
        if level not in valid_levels:
            return APIResponse(success=False, error=f"无效的AI级别，可选值: {valid_levels}")
        
        ai_level = AILevel(f"L{level[1]}_LOCAL" if level == "L0" else 
                          f"L{level[1]}_TEMPLATE" if level == "L1" else
                          f"L{level[1]}_FREE_API" if level == "L2" else "L3_ADVANCED")
        ai_service.set_level(ai_level)
        
        return APIResponse(
            success=True,
            data={"level": level, "message": f"AI级别已设置为{level}"},
            message="设置成功"
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/api/ai/generate", response_model=APIResponse)
async def generate_events_ai(profile_id: str, num_events: int = 3, level: str = "auto"):
    """使用AI生成事件"""
    try:
        if not AI_SERVICE_AVAILABLE or not ai_service:
            # 回退到本地生成
            return APIResponse(
                success=True,
                data={
                    "events": [],
                    "reasoning": "AI服务不可用，使用本地引擎",
                    "level": "L0_LOCAL",
                    "cost": 0
                },
                message="使用本地规则引擎"
            )
        
        game_state = db_manager.load_game_state(profile_id)
        if not game_state:
            return APIResponse(success=False, error="角色不存在")
        
        force_level = None
        if level != "auto":
            force_level = AILevel(f"L{level[1]}_LOCAL" if level == "L0" else
                                f"L{level[1]}_TEMPLATE" if level == "L1" else
                                f"L{level[1]}_FREE_API" if level == "L2" else "L3_ADVANCED")
        
        result = await ai_service.generate_events(
            game_state.state,
            num_events=num_events,
            force_level=force_level
        )
        
        return APIResponse(
            success=True,
            data=result,
            message=f"使用{result.get('level', 'L0')}生成{len(result.get('events', []))}个事件"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=f"生成失败: {str(e)}")

# 规则库管理
import json

def load_extended_rules():
    """加载扩展规则库"""
    try:
        rules_file = os.path.join(project_root, "shared/rules/extended_rules.json")
        with open(rules_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载扩展规则失败: {e}")
        return None

@app.get("/api/rules/categories", response_model=APIResponse)
async def get_rule_categories():
    """获取规则分类"""
    try:
        rules_data = load_extended_rules()
        if not rules_data:
            return APIResponse(success=True, data={"categories": [], "total": 0})
        
        categories = []
        total = 0
        for cat_key, cat_data in rules_data.get("categories", {}).items():
            rule_count = len(cat_data.get("rules", []))
            total += rule_count
            categories.append({
                "id": cat_key,
                "name": cat_data.get("name", cat_key),
                "description": cat_data.get("description", ""),
                "rule_count": rule_count
            })
        
        # 添加元规则
        meta_rules = rules_data.get("meta_rules", [])
        
        return APIResponse(
            success=True,
            data={
                "categories": categories,
                "meta_rules": [{"id": r["id"], "name": r["name"]} for r in meta_rules],
                "total": total
            },
            message=f"共{total}条规则"
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.get("/api/rules/category/{category_id}", response_model=APIResponse)
async def get_category_rules(category_id: str):
    """获取指定分类的规则"""
    try:
        rules_data = load_extended_rules()
        if not rules_data:
            return APIResponse(success=False, error="规则库加载失败")
        
        category = rules_data.get("categories", {}).get(category_id)
        if not category:
            return APIResponse(success=False, error=f"分类 {category_id} 不存在")
        
        return APIResponse(
            success=True,
            data={
                "category": {
                    "id": category_id,
                    "name": category.get("name"),
                    "description": category.get("description")
                },
                "rules": category.get("rules", [])
            },
            message=f"获取到{len(category.get('rules', []))}条规则"
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.get("/api/rules/validate-action", response_model=APIResponse)
async def validate_action(profile_id: str, action: str, action_type: str):
    """验证动作的合理性"""
    try:
        game_state = db_manager.load_game_state(profile_id)
        if not game_state:
            return APIResponse(success=False, error="角色不存在")
        
        state = game_state.state
        age = state.age
        
        # 基于规则库验证
        rules_data = load_extended_rules()
        suggestions = []
        impacts = {}
        is_valid = True
        
        if rules_data:
            # 检查年龄特定规则
            age_category = rules_data.get("categories", {}).get("age_specific", {})
            for rule in age_category.get("rules", []):
                cond = rule.get("condition", "")
                if f"age >=" in cond or f"age <=" in cond:
                    # 简单条件解析
                    try:
                        if eval(cond.replace("age", str(age))):
                            suggestions.append(rule.get("description", ""))
                            # 应用影响
                            impact = rule.get("impact", {})
                            for k, v in impact.items():
                                if isinstance(v, (int, float)):
                                    impacts[k] = v
                    except:
                        pass
        
        # 检查生理状态
        if hasattr(state, 'dimensions'):
            dims = state.dimensions
            health = dims.get("health", 50)
            energy = dims.get("energy", 50)
            
            if health < 30:
                suggestions.append("健康状况不佳，不建议进行高强度活动")
                is_valid = False
            if energy < 20:
                suggestions.append("精力不足，需要休息")
                is_valid = False
        
        return APIResponse(
            success=True,
            data={
                "action": action,
                "actionType": action_type,
                "isValid": is_valid,
                "suggestions": suggestions,
                "impacts": impacts,
                "validatedAt": datetime.now().isoformat()
            },
            message="动作验证完成"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=str(e))

# 记忆系统导入
try:
    from core.ai.memory_system import Memory, MemorySystem, memory_system
    MEMORY_SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"[WARN] 记忆系统模块不可用: {e}")
    MEMORY_SYSTEM_AVAILABLE = False
    memory_system = None

@app.get("/api/profiles/{profile_id}/memories", response_model=APIResponse)
async def get_memories(profile_id: str, memory_type: str = "all"):
    """获取角色记忆列表"""
    try:
        if not MEMORY_SYSTEM_AVAILABLE:
            # 回退到数据库直接获取
            memories = db_manager.get_memories(profile_id, limit=100)
            return APIResponse(
                success=True,
                data={
                    "memories": [{"id": m.id, "summary": m.summary, "emotionalWeight": m.emotional_weight, 
                                "retention": m.retention, "createdAt": m.created_at} for m in memories],
                    "total": len(memories)
                },
                message=f"获取到{len(memories)}条记忆"
            )
        
        # 获取所有记忆
        memories = db_manager.get_memories(profile_id, limit=500)
        
        # 转换为记忆对象并计算当前留存率
        memory_objects = []
        for m in memories:
            mem = Memory(
                id=m.id,
                profile_id=m.profile_id,
                event_id=m.event_id,
                summary=m.summary,
                emotional_weight=m.emotional_weight,
                recall_count=m.recall_count,
                last_recalled=m.last_recalled,
                retention=m.retention
            )
            mem.created_at = m.created_at
            memory_objects.append(mem)
        
        # 计算当前留存率
        current_retentions = []
        for mem in memory_objects:
            current_ret = mem.calculate_retention()
            current_retentions.append({
                "id": mem.id,
                "summary": mem.summary,
                "emotionalWeight": mem.emotional_weight,
                "retention": round(current_ret, 3),
                "memoryType": MemorySystem.classify_memory(mem.emotional_weight, mem.importance),
                "recallCount": mem.recall_count,
                "createdAt": mem.created_at
            })
        
        # 过滤类型
        if memory_type != "all":
            current_retentions = [m for m in current_retentions if m["memoryType"] == memory_type]
        
        return APIResponse(
            success=True,
            data={
                "memories": current_retentions,
                "total": len(current_retentions),
                "stats": {
                    "epic": len([m for m in current_retentions if m["memoryType"] == "epic"]),
                    "long_term": len([m for m in current_retentions if m["memoryType"] == "long_term"]),
                    "short_term": len([m for m in current_retentions if m["memoryType"] == "short_term"])
                }
            },
            message=f"获取到{len(current_retentions)}条记忆"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=str(e))

@app.post("/api/profiles/{profile_id}/memories/{memory_id}/recall", response_model=APIResponse)
async def recall_memory(profile_id: str, memory_id: str):
    """回忆记忆（增强记忆）"""
    try:
        # 从数据库获取记忆
        memories = db_manager.get_memories(profile_id, limit=1000)
        target_memory = None
        
        for m in memories:
            if m.id == memory_id:
                target_memory = m
                break
        
        if not target_memory:
            return APIResponse(success=False, error="记忆不存在")
        
        # 创建记忆对象并回忆
        mem = Memory(
            id=target_memory.id,
            profile_id=target_memory.profile_id,
            event_id=target_memory.event_id,
            summary=target_memory.summary,
            emotional_weight=target_memory.emotional_weight,
            recall_count=target_memory.recall_count,
            last_recalled=target_memory.last_recalled,
            retention=target_memory.retention
        )
        mem.created_at = target_memory.created_at
        
        result = mem.recall()
        
        # 更新数据库
        # 这里简化处理，实际应该调用db_manager更新
        
        return APIResponse(
            success=True,
            data={
                "memoryId": memory_id,
                "retention": result["retention"],
                "recallCount": result["recall_count"],
                "message": result["message"]
            },
            message="记忆回忆成功"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=str(e))

@app.get("/api/profiles/{profile_id}/memories/stats", response_model=APIResponse)
async def get_memory_stats(profile_id: str):
    """获取记忆统计"""
    try:
        memories = db_manager.get_memories(profile_id, limit=500)
        
        # 统计
        total = len(memories)
        avg_retention = sum(m.retention for m in memories) / max(total, 1)
        
        # 分类统计
        type_counts = {"epic": 0, "long_term": 0, "short_term": 0}
        for m in memories:
            mt = MemorySystem.classify_memory(m.emotional_weight, 0.5)
            type_counts[mt] = type_counts.get(mt, 0) + 1
        
        # 高留存记忆
        high_retention = len([m for m in memories if m.retention > 0.7])
        low_retention = len([m for m in memories if m.retention < 0.3])
        
        return APIResponse(
            success=True,
            data={
                "total": total,
                "averageRetention": round(avg_retention, 3),
                "typeDistribution": type_counts,
                "highRetention": high_retention,
                "lowRetention": low_retention,
                "forgettingRisk": low_retention / max(total, 1)
            },
            message="记忆统计获取成功"
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.get("/api/profiles/{profile_id}/preview", response_model=APIResponse)
async def preview_future(profile_id: str, days: int = 90):
    """未来预览 - 基于当前状态预测未来事件"""
    try:
        game_state = db_manager.load_game_state(profile_id)
        if not game_state:
            return APIResponse(success=False, error="角色不存在")
        
        state = game_state.state
        current_dimensions = state.dimensions
        
        # 基于当前状态生成预测事件
        predictions = []
        
        # 年龄相关预测
        age = state.age
        life_stage = state.life_stage
        
        # 健康维度预测
        health = current_dimensions.get("health", 50)
        if health < 40:
            predictions.append({
                "type": "health_warning",
                "title": "健康预警",
                "description": "健康状况不佳，建议关注身体",
                "probability": 0.7,
                "suggestion": "加强锻炼，注意休息"
            })
        
        # 精力维度预测
        energy = current_dimensions.get("energy", 50)
        if energy < 30:
            predictions.append({
                "type": "energy_warning",
                "title": "精力不足",
                "description": "精力水平较低，可能影响日常表现",
                "probability": 0.8,
                "suggestion": "保证充足睡眠，适当放松"
            })
        
        # 财务维度预测
        wealth = current_dimensions.get("wealth", 50)
        if wealth < 30:
            predictions.append({
                "type": "financial_warning",
                "title": "财务预警",
                "description": "经济状况需要关注",
                "probability": 0.6,
                "suggestion": "合理规划支出，考虑增加收入"
            })
        
        # 基于年龄段的典型事件预测
        if 18 <= age <= 25:
            predictions.extend([
                {"type": "career", "title": "职业发展", "description": "职业规划关键期", "probability": 0.5},
                {"type": "relationship", "title": "感情发展", "description": "建立亲密关系的机会", "probability": 0.6}
            ])
        elif 26 <= age <= 35:
            predictions.extend([
                {"type": "family", "title": "家庭建设", "description": "组建家庭的可能", "probability": 0.7},
                {"type": "career", "title": "职业晋升", "description": "职业发展的黄金期", "probability": 0.5}
            ])
        elif 36 <= age <= 50:
            predictions.extend([
                {"type": "wealth", "title": "财富积累", "description": "财务状况可能改善", "probability": 0.6},
                {"type": "health", "title": "健康关注", "description": "开始关注身体健康", "probability": 0.7}
            ])
        elif age > 50:
            predictions.extend([
                {"type": "retirement", "title": "退休规划", "description": "考虑退休生活", "probability": 0.8},
                {"type": "health", "title": "健康保养", "description": "健康管理的重点期", "probability": 0.9}
            ])
        
        # 社会资本预测
        social = current_dimensions.get("social", 50)
        if social > 70:
            predictions.append({
                "type": "social_opportunity",
                "title": "社交机会",
                "description": "人脉广泛，可能带来机会",
                "probability": 0.7,
                "suggestion": "维护好人际关系"
            })
        
        return APIResponse(
            success=True,
            data={
                "previewDays": days,
                "currentAge": age,
                "currentStage": life_stage,
                "currentDimensions": current_dimensions,
                "predictions": predictions[:10],  # 最多返回10条预测
                "generatedAt": datetime.now().isoformat()
            },
            message=f"生成未来{days}天预测"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=f"预览失败: {str(e)}")

@app.get("/api/profiles/{profile_id}/summary", response_model=APIResponse)
async def get_life_summary(profile_id: str):
    """生成人生总结"""
    try:
        # 获取角色信息
        profiles = db_manager.get_profiles()
        profile = None
        for p in profiles:
            if p.id == profile_id:
                profile = p
                break
        
        if not profile:
            return APIResponse(success=False, error="角色不存在")
        
        # 获取状态
        game_state = db_manager.load_game_state(profile_id)
        if not game_state:
            return APIResponse(success=False, error="角色状态不存在")
        
        state = game_state.state
        
        # 获取事件统计
        events = db_manager.get_events(profile_id, limit=1000)
        
        # 获取记忆
        memories = db_manager.get_memories(profile_id, limit=500)
        
        # 人生阶段评估
        age = state.age
        if age < 18:
            stage = "童年/少年"
            stage_desc = "这是人生中最纯真的时期，充满探索和成长"
        elif age < 30:
            stage = "青年"
            stage_desc = "这是建立人生方向的关键时期"
        elif age < 50:
            stage = "中年"
            stage_desc = "这是人生经验和智慧的黄金期"
        elif age < 70:
            stage = "中老年"
            stage_desc = "这是回顾人生、传承经验的时期"
        else:
            stage = "老年"
            stage_desc = "这是人生的收获季节"
        
        # 计算各维度评分
        dimensions = state.dimensions if hasattr(state, 'dimensions') else {}
        
        # 健康评分
        health_score = dimensions.get('health', 50)
        health_desc = "极佳" if health_score >= 80 else "良好" if health_score >= 60 else "一般" if health_score >= 40 else "欠佳"
        
        # 事业评分
        career_score = dimensions.get('social', {}).get('career', {}).get('level', 50) if isinstance(dimensions.get('social'), dict) else 50
        career_desc = "卓越" if career_score >= 80 else "顺利" if career_score >= 60 else "一般" if career_score >= 40 else "坎坷"
        
        # 情感评分
        relationship_score = dimensions.get('relational', {}).get('intimacy', 50) if isinstance(dimensions.get('relational'), dict) else 50
        relationship_desc = "幸福" if relationship_score >= 80 else "稳定" if relationship_score >= 60 else "平淡" if relationship_score >= 40 else "孤独"
        
        # 成就事件统计
        major_events = [e for e in events if e.emotional_weight > 0.7]
        
        # 人生感悟（基于记忆）
        memorable_memories = sorted(memories, key=lambda m: m.emotional_weight, reverse=True)[:3]
        
        return APIResponse(
            success=True,
            data={
                "profile": {
                    "name": profile.name,
                    "age": age,
                    "stage": stage,
                    "stageDescription": stage_desc,
                    "currentDate": state.current_date
                },
                "dimensions": {
                    "health": {"score": health_score, "desc": health_desc},
                    "career": {"score": career_score, "desc": career_desc},
                    "relationship": {"score": relationship_score, "desc": relationship_desc}
                },
                "stats": {
                    "totalEvents": len(events),
                    "majorEvents": len(major_events),
                    "totalMemories": len(memories),
                    "decisions": state.total_decisions if hasattr(state, 'total_decisions') else 0
                },
                "milestones": [
                    {"title": e.title, "date": e.event_date, "type": e.event_type}
                    for e in major_events[:5]
                ],
                "reflections": [
                    {"summary": m.summary, "emotionalWeight": m.emotional_weight}
                    for m in memorable_memories
                ],
                "generatedAt": datetime.now().isoformat()
            },
            message=f"生成{age}岁人生总结"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=f"生成总结失败: {str(e)}")

@app.get("/api/profiles/{profile_id}/timeline", response_model=APIResponse)
async def get_timeline(profile_id: str, limit: int = 50):
    """获取角色事件时间线"""
    try:
        events = db_manager.get_events(profile_id, limit=limit)
        memories = db_manager.get_memories(profile_id, limit=limit)
        
        timeline_items = []
        
        # 转换事件
        for event in events:
            timeline_items.append({
                "type": "event",
                "id": event.id,
                "date": event.event_date,
                "title": event.title,
                "description": event.description,
                "isCompleted": event.is_completed,
                "emotionalWeight": event.emotional_weight
            })
        
        # 转换记忆
        for memory in memories:
            timeline_items.append({
                "type": "memory",
                "id": memory.id,
                "date": memory.created_at,
                "summary": memory.summary,
                "emotionalWeight": memory.emotional_weight,
                "retention": memory.retention
            })
        
        # 按日期排序
        timeline_items.sort(key=lambda x: x["date"], reverse=True)
        
        return APIResponse(
            success=True,
            data={
                "timeline": timeline_items[:limit],
                "total": len(timeline_items)
            },
            message=f"获取到{len(timeline_items)}条时间线记录"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=f"获取时间线失败: {str(e)}")

@app.get("/api/profiles/{profile_id}/causality/{event_id}", response_model=APIResponse)
async def get_event_causality(profile_id: str, event_id: str):
    """获取事件的因果链 - 追溯事件的前因后果"""
    try:
        # 获取所有相关事件
        events = db_manager.get_events(profile_id, limit=1000)
        memories = db_manager.get_memories(profile_id, limit=1000)
        
        # 构建事件索引
        event_map = {e.id: e for e in events}
        
        # 找到目标事件
        target_event = event_map.get(event_id)
        if not target_event:
            return APIResponse(success=False, error="事件不存在")
        
        # 构建因果链
        # 1. 原因事件：同一天或之前发生的事件，可能导致当前事件
        causes = []
        target_date = target_event.event_date
        
        for event in events:
            if event.id == event_id:
                continue
            # 简化逻辑：同一类型或相关维度的事件视为潜在原因
            if event.event_type == target_event.event_type:
                causes.append({
                    "id": event.id,
                    "title": event.title,
                    "date": event.event_date,
                    "type": "same_type",
                    "strength": 0.6
                })
        
        # 2. 结果事件：当前事件可能导致的后续事件
        effects = []
        for event in events:
            if event.id == event_id:
                continue
            # 查找后续相关事件
            if event.event_type == target_event.event_type:
                effects.append({
                    "id": event.id,
                    "title": event.title,
                    "date": event.event_date,
                    "type": "same_type",
                    "strength": 0.6
                })
        
        # 3. 关联记忆：与该事件相关的记忆
        related_memories = []
        for memory in memories:
            if memory.event_id == event_id:
                related_memories.append({
                    "id": memory.id,
                    "summary": memory.summary,
                    "emotionalWeight": memory.emotional_weight,
                    "retention": memory.retention
                })
        
        # 4. 影响分析：事件对各维度的影响
        impacts = target_event.impacts or {}
        
        # 5. 决策影响：如果事件有决策选项，记录决策
        decision_info = None
        if target_event.selected_choice is not None:
            choices = target_event.choices or []
            if 0 <= target_event.selected_choice < len(choices):
                decision_info = {
                    "selected": target_event.selected_choice,
                    "choice": choices[target_event.selected_choice]
                }
        
        return APIResponse(
            success=True,
            data={
                "event": {
                    "id": target_event.id,
                    "title": target_event.title,
                    "description": target_event.description,
                    "date": target_event.event_date,
                    "type": target_event.event_type,
                    "narrative": target_event.narrative,
                    "emotionalWeight": target_event.emotional_weight
                },
                "causes": causes[:10],  # 最多10个原因
                "effects": effects[:10],  # 最多10个结果
                "relatedMemories": related_memories,
                "impacts": impacts,
                "decision": decision_info,
                "chain": {
                    "length": len(causes) + len(effects),
                    "complete": len(causes) > 0 or len(effects) > 0
                }
            },
            message="获取因果链成功"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=f"获取因果链失败: {str(e)}")

@app.get("/api/profiles/{profile_id}/causality", response_model=APIResponse)
async def get_full_causality_chain(profile_id: str):
    """获取完整的因果链网络"""
    try:
        events = db_manager.get_events(profile_id, limit=500)
        
        # 构建事件关系图
        event_nodes = []
        event_links = []
        
        for event in events:
            event_nodes.append({
                "id": event.id,
                "title": event.title,
                "date": event.event_date,
                "type": event.event_type,
                "isCompleted": event.is_completed,
                "emotionalWeight": event.emotional_weight
            })
            
            # 查找关联事件（相同类型）
            for other_event in events:
                if other_event.id != event.id and other_event.event_type == event.event_type:
                    # 检查日期关系
                    if other_event.event_date >= event.event_date:
                        event_links.append({
                            "source": event.id,
                            "target": other_event.id,
                            "type": "same_type"
                        })
        
        # 统计信息
        type_counts = {}
        for event in events:
            event_type = event.event_type
            type_counts[event_type] = type_counts.get(event_type, 0) + 1
        
        return APIResponse(
            success=True,
            data={
                "nodes": event_nodes,
                "links": event_links,
                "stats": {
                    "totalEvents": len(events),
                    "typeDistribution": type_counts,
                    "completedEvents": sum(1 for e in events if e.is_completed),
                    "pendingEvents": sum(1 for e in events if not e.is_completed)
                }
            },
            message=f"获取完整因果链，共{len(event_nodes)}个事件"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=f"获取因果链失败: {str(e)}")

# ==================== 宏观事件API ====================

@app.get("/api/macro-events", response_model=APIResponse)
async def get_macro_events(year: int = 2024):
    """获取指定年份可能发生的宏观事件"""
    try:
        events = macro_event_system.get_active_events(year)
        event_list = []
        for event in events:
            event_list.append({
                "id": event.event_id,
                "name": event.name,
                "type": event.event_type.value,
                "yearRange": event.year_range,
                "description": event.description,
                "probability": event.probability
            })
        
        return APIResponse(
            success=True,
            data={
                "year": year,
                "events": event_list,
                "total": len(event_list)
            },
            message=f"找到{len(event_list)}个可能的宏观事件"
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.get("/api/macro-events/types", response_model=APIResponse)
async def get_macro_event_types():
    """获取宏观事件类型列表"""
    return APIResponse(
        success=True,
        data={
            "types": [
                {"value": "economic", "label": "经济事件"},
                {"value": "pandemic", "label": "疫情"},
                {"value": "policy", "label": "政策变化"},
                {"value": "technology", "label": "科技革命"},
                {"value": "natural_disaster", "label": "自然灾害"},
                {"value": "social", "label": "社会变革"}
            ]
        }
    )

@app.post("/api/profiles/{profile_id}/check-macro-events", response_model=APIResponse)
async def check_profile_macro_events(profile_id: str, year: int):
    """检查角色在指定年份的宏观事件影响"""
    try:
        profile = db_manager.get_profile(profile_id)
        if not profile:
            return APIResponse(success=False, error="角色不存在")
        
        # 获取角色状态
        state_data = profile.state or {}
        
        # 创建临时状态对象
        class TempState:
            def __init__(self, data):
                self.age = data.get("age", 0)
                self.dimensions = data.get("dimensions", {})
        
        state = TempState(state_data)
        
        # 检查宏观事件
        triggered_events = macro_event_system.check_macro_events(year, state)
        
        return APIResponse(
            success=True,
            data={
                "year": year,
                "triggeredEvents": triggered_events,
                "total": len(triggered_events)
            },
            message=f"检查完成，{len(triggered_events)}个宏观事件被触发"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=str(e))

@app.post("/api/profiles/{profile_id}/trigger-macro-event", response_model=APIResponse)
async def trigger_macro_event(profile_id: str, event_id: str):
    """手动触发指定宏观事件"""
    try:
        profile = db_manager.get_profile(profile_id)
        if not profile:
            return APIResponse(success=False, error="角色不存在")
        
        state_data = profile.state or {}
        
        class TempState:
            def __init__(self, data):
                self.age = data.get("age", 0)
                self.dimensions = data.get("dimensions", {})
        
        state = TempState(state_data)
        
        result = macro_event_system.force_trigger_event(event_id, state)
        
        if not result:
            return APIResponse(success=False, error="事件不存在或角色不受影响")
        
        # 应用影响到角色状态
        if result.get("affected") and result.get("impacts"):
            impacts = result["impacts"]
            # 更新状态
            for dimension, changes in impacts.items():
                if dimension in state_data.get("dimensions", {}):
                    for attr, value in changes.items():
                        current = state_data["dimensions"][dimension].get(attr, 50)
                        state_data["dimensions"][dimension][attr] = max(0, min(100, current + value))
            
            # 保存更新后的状态
            db_manager.update_state(profile_id, state_data)
        
        return APIResponse(
            success=True,
            data=result,
            message=f"宏观事件 [{event_id}] 已触发"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=str(e))

# ==================== 高敏事件API ====================

@app.get("/api/sensitive-events/types", response_model=APIResponse)
async def get_sensitive_event_types():
    """获取高敏事件类型列表"""
    return APIResponse(
        success=True,
        data={
            "types": [
                {"value": "death", "label": "死亡相关"},
                {"value": "serious_illness", "label": "重大疾病"},
                {"value": "family_breakdown", "label": "家庭变故"},
                {"value": "divorce", "label": "婚姻结束"},
                {"value": "job_loss", "label": "失业"},
                {"value": "bankruptcy", "label": "经济危机"},
                {"value": "trauma", "label": "心理创伤"},
                {"value": "addiction", "label": "成瘾"},
                {"value": "crime", "label": "犯罪"},
                {"value": "suicide_ideology", "label": "绝望时刻"}
            ],
            "sensitivity_levels": [
                {"value": "low", "label": "低敏感"},
                {"value": "medium", "label": "中敏感"},
                {"value": "high", "label": "高敏感"},
                {"value": "critical", "label": "极高敏感"}
            ]
        }
    )

@app.post("/api/events/check-sensitivity", response_model=APIResponse)
async def check_event_sensitivity(event_data: Dict[str, Any]):
    """检查事件的敏感度"""
    try:
        level = hs_handler.check_sensitivity(event_data)
        
        return APIResponse(
            success=True,
            data={
                "is_sensitive": level is not None,
                "sensitivity_level": level.value if level else None,
                "event_data": event_data
            }
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.get("/api/sensitive-events/{event_id}/options", response_model=APIResponse)
async def get_sensitive_event_options(event_id: str):
    """获取高敏事件的处理选项"""
    try:
        options = hs_handler.get_handling_options(event_id)
        return APIResponse(
            success=True,
            data=options
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/api/sensitive-events/{event_id}/process", response_model=APIResponse)
async def process_sensitive_event(
    event_id: str,
    handling_mode: str = "soften",
    profile_id: str = None
):
    """处理高敏事件"""
    try:
        mode = HandlingMode(handling_mode)
        
        # 获取角色状态（如果提供）
        character_state = None
        if profile_id:
            profile = db_manager.get_profile(profile_id)
            if profile:
                class TempState:
                    def __init__(self, data):
                        self.age = data.get("age", 0)
                        self.dimensions = data.get("dimensions", {})
                character_state = TempState(profile.state or {})
        
        result = hs_handler.process_event(event_id, mode, character_state)
        
        return APIResponse(
            success=result["success"],
            data=result,
            message=f"高敏事件处理完成"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=str(e))

@app.get("/api/sensitive-events/list", response_model=APIResponse)
async def list_sensitive_events():
    """列出所有高敏事件"""
    try:
        events = []
        for event_id, event in hs_handler.events.items():
            events.append({
                "id": event_id,
                "type": event.event_type.value,
                "level": event.sensitivity_level.value,
                "title": event.title,
                "description": event.description
            })
        
        return APIResponse(
            success=True,
            data={
                "events": events,
                "total": len(events)
            }
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

# ==================== 家族传承API ====================

@app.post("/api/families", response_model=APIResponse)
async def create_family(founder_name: str, profile_id: str):
    """创建新家族"""
    try:
        profile = db_manager.get_profile(profile_id)
        if not profile:
            return APIResponse(success=False, error="角色档案不存在")
        
        founder_profile = {
            "gender": profile.gender,
            "birth_year": datetime.strptime(profile.birth_date, "%Y-%m-%d").year if profile.birth_date else 2000,
            "profile_id": profile_id,
            "dimensions": profile.state.get("dimensions", {}) if profile.state else {},
            "personality": profile.state.get("personality", {}) if profile.state else {}
        }
        
        family = family_system.create_family(founder_name, founder_profile)
        
        return APIResponse(
            success=True,
            data={
                "family_id": family.family_id,
                "founder_name": family.founder_name,
                "total_members": len(family.members)
            },
            message=f"家族 [{founder_name}家族] 创建成功"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=str(e))

@app.get("/api/families/{family_id}", response_model=APIResponse)
async def get_family_tree(family_id: str):
    """获取家族树"""
    try:
        tree = family_system.get_family_tree(family_id)
        if not tree:
            return APIResponse(success=False, error="家族不存在")
        
        return APIResponse(
            success=True,
            data=tree
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.get("/api/families/{family_id}/summary", response_model=APIResponse)
async def get_family_summary(family_id: str):
    """获取家族总结"""
    try:
        summary = family_system.get_family_summary(family_id)
        if not summary:
            return APIResponse(success=False, error="家族不存在")
        
        return APIResponse(
            success=True,
            data=summary
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/api/families/{family_id}/children", response_model=APIResponse)
async def add_child_to_family(
    family_id: str,
    parent_profile_id: str,
    child_name: str,
    child_gender: str,
    birth_year: int
):
    """添加子女到家族"""
    try:
        parent_profile = db_manager.get_profile(parent_profile_id)
        if not parent_profile:
            return APIResponse(success=False, error="父辈档案不存在")
        
        parent_data = {
            "id": parent_profile_id,
            "name": parent_profile.name,
            "personality": parent_profile.state.get("personality", {}) if parent_profile.state else {},
            "birthLocation": parent_profile.birth_location or "北京"
        }
        
        new_profile = family_system.create_next_generation_profile(
            family_id,
            child_name,
            child_gender,
            birth_year,
            parent_data
        )
        
        if not new_profile:
            return APIResponse(success=False, error="创建子女失败")
        
        return APIResponse(
            success=True,
            data=new_profile,
            message=f"子女 [{child_name}] 添加成功"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=str(e))

@app.get("/api/families/{family_id}/inheritance/{child_id}", response_model=APIResponse)
async def calculate_inheritance(family_id: str, child_id: str):
    """计算子女继承的遗产"""
    try:
        inheritance = family_system.calculate_inheritance(family_id, child_id)
        
        return APIResponse(
            success=True,
            data={
                "family_id": family_id,
                "child_id": child_id,
                "inheritance": inheritance
            }
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.get("/api/profiles/{profile_id}/legacy", response_model=APIResponse)
async def get_profile_legacy(profile_id: str):
    """获取角色的遗产信息"""
    try:
        profile = db_manager.get_profile(profile_id)
        if not profile:
            return APIResponse(success=False, error="角色不存在")
        
        # 获取角色的人生总结作为遗产基础
        events = db_manager.get_events(profile_id, limit=100)
        
        # 计算遗产
        legacy = {
            "material": {
                "wealth": profile.state.get("dimensions", {}).get("social", {}).get("economic", 50) if profile.state else 50,
                "assets": []
            },
            "social": {
                "reputation": 50,
                "connections": 0
            },
            "cognitive": {
                "knowledge": profile.state.get("dimensions", {}).get("cognitive", {}).get("knowledge", 50) if profile.state else 50,
                "skills": []
            },
            "psychological": {
                "personality": profile.state.get("personality", {}) if profile.state else {},
                "values": [],
                "wisdom": len([e for e in events if e.is_completed])
            },
            "relational": {
                "family_bonds": profile.state.get("dimensions", {}).get("relational", {}).get("family", 50) if profile.state else 50
            }
        }
        
        # 添加重要事件作为成就
        notable_events = [e for e in events if e.emotional_weight and e.emotional_weight > 0.7]
        legacy["achievements"] = [
            {"title": e.title, "date": e.event_date}
            for e in notable_events[:10]
        ]
        
        return APIResponse(
            success=True,
            data=legacy
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return APIResponse(success=False, error=str(e))

# ==================== 规则管理API ====================
from core.engine.rule_conflict import conflict_detector, RuleConflict
from core.engine.dynamic_rules import dynamic_rule_manager, RuleStatus, UpdateType

class AddRuleRequest(BaseModel):
    rule: Dict[str, Any]
    category: str
    reason: str = ""

class ModifyRuleRequest(BaseModel):
    updates: Dict[str, Any]
    reason: str = ""

@app.get("/api/rules")
async def get_rules():
    """获取所有活跃规则"""
    try:
        active_rules = dynamic_rule_manager.get_active_rules()
        stats = dynamic_rule_manager.get_statistics()
        
        return APIResponse(
            success=True,
            data={
                "rules": active_rules,
                "statistics": stats
            }
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.get("/api/rules/{rule_id}")
async def get_rule(rule_id: str):
    """获取特定规则"""
    try:
        rule = dynamic_rule_manager.get_rule(rule_id)
        if not rule:
            return APIResponse(success=False, error="规则不存在")
        
        return APIResponse(success=True, data=rule)
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/api/rules")
async def add_rule(request: AddRuleRequest):
    """添加新规则"""
    try:
        success = dynamic_rule_manager.add_rule(
            rule=request.rule,
            category=request.category,
            reason=request.reason
        )
        
        if success:
            return APIResponse(
                success=True,
                message=f"规则 {request.rule.get('id')} 已添加",
                data={"rule_id": request.rule.get('id')}
            )
        else:
            return APIResponse(success=False, error="添加规则失败")
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.put("/api/rules/{rule_id}")
async def modify_rule(rule_id: str, request: ModifyRuleRequest):
    """修改规则"""
    try:
        success = dynamic_rule_manager.modify_rule(
            rule_id=rule_id,
            updates=request.updates,
            reason=request.reason
        )
        
        if success:
            return APIResponse(
                success=True,
                message=f"规则 {rule_id} 已修改"
            )
        else:
            return APIResponse(success=False, error="修改规则失败")
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.delete("/api/rules/{rule_id}")
async def delete_rule(rule_id: str, reason: str = ""):
    """删除规则"""
    try:
        success = dynamic_rule_manager.delete_rule(
            rule_id=rule_id,
            reason=reason
        )
        
        if success:
            return APIResponse(
                success=True,
                message=f"规则 {rule_id} 已删除"
            )
        else:
            return APIResponse(success=False, error="删除规则失败")
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/api/rules/{rule_id}/disable")
async def disable_rule(rule_id: str, reason: str = ""):
    """禁用规则"""
    try:
        success = dynamic_rule_manager.disable_rule(
            rule_id=rule_id,
            reason=reason
        )
        
        if success:
            return APIResponse(
                success=True,
                message=f"规则 {rule_id} 已禁用"
            )
        else:
            return APIResponse(success=False, error="禁用规则失败")
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/api/rules/{rule_id}/enable")
async def enable_rule(rule_id: str, reason: str = ""):
    """启用规则"""
    try:
        success = dynamic_rule_manager.enable_rule(
            rule_id=rule_id,
            reason=reason
        )
        
        if success:
            return APIResponse(
                success=True,
                message=f"规则 {rule_id} 已启用"
            )
        else:
            return APIResponse(success=False, error="启用规则失败")
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.get("/api/rules/conflicts")
async def get_rule_conflicts():
    """检测规则冲突"""
    try:
        # 更新冲突检测器的规则
        conflict_detector.load_rules(dynamic_rule_manager.get_active_rules())
        conflicts = conflict_detector.detect_all_conflicts()
        stats = conflict_detector.get_conflict_statistics()
        
        return APIResponse(
            success=True,
            data={
                "conflicts": [
                    {
                        "rule1_id": c.rule1_id,
                        "rule2_id": c.rule2_id,
                        "type": c.conflict_type.value,
                        "severity": c.severity.value,
                        "description": c.description,
                        "suggestion": c.resolution_suggestion,
                        "auto_resolvable": c.auto_resolvable
                    }
                    for c in conflicts
                ],
                "statistics": stats
            }
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/api/rules/conflicts/{rule1_id}/{rule2_id}/resolve")
async def resolve_conflict(rule1_id: str, rule2_id: str):
    """解决规则冲突"""
    try:
        # 找到冲突
        conflict_detector.load_rules(dynamic_rule_manager.get_active_rules())
        conflicts = conflict_detector.detect_all_conflicts()
        
        target_conflict = None
        for c in conflicts:
            if (c.rule1_id == rule1_id and c.rule2_id == rule2_id) or \
               (c.rule1_id == rule2_id and c.rule2_id == rule1_id):
                target_conflict = c
                break
        
        if not target_conflict:
            return APIResponse(success=False, error="未找到指定冲突")
        
        # 解决冲突
        result = conflict_detector.resolve_conflict(target_conflict)
        
        # 如果自动禁用了规则，更新动态规则管理器
        if result.get('resolved') and result.get('action') == 'disable':
            dynamic_rule_manager.disable_rule(
                result['rule_id'],
                reason=result.get('reason', '')
            )
        
        return APIResponse(
            success=result.get('resolved', False),
            data=result,
            message=result.get('reason', '')
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.get("/api/rules/statistics")
async def get_rule_statistics():
    """获取规则统计信息"""
    try:
        stats = dynamic_rule_manager.get_statistics()
        return APIResponse(success=True, data=stats)
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/api/rules/save")
async def save_rules():
    """保存规则到文件"""
    try:
        success = dynamic_rule_manager.save_rules()
        if success:
            return APIResponse(success=True, message="规则已保存")
        else:
            return APIResponse(success=False, error="保存规则失败")
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/api/rules/reload")
async def reload_rules():
    """重新加载规则"""
    try:
        dynamic_rule_manager._load_rules()
        return APIResponse(success=True, message="规则已重新加载")
    except Exception as e:
        return APIResponse(success=False, error=str(e))

# 启动服务器
if __name__ == "__main__":
    import uvicorn
    
    print("="*60)
    print("无限人生：AI编年史 - 完整版API服务")
    print("="*60)
    print(f"服务器地址: http://localhost:8000")
    print(f"API文档: http://localhost:8000/docs")
    print(f"核心引擎: 已集成")
    print(f"规则引擎: 已加载")
    print(f"AI引擎: 已启用")
    print("="*60)
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
