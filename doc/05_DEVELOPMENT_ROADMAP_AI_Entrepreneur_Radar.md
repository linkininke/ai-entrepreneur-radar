# AI Entrepreneur Radar
# 开发路线图与 Sprint 任务拆解文档

版本：

V1.0


---

# 1. 开发目标


本项目目标：

使用 AI Native 开发方式，在最短时间内完成：

一个可以运行的 AI 创业情报系统 MVP。


MVP必须证明：

1. 能自动获取真实世界信息。

2. 能使用AI分析信息。

3. 能生成商业机会。

4. 能通过网页查看结果。


---

# 2. 开发原则


## 原则1：先验证价值，再完善技术。


禁止：

一开始开发复杂系统。


优先：

快速得到真实输出。


---

## 原则2：所有开发围绕核心闭环。


核心闭环：


数据输入

↓

AI分析

↓

机会生成

↓

用户阅读

↓

用户行动



---

## 原则3：每个阶段必须可运行。


不要：

连续开发几周后才测试。


要求：

每个Sprint结束：

系统可以运行。


---

# 3. 技术栈确定


## Backend


Python

FastAPI


---

## Frontend


Next.js 14

TypeScript


---

## Database


PostgreSQL


---

## Vector


pgvector


---

## Task


ARQ / Celery


---

## Deployment


Docker Compose


---

# 4. 开发阶段总览



Phase 0

项目初始化

↓

Phase 1

数据采集系统

↓

Phase 2

AI分析系统

↓

Phase 3

机会生成系统

↓

Phase 4

后端API

↓

Phase 5

前端Dashboard

↓

Phase 6

自动化运行

↓

Phase 7

商业验证



---

# Phase 0

# 项目初始化


目标：

建立工程基础。


时间：

1天。


---

任务：


## Backend


创建：

FastAPI项目。


完成：

- 项目结构
- 配置管理
- 日志


---

## Frontend


创建：

Next.js项目。


完成：

- Tailwind
- 基础Layout


---

## Infrastructure


完成：

Docker Compose。


包含：

- PostgreSQL
- Backend
- Frontend


---

验收：

执行：


docker compose up


项目正常启动。


---

# Phase 1

# 数据采集系统


目标：

获取真实世界信息。


时间：

2-3天。


---

实现：

## RSS Collector


功能：

读取RSS。


保存：

文章。


---

## Hacker News Collector


获取：

- title
- url
- score
- comments


---

## GitHub Collector


获取：

- repo
- stars
- description


---

数据库：

创建：

information表。


---

验收：

数据库存在：

1000条真实信息。


---

# Phase 2

# AI分析系统


目标：

让AI理解信息。


时间：

2-3天。


---

实现：


## LLM Service


统一封装。


支持：

Claude

OpenAI


---

## Information Agent


功能：

新闻

↓

结构化事件。


---

输出：

JSON。


---

验收：

输入新闻。


输出：

结构化分析。


---

# Phase 3

# 创业机会生成系统


目标：

从趋势产生商业机会。


时间：

3-5天。


---

实现：

## Trend Agent


功能：

发现趋势。


---

## Opportunity Agent


功能：

生成：

- 用户
- 痛点
- MVP
- 定价


---

## Evaluation Agent


功能：

评分。


---

验收：


每天自动生成：

10个创业机会。


---

# Phase 4

# 后端API


目标：

提供产品接口。


时间：

2天。


---

实现：


API:



GET /information

GET /trends

GET /opportunities

GET /search



---

要求：

- 参数验证
- 错误处理
- 文档


---

验收：

接口可访问。


---

# Phase 5

# 前端Dashboard


目标：

让用户查看结果。


时间：

3-5天。


---

页面：


## 首页


展示：

今日机会。


---

## Opportunity列表


卡片：

包含：

标题

行业

痛点

评分


---

## Detail页面


展示：

完整AI分析。


---

验收：

用户可以浏览完整流程。


---

# Phase 6

# 自动化运行


目标：

无人值守。


时间：

2天。


---

实现：


Scheduler。


每天：

自动执行：



抓取

↓

分析

↓

生成机会



---

增加：

日志。


失败重试。


---

验收：

连续运行7天。


---

# Phase 7

# 商业验证


目标：

不是完善产品。


而是寻找价值。


---

任务：


## 找10个目标用户


例如：

- 独立开发者
- 创业者
- 产品经理


---

## 收集反馈


问题：

是否有用？

愿不愿付费？


---

## 验证收费


尝试：

会员

咨询

报告服务


---

# 5. MVP停止标准


满足以下：

停止开发。


不要继续加功能。


标准：


✅ 有数据输入


✅ 有AI分析


✅ 有机会输出


✅ 有用户访问


✅ 有反馈


---

# 6. 后续商业版本


## V2


增加：

用户系统

个性推荐

收藏


---

## V3


增加：

商业数据库。


例如：

公司。

融资。

竞品。


---

## V4


增加：

AI创业顾问。


---

# 7. AI Coding协作规则


给Cursor的要求：


每次开发前：

必须：

1.
说明设计。


2.
说明修改文件。


3.
解释原因。


4.
再生成代码。


禁止：

直接生成大量未知代码。


---

# 8. Git策略


每完成一个阶段：

提交：


git commit


格式：


feat:
完成RSS采集模块

feat:
完成AI分析Agent



---

# 9. 项目最终目标


不是创建一个新闻工具。


而是创建：

个人创业者AI操作系统。


长期目标：

让一个人拥有：

投资研究团队的信息处理能力。
