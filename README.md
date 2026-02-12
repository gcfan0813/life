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

- **前端**：React + TypeScript + TailwindCSS
- **后端**：Python + SQLite + WASM规则引擎
- **AI**：本地量化模型 + 免费公共API网关
- **移动端**：React Native

## 快速开始

```bash
# 安装依赖
npm install
pip install -r requirements.txt

# 启动开发服务器
npm run dev

# 构建项目
npm run build
```

## 项目结构

```
life/
├── client/           # 前端客户端
├── server/           # 后端服务
├── shared/           # 共享代码
├── docs/             # 文档
└── tests/            # 测试
```