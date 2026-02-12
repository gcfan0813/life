"""
本地模型依赖检查和安装辅助模块
"""

import sys
import subprocess
import importlib
from typing import List, Tuple, Optional

class DependencyManager:
    """依赖管理器"""
    
    REQUIRED_PACKAGES = {
        'psutil': 'psutil>=5.9.0',
        'llama_cpp': 'llama-cpp-python>=0.2.0'
    }
    
    OPTIONAL_PACKAGES = {
        'torch': 'torch>=2.0.0',
        'transformers': 'transformers>=4.30.0'
    }
    
    def __init__(self):
        self.missing_required = []
        self.missing_optional = []
        self.check_dependencies()
    
    def check_dependencies(self) -> Tuple[List[str], List[str]]:
        """检查依赖包"""
        self.missing_required = []
        self.missing_optional = []
        
        # 检查必需包
        for module_name, pkg_spec in self.REQUIRED_PACKAGES.items():
            if not self._is_module_installed(module_name):
                self.missing_required.append(pkg_spec)
        
        # 检查可选包
        for module_name, pkg_spec in self.OPTIONAL_PACKAGES.items():
            if not self._is_module_installed(module_name):
                self.missing_optional.append(pkg_spec)
        
        return self.missing_required, self.missing_optional
    
    def _is_module_installed(self, module_name: str) -> bool:
        """检查模块是否已安装"""
        try:
            importlib.import_module(module_name)
            return True
        except ImportError:
            return False
    
    def install_package(self, package_spec: str) -> bool:
        """安装单个包"""
        try:
            print(f"[Dependency] 正在安装 {package_spec}...")
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', package_spec
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"[Dependency] {package_spec} 安装成功")
                return True
            else:
                print(f"[Dependency] {package_spec} 安装失败: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print(f"[Dependency] {package_spec} 安装超时")
            return False
        except Exception as e:
            print(f"[Dependency] 安装过程出错: {e}")
            return False
    
    def install_missing_required(self) -> bool:
        """安装所有缺失的必需包"""
        if not self.missing_required:
            return True
        
        print(f"[Dependency] 需要安装 {len(self.missing_required)} 个必需包")
        
        for pkg in self.missing_required:
            if not self.install_package(pkg):
                print(f"[Dependency] 关键包安装失败: {pkg}")
                return False
        
        return True
    
    def get_installation_guide(self) -> str:
        """获取安装指南"""
        guide = []
        guide.append("=== 本地模型依赖安装指南 ===\n")
        
        if self.missing_required:
            guide.append("【必需依赖】")
            for pkg in self.missing_required:
                guide.append(f"  pip install {pkg}")
            guide.append("")
        
        if self.missing_optional:
            guide.append("【可选依赖 - 用于更好性能】")
            for pkg in self.missing_optional:
                guide.append(f"  pip install {pkg}")
            guide.append("")
        
        guide.append("【手动安装命令】")
        if self.missing_required:
            packages = ' '.join(self.missing_required)
            guide.append(f"  pip install {packages}")
        
        guide.append("\n【注意事项】")
        guide.append("1. llama-cpp-python 可能需要C++编译器")
        guide.append("2. Windows用户建议安装Visual Studio Build Tools")
        guide.append("3. 如果安装失败，可以尝试: pip install --no-cache-dir")
        
        return '\n'.join(guide)

# 全局依赖管理器
dependency_manager = DependencyManager()