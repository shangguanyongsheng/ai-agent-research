# 🟠 10 — 如何编写 Agent 自主循环指令？（Karpathy program.md 拆解）

> 💡 一句话：**用一份 Markdown 文件指挥 AI Agent 自主干活、自主试错、自主记录，你睡觉它工作。**

---

## 一个比喻

你雇了一个超级研究员，但你不会 24 小时盯着他。怎么办？

给他一份 **《自主工作手册》**：
- 🎯 你的目标是什么
- 🟢 你可以做什么
- 🔴 你不可以做什么
- 📊 你怎么记录结果
- 🔄 你遇到问题怎么办
- 🚨 你什么时候该继续，什么时候该停

**program.md 就是 Agent 的自主工作手册。**

---

## 原版 program.md 核心结构拆解

Karpathy 的 program.md 全文 114 行，分为 5 个部分：

```
1. Setup（设置）      → 实验初始化流程
2. Experimentation（实验）→ 目标和边界
3. Output format（输出） → 结果读取方式
4. Logging results（日志）→ 结果记录格式
5. Experiment loop（循环）→ 永不停止的自主循环
```

### 第 1 部分：Setup（设置）

```markdown
1. 约定运行标签（基于日期，如 mar5）
2. 创建专用分支：git checkout -b autoresearch/mar5
3. 读取相关文件：README、prepare.py（只读）、train.py（可改）
4. 验证数据是否存在
5. 初始化结果表：results.tsv（只写表头）
6. 确认设置完毕
```

**设计思想**：每次实验都是一个干净的新分支，互不干扰。类似 GitFlow 的工作流。

### 第 2 部分：Experimentation（实验边界）

| 能做 | 不能做 |
|------|--------|
| 修改 train.py（模型、优化器、超参数） | 修改 prepare.py（数据、评估函数） |
| 尝试任何架构改进 | 安装新依赖 |
| 调整 batch size、模型大小 | 修改评估指标 |

**关键设计**：
- 目标只有一个：**最低 val_bpb**（越低越好）
- 时间预算固定：**5 分钟**（无论怎么改，都跑 5 分钟）
- 简洁性原则：小幅提升不值得加 20 行复杂代码；删除代码还能保持效果？保留

### 第 3 部分：Output format（输出格式）

明确告诉 Agent 从哪里读取结果：

```bash
grep "^val_bpb:" run.log     # 提取核心指标
grep "^peak_vram_mb:" run.log  # 提取内存使用
```

**设计思想**：不要指望 Agent 能理解完整的日志输出，给它一个精确的提取命令。

### 第 4 部分：Logging results（日志记录）

```
commit    val_bpb    memory_gb    status    description
a1b2c3d   0.997900   44.0         keep      baseline
b2c3d4e   0.993200   44.2         keep      increase LR to 0.04
c3d4e5f   1.005000   44.0         discard   switch to GeLU activation
d4e5f6g   0.000000   0.0          crash     double model width (OOM)
```

**三态管理**：
- **keep**：有改进，保留
- **discard**：没改进，回退
- **crash**：崩溃，记录后继续

**设计思想**：不用数据库、不用复杂系统，一个 TSV 文件搞定。简单到不可能出错。

### 第 5 部分：Experiment loop（永不停止的循环）

```
LOOP FOREVER:
1. 看当前 git 状态
2. 修改 train.py（新实验想法）
3. git commit
4. 运行实验: uv run train.py > run.log 2>&1
5. 读取结果: grep val_bpb run.log
6. 如果崩溃: 读错误日志，尝试修复，修不好就放弃
7. 记录到 results.tsv
8. 如果改进: 保留当前 commit（advance）
9. 如果没改进: git reset 回退
10. 回到步骤 1
```

**最关键的指令**：

> **NEVER STOP**: 一旦循环开始，不要停下来问人类要不要继续。人类可能在睡觉。你是自主的。如果没想法了，再想想——读代码里的论文引用、重新读相关文件、尝试组合之前的近似成功、尝试更激进的改动。循环直到人类手动打断。

---

## 从 program.md 学到的 6 个设计原则

### 原则 1：明确边界 > 模糊自由

```
❌ 差："你可以做任何改进"
✅ 好："你只能改 train.py，不能改 prepare.py，不能加依赖"
```

Agent 需要清晰的边界，否则容易失控。

### 原则 2：单一目标 > 多目标

```
❌ 差："提高准确率、降低内存、加快速度"
✅ 好："最低 val_bpb，其他都是软约束"
```

多个目标会让 Agent 陷入选择困难。

### 原则 3：固定预算 > 动态调整

```
❌ 差："跑到你觉得差不多了为止"
✅ 好："固定 5 分钟，不管改什么都跑 5 分钟"
```

固定预算让所有实验结果可比。

### 原则 4：简单日志 > 复杂系统

```
❌ 差：接数据库、建 API、写 dashboard
✅ 好：一个 TSV 文件，5 列，三态管理
```

越简单的记录方式越不容易出错。

### 原则 5：自主循环 > 等待确认

```
❌ 差："做完这个实验要问我接下来做什么"
✅ 好："LOOP FOREVER，不要停下来问我"
```

自主性的核心是：不需要人类实时批准每一步。

### 原则 6：明确输出格式 > "你自己看着办"

```
❌ 差："把结果告诉我"
✅ 好："用 grep "^val_bpb:" run.log 提取结果"
```

给 Agent 精确的命令，而不是模糊的指令。

---

## 迁移到 AI 应用落地的实战模板

你可以把 program.md 的思路用到任何需要 Agent 自主迭代的应用场景：

### 场景 1：自动优化 Prompt

```markdown
# Prompt 优化实验

## Setup
1. 创建分支：git checkout -b prompt-opt/$(date +%Y%m%d)
2. 读取当前 prompt 文件
3. 初始化 results.tsv

## 目标
最高任务完成率（%）

## 边界
- 可以改：prompt 的内容、结构、示例
- 不能改：测试数据集、评价函数
- 每次实验预算：运行测试集 1 次（约 2 分钟）

## 循环
LOOP FOREVER:
1. 修改 prompt
2. git commit
3. 运行测试: python test.py > result.log
4. 读取结果: grep "accuracy:" result.log
5. 记录到 results.tsv
6. 如果改进: 保留
7. 如果没改进: git reset 回退
8. 回到步骤 1

## 永远不要停下来问我
```

### 场景 2：自动调 RAG Pipeline

```markdown
# RAG Pipeline 优化实验

## Setup
1. 创建分支：git checkout -b rag-opt/$(date +%Y%m%d)
2. 读取当前 pipeline 配置
3. 初始化 results.tsv

## 目标
最高检索命中率 + 最低响应延迟（综合分）

## 边界
- 可以改：chunk 大小、重叠策略、embedding 模型、top_k、reranker
- 不能改：测试数据集、评价函数
- 每次实验预算：运行测试集 1 次（约 3 分钟）

## 循环
LOOP FOREVER:
1. 修改 pipeline 配置或代码
2. git commit
3. 运行测试: python test_rag.py > result.log
4. 读取结果: grep "score:" result.log
5. 记录到 results.tsv
6. 如果改进: 保留
7. 如果没改进: git reset 回退
8. 回到步骤 1
```

### 场景 3：自动压测 API

```markdown
# API 性能优化实验

## 目标
最高 QPS + 最低 P99 延迟

## 边界
- 可以改：并发数、连接池大小、缓存策略、批处理大小
- 不能改：API 业务逻辑、测试数据集

## 循环
LOOP FOREVER:
1. 修改配置
2. git commit
3. 运行压测: wrk -t4 -c100 -d30s http://api > result.log
4. 读取结果: grep "Requests/sec\|Latency" result.log
5. 记录到 results.tsv
6. 如果改进: 保留
7. 如果没改进: git reset 回退
```

---

## 总结

| 设计要素 | program.md 的做法 | 你可以怎么用 |
|----------|------------------|-------------|
| 边界控制 | 只改 train.py，不动 prepare.py | 只改 X 文件，不动 Y 文件 |
| 目标 | 最低 val_bpb | 你的核心指标（准确率、QPS、延迟...） |
| 预算 | 固定 5 分钟 | 你的实验运行时长 |
| 日志 | results.tsv，三态管理 | 同样的 TSV，同样的三态 |
| 循环 | LOOP FOREVER，不要停 | 同样的自主循环 |
| 回退 | git reset 到改进前的 commit | 同样的 git 版本控制 |

> **program.md 的本质**：它不是代码，它是"元代码"——指挥 Agent 怎么写代码、怎么跑实验、怎么记录结果的指令文件。这个思路可以迁移到任何需要 AI Agent 自主迭代的应用场景。

---

_📁 原始 program.md 存档：references/program.md_
_📅 学习文档创建日期：2026-04-28_
