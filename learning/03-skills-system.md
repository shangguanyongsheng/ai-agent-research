# 03. Skills 工具系统

> 让 Agent 能够使用工具

---

## 🎯 学习目标

理解 Skills 的三个核心概念：
- **定义** - 如何定义一个 Skill
- **管理** - 如何加载和管理 Skills
- **执行** - 如何调用和执行 Skills

---

## 第一步：概念解释

### Skills 是什么？

**Skills = Agent 的工具箱**

想象一个厨师：
- 🔪 有刀（切菜工具）
- 🍳 有锅（烹饪工具）
- 📏 有尺（测量工具）

Agent 也一样，需要不同的工具来完成不同任务：
- 📊 分组聚合工具
- 🔍 数据筛选工具
- 📈 图表创建工具

### 为什么需要 Skills？

**没有 Skills：**
```
用户：按类型分组统计
Agent：生成 pandas 代码
        ↓
     每次都要生成
     容易出错
     不稳定
```

**有 Skills：**
```
用户：按类型分组统计
Agent：调用 group_aggregate Skill
        ↓
     复用已验证的代码
     稳定可靠
```

---

## 第二步：类比理解

### 类比 1：Java Spring Bean

| Agent Skills | Java Spring | 说明 |
|--------------|-------------|------|
| Skill 定义 | @Component | 定义一个组件 |
| Skill 注册 | ApplicationContext | 管理所有组件 |
| Skill 调用 | @Autowired | 注入并使用 |

### 类比 2：工具箱模式

```
Skills/                      ToolBox/
├── group_aggregate.md   ←→  刀（切片工具）
├── filter_data.md       ←→  过滤器（筛选工具）
└── create_chart.md      ←→  模具（成型工具）
```

---

## 第三步：代码实现

### Skill 定义示例

```markdown
# Skill: group_aggregate

## 描述
按指定列分组并对数值列进行聚合计算。

## 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| group_by | string | 是 | 分组列名 |
| agg_column | string | 是 | 聚合列名 |
| agg_func | string | 否 | 聚合函数，默认 sum |

## 使用示例

用户请求：按授信类型统计合同金额

Agent 调用：
{
  "tool": "group_aggregate",
  "parameters": {
    "group_by": "授信类型",
    "agg_column": "合同金额",
    "agg_func": "sum"
  }
}
```

### Skills 管理器核心代码

```python
# agent/skills.py

class SkillManager:
    """Skills 管理器 - 加载和执行 Skills"""
    
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.skills = {}
        self._load_skills()
    
    def _load_skills(self):
        """加载所有 Skills（类似 Spring 扫描 @Component）"""
        for skill_file in self.skills_dir.glob("*.md"):
            skill_name = skill_file.stem
            skill_content = skill_file.read_text(encoding="utf-8")
            
            # 解析 Skill 定义
            self.skills[skill_name] = {
                "name": skill_name,
                "description": self._extract_description(skill_content),
                "parameters": self._extract_parameters(skill_content)
            }
    
    def execute_skill(self, skill_name: str, parameters: Dict, df):
        """执行 Skill（类似调用 Bean 的方法）"""
        if skill_name == "group_aggregate":
            return self._execute_group_aggregate(parameters, df)
        elif skill_name == "filter_data":
            return self._execute_filter_data(parameters, df)
        # ...
```

### Java 程序员的理解

```java
// Java 伪代码类比

@Component
public class SkillManager {
    private Map<String, Skill> skills = new HashMap<>();
    
    /**
     * 初始化时加载所有 Skills
     * 类似 Spring 的 @PostConstruct
     */
    @PostConstruct
    public void loadSkills() {
        // 扫描 skills 目录
        Files.walk(skillDir)
            .filter(f -> f.endsWith(".md"))
            .forEach(f -> {
                Skill skill = parseSkill(f);
                skills.put(skill.getName(), skill);
            });
    }
    
    /**
     * 执行 Skill
     * 类似调用 Service 方法
     */
    public Result executeSkill(String skillName, Map<String, Object> params, DataFrame df) {
        Skill skill = skills.get(skillName);
        if (skill == null) {
            throw new SkillNotFoundException(skillName);
        }
        
        // 根据类型分发
        switch (skillName) {
            case "group_aggregate":
                return executeGroupAggregate(params, df);
            case "filter_data":
                return executeFilterData(params, df);
            default:
                throw new UnsupportedOperationException(skillName);
        }
    }
}
```

---

## 第四步：详细解析

### 1. Skill 定义结构

```
每个 Skill 包含四个部分：

┌─────────────────────────────────────────────────────────────────┐
│ # Skill: [名称]                                                  │
├─────────────────────────────────────────────────────────────────┤
│ ## 描述                                                          │
│ 这个 Skill 做什么                                                │
├─────────────────────────────────────────────────────────────────┤
│ ## 参数                                                          │
│ | 参数 | 类型 | 必填 | 说明 |                                     │
│ 调用这个 Skill 需要什么参数                                       │
├─────────────────────────────────────────────────────────────────┤
│ ## 使用示例                                                      │
│ 具体的调用例子                                                    │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Skill 调用流程

```
用户请求："按授信类型统计合同金额"
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│ ReAct Thought: 用户想分组统计，应该用 group_aggregate            │
└─────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│ ReAct Action: 调用 group_aggregate Skill                        │
│ {                                                               │
│   "tool": "group_aggregate",                                    │
│   "parameters": {                                               │
│     "group_by": "授信类型",                                      │
│     "agg_column": "合同金额",                                    │
│     "agg_func": "sum"                                           │
│   }                                                             │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│ SkillManager.execute_skill()                                    │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 1. 验证参数                                                   │ │
│ │ 2. 生成 pandas 代码                                          │ │
│ │ 3. 执行代码                                                   │ │
│ │ 4. 返回结果                                                   │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│ ReAct Observation: 返回分组统计结果                              │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Skill 与 LLM 的配合

```python
def get_skill_prompt(self) -> str:
    """生成 Skills 提示词，告诉 LLM 有哪些工具可用"""
    
    return """
## 可用的 Skills (工具)

你可以使用以下工具来完成任务：

- group_aggregate: 分组聚合分析 (参数: group_by, agg_column)
- filter_data: 数据筛选 (参数: column, operator, value)
- create_chart: 创建图表 (参数: chart_type, x_column, y_column)

## 调用格式

当需要使用工具时，返回 JSON：
{
    "tool": "工具名称",
    "parameters": {"参数名": "参数值"}
}
"""
```

---

## 第五步：知识关联

### Skills 与其他概念的关系

```
┌─────────────────────────────────────────────────────────────────┐
│                      Skills 工具系统                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   定义层 ──────────────────────────────────────────────────────  │
│   │                                                              │
│   │  skills/*.md ─────────────────────────────────────────────  │
│   │  • group_aggregate.md                                       │
│   │  • filter_data.md                                           │
│   │  • create_chart.md                                          │
│   │                                                              │
│   └───────────┬─────────────────────────────────────────────────┤
│               │                                                  │
│               ▼                                                  │
│   管理层 ──────────────────────────────────────────────────────  │
│   │                                                              │
│   │  agent/skills.py ─────────────────────────────────────────  │
│   │  • 加载 Skills                                              │
│   │  • 验证参数                                                  │
│   │  • 执行 Skill                                               │
│   │                                                              │
│   └───────────┬─────────────────────────────────────────────────┤
│               │                                                  │
│               ▼                                                  │
│   调用层 ──────────────────────────────────────────────────────  │
│   │                                                              │
│   │  ReAct Action ────────────────────────────────────────────  │
│   │  • Thought 阶段决定使用哪个 Skill                           │
│   │  • Action 阶段调用 Skill                                    │
│   │                                                              │
│   └───────────┬─────────────────────────────────────────────────┤
│               │                                                  │
│               ▼                                                  │
│   进化层 ──────────────────────────────────────────────────────  │
│   │                                                              │
│   │  进化引擎 ────────────────────────────────────────────────  │
│   │  • 分析高频问题                                              │
│   │  • 自动生成新 Skill                                         │
│   │                                                              │
│   └─────────────────────────────────────────────────────────────┘
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 第六步：练习思考

### 思考题

1. **为什么不直接让 LLM 生成代码，而要用 Skills？**
   - 答：Skills 是预定义、已验证的，更稳定可靠

2. **如何让 LLM 知道有哪些 Skills 可用？**
   - 答：通过 get_skill_prompt() 生成提示词，告诉 LLM

3. **新 Skill 是如何产生的？**
   - 答：进化引擎分析高频问题，自动生成新 Skill

### 练习题

1. 创建一个新的 Skill: `stat_summary`（统计摘要）
2. 修改 SkillManager，支持 Skill 的热加载
3. 实现一个 Skill 调用链（一个 Skill 调用另一个 Skill）

---

## 📚 延伸阅读

- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [LangChain Tools](https://python.langchain.com/docs/modules/tools/)

---

## 下一步

理解了 Skills 后，让我们学习 [04. 进化引擎](./04-evolution-engine.md)，看看 Agent 如何自我改进。