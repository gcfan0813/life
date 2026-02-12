"""
设备兼容性检测和适配模块
"""

import platform
import subprocess
import json
import os
from typing import Dict, List, Any, Optional
from enum import Enum
import sys
from dataclasses import asdict

class Architecture(Enum):
    """CPU架构"""
    X86_64 = "x86_64"
    ARM64 = "arm64"
    ARM32 = "arm32"
    X86 = "x86"
    UNKNOWN = "unknown"

class OSPlatform(Enum):
    """操作系统平台"""
    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"
    UNKNOWN = "unknown"

class CompatibilityIssue:
    """兼容性问题"""
    def __init__(self, severity: str, message: str, solution: str = ""):
        self.severity = severity  # critical, warning, info
        self.message = message
        self.solution = solution

class DeviceCompatibilityChecker:
    """设备兼容性检查器"""
    
    def __init__(self):
        self.system_info = self._collect_system_info()
        self.compatibility_issues = []
        self.check_compatibility()
    
    def _collect_system_info(self) -> Dict[str, Any]:
        """收集系统信息"""
        info = {
            "platform": platform.system().lower(),
            "architecture": platform.machine().lower(),
            "processor": platform.processor(),
            "python_version": sys.version,
            "python_bits": 64 if sys.maxsize > 2**32 else 32
        }
        
        # 检测操作系统
        if info["platform"] == "windows":
            info["os_platform"] = OSPlatform.WINDOWS
        elif info["platform"] == "linux":
            info["os_platform"] = OSPlatform.LINUX
        elif info["platform"] == "darwin":
            info["os_platform"] = OSPlatform.MACOS
        else:
            info["os_platform"] = OSPlatform.UNKNOWN
        
        # 检测架构
        arch = info["architecture"]
        if "x86_64" in arch or "amd64" in arch:
            info["cpu_arch"] = Architecture.X86_64
        elif "aarch64" in arch or "arm64" in arch:
            info["cpu_arch"] = Architecture.ARM64
        elif "arm" in arch:
            info["cpu_arch"] = Architecture.ARM32
        elif "i386" in arch or "i686" in arch:
            info["cpu_arch"] = Architecture.X86
        else:
            info["cpu_arch"] = Architecture.UNKNOWN
        
        # 尝试获取更详细的信息
        self._enhance_system_info(info)
        
        return info
    
    def _enhance_system_info(self, info: Dict[str, Any]):
        """增强系统信息收集"""
        try:
            import psutil
            
            # 内存信息
            memory = psutil.virtual_memory()
            info["total_memory_gb"] = round(memory.total / (1024**3), 1)
            info["available_memory_gb"] = round(memory.available / (1024**3), 1)
            info["memory_percent"] = memory.percent
            
            # CPU信息
            info["cpu_count_logical"] = psutil.cpu_count(logical=True)
            info["cpu_count_physical"] = psutil.cpu_count(logical=False)
            
            # 磁盘信息
            disk = psutil.disk_usage('/')
            info["disk_free_gb"] = round(disk.free / (1024**3), 1)
            
        except ImportError:
            info["warning"] = "psutil not available, limited system info"
        except Exception as e:
            info["error"] = f"Failed to collect enhanced info: {e}"
        
        # GPU信息
        self._detect_gpu_info(info)
    
    def _detect_gpu_info(self, info: Dict[str, Any]):
        """检测GPU信息"""
        info["gpu_info"] = []
        
        # NVIDIA GPU检测
        try:
            if info["os_platform"] == OSPlatform.WINDOWS:
                result = subprocess.run([
                    "nvidia-smi", "--query-gpu=name,memory.total,memory.free",
                    "--format=csv,noheader,nounits"
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    for line in result.stdout.strip().split('\n'):
                        if line.strip():
                            parts = line.split(', ')
                            if len(parts) >= 2:
                                info["gpu_info"].append({
                                    "vendor": "nvidia",
                                    "name": parts[0].strip(),
                                    "total_memory_mb": int(parts[1]),
                                    "free_memory_mb": int(parts[2]) if len(parts) > 2 else 0
                                })
            
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
            pass
        
        # Apple Silicon 检测
        if info["cpu_arch"] == Architecture.ARM64 and info["os_platform"] == OSPlatform.MACOS:
            try:
                result = subprocess.run([
                    "sysctl", "-n", "machdep.cpu.brand_string"
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    cpu_info = result.stdout.strip()
                    if "Apple" in cpu_info:
                        info["gpu_info"].append({
                            "vendor": "apple",
                            "name": cpu_info,
                            "type": "integrated"
                        })
            except:
                pass
    
    def check_compatibility(self) -> List[CompatibilityIssue]:
        """检查兼容性"""
        self.compatibility_issues.clear()
        
        self._check_os_compatibility()
        self._check_architecture_compatibility()
        self._check_memory_compatibility()
        self._check_disk_space()
        self._check_python_compatibility()
        self._check_dependencies_compatibility()
        
        return self.compatibility_issues
    
    def _check_os_compatibility(self):
        """检查操作系统兼容性"""
        os_platform = self.system_info.get("os_platform")
        
        if os_platform == OSPlatform.UNKNOWN:
            self.compatibility_issues.append(CompatibilityIssue(
                "critical",
                f"不支持的操作系统: {self.system_info.get('platform')}",
                "请使用 Windows、Linux 或 macOS"
            ))
        elif os_platform == OSPlatform.WINDOWS:
            # Windows 通常兼容性良好
            pass
        elif os_platform == OSPlatform.LINUX:
            # Linux 需要检查一些依赖
            pass
        elif os_platform == OSPlatform.MACOS:
            # macOS 需要检查架构
            if self.system_info.get("cpu_arch") == Architecture.ARM64:
                # Apple Silicon 需要特殊处理
                pass
    
    def _check_architecture_compatibility(self):
        """检查架构兼容性"""
        cpu_arch = self.system_info.get("cpu_arch")
        python_bits = self.system_info.get("python_bits")
        
        if cpu_arch == Architecture.UNKNOWN:
            self.compatibility_issues.append(CompatibilityIssue(
                "warning",
                f"未知的CPU架构: {self.system_info.get('architecture')}",
                "某些模型可能无法正常运行"
            ))
        
        # 检查Python位数匹配
        if python_bits == 32:
            self.compatibility_issues.append(CompatibilityIssue(
                "critical",
                "检测到32位Python，建议使用64位Python",
                "请从官网下载64位Python安装包"
            ))
        
        # ARM架构特殊处理
        if cpu_arch == Architecture.ARM64:
            self.compatibility_issues.append(CompatibilityIssue(
                "info",
                "检测到ARM64架构（如Apple Silicon或ARM服务器）",
                "某些模型可能需要特殊编译版本"
            ))
    
    def _check_memory_compatibility(self):
        """检查内存兼容性"""
        total_memory = self.system_info.get("total_memory_gb", 0)
        
        if total_memory == 0:
            self.compatibility_issues.append(CompatibilityIssue(
                "warning",
                "无法检测系统内存",
                "请确保至少有4GB可用内存来运行本地模型"
            ))
            return
        
        if total_memory < 4:
            self.compatibility_issues.append(CompatibilityIssue(
                "critical",
                f"系统内存不足: {total_memory}GB (推荐4GB+)",
                "建议使用更小尺寸的模型或升级硬件"
            ))
        elif total_memory < 8:
            self.compatibility_issues.append(CompatibilityIssue(
                "warning",
                f"系统内存较少: {total_memory}GB (推荐8GB+)",
                "建议只使用1.5B或3B尺寸的模型"
            ))
        elif total_memory < 16:
            self.compatibility_issues.append(CompatibilityIssue(
                "info",
                f"系统内存适中: {total_memory}GB",
                "可以运行7B及以下尺寸的模型"
            ))
        else:
            self.compatibility_issues.append(CompatibilityIssue(
                "info",
                f"系统内存充足: {total_memory}GB",
                "可以运行所有支持的模型尺寸"
            ))
    
    def _check_disk_space(self):
        """检查磁盘空间"""
        disk_free = self.system_info.get("disk_free_gb", 0)
        
        if disk_free == 0:
            self.compatibility_issues.append(CompatibilityIssue(
                "warning",
                "无法检测磁盘空间",
                "请确保至少有5GB可用空间存储模型文件"
            ))
            return
        
        required_space = 10  # GB
        if disk_free < required_space:
            self.compatibility_issues.append(CompatibilityIssue(
                "critical",
                f"磁盘空间不足: {disk_free}GB (需要{required_space}GB+)",
                "请清理磁盘空间或更改模型存储位置"
            ))
    
    def _check_python_compatibility(self):
        """检查Python兼容性"""
        python_version = self.system_info.get("python_version", "")
        
        # 检查Python版本
        if "3.8" not in python_version and "3.9" not in python_version and "3.10" not in python_version and "3.11" not in python_version:
            self.compatibility_issues.append(CompatibilityIssue(
                "warning",
                f"Python版本可能不兼容: {python_version}",
                "推荐使用Python 3.8-3.11"
            ))
    
    def _check_dependencies_compatibility(self):
        """检查依赖兼容性"""
        # 检查llama-cpp-python的特定要求
        os_platform = self.system_info.get("os_platform")
        cpu_arch = self.system_info.get("cpu_arch")
        
        if os_platform == OSPlatform.WINDOWS:
            self.compatibility_issues.append(CompatibilityIssue(
                "info",
                "Windows平台需要Visual Studio Build Tools来编译llama-cpp-python",
                "可以从 https://visualstudio.microsoft.com/visual-cpp-build-tools/ 下载"
            ))
        
        if cpu_arch == Architecture.ARM64:
            self.compatibility_issues.append(CompatibilityIssue(
                "info",
                "ARM64架构可能需要从源码编译llama-cpp-python",
                "这可能需要较长时间和额外的编译工具"
            ))
    
    def get_recommended_models(self) -> List[str]:
        """根据设备兼容性推荐模型"""
        total_memory = self.system_info.get("total_memory_gb", 8)
        cpu_arch = self.system_info.get("cpu_arch")
        
        recommendations = []
        
        # 基于内存推荐
        if total_memory < 4:
            recommendations.extend(["qwen-1.5b-chat-q4", "phi-2-q4"])
        elif total_memory < 8:
            recommendations.extend(["qwen-1.5b-chat-q4", "qwen-3b-chat-q4", "phi-2-q4", "phi-3-mini-q4"])
        elif total_memory < 16:
            recommendations.extend(["qwen-3b-chat-q4", "qwen-7b-chat-q4", "phi-3-mini-q4", "mistral-7b-q4"])
        else:
            recommendations.extend(["qwen-7b-chat-q4", "mistral-7b-q4"])
        
        # 基于架构的特殊考虑
        if cpu_arch == Architecture.ARM64:
            # ARM64可能对某些模型有更好的优化
            pass
        
        return recommendations
    
    def get_compatibility_report(self) -> Dict[str, Any]:
        """获取兼容性报告"""
        critical_issues = [issue for issue in self.compatibility_issues if issue.severity == "critical"]
        warning_issues = [issue for issue in self.compatibility_issues if issue.severity == "warning"]
        info_issues = [issue for issue in self.compatibility_issues if issue.severity == "info"]
        
        # 手动转换CompatibilityIssue为字典
        def issue_to_dict(issue):
            return {
                "severity": issue.severity,
                "message": issue.message,
                "solution": issue.solution
            }
        
        return {
            "system_info": self.system_info,
            "compatibility_status": "compatible" if not critical_issues else "incompatible",
            "critical_issues": [issue_to_dict(issue) for issue in critical_issues],
            "warning_issues": [issue_to_dict(issue) for issue in warning_issues],
            "info_issues": [issue_to_dict(issue) for issue in info_issues],
            "recommended_models": self.get_recommended_models(),
            "can_run_local_models": len(critical_issues) == 0
        }

# 全局兼容性检查器
device_compatibility_checker = DeviceCompatibilityChecker()