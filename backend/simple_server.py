#!/usr/bin/env python3
"""
简化版后端API服务 - 用于前端功能测试和降级方案

⚠️ 重要说明：此文件是临时解决方案，绕过了核心引擎。
完整功能需要使用完整后端（集成core/引擎模块）。

功能限制：
- 无500+学术验证规则
- 无AI推演引擎
- 无规则约束机制
- 事件质量低下
- 仅适合演示和测试
"""

import json
import sqlite3
import os
from datetime import datetime
from typing import Dict, Any, List

# 简化版FastAPI服务
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="无限人生简化API")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库配置
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "life_simulation.db")

# API模型
class CreateProfileRequest(BaseModel):
    name: str
    gender: str
    birthDate: str
    birthLocation: str
    familyBackground: str
    initialPersonality: Dict[str, float]

class APIResponse(BaseModel):
    success: bool
    data: Any = None
    error: str = None
    message: str = None

# 工具函数
def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建角色档案表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            birthDate TEXT NOT NULL,
            birthLocation TEXT,
            familyBackground TEXT,
            initialPersonality TEXT,
            createdAt TEXT
        )
    """)
    
    # 创建事件日志表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            profileId TEXT,
            title TEXT,
            description TEXT,
            choices TEXT,
            isCompleted BOOLEAN DEFAULT 0,
            createdAt TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# API路由
@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/profiles", response_model=APIResponse)
async def create_profile(request: CreateProfileRequest):
    """创建角色档案"""
    try:
        profile_id = f"profile_{datetime.now().timestamp()}"
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO profiles (id, name, gender, birthDate, birthLocation, 
                                familyBackground, initialPersonality, createdAt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            profile_id,
            request.name,
            request.gender,
            request.birthDate,
            request.birthLocation,
            request.familyBackground,
            json.dumps(request.initialPersonality),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return APIResponse(
            success=True,
            data={
                "id": profile_id,
                "name": request.name,
                "gender": request.gender,
                "birthDate": request.birthDate,
                "birthLocation": request.birthLocation,
                "familyBackground": request.familyBackground,
                "initialPersonality": request.initialPersonality,
                "createdAt": datetime.now().isoformat()
            },
            message="角色创建成功"
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.get("/api/profiles", response_model=APIResponse)
async def get_profiles():
    """获取所有角色档案"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM profiles ORDER BY createdAt DESC")
        rows = cursor.fetchall()
        conn.close()
        
        profiles = []
        for row in rows:
            profiles.append({
                "id": row[0],
                "name": row[1],
                "gender": row[2],
                "birthDate": row[3],
                "birthLocation": row[4],
                "familyBackground": row[5],
                "initialPersonality": json.loads(row[6]),
                "createdAt": row[7]
            })
        
        return APIResponse(success=True, data=profiles)
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/api/advance", response_model=APIResponse)
async def advance_time(profile_id: str, days: int = 30):
    """推进时间并生成事件"""
    try:
        # 模拟AI生成事件
        events = [
            {
                "id": f"event_{datetime.now().timestamp()}",
                "profileId": profile_id,
                "title": "工作机会",
                "description": "你收到了一份新的工作邀请",
                "choices": [
                    {"text": "接受工作", "impact": "+10社会"},
                    {"text": "继续寻找", "impact": "+5认知"}
                ],
                "isCompleted": False,
                "createdAt": datetime.now().isoformat()
            }
        ]
        
        # 保存事件
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        for event in events:
            cursor.execute("""
                INSERT INTO events (id, profileId, title, description, choices, createdAt)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                event["id"],
                event["profileId"],
                event["title"],
                event["description"],
                json.dumps(event["choices"]),
                event["createdAt"]
            ))
        
        conn.commit()
        conn.close()
        
        return APIResponse(
            success=True,
            data={
                "events": events,
                "newDate": datetime.now().isoformat().split("T")[0],
                "message": f"成功推进{days}天"
            }
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.get("/api/events/{profile_id}")
async def get_events(profile_id: str):
    """获取角色事件"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, description, choices, isCompleted 
            FROM events 
            WHERE profileId = ? 
            ORDER BY createdAt DESC
        """, (profile_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        events = []
        for row in rows:
            events.append({
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "choices": json.loads(row[3]),
                "isCompleted": bool(row[4])
            })
        
        return APIResponse(success=True, data=events)
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/api/profiles/{profile_id}/advance")
async def advance_time(profile_id: str, request: Dict[str, Any]):
    """推进时间"""
    try:
        days = request.get("days", 30)
        
        # 生成模拟事件
        event_templates = [
            {
                "title": "工作机会",
                "description": "你收到了一份新的工作邀请，薪资和职位都很有吸引力",
                "choices": [
                    {"text": "接受新工作", "impact": {"social.career.level": 1, "social.economic": 5000}},
                    {"text": "继续留在现公司", "impact": {"social.socialCapital": 10}},
                    {"text": "自己创业", "impact": {"social.economic": -10000, "psychological.openness": 5}}
                ]
            },
            {
                "title": "健康检查",
                "description": "你决定进行一次全面的健康检查",
                "choices": [
                    {"text": "坚持运动锻炼", "impact": {"physical.health": 10, "physical.energy": 5}},
                    {"text": "调整饮食结构", "impact": {"physical.health": 8, "physical.appearance": 3}},
                    {"text": "忽视健康问题", "impact": {"physical.health": -5}}
                ]
            },
            {
                "title": "社交活动",
                "description": "朋友邀请你参加一个社交聚会",
                "choices": [
                    {"text": "积极参加", "impact": {"social.socialCapital": 15, "psychological.extraversion": 3}},
                    {"text": "婉言谢绝", "impact": {"psychological.neuroticism": -3}},
                    {"text": "只参加熟悉的朋友聚会", "impact": {"relational.intimacy": 5}}
                ]
            }
        ]
        
        # 随机选择事件模板
        import random
        template = random.choice(event_templates)
        
        event = {
            "id": f"event_{datetime.now().timestamp()}",
            "profileId": profile_id,
            "title": template["title"],
            "description": template["description"],
            "choices": template["choices"],
            "isCompleted": False,
            "createdAt": datetime.now().isoformat()
        }
        
        # 保存事件
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO events (id, profileId, title, description, choices, createdAt)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            event["id"],
            event["profileId"],
            event["title"],
            event["description"],
            json.dumps(event["choices"]),
            event["createdAt"]
        ))
        
        conn.commit()
        conn.close()
        
        return APIResponse(
            success=True,
            data={
                "events": [event],
                "newDate": datetime.now().isoformat().split("T")[0],
                "message": f"成功推进{days}天，生成新事件"
            }
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/api/profiles/{profile_id}/decisions")
async def make_decision(profile_id: str, request: Dict[str, Any]):
    """处理决策"""
    try:
        event_id = request.get("eventId")
        choice_index = request.get("choiceIndex", 0)
        
        # 获取事件
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, description, choices 
            FROM events 
            WHERE profileId = ? AND id = ?
        """, (profile_id, event_id))
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            return APIResponse(success=False, error="事件不存在")
        
        event = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "choices": json.loads(row[3])
        }
        
        # 检查选择索引
        if choice_index >= len(event["choices"]):
            conn.close()
            return APIResponse(success=False, error="无效的选择")
        
        # 标记事件为已完成
        cursor.execute("""
            UPDATE events 
            SET isCompleted = 1 
            WHERE id = ?
        """, (event_id,))
        
        conn.commit()
        conn.close()
        
        return APIResponse(
            success=True,
            data={
                "newState": {},  # 简化处理
                "newMemories": [],
                "immediateEffects": [],
                "longTermEffects": [],
                "message": "决策已记录"
            }
        )
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.get("/api/data/exists")
async def check_data():
    """检查是否有数据"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM profiles")
        count = cursor.fetchone()[0]
        conn.close()
        
        return APIResponse(success=True, data={"hasData": count > 0})
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.get("/api/health")
async def health():
    """健康检查"""
    return APIResponse(
        success=True,
        data={"status": "healthy", "version": "1.0.0", "timestamp": datetime.now().isoformat()}
    )

# 初始化数据库
init_db()

if __name__ == "__main__":
    import uvicorn
    print("启动简化版无限人生API服务器...")
    print("服务器地址: http://localhost:8001")
    print("API文档: http://localhost:8001/docs")
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
