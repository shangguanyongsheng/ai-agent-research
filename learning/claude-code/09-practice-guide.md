# 落地实践指南：从 Claude Code 学写 OpenClaw Skills

> ⏱️ 30 分钟 | 📍 第九章
> 
> 将 Claude Code 源码智慧转化为 OpenClaw Skills

[← 返回导航](08-architecture-nav.md)

---

## 目标

学完本章，你将能够：

1. 理解 Skill 的核心设计原则
2. 编写符合最佳实践的 SKILL.md
3. 设计有效的工具化脚本
4. 组织 Skill 的资源目录结构

---

## Part 1：设计原则（从 Claude Code 学到的）

### 原则 1：Everything is a Tool

Claude Code 的核心设计：**每个能力都是独立、可组合的工具**。

```
Claude Code 工具设计：

├── 统一接口
│   ├── name         工具名称
│   ├── description  工具描述（触发关键词）
│   ├── inputSchema  输入参数（Zod Schema）
│   ├── outputSchema 输出结果
│   └── execute()    执行方法
│
├── 权限控制
│   ├── allow    自动允许
│   ├── deny     拒绝执行
│   └── ask      询问用户
│
└── 隔离性
    ├── 一个工具出错不影响其他
    ├── 独立测试
    └── 独立更新
```

**应用到 OpenClaw Skills**：

```yaml
# SKILL.md frontmatter
---
name: my-skill
description: |
  技能描述。
  包含触发关键词："关键词1", "关键词2", "场景描述"。
  Use when: 用户需要做 XXX 任务。
---
```

### 原则 2：渐进式披露

Claude Code 的上下文管理：**按需加载，避免 Token 浪费**。

```
三级加载：

Level 1: Metadata (name + description)
         → 常驻上下文 (~100 tokens)
         → 决定是否触发

Level 2: SKILL.md body
         → 触发后加载 (<5k tokens)
         → 核心流程

Level 3: Bundled resources
         → 按需加载 (scripts/references/assets)
         → 详细信息
```

**应用到 OpenClaw Skills**：

```
skill-name/
├── SKILL.md          (核心流程，<500 行)
├── references/
│   ├── detailed.md   (详细文档)
│   └── examples.md   (示例)
└── scripts/
    └── helper.py     (执行脚本)
```

### 原则 3：触发机制清晰

Claude Code 工具的 description 是触发核心：**明确写清何时使用**。

```
好的 description：

"搜索代码库中的文件和内容。
支持正则表达式、文件过滤。
Use when: 
(1) 需要搜索代码
(2) 需要查找文件
(3) 需要定位函数定义
触发关键词：'搜索', '查找', 'find', 'search'"

坏的 description：

"这是一个搜索工具"  ← 太模糊，不知道何时触发
```

**应用到 OpenClaw Skills**：

```yaml
description: |
  处理 PDF 文档的提取、旋转、合并。
  Use when:
  (1) 用户提到 PDF 文件
  (2) 需要提取 PDF 内容
  (3) 需要旋转/合并 PDF
  触发关键词："pdf", "PDF", "提取PDF", "旋转PDF"
```

---

## Part 2：Skill 结构详解

### 目录结构

```
skill-name/
├── SKILL.md          (必需) 技能入口
├── references/       (可选) 参考文档
│   ├── api.md        API 文档
│   ├── examples.md   使用示例
│   └── schemas.md    数据结构
├── scripts/          (可选) 执行脚本
│   ├── main.py       主要脚本
│   └── utils.py      辅助脚本
└── assets/           (可选) 输出资源
    ├── template.md   输出模板
    └── logo.png      图片资源
```

### SKILL.md 结构

```markdown
---
name: skill-name
description: |
  技能描述（触发核心）。
  包含：功能 + 使用场景 + 触发关键词。
---

# Skill Title

简短介绍（1-2 行）。

## Quick Start

最常用的用法（代码示例）。

## Workflow

工作流程（步骤清晰）。

## Advanced

高级用法（链接到 references）。

## Troubleshooting

常见问题。
```

---

## Part 3：编写实战示例

### 示例 1：简单 Skill（无脚本）

```markdown
---
name: weather
description: |
  获取天气信息和预报。
  Use when:
  (1) 用户问天气、温度
  (2) 用户问某个城市天气
  (3) 用户问未来几天的天气
  触发关键词："天气", "温度", "weather", "forecast"
---

# Weather Skill

获取当前天气和预报。

## Quick Start

```bash
# 当前天气
curl -s "wttr.in/Shanghai?format=3"

# 详细预报
curl -s "wttr.in/Shanghai"
```

## Workflow

1. 解析城市名（用户说"上海" → "Shanghai"）
2. 调用 wttr.in API
3. 格式化输出（中文）

## Multiple Cities

```bash
curl -s "wttr.in/Shanghai,Beijing,Guangzhou?format=3"
```
```

### 示例 2：中等 Skill（带脚本）

```markdown
---
name: video-frames
description: |
  从视频中提取帧或短片。
  Use when:
  (1) 用户想从视频提取图片
  (2) 用户想截取视频片段
  (3) 用户说"提取帧"、"截取视频"
  触发关键词："视频", "帧", "frame", "clip", "ffmpeg"
---

# Video Frames

使用 ffmpeg 从视频提取帧或短片。

## Quick Start

提取每秒 1 帧：

```bash
ffmpeg -i input.mp4 -vf fps=1 frames/%04d.png
```

提取特定时间段的帧：

```bash
ffmpeg -i input.mp4 -ss 00:01:30 -t 5 -vf fps=1 frames/%04d.png
```

## Scripts

详细脚本见 `scripts/extract_frames.py`。

## Advanced

多视频处理、批量提取 → 见 `references/batch.md`。
```

### 示例 3：复杂 Skill（完整结构）

```
pdf-processor/
├── SKILL.md
├── references/
│   ├── pdftk-guide.md    # pdftk 详细文档
│   ├── pdfplumber.md     # pdfplumber API
│   └── ocrmypdf.md       # OCR 文档
├── scripts/
│   ├── rotate.py         # 旋转 PDF
│   ├── merge.py          # 合合 PDF
│   └── extract_text.py   # 提取文本
└── assets/
    └── template.md       # 输出模板
```

**SKILL.md 内容**：

```markdown
---
name: pdf-processor
description: |
  处理 PDF 文档：旋转、合并、拆分、提取文本、OCR。
  Use when:
  (1) 用户提到 PDF 文件
  (2) 需要旋转/合并/拆分 PDF
  (3) 需要提取 PDF 内容
  (4) 需要对 PDF 进行 OCR
  触发关键词："pdf", "PDF", "旋转PDF", "合并PDF", "提取PDF"
---

# PDF Processor

处理 PDF 文档的完整工具集。

## Quick Start

```bash
# 旋转 PDF
python3 scripts/rotate.py input.pdf 90 output.pdf

# 合合 PDF
python3 scripts/merge.py file1.pdf file2.pdf output.pdf

# 提取文本
python3 scripts/extract_text.py input.pdf
```

## Capabilities

| 功能 | 脚本 | 说明 |
|------|------|------|
| 旋转 | `rotate.py` | 90/180/270 度 |
| 合合 | `merge.py` | 多个 PDF 合成一个 |
| 拆分 | `split.py` | 按页码拆分 |
| 提取文本 | `extract_text.py` | 使用 pdfplumber |
| OCR | `ocr.py` | 使用 ocrmypdf |

## Workflow

1. 确认用户需求（旋转/合并/提取？）
2. 选择对应的脚本
3. 执行脚本
4. 验证结果

## References

- PDFtk 详细用法 → `references/pdftk-guide.md`
- pdfplumber API → `references/pdfplumber.md`
- OCRmyPDF 配置 → `references/ocrmypdf.md`

## Troubleshooting

- **缺少依赖？** 运行 `pip install pdfplumber pypdf ocrmypdf`
- **OCR 失败？** 检查 tesseract 是否安装
```

---

## Part 4：从 Claude Code 源码提炼的 Skill 设计模式

### 模式 1：工具封装模式

Claude Code 的每个工具都是独立封装。应用到 Skill：

```
设计思路：
1. 识别重复性任务
2. 封装为脚本
3. Skill 中引用脚本

好处：
├── Token 效率高（脚本不加载到上下文）
├── 确定性执行（脚本逻辑固定）
├── 可复用（多次调用不重写代码）
└── 可维护（脚本独立更新）
```

**示例**：

```python
# scripts/rotate.py
import sys
from pypdf import PdfReader, PdfWriter

def rotate_pdf(input_path, degrees, output_path):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        page.rotate(degrees)
        writer.add_page(page)
    
    writer.write(output_path)

if __name__ == "__main__":
    rotate_pdf(sys.argv[1], int(sys.argv[2]), sys.argv[3])
```

```markdown
# SKILL.md
## Quick Start
```bash
python3 scripts/rotate.py input.pdf 90 output.pdf
```
```

### 模式 2：工作流编排模式

Claude Code 的 Agentic Loop 是工作流编排。应用到 Skill：

```
设计思路：
1. 定义工作流步骤
2. 每步有清晰的输入/输出
3. 步骤之间有明确的衔接

好处：
├── 可追踪（知道当前在哪一步）
├── 可中断（可以在任意步骤停止）
├── 可恢复（从失败步骤重新开始）
└── 可调试（定位问题在哪个步骤）
```

**示例**：

```markdown
# SKILL.md

## Workflow

### 步骤 1：收集信息
```bash
# 读取相关文件
```

### 步骤 2：分析处理
```bash
# 执行分析
```

### 步骤 3：生成输出
```bash
# 写入结果文件
```

### 步骤 4：验证
```bash
# 检查结果
```
```

### 模式 3：权限控制模式

Claude Code 的三级权限（allow/deny/ask）。应用到 Skill：

```
设计思路：
1. 标识危险操作
2. 在 Skill 中明确提示
3. 建议用户确认

危险操作：
├── 删除文件
├── 网络请求（发送数据）
├── 执行不可逆命令
└── 修改系统配置

安全操作：
├── 读取文件
├── 网络请求（只获取）
├── 临时文件操作
└── 查询命令
```

**示例**：

```markdown
# SKILL.md

## ⚠️ Safety

**危险操作（需要用户确认）**：
- 删除文件：`rm -rf`
- 发送邮件：需要确认收件人
- 提交代码：需要确认内容

**安全操作（自动执行）**：
- 读取文件
- 搜索代码
- 运行测试
```

### 模式 4：渐进式复杂度模式

Claude Code 的功能分层。应用到 Skill：

```
设计思路：
1. Level 1：最简单用法（一行命令）
2. Level 2：常用用法（多行示例）
3. Level 3：高级用法（链接到 references）
4. Level 4：完整文档（外部链接）

好处：
├── 新手快速上手
├── 进阶逐步学习
├── 专家查阅细节
└── Token 高效利用
```

**示例**：

```markdown
# SKILL.md

## Quick Start (Level 1)

```bash
python3 scripts/main.py input output
```

## Common Usage (Level 2)

```bash
# 带参数
python3 scripts/main.py input output --option value
```

## Advanced (Level 3)

详细配置见 `references/advanced.md`。

## Full Docs (Level 4)

官方文档：https://example.com/docs
```

---

## Part 5：Skill 编写流程

### 步骤 1：明确需求

```
问自己三个问题：

1. 这个 Skill 解决什么问题？
   → 重复性任务？复杂流程？专业知识？

2. 用户如何触发这个 Skill？
   → 关键词是什么？场景是什么？

3. Skill 需要什么资源？
   → scripts？references？assets？
```

### 步骤 2：设计结构

```
根据复杂度选择结构：

简单 Skill（<100 行）：
└── SKILL.md

中等 Skill（带脚本）：
├── SKILL.md
└── scripts/
    └── main.py

复杂 Skill（完整结构）：
├── SKILL.md
├── references/
│   ├── api.md
│   └── examples.md
├── scripts/
│   ├── main.py
│   └── utils.py
└── assets/
    └── template.md
```

### 步骤 3：编写 SKILL.md

```
必须部分：

1. Frontmatter (name + description)
   → 触发核心

2. Quick Start
   → 最简单用法

3. Workflow
   → 工作流程

可选部分：

4. References
   → 链接到详细文档

5. Troubleshooting
   → 常见问题
```

### 步骤 4：编写脚本

```
脚本要点：

1. 参数清晰
   ├── 使用 sys.argv 或 argparse
   └── 提供帮助信息

2. 错误处理
   ├── 捕获异常
   ├── 提供友好错误消息
   └── 建议解决方案

3. 输出标准
   ├── 使用 JSON 或结构化文本
   └── 方便 AI 解析
```

### 步骤 5：测试验证

```
测试清单：

1. 触发测试
   → 用户说关键词能否触发？

2. 功能测试
   → 脚本能否正常执行？

3. 错误测试
   → 错误输入能否正确处理？

4. Token 测试
   → SKILL.md 是否 <500 行？
```

---

## Part 6：实际案例 - 编写一个 Skill

### 案例：编写 "代码搜索" Skill

**需求**：用户经常需要搜索代码库，我们封装一个 Skill。

**步骤 1：明确需求**

```
问题：重复写 grep/find 命令
触发："搜索代码", "查找文件", "定位函数"
资源：脚本 + 参考
```

**步骤 2：设计结构**

```
code-search/
├── SKILL.md
├── references/
│   ├── grep-cheatsheet.md
│   └── find-cheatsheet.md
└── scripts/
    └── smart_search.py
```

**步骤 3：编写 SKILL.md**

```markdown
---
name: code-search
description: |
  搜索代码库中的文件和内容。
  支持正则表达式、文件类型过滤、项目搜索。
  Use when:
  (1) 用户需要搜索代码
  (2) 用户需要查找文件
  (3) 用户需要定位函数/类定义
  触发关键词："搜索", "查找", "find", "search", "grep", "定位"
---

# Code Search

搜索代码库的智能工具。

## Quick Start

```bash
# 搜索文件名
find . -name "*.py" -type f

# 搜索内容
grep -r "function_name" --include="*.py"

# 使用脚本（智能搜索）
python3 scripts/smart_search.py "query" --type py
```

## Workflow

1. 解析用户需求（文件名？内容？）
2. 选择搜索方式（find/grep/脚本）
3. 执行搜索
4. 格式化结果

## References

- grep 完整用法 → `references/grep-cheatsheet.md`
- find 完整用法 → `references/find-cheatsheet.md`

## Troubleshooting

- **搜索太慢？** 使用 `--maxdepth` 限制深度
- **结果太多？** 使用 `--include` 过滤文件类型
```

**步骤 4：编写脚本**

```python
# scripts/smart_search.py
import subprocess
import sys
import json

def smart_search(query, file_type=None, max_depth=None):
    """智能搜索代码库"""
    
    # 构建命令
    cmd = ["grep", "-r", "-n", query]
    
    if file_type:
        cmd.extend(["--include", f"*.{file_type}"])
    
    if max_depth:
        cmd.extend(["--maxdepth", str(max_depth)])
    
    # 执行搜索
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # 解析结果
    matches = []
    for line in result.stdout.split("\n"):
        if line:
            parts = line.split(":", 2)
            if len(parts) >= 3:
                matches.append({
                    "file": parts[0],
                    "line": int(parts[1]),
                    "content": parts[2]
                })
    
    return matches

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--type", default=None)
    parser.add_argument("--maxdepth", type=int, default=None)
    
    args = parser.parse_args()
    
    matches = smart_search(args.query, args.type, args.maxdepth)
    print(json.dumps(matches, indent=2))
```

**步骤 5：测试验证**

```bash
# 测试脚本
python3 scripts/smart_search.py "def main" --type py

# 测试触发
用户说："搜索代码中的 main 函数"
→ 应该触发这个 Skill
```

---

## Part 7：最佳实践清单

### ✅ SKILL.md 最佳实践

| 项目 | 要求 | 原因 |
|------|------|------|
| Frontmatter | name + description | 触发核心 |
| description | 包含触发关键词 | 让 AI 知道何时用 |
| description | 包含 Use when | 明确使用场景 |
| 主体内容 | <500 行 | Token 效率 |
| Quick Start | 一行命令 | 快速上手 |

### ✅ 脚本最佳实践

| 项目 | 要求 | 原因 |
|------|------|------|
| 参数 | argparse | 清晰易用 |
| 输出 | JSON 格式 | AI 易解析 |
| 错误 | 友好消息 | 方便调试 |
| 依赖 | 明确列出 | 安装指引 |

### ✅ References 最佳实践

| 项目 | 要求 | 原因 |
|------|------|------|
| 组织 | 按主题分文件 | 按需加载 |
| 内容 | 详细但不重复 | 避免冗余 |
| 链接 | SKILL.md 中引用 | 可发现性 |

---

## Part 8：Claude Code → OpenClaw 对照表

| Claude Code 概念 | OpenClaw 实现 | 应用建议 |
|------------------|---------------|----------|
| Tool Interface | 内置工具 + MCP | 工具化设计 |
| Permission Model | exec 安全模式 | 权限控制 |
| Query Engine | agent loop | 工作流编排 |
| Context Window | Token 限制 | 渐进式披露 |
| Subagent | sessions_spawn | 复杂任务 |
| Skills | Skills | 自定义工作流 |
| CLAUDE.md | AGENTS.md | 项目规则 |
| Auto Memory | MEMORY.md | 长期记忆 |

---

## 检查清单

完成本章后，你应该能够：

- [ ] 理解 Skill 设计原则
- [ ] 知道 SKILL.md 结构
- [ ] 能够编写简单 Skill
- [ ] 能够编写带脚本的 Skill
- [ ] 理解渐进式披露
- [ ] 知道如何组织资源目录
- [ ] 能够测试和验证 Skill

---

## 下一步

- [返回导航](08-architecture-nav.md)
- [开始编写你的第一个 Skill](../../skills/)
- [查看 Skill Creator Skill](/opt/openclaw/skills/skill-creator/SKILL.md)

---

**本章用时**：约 30 分钟  
**上一章**：[架构导航](08-architecture-nav.md)