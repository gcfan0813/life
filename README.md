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

### Python环境
```bash
# 安装Python依赖
pip install -r requirements.txt

# 运行AI推演测试
python -m core.ai.generator

# 运行规则引擎测试
python -m core.engine.validator
```

## 📁 项目结构

```
life/
├── src/                    # 前端源码
│   ├── components/         # React组件
│   │   ├── App.tsx        # 主应用组件
│   │   ├── LifeTimeline.tsx # 时间轴组件
│   │   ├── CharacterCreation.tsx # 角色创建
│   │   ├── EventCard.tsx   # 事件卡片
│   │   ├── Navigation.tsx  # 导航栏
│   │   ├── Settings.tsx    # 设置面板
│   │   ├── StatusPanel.tsx # 状态面板
│   │   └── TimeControls.tsx # 时间控制
│   ├── stores/            # 状态管理
│   │   └── lifeStore.ts   # 全局状态
│   ├── App.tsx           # 主应用入口
│   └── main.tsx          # 应用启动
├── shared/                # 共享代码
│   └── types.ts          # TypeScript类型定义
├── core/                  # 核心引擎
│   ├── ai/               # AI推演引擎
│   │   └── generator.py  # 事件生成器
│   ├── engine/           # 规则引擎
│   │   └── validator.py  # 规则校验器
│   └── storage/          # 存储引擎
│       └── database.py   # 数据库操作
├── 配置文件
│   ├── package.json      # 前端依赖配置
│   ├── tsconfig.json     # TypeScript配置
│   ├── vite.config.ts    # Vite构建配置
│   ├── tailwind.config.js # TailwindCSS配置
│   └── .eslintrc.json    # ESLint规范
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

🔄 **进行中**
- 开发服务器测试与优化
- 核心引擎功能完善

📋 **待完成**
- 事件溯源存储引擎
- 规则校验引擎
- AI推演逻辑实现
- 移动端适配

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

## 🤝 贡献指南

欢迎贡献代码！请遵循以下规范：
1. 使用TypeScript确保类型安全
2. 遵循ESLint代码规范
3. 提交前运行测试
4. 更新相关文档

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。