# OpenClaw Gateway 网关

> 使用费曼学习法：理解 Gateway 的运维与监控。

## 📖 概念解释

**什么是 Gateway？**

Gateway 是 OpenClaw 的核心服务进程。它：
1. 监听所有 Channel 的消息
2. 路由消息到正确的 Agent
3. 管理 Session（会话）状态
4. 提供 API 接口（WebSocket + HTTP）
5. 托管 Control UI（控制面板）

Gateway 是"单一真实来源"，协调一切。

## 🎯 类比理解

**把 Gateway 想象成"酒店前台"**

- 前台接听所有电话 → Gateway 接收所有消息
- 前台分配房间 → Gateway 路由会话
- 前台管理入住信息 → Gateway 管理 Session
- 前台提供查询服务 → Gateway 提供 API

就像酒店前台是中央枢纽，Gateway 是 OpenClaw 的中央枢纽。

## 🔧 实践示例

### 启动 Gateway

#### 直接启动

```bash
# 前台运行（调试用）
openclaw gateway --port 18789

# 详细日志
openclaw gateway --port 18789 --verbose

# 强制占用端口
openclaw gateway --force
```

#### 服务安装（推荐）

```bash
# 安装为系统服务
openclaw gateway install

# 检查状态
openclaw gateway status

# 重启服务
openclaw gateway restart

# 停止服务
openclaw gateway stop
```

### 不同平台的系统服务

#### macOS (launchd)

```bash
openclaw gateway install
# 创建 LaunchAgent: ai.openclaw.gateway
```

服务标签：`ai.openclaw.gateway`（默认）或 `ai.openclaw.<profile>`（命名配置）

#### Linux (systemd)

**用户服务：**
```bash
openclaw gateway install
systemctl --user enable --now openclaw-gateway.service
```

**持久化（退出后保持运行）：**
```bash
sudo loginctl enable-linger <user>
```

**系统服务（多用户）：**
```bash
sudo systemctl enable --now openclaw-gateway.service
```

#### Windows (计划任务)

```powershell
openclaw gateway install
# 创建计划任务: OpenClaw Gateway
```

### Gateway 状态检查

```bash
# 基本状态
openclaw gateway status

# 深度状态（扫描系统服务）
openclaw gateway status --deep

# JSON 格式输出
openclaw gateway status --json
```

**健康基准：**
```
Runtime: running
RPC probe: ok
```

### 端口与绑定

| 设置 | 解析顺序 |
|------|----------|
| Gateway 端口 | `--port` → 环境变量 → `gateway.port` → `18789` |
| 绑定模式 | CLI → `gateway.bind` → `loopback` |

**绑定模式：**
- `loopback`（默认）：只监听本地
- 其他绑定需要配置认证

### Gateway 协议

#### WebSocket 连接流程

1. 客户端发送 `connect` 帧
2. Gateway 返回 `hello-ok`（包含状态快照）
3. 请求：`req(method, params)` → `res(ok|error)`
4. 事件：实时推送（`agent`, `chat`, `health` 等）

#### Agent 运行流程

```
消息到达 → Gateway 接收 → 创建 Agent 任务
                ↓
          状态: accepted（立即确认）
                ↓
          Agent 处理（流式事件）
                ↓
          状态: ok 或 error（最终响应）
```

### OpenAI 兼容端点

Gateway 提供 OpenAI 兼容的 HTTP API：

| 端点 | 说明 |
|------|------|
| `GET /v1/models` | 模型列表 |
| `GET /v1/models/{id}` | 单个模型 |
| `POST /v1/embeddings` | 嵌入向量 |
| `POST /v1/chat/completions` | 聊天补全 |
| `POST /v1/responses` | Responses API |

**用途：**
- 连接 Open WebUI、LobeChat 等
- RAG 管道的嵌入接口
- Agent 原生客户端

**模型命名：**
- `openclaw` / `openclaw/default`：默认 Agent
- `openclaw/<agentId>`：特定 Agent

### 远程访问

#### 推荐：Tailscale/VPN

```bash
# 配置 Tailscale
openclaw config set gateway.tailscale.enabled true
```

#### 备选：SSH 隧道

```bash
ssh -N -L 18789:127.0.0.1:18789 user@host
```

本地连接到 `ws://127.0.0.1:18789`

**注意：** SSH 隧道不绕过认证，客户端仍需提供 token/password。

### 多 Gateway 配置

大多数场景只需一个 Gateway。多 Gateway 用于：
- 严格隔离
- 救援备用

**每个 Gateway 需要：**
- 唯一端口
- 唯一配置路径
- 唯一状态目录
- 唯一工作空间

```bash
# Gateway A
OPENCLAW_CONFIG_PATH=~/.openclaw/a.json \
OPENCLAW_STATE_DIR=~/.openclaw-a \
openclaw gateway --port 19001

# Gateway B
OPENCLAW_CONFIG_PATH=~/.openclaw/b.json \
OPENCLAW_STATE_DIR=~/.openclaw-b \
openclaw gateway --port 19002
```

### 热加载模式

| 模式 | 行为 |
|------|------|
| `hybrid`（默认） | 安全修改热加载，关键修改自动重启 |
| `hot` | 只热加载，关键修改需手动重启 |
| `restart` | 任何修改都重启 |
| `off` | 禁用监听 |

**什么需要重启？**
- Gateway 端口、绑定、认证
- 插件、发现服务

**什么热加载？**
- Channel 配置
- Agent/模型配置
- Skills、工具配置
- Session、消息配置

### 日志查看

```bash
# 实时日志
openclaw logs --follow

# 最近日志
openclaw logs --limit 100
```

### 问题诊断

```bash
# 诊断工具
openclaw doctor

# 自动修复
openclaw doctor --fix
```

## 🔗 知识关联

### Gateway 与其他概念

| 概念 | 与 Gateway 的关系 |
|------|--------------------|
| Channel | Gateway 管理 Channel 连接 |
| Agent | Gateway 路由消息到 Agent |
| Session | Gateway 维护 Session 状态 |
| Control UI | Gateway 托管 Web 界面 |
| MCP | Gateway 通过 MCP 暴露接口 |

### Gateway 命令汇总

```bash
# 启动/停止
openclaw gateway [--port] [--verbose] [--force]
openclaw gateway install
openclaw gateway restart
openclaw gateway stop

# 状态检查
openclaw gateway status [--deep] [--json]
openclaw status
openclaw health

# 日志
openclaw logs --follow

# 诊断
openclaw doctor [--fix]

# 通道状态
openclaw channels status --probe
```

### 配置热加载流程

```
配置文件修改 → Gateway 监听
                    ↓
              判断修改类型
                    ↓
         安全修改 → 热加载生效
         关键修改 → 重启 Gateway
```

## ⚠️ 常见问题

### Gateway 拒绝启动

| 错误 | 原因 | 解决 |
|------|------|------|
| `refusing to bind without auth` | 非本地绑定缺少认证 | 配置 token/password |
| `another gateway is listening` | 端口被占用 | 使用 `--force` 或换端口 |
| `Gateway start blocked` | 配置损坏 | 运行 `doctor --fix` |
| `unauthorized` | 认证不匹配 | 检查 token/password |

### 多 Gateway 检测

```bash
openclaw gateway status --deep
# 可能报告: Other gateway-like services detected
```

检查：
```bash
openclaw gateway probe
# 警告: multiple reachable gateways
```

如果是预期行为，确保端口和配置隔离。

### 事件丢失

Gateway 不重放历史事件。如果客户端断开：
- 重新连接
- 刷新状态（`health`, `system-presence`）
- 用 `messages_read` 读取历史

## 📝 总结

Gateway 是"酒店前台"：
- 接收所有消息
- 路由到 Agent
- 管理会话状态
- 提供 API 服务

运维命令：
- `gateway status`：检查状态
- `gateway install`：安装服务
- `gateway restart`：重启服务
- `doctor`：诊断问题

关键特性：
- 自动热加载配置
- OpenAI 兼容 API
- 系统服务管理

---

*费曼学习法：概念解释 → 类比理解 → 实践示例 → 知识关联*