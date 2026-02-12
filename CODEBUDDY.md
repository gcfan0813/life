# CODEBUDDY.md This file provides guidance to CodeBuddy when working with code in this repository.

## 项目架构概述

《无限人生》是一个AI推演人生模拟系统，采用AI推演+规则约束混合引擎架构。系统分为本地客户端和平台服务两大模块，核心设计理念是离线优先、用户主权。

### 核心架构组件

1. **本地客户端（离线优先）**
   - 时光卷轴界面：基于React的交互界面
   - 核心推演引擎：AI推演 + 规则校验混合引擎
   - 存储引擎：SQLite + 事件溯源架构
   - 本地AI模型：分层部署的量化模型（1.5B/3B/7B）

2. **平台服务（云端增强）**
   - 免费API网关：零配置AI服务路由
   - 规则库仓库：增量更新机制
   - 加密云存储：端到端加密备份

### 五维耦合系统

系统包含五个维度的动态交互：
- 生理系统：健康、精力、外貌
- 心理系统：大五人格、情绪、韧性
- 社会系统：社会资本、职业、经济
- 认知系统：知识、技能、记忆
- 关系系统：亲密度、网络效应

## 开发命令

### 前端开发
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 运行测试
npm test
```

### 后端开发
```bash
# 安装Python依赖
pip install -r requirements.txt

# 运行本地规则引擎测试
python -m tests.rule_engine

# 启动AI推演服务
python -m server.ai_service

# 数据库迁移
python -m scripts.migrate_db
```

### 移动端开发
```bash
# Android开发
npm run android

# iOS开发
npm run ios

# 构建移动端
npm run build:mobile
```

## 核心开发流程

### 添加新规则
1. 在 `shared/rules/` 目录下创建JSON规则文件
2. 规则必须包含学术依据和验证数据
3. 运行 `python -m scripts.validate_rules` 验证规则合规性
4. 更新规则清单 `shared/rules/manifest.json`

### AI推演引擎开发
- 事件生成使用 `core/ai/generator.py`
- 规则校验使用 `core/engine/validator.py`
- 状态更新使用 `core/engine/state_manager.py`

### 存储引擎开发
- 采用事件溯源架构，避免全量快照
- 数据库操作使用 `core/storage/database.py`
- 增量检查点策略在 `core/storage/checkpoint.py`

## 重要配置文件

- `package.json` - 前端依赖和脚本
- `requirements.txt` - Python依赖
- `shared/config/` - 共享配置文件
- `shared/rules/` - 规则库（学术验证规则）

## 测试策略

- 单元测试：核心引擎和规则逻辑
- 集成测试：AI推演完整流程
- 性能测试：存储引擎和渲染性能
- 设备兼容性测试：五档DPS设备分级