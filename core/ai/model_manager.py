"""
模型下载和管理模块
"""

import os
import sys
import json
import hashlib
import requests
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from urllib.parse import urlparse
import threading
from dataclasses import dataclass

@dataclass
class DownloadProgress:
    """下载进度信息"""
    filename: str
    total_size: int
    downloaded: int
    percentage: float
    speed: float  # bytes per second
    status: str  # downloading, completed, error

class ModelDownloadManager:
    """模型下载管理器"""
    
    # 预定义的模型下载信息
    MODEL_REPOSITORIES = {
        "qwen-1.5b-chat-q4": {
            "url": "https://huggingface.co/Qwen/Qwen-1.5-1.8B-Chat-GGUF/resolve/main/qwen1.5-1.8b-chat-q4_0.gguf",
            "filename": "qwen-1.5b-chat-q4_0.gguf",
            "size_mb": 1200,
            "sha256": None,  # 可选的校验和
            "description": "Qwen 1.5B Chat Model (Q4 quantized)"
        },
        "qwen-3b-chat-q4": {
            "url": "https://huggingface.co/Qwen/Qwen-1.5-3B-Chat-GGUF/resolve/main/qwen1.5-3b-chat-q4_0.gguf",
            "filename": "qwen-3b-chat-q4_0.gguf",
            "size_mb": 2000,
            "sha256": None,
            "description": "Qwen 3B Chat Model (Q4 quantized)"
        },
        "qwen-7b-chat-q4": {
            "url": "https://huggingface.co/Qwen/Qwen-1.5-7B-Chat-GGUF/resolve/main/qwen1.5-7b-chat-q4_0.gguf",
            "filename": "qwen-7b-chat-q4_0.gguf",
            "size_mb": 4200,
            "sha256": None,
            "description": "Qwen 7B Chat Model (Q4 quantized)"
        },
        "phi-2-q4": {
            "url": "https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf",
            "filename": "phi-2-q4.gguf",
            "size_mb": 1800,
            "sha256": None,
            "description": "Phi-2 Model (Q4 quantized)"
        },
        "phi-3-mini-q4": {
            "url": "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf",
            "filename": "phi-3-mini-q4.gguf",
            "size_mb": 2400,
            "sha256": None,
            "description": "Phi-3 Mini Model (Q4 quantized)"
        },
        "mistral-7b-q4": {
            "url": "https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf",
            "filename": "mistral-7b-v0.1-q4.gguf",
            "size_mb": 4300,
            "sha256": None,
            "description": "Mistral 7B Model (Q4 quantized)"
        }
    }
    
    def __init__(self, models_dir: str = "models/"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.download_progress: Dict[str, DownloadProgress] = {}
        self.active_downloads: Dict[str, threading.Thread] = {}
        self.callbacks: Dict[str, List[Callable]] = {
            'progress': [],
            'completed': [],
            'error': []
        }
    
    def get_model_info(self, model_name: str) -> Optional[Dict]:
        """获取模型信息"""
        return self.MODEL_REPOSITORIES.get(model_name)
    
    def is_model_downloaded(self, model_name: str) -> bool:
        """检查模型是否已下载"""
        model_info = self.get_model_info(model_name)
        if not model_info:
            return False
        
        model_path = self.models_dir / model_info["filename"]
        return model_path.exists()
    
    def get_downloaded_models(self) -> List[Dict]:
        """获取已下载的模型列表"""
        downloaded = []
        
        for model_name, repo_info in self.MODEL_REPOSITORIES.items():
            if self.is_model_downloaded(model_name):
                model_path = self.models_dir / repo_info["filename"]
                stat = model_path.stat()
                
                downloaded.append({
                    "name": model_name,
                    "filename": repo_info["filename"],
                    "size_mb": repo_info["size_mb"],
                    "actual_size_mb": round(stat.st_size / 1024 / 1024, 1),
                    "description": repo_info["description"],
                    "download_date": stat.st_mtime
                })
        
        return downloaded
    
    def download_model(self, 
                      model_name: str,
                      progress_callback: Optional[Callable] = None,
                      force_redownload: bool = False) -> bool:
        """下载模型"""
        model_info = self.get_model_info(model_name)
        if not model_info:
            print(f"[ModelManager] 未知模型: {model_name}")
            return False
        
        # 检查是否已存在
        if not force_redownload and self.is_model_downloaded(model_name):
            print(f"[ModelManager] 模型已存在: {model_name}")
            return True
        
        # 检查URL是否有效
        if not model_info.get("url"):
            print(f"[ModelManager] 模型 {model_name} 没有下载链接")
            return False
        
        # 开始下载
        return self._download_file(model_name, model_info, progress_callback)
    
    def _download_file(self, model_name: str, model_info: Dict, progress_callback: Optional[Callable]) -> bool:
        """下载文件"""
        url = model_info["url"]
        filename = model_info["filename"]
        expected_size = model_info.get("size_mb", 0) * 1024 * 1024
        
        model_path = self.models_dir / filename
        temp_path = self.models_dir / f"{filename}.tmp"
        
        print(f"[ModelManager] 开始下载: {model_name} ({filename})")
        print(f"[ModelManager] 大小: {model_info.get('size_mb', 'unknown')} MB")
        print(f"[ModelManager] 源: {url}")
        
        try:
            # 发起请求
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # 获取实际文件大小
            total_size = int(response.headers.get('content-length', expected_size))
            
            # 初始化进度
            progress = DownloadProgress(
                filename=filename,
                total_size=total_size,
                downloaded=0,
                percentage=0,
                speed=0,
                status="downloading"
            )
            self.download_progress[model_name] = progress
            
            # 下载文件
            start_time = time.time()
            downloaded = 0
            chunk_size = 8192
            
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # 更新进度
                        elapsed = time.time() - start_time
                        speed = downloaded / elapsed if elapsed > 0 else 0
                        
                        progress.downloaded = downloaded
                        progress.percentage = (downloaded / total_size) * 100
                        progress.speed = speed
                        
                        # 调用进度回调
                        if progress_callback:
                            progress_callback(progress)
                        
                        # 触发全局回调
                        for cb in self.callbacks['progress']:
                            try:
                                cb(progress)
                            except:
                                pass
            
            # 下载完成，重命名文件
            temp_path.rename(model_path)
            
            # 验证文件大小
            actual_size = model_path.stat().st_size
            if actual_size < total_size * 0.9:  # 小于预期的90%认为失败
                print(f"[ModelManager] 文件大小异常: {actual_size} vs {total_size}")
                model_path.unlink()  # 删除不完整的文件
                raise Exception("下载文件不完整")
            
            # 更新进度状态
            progress.status = "completed"
            progress.percentage = 100
            
            print(f"[ModelManager] 下载完成: {filename} ({actual_size/1024/1024:.1f} MB)")
            
            # 触发完成回调
            for cb in self.callbacks['completed']:
                try:
                    cb(model_name, str(model_path))
                except:
                    pass
            
            return True
            
        except Exception as e:
            print(f"[ModelManager] 下载失败: {e}")
            
            # 清理临时文件
            if temp_path.exists():
                temp_path.unlink()
            
            # 更新进度状态
            if model_name in self.download_progress:
                self.download_progress[model_name].status = "error"
            
            # 触发错误回调
            for cb in self.callbacks['error']:
                try:
                    cb(model_name, str(e))
                except:
                    pass
            
            return False
    
    def download_in_background(self, 
                              model_name: str,
                              progress_callback: Optional[Callable] = None,
                              completion_callback: Optional[Callable] = None) -> bool:
        """后台下载模型"""
        if model_name in self.active_downloads:
            print(f"[ModelManager] 模型 {model_name} 已在下载中")
            return False
        
        def download_thread():
            success = self.download_model(model_name, progress_callback)
            
            if completion_callback:
                try:
                    completion_callback(model_name, success)
                except:
                    pass
            
            # 清理活动下载记录
            if model_name in self.active_downloads:
                del self.active_downloads[model_name]
        
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
        
        self.active_downloads[model_name] = thread
        return True
    
    def cancel_download(self, model_name: str) -> bool:
        """取消下载"""
        # 注意：这里简化处理，实际需要更复杂的取消机制
        if model_name in self.active_downloads:
            print(f"[ModelManager] 标记取消下载: {model_name}")
            # 实际实现需要能够中断下载线程
            return True
        return False
    
    def delete_model(self, model_name: str) -> bool:
        """删除已下载的模型"""
        model_info = self.get_model_info(model_name)
        if not model_info:
            return False
        
        model_path = self.models_dir / model_info["filename"]
        
        if not model_path.exists():
            print(f"[ModelManager] 模型文件不存在: {model_name}")
            return False
        
        try:
            model_path.unlink()
            print(f"[ModelManager] 已删除模型: {model_name}")
            return True
        except Exception as e:
            print(f"[ModelManager] 删除失败: {e}")
            return False
    
    def get_download_progress(self, model_name: str) -> Optional[DownloadProgress]:
        """获取下载进度"""
        return self.download_progress.get(model_name)
    
    def register_callback(self, event_type: str, callback: Callable):
        """注册回调函数"""
        if event_type in self.callbacks:
            self.callbacks[event_type].append(callback)
    
    def get_repository_status(self) -> Dict[str, Any]:
        """获取仓库状态"""
        total_models = len(self.MODEL_REPOSITORIES)
        downloaded_models = len(self.get_downloaded_models())
        total_size_mb = sum(info.get("size_mb", 0) for info in self.MODEL_REPOSITORIES.values())
        downloaded_size_mb = sum(m["actual_size_mb"] for m in self.get_downloaded_models())
        
        return {
            "total_models": total_models,
            "downloaded_models": downloaded_models,
            "available_models": total_models - downloaded_models,
            "total_size_mb": total_size_mb,
            "downloaded_size_mb": downloaded_size_mb,
            "repository_urls": list(set(info["url"] for info in self.MODEL_REPOSITORIES.values() if info.get("url")))
        }

# 全局模型管理器实例
model_download_manager = ModelDownloadManager()