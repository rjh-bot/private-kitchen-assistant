# 私人厨房助理 (Private Kitchen Assistant)

融合 LLM、RAG、Agent、多模态技术的个性化饮食管理系统。

## 项目结构

```
private-kitchen-assistant/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── main.py            # 入口 & FastAPI 应用
│   │   ├── config.py          # 配置
│   │   ├── agent/             # Agent 系统
│   │   │   ├── agent_hub.py   # AgentHub: 统一管理Agent/Tool/Provider
│   │   │   ├── react_agent.py # ReAct Agent: 推理→工具调用→结果整合
│   │   │   └── subagent.py    # Subagent 专家框架
│   │   ├── tools/             # 工具体系
│   │   │   ├── recipe.py      # 菜谱 RAG 检索
│   │   │   ├── nutrition.py   # 营养分析
│   │   │   ├── diet_plan.py   # 饮食计划
│   │   │   └── web_search.py  # 联网搜索
│   │   ├── rag/               # RAG 混合检索
│   │   │   ├── retriever.py   # 向量+BM25混合检索
│   │   │   └── cache.py       # L1(内存)+L2(语义近似)双层缓存
│   │   ├── models/            # 数据模型
│   │   │   ├── database.py    # SQLite 数据库
│   │   │   ├── user.py        # 用户模型
│   │   │   └── recipe.py      # 菜谱模型
│   │   ├── api/               # API 路由
│   │   │   ├── chat.py        # SSE 流式对话
│   │   │   ├── user.py        # 用户档案管理
│   │   │   └── image.py       # 图片识别
│   │   └── llm/               # LLM 客户端
│   │       └── deepseek.py    # DeepSeek API 封装
│   ├── data/
│   │   └── recipes.json       # 种子菜谱数据
│   ├── .env.example
│   └── requirements.txt
├── frontend/                   # React 前端
│   ├── src/
│   │   ├── App.jsx            # 主应用
│   │   ├── App.css            # 样式
│   │   ├── api.js             # API 客户端
│   │   └── components/
│   │       ├── ChatView.jsx   # 对话界面 (SSE 实时流)
│   │       ├── Sidebar.jsx    # 侧边栏导航
│   │       ├── UserProfile.jsx # 用户档案
│   │       ├── DietPlan.jsx   # 饮食计划生成器
│   │       └── ImageUpload.jsx # 图片上传识别
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 核心功能

### 1. Agent 智能饮食管家 (ReAct + AgentHub)
- **ReAct 推理闭环**: 分析用户意图 → 调用工具 → 整合结果 → 自然语言回复
- **AgentHub**: 统一管理所有 Agent、Tool、Subagent 的注册与调度
- **SSE 事件流**: 实时展示 Agent 推理过程
- **上下文压缩**: 高效管理对话历史

### 2. 工具体系
- **菜谱 RAG 检索**: 向量+BM25混合检索，L1/L2双层缓存
- **营养分析**: 常见食物营养数据库查询
- **饮食计划**: 按目标(减脂/增肌/控糖)自动生成
- **饮食记录**: 记录进食内容

### 3. Subagent 专家体系
- **营养师**: 专业营养分析与饮食方案建议
- **烹饪顾问**: 烹饪技巧指导与菜谱推荐

### 4. 多模态图片识别
- 食材/菜品图片智能识别
- 联动营养数据库估算热量与宏量营养

### 5. 用户画像
- 健康目标(减脂/增肌/控糖/健康饮食)
- 饮食偏好与过敏原
- 长期饮食指令
- 个性化输出

## 快速开始

### 前置要求
- Python 3.10+
- Node.js 18+
- DeepSeek API Key

### 1. 配置后端

```bash
cd backend
cp .env.example .env
# 编辑 .env，填入你的 DeepSeek API Key
```

### 2. 安装依赖

```bash
# 后端
cd backend
pip install -r requirements.txt

# 前端
cd ../frontend
npm install
```

### 3. 启动

```bash
# 启动后端 (终端1)
cd backend
python -m app.main

# 启动前端 (终端2)
cd frontend
npm run dev
```

### 4. 访问

打开浏览器访问 http://localhost:5173

## 技术栈

- **后端**: Python, FastAPI, SQLAlchemy, SQLite
- **前端**: React 18, Vite
- **LLM**: DeepSeek API (deepseek-chat)
- **RAG**: Sentence-Transformers, BM25, 自定义混合检索
- **缓存**: 内存级 L1(精确) + L2(语义近似) 双层缓存
- **Agent**: 自定义 ReAct Agent + AgentHub + Subagent
- **数据库**: SQLite + aiosqlite
