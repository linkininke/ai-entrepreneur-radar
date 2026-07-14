# AI Entrepreneur Radar
# 系统架构设计文档 SDD

版本：
V1.0

项目类型：
AI Native SaaS / Personal Intelligence System


---

# 1. 文档目的


本文档定义：

AI Entrepreneur Radar 系统的软件架构。


目标：

指导 AI Coding Agent 和工程团队构建一个：

- 可维护
- 可扩展
- AI Native
- 支持未来商业化

的软件系统。


---

# 2. 架构设计原则


## 原则1：模块化


系统必须采用模块化设计。


禁止：

所有逻辑写在单个文件。


要求：

不同职责独立。


---

## 原则2：数据驱动


系统核心资产：

不是代码。

而是：

信息数据。

趋势数据。

机会数据。

用户反馈数据。


---

## 原则3：AI作为核心服务


AI不是外挂功能。


AI应该参与：

- 信息理解
- 趋势发现
- 商业分析
- 推荐决策


---

## 原则4：快速迭代


第一版本：

优先验证价值。


不要过度工程。


---

# 3. 总体系统架构


系统采用：

前后端分离架构。


整体：

             外部数据源

    ┌────────────────────┐
    │ RSS                │
    │ Hacker News        │
    │ GitHub API         │
    │ Product Hunt       │
    │ arXiv              │
    │ Reddit             │
    └─────────┬──────────┘


              ↓


    Data Collection Layer

    数据采集层


              ↓


    Data Processing Layer

    数据处理层


              ↓


    AI Intelligence Layer

    AI智能分析层


              ↓


    Knowledge Storage Layer

    知识存储层


              ↓


    Application Layer

    应用服务层


              ↓


    Frontend Dashboard

    用户界面层


---

# 4. 技术架构


## Frontend


技术：

Next.js 14

TypeScript

Tailwind CSS


职责：

- Dashboard
- 数据展示
- 用户交互


---

## Backend


技术：

Python FastAPI


职责：

- API服务
- 业务逻辑
- AI调用
- 数据处理


---

## Database


技术：

PostgreSQL


原因：

成熟。

支持复杂关系。


---

## Vector Database


技术：

pgvector


用途：

存储：

文本Embedding。


支持：

语义搜索。


---

## Task Queue


技术：

ARQ 或 Celery


用途：

后台任务。


例如：

每日抓取。

AI分析。


---

## Deployment


技术：

Docker Compose


要求：

一键启动。


---

# 5. 系统模块设计


系统拆分：


backend

├── api

├── core

├── models

├── schemas

├── services

│
├── crawler

│
├── ai

│
├── analysis

│
├── recommendation

│
└── workers



---

# 6. 数据采集模块


## Data Collector


职责：

从外部获取信息。


支持：

RSS

API

网页解析


---

## 数据来源


第一阶段：

### Hacker News


获取：

- title
- url
- score
- comments


---

### GitHub


获取：

- repository
- stars
- language
- description


---

### Product Hunt


获取：

- product name
- description
- category


---

### RSS


支持动态配置。


例如：

科技媒体。

AI博客。


---

# 7. 数据处理模块


职责：

原始数据转换。


流程：


Raw Data

↓

Cleaning

↓

Deduplication

↓

Classification

↓

Embedding

↓

Storage



---

# 8. AI Intelligence Layer


核心。


包含：

多个AI Agent。


---

## Agent 1

Information Analyzer


输入：

新闻。


输出：

结构化信息。


例如：


事件：

OpenAI发布新模型

影响：

软件开发效率提升

涉及行业：

开发工具



---

## Agent 2

Trend Discovery Agent


输入：

大量信息。


输出：

趋势。


例如：


趋势：

AI Agent企业化

原因：

模型能力提升

影响：

企业软件重新设计



---

## Agent 3

Opportunity Generator


输入：

趋势。


输出：

创业机会。


格式：


目标用户：

问题：

解决方案：

MVP：

收费：



---

## Agent 4

Opportunity Evaluator


评分：

0-100。


维度：

市场规模

付费能力

竞争

技术难度

个人匹配度


---

# 9. API设计


## 信息接口


GET:


/api/information



返回：

信息列表。


---

## 趋势接口


GET:


/api/trends



返回：

趋势分析。


---

## 机会接口


GET:


/api/opportunities



返回：

创业机会。


---

## 搜索接口


GET:


/api/search



支持：

关键词。

语义搜索。


---

# 10. 前端架构


页面：


## Dashboard


展示：

今日趋势。


---

## Opportunity Page


展示：

机会列表。


每个Card：


标题

行业

用户

痛点

MVP

评分


---

## Detail Page


展示：

完整AI分析。


---

# 11. 数据流设计


每日任务：



Scheduler

↓

Collector Worker

↓

获取信息

↓

数据库

↓

Analyzer Worker

↓

LLM分析

↓

生成趋势

↓

Opportunity Agent

↓

生成机会

↓

Dashboard展示



---

# 12. 扩展设计


未来支持：


## 更多数据源


增加：

- 小红书
- 抖音
- 微信公众号
- Amazon Reviews
- App Store Reviews


---

## 更多AI能力


增加：

- 用户画像Agent
- 市场研究Agent
- 竞争分析Agent
- 销售话术Agent


---

# 13. 工程质量要求


必须：

- 类型检查
- 单元测试
- 日志
- 错误处理
- 环境变量管理
- Docker化


---

禁止：

- 硬编码API Key
- 巨型文件
- 随意耦合


---

# 14. 开发策略


采用：

Incremental Development。


顺序：


Phase 1:

项目初始化


Phase 2:

数据库


Phase 3:

数据采集


Phase 4:

AI分析


Phase 5:

API


Phase 6:

Frontend


Phase 7:

部署



---

# 最终目标


构建：

一个个人创业者的AI信息操作系统。


它不是新闻网站。


它是：

发现商业机会的智能基础设施。