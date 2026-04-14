# 09-Serverless部署

> 使用 Daytona 或 Modal 的 Serverless 后端，让 Hermes 在空闲时几乎零成本运行。

---

## 第一步：概念解释

### 什么是 Serverless 部署？

**Serverless** 意味着：
- Agent 环境"休眠"时不付费
- 有请求时自动唤醒
- 持久化环境（安装的包/文件不丢失）

Hermes 支持两个 Serverless 后端：
- **Daytona**：云沙盒工作空间
- **Modal**：云端执行

---

### 与传统部署的对比

| 部署方式 | 成本 | 持久化 | 唤醒 |
|----------|------|--------|------|
| 本地 | 免费 | 是 | 即时 |
| VPS ($5/月) | 固定 | 是 | 即时 |
| Daytona | 空闲免费 | 是 | 按需 |
| Modal | 空闲免费 | 部分 | 按需 |

---

## 第二步：类比理解

### Serverless = 智能休眠的办公空间

传统 VPS → 24/7 租用办公室，即使没人也付费
Serverless → 智能办公室：
  - 有人时立即可用
  - 无人时自动休眠（不付费）
  - 所有东西保留（持久化）

**类比：**

```
传统 VPS：
- 每月 $5，不管你用不用
- 24/7 在线

Daytona/Modal：
- 用时唤醒（几秒启动）
- 闲时休眠（不付费）
- 下次唤醒，环境还是你上次的样子
  - pip install 的包还在
  - 创建的文件还在
  - 配置还在
```

---

## 第三步：代码/实践

### Modal 后端

#### 安装配置

```bash
pip install modal
modal setup  # 认证
hermes config set terminal.backend modal
```

#### 配置选项

```yaml
# ~/.hermes/config.yaml
terminal:
  backend: modal
  container_cpu: 1
  container_memory: 5120  # MB
  container_disk: 51200   # MB
  container_persistent: true
```

#### 工作原理

- Modal 运行时按需启动
- 空闲时自动休眠
- `container_persistent: true` 保持文件系统

---

### Daytona 后端

#### 安装配置

```bash
# 安装 Daytona CLI
# 参考：https://daytona.io

hermes config set terminal.backend daytona
```

#### 配置选项

```yaml
# ~/.hermes/config.yaml
terminal:
  backend: daytona
  container_cpu: 1
  container_memory: 5120
  container_disk: 51200
  container_persistent: true
```

#### 工作原理

- Daytona 提供持久化工作空间
- 空闲时休眠
- 唤醒时恢复完整环境

---

### 混合部署策略

```
┌────────────────────────────────────────────┐
│           本地机器                          │
│                                            │
│  Gateway（前台）                           │
│  接收消息，管理会话                        │
└────────────────────────────────────────────┘
                    ↓ 指令
┌────────────────────────────────────────────┐
│           Daytona/Modal（云端）            │
│                                            │
│  Terminal Backend                          │
│  执行终端命令，持久化环境                  │
│  空闲时休眠，不付费                        │
└────────────────────────────────────────────┘
```

**推荐架构：**
- Gateway 在本地（或低成本 VPS）24/7 运行
- Terminal Backend 在 Daytona/Modal Serverless
- 这样 Gateway 随时可接收消息，终端环境空闲时休眠

---

### 成本优化

#### Gateway 部署

```bash
# Gateway 需 24/7 运行
# 最低成本选项：

# 1. 本地机器（如果总是开机）
hermes gateway start

# 2. 低成本 VPS（$5/月）
# 安装 Hermes，运行 Gateway

# 3. Home Assistant（如果已有）
hermes gateway start
```

#### Terminal 部署

```bash
# Terminal 可以 Serverless
hermes config set terminal.backend modal  # 或 daytona

# 这样：
# - Gateway 在 $5 VPS
# - Terminal 在 Modal（空闲免费）
# → 总成本接近 $5/月
```

---

### 其他终端后端对比

| 后端 | 成本 | 持久化 | 安全 | 用途 |
|------|------|--------|------|------|
| local | 免费 | 是 | 低 | 开发、信任任务 |
| docker | 免费 | 是 | 高 | 本地隔离 |
| ssh | VPS | 是 | 高 | Agent 无法修改自己 |
| singularity | 免费 | 是 | 高 | HPC 集群 |
| modal | Serverless | 部分 | 高 | 云端执行 |
| daytona | Serverless | 是 | 高 | 持久工作空间 |

---

## 第四步：知识关联

### Serverless 与其他系统的关系

```
┌─────────────────┐
│   Gateway       │  ← 需 24/7 运行
│   (消息接收)    │     推荐本地/低成本 VPS
└─────────────────┘
        ↓
┌─────────────────┐
│   Terminal      │  ← 可 Serverless
│   Backend       │     Daytona/Modal 空闲免费
└─────────────────┘
        ↓
┌─────────────────┐
│   Cron Jobs     │  ← 也用 Terminal Backend
│   (定时任务)    │     Serverless 执行
└─────────────────┘
```

### 相关概念

| 概念 | 关系 |
|------|------|
| [架构详解](03-架构详解.md) | environments/ 目录 |
| [多平台网关](06-多平台网关.md) | Gateway 部署策略 |
| [Cron 调度](07-Cron调度.md) | Cron 执行用 Terminal Backend |

---

## 🎯 关键理解

1. **Serverless = 空闲免费**：休眠时不付费
2. **持久化**：安装的包、文件不丢失
3. **混合部署**：Gateway 24/7，Terminal Serverless
4. **成本优化**：接近 $5/月（仅 Gateway）
5. **唤醒延迟**：Serverless 启动需几秒

---

## 📋 最佳实践

### 推荐架构

```
本地机器（或 $5 VPS）
├── Gateway（24/7）
├── Session Storage
└── Cron Scheduler

Daytona/Modal（Serverless）
├── Terminal Backend
├── 持久化文件系统
└── 空闲时休眠
```

### 不适合 Serverless 的场景

```markdown
❌ 不适合：
- 需即时响应的任务（唤醒延迟）
- 频繁执行的 Cron（每次唤醒）
- 需大量本地文件的任务

✅ 适合：
- 按需执行的终端命令
- 不频繁的 Cron 任务
- 需云端环境的任务
```

### 配置检查

```bash
hermes config show  # 查看当前配置
hermes doctor       # 诊断问题
```

---

## 🔗 官方文档

- [Modal 官网](https://modal.com)
- [Daytona 官网](https://daytona.io)
- [Hermes Terminal Backends](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools#terminal-backends)

---

*费曼学习法文档 - Hermes Agent*