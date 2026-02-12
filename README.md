# 无限人生：AI编年史

## 项目简介

《无限人生》是一个用户主权式的AI推演人生模拟系统，基于真实世界规律约束，使用生成式AI作为核心推演引擎，让玩家在每一个生命节点自主选择决策，由AI实时推演未来的无限可能性。

## 核心特性

- **AI推演+规则约束混合引擎**：AI负责发散创造，规则负责收敛约束
- **五维耦合系统**：生理/心理/社会/认知/关系动态交互
- **离线优先架构**：核心功能完全本地运行，无需网络
- **用户数据主权**：全量本地加密存储，零网络传输
- **零成本AI**：免费公共API + 本地量化模型分层部署

## 技术栈

### 前端架构
- **框架**：React 18 + TypeScript + Vite
- **样式**：TailwindCSS + 自定义主题
- **状态管理**：Zustand（持久化存储）
- **路由**：React Router v6
- **网络请求**：React Query
- **图标**：Lucide React

### 后端核心
- **语言**：Python 3.8+
- **数据库**：SQLite + 事件溯源架构
- **AI引擎**：本地量化模型 + 免费API网关
- **规则引擎**：WASM + 学术验证规则库

### 移动端
- **框架**：React Native（开发中）

## 🚀 快速开始

### 环境要求
- Node.js 18+
- Python 3.8+
- npm 或 yarn

### 安装运行
```bash
# 安装前端依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

### Python后端环境
```bash
# 安装后端依赖
pip install -r requirements.txt

# 启动后端API服务
python backend/main.py

# 或使用uvicorn启动
cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 完整开发流程
```bash
# 终端1：启动后端API服务（端口8000）
python backend/main.py

# 终端2：启动前端开发服务器
npm run dev

# 访问应用
# 前端：http://localhost:3002/
# 后端API文档：http://localhost:8000/docs
```

### 当前系统状态
- ✅ **前端**：http://localhost:3002/ （实时重载）
- ✅ **后端**：http://localhost:8000/ （完整版API - 集成核心引擎）
- ✅ **数据库**：SQLite（自动创建和管理）
- ✅ **功能**：角色创建、事件推演、状态管理、规则校验、AI推演

### 后端API接口（端口8000 - 完整版）

#### 角色管理（集成核心引擎）
- `POST /api/profiles` - 创建新角色档案（使用CharacterInitializer）
- `GET /api/profiles` - 获取所有角色列表

#### 时间推进（集成核心引擎）
- `POST /api/profiles/{id}/advance` - 推进时间并生成事件（使用SimulationEngine）

#### 事件处理（集成核心引擎）
- `POST /api/profiles/{id}/decisions` - 处理用户决策（使用SimulationEngine）

#### 高级功能
- `GET /api/profiles/{id}/preview?days=90` - 未来预览（基于当前状态预测）
- `GET /api/profiles/{id}/timeline` - 获取事件时间线
- `GET /api/profiles/{id}/causality` - 获取完整因果链网络
- `GET /api/profiles/{id}/causality/{event_id}` - 获取单个事件因果链
- `GET /api/profiles/{id}/summary` - 人生总结（阶段评估、成就统计、人生感悟）

#### 记忆系统
- `GET /api/profiles/{id}/memories` - 获取记忆列表（艾宾浩斯留存率）
- `GET /api/profiles/{id}/memories/stats` - 记忆统计
- `POST /api/profiles/{id}/memories/{memory_id}/recall` - 回忆记忆（增强留存）

#### 规则引擎
- `GET /api/rules/stats` - 获取规则库统计信息
- `GET /api/rules/categories` - 获取规则分类
- `GET /api/rules/category/{id}` - 获取指定分类规则
- `POST /api/rules/validate-event` - 验证事件合理性
- `POST /api/rules/validate-decision` - 验证决策风险
- `GET /api/rules/validate-action` - 验证动作合理性

**学术规则分类：**
- 生理系统规则（健康、精力、外貌）
- 心理系统规则（大五人格、情绪）
- 社会系统规则（职业、经济、社交）
- 认知系统规则（知识、技能、记忆）
- 关系系统规则（亲密度、家庭）
- 年龄特定规则（童年、青年、中年、老年）

#### AI服务
- `GET /api/ai/status` - 获取AI服务状态和可用API
- `POST /api/ai/level` - 设置AI推演级别（L0-L3）
- `POST /api/ai/generate` - 使用AI生成事件

**AI推演级别：**
- L0: 本地规则引擎（免费）
- L1: 模板生成（免费）
- L2: 免费API（硅基流动、智谱等）
- L3: 高级API（更智能）

#### 宏观事件系统
- `GET /api/macro-events?year=2024` - 获取指定年份可能的宏观事件
- `GET /api/macro-events/types` - 获取宏观事件类型列表
- `POST /api/profiles/{id}/check-macro-events?year=2024` - 检查角色宏观事件
- `POST /api/profiles/{id}/trigger-macro-event?event_id=xxx` - 触发指定宏观事件

**宏观事件类型：**
- 经济事件：金融危机、贸易摩擦
- 疫情：非典、新冠
- 政策变化：改革开放、调控政策
- 科技革命：互联网、AI革命
- 自然灾害：地震、洪涝
- 社会变革：教育改革、医疗改革

#### 高敏事件处理系统
- `GET /api/sensitive-events/types` - 获取高敏事件类型列表
- `POST /api/events/check-sensitivity` - 检查事件敏感度
- `GET /api/sensitive-events/{event_id}/options` - 获取高敏事件处理选项
- `POST /api/sensitive-events/{event_id}/process` - 处理高敏事件
- `GET /api/sensitive-events/list` - 获取高敏事件列表

**处理方式：**
- 跳过（skip）：不经历这个事件
- 温和处理（soften）：降低影响，使用温和叙述
- 完整体验（full）：完整经历所有内容

**高敏事件类型：**
- 死亡相关：角色死亡、亲人离世
- 重大疾病：癌症、重大事故
- 家庭变故：离婚、家庭破裂
- 心理创伤：抑郁、绝望时刻
- 经济危机：破产、失业

#### 系统信息
- `GET /api/health` - 健康检查（显示引擎状态）
- `GET /api/data/exists` - 检查数据是否存在

### 简化版API（端口8001 - 已移除）

简化版API已被移除，统一使用完整版API（端口8000）。

### 启动问题已解决

**2026-02-12更新：**
- ✅ 修复了Python路径问题
- ✅ 修复了shared.types导入问题
- ✅ 创建了debug_main.py测试脚本
- ✅ 所有核心模块导入成功
- ✅ 可以使用start.bat启动服务

#### 请求/响应格式
```typescript
// 请求示例
interface CreateProfileRequest {
  name: string
  gender: 'male' | 'female'
  birthDate: string
  birthLocation: string
  familyBackground: string
  initialPersonality: {
    openness: number
    conscientiousness: number
    extraversion: number
    agreeableness: number
    neuroticism: number
  }
}

// 响应格式
interface APIResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
}
```

## 📁 项目结构

```
life/
├── src/                    # 前端源码
│   ├── components/        # React组件
│   │   ├── App.tsx        # 主应用组件
│   │   ├── LifeTimeline.tsx # 时间轴组件
│   │   ├── CharacterCreation.tsx # 角色创建
│   │   ├── EventCard.tsx  # 事件卡片
│   │   ├── Navigation.tsx # 导航栏
│   │   ├── Settings.tsx   # 设置面板
│   │   ├── StatusPanel.tsx # 状态面板
│   │   └── TimeControls.tsx # 时间控制
│   ├── stores/            # 状态管理
│   │   └── lifeStore.ts  # 全局状态
│   ├── services/          # API服务层
│   │   ├── api.ts        # API服务
│   │   ├── localService.ts # 本地服务
│   │   └── index.ts      # 服务导出
│   ├── App.tsx           # 主应用入口
│   └── main.tsx          # 应用启动
├── backend/               # 后端API服务
│   ├── main.py           # FastAPI应用
│   └── requirements.txt  # Python依赖
├── core/                  # 核心引擎
│   ├── ai/               # AI推演引擎
│   │   └── generator.py  # 事件生成器
│   ├── engine/           # 规则引擎
│   │   ├── validator.py  # 规则校验器
│   │   ├── simulation.py # 模拟引擎
│   │   └── character.py  # 角色初始化
│   └── storage/          # 存储引擎
│       └── database.py   # 数据库操作
├── shared/                # 共享代码
│   ├── types.ts          # TypeScript类型定义
│   └── config/           # 配置文件
│       └── api_config.py # API配置
├── 配置文件
│   ├── package.json      # 前端依赖配置
│   ├── tsconfig.json     # TypeScript配置
│   ├── vite.config.ts    # Vite构建配置
│   ├── tailwind.config.js # TailwindCSS配置
│   └── .eslintrc.json    # ESLint规范
├── 测试文件
│   ├── test_storage.py   # 存储引擎测试
│   ├── test_validator.py # 规则引擎测试
│   └── test_simulation.py # 模拟引擎测试
├── life_simulation.db     # SQLite数据库文件
└── 文档
    ├── README.md         # 项目说明
    ├── to-do.md          # 开发计划
    └── CODEBUDDY.md      # AI助手指南
```

## 🎯 当前状态

✅ **已完成**
- 前端基础架构搭建（React + TypeScript + TailwindCSS）
- 核心状态管理系统（Zustand持久化）
- 开发环境配置（Vite + ESLint）
- 核心组件开发（时间轴、角色创建、事件卡片等）
- 事件溯源存储引擎（SQLite + 事件溯源架构）
- 规则校验引擎基础框架（5类学术验证规则）
- 开发服务器测试与优化（成功运行）
- AI推演引擎核心功能（事件生成器、模拟引擎）
- 角色状态初始化系统
- 模拟引擎集成测试框架
- 五维耦合系统完整实现（生理/心理/社会/认知/关系）
- 完整的演示系统（可运行5年人生模拟）
- 决策处理系统完整实现（事件选择、影响应用）
- 数据库存储优化（JSON序列化、事件查询）
- AI事件生成器模板扩展（新增运动锻炼、恋爱关系、家庭建设等事件）
- 五维系统数值平衡优化
- 前端与后端通信集成（API服务层 + 本地服务层）
- FastAPI后端服务搭建（端口8001）
- 前后端类型定义统一
- 前端可视化界面完成（角色创建、时间轴、状态面板）
- 后端API服务测试版（简化版服务已启动）
- 前后端联调完成
- **后端API接口完善**（角色创建、时间推进、事件处理、决策记录）
- **前端与后端真实数据交互**（API调用、状态同步、错误处理）

🔄 **进行中**
- 后端服务稳定性优化
- API接口完善和测试
- 规则库扩展和优化

📋 **待完成**
- 移动端适配
- AI模型分层集成（L0-L3）
- 用户界面优化
- 高级功能实现（未来预览、因果链追溯等）

## 🔧 开发命令

```bash
# 开发模式
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview

# 运行测试
npm test

# 代码检查
npm run lint
```

## 🐛 常见问题

### Q: 前端卡在"正在加载..."页面？
**A**: 刷新浏览器（F5）或检查浏览器控制台（F12）

### Q: 后端服务启动失败？
**A**: 使用简化版服务：`cd backend && python simple_server.py`

### Q: 前端无法连接后端？
**A**: 检查端口：前端3002，后端8001，确保没有被占用

### Q: 如何重置数据？
**A**: 删除 `life_simulation.db` 文件，系统会自动重建

### Q: API返回错误怎么办？
**A**: 检查后端服务是否运行：`cd backend && python simple_server.py`

### Q: 前端显示异常？
**A**: 打开浏览器控制台（F12）查看错误信息，检查网络请求

### Q: 如何查看数据库内容？
**A**: 使用SQLite工具打开 `life_simulation.db` 文件，查看profiles和events表

## 🤝 贡献指南

欢迎贡献代码！请遵循以下规范：
1. 使用TypeScript确保类型安全
2. 遵循ESLint代码规范
3. 提交前运行测试
4. 更新相关文档

## 📞 技术支持

如遇到问题，请检查：
1. [开发文档](CODEBUDDY.md) - 项目架构和开发指南
2. [设计文档](设计文档.md) - 系统设计和实现细节
3. [待办清单](to-do.md) - 开发进度和计划

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。