# OpenViking + OpenClaw 集成方案

> **architect-agent 设计文档**

---

## 🏗️ 架构设计

### 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenClaw Gateway                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    OpenViking Context DB                    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  memories/  │  │ resources/  │  │  skills/    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                             │
│  L0 (核心)  ←→  L1 (相关)  ←→  L2 (扩展)                   │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  pm-agent   │     │ dev-agent   │     │  qa-agent   │
│  workspace  │     │  workspace  │     │  workspace  │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## 📁 目录结构

```
~/.openviking/
├── ov.conf                    # OpenViking 配置
└── workspaces/
    └── openclaw/
        ├── memories/
        │   ├── main/          # main agent 记忆
        │   ├── pm-agent/      # pm-agent 记忆
        │   ├── dev-agent/     # dev-agent 记忆
        │   └── ...
        ├── resources/
        │   ├── projects/      # 项目资源
        │   ├── docs/          # 文档资源
        │   └── data/          # 数据资源
        └── skills/
            ├── shared/        # 共享技能
            └── per-agent/     # Agent 专属技能
```

---

## 🔧 配置方案

### ov.conf (使用 DashScope)

```json
{
  "storage": {
    "workspace": "/home/admin/.openviking/workspaces/openclaw"
  },
  "log": {
    "level": "INFO",
    "output": "stdout"
  },
  "embedding": {
    "dense": {
      "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
      "api_key": "${DASHSCOPE_API_KEY}",
      "provider": "openai",
      "dimension": 1024,
      "model": "text-embedding-v3"
    },
    "max_concurrent": 10
  },
  "vlm": {
    "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "api_key": "${DASHSCOPE_API_KEY}",
    "provider": "litellm",
    "model": "dashscope/qwen-turbo",
    "max_concurrent": 100
  }
}
```

---

## 🔄 与 OpenClaw 集成点

### 1. 记忆层集成

```python
# 替代现有的 MEMORY.md
# OpenViking 自动管理 Agent 记忆
```

### 2. 技能注册集成

```python
# 技能注册到 OpenViking skills/ 目录
# 支持分层加载和搜索
```

### 3. 资源管理集成

```python
# 项目资源统一管理
# 支持跨 Agent 共享
```

---

## 📊 预期收益

| 方面 | 当前 | 集成后 |
|------|------|--------|
| 记忆管理 | 手动 MEMORY.md | 自动分层管理 |
| Token 消耗 | 全量加载 | 按需加载 L0/L1/L2 |
| 检索效果 | 简单关键词 | 目录+语义混合 |
| 可观察性 | 黑盒 | 可视化轨迹 |
| 自进化 | 无 | 自动压缩+长期记忆 |

---

## 📋 实施计划

| 阶段 | 任务 | Agent | 预计时间 |
|------|------|-------|----------|
| 1 | 安装 Go + OpenViking | ops-agent | 30min |
| 2 | 配置 DashScope | dev-agent | 10min |
| 3 | 创建工作空间 | dev-agent | 15min |
| 4 | 集成测试 | qa-agent | 30min |
| 5 | 文档编写 | doc-agent | 15min |

---

*architect-agent 设计*