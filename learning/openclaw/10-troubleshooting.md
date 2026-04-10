# 故障排查

> 🔧 常见问题与解决方案

---

## 第一步：概念解释

**故障排查是什么？**
- 就像「医生诊断」
- 症状 → 检查 → 诊断 → 治疗

**类比**：
- doctor 命令 = 体检
- logs 命令 = 病历
- 症状描述 = 患者主诉
- 配置检查 = 血液检查

**排查流程**：
```
发现问题
    ↓
openclaw doctor（诊断）
    ↓
查看 logs（找线索）
    ↓
定位原因
    ↓
应用修复
    ↓
验证解决
```

---

## 第二步：类比理解

| 工具 | 类比 | 用途 |
|------|------|------|
| `openclaw doctor` | 体检报告 | 全面检查 |
| `openclaw logs` | 病历记录 | 查看历史 |
| `openclaw gateway status` | 心电图 | 当前状态 |
| `openclaw doctor --fix` | 治疗 | 自动修复 |

---

## 第三步：动手实践

### 基础诊断命令

```bash
# 全面检查
openclaw doctor

# 自动修复
openclaw doctor --fix

# 查看状态
openclaw gateway status

# 查看日志
openclaw logs

# 实时日志
openclaw logs --follow

# 过滤日志
openclaw logs --filter channel:telegram
```

### 常见问题与解决

#### 1. Gateway 无法启动

**症状**：`openclaw gateway start` 失败

**排查**：
```bash
# 检查配置
openclaw doctor

# 查看错误日志
openclaw logs --tail 50
```

**常见原因**：

| 原因 | 解决 |
|------|------|
| 配置语法错误 | 检查 JSON5 格式 |
| 端口被占用 | 改用其他端口 |
| Node 版本低 | 升级到 v22.14+ |
| 权限问题 | 检查文件权限 |

**解决示例**：
```bash
# 端口被占用
openclaw config set gateway.port 18790
openclaw gateway start
```

#### 2. 通道无法连接

**症状**：Telegram/WhatsApp 连不上

**排查**：
```bash
# 检查通道状态
openclaw channels status

# 查看通道日志
openclaw logs --filter channel:telegram
```

**常见原因**：

| 原因 | 解决 |
|------|------|
| Token 无效 | 重新获取 Token |
| 网络问题 | 检查防火墙 |
| Bot 权限不足 | 检查 Bot 权限 |
| 配置错误 | 检查 openclaw.json |

#### 3. Agent 不回复

**症状**：发送消息，Agent 无响应

**排查**：
```bash
# 检查是否被允许
openclaw config get channels.telegram.allowFrom

# 检查 dmPolicy
openclaw config get channels.telegram.dmPolicy

# 查看是否在 pairing 状态
openclaw logs --filter pairing
```

**常见原因**：

| 原因 | 解决 |
|------|------|
| 未配对 | 完成配对流程 |
| 不在 allowFrom | 添加到白名单 |
| 群聊未 @mention | 发送时 @Agent |
| Session 问题 | 检查 sessions.json |

#### 4. API Key 错误

**症状**：模型调用失败

**排查**：
```bash
# 检查模型配置
openclaw config get agents.defaults.model

# 检查 API Key
openclaw config get models.providers.openai.apiKey
```

**常见原因**：

| 原因 | 解决 |
|------|------|
| API Key 无效 | 重新获取 |
| 环境变量未设置 | 设置环境变量 |
| 余额不足 | 检查账户余额 |
| 模型名称错误 | 检查模型 ID |

#### 5. 工具调用失败

**症状**：exec/browser 等工具报错

**排查**：
```bash
# 检查工具权限
openclaw logs --filter tool:exec

# 检查沙箱配置
openclaw config get agents.defaults.sandbox
```

**常见原因**：

| 原因 | 解决 |
|------|------|
| 权限不足 | 检查工具权限 |
| 沙箱问题 | 检查沙箱镜像 |
| 命令不存在 | 检查命令路径 |
| 网络限制 | 检查网络访问 |

---

## 第四步：知识关联

### 日志分析

**日志级别**：
- `error` - 错误
- `warn` - 警告
- `info` - 信息
- `debug` - 调试

**日志位置**：
```
~/.openclaw/logs/
├── gateway.log      # Gateway 日志
├── channel-xxx.log  # 通道日志
└── agent-xxx.log    # Agent 日志
```

### 配置验证

```bash
# 查看完整 schema
openclaw config schema

# 检查特定配置
openclaw config get <path>

# 验证配置
openclaw doctor --config
```

### Session 问题

```bash
# 查看活跃 Sessions
openclaw sessions list

# 清理 Session
openclaw sessions clear --agent main

# 重置 Session
openclaw sessions reset --session-key xxx
```

---

## 快速排查清单

### Gateway 问题

```bash
1. openclaw gateway status    # 是否运行
2. openclaw doctor            # 全面检查
3. openclaw logs              # 看错误
4. openclaw gateway restart   # 重启试试
```

### 通道问题

```bash
1. openclaw channels status   # 连接状态
2. openclaw logs --filter channel:xxx  # 通道日志
3. 检查 Token/凭证
4. 检查 allowFrom 配置
```

### Agent 问题

```bash
1. openclaw agents list       # Agent 状态
2. openclaw logs --agent xxx  # Agent 日志
3. 检查 model 配置
4. 检查 skills 配置
```

### 工具问题

```bash
1. openclaw logs --filter tool:xxx  # 工具日志
2. 检查工具权限
3. 检查沙箱配置
4. 检查网络访问
```

---

## 常用诊断命令速查

```bash
# 基础检查
openclaw doctor
openclaw doctor --fix
openclaw gateway status
openclaw agents list
openclaw sessions list

# 日志查看
openclaw logs
openclaw logs --follow
openclaw logs --filter channel:telegram
openclaw logs --tail 100

# 配置检查
openclaw config get agents.defaults.model
openclaw config get channels.telegram.dmPolicy
openclaw config schema

# 通道检查
openclaw channels status

# 重启
openclaw gateway restart
```

---

## 获取帮助

- **官方文档**：https://docs.openclaw.ai/help
- **Discord社区**：https://discord.gg/clawd
- **GitHub Issues**：https://github.com/openclaw/openclaw/issues

---

## 下一步

- [06-Gateway网关](./06-gateway.md) - Gateway 配置
- [09-安全最佳实践](./09-security.md) - 安全排查
- [官方帮助](https://docs.openclaw.ai/help) - 更多故障排查

---

> ✅ doctor 命令是你的首选诊断工具，大多数问题都能定位。