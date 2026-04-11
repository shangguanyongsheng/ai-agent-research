# Hermes Agent 研究报告

**调研日期**: 2026-04-11  
**项目地址**: https://github.com/NousResearch/hermes-agent  
**开发者**: Nous Research

---

## 一、产品定位

### 核心口号

> **The self-improving AI agent that grows with you**
> 随你成长的自我进化 AI Agent

### 核心差异化

Hermes 是**唯一内置学习循环的 AI Agent**：
- ✅ 从经验创建技能（Skills）
- ✅ 使用时自动改进技能
- ✅ 周期性提醒自己持久化知识
- ✅ 搜索过往对话历史
- ✅ 跨会话构建用户的深度画像

**一句话总结**: 它不是帮你做事的 Agent，是**会学习的 Agent**。

---

## 二、核心技术架构

### 2.1 学习闭环系统

```
用户交互 → Agent 执行 → 创建/改进技能 → 持久化记忆 → 下次调用
         ↑                                          ↓
         └────────── 跨会话搜索 ←──────────────────┘
```

| 组件 | 功能 |
|------|------|
| **Agent-curated memory** | Agent 自主管理记忆，定期提醒持久化 |
| **Skills self-improve** | 复杂任务后自动创建技能，使用时改进 |
| **FTS5 session search** | 全文搜索历史对话，LLM 总结跨会话召回 |
| **Honcho user modeling** | 辩证式用户建模，构建深度用户画像 |

### 2.2 多模型支持

| Provider | 特点 |
|----------|------|
| **Nous Portal** | 自家平台，可能有专属优化 |
| **OpenRouter** | 200+ 模型，一站式切换 |
| **z.ai/GLM** | 中文场景友好 |
| **Kimi/Moonshot** | 长文本能力强 |
| **MiniMax** | 多模态支持 |
| **OpenAI** | GPT 系列经典模型 |
| **自定义 endpoint** | 完全开放，无锁定 |

**切换方式**: `hermes model` 命令，无需改代码。

### 2.3 多终端后端

| 后端 | 适用场景 |
|------|----------|
| **Local** | 本地开发测试 |
| **Docker** | 容器化部署 |
| **SSH** | 远程服务器 |
| **Daytona** | Serverless 持久化，空闲时休眠 |
| **Singularity** | HPC 环境 |
| **Modal** | Serverless GPU，按需计费 |

**亮点**: Daytona 和 Modal 支持 serverless 持久化 —— Agent 环境空闲时休眠，唤醒时恢复，**几乎不花钱**。

---

## 三、关键功能详解

### 3.1 Skills 系统（核心）

- **Procedural memory**: 技能是 Agent 的"程序记忆"
- **Skills Hub**: https://agentskills.io 开放标准，可分享技能
- **自动创建**: 完成复杂任务后，Agent 自动提取技能
- **使用改进**: 每次调用技能时，Agent 会优化它

**对比传统 Agent**: 传统 Agent 每次从零开始；Hermes 每次都在"积累经验"。

### 3.2 多平台消息网关

| 平台 | 功能 |
|------|------|
| Telegram | ✅ 全功能 |
| Discord | ✅ 全功能 |
| Slack | ✅ 全功能 |
| WhatsApp | ✅ 全功能 |
| Signal | ✅ 全功能 |
| CLI | ✅ 全功能 TUI |

**特色**:
- 语音备忘录转录
- 跨平台对话连续性（Telegram ↔ Discord ↔ CLI）
- 单一 gateway 进程管理所有平台

### 3.3 Cron 调度器

- 内置调度系统
- 自然语言定义任务
- 支持多平台交付
- 示例：每日报告、夜间备份、每周审计

### 3.4 子 Agent 并行

- Spawn isolated subagents
- Python 脚本通过 RPC 调用工具
- 多步骤流水线压缩为零上下文成本的 turn

### 3.5 研究友好特性

| 特性 | 用途 |
|------|------|
| **Batch trajectory generation** | 批量生成 Agent 轨迹数据 |
| **Atropos RL environments** | 强化学习训练环境 |
| **Trajectory compression** | 训练下一代 tool-calling 模型 |

---

## 四、与 OpenClaw 对比分析

### 4.1 功能对比

| 功能 | Hermes Agent | OpenClaw |
|------|--------------|----------|
| **学习闭环** | ✅ 内置 | ❌ 需手动管理记忆 |
| **技能系统** | ✅ 自动创建/改进 | ✅ Skills 系统，但需手动 |
| **多模型** | ✅ 200+ via OpenRouter | ✅ 多 Provider 支持 |
| **多平台** | ✅ 6+ 平台 | ✅ 多平台 Gateway |
| **Cron 调度** | ✅ 内置 | ✅ openclaw-cron |
| **Serverless** | ✅ Daytona/Modal | ❌ 需自建 |
| **子 Agent** | ✅ spawn subagents | ✅ sessions_spawn |
| **用户建模** | ✅ Honcho dialectic | ❌ 无深度画像 |
| **会话搜索** | ✅ FTS5 + LLM | ❌ 无搜索功能 |

### 4.2 架构对比

| 维度 | Hermes | OpenClaw |
|------|--------|----------|
| **设计哲学** | 学习优先 | 工具优先 |
| **记忆系统** | Agent 自主管理 | 用户手动 MEMORY.md |
| **技能进化** | 使用时自动改进 | 静态 SKILL.md |
| **用户画像** | Honcho 建模 | USER.md 手动维护 |

### 4.3 迁移支持

Hermes 提供**一键迁移 OpenClaw**:

```bash
hermes claw migrate          # 完整迁移
hermes claw migrate --dry-run  # 预览
hermes claw migrate --preset user-data  # 仅用户数据
```

**迁移内容**:
- ✅ SOUL.md → persona
- ✅ MEMORY.md / USER.md → 记忆
- ✅ 用户创建的技能 → ~/.hermes/skills/openclaw-imports/
- ✅ 命令 allowlist
- ✅ 平台配置
- ✅ API keys（Telegram、OpenRouter、OpenAI、Anthropic、ElevenLabs）
- ✅ TTS 资产
- ✅ AGENTS.md（可选）

---

## 五、适用场景

### 5.1 推荐使用 Hermes

| 场景 | 原因 |
|------|------|
| **长期陪伴型 Agent** | 学习闭环，越用越懂你 |
| **多平台用户** | Telegram + Discord + Slack 一体化 |
| **成本敏感** | Serverless 模式，空闲几乎免费 |
| **研究者** | RL 训练、轨迹生成友好 |
| **OpenClaw 用户想升级** | 一键迁移，无缝切换 |

### 5.2 推荐使用 OpenClaw

| 场景 | 原因 |
|------|------|
| **已有成熟工作流** | OpenClaw 生态稳定 |
| **需要精细控制** | 手动管理记忆更可控 |
| **企业部署** | OpenClaw 更成熟的企业级特性 |
| **中国本地化** | OpenClaw 对国内环境适配更好 |

---

## 六、未来趋势判断

### 6.1 Agent 学习化趋势

Hermes 代表了 Agent 发展的**下一阶段**：

```
阶段 1: Tool-using Agent（当前主流）
阶段 2: Learning Agent（Hermes 代表）
阶段 3: Self-evolving Agent（未来）
```

**核心演进**:
- 从"帮你做事" → "帮你做事并学习" → "自主进化"
- 从静态技能 → 动态技能 → 自创技能
- 从手动记忆 → Agent 管理 → 用户建模

### 6.2 Serverless Agent 趋势

Daytona/Modal 模式代表**Agent 部署的新范式**：
- 空闲时休眠，唤醒时恢复
- 按使用付费，而非按资源付费
- Agent 不再绑定笔记本，真正云端化

### 6.3 开放标准趋势

- **agentskills.io**: 技能开放标准
- **MCP**: 工具协议标准化
- **Honcho**: 用户建模标准化

Agent 生态正在从"各自封闭"走向"开放互联"。

---

## 七、总结

### Hermes Agent 核心价值

| 维度 | 评分 | 说明 |
|------|------|------|
| **学习能力** | ⭐⭐⭐⭐⭐ | 真正的学习闭环，行业首创 |
| **多平台** | ⭐⭐⭐⭐⭐ | 6+ 平台一体化 |
| **成本控制** | ⭐⭐⭐⭐ | Serverless 模式优秀 |
| **研究友好** | ⭐⭐⭐⭐⭐ | RL/轨迹生成专精 |
| **迁移友好** | ⭐⭐⭐⭐⭐ | OpenClaw 一键迁移 |
| **成熟度** | ⭐⭐⭐ | 相比 OpenClaw 较新 |

### 最终建议

- **如果你是 OpenClaw 用户**: 可以尝试 Hermes，一键迁移无痛切换，体验"学习型 Agent"
- **如果你是研究者**: Hermes 的 RL 环境和轨迹生成是独特优势
- **如果你追求稳定**: OpenClaw 生态更成熟，等 Hermes 成熟后再迁移

---

## 八、快速上手

```bash
# 安装
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# 启动
source ~/.bashrc
hermes

# 选择模型
hermes model

# OpenClaw 用户迁移
hermes claw migrate

# 启动消息网关
hermes gateway setup
hermes gateway start
```

---

*📅 调研报告生成时间: 2026-04-11*  
*🔗 项目地址: https://github.com/NousResearch/hermes-agent*  
*📚 文档: https://hermes-agent.nousresearch.com/docs/*