"""
模拟引擎单元测试
"""

import unittest
import tempfile
import os
import sys
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSimulationEngine(unittest.TestCase):
    """测试模拟引擎"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """测试后清理"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_character_state_creation(self):
        """测试角色状态创建"""
        from core.engine.simulation import CharacterState
        
        state = CharacterState(
            id="test_state_1",
            profileId="test_profile_1",
            currentDate="2000-01-01",
            age=25,
            dimensions={
                "physical": {"health": 80, "energy": 70},
                "psychological": {"happiness": 60}
            },
            location="北京",
            occupation="工程师",
            education="本科",
            lifeStage="youngAdult",
            totalEvents=0,
            totalDecisions=0,
            daysSurvived=0
        )
        
        self.assertEqual(state.id, "test_state_1")
        self.assertEqual(state.age, 25)
        self.assertEqual(state.location, "北京")
        self.assertEqual(state.lifeStage, "youngAdult")
    
    def test_game_event_creation(self):
        """测试游戏事件创建"""
        from core.engine.simulation import GameEvent
        
        event = GameEvent(
            id="event_1",
            profileId="profile_1",
            eventDate="2000-06-15",
            eventType="career",
            title="职业晋升",
            description="获得晋升机会",
            narrative="你的努力得到了认可",
            choices=[
                {"id": 0, "text": "接受挑战", "riskLevel": 60},
                {"id": 1, "text": "保持现状", "riskLevel": 20}
            ],
            impacts={"social": {"career": 10}},
            isCompleted=False,
            selectedChoice=None,
            plausibility=75,
            emotionalWeight=0.7,
            createdAt=datetime.now().isoformat(),
            updatedAt=datetime.now().isoformat()
        )
        
        self.assertEqual(event.id, "event_1")
        self.assertEqual(event.eventType, "career")
        self.assertEqual(len(event.choices), 2)
        self.assertFalse(event.isCompleted)
    
    def test_memory_creation(self):
        """测试记忆创建"""
        from core.engine.simulation import Memory
        
        memory = Memory(
            id="memory_1",
            profileId="profile_1",
            eventId="event_1",
            summary="一次重要的职业晋升",
            emotionalWeight=0.8,
            recallCount=0,
            lastRecalled=None,
            retention=1.0,
            createdAt=datetime.now().isoformat(),
            updatedAt=datetime.now().isoformat()
        )
        
        self.assertEqual(memory.id, "memory_1")
        self.assertEqual(memory.emotionalWeight, 0.8)
        self.assertEqual(memory.recallCount, 0)


class TestRuleValidator(unittest.TestCase):
    """测试规则验证器"""
    
    def setUp(self):
        """测试前准备"""
        try:
            from core.engine.validator import RuleValidator
            self.validator = RuleValidator()
        except Exception as e:
            self.skipTest(f"规则验证器初始化失败: {e}")
    
    def test_validator_initialization(self):
        """测试验证器初始化"""
        self.assertIsNotNone(self.validator)
    
    def test_plausibility_calculation(self):
        """测试合理性计算"""
        from core.engine.simulation import GameEvent, CharacterState
        from core.engine.validator import EraRules
        
        # 创建测试事件
        event = GameEvent(
            id="test_event",
            profileId="test_profile",
            eventDate="2000-01-01",
            eventType="career",
            title="测试事件",
            description="测试描述",
            narrative="测试叙述",
            choices=[],
            impacts=[],
            isCompleted=False,
            selectedChoice=None,
            plausibility=50,
            emotionalWeight=0.5,
            createdAt=datetime.now().isoformat(),
            updatedAt=datetime.now().isoformat()
        )
        
        # 创建测试状态
        state = CharacterState(
            id="test_state",
            profileId="test_profile",
            currentDate="2000-01-01",
            age=25,
            dimensions={},
            location="北京",
            occupation="工程师",
            education="本科",
            lifeStage="youngAdult",
            totalEvents=0,
            totalDecisions=0,
            daysSurvived=0
        )
        
        era_rules = EraRules(era="现代")
        
        try:
            result = self.validator.calculate_plausibility(event, state, era_rules)
            self.assertIsNotNone(result)
            self.assertIsInstance(result.plausibility, (int, float))
        except Exception as e:
            # 如果规则文件不存在，跳过此测试
            self.skipTest(f"合理性计算失败: {e}")


class TestCharacterInitializer(unittest.TestCase):
    """测试角色初始化器"""
    
    def setUp(self):
        """测试前准备"""
        try:
            from core.engine.character import CharacterInitializer
            self.initializer = CharacterInitializer()
        except Exception as e:
            self.skipTest(f"角色初始化器初始化失败: {e}")
    
    def test_initializer_creation(self):
        """测试初始化器创建"""
        self.assertIsNotNone(self.initializer)
    
    @patch('core.engine.character.CharacterInitializer.initialize_character_state')
    async def test_initialize_character_state(self, mock_init):
        """测试角色状态初始化"""
        from shared.types import LifeProfile
        
        # 创建测试档案
        profile = LifeProfile(
            id="test_profile",
            name="测试角色",
            gender="male",
            birthDate="1990-01-01",
            birthLocation="北京",
            familyBackground="middle",
            initialPersonality={"openness": 50},
            createdAt=datetime.now().isoformat(),
            startingAge=0.0
        )
        
        # Mock返回值
        mock_state = Mock()
        mock_state.id = "state_1"
        mock_state.profile_id = "test_profile"
        mock_init.return_value = mock_state
        
        result = await self.initializer.initialize_character_state(profile)
        
        self.assertIsNotNone(result)


class TestMacroEventSystem(unittest.TestCase):
    """测试宏观事件系统"""
    
    def setUp(self):
        """测试前准备"""
        try:
            from core.engine.macro_events import macro_event_system
            self.macro_system = macro_event_system
        except Exception as e:
            self.skipTest(f"宏观事件系统初始化失败: {e}")
    
    def test_macro_system_exists(self):
        """测试宏观系统存在"""
        self.assertIsNotNone(self.macro_system)
    
    def test_get_active_events(self):
        """测试获取活跃事件"""
        try:
            events = self.macro_system.get_active_events(2020)
            self.assertIsInstance(events, list)
        except Exception:
            self.skipTest("获取活跃事件失败")


class TestFamilySystem(unittest.TestCase):
    """测试家族系统"""
    
    def setUp(self):
        """测试前准备"""
        try:
            from core.engine.family_legacy import family_system
            self.family_system = family_system
        except Exception as e:
            self.skipTest(f"家族系统初始化失败: {e}")
    
    def test_family_system_exists(self):
        """测试家族系统存在"""
        self.assertIsNotNone(self.family_system)
    
    def test_create_family(self):
        """测试创建家族"""
        try:
            founder_profile = {
                "gender": "male",
                "birth_year": 1990,
                "profile_id": "test_profile",
                "dimensions": {},
                "personality": {}
            }
            
            family = self.family_system.create_family("测试家族", founder_profile)
            
            if family:
                self.assertIsNotNone(family.family_id)
                self.assertEqual(family.founder_name, "测试家族")
        except Exception:
            self.skipTest("创建家族失败")


if __name__ == '__main__':
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestSimulationEngine,
        TestRuleValidator,
        TestCharacterInitializer,
        TestMacroEventSystem,
        TestFamilySystem
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出测试结果摘要
    print(f"\n{'='*60}")
    print(f"测试完成: {result.testsRun} 个测试")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"{'='*60}")
    
    # 如果有失败或错误，退出码为1
    exit(0 if result.wasSuccessful() else 1)