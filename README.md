# AI Entrepreneur Radar（AI 嗅探雷达）

AI Native 创业情报系统 — 帮助个人创业者从信息过载中识别真实创业机会。

## 项目简介

在 AI 成为新生产力基础设施的时代，创业机会快速涌现，但创业者面临的核心问题不是缺少信息，而是**信息过载**与**信号识别困难**。

AI Entrepreneur Radar 旨在构建一套智能化的创业情报系统，通过多源数据采集、AI 分析与结构化输出，帮助创业者更快发现、评估和跟踪有价值的创业信号。

## 技术栈

| 层级 | 技术 |
|------|------|
| Backend | Python 3.12, FastAPI, SQLAlchemy, Alembic |
| Frontend | Next.js 14, TypeScript, Tailwind CSS |
| Database | PostgreSQL 16 |
| Infrastructure | Docker Compose |

## 项目结构

```
ai-entrepreneur-radar/
├── backend/              # FastAPI 后端
│   └── app/
│       ├── api/          # API 路由
│       ├── core/         # 配置与日志
│       ├── database/     # 数据库连接
│       ├── models/       # 数据模型（Phase 1+）
│       ├── schemas/      # Pydantic 模式
│       ├── services/     # 业务逻辑
│       └── workers/      # 后台任务
├── frontend/             # Next.js 前端
├── docs/                 # 项目设计文档
├── docker-compose.yml    # 容器编排
├── .env.example          # 环境变量模板
└── README.md
```

## 快速启动

### 前置条件

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)（已安装并运行）
- Git

### 启动步骤

```bash
# 1. 克隆仓库
git clone https://github.com/linkininke/ai-entrepreneur-radar.git
cd ai-entrepreneur-radar

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，至少修改 POSTGRES_PASSWORD

# 3. 一键启动全部服务
docker compose up --build
```

### 验证

| 服务 | 地址 | 预期结果 |
|------|------|----------|
| Frontend | http://localhost:3000 | 显示 "AI Entrepreneur Radar" 与 "System initialized successfully." |
| Backend Health | http://localhost:8000/health | `{"status":"ok","database":"ok"}` |
| PostgreSQL | localhost:5433 | backend health 中 database 为 ok |

### 停止服务

```bash
docker compose down
```

## 文档

| 文档 | 说明 |
|------|------|
| [产品需求文档 PRD](docs/01_PRD_AI_Entrepreneur_Radar.md) | 产品背景、目标用户、核心功能 |
| [系统设计 SDD](docs/02_SDD_AI_Entrepreneur_Radar_System_Design.md) | 系统架构与技术方案 |
| [数据库设计](docs/03_DB_AI_Entrepreneur_Radar_Database_Design.md) | 数据模型与存储设计 |
| [AI Agent 设计](docs/04_AI_Agent_Design_AI_Entrepreneur_Radar.md) | Agent 工作流与提示工程 |
| [开发路线图](docs/05_DEVELOPMENT_ROADMAP_AI_Entrepreneur_Radar.md) | 分阶段开发计划 |
| [Cursor AI 编码规范](docs/06_CURSOR_AI_CODING_RULES.md) | AI 辅助开发规范 |
| [商业验证](docs/07_BUSINESS_VALIDATION_AI_Entrepreneur_Radar.md) | 商业模式与市场验证 |
| [创始人操作系统](docs/08_FOUNDER_OPERATING_SYSTEM_AI_Entrepreneur_Radar.md) | 创始人运营框架 |

## 开发阶段

当前处于 **Phase 3 — 机会生成系统**（已从 AI 分析生成创业机会）。

### API 快速测试

```bash
# 1. 采集 Hacker News Top Stories
curl -X POST "http://localhost:8000/api/crawl/hackernews?limit=10"

# 2. 批量 AI 分析（需配置 LLM_API_KEY）
curl -X POST "http://localhost:8000/api/analyze/batch?limit=5"

# 3. 批量生成创业机会
curl -X POST "http://localhost:8000/api/opportunities/generate/batch?limit=5"

# 4. 查看机会列表
curl "http://localhost:8000/api/opportunities?limit=10"
```

下一阶段：**Phase 4 — 后端 API 完善**。

## License

待定
