# Karpathy autoresearch 项目研究报告

> 报告日期：2026-04-28
> 项目地址：https://github.com/karpathy/autoresearch
> 作者：Andrej Karpathy（@karpathy）
> Stars：77,264+ | Forks：11,267+
> 许可证：MIT

---

## 一、项目概述

**autoresearch** 是 Andrej Karpathy 于 2026 年 3 月 6 日发布的一个开创性项目，核心理念极其简单但深刻：

> **给 AI Agent 一个真实的 LLM 训练环境，让它自主做研究。**

传统科研流程是：人类研究者读论文 -> 产生想法 -> 修改代码 -> 跑实验 -> 分析结果 -> 迭代。Karpathy 把这个流程完全交给了 AI Agent —— 你只需要睡觉前启动它，第二天早上就能收获一整夜自动完成的实验记录和（通常）一个更好的模型。

项目创建后不到一个月获得 77,000+ 颗 Star，成为 GitHub 上增长最快的 AI 项目之一，社区涌现了 macOS、Windows、AMD ROCm 等多个平台适配 fork。

---

## 二、解决的核心问题

### 2.1 传统 LLM 研究的瓶颈

| 痛点 | 传统方式 | autoresearch 的方式 |
|------|----------|---------------------|
| 实验迭代速度 | 人类每天能做 3-5 个实验 | 每小时约 12 个实验，一夜约 100 个 |
| 时间窗口 | 仅限于人类工作时段 | 24/7 不间断，包括睡眠时间 |
| 想法 -> 验证延迟 | 几小时到几天 | 5 分钟一个实验周期 |
| 平台差异 | 需要复杂的跨平台配置管理 | 固定 5 分钟预算，自动适配当前硬件 |
| 知识复用 | 依赖研究者个人经验和记忆 | `program.md` 持续积累和迭代 |

### 2.2 核心创新点

1. **固定时间预算设计**：所有训练严格限制 5 分钟（wall clock，不含启动/编译）。这使得不同架构、不同超参数的实验结果可以公平比较，不管 Agent 改了什么（模型大小、batch size、优化器等）。

2. **"研究组织编程"范式**：人类不直接写训练代码，而是编写 `program.md` —— 一份给 AI Agent 的"研究指令文档"。这本质上是在编写"研究组织的代码"，类似于编程一个虚拟研究团队的行为逻辑。

3. **单文件修改边界**：Agent 只能修改 `train.py`，`prepare.py` 是只读的评价/数据基础设施。这保证了实验范围可控、diff 可审查。

4. **自主试错循环**：Agent 修改代码 -> 提交 -> 训练 -> 读取结果 -> 如果改进则保留，否则回退。这个 loop 永不停止，直到人类手动干预。

---

## 三、技术架构详解

### 3.1 三个核心文件

```
prepare.py      — 固定常量、数据准备、tokenizer、评估函数（只读，Agent 不修改）
train.py        — 模型架构、优化器、训练循环（Agent 修改的唯一文件）
program.md      — Agent 的指令文件（人类修改，引导研究方向）
```

### 3.2 模型基线

项目基于 Karpathy 的 [nanochat](https://github.com/karpathy/nanochat) 简化而来，初始模型配置：

- **模型架构**：GPT Decoder-only Transformer
- **深度**：8 层
- **注意力**：Flash Attention 3，SSSL 窗口模式（Sliding-Sliding-Sliding-Local）
- **Value Embedding（ResFormer）**：交替层使用 value residual
- **残差连接**：可学习的 resid_lambdas + x0_lambdas
- **激活函数**：ReLU 平方（GELU 的近似）
- **归一化**：RMSNorm
- **优化器**：Muon（主） + AdamW
- **Tokenizer**：BPE，8192 vocab size
- **数据**：ClimbMix-400B 数据集（HuggingFace）
- **序列长度**：2048
- **评价度量**：val_bpb（validation bits per byte，越低越好）

### 3.3 实验循环流程

```
1. 读取当前 git 状态和 results.tsv 历史记录
2. 产生实验想法（基于已有结果、论文、直觉）
3. 直接修改 train.py 的代码
4. git commit 保存改动
5. 运行训练: uv run train.py > run.log 2>&1（~5 分钟）
6. 读取结果: grep val_bpb run.log
7. 记录到 results.tsv（commit / val_bpb / 内存 / 状态 / 描述）
8. 如果 val_bpb 降低（改进）→ 保留当前 commit
9. 如果 val_bpb 没变或变差 → git reset 回退到改进前的 commit
10. 回到步骤 1，永不停止
```

### 3.4 `program.md` 的设计

`program.md` 是项目的灵魂，它本质上是一个轻量级的"skill"文件，定义了：

- 实验设置流程（创建分支、验证数据、初始化结果表）
- Agent 可以做什么（修改 train.py）和不能做什么（不修改 prepare.py、不添加依赖）
- 优化目标（最低 val_bpb）
- 输出格式规范（TSV 日志）
- 实验循环的完整逻辑
- 崩溃处理策略
- **明确指令：永远不要停下来问人类**

---

## 四、关键技术选择分析

### 4.1 为什么用 val_bpb 而不是 perplexity？

val_bpb（bits per byte）是词汇表大小无关的度量。当 Agent 尝试改变 vocab_size 时，perplexity 无法公平比较，但 bpb 可以。这是一个非常实用的设计选择。

### 4.2 为什么固定 5 分钟时间预算？

- **可比性**：所有实验在相同时间内比较，无论模型大小、batch size 如何变化
- **可预期性**：约 12 个实验/小时，一夜约 100 个实验
- **硬件自适应**：自动找到当前硬件在 5 分钟内最优的模型配置
- **缺点**：结果无法跨硬件平台直接比较

### 4.3 为什么只允许修改 train.py？

- 保持 Agent 的修改范围可控
- diff 易于审查和理解
- 避免了 Agent 可能造成的混乱（改数据管道、改评估逻辑等）
- 类似一个研究者在一个代码文件上持续工作的场景

### 4.4 优化器选择：Muon

Muon 是一种相对较新的优化器，适合 Transformer 训练。结合 AdamW 使用，可以在某些场景下获得比纯 AdamW 更好的收敛效果。Agent 可以自由更换优化器。

---

## 五、项目意义与影响

### 5.1 范式转变

autoresearch 展示了一个新的研究范式：

```
传统范式：人类研究者 -> 写代码 -> 跑实验 -> 分析
新范式：   人类编写 program.md -> AI Agent 自主循环 -> 人类分析结果
```

人类的角色从"执行者"变成了"元编程者"——你不再直接做实验，而是编程一个会自己做实验的 Agent。

### 5.2 开源社区影响

- 77,000+ Stars 说明社区对 AI 自主研究的强烈兴趣
- 多个平台 fork（macOS、Windows、AMD）显示了可扩展性
- 降低了 LLM 预训练研究的门槛——只需要一张 NVIDIA GPU

### 5.3 对 AI Agent 领域的启示

1. **Agent 需要真实环境**：不是 mock，不是 toy problem，而是真正的 GPU 训练环境
2. **指令即代码**：`program.md` 本质上是一种"研究组织编程语言"
3. **自主性需要边界**：明确的 can/cannot do 清单是关键
4. **快速迭代优于深思熟虑**：5 分钟一个实验，一夜 100 次迭代

---

## 六、局限性与改进空间

### 6.1 当前限制

| 限制 | 说明 |
|------|------|
| 硬件要求 | 仅支持单 NVIDIA GPU（已有社区 fork 扩展到其他平台） |
| 单模型 | 不支持分布式训练、多 GPU |
| 固定时间 | 5 分钟预算可能不足以观察某些架构的长期训练效果 |
| 单 Agent | 只有一个 Agent，没有多 Agent 协作或对抗机制 |
| 无外部知识 | Agent 默认没有论文检索能力，只能基于已有知识和直觉 |
| 缺乏多样性 | 循环是顺序的，没有并行探索不同方向 |

### 6.2 潜在改进方向

1. **多 Agent 并行**：同时运行多个 Agent，各自探索不同方向，定期交流发现
2. **论文检索集成**：让 Agent 能搜索 arXiv，阅读相关论文，将新想法带回实验
3. **元学习 program.md**：用实验结果自动优化 `program.md` 本身
4. **多时间预算**：支持短期快速实验和长期验证实验的组合
5. **跨平台标准化**：建立跨硬件可比的评价协议
6. **Agent 记忆**：让 Agent 能跨会话记住成功的策略和失败教训

---

## 七、与本项目（ai-agent-research）的关联

本项目 `ai-agent-research` 是一个 AI Agent 研究工作空间，包含多个 Agent 相关的项目、学习记录和研究报告。Karpathy 的 autoresearch 为我们提供了以下借鉴：

1. **Agent 自主研究的最佳实践**：program.md 的设计理念可以借鉴到我们的 Agent 工作流中
2. **实验管理方法**：results.tsv 的日志格式和 keep/discard/crash 三态管理
3. **边界控制**：明确 Agent 可以做什么和不能做什么的设计思路
4. **持续迭代哲学**：永不停止的自动循环，直到人类干预

---

## 八、总结

Karpathy 的 autoresearch 是一个看似简单但极具深远意义的项目。它用一个 README、三个代码文件和一个 Markdown 指令文件，就搭建了一个完整的 AI 自主研究框架。

**它解决的本质问题是**：如何让 AI Agent 在真实的研究环境中自主迭代，而非仅作为代码生成工具。这代表了一种从 "AI 辅助研究" 到 "AI 自主研究" 的范式跃迁。

项目的精妙之处在于其极简设计——没有复杂的配置系统、没有分布式框架、没有外部依赖。只有一个清晰的边界（只能改 train.py）、一个明确的指标（最低 val_bpb）、一个永不停止的循环。这种极简主义恰恰使得它成为了一个强大的研究原语（primitive），任何人都可以在此基础上构建更复杂的研究系统。

---

## 参考资料

- 项目仓库：https://github.com/karpathy/autoresearch
- nanochat 项目：https://github.com/karpathy/nanochat
- ClimbMix 数据集：https://huggingface.co/datasets/karpathy/climbmix-400b-shuffle
- Karpathy 推文 1：https://x.com/karpathy/status/2029701092347630069
- Karpathy 推文 2：https://x.com/karpathy/status/2031135152349524125
- Dummy's Guide 入门指南：https://x.com/hooeem/status/2030720614752039185
- 社区 fork：
  - macOS: https://github.com/miolini/autoresearch-macos
  - macOS MLX: https://github.com/trevin-creator/autoresearch-mlx
  - Windows RTX: https://github.com/jsegov/autoresearch-win-rtx
  - AMD ROCm: https://github.com/andyluo7/autoresearch
