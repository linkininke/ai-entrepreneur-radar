# AI Entrepreneur Radar
# AI Agent 系统设计文档

版本：
V1.0


---

# 1. 文档目的


本文档定义 AI Entrepreneur Radar 中 AI Agent 系统的设计。


目标：

构建一个多 Agent 协作系统。

让 AI 完成：

信息理解

↓

趋势发现

↓

商业机会生成

↓

创业价值评估

↓

个性化推荐


最终输出：

可执行的创业机会。


---

# 2. 核心设计理念


## 不做新闻总结器


普通AI：

输入新闻

↓

总结新闻


价值有限。


---

本系统：

输入：

世界变化。


↓

理解：

发生了什么。


↓

推理：

为什么重要。


↓

发现：

商业机会在哪里。


↓

行动：

应该做什么产品。


---

# 3. Agent总体架构


系统采用：

Multi-Agent Pipeline。


整体流程：


External Information

    ↓

Agent 1

Information Understanding Agent

    ↓

Agent 2

Trend Discovery Agent

    ↓

Agent 3

Opportunity Generation Agent

    ↓

Agent 4

Business Evaluation Agent

    ↓

Agent 5

Founder Matching Agent

    ↓

Final Opportunity Report



---

# 4. Agent 1

# Information Understanding Agent


## 职责


负责理解原始信息。


输入：

新闻

论文

Github项目

产品发布

社区讨论


输出：

结构化事件。


---

## 输入格式


```json
{
"title":"",
"content":"",
"source":"",
"time":""
}

输出格式
{

"event":

"OpenAI发布新的Agent能力",


"technology":

"AI Agent",


"change":

"模型自主执行任务能力提升",


"affected_fields":

[
"Software",
"Enterprise"
],


"importance":

85

}

Prompt原则

你是一名技术分析师。

不要总结文章。

需要回答：

这个事件改变了什么？

5. Agent 2
Trend Discovery Agent
职责

从大量事件中发现长期趋势。

输入：

100-1000个事件。

输出：

趋势。

核心任务

判断：

这是短期新闻？

还是长期变化？

判断维度
技术成熟度

是否：

成本下降
性能提升
普及增加
市场变化

是否：

用户需求增加
企业开始购买
创业机会

是否产生：

新市场。

输出格式
{

"trend":

"AI Agent替代部分企业流程",


"description":

"企业软件开始从工具转向智能执行系统",


"evidence":

[
"多家公司发布Agent产品",
"企业采用增加"
],


"score":

90

}

6. Agent 3
Opportunity Generation Agent
职责

将趋势转换成创业机会。

这是系统核心。

思考模型

趋势：

↓

谁受到影响？

↓

他们有什么痛苦？

↓

谁愿意付钱？

↓

最小解决方案是什么？

输出格式
{

"title":

"中小企业AI客服自动化"


,
"customer":

"50-500人企业"


,
"problem":

"客服成本高"


,
"solution":

"AI客服Agent"


,
"mvp":

"接入企业知识库，实现自动回复"


,
"pricing":

"299-999/月"


}

7. Agent 4
Business Evaluation Agent
职责

像投资人一样评估机会。

评分模型

总分100。

公式：


Opportunity Score


=

Market

+

Pain

+

Payment

+

Competition

+

Execution


评分维度
Market

市场规模：

0-20

Pain

痛点强度：

0-20

Payment

付费可能：

0-20

Competition

竞争优势：

0-20

Execution

个人实现难度：

0-20

输出
{

"market_score":18,

"pain_score":17,

"payment_score":16,

"competition_score":12,

"execution_score":19,


"total_score":

82,


"recommendation":

"值得验证"

}

8. Agent 5
Founder Matching Agent
职责

根据创业者自身条件判断机会。

因为：

机会不是绝对的。

适合别人：

不一定适合你。

输入

用户画像：

{

"skills":

[
"Java",
"Python",
"AI"
],


"capital":

1000,


"time":

"full-time"


}

输出
{

"fit_score":

90,


"reason":

"该方向适合软件开发者低成本验证"


,
"next_action":

[
"寻找10个目标用户",
"制作MVP"
]

}

9. Agent Pipeline实现方式

第一阶段：

顺序Pipeline。


Collector


↓

Analyzer


↓

Trend Agent


↓

Opportunity Agent


↓

Evaluation Agent


↓

Database




第二阶段：

Agent自主协作。

增加：

Agent Manager。

负责：

任务分配。

10. Prompt管理系统

禁止：

Prompt硬编码。

建立：


prompts/


├── information_analysis.txt


├── trend_detection.txt


├── opportunity_generation.txt


├── evaluation.txt


└── recommendation.txt


11. LLM调用设计

封装统一接口。

例如：

class LLMService:


    def analyze(
        prompt,
        model,
        temperature
    ):

        pass


支持：

Claude

OpenAI

Gemini

国产模型

12. AI输出可靠性设计

不能完全相信AI。

必须：

结构化输出。

使用：

JSON Schema。

增加：

Confidence。

例如：

{

"score":85,

"confidence":0.72

}

13. 人机协作设计

最终决策：

人。

流程：

AI发现机会

↓

用户查看

↓

用户判断

↓

用户验证市场

↓

反馈数据

14. Feedback Loop

系统长期成长核心。

流程：


AI推荐机会


↓

用户行动


↓

获得结果


↓

记录


↓

优化评分模型



记录：

是否开发
是否获得用户
是否收费
收入多少
15. 未来Agent扩展
Market Research Agent

自动研究：

市场规模。

竞品。

Customer Interview Agent

帮助：

设计访谈问题。

Sales Agent

生成：

销售邮件。

推广内容。

Product Manager Agent

自动：

拆需求。

写PRD。

16. 第一版本实现范围

MVP只实现：

必须：

Information Agent

Trend Agent

Opportunity Agent

Evaluation Agent

暂不实现：

复杂自主Agent。

17. 最终目标

构建：

一个AI创业合伙人。

它不是回答问题。

而是持续：

观察世界。

发现变化。

寻找机会。

帮助创业者行动。

最终成为：

个人创业者的信息优势系统。