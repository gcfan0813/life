"""
本地模型加载策略单元测试
"""

import unittest
import tempfile
import os
import sys
from unittest.mock import Mock, patch, MagicMock
import json

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ai.local_model_loader import (
    LocalModelManager, ModelSize, ModelStatus, DeviceTier, 
    ModelConfig, DeviceProfile
)
from core.ai.model_dependencies import DependencyManager
from core.ai.model_benchmark import ModelBenchmark, BenchmarkResult
from core.ai.model_manager import ModelDownloadManager
from core.ai.device_compatibility import DeviceCompatibilityChecker, CompatibilityIssue

class TestLocalModelLoader(unittest.TestCase):
    """测试本地模型加载器"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.model_manager = LocalModelManager(models_dir=self.temp_dir)
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_model_config_creation(self):
        """测试模型配置创建"""
        config = ModelConfig(
            name="test-model",
            size=ModelSize.TINY,
            path="test.gguf",
            quantization="Q4",
            min_ram_gb=1.5,
            vram_gb=0,
            tokens_per_second=25,
            quality_score=60
        )
        
        self.assertEqual(config.name, "test-model")
        self.assertEqual(config.size, ModelSize.TINY)
        self.assertEqual(config.min_ram_gb, 1.5)
        self.assertEqual(config.quality_score, 60)
    
    def test_device_profile_creation(self):
        """测试设备档案创建"""
        profile = DeviceProfile(
            tier=DeviceTier.MID_RANGE,
            total_ram_gb=8.0,
            available_ram_gb=4.0,
            cpu_cores=4,
            has_gpu=False,
            recommended_model=ModelSize.SMALL
        )
        
        self.assertEqual(profile.tier, DeviceTier.MID_RANGE)
        self.assertEqual(profile.total_ram_gb, 8.0)
        self.assertEqual(profile.recommended_model, ModelSize.SMALL)
    
    @patch('core.ai.local_model_loader.psutil.virtual_memory')
    @patch('core.ai.local_model_loader.psutil.cpu_count')
    def test_device_detection(self, mock_cpu_count, mock_virtual_memory):
        """测试设备检测"""
        # Mock系统信息
        mock_memory = Mock()
        mock_memory.total = 8 * 1024**3  # 8GB
        mock_memory.available = 4 * 1024**3  # 4GB
        mock_virtual_memory.return_value = mock_memory
        
        mock_cpu_count.return_value = 4
        
        # 重新初始化管理器以触发设备检测
        manager = LocalModelManager(models_dir=self.temp_dir)
        
        self.assertIsNotNone(manager.device_profile)
        self.assertEqual(manager.device_profile.total_ram_gb, 8.0)
        self.assertEqual(manager.device_profile.cpu_cores, 4)
    
    def test_model_config_initialization(self):
        """测试模型配置初始化"""
        self.assertIn(ModelSize.TINY, self.model_manager.model_configs)
        self.assertIn(ModelSize.SMALL, self.model_manager.model_configs)
        self.assertIn(ModelSize.MEDIUM, self.model_manager.model_configs)
        
        # 检查TINY模型配置
        tiny_configs = self.model_manager.model_configs[ModelSize.TINY]
        self.assertGreater(len(tiny_configs), 0)
        
        first_config = tiny_configs[0]
        self.assertEqual(first_config.size, ModelSize.TINY)
        self.assertIn("qwen-1.5b", first_config.name)
    
    @patch('core.ai.local_model_loader.LocalModelManager._check_memory')
    @patch('os.path.exists')
    def test_load_model_insufficient_memory(self, mock_exists, mock_check_memory):
        """测试内存不足时的模型加载"""
        mock_exists.return_value = True
        mock_check_memory.return_value = False
        
        result = self.model_manager.load_model(model_size=ModelSize.TINY)
        
        self.assertFalse(result)
        self.assertEqual(self.model_manager.model_status, ModelStatus.ERROR)
    
    @patch('core.ai.local_model_loader.LocalModelManager._check_memory')
    @patch('os.path.exists')
    def test_load_model_file_not_found(self, mock_exists, mock_check_memory):
        """测试模型文件不存在的情况"""
        mock_exists.return_value = False
        mock_check_memory.return_value = True
        
        result = self.model_manager.load_model(model_size=ModelSize.TINY)
        
        self.assertFalse(result)
        self.assertEqual(self.model_manager.model_status, ModelStatus.ERROR)
    
    def test_get_recommended_model(self):
        """测试获取推荐模型"""
        # Mock设备档案
        self.model_manager.device_profile = DeviceProfile(
            tier=DeviceTier.LOW_END,
            total_ram_gb=2.0,
            available_ram_gb=1.0,
            cpu_cores=2,
            has_gpu=False,
            recommended_model=ModelSize.TINY
        )
        
        recommended = self.model_manager.get_recommended_model()
        
        self.assertIsNotNone(recommended)
        self.assertEqual(recommended.size, ModelSize.TINY)
    
    def test_get_status(self):
        """测试获取状态"""
        status = self.model_manager.get_status()
        
        self.assertIn("status", status)
        self.assertIn("device_tier", status)
        self.assertIn("recommended_model", status)
        
        self.assertEqual(status["status"], ModelStatus.NOT_LOADED.value)
    
    def test_get_available_models(self):
        """测试获取可用模型列表"""
        models = self.model_manager.get_available_models()
        
        self.assertIsInstance(models, list)
        self.assertGreater(len(models), 0)
        
        # 检查模型信息结构
        first_model = models[0]
        required_fields = ["name", "size", "quantization", "min_ram_gb", "quality_score", "available"]
        for field in required_fields:
            self.assertIn(field, first_model)

class TestDependencyManager(unittest.TestCase):
    """测试依赖管理器"""
    
    def test_dependency_manager_creation(self):
        """测试依赖管理器创建"""
        dep_manager = DependencyManager()
        
        self.assertIsInstance(dep_manager.REQUIRED_PACKAGES, dict)
        self.assertIsInstance(dep_manager.OPTIONAL_PACKAGES, dict)
    
    @patch('importlib.import_module')
    def test_check_dependencies(self, mock_import):
        """测试依赖检查"""
        # Mock导入成功
        mock_import.return_value = Mock()
        
        dep_manager = DependencyManager()
        missing_required, missing_optional = dep_manager.check_dependencies()
        
        # 由于我们使用了mock，应该没有缺失的包
        self.assertIsInstance(missing_required, list)
        self.assertIsInstance(missing_optional, list)

class TestModelBenchmark(unittest.TestCase):
    """测试模型基准测试"""
    
    def setUp(self):
        """测试前准备"""
        self.model_manager = Mock()
        self.benchmark = ModelBenchmark(self.model_manager)
    
    def test_benchmark_result_creation(self):
        """测试基准测试结果创建"""
        result = BenchmarkResult(
            model_name="test-model",
            model_size="TINY",
            load_time=1.5,
            first_token_time=0.1,
            avg_token_time=0.05,
            tokens_per_second=20.0,
            memory_usage_mb=500.0,
            test_prompt="test",
            test_output_length=50,
            success=True
        )
        
        self.assertEqual(result.model_name, "test-model")
        self.assertTrue(result.success)
        self.assertEqual(result.tokens_per_second, 20.0)

class TestModelDownloadManager(unittest.TestCase):
    """测试模型下载管理器"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.download_manager = ModelDownloadManager(models_dir=self.temp_dir)
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_model_info_retrieval(self):
        """测试模型信息获取"""
        model_info = self.download_manager.get_model_info("qwen-1.5b-chat-q4")
        
        self.assertIsNotNone(model_info)
        self.assertIn("url", model_info)
        self.assertIn("filename", model_info)
        self.assertIn("size_mb", model_info)
    
    def test_unknown_model_info(self):
        """测试未知模型信息"""
        model_info = self.download_manager.get_model_info("unknown-model")
        
        self.assertIsNone(model_info)
    
    def test_is_model_downloaded(self):
        """测试模型下载状态检查"""
        # 模型文件不存在，应该返回False
        result = self.download_manager.is_model_downloaded("qwen-1.5b-chat-q4")
        self.assertFalse(result)
    
    def test_get_repository_status(self):
        """测试仓库状态获取"""
        status = self.download_manager.get_repository_status()
        
        self.assertIn("total_models", status)
        self.assertIn("downloaded_models", status)
        self.assertIn("available_models", status)
        self.assertIn("total_size_mb", status)
        
        self.assertEqual(status["total_models"], len(self.download_manager.MODEL_REPOSITORIES))

class TestDeviceCompatibilityChecker(unittest.TestCase):
    """测试设备兼容性检查器"""
    
    def setUp(self):
        """测试前准备"""
        self.compatibility_checker = DeviceCompatibilityChecker()
    
    def test_system_info_collection(self):
        """测试系统信息收集"""
        system_info = self.compatibility_checker.system_info
        
        self.assertIn("platform", system_info)
        self.assertIn("architecture", system_info)
        self.assertIn("python_version", system_info)
        self.assertIn("os_platform", system_info)
        self.assertIn("cpu_arch", system_info)
    
    def test_compatibility_check(self):
        """测试兼容性检查"""
        issues = self.compatibility_checker.check_compatibility()
        
        self.assertIsInstance(issues, list)
        
        # 检查问题严重程度分类
        severities = set(issue.severity for issue in issues)
        valid_severities = {"critical", "warning", "info"}
        self.assertTrue(severities.issubset(valid_severities))
    
    def test_get_recommended_models(self):
        """测试获取推荐模型"""
        recommended = self.compatibility_checker.get_recommended_models()
        
        self.assertIsInstance(recommended, list)
        self.assertGreater(len(recommended), 0)
    
    def test_compatibility_report(self):
        """测试兼容性报告"""
        report = self.compatibility_checker.get_compatibility_report()
        
        self.assertIn("system_info", report)
        self.assertIn("compatibility_status", report)
        self.assertIn("critical_issues", report)
        self.assertIn("recommended_models", report)
        self.assertIn("can_run_local_models", report)
        
        self.assertIsInstance(report["can_run_local_models"], bool)

class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow_simulation(self):
        """测试完整工作流程模拟"""
        # 这个测试模拟完整的模型加载工作流程
        
        # 1. 创建设备兼容性检查器
        compatibility_checker = DeviceCompatibilityChecker()
        report = compatibility_checker.get_compatibility_report()
        
        # 2. 创建模型管理器
        temp_dir = tempfile.mkdtemp()
        try:
            model_manager = LocalModelManager(models_dir=temp_dir)
            
            # 3. 检查状态
            status = model_manager.get_status()
            self.assertIn("status", status)
            
            # 4. 获取推荐模型
            recommended = model_manager.get_recommended_model()
            # 可能为None，但不应该崩溃
            
            # 5. 获取可用模型列表
            available_models = model_manager.get_available_models()
            self.assertIsInstance(available_models, list)
            
        finally:
            import shutil
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

if __name__ == '__main__':
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestLocalModelLoader,
        TestDependencyManager,
        TestModelBenchmark,
        TestModelDownloadManager,
        TestDeviceCompatibilityChecker,
        TestIntegration
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