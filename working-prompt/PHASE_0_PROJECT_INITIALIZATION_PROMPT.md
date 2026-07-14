# AI Entrepreneur Radar
# Phase 0 项目初始化任务

你的身份：

你是本项目的 Senior Full Stack Engineer。

当前任务：

完成 AI Entrepreneur Radar 项目的 Phase 0 初始化。

注意：

现在不要开发业务功能。

目标只是建立一个稳定、可扩展、符合后续开发要求的工程基础。


---

# 1. 项目背景


AI Entrepreneur Radar 是一个 AI Native 创业情报系统。


目标：

从全球科技信息中：

采集数据

↓

AI分析

↓

发现趋势

↓

生成创业机会。


当前阶段：

MVP开发。


完整项目设计已经存在：

- PRD
- System Design
- Database Design
- AI Agent Design
- Development Roadmap
- Coding Rules
- Business Validation
- Founder Operating System


请严格遵守这些设计。


---

# 2. Phase 0目标


完成以下内容：


## Backend 初始化


创建：

FastAPI后端项目。


要求：

- Python 3.12+
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic


---

## Frontend 初始化


创建：

Next.js项目。


要求：

- Next.js 14+
- TypeScript
- Tailwind CSS


---

## Database 初始化


使用：

PostgreSQL。


通过：

Docker Compose运行。


---

## 基础工程能力


完成：

- 环境变量管理
- Docker配置
- 日志系统
- 项目目录结构
- README


---

# 3. 项目目录设计


最终目标：


ai-entrepreneur-radar/

├── backend/

│
├── frontend/

│
├── docker-compose.yml

│
├── .env.example

│
├── README.md

│
└── docs/



---

# 4. Backend要求


目录：


backend/

app/

├── main.py

├── api/

├── core/

├── models/

├── schemas/

├── services/

├── workers/

└── database/



---

## main.py


要求：

启动FastAPI。


提供：

健康检查接口。


例如：


GET /health


返回：


```json
{
"status":"ok"
}

5. Database要求

docker-compose启动：

PostgreSQL。

配置：

数据库名：

ai_radar

用户：

ai_radar

密码：

通过环境变量。

6. Frontend要求

创建基础页面。

首页显示：


AI Entrepreneur Radar


System initialized successfully.


7. Docker要求

创建：

docker-compose.yml

包含：

service:

postgres

backend

frontend

要求：

一次启动：

docker compose up

可以运行。

8. Environment要求

创建：

.env.example

包含：


DATABASE_URL=

LLM_API_KEY=

APP_ENV=


禁止：

真实Key写入代码。

9. Logging要求

添加基础日志。

要求：

未来方便调试：

Crawler

AI Agent

API

10. Code Quality要求

必须：

类型提示
清晰目录
模块化
README说明

禁止：

生成大量无意义代码。

11. 开发流程要求

开始编码前：

先输出：

Step 1

你的实施计划。

包括：

创建哪些文件
为什么这样设计
技术选择
Step 2

执行初始化。

Step 3

运行测试。

验证：

docker启动成功。

backend启动成功。

frontend启动成功。

health接口正常。

12. 不允许做的事情

当前阶段禁止：

❌ 开发爬虫

❌ 接入LLM

❌ 开发Agent

❌ 开发用户系统

❌ 开发复杂UI

❌ 添加微服务

❌ 过度设计

13. 完成标准

Phase 0完成必须满足：

✅ 项目可以clone运行

✅ Docker可以启动全部服务

✅ FastAPI健康检查正常

✅ Next.js页面正常访问

✅ PostgreSQL连接正常

✅ README完整

14. 完成后输出报告

完成后，请输出：

项目结构。

创建文件列表。

启动方法。

测试结果。

下一阶段建议。