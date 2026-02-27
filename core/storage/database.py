"""
数据库存储引擎 - 采用事件溯源架构
"""

import sqlite3
import json
import hashlib
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Optional, Any
from pathlib import Path
import zlib
import pickle

from typing import List, Dict, Optional, Any
import json
from datetime import datetime

from shared.types import LifeProfile, CharacterState, GameEvent, Memory

class DatabaseManager:
    """数据库管理器 - 事件溯源架构实现"""
    
    def __init__(self, db_path: str = "life_simulation.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 角色档案表 - 与 TypeScript 类型保持一致
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS life_profile (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                birth_place TEXT NOT NULL,
                gender TEXT NOT NULL,
                family_background TEXT DEFAULT 'middle',
                initial_traits BLOB NOT NULL,
                starting_age REAL DEFAULT 0.0,
                era TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # 事件日志表 - 事件溯源核心
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS event_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id TEXT NOT NULL,
                event_date TEXT NOT NULL,
                event_type TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                narrative TEXT NOT NULL,
                choices BLOB NOT NULL,
                impacts BLOB NOT NULL,
                is_completed INTEGER DEFAULT 0,
                selected_choice INTEGER,
                plausibility INTEGER DEFAULT 60,
                emotional_weight REAL DEFAULT 0.5,
                created_at TEXT NOT NULL,
                FOREIGN KEY (profile_id) REFERENCES life_profile (id)
            )
        """)
        
        # 状态快照表 - 性能优化检查点
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS state_snapshot (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id TEXT NOT NULL,
                snapshot_date TEXT NOT NULL,
                full_state BLOB NOT NULL,
                event_offset INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (profile_id) REFERENCES life_profile (id)
            )
        """)
        
        # 记忆表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id TEXT PRIMARY KEY,
                profile_id TEXT NOT NULL,
                event_id INTEGER NOT NULL,
                summary TEXT NOT NULL,
                emotional_weight REAL DEFAULT 0.5,
                recall_count INTEGER DEFAULT 0,
                last_recalled TEXT,
                retention REAL DEFAULT 1.0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (profile_id) REFERENCES life_profile (id),
                FOREIGN KEY (event_id) REFERENCES event_log (id)
            )
        """)
        
        # 索引优化
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_event_log_profile_date ON event_log(profile_id, event_date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_snapshot_profile_date ON state_snapshot(profile_id, snapshot_date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_profile ON memory(profile_id)")
        
        conn.commit()
        conn.close()
    
    def create_profile(self, profile_data: Dict[str, Any]) -> LifeProfile:
        """创建新角色档案"""
        # 如果提供了 ID 则使用，否则生成
        profile_id = profile_data.get('id')
        if not profile_id:
            profile_id = hashlib.sha256(f"{datetime.now().isoformat()}{profile_data['name']}".encode()).hexdigest()[:16]
        
        now = datetime.now().isoformat()
        
        profile = LifeProfile(
            id=profile_id,
            name=profile_data['name'],
            birthDate=profile_data['birthDate'] if 'birthDate' in profile_data else profile_data.get('birth_date'),
            birthLocation=profile_data['birthLocation'] if 'birthLocation' in profile_data else profile_data.get('birth_place'),
            gender=profile_data['gender'],
            familyBackground=profile_data.get('familyBackground', profile_data.get('family_background', 'middle')),
            initialPersonality=profile_data.get('initialPersonality', profile_data.get('initial_traits', {})),
            createdAt=profile_data.get('createdAt', now),
            startingAge=profile_data.get('startingAge', profile_data.get('starting_age', 0.0))
        )


        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO life_profile 
            (id, name, birth_date, birth_place, gender, family_background, initial_traits, 
             starting_age, era, difficulty, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            profile.id, profile.name, profile.birthDate, profile.birthLocation,
            profile.gender, profile.familyBackground, json.dumps(profile.initialPersonality),
            profile.startingAge, profile_data.get('era', '21世纪'),
            profile_data.get('difficulty', 'normal'), profile.createdAt, profile.createdAt
        ))
        
        conn.commit()
        conn.close()
        
        return profile
    
    def get_profiles(self) -> List[LifeProfile]:
        """获取所有角色档案"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM life_profile ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
        profiles: List[LifeProfile] = []
        for row in rows:
            # 新表结构: id, name, birth_date, birth_place, gender, family_background, 
            # initial_traits, starting_age, era, difficulty, created_at, updated_at
            profile = LifeProfile(
                id=row[0], 
                name=row[1], 
                birthDate=row[2], 
                birthLocation=row[3],
                gender=row[4], 
                familyBackground=row[5] if len(row) > 5 else 'middle',
                initialPersonality=json.loads(row[6]) if len(row) > 6 else {}, 
                createdAt=row[10] if len(row) > 10 else row[8],
                startingAge=row[7] if len(row) > 7 else 0.0
            )
            profiles.append(profile)

        
        conn.close()
        return profiles
    
    def get_profile(self, profile_id: str) -> Optional[LifeProfile]:
        """获取单个角色档案"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM life_profile WHERE id = ?", (profile_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # 新表结构: id, name, birth_date, birth_place, gender, family_background, 
            # initial_traits, starting_age, era, difficulty, created_at, updated_at
            return LifeProfile(
                id=row[0], 
                name=row[1], 
                birthDate=row[2], 
                birthLocation=row[3],
                gender=row[4], 
                familyBackground=row[5] if len(row) > 5 else 'middle',
                initialPersonality=json.loads(row[6]) if len(row) > 6 else {}, 
                createdAt=row[10] if len(row) > 10 else row[8],
                startingAge=row[7] if len(row) > 7 else 0.0
            )
        return None

    
    def save_event(self, profile_id: str, event: GameEvent) -> int:
        """保存事件到日志"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO event_log 
            (profile_id, event_date, event_type, title, description, narrative, 
             choices, impacts, is_completed, selected_choice, plausibility, 
             emotional_weight, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            profile_id, event.eventDate, event.eventType, event.title,
            event.description, event.narrative, json.dumps(event.choices),
            json.dumps(event.impacts), event.isCompleted, event.selectedChoice,
            event.plausibility, event.emotionalWeight, event.createdAt
        ))
        
        event_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return event_id
    
    def save_snapshot(self, profile_id: str, snapshot_date: str, state: CharacterState, event_offset: int):
        """保存状态快照"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 压缩存储
        compressed_state = zlib.compress(pickle.dumps(state))
        
        cursor.execute("""
            INSERT INTO state_snapshot 
            (profile_id, snapshot_date, full_state, event_offset, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (profile_id, snapshot_date, compressed_state, event_offset, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_latest_snapshot(self, profile_id: str) -> Optional[tuple]:
        """获取最新快照"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT full_state, event_offset, snapshot_date 
            FROM state_snapshot 
            WHERE profile_id = ? 
            ORDER BY snapshot_date DESC 
            LIMIT 1
        """, (profile_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            state = pickle.loads(zlib.decompress(row[0]))
            return state, row[1], row[2]
        
        return None
    
    def get_events_after_offset(self, profile_id: str, offset: int, target_date: str) -> List[GameEvent]:
        """获取指定偏移量之后的事件"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM event_log 
            WHERE profile_id = ? AND id > ? AND event_date <= ?
            ORDER BY event_date, id
        """, (profile_id, offset, target_date))
        
        rows = cursor.fetchall()
        events = []
        
        for row in rows:
            event = GameEvent(
                id=row[0], profileId=row[1], eventDate=row[2], eventType=row[3],
                title=row[4], description=row[5], narrative=row[6],
                choices=json.loads(row[7]), impacts=json.loads(row[8]),
                isCompleted=bool(row[9]), selectedChoice=row[10],
                plausibility=row[11], emotionalWeight=row[12],
                createdAt=row[13], updatedAt=row[13]
            )
            events.append(event)
        
        conn.close()
        return events

    def get_events(self, profile_id: str, limit: int = 100) -> List[GameEvent]:
        """获取角色的事件列表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM event_log 
            WHERE profile_id = ? 
            ORDER BY event_date DESC, id DESC
            LIMIT ?
        """, (profile_id, limit))
        
        rows = cursor.fetchall()
        events = []
        
        for row in rows:
            event = GameEvent(
                id=row[0], profileId=row[1], eventDate=row[2], eventType=row[3],
                title=row[4], description=row[5], narrative=row[6],
                choices=json.loads(row[7]), impacts=json.loads(row[8]),
                isCompleted=bool(row[9]), selectedChoice=row[10],
                plausibility=row[11], emotionalWeight=row[12],
                createdAt=row[13], updatedAt=row[13]
            )
            events.append(event)
        
        conn.close()
        return events

    
    def save_memory(self, profile_id: str, memory: Memory):
        """保存记忆"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO memory 
            (id, profile_id, event_id, summary, emotional_weight, 
             recall_count, last_recalled, retention, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            memory.id, profile_id, memory.eventId, memory.summary,
            memory.emotionalWeight, memory.recallCount, memory.lastRecalled,
            memory.retention, memory.createdAt, memory.updatedAt
        ))

        
        conn.commit()
        conn.close()
    
    def get_memories(self, profile_id: str, min_retention: float = 0.3, limit: int = 500) -> List[Memory]:
        """获取保留度高于阈值的记忆"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM memory 
            WHERE profile_id = ? AND retention >= ?
            ORDER BY emotional_weight DESC, last_recalled DESC
            LIMIT ?
        """, (profile_id, min_retention, limit))
        
        rows = cursor.fetchall()
        memories = []

        
        for row in rows:
            memory = Memory(
                id=row[0], profileId=row[1], eventId=row[2], summary=row[3],
                emotionalWeight=row[4], recallCount=row[5], lastRecalled=row[6],
                retention=row[7], createdAt=row[8], updatedAt=row[9]
            )
            memories.append(memory)
        
        conn.close()
        return memories
    
    def check_existing_data(self) -> bool:
        """检查是否存在数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM life_profile")
        count = cursor.fetchone()[0]
        
        conn.close()
        return count > 0

# 全局数据库实例
db_manager = DatabaseManager()