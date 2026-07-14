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

当前处于 **Phase 6 — 自动化运行**（定时采集、Pipeline 调度、任务记录）。

### 自动化服务

`docker compose up` 会启动 `worker` 容器，按配置定时执行：

| 任务 | 默认间隔 | 说明 |
|------|----------|------|
| Crawl | 60 分钟 | 采集全部数据源（HN / GitHub / RSS / Product Hunt） |
| Full Pipeline | 120 分钟 | 采集 → 分析 → 生成机会 |

### 数据源 API

```bash
# 查看已启用/可用的采集源
curl "http://localhost:8000/api/crawl/sources"

# 采集全部数据源
curl -X POST "http://localhost:8000/api/crawl/all?limit=20"

# 单独采集某一来源
curl -X POST "http://localhost:8000/api/crawl/github?limit=10"
curl -X POST "http://localhost:8000/api/crawl/rss?limit=10"
curl -X POST "http://localhost:8000/api/crawl/producthunt?limit=10"
curl -X POST "http://localhost:8000/api/crawl/hackernews?limit=10"
```

### Pipeline API

```bash
# 查看调度状态与最近任务
curl "http://localhost:8000/api/pipeline/status"

# 手动触发完整 Pipeline
curl -X POST "http://localhost:8000/api/pipeline/run"
```

下一阶段：**Phase 7 — 商业验证**。

## License

待定
