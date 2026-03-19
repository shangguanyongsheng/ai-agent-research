# 02. 记忆系统

> 让 Agent 能够记住和学习

---

## 🎯 学习目标

理解 Agent 的三种记忆：
- **全局记忆** - 所有用户共享的规则
- **用户记忆** - 每个用户独立的偏好
- **工作记忆** - 当前会话的反思

---

## 第一步：概念解释

### 为什么 Agent 需要记忆？

想象一个没有记忆的助手：

```
用户：我喜欢表格展示
Agent：好的，用表格展示

（下次对话）

用户：分析销售数据
Agent：用柱状图展示 ← 忘了用户喜欢表格！
```

**有记忆的助手：**

```
用户：我喜欢表格展示
Agent：好的，记住你喜欢表格

（下次对话）

用户：分析销售数据
Agent：用表格展示 ← 记住了用户偏好！
```

### Claude Code 的双记忆系统

Claude Code 有两种记忆：

| 类型 | 谁编写 | 存什么 |
|------|--------|--------|
| **CLAUDE.md** | 用户 | 规则、偏好、约定 |
| **Auto Memory** | Claude | 学习到的内容 |

**我们借鉴这个设计，增加了用户隔离！**

---

## 第二步：类比理解

### 类比 1：Java 应用配置

| Agent 记忆 | Java 类比 | 说明 |
|------------|-----------|------|
| 全局记忆 | application.yml | 所有用户共享的配置 |
| 用户记忆 | 用户 Session | 每个用户独立的配置 |
| 工作记忆 | 方法局部变量 | 当前请求有效 |

### 类比 2：数据库设计

```
memory/
├── BI_RULES.md              ← 全局配置表（所有记录共享）
│
└── users/
    ├── user_001/
    │   ├── preferences.json  ← 用户配置表（按 user_id 隔离）
    │   └── corrections.jsonl ← 用户历史表
    │
    └── user_002/
        └── ...
```

**类比 SQL：**

```sql
-- 全局记忆
SELECT * FROM global_rules;  -- BI_RULES.md

-- 用户记忆
SELECT * FROM user_preferences WHERE user_id = 'user_001';

-- 工作记忆（内存中，会话级）
-- 类似 Connection 级别的临时变量
```

---

## 第三步：代码实现

### 记忆管理器核心代码

```python
# agent/core.py

class MemoryManager:
    """记忆管理器 - 管理双记忆系统"""
    
    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = Path(memory_dir)
        self.user_manager = UserManager(memory_dir)
    
    def load_session_context(self, user_id: str) -> Dict:
        """
        加载会话上下文
        
        返回：
        {
            "global_rules": "全局规则内容",
            "user_memory": {"preferences": {...}, "corrections": [...]},
            "user_id": "user_001"
        }
        """
        context = {
            "global_rules": self._load_global_rules(),
            "user_memory": self.user_manager.get_or_create_user(user_id),
            "user_id": user_id or "default"
        }
        return context
    
    def _load_global_rules(self) -> str:
        """加载全局规则（所有用户共享）"""
        rules_file = self.memory_dir / "BI_RULES.md"
        if rules_file.exists():
            return rules_file.read_text(encoding="utf-8")
        return ""
```

### Java 程序员的理解

```java
// Java 伪代码类比

public class MemoryManager {
    private Path memoryDir;
    private UserManager userManager;
    
    /**
     * 加载会话上下文
     * 类似于 Spring 的 @SessionScope Bean
     */
    public SessionContext loadSessionContext(String userId) {
        SessionContext context = new SessionContext();
        
        // 1. 加载全局规则（类似 application.yml）
        context.setGlobalRules(loadGlobalRules());
        
        // 2. 加载用户记忆（类似用户 Session）
        context.setUserMemory(userManager.getOrCreateUser(userId));
        
        // 3. 设置用户ID
        context.setUserId(userId);
        
        return context;
    }
    
    private String loadGlobalRules() {
        // 类似读取 classpath:application.yml
        Path rulesFile = memoryDir.resolve("BI_RULES.md");
        if (Files.exists(rulesFile)) {
            return Files.readString(rulesFile);
        }
        return "";
    }
}
```

---

## 第四步：详细解析

### 1. 全局记忆 (BI_RULES.md)

**作用：** 定义所有用户共享的规则

```markdown
# BI_RULES.md - 通用分析规则

## 默认行为

1. 图表类型选择
   - 分类数据对比 → 柱状图
   - 明细数据 → 表格（默认）

2. 数据展示
   - 数值保留 2 位小数

## 安全规则

1. 代码执行使用沙箱环境
2. 禁止访问外部网络
```

**类比 Java：**
```yaml
# application.yml
bi:
  default-chart-type: table
  decimal-places: 2
  
security:
  sandbox: true
  network-access: false
```

### 2. 用户记忆（用户隔离）

**目录结构：**

```
memory/users/
├── user_001/
│   ├── MEMORY.md           # 用户记忆索引
│   ├── preferences.json    # 用户偏好
│   ├── corrections.jsonl   # 纠正记录
│   └── success_patterns.jsonl  # 成功模式
│
└── user_002/
    └── ...
```

**用户偏好文件 (preferences.json)：**

```json
{
  "chart_type": "table",
  "decimal_places": 2,
  "date_format": "YYYY-MM-DD"
}
```

**类比 Java：**

```java
// 用户配置实体
@Entity
@Table(name = "user_preferences")
public class UserPreferences {
    @Id
    private String userId;
    
    private String chartType = "table";
    private Integer decimalPlaces = 2;
    private String dateFormat = "YYYY-MM-DD";
}
```

### 3. 工作记忆（会话级）

**作用：** 存储当前会话的反思

```python
# agent/reflection.py

class ReflectionEngine:
    def __init__(self):
        self.working_memory = []  # 工作记忆
    
    def _reflect(self, query, trajectory, observation):
        """生成反思并存储"""
        reflection = self._analyze_error(observation)
        
        # 存入工作记忆
        self.working_memory.append({
            "query": query,
            "error": observation.get("error"),
            "reflection": reflection,
            "timestamp": datetime.now().isoformat()
        })
        
        return reflection
```

**类比 Java：**

```java
// 类似方法内的局部变量
public class ReflectionEngine {
    private List<Reflection> workingMemory = new ArrayList<>();
    
    public void reflect(String query, Observation observation) {
        Reflection reflection = analyzeError(observation);
        workingMemory.add(reflection);  // 方法结束时清空
    }
}
```

---

## 第五步：记忆加载流程

### 会话开始时的加载顺序

```
┌─────────────────────────────────────────────────────────────────┐
│                     会话开始                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  1. 加载全局规则 (BI_RULES.md)                                   │
│     • 编码标准                                                   │
│     • 安全规则                                                   │
│     • 默认行为                                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. 加载用户记忆 (memory/users/xxx/)                             │
│     • preferences.json → 用户偏好                                │
│     • corrections.jsonl → 历史纠正                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. 初始化工作记忆（空）                                          │
│     • 当前会话的反思会存入这里                                    │
│     • 会话结束后清空                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     开始处理用户请求                              │
└─────────────────────────────────────────────────────────────────┘
```

### 与 Claude Code 的对比

| 维度 | Claude Code | Simple BI Agent |
|------|-------------|-----------------|
| **全局记忆** | CLAUDE.md | BI_RULES.md |
| **用户记忆** | 无用户隔离 | ✅ 用户隔离 |
| **自动记忆** | Auto Memory (LLM 自动判断) | corrections.jsonl (只记录) |
| **加载方式** | 前 200 行 + 按需 | 完整加载 |

---

## 第六步：知识关联

### 记忆系统与其他概念的关系

```
┌─────────────────────────────────────────────────────────────────┐
│                      记忆系统                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   全局记忆 ─────────────────────────────────────────────────────│
│   │                                                              │
│   │  提供：默认规则、安全策略                                     │
│   │                                                              │
│   └───────────┬─────────────────────────────────────────────────┤
│               │                                                  │
│               ▼                                                  │
│   用户记忆 ─────────────────────────────────────────────────────│
│   │                                                              │
│   │  提供：用户偏好、历史纠正                                     │
│   │  用于：ReAct 的 Thought 阶段                                 │
│   │                                                              │
│   └───────────┬─────────────────────────────────────────────────┤
│               │                                                  │
│               ▼                                                  │
│   工作记忆 ─────────────────────────────────────────────────────│
│   │                                                              │
│   │  提供：当前会话的反思                                         │
│   │  来自：ReAct 的 Reflection 阶段                              │
│   │                                                              │
│   └───────────┬─────────────────────────────────────────────────┤
│               │                                                  │
│               ▼                                                  │
│   日志系统 ─────────────────────────────────────────────────────│
│   │                                                              │
│   │  记录：所有交互、纠正、错误                                   │
│   │  用于：进化引擎分析                                           │
│   │                                                              │
│   └─────────────────────────────────────────────────────────────┘
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 第七步：练习思考

### 思考题

1. **为什么不把所有内容都放在全局记忆？**
   - 答：不同用户有不同偏好，需要隔离

2. **工作记忆为什么不持久化？**
   - 答：工作记忆是当前会话的临时反思，会话结束后无意义

3. **如何让 Agent "记住"用户的偏好？**
   - 答：通过 corrections.jsonl 记录纠正，进化引擎定期分析

### 练习题

1. 为用户添加一个新的偏好字段（如 `language`）
2. 实现一个方法，返回用户最喜欢的图表类型
3. 添加一个 "黑名单" 功能，记录用户不喜欢的操作

---

## 📚 延伸阅读

- [Claude Code Memory](https://code.claude.com/docs/en/memory)
- [LangChain Memory](https://python.langchain.com/docs/modules/memory/)

---

## 下一步

理解了记忆系统后，让我们学习 [03. Skills 工具系统](./03-skills-system.md)，看看 Agent 如何使用工具。