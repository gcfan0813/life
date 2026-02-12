"""
模型性能基准测试和预热模块
"""

import time
import statistics
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class BenchmarkResult:
    """基准测试结果"""
    model_name: str
    model_size: str
    load_time: float
    first_token_time: float
    avg_token_time: float
    tokens_per_second: float
    memory_usage_mb: float
    test_prompt: str
    test_output_length: int
    success: bool
    error_msg: Optional[str] = None

class ModelBenchmark:
    """模型性能基准测试"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.results = []
    
    def warm_up_model(self, model_config=None, warm_up_iterations: int = 3) -> bool:
        """预热模型"""
        print("[Benchmark] 开始模型预热...")
        
        try:
            # 确保模型已加载
            if not self.model_manager.load_model(
                model_size=model_config.size if model_config else None,
                model_name=model_config.name if model_config else None
            ):
                print("[Benchmark] 模型加载失败，无法预热")
                return False
            
            # 执行几次空生成来预热
            warm_up_prompts = [
                "你好",
                "1+1等于几",
                "今天天气怎么样"
            ]
            
            for i in range(warm_up_iterations):
                prompt = warm_up_prompts[i % len(warm_up_prompts)]
                result = self.model_manager.generate(
                    prompt=prompt,
                    max_tokens=50,
                    temperature=0.7
                )
                
                if result["success"]:
                    print(f"[Benchmark] 预热迭代 {i+1}/{warm_up_iterations} 完成")
                else:
                    print(f"[Benchmark] 预热迭代 {i+1} 失败: {result.get('error')}")
                
                time.sleep(0.5)  # 短暂休息
            
            print("[Benchmark] 模型预热完成")
            return True
            
        except Exception as e:
            print(f"[Benchmark] 预热过程出错: {e}")
            return False
    
    def benchmark_model(self, 
                       model_config=None,
                       test_prompts: Optional[List[str]] = None,
                       iterations: int = 3) -> BenchmarkResult:
        """对模型进行基准测试"""
        print(f"[Benchmark] 开始基准测试: {model_config.name if model_config else '推荐模型'}")
        
        result = BenchmarkResult(
            model_name=model_config.name if model_config else "unknown",
            model_size=model_config.size.value if model_config else "unknown",
            load_time=0,
            first_token_time=0,
            avg_token_time=0,
            tokens_per_second=0,
            memory_usage_mb=0,
            test_prompt="",
            test_output_length=0,
            success=False
        )
        
        try:
            # 记录加载时间
            load_start = time.time()
            if not self.model_manager.load_model(
                model_size=model_config.size if model_config else None,
                model_name=model_config.name if model_config else None
            ):
                result.error_msg = "模型加载失败"
                return result
            
            result.load_time = time.time() - load_start
            
            # 获取内存使用情况
            try:
                import psutil
                process = psutil.Process()
                result.memory_usage_mb = process.memory_info().rss / 1024 / 1024
            except:
                pass
            
            # 预热模型
            self.warm_up_model(model_config, warm_up_iterations=1)
            
            # 测试提示词
            if not test_prompts:
                test_prompts = [
                    "请简单介绍一下人工智能的发展历程",
                    "写一首关于春天的短诗",
                    "解释一下量子计算的基本原理"
                ]
            
            load_times = []
            token_times = []
            token_counts = []
            
            for i, prompt in enumerate(test_prompts[:iterations]):
                print(f"[Benchmark] 测试 {i+1}/{min(len(test_prompts), iterations)}: {prompt[:30]}...")
                
                # 测试加载时间（第二次应该更快）
                gen_start = time.time()
                
                gen_result = self.model_manager.generate(
                    prompt=prompt,
                    max_tokens=100,
                    temperature=0.7
                )
                
                if not gen_result["success"]:
                    result.error_msg = gen_result.get("error", "生成失败")
                    return result
                
                total_time = time.time() - gen_start
                load_times.append(total_time)
                
                # 估算token数量和速度
                output_text = gen_result["text"]
                token_count = len(output_text.split())  # 简单估算
                token_counts.append(token_count)
                
                if token_count > 0:
                    token_time = total_time / token_count
                    token_times.append(token_time)
                
                # 记录第一个测试的详细信息
                if i == 0:
                    result.test_prompt = prompt
                    result.test_output_length = len(output_text)
            
            # 计算结果
            if load_times:
                result.first_token_time = load_times[0]  # 第一次生成的完整时间
                result.avg_token_time = statistics.mean(token_times) if token_times else 0
                result.tokens_per_second = 1 / result.avg_token_time if result.avg_token_time > 0 else 0
            
            result.success = True
            print(f"[Benchmark] 测试完成 - 加载时间: {result.load_time:.2f}s, 速度: {result.tokens_per_second:.1f} tokens/s")
            
        except Exception as e:
            result.error_msg = str(e)
            print(f"[Benchmark] 基准测试失败: {e}")
        
        self.results.append(result)
        return result
    
    def benchmark_all_models(self, iterations: int = 2) -> List[BenchmarkResult]:
        """测试所有可用模型"""
        print("[Benchmark] 开始测试所有可用模型...")
        
        all_results = []
        available_models = self.model_manager.get_available_models()
        
        for model_info in available_models:
            if not model_info["available"]:
                print(f"[Benchmark] 跳过不可用模型: {model_info['name']}")
                continue
            
            # 查找对应的ModelConfig
            model_config = None
            for configs in self.model_manager.model_configs.values():
                for config in configs:
                    if config.name == model_info["name"]:
                        model_config = config
                        break
                if model_config:
                    break
            
            if model_config:
                result = self.benchmark_model(model_config, iterations=iterations)
                all_results.append(result)
        
        return all_results
    
    def get_best_model_for_speed(self) -> Optional[BenchmarkResult]:
        """获取速度最快的模型"""
        successful_results = [r for r in self.results if r.success]
        if not successful_results:
            return None
        
        return max(successful_results, key=lambda x: x.tokens_per_second)
    
    def get_best_model_for_quality(self) -> Optional[BenchmarkResult]:
        """获取质量最好的模型（基于quality_score和性能平衡）"""
        # 这里可以根据具体需求定义质量评估标准
        # 目前简单返回综合表现最好的
        successful_results = [r for r in self.results if r.success]
        if not successful_results:
            return None
        
        # 综合考虑质量和性能
        def score(result):
            quality = 70  # 默认质量分数，实际应该从model_config获取
            perf_score = min(result.tokens_per_second / 20, 1.0)  # 标准化性能分数
            return quality * 0.6 + perf_score * 40
        
        return max(successful_results, key=score)
    
    def save_results(self, filepath: str = "model_benchmark_results.json"):
        """保存基准测试结果"""
        try:
            results_data = [asdict(r) for r in self.results]
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results_data, f, ensure_ascii=False, indent=2)
            print(f"[Benchmark] 结果已保存到 {filepath}")
        except Exception as e:
            print(f"[Benchmark] 保存结果失败: {e}")
    
    def print_summary(self):
        """打印测试摘要"""
        if not self.results:
            print("[Benchmark] 没有测试结果")
            return
        
        print("\n" + "="*60)
        print("模型基准测试摘要")
        print("="*60)
        
        successful = [r for r in self.results if r.success]
        failed = [r for r in self.results if not r.success]
        
        print(f"总测试数: {len(self.results)}")
        print(f"成功: {len(successful)}, 失败: {len(failed)}")
        
        if successful:
            print("\n成功模型:")
            for result in successful:
                print(f"  • {result.model_name} ({result.model_size})")
                print(f"    加载时间: {result.load_time:.2f}s")
                print(f"    生成速度: {result.tokens_per_second:.1f} tokens/s")
                print(f"    内存使用: {result.memory_usage_mb:.1f}MB")
                print()
            
            best_speed = self.get_best_model_for_speed()
            best_quality = self.get_best_model_for_quality()
            
            if best_speed:
                print(f"🏆 最快模型: {best_speed.model_name} ({best_speed.tokens_per_second:.1f} tokens/s)")
            if best_quality:
                print(f"🎯 推荐模型: {best_quality.model_name}")
        
        if failed:
            print("\n失败模型:")
            for result in failed:
                print(f"  • {result.model_name}: {result.error_msg}")

# 全局基准测试实例
model_benchmark = ModelBenchmark(None)  # 将在初始化时设置