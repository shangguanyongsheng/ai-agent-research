# Claude Code 源码深度分析报告

> 分析时间：2026-04-01
> 数据来源：[instructkr/claw-code](https://github.com/instructkr/claw-code) - Python/Rust 重构项目

---

## 一、项目概述

### 1.1 项目背景

这是 instructkr 对 Claude Code 源码泄露事件的**清洁室重构项目**（Clean-room Rewrite）：

```
时间线：
├── 2026-03-31 04:00  源码泄露事件爆发
├── 同日清晨          instructkr 开始 Python 重构
├── 2小时内           GitHub Star 破 50K（历史最快）
└── 当前              Python + Rust 双版本并行开发
```

### 1.2 重构策略

```
清洁室重构原则：
├── 不直接复制 TypeScript 源码
├── 从架构模式重新实现
├── Python 版本作为理解性重构
├── Rust 版本作为生产级实现
└── 保留元数据（工具列表、命令列表）作为参考
```

---

## 二、源码结构分析

### 2.1 目录结构

```
claw-code/
├── src/                    # Python 重构版本
│   ├── main.py             # CLI 入口
│   ├── query_engine.py     # 核心查询引擎
│   ├── tools.py            # 工具管理
│   ├── commands.py         # 命令管理
│   ├── models.py           # 数据模型
│   ├── runtime.py          # 运行时环境
│   ├── permissions.py      # 权限系统
│   ├── session_store.py    # 会话存储
│   ├── reference_data/     # 元数据快照
│   │   ├── subsystems/     # 29 个子系统描述
│   │   ├── tools_snapshot.json    # 184 个工具
│   │   └── commands_snapshot.json # 命令列表
│   └── [其他模块...]
│
├── rust/                   # Rust 生产版本
│   ├── crates/
│   │   ├── api/            # Anthropic API 客户端
│   │   ├── commands/       # 斜杠命令
│   │   ├── runtime/        # 运行时核心
│   │   ├── tools/          # 工具系统
│   │   └── rusty-claude-cli/  # CLI 入口
│   │
│   └── [配置文件...]
│
├── tests/                  # 测试验证
├── assets/                 # 文档资源
└── PARITY.md               # TypeScript vs Rust 对比分析
```

### 2.2 子系统列表（29 个）

| 序号 | 子系统 | 文件数 | 职责 |
|------|--------|--------|------|
| 1 | **cli** | 19 | 命令行界面、传输层、处理器 |
| 2 | **assistant** | ? | 助手模式（Kairos）、会话历史 |
| 3 | **bridge** | ? | IDE 桥接、远程控制 |
| 4 | **buddy** | ? | 伴侣角色系统（UI 精灵） |
| 5 | **bootstrap** | ? | 启动引导、初始化 |
| 6 | **components** | ? | React UI 组件 |
| 7 | **constants** | ? | 常量配置 |
| 8 | **coordinator** | ? | 协调器 |
| 9 | **entrypoints** | ? | 应用入口 |
| 10 | **hooks** | ? | 钩子系统 |
| 11 | **keybindings** | ? | 键绑定 |
| 12 | **memdir** | ? | 记忆目录 |
| 13 | **migrations** | ? | 迁移脚本 |
| 14 | **moreright** | ? | 扩展权限 |
| 15 | **native_ts** | ? | TypeScript 原生模块 |
| 16 | **outputStyles** | ? | 输出样式 |
| 17 | **plugins** | ? | 插件系统 |
| 18 | **remote** | ? | 远程控制 |
| 19 | **schemas** | ? | Schema 定义 |
| 20 | **screens** | ? | 屏幕/界面 |
| 21 | **server** | ? | 服务端 |
| 22 | **services** | ? | 核心服务层 |
| 23 | **skills** | ? | 技能系统 |
| 24 | **state** | ? | 状态管理 |
| 25 | **types** | ? | 类型定义 |
| 26 | **upstreamproxy** | ? | 上游代理 |
| 27 | **utils** | ? | 工具函数 |
| 28 | **vim** | ? | Vim 模式 |
| 29 | **voice** | ? | 语音系统 |

---

## 三、工具系统分析

### 3.1 工具总览（184 个工具模块）

```
工具分布：

├── AgentTool（子代理系统）        ~20 个模块
│   ├── UI                        代理界面
│   ├── agentColorManager         颜色管理
│   ├── agentDisplay              显示管理
│   ├── agentMemory               代理记忆
│   ├── agentMemorySnapshot       记忆快照
│   ├── built-in agents:          内置代理
│   │   ├── claudeCodeGuideAgent  Claude 指导代理
│   │   ├── exploreAgent          探索代理
│   │   ├── generalPurposeAgent   通用代理
│   │   ├── planAgent             规划代理
│   │   ├── verificationAgent     验证代理
│   ├── forkSubagent              分支子代理
│   ├── resumeAgent               恢复代理
│   └── runAgent                  运行代理
│
├── 文件操作工具                    ~15 个
│   ├── FileReadTool              读取文件
│   ├── FileEditTool              编辑文件
│   ├── FileWriteTool             写入文件
│   └── [其他文件工具...]
│
├── 搜索工具                        ~10 个
│   ├── GlobTool                  文件搜索
│   ├── GrepTool                  内容搜索
│   ├── ToolSearchTool            工具搜索
│   └── LSPTool                   LSP 语言服务
│
├── 命令执行工具                    ~5 个
│   ├── BashTool                  Shell 命令
│   └── [其他执行工具...]
│
├── 网络工具                        ~5 个
│   ├── WebFetchTool              获取网页
│   ├── WebSearchTool             Web 搜索
│   └── [其他网络工具...]
│
├── MCP 工具                        ~10 个
│   ├── MCPTool                   MCP 调用
│   ├── McpAuthTool               MCP 认证
│   ├── ListMcpResourcesTool      MCP 资源列表
│   └── ReadMcpResourceTool       MCP 资源读取
│
├── 调度工具                        ~5 个
│   ├── ScheduleCronTool          定时任务
│   └── [其他调度工具...]
│
├── 技能工具                        ~5 个
│   ├── SkillTool                 技能调用
│   └── [其他技能工具...]
│
├── 任务管理工具                    ~10 个
│   ├── Task*                     任务系列
│   ├── Team*                     团队系列
│   └── TodoWriteTool             Todo 写入
│
├── 配置工具                        ~5 个
│   ├── ConfigTool                配置管理
│   └── [其他配置工具...]
│
├── 远程触发工具                    ~5 个
│   ├── RemoteTriggerTool         远程触发
│   └── [其他远程工具...]
│
├── Notebook 工具                   ~5 个
│   ├── Notebook 工具              Jupyter 支持
│   └── [其他 Notebook 工具...]
│
├── REPL 工具                       ~5 个
│   ├── REPL 工具                  REPL 支持
│   └── [其他 REPL 工具...]
│
└── 其他工具                        ~剩余模块
```

### 3.2 核心工具接口

```python
# Python 重构中的工具模型
@dataclass(frozen=True)
class ToolExecution:
    name: str           # 工具名称
    source_hint: str    # 来源路径
    payload: str        # 执行参数
    handled: bool       # 是否处理
    message: str        # 执行消息

# 工具查找函数
def get_tool(name: str) -> PortingModule | None
def get_tools(simple_mode, include_mcp, permission_context)
def find_tools(query: str, limit: int)
def execute_tool(name: str, payload: str) -> ToolExecution
```

---

## 四、命令系统分析

### 4.1 命令分布

```
斜杠命令分类：

├── 核心命令
│   ├── /help            帮助
│   ├── /status          状态查看
│   ├── /clear           清除会话
│   ├── /compact         压缩上下文
│   ├── /cost            成本统计
│   ├── /version         版本信息
│   └── /export          导出会话
│
├── 模型命令
│   ├── /model           模型切换
│   └── [其他模型命令...]
│
├── 权限命令
│   ├── /permissions     权限管理
│   ├── /plan            计划模式
│   └── [其他权限命令...]
│
├── 会话命令
│   ├── /resume          恢复会话
│   ├── /session         会话管理
│   ├── /diff            差异查看
│   └── [其他会话命令...]
│
├── 记忆命令
│   ├── /memory          记忆管理
│   ├── /init            初始化项目
│   └── [其他记忆命令...]
│
├── MCP 命令
│   ├── /mcp             MCP 管理
│   └── [其他 MCP 命令...]
│
├── Skills 命令
│   ├── /skills          技能管理
│   └── [其他技能命令...]
│
├── 插件命令
│   ├── /plugin          插件管理
│   ├── /reload-plugins  重载插件
│   └── [其他插件命令...]
│
├── 代理命令
│   ├── /agents          代理管理
│   └── [其他代理命令...]
│
├── 任务命令
│   ├── /tasks           任务管理
│   └── [其他任务命令...]
│
├── 钩子命令
│   ├── /hooks           钩子管理
│   └── [其他钩子命令...]
│
├── 审查命令
│   ├── /review          审查功能
│   └── [其他审查命令...]
│
└── 其他命令
```

### 4.2 命令接口

```python
# Python 重构中的命令模型
@dataclass(frozen=True)
class CommandExecution:
    name: str           # 命令名称
    source_hint: str    # 来源路径
    prompt: str         # 输入提示
    handled: bool       # 是否处理
    message: str        # 执行消息

# 命令查找函数
def get_command(name: str) -> PortingModule | None
def get_commands(include_plugin_commands, include_skill_commands)
def find_commands(query: str, limit: int)
def execute_command(name: str, prompt: str) -> CommandExecution
```

---

## 五、核心架构分析

### 5.1 Query Engine（查询引擎）

```python
# 查询引擎配置
@dataclass(frozen=True)
class QueryEngineConfig:
    max_turns: int = 8                  # 最大循环次数
    max_budget_tokens: int = 2000       # Token 预算
    compact_after_turns: int = 12       # 压缩阈值
    structured_output: bool = False     # 结构化输出
    structured_retry_limit: int = 2     # 重试限制

# 循环结果
@dataclass(frozen=True)
class TurnResult:
    prompt: str                         # 输入
    output: str                         # 输出
    matched_commands: tuple[str, ...]   # 匹配的命令
    matched_tools: tuple[str, ...]      # 匹配的工具
    permission_denials: tuple[...]      # 权限拒绝
    usage: UsageSummary                 # Token 使用
    stop_reason: str                    # 停止原因
```

### 5.2 Agentic Loop 实现

```python
def submit_message(self, prompt, matched_commands, matched_tools, denied_tools):
    """
    核心循环逻辑：
    
    1. 检查是否达到最大循环次数
    2. 处理匹配的命令和工具
    3. 记录权限拒绝
    4. 计算 Token 使用
    5. 判断是否达到预算限制
    6. 压缩消息（如果需要）
    7. 返回结果
    """

def stream_submit_message(self, prompt, ...):
    """
    流式输出：
    
    yield {'type': 'message_start', 'session_id', 'prompt'}
    yield {'type': 'command_match', 'commands'}
    yield {'type': 'tool_match', 'tools'}
    yield {'type': 'permission_denial', 'denials'}
    yield {'type': 'message_delta', 'text'}
    yield {'type': 'message_stop', 'usage', 'stop_reason'}
    """
```

### 5.3 会话管理

```python
@dataclass
class StoredSession:
    session_id: str
    messages: tuple[str, ...]
    input_tokens: int
    output_tokens: int

def load_session(session_id: str) -> StoredSession
def save_session(session: StoredSession) -> Path
```

### 5.4 权限系统

```python
@dataclass(frozen=True)
class PermissionDenial:
    tool_name: str      # 工具名称
    reason: str         # 拒绝原因

@dataclass
class ToolPermissionContext:
    # 权限过滤
    def blocks(self, tool_name: str) -> bool
    
    @classmethod
    def from_iterables(deny_tool, deny_prefix)
```

---

## 六、TypeScript vs Rust 对比（PARITY.md 分析）

### 6.1 功能对比表

| 模块 | TypeScript | Rust | 差距 |
|------|-----------|------|------|
| **tools** | 完整 (~40 工具) | MVP (核心工具) | ⚠️ 大 |
| **hooks** | 完整执行管道 | 仅配置解析 | ⚠️ 大 |
| **plugins** | 完整生态系统 | **缺失** | ❌ 无 |
| **skills** | 注册表 + 打包 | 仅本地加载 | ⚠️ 中 |
| **cli** | 50+ 命令 | 15 命令 | ⚠️ 大 |
| **assistant** | 完整编排 | 核心循环 | ⚠️ 中 |
| **services** | 完整生态 | 核心 API | ⚠️ 大 |

### 6.2 Rust 缺失的关键功能

```
Rust 版本缺失：

1️⃣ 插件系统（plugins）
   ├── 无插件加载器
   ├── 无市场安装流程
   ├── 无插件扩展机制
   └── 完全缺失

2️⃣ 钩子执行（hooks）
   ├── PreToolUse 钩子 - 缺失
   ├── PostToolUse 钩子 - 缺失
   ├── 变更/拒绝/重写行为 - 缺失
   └── 只有配置解析，无执行

3️⃣ 工具覆盖
   ├── AskUserQuestionTool - 缺失
   ├── LSPTool - 缺失
   ├── MCP 工具系列 - 大部分缺失
   ├── ScheduleCronTool - 缺失
   ├── Task/Team 系列 - 缺失
   └── RemoteTriggerTool - 缺失

4️⃣ 命令覆盖
   ├── /agents - 缺失
   ├── /hooks - 缺失
   ├── /mcp - 缺失
   ├── /plugin - 缺失
   ├── /skills - 缺失
   ├── /plan - 缺失
   ├── /review - 缺失
   ├── /tasks - 缺失
   └── 很多其他命令缺失

5️⃣ 服务生态
   ├── 分析服务 - 缺失
   ├── 设置同步 - 缺失
   ├── 策略限制 - 缺失
   ├── 团队记忆 - 缺失
   ├── 通知服务 - 缺失
   └── 语音服务 - 缺失
```

---

## 七、Skills 转"机器语言"机制分析

### 7.1 现有转换机制

从源码分析，Skills 的转换机制是：

```
转换流程：

SKILL.md（模型语言）
        │
        │  加载到 Context Window
        │  AI 理解触发条件
        │
        ▼
┌────────────────────────────────────────┐
│  SkillTool / Skill 命令                │
│                                        │
│  src/skills/loadSkillsDir.ts           │
│  src/skills/bundledSkills.ts           │
│  src/skills/mcpSkillBuilders.ts        │
│                                        │
│  转换为：                               │
│  ├── 工具调用请求                       │
│  ├── 命令执行请求                       │
│  └── 脚本执行请求                       │
│                                        │
└────────────────────────────────────────┘
        │
        │  执行 scripts/ 中的脚本
        │  或调用其他工具
        │
        ▼
机器语言执行（Python/Bash/etc）
```

### 7.2 可能的"转换"方向

你同事说的"Skills 转机器语言/模型语言"，可能是指：

```
可能的转换方向：

1️⃣ 预编译转换（SKILL.md → JSON Schema）
   ┌────────────────────────────────────────┐
   │  转换前：                               │
   │  ---                                    │
   │  name: pdf-rotate                       │
   │  description: "旋转 PDF..."             │
   │  ---                                    │
   │  ## Quick Start                         │
   │  ```bash                                │
   │  python3 scripts/rotate.py              │
   │  ```                                    │
   │                                         │
   │  转换后（MCP Tool Definition 格式）：    │
   │  {                                      │
   │    "name": "pdf-rotate",                │
   │    "inputSchema": {                     │
   │      "type": "object",                  │
   │      "properties": {                    │
   │        "input_path": {"type": "string"},│
   │        "degrees": {"type": "integer"}   │
   │      }                                  │
   │    },                                   │
   │    "description": "Rotate PDF pages"    │
   │  }                                      │
   └────────────────────────────────────────┘
   
   好处：
   ├── 不需要加载 SKILL.md 到上下文
   ├── 直接作为工具定义注册
   ├── 更高效的触发机制
   └── 减少 Token 消耗

2️⃣ 动态解析转换（运行时转换）
   ┌────────────────────────────────────────┐
   │  流程：                                 │
   │                                         │
   │  1. 读取 SKILL.md                       │
   │  2. 解析 YAML frontmatter               │
   │  3. 解析 Markdown 代码块                │
   │  4. 提取脚本路径                        │
   │  5. 构建 ToolDefinition 对象            │
   │  6. 注册到工具注册表                    │
   │                                         │
   │  源码位置（TypeScript）：               │
   │  src/skills/loadSkillsDir.ts            │
   │  src/skills/bundledSkills.ts            │
   │  src/skills/mcpSkillBuilders.ts         │
   └────────────────────────────────────────┘

3️⃣ MCP Skill Builders（特殊转换）
   ┌────────────────────────────────────────┐
   │  MCP Skill Builder 可以：              │
   │                                         │
   │  • 将 Skills 转换为 MCP 工具            │
   │  • 通过 MCP 协议暴露 Skills            │
   │  • 允许其他 AI 系统使用 Skills         │
   │                                         │
   │  源码位置：                             │
   │  src/skills/mcpSkillBuilders.ts        │
   └────────────────────────────────────────┘
```

---

## 八、设计思想总结

### 8.1 Claude Code 的核心设计模式

```
设计模式总结：

1️⃣ Everything is a Tool
   ├── 184 个工具模块
   ├── 统一接口
   ├── 权限可控
   └── 独立隔离

2️⃣ Progressive Disclosure
   ├── 三级加载（Metadata → SKILL.md → Resources）
   ├── Token 效率优化
   └── 按需加载详细内容

3️⃣ Permission Model
   ├── Allow / Deny / Ask
   ├── 工具级权限
   ├── 文件级权限
   └── 命令级权限

4️⃣ Streaming Everything
   ├── 流式响应
   ├── 实时反馈
   ├── 可中断执行

5️⃣ Multi-Agent Orchestration
   ├── 子代理系统（AgentTool）
   ├── 独立上下文
   ├── 并行执行
   └── 结果摘要

6️⃣ Plugin Architecture
   ├── 插件生命周期
   ├── 市场安装
   ├── 扩展机制
   └── 钩子注入

7️⃣ Hooks System
   ├── PreToolUse
   ├── PostToolUse
   ├── 变更/拒绝/重写
   └── 事件驱动
```

### 8.2 架构层级

```
架构层级图：

┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code 架构层级                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Layer 0: Runtime (运行时)                                      │
│  ├── Entry points                                              │
│  ├── Bootstrap                                                 │
│  ├── Environment                                               │
│  └── Session lifecycle                                         │
│                                                                 │
│  Layer 1: CLI (命令行界面)                                      │
│  ├── Transports (传输层)                                       │
│  ├── Handlers (处理器)                                         │
│  ├── Commands (斜杠命令)                                        │
│  └── Structured/Remote IO                                      │
│                                                                 │
│  Layer 2: Services (服务层)                                     │
│  ├── API Client                                                │
│  ├── OAuth                                                     │
│  ├── MCP                                                       │
│  ├── Plugins                                                   │
│  ├── Analytics                                                 │
│  ├── Voice                                                     │
│  └── Notifier                                                  │
│                                                                 │
│  Layer 3: Assistant (助手层)                                    │
│  ├── Query Engine                                              │
│  ├── Session History                                           │
│  ├── Tool Orchestration                                        │
│  ├── Streaming Executor                                        │
│  └── Hook Integration                                          │
│                                                                 │
│  Layer 4: Tools (工具层)                                        │
│  ├── File Tools                                                │
│  ├── Search Tools                                              │
│  ├── Execution Tools                                           │
│  ├── Web Tools                                                 │
│  ├── Agent Tools                                               │
│  ├── MCP Tools                                                 │
│  └── Skill Tools                                               │
│                                                                 │
│  Layer 5: Extensions (扩展层)                                   │
│  ├── Skills                                                    │
│  ├── Hooks                                                     │
│  ├── Plugins                                                   │
│  ├── MCP Servers                                               │
│  └── Subagents                                                 │
│                                                                 │
│  Layer 6: State (状态层)                                        │
│  ├── Memory                                                    │
│  ├── Session Store                                             │
│  ├── Config                                                    │
│  ├── Permissions                                               │
│  └── Transcript                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 九、OpenClaw 落地启示

### 9.1 可以借鉴的设计

| Claude Code 设计 | OpenClaw 应用 | 实现建议 |
|------------------|---------------|----------|
| 184 工具模块 | MCP 扩展 | 通过 MCP 补充工具缺口 |
| Skills 系统 | Skills | 保持 SKILL.md 格式兼容 |
| Hooks 系统 | 可新增 | PreToolUse/PostToolUse 钩子 |
| 子代理系统 | sessions_spawn | 已有，可优化 |
| 插件系统 | 可新增 | 插件市场机制 |
| 流式输出 | 已支持 | 优化实时体验 |

### 9.2 Skills 转换建议

如果你想做 Skills 转换：

```
建议实现：

1️⃣ 预编译转换
   ├── SKILL.md → JSON Tool Definition
   ├── 注册为 MCP 工具
   ├── 减少上下文加载
   └── 提高触发效率

2️⃣ Skill → MCP Bridge
   ├── 使用 mcpSkillBuilders 逻辑
   ├── 暴露 Skills 为 MCP 工具
   ├── 允许其他系统调用
   └── 统一工具接口

3️⃣ 动态注册
   ├── 启动时扫描 Skills 目录
   ├── 解析 SKILL.md
   ├── 构建 ToolDefinition
   ├── 注册到工具注册表
   └── 无需加载完整内容
```

---

## 十、总结

### 10.1 源码规模

```
规模统计：

├── TypeScript 源码（原始）
│   ├── ~1,900 文件
│   ├── ~512,000 行代码
│   ├── 29 个子系统
│   ├── 184 个工具模块
│   └── ~50 个斜杠命令
│
├── Python 重构（instructkr）
│   ├── 98 文件
│   ├── 元数据快照保留
│   ├── 清洁室重构
│   └── 理解性实现
│
└── Rust 版本（进行中）
│   ├── 6 个 crates
│   ├── MVP 工具集
│   ├── 核心循环实现
│   └── 缺失插件/钩子/完整工具
```

### 10.2 关键发现

1. **工具数量惊人**：184 个工具模块，远超预期
2. **子系统复杂**：29 个子系统，分层清晰
3. **插件系统关键**：TypeScript 有完整插件生态，Rust 缺失
4. **钩子系统重要**：PreToolUse/PostToolUse 是核心安全机制
5. **Skills 可转换**：有 mcpSkillBuilders 机制，可转为 MCP 工具

---

## 参考资料

- [instructkr/claw-code](https://github.com/instructkr/claw-code) - 源码分析项目
- [PARITY.md](PARITY.md) - TypeScript vs Rust 功能对比
- [Claude Code 源码泄露研究报告](../../docs/Claude%20Code%20%E6%BA%90%E7%A0%81%E6%B3%84%E9%9C%B2%E7%A0%94%E7%A9%B6%E6%8A%A5%E5%91%8A.md)

---

**报告生成时间**：2026-04-01
**数据来源**：instructkr/claw-code GitHub 仓库