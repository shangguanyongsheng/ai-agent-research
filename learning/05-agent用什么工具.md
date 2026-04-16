# 🟡 05 — Agent 用什么工具？

> 💡 一句话：**OpenClaw（聊天渠道）+ Claude Code（终端渠道）+ Skills（能力包）。**

---

## 一张图看懂

```
              你
               │
        ┌──────┴──────┐
        ▼             ▼
   📱 发消息       💻 终端操作
   OpenClaw      Claude Code
   （聊天网关）   （终端 Agent）
        │             │
        └──────┬──────┘
               ▼
          Skills（能力包）
          ├── github
          ├── web_search
          └── 自定义技能
```

## OpenClaw vs Claude Code

| | OpenClaw | Claude Code |
|--|----------|-------------|
| **在哪用** | WhatsApp/Telegram/Discord | 终端（Terminal） |
| **适合什么** | 随时随地的轻任务 | 深度开发、代码工作 |
| **运行方式** | 自托管网关，24/7 在线 | 按需启动 |
| **类比** | 🤖 智能客服 | 👨‍💻 AI 程序员 |

## 选哪个？

```
你需要...
  │
  ├─ 在手机上随时问问题？  → OpenClaw + Telegram
  ├─ 在电脑上写代码？     → Claude Code
  ├─ 每天定时发日报？     → OpenClaw + Cron
  └─ 需要专业领域能力？   → 安装对应 Skill
```

## Skills：Agent 的能力包

**Skills 就像手机 App**——需要什么能力，就装什么 Skill。

每个 Skill 是一个 `SKILL.md` 文件，告诉 Agent："遇到这种情况，这样做"。

### 创建 Skill（3 步）

```bash
# Step 1: 创建目录
mkdir -p ~/.claude/skills/my-skill

# Step 2: 写 SKILL.md（文件名必须大写！）
cat > ~/.claude/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: 描述这个技能做什么
---

当用户做 XX 事时：
1. 第一步...
2. 第二步...
3. 第三步...
EOF

# Step 3: 验证
claude → 输入 /skills → 看到 my-skill ✅
```

### Skill vs CLAUDE.md

| | Skill | CLAUDE.md |
|--|-------|-----------|
| **是什么** | 特定任务的工作流 | 项目的通用规则 |
| **生效时机** | 需要特定能力时 | 每次交互都生效 |
| **类比** | 📱 手机 App | ⚙️ 系统设置 |
| **例子** | "生成架构图" 的流程 | "用 2 空格缩进" |

## 总结

> OpenClaw 让你在聊天中用 Agent，Claude Code 让你在终端里用 Agent，
> Skills 让 Agent 拥有特定领域的专业能力。
>
> 下一篇 → [Agent 怎么变聪明？](06-agent怎么变聪明.md)
