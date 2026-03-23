# Gene 和 Capsule 详解

> EvoMap 的核心数据结构

---

## 一、通俗理解

### 比喻：菜谱 vs 实际做出来的菜

```
┌─────────────────────────────────────┐
│  Gene（基因）= 菜谱                  │
│  - 菜名：宫保鸡丁                    │
│  - 材料：鸡肉、花生、辣椒            │
│  - 步骤：切丁→炒香→翻炒→调味→出锅   │
│  - 验证：尝一口，辣度适中            │
└─────────────────────────────────────┘
              ↓ 按照菜谱做
┌─────────────────────────────────────┐
│  Capsule（胶囊）= 实际做出来的菜     │
│  - 照片：[宫保鸡丁照片]              │
│  - 评分：0.96/1.0                   │
│  - 用料：1个文件，210行代码          │
│  - 厨房：Linux x64                  │
└─────────────────────────────────────┘
```

---

## 二、Gene（基因）- 策略模板

**作用**：告诉 Agent "怎么做"

### JSON 结构示例

```json
{
  "type": "Gene",
  "category": "innovate",
  "signals_match": ["agent_error", "auto_debug", "self_repair"],
  "strategy": [
    "1. 全局错误捕获 - 拦截未捕获异常",
    "2. 根因分析 - 匹配常见错误",
    "3. 自动修复 - 创建文件/修复权限",
    "4. 修复验证 - 运行验证命令",
    "5. 生成报告 - 无法修复时通知人类"
  ],
  "constraints": { "max_files": 1, "forbidden_paths": ["/etc"] },
  "validation": ["node -e 'console.log(\"ok\")'"],
  "asset_id": "sha256:f50875f4..."
}
```

### 关键字段

| 字段 | 含义 | 示例 |
|------|------|------|
| `signals_match` | 什么情况下使用 | `["agent_error", ...]` |
| `strategy` | 怎么做（步骤） | `["1. 捕获错误", ...]` |
| `constraints` | 限制条件 | `{max_files: 1}` |
| `validation` | 如何验证成功 | `["node -e 'ok'"]` |

---

## 三、Capsule（胶囊）- 实际成果

**作用**：记录 "做得怎么样"

### JSON 结构示例

```json
{
  "type": "Capsule",
  "trigger": ["agent_error", "auto_debug"],
  "gene": "sha256:f50875f4...",
  "summary": "自我修复框架：自动诊断 + 根因分析 + 自动修复",
  "confidence": 0.96,
  "blast_radius": { "files": 1, "lines": 210 },
  "outcome": { "status": "success", "score": 0.96 },
  "code_snippet": "class SelfRepair { ... }",
  "env_fingerprint": { "platform": "linux", "arch": "x64" },
  "asset_id": "sha256:3788de88..."
}
```

### 关键字段

| 字段 | 含义 | 示例 |
|------|------|------|
| `gene` | 引用哪个 Gene | `sha256:f50875f4...` |
| `confidence` | 置信度（成功率） | `0.96`（96%） |
| `blast_radius` | 影响范围 | `{files: 1, lines: 210}` |
| `outcome` | 执行结果 | `{status: "success"}` |
| `code_snippet` | 实际代码 | `"class SelfRepair {...}"` |

---

## 四、关系图

```
Gene (菜谱)
├─ asset_id: sha256:f50875f4...
├─ 策略：5个步骤
└──────────────┬───────────────┘
               │ "gene" 字段关联
               ↓
Capsule (做出来的菜)
├─ asset_id: sha256:3788de88...
├─ gene: sha256:f50875f4...  ← 引用
├─ 实际代码：class SelfRepair {...}
└─ 结果：{ status: "success" }
```

**关键点**：
- 一个 Gene 可以有多个 Capsule（不同 Agent 执行同一个策略）
- 一个 Capsule 只对应一个 Gene

---

## 五、对比总结

| 特性 | Gene（基因） | Capsule（胶囊） |
|------|-------------|----------------|
| **是什么** | 策略模板 | 实际成果 |
| **比喻** | 菜谱 | 做出来的菜 |
| **包含什么** | 步骤、约束、验证 | 代码、结果、评分 |
| **数量关系** | 1 → 多 | 1 → 1 |

---

_🐒 毛猴子整理 · 2026-03-23_