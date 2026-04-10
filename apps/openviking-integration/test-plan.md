# OpenViking 集成测试计划

> **qa-agent 测试文档**

---

## 🧪 测试范围

### 1. 环境测试

| 测试项 | 命令 | 预期结果 |
|--------|------|----------|
| Go 版本 | `go version` | ≥ 1.22 |
| OpenViking CLI | `ov_cli --version` | 安装成功 |
| Python 依赖 | `pip show openviking` | 已安装 |

### 2. 功能测试

| 测试项 | 描述 | 状态 |
|--------|------|------|
| 配置加载 | 加载 ov.conf | ⏳ 待测试 |
| 工作空间创建 | 创建 openclaw 工作空间 | ⏳ 待测试 |
| 记忆存储 | 存储测试记忆 | ⏳ 待测试 |
| 语义搜索 | 搜索测试记忆 | ⏳ 待测试 |
| 分层加载 | L0/L1/L2 加载 | ⏳ 待测试 |

### 3. 集成测试

| 测试项 | 描述 | 状态 |
|--------|------|------|
| OpenClaw 连接 | 与 OpenClaw Gateway 集成 | ⏳ 待测试 |
| 多 Agent 支持 | 多个 Agent 独立工作空间 | ⏳ 待测试 |
| 共享技能 | 跨 Agent 技能共享 | ⏳ 待测试 |

---

## 📋 测试用例

### TC-001: OpenViking 安装验证

```bash
# 步骤 1: 检查 Go
go version

# 步骤 2: 检查 OpenViking CLI
ov_cli --version

# 步骤 3: 检查 Python 包
pip show openviking
```

### TC-002: 配置文件验证

```bash
# 步骤 1: 创建配置目录
mkdir -p ~/.openviking

# 步骤 2: 创建配置文件
cat > ~/.openviking/ov.conf << 'EOF'
{
  "storage": {
    "workspace": "/home/admin/.openviking/workspaces/openclaw"
  },
  ...
}
EOF

# 步骤 3: 验证配置
ov_cli config validate
```

### TC-003: 记忆存储测试

```bash
# 步骤 1: 创建测试记忆
ov_cli memory create --agent test-agent --content "测试记忆内容"

# 步骤 2: 搜索记忆
ov_cli memory search --query "测试记忆"

# 步骤 3: 验证结果
# 应返回测试记忆内容
```

---

## 📊 测试报告模板

| 测试项 | 通过 | 失败 | 备注 |
|--------|------|------|------|
| TC-001 | - | - | - |
| TC-002 | - | - | - |
| TC-003 | - | - | - |

---

*qa-agent 测试计划*