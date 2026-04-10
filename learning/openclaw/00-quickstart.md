# 5分钟快速上手

> 🎯 目标：从安装到第一次对话，5分钟完成

---

## 第一步：概念解释（像教小孩）

**OpenClaw 是什么？**
- 就像一个「电话接线员」
- 你在 WhatsApp 打电话（发消息）
- 接线员（OpenClaw）接通 AI 大脑
- AI 回话 → 接线员送回给你

**需要什么？**
1. 一台电脑（Mac/Linux/Windows）
2. Node.js（就像电，给程序提供能量）
3. 一个 AI API Key（就像会员卡，让 AI 为你服务）

---

## 第二步：类比理解

| 真实场景 | OpenClaw 对应 |
|----------|---------------|
| 你的手机 | 聊天软件（WhatsApp/Telegram） |
| 电话公司 | OpenClaw Gateway |
| 客服中心 | AI 模型（Claude/GPT） |
| 客服工号 | API Key |

**工作流程**：
```
你发消息 → 电话公司收到 → 转给客服 → 客服回复 → 电话公司送回 → 你收到
```

---

## 第三步：动手实践

### 1️⃣ 检查 Node.js

```bash
node --version
# 需要 v22.14+ 或 v24（推荐）
```

如果没有安装：
- Mac: `brew install node`
- Linux: 见 [安装指南](./01-installation.md)

### 2️⃣ 安装 OpenClaw

**Mac / Linux**：
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows (PowerShell)**：
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

### 3️⃣ 运行初始化

```bash
openclaw onboard --install-daemon
```

这个命令会：
1. 问你要用什么 AI（选 Anthropic Claude 或 OpenAI GPT）
2. 让你输入 API Key
3. 安装后台服务（daemon）
4. 启动 Gateway

**整个过程约 2 分钟**。

### 4️⃣ 验证运行

```bash
openclaw gateway status
```

看到类似输出表示成功：
```
Gateway is running on port 18789
```

### 5️⃣ 打开控制面板

```bash
openclaw dashboard
```

浏览器会打开 `http://127.0.0.1:18789`

### 6️⃣ 发送第一条消息

在控制面板的聊天框输入：
```
你好，介绍一下你自己
```

AI 会回复你！

---

## 第四步：知识关联

### 常见问题

**Q: 没有 API Key 怎么办？**
- Anthropic: https://console.anthropic.com
- OpenAI: https://platform.openai.com

**Q: Gateway 没启动？**
```bash
openclaw gateway start
```

**Q: 想从手机聊天？**
最快方式是 Telegram：
```bash
# 1. 在 Telegram 创建 Bot，获取 token
# 2. 配置到 ~/.openclaw/openclaw.json
openclaw configure
```

详见 [通道集成](./05-channels.md)

---

## 关键命令速查

```bash
# 安装
curl -fsSL https://openclaw.ai/install.sh | bash

# 初始化（会问 API Key）
openclaw onboard --install-daemon

# 查状态
openclaw gateway status

# 打开面板
openclaw dashboard

# 看日志
openclaw logs

# 健康检查
openclaw doctor

# 重启网关
openclaw gateway restart

# 停止网关
openclaw gateway stop
```

---

## 下一步

- [01-安装指南](./01-installation.md) - 不同平台安装详解
- [02-配置详解](./02-configuration.md) - 配置文件详解
- [05-通道集成](./05-channels.md) - 连接聊天软件

---

> ✅ **恭喜！** 你已经能用 OpenClaw 与 AI 对话了。接下来学习如何从手机聊天。