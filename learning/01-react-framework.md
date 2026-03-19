# 01. ReAct 框架

> 让 Agent 能够思考、行动、观察、反思

---

## 🎯 学习目标

理解 ReAct 框架的四个核心步骤：
- Thought（思考）
- Action（行动）
- Observation（观察）
- Reflection（反思）

---

## 第一步：概念解释

### ReAct 是什么？

**ReAct = Reasoning + Acting**（推理 + 行动）

想象你在做一个数学题：
1. 🤔 先思考：这道题考的是什么公式？
2. ✍️ 然后行动：写出解题步骤
3. 👀 再观察：检查结果对不对
4. 🔄 如果不对，反思：哪里出错了？

这就是 ReAct 的核心思想！

### 为什么需要 ReAct？

**没有 ReAct 的 Agent：**
```
用户问题 → LLM 直接回答 → 结束
（错了就错了，不会修正）
```

**有 ReAct 的 Agent：**
```
用户问题 → 思考 → 行动 → 观察
                  ↓
              失败了？
                  ↓
              反思 → 重新思考 → 再次行动
```

---

## 第二步：类比理解

### 类比 1：程序员修 Bug

| ReAct 步骤 | 程序员修 Bug | Agent 分析数据 |
|------------|-------------|----------------|
| Thought | "这个 Bug 可能是空指针" | "用户想按授信类型分组" |
| Action | 打断点、看日志 | 执行分组代码 |
| Observation | 确实是空指针 | 结果正确/错误 |
| Reflection | "下次要加非空判断" | "分组列名拼写错误" |

### 类比 2：Java 异常处理

```java
// Java 异常处理类比
try {
    // Action: 执行代码
    result = processData(data);
} catch (Exception e) {
    // Observation: 捕获错误
    log.error("处理失败: " + e.getMessage());
    
    // Reflection: 反思
    if (e instanceof NullPointerException) {
        // 修正策略：添加空检查
        data = Optional.ofNullable(data).orElse(defaultValue);
        // 重试
        result = processData(data);
    }
}
```

---

## 第三步：代码实现

### ReAct 循环核心代码

```python
# agent/reflection.py

class ReflectionEngine:
    """ReAct 反思引擎"""
    
    def __init__(self, max_iterations: int = 3):
        self.max_iterations = max_iterations
        self.working_memory = []  # 工作记忆
    
    def analyze_with_reflection(self, query, df, llm_caller, code_executor):
        """
        ReAct 循环:
        Thought → Action → Observation → (失败则反思) → 重试
        """
        
        iteration = 0
        trajectory = []  # 记录整个轨迹
        
        while iteration < self.max_iterations:
            iteration += 1
            
            # === 1. Thought（思考）===
            thought = self._generate_thought(query, trajectory)
            trajectory.append({"step": "thought", "content": thought})
            
            # === 2. Action（行动）===
            action = self._decide_action(query, df, trajectory)
            trajectory.append({"step": "action", "content": action})
            
            # === 3. Observation（观察）===
            observation = code_executor(action["code"], df)
            trajectory.append({"step": "observation", "content": observation})
            
            # === 4. Evaluate（评估）===
            if self._is_success(observation):
                return {"success": True, "result": observation}
            
            # === 5. Reflection（反思）===
            reflection = self._reflect(query, trajectory, observation)
            self.working_memory.append(reflection)  # 存入工作记忆
            trajectory.append({"step": "reflection", "content": reflection})
        
        return {"success": False, "error": "达到最大重试次数"}
```

### Java 程序员的理解

```java
// Java 伪代码类比

public class ReactEngine {
    private int maxIterations = 3;
    private List<Reflection> workingMemory = new ArrayList<>();
    
    public Result analyzeWithReflection(String query, DataFrame df) {
        int iteration = 0;
        List<Trajectory> trajectory = new ArrayList<>();
        
        while (iteration < maxIterations) {
            iteration++;
            
            // 1. Thought
            String thought = generateThought(query, trajectory);
            trajectory.add(new Trajectory("thought", thought));
            
            // 2. Action
            Action action = decideAction(query, df, trajectory);
            trajectory.add(new Trajectory("action", action));
            
            // 3. Observation
            Observation observation = executeAction(action, df);
            trajectory.add(new Trajectory("observation", observation));
            
            // 4. Evaluate
            if (isSuccess(observation)) {
                return new Result(true, observation);
            }
            
            // 5. Reflection
            Reflection reflection = reflect(query, trajectory, observation);
            workingMemory.add(reflection);  // 存入工作记忆
            trajectory.add(new Trajectory("reflection", reflection));
        }
        
        return new Result(false, "达到最大重试次数");
    }
}
```

---

## 第四步：详细解析

### 1. Thought（思考）

```python
def _generate_thought(self, query, trajectory):
    """生成思考"""
    
    if len(trajectory) == 0:
        # 第一次思考：分析用户需求
        return f"分析用户需求：{query}"
    
    # 后续思考：基于反思调整策略
    last_reflection = None
    for t in reversed(trajectory):
        if t.get("step") == "reflection":
            last_reflection = t.get("content")
            break
    
    if last_reflection:
        return f"根据反思调整策略：{last_reflection}"
```

**类比 Java：**
```java
// 就像 Servlet 的 service() 方法
// 根据请求类型决定处理逻辑
if (firstRequest) {
    return "分析请求...";
} else {
    return "根据上次错误调整...";
}
```

### 2. Action（行动）

```python
def _decide_action(self, query, df, trajectory):
    """决定行动：选择 Skill 或生成代码"""
    
    # 优先使用 Skill
    if "分组" in query or "统计" in query:
        return {
            "type": "skill",
            "skill_name": "group_aggregate",
            "parameters": {"group_by": "...", "agg_column": "..."}
        }
    
    # 没有 Skill，生成代码
    return {
        "type": "code",
        "code": "result = df.groupby('...').sum()"
    }
```

**类比 Java：**
```java
// 就像策略模式，选择不同的处理策略
if (query.contains("分组")) {
    return new SkillAction("group_aggregate", params);
} else {
    return new CodeAction(generateCode(query));
}
```

### 3. Observation（观察）

```python
def _is_success(self, observation):
    """判断是否成功"""
    if isinstance(observation, dict):
        return not observation.get("error")
    return observation is not None
```

**类比 Java：**
```java
// 就像检查返回值
if (observation instanceof ErrorResponse) {
    return false;
}
return observation != null;
```

### 4. Reflection（反思）

```python
def _reflect(self, query, trajectory, observation):
    """生成反思"""
    
    error = observation.get("error", "")
    
    # 分析错误类型
    if "not in" in error.lower():
        return "列名不存在，应该先检查数据列名"
    elif "type" in error.lower():
        return "数据类型错误，应该先检查类型"
    else:
        return f"分析错误原因：{error}"
```

**类比 Java：**
```java
// 就像异常分类处理
if (error.contains("not in")) {
    return "列名不存在，检查列名";
} else if (error.contains("type")) {
    return "类型错误，检查类型";
}
```

---

## 第五步：知识关联

### ReAct 与其他概念的关系

```
┌─────────────────────────────────────────────────────────────────┐
│                       AI Agent 生态                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐     使用      ┌─────────────┐                │
│   │  ReAct 框架 │ ─────────────→ │   Skills    │                │
│   └─────────────┘                └─────────────┘                │
│         │                              │                         │
│         │ 存储反思                      │ 调用                    │
│         ▼                              ▼                         │
│   ┌─────────────┐                ┌─────────────┐                │
│   │  工作记忆   │                │  记忆系统   │                │
│   └─────────────┘                └─────────────┘                │
│         │                              │                         │
│         │ 提供数据                     │ 记录模式                │
│         ▼                              ▼                         │
│   ┌─────────────────────────────────────────────────┐           │
│   │                  进化引擎                        │           │
│   │   每日：分析 ReAct 轨迹 → 识别错误模式           │           │
│   │   每月：生成新 Skill → 优化 ReAct 策略          │           │
│   └─────────────────────────────────────────────────┘           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### ReAct vs Chain of Thought

| 维度 | Chain of Thought | ReAct |
|------|------------------|-------|
| **核心** | 推理链 | 推理 + 行动 |
| **交互** | 单次 | 循环迭代 |
| **错误处理** | 无 | 反思重试 |
| **工具使用** | 无 | 可调用工具 |

---

## 第六步：练习思考

### 思考题

1. **如果 ReAct 循环一直没有成功，会发生什么？**
   - 答：达到 max_iterations 后返回失败，避免无限循环

2. **工作记忆和长期记忆的区别？**
   - 工作记忆：当前会话有效，存储反思
   - 长期记忆：持久化存储，跨会话使用

3. **ReAct 如何与 Skills 配合？**
   - Thought 决定使用哪个 Skill
   - Action 调用 Skill
   - Observation 检查 Skill 结果

### 练习题

1. 修改 `max_iterations` 为 5，观察行为变化
2. 在 `_reflect` 中添加更多错误类型判断
3. 实现一个新的 Skill 并在 ReAct 中调用

---

## 📚 延伸阅读

- [ReAct 论文](https://arxiv.org/abs/2210.03629)
- [Reflexion 论文](https://arxiv.org/abs/2303.11366)
- [Lilian Weng: LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)

---

## 下一步

理解了 ReAct 框架后，让我们学习 [02. 记忆系统](./02-memory-system.md)，看看 Agent 如何记忆和学习。