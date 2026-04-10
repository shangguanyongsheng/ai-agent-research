# 安装指南

> 🛠️ 各平台安装方法详解

---

## 第一步：概念解释

**安装 OpenClaw 需要什么？**
- 就像组装一台收音机，需要：
  1. **电源** - Node.js（提供运行环境）
  2. **主机** - OpenClaw 程序本身
  3. **天线** - Gateway 服务（连接各通道）

**版本要求**：
- Node.js: v24 推荐，v22.14+ 也支持
- 系统: macOS, Linux, Windows (原生或 WSL2)

---

## 第二步：类比理解

| 安装阶段 | 类比 |
|----------|------|
| 安装 Node.js | 给收音机接电源 |
| 安装 OpenClaw | 安装主机电路板 |
| 运行 onboard | 调频找电台 |
| 启动 Gateway | 开机播放 |

---

## 第三步：动手实践

### 方法一：脚本安装（推荐）

**macOS / Linux**：
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows PowerShell**：
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

安装脚本会：
1. 检测 Node.js 版本
2. 安装 npm 包
3. 配置 PATH

### 方法二：npm 安装

```bash
npm install -g openclaw@latest
```

### 方法三：Docker 安装

```bash
docker run -d \
  --name openclaw \
  -p 18789:18789 \
  -v ~/.openclaw:/root/.openclaw \
  openclaw/openclaw:latest
```

### 方法四：Nix 安装

```nix
# flake.nix
{
  inputs.openclaw.url = "github:openclaw/openclaw";
}
```

---

## 初始化流程

安装完成后，运行：

```bash
openclaw onboard --install-daemon
```

**交互式问答**：

1. **选择模型提供商**
   ```
   ? Choose model provider:
   > Anthropic (Claude)
     OpenAI (GPT)
     Google (Gemini)
     Other...
   ```

2. **输入 API Key**
   ```
   ? Enter API key: sk-xxx...
   ```

3. **选择模式**
   ```
   ? Install as daemon service? (Y/n)
   ```
   推荐 Y，后台运行

4. **完成**
   ```
   ✓ Gateway installed and started
   ✓ Control UI at http://127.0.0.1:18789
   ```

---

## 特殊平台安装

### Raspberry Pi

```bash
# 安装 Node.js 24
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt install -y nodejs

# 安装 OpenClaw
npm install -g openclaw@latest

# 初始化
openclaw onboard --install-daemon
```

### macOS App

如果使用 macOS App（独立应用）：

1. 下载安装 dmg
2. 打开 App 会自动启动 Gateway
3. 菜单栏图标显示状态

### WSL2 (Windows)

```bash
# 在 WSL2 Ubuntu 中
curl -fsSL https://openclaw.ai/install.sh | bash

# Windows 浏览器访问
# http://localhost:18789
```

### 服务器部署

**VPS / 云服务器**：

```bash
# 1. SSH 连接服务器
ssh user@server

# 2. 安装
curl -fsSL https://openclaw.ai/install.sh | bash

# 3. 配置远程访问（详见高级模式）
openclaw configure

# 4. 使用 Tailscale 或 SSH 隧道
```

---

## 第四步：知识关联

### 安装验证

```bash
# 检查版本
openclaw --version

# 检查 Gateway 状态
openclaw gateway status

# 健康诊断
openclaw doctor
```

### 常见安装问题

| 问题 | 解决 |
|------|------|
| Node 版本过低 | 升级到 v22.14+ |
| npm 安装失败 | 检查网络或使用 npx |
| 权限错误 | `sudo npm install -g openclaw` |
| PATH 未配置 | 重开终端或手动添加 |

### 卸载

```bash
openclaw uninstall
# 或
npm uninstall -g openclaw
```

### 更新

```bash
openclaw update
# 或
npm update -g openclaw
```

---

## 文件位置

安装后文件结构：

```
~/.openclaw/
├── openclaw.json      # 配置文件
├── sessions.json      # 会话记录
├── skills/            # Skills 目录
├── workspace/         # 默认工作目录
├── logs/              # 日志文件
└── daemon/            # 后台服务
```

---

## 下一步

- [02-配置详解](./02-configuration.md) - 配置 openclaw.json
- [05-通道集成](./05-channels.md) - 连接聊天软件

---

> ✅ 安装完成！Gateway 应该正在运行，访问 http://127.0.0.1:18789 确认。