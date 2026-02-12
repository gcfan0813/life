"""
数据库存储引擎 - 采用事件溯源架构
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path
import zlib
import pickle

from ..shared.types import (
    LifeProfile, CharacterState, GameEvent, Memory, 
    FiveDimensions, Relationship, CareerInfo, 
    EducationInfo, FinancialInfo, HealthInfo
)

class DatabaseManager:
    """数据库管理器 - 事件溯源架构实现"""
    
    def __init__(self, db_path: str = "life_simulation.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 角色档案表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS life_profile (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                birth_place TEXT NOT NULL,
                gender TEXT NOT NULL,
                initial_traits BLOB NOT NULL,
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
        profile_id = hashlib.sha256(f"{datetime.now().isoformat()}{profile_data['name']}".encode()).hexdigest()[:16]
        now = datetime.now().isoformat()
        
        profile = LifeProfile(
            id=profile_id,
            name=profile_data['name'],
            birth_date=profile_data['birth_date'],
            birth_place=profile_data['birth_place'],
            gender=profile_data['gender'],
            initial_traits=profile_data['initial_traits'],
            era=profile_data['era'],
            difficulty=profile_data['difficulty'],
            created_at=now,
            updated_at=now
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO life_profile 
            (id, name, birth_date, birth_place, gender, initial_traits, era, difficulty, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            profile.id, profile.name, profile.birth_date, profile.birth_place,
            profile.gender, pickle.dumps(profile.initial_traits), profile.era,
            profile.difficulty, profile.created_at, profile.updated_at
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
        
        profiles = []
        for row in rows:
            profile = LifeProfile(
                id=row[0], name=row[1], birth_date=row[2], birth_place=row[3],
                gender=row[4], initial_traits=pickle.loads(row[5]), era=row[6],
                difficulty=row[7], created_at=row[8], updated_at=row[9]
            )
            profiles.append(profile)
        
        conn.close()
        return profiles
    
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
            profile_id, event.event_date, event.event_type, event.title,
            event.description, event.narrative, pickle.dumps(event.choices),
            pickle.dumps(event.impacts), event.is_completed, event.selected_choice,
            event.plausibility, event.emotional_weight, event.created_at
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
                id=row[0], profile_id=row[1], event_date=row[2], event_type=row[3],
                title=row[4], description=row[5], narrative=row[6],
                choices=pickle.loads(row[7]), impacts=pickle.loads(row[8]),
                is_completed=bool(row[9]), selected_choice=row[10],
                plausibility=row[11], emotional_weight=row[12],
                created_at=row[13], updated_at=row[13]
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
            memory.id, profile_id, memory.event_id, memory.summary,
            memory.emotional_weight, memory.recall_count, memory.last_recalled,
            memory.retention, memory.created_at, memory.updated_at
        ))
        
        conn.commit()
        conn.close()
    
    def get_memories(self, profile_id: str, min_retention: float = 0.3) -> List[Memory]:
        """获取保留度高于阈值的记忆"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM memory 
            WHERE profile_id = ? AND retention >= ?
            ORDER BY emotional_weight DESC, last_recalled DESC
        """, (profile_id, min_retention))
        
        rows = cursor.fetchall()
        memories = []
        
        for row in rows:
            memory = Memory(
                id=row[0], profile_id=row[1], event_id=row[2], summary=row[3],
                emotional_weight=row[4], recall_count=row[5], last_recalled=row[6],
                retention=row[7], created_at=row[8], updated_at=row[9]
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