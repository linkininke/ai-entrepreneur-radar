# AI Entrepreneur Radar
# 数据库设计文档 DB Design

版本：
V1.0


---

# 1. 数据库设计目标


本数据库负责存储：

1. 外部信息数据

2. AI分析结果

3. 商业趋势数据

4. 创业机会数据

5. 用户画像数据

6. 用户反馈数据


数据库不仅用于展示。

同时用于：

AI学习。

机会推荐。

商业分析。


---

# 2. 技术选择


数据库：

PostgreSQL


原因：

- 成熟稳定
- 支持复杂关系
- 支持JSON字段
- 支持pgvector


向量：

pgvector


用途：

保存：

文本Embedding。


支持：

语义搜索。


---

# 3. 数据模型总览



Source

|

↓

Information

|

↓

Analysis

|

↓

Trend

|

↓

Opportunity

|

↓

Validation



数据演进：

原始信息

↓

AI理解

↓

趋势

↓

商业机会

↓

真实反馈


---

# 4. 数据表设计


---

# Table 1

## sources

数据来源表


用途：

管理所有信息来源。


字段：

```sql
CREATE TABLE sources (

id BIGSERIAL PRIMARY KEY,


name VARCHAR(100),


type VARCHAR(50),


url TEXT,


enabled BOOLEAN DEFAULT TRUE,


created_at TIMESTAMP

);


示例：

Hacker News

RSS TechCrunch

GitHub Trending

Table 2
information

原始信息表

用途：

保存采集的数据。

字段：

CREATE TABLE information (

id BIGSERIAL PRIMARY KEY,


source_id BIGINT,


title TEXT,


content TEXT,


url TEXT,


author VARCHAR(200),


published_time TIMESTAMP,


category VARCHAR(100),


language VARCHAR(20),


embedding VECTOR,


metadata JSONB,


created_at TIMESTAMP

);


字段说明：

title：

标题。

content：

正文。

metadata：

保存额外信息。

例如：

GitHub:

{
stars:10000,
language:"Python"
}

Table 3
information_tags

信息标签。

用途：

分类。

字段：

CREATE TABLE information_tags (

id BIGSERIAL PRIMARY KEY,


information_id BIGINT,


tag VARCHAR(100)

);


例如：

AI

SaaS

Agent

Blockchain

Healthcare

Table 4
ai_analysis

AI分析结果表。

用途：

保存LLM处理结果。

字段：

CREATE TABLE ai_analysis (

id BIGSERIAL PRIMARY KEY,


information_id BIGINT,


summary TEXT,


technical_change TEXT,


business_impact TEXT,


affected_industry TEXT,


potential_customer TEXT,


created_at TIMESTAMP

);

Table 5
trends

趋势表。

用途：

保存长期趋势。

字段：

CREATE TABLE trends (

id BIGSERIAL PRIMARY KEY,


name VARCHAR(200),


description TEXT,


industry VARCHAR(100),


evidence TEXT,


trend_score INT,


created_at TIMESTAMP

);


示例：

name:

AI Agent企业化


description:

企业软件开始被Agent重新设计


industry:

Enterprise Software


score:

90

Table 6
trend_information

趋势与信息关联。

一个趋势：

可能来自：

很多新闻。

字段：

CREATE TABLE trend_information (

trend_id BIGINT,


information_id BIGINT

);

Table 7
opportunities

创业机会核心表。

这是系统最重要的数据。

字段：

CREATE TABLE opportunities (

id BIGSERIAL PRIMARY KEY,


trend_id BIGINT,


title VARCHAR(200),


problem TEXT,


customer TEXT,


solution TEXT,


mvp TEXT,


pricing TEXT,


competition TEXT,


market_size TEXT,


difficulty_score INT,


business_score INT,


personal_fit_score INT,


total_score INT,


status VARCHAR(50),


created_at TIMESTAMP

);


字段说明：

problem:

用户痛点。

customer:

目标客户。

solution:

解决方案。

mvp:

最小产品。

pricing:

收费方式。

total_score:

综合评分。

Table 8
user_profiles

用户画像。

未来个性化推荐核心。

字段：

CREATE TABLE user_profiles (

id BIGSERIAL PRIMARY KEY,


skills JSONB,


experience JSONB,


capital INT,


location VARCHAR(100),


interests JSONB,


risk_level VARCHAR(50),


created_at TIMESTAMP

);


示例：

{
skills:[
"Java",
"Python",
"AI"
],

capital:
1000,

interest:[
"SaaS",
"Automation"
]

}

Table 9
opportunity_recommendations

机会推荐。

用途：

根据用户画像推荐机会。

字段：

CREATE TABLE opportunity_recommendations (

id BIGSERIAL PRIMARY KEY,


user_id BIGINT,


opportunity_id BIGINT,


reason TEXT,


match_score INT,


created_at TIMESTAMP

);

Table 10
validation_records

商业验证记录。

非常重要。

未来形成数据壁垒。

字段：

CREATE TABLE validation_records (

id BIGSERIAL PRIMARY KEY,


opportunity_id BIGINT,


customer_feedback TEXT,


payment_status VARCHAR(50),


revenue NUMERIC,


conversion_rate FLOAT,


created_at TIMESTAMP

);

5. 向量搜索设计

information:

保存：

新闻Embedding。

trend:

保存：

趋势Embedding。

opportunity:

保存：

机会Embedding。

用途：

用户搜索：

“AI电商工具”

系统找到：

相关机会。

6. 数据生命周期

流程：


External Data


↓

information


↓

AI Analysis


↓

trend


↓

opportunity


↓

validation


↓

Feedback


↓

Improve AI


7. 索引设计

必须添加：

时间索引：

published_time


来源索引：

source_id


评分索引：

total_score


向量索引：

pgvector

8. 数据安全

要求：

API Key:

禁止存数据库。

用户数据：

隔离。

日志：

禁止记录敏感信息。

9. 未来扩展
商业数据库

增加：

公司表。

记录：

创业公司。

融资。

产品。

竞争分析数据库

记录：

竞品。

价格。

功能。

用户行为数据库

记录：

点击。

收藏。

购买。

最终目标

数据库不是简单存储。

它应该成为：

AI创业机会判断系统的长期记忆。

未来价值来自：

越来越多的信息。

越来越多判断。

越来越多真实商业反馈。