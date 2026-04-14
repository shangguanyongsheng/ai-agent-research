# 11-OpenClaw迁移

> 从 OpenClaw 一键迁移到 Hermes，保留所有设置、记忆、技能、API Keys。

---

## 第一步：概念解释

### OpenClaw 是什么？

**OpenClaw** 是一个开源 AI Agent 项目，与 Hermes Agent 架构相似：
- CLI + Gateway
- Skills + Memory
- 多平台支持

**Hermes 支持 OpenClaw 一键迁移**，因为：
- 两者架构兼容
- Skills 标准（agentskills.io）兼容
- Memory 格式兼容

---

### 迁移什么？

| 内容 | 说明 |
|------|------|
| **SOUL.md** | 人设文件 |
| **Memories** | MEMORY.md + USER.md |
| **Skills** | 用户创建的技能 |
| **Command Allowlist** | 命令批准规则 |
| **Messaging Settings** | 平台配置、允许用户、工作目录 |
| **API Keys** | 允许列表中的密钥（Telegram/OpenRouter/OpenAI/Anthropic/ElevenLabs） |
| **TTS Assets** | Workspace 音频文件 |
| **Workspace Instructions** | AGENTS.md |

---

## 第二步：类比理解

### 迁移 = 员工转岗

传统迁移 → 新入职，重新配置一切
Hermes 迁移 → 带着所有东西转岗：
  - 带笔记本（Memory）
  - 带操作手册（Skills）
  - 带人设（SOUL.md）
  - 带联系方式（API Keys）

**类比：**

```
手动迁移：
- 重新配置 Telegram Bot
- 重新写 Skills
- 重新设置 Memory
- 重新输入 API Keys
→ 几小时工作量

Hermes 一键迁移：
hermes claw migrate
→ 自动导入所有内容
→ 几分钟完成
```

---

## 第三步：代码/实践

### 迁移命令

```bash
# 首次安装时自动检测 ~/.openclaw 并提示迁移
hermes setup

# 随时迁移
hermes claw migrate              # 交互式迁移（完整预设）
hermes claw migrate --dry-run    # 预览（不实际执行）
hermes claw migrate --preset user-data  # 只迁移用户数据（不含密钥）
hermes claw migrate --overwrite  # 覆盖已有冲突
```

---

### 迁移预设

| 预设 | 内容 |
|------|------|
| **完整（默认）** | 所有内容 |
| **user-data** | 用户数据（不含密钥） |
| **secrets-only** | 仅密钥 |

---

### 迁移目标位置

| OpenClaw 位置 | Hermes 位置 |
|---------------|-------------|
| `~/.openclaw/SOUL.md` | `~/.hermes/SOUL.md` |
| `~/.openclaw/memory/MEMORY.md` | `~/.hermes/memories/MEMORY.md` |
| `~/.openclaw/memory/USER.md` | `~/.hermes/memories/USER.md` |
| `~/.openclaw/skills/*` | `~/.hermes/skills/openclaw-imports/` |
| `~/.openclaw/.env` | `~/.hermes/.env`（仅允许列表密钥） |
| `~/.openclaw/config.yaml` | 合并入 `~/.hermes/config.yaml` |

---

### API Key 允许列表

自动迁移的密钥：

| 密钥 | 说明 |
|------|------|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token |
| `OPENROUTER_API_KEY` | OpenRouter |
| `OPENAI_API_KEY` | OpenAI |
| `ANTHROPIC_API_KEY` | Anthropic |
| `ELEVENLABS_API_KEY` | ElevenLabs TTS |

其他密钥不自动迁移（安全考虑）。

---

### 干运行预览

```bash
hermes claw migrate --dry-run
```

输出：

```
Migration Preview:
- SOUL.md → ~/.hermes/SOUL.md
- MEMORY.md → ~/.hermes/memories/MEMORY.md (12 entries)
- USER.md → ~/.hermes/memories/USER.md (5 entries)
- Skills → ~/.hermes/skills/openclaw-imports/ (3 skills)
- TELEGRAM_BOT_TOKEN → ~/.hermes/.env
- Command allowlist → config.yaml

Run without --dry-run to execute.
```

---

### 迁移后检查

```bash
hermes config show   # 查看配置
hermes skills list   # 查看技能
hermes memory status # 查看记忆状态
hermes doctor        # 诊断问题
```

---

### 冲突处理

```bash
# 如果 Hermes 已有同名文件
hermes claw migrate --overwrite  # 覆盖

# 或交互式选择
hermes claw migrate
# 会询问每个冲突的处理方式
```

---

### Workspace 迁移

```bash
# 如果要迁移 Workspace 的 AGENTS.md
hermes claw migrate --workspace-target ~/.hermes/
```

---

## 第四步：知识关联

### OpenClaw vs Hermes

| 特性 | OpenClaw | Hermes |
|------|----------|--------|
| CLI | ✅ | ✅ |
| Gateway | ✅ | ✅ |
| Skills | agentskills.io | agentskills.io |
| Memory | MEMORY.md/USER.md | MEMORY.md/USER.md |
| Cron | ✅ | ✅（自然语言） |
| Learning Loop | 部分 | 完整闭环 |
| Skills Hub | — | ✅ |
| RL Training | — | ✅ |

### 相关概念

| 概念 | 关系 |
|------|------|
| [Skills](04-Skills系统.md) | Skills 迁移 |
| [记忆系统](05-记忆与用户建模.md) | Memory 迁移 |
| [多平台网关](06-多平台网关.md) | 平台配置迁移 |

---

## 🎯 关键理解

1. **一键迁移**：自动导入所有兼容内容
2. **Skills 兼容**：agentskills.io 标准
3. **密钥安全**：只迁移允许列表中的密钥
4. **预览模式**：`--dry-run` 查看将要迁移什么
5. **冲突处理**：`--overwrite` 或交互式选择

---

## 📋 迁移流程

### 标准迁移

```bash
# 1. 安装 Hermes
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# 2. 预览迁移
hermes claw migrate --dry-run

# 3. 执行迁移
hermes claw migrate

# 4. 检查结果
hermes doctor
hermes skills list
hermes memory status

# 5. 启动 Hermes
hermes
```

---

### 仅迁移用户数据

```bash
# 不迁移密钥（手动配置 API）
hermes claw migrate --preset user-data

# 手动配置 API Key
hermes model
```

---

### 迁移后使用 OpenClaw Skills

```bash
# Skills 自动放入 openclaw-imports 目录
hermes skills list
# 显示：openclaw-imports/skill1, openclaw-imports/skill2

# 使用
/openclaw-imports/skill1 help me with...
```

---

## 🔗 官方文档

- [OpenClaw Migration Guide](https://hermes-agent.nousresearch.com/docs/guides/openclaw-migration)
- [agentskills.io 标准](https://agentskills.io)

---

*费曼学习法文档 - Hermes Agent*