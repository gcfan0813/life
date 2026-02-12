"""
《无限人生：AI编年史》演示脚本
展示项目的核心功能
"""

import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from core.engine.character import character_initializer, LifeProfile
from core.engine.simulation import simulation_engine
from core.storage.database import db_manager

class DemoSimulation:
    """演示模拟系统"""
    
    def __init__(self):
        self.profiles = []
        self.current_state = None
    
    async def setup_demo(self):
        """设置演示环境"""
        print(">>> 设置《无限人生：AI编年史》演示环境")
        print("=" * 60)
        
        # 创建演示角色
        demo_profile = LifeProfile(
            id="demo_profile_001",
            name="李明",
            birth_date="1990-06-15",
            birth_place="上海",
            gender="male",
            initial_traits={
                "familyBackground": "middle",
                "educationLevel": "college", 
                "healthStatus": "good",
                "riskTolerance": 65,
                "ambition": 75,
                "empathy": 60
            },
            era="现代中国",
            difficulty="normal",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        print(f"[INFO] 创建演示角色: {demo_profile.name}")
        print(f"   出生日期: {demo_profile.birth_date}")
        print(f"   出生地点: {demo_profile.birth_place}")
        print(f"   初始特质: {demo_profile.initial_traits}")
        
        # 初始化角色状态
        self.current_state = await character_initializer.initialize_character_state(demo_profile)
        
        print("[OK] 角色初始化完成")
        print(f"   年龄: {self.current_state.age}岁")
        print(f"   人生阶段: {self.current_state.life_stage}")
        print(f"   健康值: {self.current_state.dimensions['physiological']['health']}")
        print(f"   幸福感: {self.current_state.dimensions['psychological']['happiness']}")
        
        return demo_profile
    
    async def run_life_simulation(self, profile, years: int = 5):
        """运行人生模拟"""
        print(f"\n[START] 开始模拟 {years} 年人生历程")
        print("-" * 40)
        
        total_days = years * 365
        current_year = 0
        
        for year in range(1, years + 1):
            print(f"\n[YEAR] 第 {year} 年模拟 (年龄: {self.current_state.age:.1f}岁)")
            
            # 每年推进365天
            result = await simulation_engine.advance_time(profile.id, self.current_state, 365)
            self.current_state = result.new_state
            
            print(f"   生成事件: {len(result.new_events)} 个")
            print(f"   生成记忆: {len(result.new_memories)} 个")
            
            # 显示重要事件
            for i, event in enumerate(result.new_events[:2]):  # 只显示前2个事件
                print(f"   [EVENT] 事件{i+1}: {event.title}")
                print(f"      描述: {event.description}")
                print(f"      可信度: {event.plausibility}%")
                
                # 如果有选择，显示选择项
                if hasattr(event, 'choices') and event.choices:
                    print(f"      选择项: {len(event.choices)} 个")
            
            # 显示状态变化
            health = self.current_state.dimensions['physiological']['health']
            happiness = self.current_state.dimensions['psychological']['happiness']
            career_level = self.current_state.dimensions['social']['career']['level']
            
            print(f"   状态变化:")
            print(f"     健康: {health:.1f} | 幸福: {happiness:.1f} | 职业: {career_level:.1f}")
    
    async def demo_decision_making(self, profile):
        """演示决策过程"""
        print("\n[DECISION] 演示决策过程")
        print("-" * 30)
        
        # 推进30天生成一些事件
        result = await simulation_engine.advance_time(profile.id, self.current_state, 30)
        
        if result.new_events:
            # 获取第一个事件
            event = result.new_events[0]
            print(f"[EVENT] 面临事件: {event.title}")
            print(f"   描述: {event.description}")
            
            if hasattr(event, 'choices') and event.choices:
                print("\n[CHOICES] 可选决策:")
                for i, choice in enumerate(event.choices):
                    print(f"   {i+1}. {choice['text']}")
                    
                    # 显示影响
                    impacts = choice.get('immediateImpacts', [])
                    if impacts:
                        for impact in impacts:
                            dim = impact.get('dimension', '')
                            sub = impact.get('subDimension', '')
                            change = impact.get('change', 0)
                            print(f"      影响: {dim}.{sub} {'+' if change > 0 else ''}{change}")
                
                # 模拟选择第一个选项
                print("\n[OK] 选择第1个选项")
                decision_result = await simulation_engine.process_decision(
                    profile.id, self.current_state, event.id, 0
                )
                
                print(f"   决策总数: {self.current_state.total_decisions}")
                print(f"   即时影响: {len(decision_result.immediate_effects)} 个")
    
    def show_final_summary(self, profile):
        """显示最终总结"""
        print("\n[SUMMARY] 模拟总结")
        print("=" * 50)
        
        print(f"[CHARACTER] 角色信息:")
        print(f"   姓名: {profile.name}")
        print(f"   年龄: {self.current_state.age:.1f}岁")
        print(f"   人生阶段: {self.current_state.life_stage}")
        print(f"   存活天数: {self.current_state.days_survived}")
        
        print(f"\n[STATS] 最终状态:")
        dims = self.current_state.dimensions
        print(f"   生理健康: {dims['physiological']['health']:.1f}")
        print(f"   心理幸福: {dims['psychological']['happiness']:.1f}")
        print(f"   职业等级: {dims['social']['career']['level']:.1f}")
        print(f"   知识水平: {dims['cognitive']['knowledge']['academic']:.1f}")
        print(f"   家庭关系: {dims['relational']['intimacy']['family']:.1f}")
        
        print(f"\n[ACHIEVEMENTS] 成就统计:")
        print(f"   总事件数: {self.current_state.total_events}")
        print(f"   总决策数: {self.current_state.total_decisions}")
        print(f"   人生阶段: {self.current_state.life_stage}")

async def main():
    """主演示函数"""
    demo = DemoSimulation()
    
    try:
        # 1. 设置演示环境
        profile = await demo.setup_demo()
        
        # 2. 运行5年人生模拟
        await demo.run_life_simulation(profile, years=5)
        
        # 3. 演示决策过程
        await demo.demo_decision_making(profile)
        
        # 4. 显示最终总结
        demo.show_final_summary(profile)
        
        print("\n[DONE] 演示完成！")
        print("《无限人生：AI编年史》核心功能已成功展示")
        
    except Exception as e:
        print(f"\n[ERROR] 演示过程中出现错误: {e}")
        print("请检查系统配置和依赖项")

if __name__ == "__main__":
    # 运行演示
    asyncio.run(main())