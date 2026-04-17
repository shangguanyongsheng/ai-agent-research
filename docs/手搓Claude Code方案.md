# 手搓 Claude Code — 完整方案文档

> 项目目标：从零构建一个类 Claude Code 的 CLI 编程助手，**学习 AI 应用落地的完整工程过程**。
> 参考来源：泄露的 Claude Code 源码架构分析 + instructkr Python 重构项目 + 公开 API 文档。

---

## 一、项目定位

### 1.1 做什么

一个终端里的 AI 编程助手，能：
- 对话式交互，理解用户的编程意图
- 读写文件、执行命令、搜索代码
- 启动子代理并行处理复杂任务
- 跨会话保持记忆和上下文
- 通过 Skills/Hooks/MCP 扩展能力

### 1.2 不做什么

- 不是商业产品，不追求生产级稳定性
- 不直接复制泄露的源码（clean-room 实现）
- 不追求 184 个工具全覆盖，优先核心能力

### 1.3 学习价值

通过从零构建，理解以下工程问题：
1. **LLM 如何被编排成 Agent** — 不是简单的 API 调用，而是循环、工具、决策的闭环
2. **工具系统如何设计** — 统一接口、权限控制、隔离执行
3. **多代理如何协作** — 上下文隔离、并行执行、结果聚合
4. **状态如何持久化** — 跨会话记忆、项目上下文、配置管理
5. **扩展机制如何工作** — Skills、Hooks、MCP 的加载和触发

---

## 二、参考架构总结

### 2.1 泄露源码的 7 层架构

```
Layer 6: State (状态层)    — Memory / Session / Config / Permissions
Layer 5: Extensions (扩展层) — Skills / Hooks / Plugins / MCP / Subagents
Layer 4: Tools (工具层)     — File / Search / Execution / Web / Agent / MCP
Layer 3: Assistant (助手层)  — Query Engine / Session History / Hook Integration
Layer 2: Services (服务层)   — API Client / OAuth / MCP / Plugins / Analytics
Layer 1: CLI (命令行层)     — Transports / Handlers / Commands / IO
Layer 0: Runtime (运行时层)  — Entry / Bootstrap / Environment / Lifecycle
```

### 2.2 核心设计模式

| 模式 | 说明 | 我们的应用 |
|------|------|-----------|
| Everything is a Tool | 所有能力统一为工具，接口一致、权限可控 | 工具抽象基类 + 注册表 |
| Progressive Disclosure | 三级加载：元数据 → 详情 → 资源，按需加载省 Token | Skills 按需加载 |
| Permission Model | 每个工具独立 allow/deny/ask | 工具级权限检查 |
| Streaming | 流式输出 + 流式事件（tool 匹配/拒绝） | Rich 实时渲染 |
| Multi-Agent | 子代理独立上下文，并行执行后聚合 | AgentTool + 隔离 loop |
| Hooks | PreToolUse / PostToolUse 事件驱动 | 钩子回调机制 |

### 2.3 关键数据规模

- 泄露源码：~1,900 TypeScript 文件，~512,000 行
- 工具模块：184 个（核心 ~40 个）
- 斜杠命令：~50 个
- 子系统：29 个
- **我们目标**：Phase 1 实现 5 核心工具 + 5 斜杠命令 + 基础循环

---

## 三、技术选型

### 3.1 语言与框架

| 选择 | 理由 |
|------|------|
| **Python 3.10+** | AI 生态第一语言，anthropic SDK 原生支持，快速迭代 |
| **anthropic SDK** | 官方 Python 客户端，streaming / tool_use 原生支持 |
| **prompt_toolkit** | 成熟的 Python REPL 框架，支持历史、补全、样式 |
| **Rich** | 终端富文本渲染（Markdown、Panel、Table） |
| **Pydantic v2** | 数据模型验证，与 anthropic SDK 风格一致 |
| **httpx** | 异步 HTTP，用于 WebFetch / WebSearch |

### 3.2 为什么不选其他方案

- **Node.js/TypeScript**：接近原版但学习成本高，TS 类型系统对快速原型偏重
- **Rust**：生产级但开发慢，不适合"学习理解"场景
- **Go**：并发好但 AI 生态弱，anthropic SDK 社区支持少

### 3.3 项目结构

```
my-claude-code/
├── pyproject.toml              # 项目配置
├── config.py                   # 全局配置（API key、模型、权限）
│
├── src/
│   ├── __init__.py
│   ├── main.py                 # CLI 入口 + REPL 循环
│   ├── loop.py                 # Agentic Loop 核心（Query Engine 简化版）
│   ├── permissions.py          # 权限系统
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── client.py           # Anthropic API 封装（streaming + 非 streaming）
│   │   └── models.py           # 消息/工具定义的数据模型
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── base.py             # Tool 抽象基类
│   │   ├── registry.py         # 工具注册表 + 搜索
│   │   ├── file_tools.py       # Read / Write / Edit / Glob
│   │   ├── bash_tool.py        # Bash 命令执行
│   │   ├── grep_tool.py        # 正则内容搜索
│   │   ├── web_tools.py        # WebFetch / WebSearch
│   │   └── agent_tool.py       # 子代理启动
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py             # Agent 抽象
│   │   ├── explore.py          # 代码探索代理
│   │   ├── plan.py             # 规划代理
│   │   └── general.py          # 通用任务代理
│   │
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── session.py          # 会话历史存储
│   │   ├── project.py          # 项目上下文（CLAUDE.md 等）
│   │   └── user.py             # 用户偏好
│   │
│   ├── skills/
│   │   ├── __init__.py
│   │   ├── loader.py           # SKILL.md 解析
│   │   └── registry.py         # 技能注册
│   │
│   ├── hooks/
│   │   ├── __init__.py
│   │   └── engine.py           # PreToolUse / PostToolUse 钩子
│   │
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── base.py             # 斜杠命令抽象
│   │   └── builtin.py          # 内置命令（/help, /clear, /model...）
│   │
│   └── ui/
│       ├── __init__.py
│       ├── render.py           # Rich 渲染器（流式文本、工具状态）
│       └── prompt.py           # prompt_toolkit 集成
│
├── tests/
│   ├── test_tools.py
│   ├── test_loop.py
│   └── test_permissions.py
│
└── docs/
    └── architecture.md         # 架构文档
```

---

## 四、分阶段实现计划

### Phase 1: 最小可用核心 (MVP) — 2-3 天

**目标**：跑通 "用户输入 → LLM → 工具调用 → 执行 → 输出" 完整循环

#### 1.1 项目骨架
- [ ] `pyproject.toml` — 依赖声明
- [ ] `config.py` — 从环境变量/配置文件加载设置
- [ ] `src/main.py` — REPL 入口循环（prompt_toolkit）

#### 1.2 API 客户端
- [ ] `src/api/client.py` — Anthropic SDK 封装
  - `create_message()` — 非流式调用
  - `stream_message()` — 流式调用，yield 事件
- [ ] `src/api/models.py` — 数据模型
  - `ToolDefinition` — 工具定义（name, description, input_schema）
  - `ToolResult` — 工具执行结果（name, output, is_error）

#### 1.3 核心工具（5 个）
- [ ] `ReadTool` — 读取文件，支持行号限制
- [ ] `WriteTool` — 创建/覆盖文件
- [ ] `EditTool` — 精确字符串替换
- [ ] `GlobTool` — 文件模式搜索
- [ ] `BashTool` — Shell 命令执行，超时控制

#### 1.4 工具系统基础设施
- [ ] `BaseTool` — 抽象基类（definition + execute）
- [ ] `ToolRegistry` — 注册表 + API 格式转换 + 搜索
- [ ] `permissions.py` — allow/deny/ask 三级权限

#### 1.5 Agentic Loop
- [ ] `src/loop.py` — 核心循环
  - 维护消息历史
  - 调用 API
  - 解析 tool_use 响应
  - 权限检查
  - 执行工具
  - 将结果追加历史
  - 循环直到无 tool_use 或达 max_turns

**验收标准**：
```bash
$ export ANTHROPIC_API_KEY=xxx
$ python -m src.main
mycc> 帮我创建一个 hello.py，内容是打印 Hello World
```
应该能看到：LLM 调用 WriteTool → 用户确认 → 文件创建 → LLM 回复完成。

---

### Phase 2: 工具扩展 + 搜索 — 1-2 天

**目标**：覆盖日常编码所需的工具

- [ ] `GrepTool` — 正则内容搜索（基于 ripgrep 或 Python re）
- [ ] `WebFetchTool` — 获取网页内容（httpx + 转 markdown）
- [ ] `WebSearchTool` — 网络搜索（对接搜索 API）
- [ ] 图片读取（base64 编码传给 LLM）
- [ ] PDF 读取（pdfplumber 提取文本）
- [ ] 工具权限上下文（文件级白名单/黑名单）
- [ ] `ToolSearchTool` — 按名称/描述搜索可用工具

**学习重点**：理解 Claude Code 如何用工具扩展 LLM 的能力边界。

---

### Phase 3: 多代理系统 — 2-3 天

**目标**：实现子代理（swarm）能力

- [ ] `AgentTool` — 启动子代理的接口
  - 输入：prompt, subagent_type, model
  - 输出：子代理执行摘要
- [ ] `BaseAgent` — 代理抽象（prompt + tools + memory）
- [ ] `ExploreAgent` — 专注代码探索
- [ ] `PlanAgent` — 专注规划
- [ ] `GeneralAgent` — 通用任务
- [ ] 上下文隔离（子代理有独立的 history）
- [ ] 并行执行（asyncio.gather）
- [ ] 结果摘要（子代理输出压缩后返回主循环）

**学习重点**：理解多代理如何解决"一个模型上下文不够"的问题。

---

### Phase 4: 持久化记忆 — 1-2 天

**目标**：跨会话保持上下文

- [ ] 会话历史存储（JSON 文件，按 session_id）
- [ ] 项目上下文自动加载（`.claude/CLAUDE.md`）
- [ ] 用户偏好存储（`~/.claude/settings.json`）
- [ ] 跨会话记忆（用户说"记住 X"→ 写入文件 → 下次加载）
- [ ] 会话恢复（`/resume` 命令）

**学习重点**：理解"记忆"不只是聊天记录，还包括偏好、项目规则、决策历史。

---

### Phase 5: 扩展系统 — 2-3 天

**目标**：Skills + Hooks + 斜杠命令

#### 5.1 Skills 系统
- [ ] `SKILL.md` 格式解析（YAML frontmatter + markdown body）
- [ ] 启动时扫描 skills 目录
- [ ] Skills 触发：用户提到 skill 名称时自动加载
- [ ] Skills 作为工具暴露给 LLM

#### 5.2 Hooks 系统
- [ ] `settings.json` 中 hooks 配置解析
- [ ] `PreToolUse` — 工具执行前拦截
- [ ] `PostToolUse` — 工具执行后处理
- [ ] 钩子行为：allow / deny / modify

#### 5.3 斜杠命令
- [ ] `/help` — 帮助
- [ ] `/clear` — 清除历史
- [ ] `/compact` — 上下文压缩
- [ ] `/model` — 模型切换
- [ ] `/cost` — Token 成本统计
- [ ] `/tools` — 列出工具
- [ ] `/memory` — 查看记忆
- [ ] `/init` — 初始化项目记忆

#### 5.4 MCP 支持（可选）
- [ ] MCP Server 连接
- [ ] MCP 工具发现与调用

**学习重点**：理解 Claude Code 如何通过 Skills/Hooks/MCP 实现"用户可扩展的能力"。

---

### Phase 6: UI 优化 + 高级特性 — 2-3 天

- [ ] 流式文本实时渲染（token by token）
- [ ] 工具执行状态可视化（pending → running → done）
- [ ] 多模型切换（Sonnet / Opus / Haiku）
- [ ] 上下文压缩（达到 token 限制时自动精简历史）
- [ ] 成本统计（每次调用的 input/output/token 费用）
- [ ] 会话导出/导入
- [ ] 计划模式（Plan mode — 先规划再执行）
- [ ] 语法高亮（代码输出）

---

## 五、关键实现细节

### 5.1 Agentic Loop 伪代码

```python
def run_turn(self, user_prompt):
    # 1. 追加用户消息到历史
    self.history.append({"role": "user", "content": user_prompt})

    # 2. 进入循环
    for turn in range(max_turns):
        # 3. 调用 LLM
        response = api.create_message(
            model=model,
            messages=history,
            tools=registry.to_api_tools(),
        )

        # 4. 提取文本和工具调用
        text = extract_text(response)
        tool_uses = extract_tool_uses(response)

        # 5. 显示文本
        if text: render(text)

        # 6. 无工具调用 → 结束
        if not tool_uses: break

        # 7. 对每个工具调用：权限检查 → 执行 → 结果
        tool_results = []
        for tool_use in tool_uses:
            if check_permission(tool_use.name) == "deny":
                tool_results.append(denied_result(tool_use))
                continue
            result = registry.get(tool_use.name).execute(tool_use.input)
            tool_results.append(tool_result(tool_use, result))

        # 8. 将 assistant 响应 + 工具结果追加历史
        history.append(response)
        history.extend(tool_results)
```

### 5.2 Tool 接口设计

```python
class BaseTool(ABC):
    @property
    @abstractmethod
    def definition(self) -> ToolDefinition:
        """返回工具的 API 格式定义"""

    @abstractmethod
    def execute(self, params: dict) -> ToolResult:
        """执行工具，返回结果"""
```

这与 Claude Code 的设计一致——每个工具是独立的、可组合的单元。

### 5.3 权限流程

```
用户输入 → LLM 响应 → 检测到 tool_use
                              │
                    ┌─────────┼─────────┐
                    ▼         ▼         ▼
               allow      deny        ask
               (直接执行)  (跳过)    (用户确认 y/n)
                    │         │         │
                    ▼         ▼         ▼
               执行工具    返回错误   用户选择后执行
```

### 5.4 Skills 转换流程

```
SKILL.md (模型语言)
    │
    ├─ YAML frontmatter → name, description, trigger
    ├─ Markdown body → 执行指令（给 LLM 看）
    └─ scripts/ → 实际可执行脚本
    │
    ▼
注册为 ToolDefinition → 暴露给 LLM 调用
    │
    ▼
LLM 调用 Skill → 加载指令到上下文 → 执行脚本
```

---

## 六、依赖参考

### 6.1 instructkr Python 重构参考

instructkr 的项目（`instructkr/claw-code`）是 clean-room 重构，可以作为架构参考：
- `query_engine.py` → 我们的 `loop.py`
- `tools.py` → 我们的 `tools/` 目录
- `permissions.py` → 我们的 `permissions.py`
- `session_store.py` → 我们的 `memory/session.py`
- `commands.py` → 我们的 `commands/` 目录

### 6.2 泄露源码参考

泄露报告中提取的关键信息：
- 工具数量 184 → 我们 Phase 1 做 5 个，Phase 2 扩展到 ~10 个
- 29 个子系统 → 我们聚焦核心 5-6 个
- 权限模型 `allow/deny/ask` → 直接采用
- Streaming 一切 → 我们的 UI 也做流式

---

## 七、风险与应对

| 风险 | 影响 | 应对 |
|------|------|------|
| API 配额限制 | 无法充分测试 | 使用 Haiku 模型降低费用，mock 测试 |
| 工具执行安全 | 恶意命令 | 严格权限控制，deny 危险前缀 |
| 上下文溢出 | 长对话失败 | Phase 6 实现 compact |
| 学习曲线 | 进展慢 | 每个 Phase 独立验收，不追求完美 |

---

## 八、学习里程碑

```
Week 1: MVP 跑通
├── 能对话、读写文件、执行命令
├── 理解了 Agentic Loop 的本质
└── 理解了"工具是 LLM 的手脚"

Week 2: 工具 + 代理
├── 理解了"工具扩展 = 能力扩展"
├── 理解了"多代理 = 并行化 + 专业化"
└── 能用自己的话解释整个架构

Week 3: 记忆 + 扩展
├── 理解了"记忆 = 跨会话智能"
├── 理解了"Skills/Hooks = 用户可编程扩展"
└── 能独立设计一个新工具或新技能

Week 4: 优化 + 总结
├── 完整的 CLI 体验
├── 写一份架构总结文档
└── 对比原版 Claude Code，理解差距和取舍
```

---

## 九、下一步

**当前阶段**：方案设计完成，等待确认。

**确认后开始**：Phase 1 — 项目骨架 + MVP 核心循环。

预计 Phase 1 完成时间：2-3 天。

---

_📅 创建日期：2026-04-17_
_📋 版本：v1.0_
