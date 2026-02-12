"""
本地模型动态加载策略
支持分层部署的量化模型（1.5B/3B/7B），根据设备性能自动选择和加载
"""

import os
import sys
import json
import threading
import time
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import hashlib

# 导入依赖管理
from .model_dependencies import dependency_manager
from .model_benchmark import ModelBenchmark, BenchmarkResult
from .model_manager import model_download_manager
from .device_compatibility import device_compatibility_checker, CompatibilityIssue

class ModelSize(Enum):
    """模型大小"""
    TINY = "1.5B"      # 1.5B参数 - 最小模型
    SMALL = "3B"       # 3B参数 - 小型模型
    MEDIUM = "7B"      # 7B参数 - 中型模型
    LARGE = "13B"      # 13B参数 - 大型模型（高端设备）

class ModelStatus(Enum):
    """模型状态"""
    NOT_LOADED = "not_loaded"
    LOADING = "loading"
    READY = "ready"
    ERROR = "error"
    UNLOADING = "unloading"

class DeviceTier(Enum):
    """设备档次"""
    LOW_END = "low"        # 低端设备：<4GB RAM
    MID_RANGE = "mid"      # 中端设备：4-8GB RAM
    HIGH_END = "high"      # 高端设备：8-16GB RAM
    ULTRA = "ultra"        # 旗舰设备：>16GB RAM

@dataclass
class ModelConfig:
    """模型配置"""
    name: str
    size: ModelSize
    path: str
    quantization: str  # Q4, Q5, Q8
    min_ram_gb: float
    vram_gb: float
    tokens_per_second: int
    quality_score: int  # 1-100

@dataclass
class DeviceProfile:
    """设备性能档案"""
    tier: DeviceTier
    total_ram_gb: float
    available_ram_gb: float
    cpu_cores: int
    has_gpu: bool
    vram_gb: float = 0
    recommended_model: ModelSize = ModelSize.TINY

class LocalModelManager:
    """本地模型管理器"""
    
    def __init__(self, models_dir: str = "models/"):
        self.models_dir = models_dir
        self.current_model: Optional[Any] = None
        self.current_config: Optional[ModelConfig] = None
        self.model_status = ModelStatus.NOT_LOADED
        self.device_profile: Optional[DeviceProfile] = None
        self.model_cache: Dict[str, Any] = {}
        self.load_callbacks: List[Callable] = []
        self.unload_callbacks: List[Callable] = []
        self.lock = threading.Lock()
        self.last_used: Optional[datetime] = None
        self.idle_timeout_seconds = 300  # 5分钟无使用自动卸载
        
        # 模型配置表
        self.model_configs = self._init_model_configs()
        
        # 初始化设备档案
        self._detect_device()
        
        # 检查依赖
        missing_required, missing_optional = dependency_manager.check_dependencies()
        if missing_required:
            print(f"[LocalModel] WARNING: 缺少必需依赖: {', '.join(missing_required)}")
            print("[LocalModel] 运行 'python -c \"from core.ai.model_dependencies import dependency_manager; dependency_manager.install_missing_required()\"' 来安装")
        
        # 启动空闲检测
        self._start_idle_monitor()
        
        # 初始化基准测试器
        self.benchmark = ModelBenchmark(self)
        
        # 检查设备兼容性
        compat_report = device_compatibility_checker.get_compatibility_report()
        if not compat_report["can_run_local_models"]:
            print("[LocalModel] WARNING: 设备可能不完全兼容本地模型运行")
            for issue in compat_report.get("critical_issues", []):
                print(f"   • {issue['message']}")
    
    def _init_model_configs(self) -> Dict[ModelSize, List[ModelConfig]]:
        """初始化模型配置"""
        return {
            ModelSize.TINY: [
                ModelConfig(
                    name="qwen-1.5b-chat-q4",
                    size=ModelSize.TINY,
                    path="qwen-1.5b-chat-q4_0.gguf",
                    quantization="Q4",
                    min_ram_gb=1.5,
                    vram_gb=0,
                    tokens_per_second=25,
                    quality_score=60
                ),
                ModelConfig(
                    name="phi-2-q4",
                    size=ModelSize.TINY,
                    path="phi-2-q4.gguf",
                    quantization="Q4",
                    min_ram_gb=1.2,
                    vram_gb=0,
                    tokens_per_second=30,
                    quality_score=55
                )
            ],
            ModelSize.SMALL: [
                ModelConfig(
                    name="qwen-3b-chat-q4",
                    size=ModelSize.SMALL,
                    path="qwen-3b-chat-q4_0.gguf",
                    quantization="Q4",
                    min_ram_gb=3.0,
                    vram_gb=0,
                    tokens_per_second=18,
                    quality_score=75
                ),
                ModelConfig(
                    name="phi-3-mini-q4",
                    size=ModelSize.SMALL,
                    path="phi-3-mini-q4.gguf",
                    quantization="Q4",
                    min_ram_gb=2.5,
                    vram_gb=0,
                    tokens_per_second=22,
                    quality_score=70
                )
            ],
            ModelSize.MEDIUM: [
                ModelConfig(
                    name="qwen-7b-chat-q4",
                    size=ModelSize.MEDIUM,
                    path="qwen-7b-chat-q4_0.gguf",
                    quantization="Q4",
                    min_ram_gb=6.0,
                    vram_gb=0,
                    tokens_per_second=12,
                    quality_score=85
                ),
                ModelConfig(
                    name="mistral-7b-q4",
                    size=ModelSize.MEDIUM,
                    path="mistral-7b-v0.1-q4.gguf",
                    quantization="Q4",
                    min_ram_gb=5.5,
                    vram_gb=0,
                    tokens_per_second=14,
                    quality_score=82
                )
            ],
            ModelSize.LARGE: [
                ModelConfig(
                    name="qwen-13b-chat-q4",
                    size=ModelSize.LARGE,
                    path="qwen-13b-chat-q4_0.gguf",
                    quantization="Q4",
                    min_ram_gb=10.0,
                    vram_gb=0,
                    tokens_per_second=8,
                    quality_score=90
                )
            ]
        }
    
    def _detect_device(self) -> DeviceProfile:
        """检测设备性能"""
        try:
            import psutil
            
            total_ram = psutil.virtual_memory().total / (1024**3)
            available_ram = psutil.virtual_memory().available / (1024**3)
            cpu_cores = psutil.cpu_count(logical=False) or 1
            
            # 检测GPU
            has_gpu = False
            vram_gb = 0
            try:
                import subprocess
                result = subprocess.run(['nvidia-smi', '--query-gpu=memory.total', '--format=csv,noheader'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    has_gpu = True
                    vram_str = result.stdout.strip().split()[0]
                    vram_gb = float(vram_str) / 1024
            except:
                pass
            
            # 确定设备档次
            if total_ram < 4:
                tier = DeviceTier.LOW_END
                recommended = ModelSize.TINY
            elif total_ram < 8:
                tier = DeviceTier.MID_RANGE
                recommended = ModelSize.SMALL
            elif total_ram < 16:
                tier = DeviceTier.HIGH_END
                recommended = ModelSize.MEDIUM
            else:
                tier = DeviceTier.ULTRA
                recommended = ModelSize.LARGE
            
            self.device_profile = DeviceProfile(
                tier=tier,
                total_ram_gb=total_ram,
                available_ram_gb=available_ram,
                cpu_cores=cpu_cores,
                has_gpu=has_gpu,
                vram_gb=vram_gb,
                recommended_model=recommended
            )
            
            print(f"[LocalModel] 设备检测: {tier.value}端设备, RAM: {total_ram:.1f}GB, 推荐模型: {recommended.value}")
            
        except Exception as e:
            print(f"[LocalModel] 设备检测失败，使用默认配置: {e}")
            self.device_profile = DeviceProfile(
                tier=DeviceTier.MID_RANGE,
                total_ram_gb=8.0,
                available_ram_gb=4.0,
                cpu_cores=4,
                has_gpu=False,
                recommended_model=ModelSize.SMALL
            )
        
        return self.device_profile
    
    def _start_idle_monitor(self):
        """启动空闲监控"""
        def monitor():
            while True:
                time.sleep(60)  # 每分钟检查一次
                with self.lock:
                    if self.model_status == ModelStatus.READY and self.last_used:
                        idle_seconds = (datetime.now() - self.last_used).total_seconds()
                        if idle_seconds > self.idle_timeout_seconds:
                            print("[LocalModel] 模型空闲超时，自动卸载")
                            self._unload_model_internal()
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
    
    def get_recommended_model(self) -> ModelConfig:
        """获取推荐模型配置"""
        if not self.device_profile:
            self._detect_device()
        
        size = self.device_profile.recommended_model
        configs = self.model_configs.get(size, [])
        
        if not configs:
            # 降级到更小的模型
            for smaller_size in [ModelSize.TINY, ModelSize.SMALL]:
                if smaller_size != size:
                    configs = self.model_configs.get(smaller_size, [])
                    if configs:
                        break
        
        return configs[0] if configs else None
    
    def load_model(self, model_size: Optional[ModelSize] = None, 
                   model_name: Optional[str] = None) -> bool:
        """加载模型"""
        with self.lock:
            if self.model_status == ModelStatus.READY:
                return True
            
            if self.model_status == ModelStatus.LOADING:
                print("[LocalModel] 模型正在加载中...")
                return False
            
            self.model_status = ModelStatus.LOADING
        
        try:
            # 选择模型配置
            if model_name:
                config = self._find_model_by_name(model_name)
            elif model_size:
                configs = self.model_configs.get(model_size, [])
                config = configs[0] if configs else None
            else:
                config = self.get_recommended_model()
            
            if not config:
                print("[LocalModel] 未找到合适的模型配置")
                self.model_status = ModelStatus.ERROR
                return False
            
            # 检查内存是否足够
            if not self._check_memory(config):
                print(f"[LocalModel] 内存不足，无法加载模型 {config.name}")
                self.model_status = ModelStatus.ERROR
                return False
            
            # 检查模型文件是否存在
            model_path = os.path.join(self.models_dir, config.path)
            if not os.path.exists(model_path):
                print(f"[LocalModel] 模型文件不存在: {model_path}")
                print("[LocalModel] 请下载模型文件或使用API模式")
                self.model_status = ModelStatus.ERROR
                return False
            
            # 加载模型
            print(f"[LocalModel] 正在加载模型: {config.name}")
            start_time = time.time()
            
            # 尝试使用 llama-cpp-python
            try:
                from llama_cpp import Llama
                
                self.current_model = Llama(
                    model_path=model_path,
                    n_ctx=2048,  # 上下文长度
                    n_threads=self.device_profile.cpu_cores if self.device_profile else 4,
                    verbose=False
                )
                
                load_time = time.time() - start_time
                print(f"[LocalModel] 模型加载完成，耗时: {load_time:.1f}秒")
                
                self.current_config = config
                self.model_status = ModelStatus.READY
                self.last_used = datetime.now()
                
                # 触发回调
                for callback in self.load_callbacks:
                    try:
                        callback(config)
                    except:
                        pass
                
                return True
                
            except ImportError:
                print("[LocalModel] llama-cpp-python 未安装")
                print("[LocalModel] 请运行: pip install llama-cpp-python")
                self.model_status = ModelStatus.ERROR
                return False
                
        except Exception as e:
            print(f"[LocalModel] 模型加载失败: {e}")
            self.model_status = ModelStatus.ERROR
            return False
    
    def _find_model_by_name(self, name: str) -> Optional[ModelConfig]:
        """按名称查找模型配置"""
        for configs in self.model_configs.values():
            for config in configs:
                if config.name == name:
                    return config
        return None
    
    def _check_memory(self, config: ModelConfig) -> bool:
        """检查内存是否足够"""
        try:
            import psutil
            available_ram = psutil.virtual_memory().available / (1024**3)
            
            # 预留一些内存给系统
            required = config.min_ram_gb * 1.2
            
            return available_ram >= required
        except:
            return True  # 无法检测时假设足够
    
    def unload_model(self) -> bool:
        """卸载模型"""
        with self.lock:
            return self._unload_model_internal()
    
    def _unload_model_internal(self) -> bool:
        """内部卸载方法（需要在lock内调用）"""
        if self.model_status != ModelStatus.READY:
            return True
        
        self.model_status = ModelStatus.UNLOADING
        
        try:
            # 触发回调
            for callback in self.unload_callbacks:
                try:
                    callback(self.current_config)
                except:
                    pass
            
            # 释放模型
            if self.current_model:
                del self.current_model
                self.current_model = None
            
            self.current_config = None
            self.model_status = ModelStatus.NOT_LOADED
            
            # 强制垃圾回收
            import gc
            gc.collect()
            
            print("[LocalModel] 模型已卸载")
            return True
            
        except Exception as e:
            print(f"[LocalModel] 卸载失败: {e}")
            self.model_status = ModelStatus.ERROR
            return False
    
    def generate(self, prompt: str, max_tokens: int = 512, 
                 temperature: float = 0.7) -> Dict[str, Any]:
        """生成文本"""
        if self.model_status != ModelStatus.READY:
            # 尝试自动加载
            if not self.load_model():
                return {
                    "success": False,
                    "error": "模型未加载",
                    "text": ""
                }
        
        try:
            self.last_used = datetime.now()
            
            output = self.current_model(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
                echo=False
            )
            
            text = output['choices'][0]['text'] if output.get('choices') else ""
            
            return {
                "success": True,
                "text": text,
                "model": self.current_config.name if self.current_config else "unknown",
                "tokens_used": len(text.split())
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "text": ""
            }
    
    def generate_events(self, state: Any, num_events: int = 3) -> Dict[str, Any]:
        """生成事件（专门用于人生模拟）"""
        age = getattr(state, 'age', 25)
        life_stage = getattr(state, 'life_stage', '青年')
        dimensions = getattr(state, 'dimensions', {})
        
        prompt = f"""请为以下角色生成{num_events}个人生事件，以JSON格式返回：
角色信息：
- 年龄：{age}岁
- 人生阶段：{life_stage}
- 当前状态：{json.dumps(dimensions, ensure_ascii=False)}

请返回事件数组，每个事件包含：
- title: 事件标题
- description: 事件描述
- eventType: 事件类型
- choices: 选项数组
- impacts: 影响对象

返回格式：[{{事件1}}, {{事件2}}, {{事件3}}]
"""
        
        result = self.generate(prompt, max_tokens=1000)
        
        if result["success"]:
            try:
                # 尝试解析JSON
                text = result["text"]
                # 提取JSON部分
                if '[' in text and ']' in text:
                    start = text.index('[')
                    end = text.rindex(']') + 1
                    json_str = text[start:end]
                    events = json.loads(json_str)
                    return {
                        "events": events,
                        "reasoning": "本地模型生成",
                        "confidence": self.current_config.quality_score / 100 if self.current_config else 0.6,
                        "level": "L1_LOCAL_MODEL",
                        "provider": "local",
                        "cost": 0
                    }
            except:
                pass
        
        return {
            "events": [],
            "reasoning": "生成失败",
            "confidence": 0,
            "error": result.get("error", "解析失败")
        }
    
    def register_load_callback(self, callback: Callable):
        """注册加载回调"""
        self.load_callbacks.append(callback)
    
    def register_unload_callback(self, callback: Callable):
        """注册卸载回调"""
        self.unload_callbacks.append(callback)
    
    def get_status(self) -> Dict[str, Any]:
        """获取模型状态"""
        return {
            "status": self.model_status.value,
            "current_model": self.current_config.name if self.current_config else None,
            "model_size": self.current_config.size.value if self.current_config else None,
            "device_tier": self.device_profile.tier.value if self.device_profile else None,
            "available_ram_gb": self.device_profile.available_ram_gb if self.device_profile else 0,
            "recommended_model": self.device_profile.recommended_model.value if self.device_profile else None,
            "last_used": self.last_used.isoformat() if self.last_used else None
        }
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """获取可用模型列表"""
        models = []
        for size, configs in self.model_configs.items():
            for config in configs:
                model_path = os.path.join(self.models_dir, config.path)
                # 同时检查本地文件系统和下载管理器
                file_available = os.path.exists(model_path)
                download_info = model_download_manager.get_model_info(config.name)
                
                models.append({
                    "name": config.name,
                    "size": config.size.value,
                    "quantization": config.quantization,
                    "min_ram_gb": config.min_ram_gb,
                    "quality_score": config.quality_score,
                    "available": file_available,
                    "downloadable": download_info is not None,
                    "recommended": size == (self.device_profile.recommended_model if self.device_profile else ModelSize.TINY),
                    "description": download_info.get("description", "") if download_info else ""
                })
        return models
    
    def download_model(self, model_name: str, force_redownload: bool = False) -> bool:
        """下载指定模型"""
        return model_download_manager.download_model(model_name, force_redownload=force_redownload)
    
    def download_model_async(self, model_name: str, progress_callback: Optional[Callable] = None) -> bool:
        """异步下载模型"""
        def completion_callback(name, success):
            if success:
                print(f"[LocalModel] 模型 {name} 下载完成")
                # 可以在这里触发模型加载
            else:
                print(f"[LocalModel] 模型 {name} 下载失败")
        
        return model_download_manager.download_in_background(
            model_name, 
            progress_callback=progress_callback,
            completion_callback=completion_callback
        )
    
    def delete_model(self, model_name: str) -> bool:
        """删除模型文件"""
        # 先从下载管理器删除
        model_download_manager.delete_model(model_name)
        
        # 再从本地文件删除
        model_info = model_download_manager.get_model_info(model_name)
        if model_info:
            model_path = os.path.join(self.models_dir, model_info["filename"])
            if os.path.exists(model_path):
                try:
                    os.remove(model_path)
                    print(f"[LocalModel] 已删除模型文件: {model_name}")
                    return True
                except Exception as e:
                    print(f"[LocalModel] 删除模型文件失败: {e}")
        return False
    
    def get_downloaded_models(self) -> List[Dict]:
        """获取已下载的模型列表"""
        return model_download_manager.get_downloaded_models()
    
    def get_download_progress(self, model_name: str) -> Optional[Dict]:
        """获取模型下载进度"""
        progress = model_download_manager.get_download_progress(model_name)
        if progress:
            return {
                "filename": progress.filename,
                "total_size": progress.total_size,
                "downloaded": progress.downloaded,
                "percentage": progress.percentage,
                "speed": progress.speed,
                "status": progress.status
            }
        return None
    
    def benchmark_model(self, model_name: Optional[str] = None, 
                       iterations: int = 3) -> Optional[BenchmarkResult]:
        """基准测试指定模型"""
        # 找到模型配置
        target_config = None
        if model_name:
            for configs in self.model_configs.values():
                for config in configs:
                    if config.name == model_name:
                        target_config = config
                        break
                if target_config:
                    break
        
        if not target_config:
            target_config = self.get_recommended_model()
        
        if not target_config:
            print("[LocalModel] 没有可用的模型进行测试")
            return None
        
        # 确保模型已下载
        if not self.is_model_downloaded(target_config.name):
            print(f"[LocalModel] 模型 {target_config.name} 未下载，开始下载...")
            if not self.download_model(target_config.name):
                print("[LocalModel] 模型下载失败，无法进行基准测试")
                return None
        
        # 执行基准测试
        return self.benchmark.benchmark_model(target_config, iterations=iterations)
    
    def benchmark_all_models(self, iterations: int = 2) -> List[BenchmarkResult]:
        """测试所有可用模型"""
        return self.benchmark.benchmark_all_models(iterations=iterations)
    
    def is_model_downloaded(self, model_name: str) -> bool:
        """检查模型是否已下载"""
        return model_download_manager.is_model_downloaded(model_name)
    
    def get_compatibility_report(self) -> Dict[str, Any]:
        """获取设备兼容性报告"""
        return device_compatibility_checker.get_compatibility_report()
    
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统信息"""
        return device_compatibility_checker.system_info
    
    def get_dependency_status(self) -> Dict[str, Any]:
        """获取依赖状态"""
        missing_required, missing_optional = dependency_manager.check_dependencies()
        return {
            "missing_required": missing_required,
            "missing_optional": missing_optional,
            "installation_guide": dependency_manager.get_installation_guide()
        }

# 全局本地模型管理器实例
local_model_manager = LocalModelManager()
