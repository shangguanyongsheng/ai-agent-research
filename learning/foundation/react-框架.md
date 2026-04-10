# ReAct 框架

> 知识分支：foundation（基础概念）

---

## 🎯 学习目标

理解 ReAct 框架的核心循环：Thought → Action → Observation → Reflection

---

## 第一步：概念解释

### ReAct 是什么？

**给小孩解释**：
> ReAct 就像做题四步法：思考 → 写答案 → 检查 → 改错。如果错了，就重新思考再做一遍。

**一句话定义**：
> ReAct = Reasoning + Acting（推理 + 行动）

### 核心循环

```
┌─────────────────────────────────────────────────────┐
│                   ReAct 循环                         │
│                                                     │
│   Thought（思考）                                    │
│      ↓                                              │
│   Action（行动）                                     │
│      ↓                                              │
│   Observation（观察）                                │
│      ↓                                              │
│   失败了？── 是 ──► Reflection（反思）──┐           │
│      │                                  │           │
│      否                                 │           │
│      ↓                                  │           │
│   成功！◄───────────────────────────────┘           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

| 步骤 | 说明 | 类比 |
|------|------|------|
| Thought | 思考如何完成任务 | 做题前先想思路 |
| Action | 执行具体操作 | 写答案 |
| Observation | 检查执行结果 | 检查答案 |
| Reflection | 如果失败，反思原因 | 找错误原因 |

---

## 第二步：类比理解

### 类比 1：程序员修 Bug

| ReAct 步骤 | 程序员修 Bug | Agent 分析数据 |
|------------|-------------|----------------|
| Thought | "这个 Bug 可能是空指针" | "用户想按类型分组" |
| Action | 打断点、看日志 | 执行分组代码 |
| Observation | 确实是空指针 | 结果正确/错误 |
| Reflection | "下次要加非空判断" | "列名拼写错误" |

### 类比 2：医生诊断

| ReAct 步骤 | 医生诊断 | Agent 处理任务 |
|------------|---------|---------------|
| Thought | "症状可能是感冒" | "需要调用搜索工具" |
| Action | 开检查单 | 调用工具 |
| Observation | 检查结果显示... | 工具返回结果 |
| Reflection | "原来不是感冒，是过敏" | "需要换个方法" |

---

## 第三步：实际例子

### 任务：分析销售数据

```
用户：帮我分析 sales.csv 的销售趋势

Step 1 - Thought:
"我需要先读取文件，然后分析数据，最后生成报告"

Step 2 - Action:
执行：read_file("sales.csv")

Step 3 - Observation:
结果：成功读取，数据包含日期、产品、销售额

Step 4 - Thought:
"现在需要按日期分组，计算销售趋势"

Step 5 - Action:
执行：df.groupby('date').sum()

Step 6 - Observation:
结果：成功！销售额呈上升趋势

Step 7 - 成功！输出报告
```

### 失败时的 Reflection

```
Step 2 - Action:
执行：read_file("sales.cs")  # 文件名打错了

Step 3 - Observation:
结果：Error - 文件不存在

Step 4 - Reflection:
"文件名可能有误，让我列出目录看看实际文件名"

Step 5 - Action:
执行：list_files()

Step 6 - Observation:
结果：文件名是 "sales.csv"，不是 "sales.cs"

Step 7 - Thought:
"找到正确的文件名了，重新读取"

Step 8 - Action:
执行：read_file("sales.csv")  # 正确！

...继续后续步骤
```

---

## 第四步：知识关联

### ReAct 在知识体系中的位置

```
AI Agent 知识体系
│
├── foundation（基础概念）
│   ├── Agent 定义
│   ├── Agent Harness
│   └── ReAct 框架 ◄── 你在这里
│
├── evolution（进化系统）
│   └── 进化引擎会分析 ReAct 的 Reflection
│
└── advanced（进阶主题）
    └── Prompt Engineering 会影响 Thought 质量
```

### 与其他概念的关系

- **Planning**：Thought 是 Planning 的体现
- **Tools**：Action 需要调用 Tools
- **Evolution**：Reflection 的积累促成进化
- **Memory**：Observation 存入工作记忆

---

## 🧪 动手实验

### 实验：观察 ReAct 循环

```bash
# 使用 Claude Code，让它显示思考过程
claude

> 请帮我分析当前目录的代码结构，并总结

# 观察 Agent 如何：
# 1. Thought：先列出目录结构
# 2. Action：执行 ls -la
# 3. Observation：看到文件列表
# 4. Thought：决定读取关键文件
# 5. Action：读取 README.md
# ... 循环直到完成任务
```

---

## ❓ 思考题

1. 为什么需要 Reflection（反思）步骤？没有它会有什么问题？
2. ReAct 循环最多应该重试几次？为什么？
3. Thought 的质量如何影响最终结果？

---

## 📚 延伸阅读

- [Planning](./planning.md) - 理解任务分解和规划
- [进化引擎](../evolution/进化引擎.md) - 理解如何从 Reflection 中学习
- [原始文档](../../learning/01-react-framework.md) - 完整技术文档

---

_📅 更新日期：2026-03-23_
_🐒 毛猴子整理_