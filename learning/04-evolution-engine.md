# 04. 进化引擎

> 让 Agent 能够自我改进

---

## 🎯 学习目标

理解螺旋上升的两个层次：
- **每日进化** - 分析错误模式，低风险自动修复
- **每月进化** - 生成新 Skill，通知决策者

---

## 第一步：概念解释

### 进化引擎是什么？

**进化引擎 = Agent 的自我改进系统**

想象一个学习者：
- 📝 每天记录错误
- 📊 每周分析模式
- 🚀 每月总结提升

Agent 也需要这样的学习过程：
- 每日：分析日志，识别错误模式
- 每月：生成新 Skill，优化架构

### 螺旋上升 vs 即时反思

| 类型 | 时机 | 作用 |
|------|------|------|
| **即时反思 (ReAct)** | 会话内 | 当前任务失败时重试 |
| **螺旋上升 (进化引擎)** | 会话外 | 长期积累，持续改进 |

---

## 第二步：类比理解

### 类比 1：敏捷开发迭代

| 进化引擎 | 敏捷开发 | 说明 |
|----------|----------|------|
| 每日统计 | Daily Standup | 每天检查进度和问题 |
| 每月进化 | Sprint Review | 定期总结和改进 |
| Skill 生成 | 技术债务清理 | 优化代码结构 |

### 类比 2：机器学习训练

```
训练循环：
数据 → 前向传播 → 损失计算 → 反向传播 → 更新权重

进化循环：
日志 → 错误分析 → 模式识别 → 生成改进 → 更新 Skill
```

---

## 第三步：代码实现

### 进化引擎核心代码

```python
# evolution/engine.py

class EvolutionEngine:
    """进化引擎 - 螺旋上升"""
    
    def __init__(self):
        self.thresholds = {
            "same_error_count": 3,       # 同类错误次数阈值
            "same_correction_count": 2,   # 同一纠正次数阈值
            "monthly_corrections": 10,    # 月度纠正阈值
        }
    
    def daily_evolution(self) -> Dict:
        """
        每日进化 - 分析昨日日志
        
        流程：
        1. 收集统计数据
        2. 分析错误模式
        3. 分析纠正模式
        4. 检查触发条件
        5. 应用低风险修复
        """
        
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # 1. 收集统计
        daily_records = self._load_daily_logs(yesterday)
        correction_records = self._load_correction_logs(yesterday)
        
        report = {
            "statistics": {
                "total_interactions": len(daily_records),
                "total_failures": len([r for r in daily_records if r.get("result") == "failure"]),
                "total_corrections": len(correction_records),
            },
            "patterns": [],
            "actions": []
        }
        
        # 2. 分析错误模式
        error_patterns = self._analyze_error_patterns(daily_records)
        report["patterns"].extend(error_patterns)
        
        # 3. 检查触发条件
        for pattern in report["patterns"]:
            if pattern["count"] >= self.thresholds["same_error_count"]:
                # 触发修复
                report["actions"].append({
                    "type": "auto_fix",
                    "pattern": pattern["pattern"],
                    "risk": "low"
                })
        
        return report
    
    def monthly_evolution(self) -> Dict:
        """
        每月进化 - 深度分析和 Skill 生成
        
        流程：
        1. 汇总月度数据
        2. 识别高频问题
        3. 生成新 Skill 建议
        4. 通知决策者
        """
        
        # 汇总 30 天数据
        all_records = []
        for i in range(30):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            all_records.extend(self._load_daily_logs(date))
        
        # 识别高频问题
        error_counter = Counter()
        for record in all_records:
            if record.get("result") == "failure":
                error_counter[record.get("error", "")[:100]] += 1
        
        # 生成 Skill 建议
        skills_to_create = []
        for error, count in error_counter.most_common(10):
            if count >= 5:
                skills_to_create.append({
                    "error_pattern": error,
                    "frequency": count,
                    "suggested_skill": f"handle_{error[:20]}"
                })
        
        return {
            "statistics": {...},
            "skills_to_create": skills_to_create,
            "notify_decision_maker": True
        }
```

### Java 程序员的理解

```java
// Java 伪代码类比

@Component
public class EvolutionEngine {
    
    @Scheduled(cron = "0 0 1 * * ?")  // 每天凌晨1点执行
    public EvolutionReport dailyEvolution() {
        // 1. 收集昨日日志
        List<InteractionLog> logs = logRepository.findByDate(yesterday);
        
        // 2. 统计分析
        Map<String, Integer> errorPatterns = analyzeErrors(logs);
        
        // 3. 检查触发条件
        List<Action> actions = new ArrayList<>();
        for (Map.Entry<String, Integer> entry : errorPatterns.entrySet()) {
            if (entry.getValue() >= 3) {
                actions.add(new Action("auto_fix", entry.getKey()));
            }
        }
        
        // 4. 保存报告
        return saveReport(actions);
    }
    
    @Scheduled(cron = "0 0 2 1 * ?")  // 每月1号凌晨2点执行
    public EvolutionReport monthlyEvolution() {
        // 1. 汇总月度数据
        List<InteractionLog> logs = logRepository.findLast30Days();
        
        // 2. 识别高频问题
        List<SkillSuggestion> skills = generateSkillSuggestions(logs);
        
        // 3. 通知决策者
        notificationService.notifyDecisionMaker(skills);
        
        return saveReport(skills);
    }
}
```

---

## 第四步：详细解析

### 1. 触发条件设计

```python
TRIGGER_CONFIG = {
    # 每日触发
    "daily": {
        "same_error_count": 3,      # 同类错误出现 3 次
        "same_correction_count": 2,  # 同一纠正出现 2 次
    },
    
    # 每月触发
    "monthly": {
        "total_corrections": 10,     # 累计纠正 10 次
        "affected_users": 3,         # 影响 3 个用户
    }
}
```

**类比 Java：**

```java
// 类似业务规则引擎
public class TriggerConfig {
    public static final int SAME_ERROR_THRESHOLD = 3;
    public static final int MONTHLY_CORRECTIONS_THRESHOLD = 10;
    
    public boolean shouldTriggerDaily(List<Error> errors) {
        Map<String, Long> counts = errors.stream()
            .collect(Collectors.groupingBy(Error::getType, Collectors.counting()));
        
        return counts.values().stream().anyMatch(c -> c >= SAME_ERROR_THRESHOLD);
    }
}
```

### 2. 风险分级

```
┌─────────────────────────────────────────────────────────────────┐
│                        风险分级                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   低风险 ─────────────────────────────────────────────────────  │
│   • 参数默认值调整                                               │
│   • 提示词优化                                                   │
│   • 文档更新                                                     │
│   → 自动应用                                                     │
│                                                                  │
│   中风险 ─────────────────────────────────────────────────────  │
│   • 新 Skill 生成                                                │
│   • 代码逻辑修改                                                 │
│   → 记录待审                                                     │
│                                                                  │
│   高风险 ─────────────────────────────────────────────────────  │
│   • 架构变更                                                     │
│   • 安全策略修改                                                 │
│   → 通知决策者                                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3. 日志分析流程

```
┌─────────────────────────────────────────────────────────────────┐
│                      日志分析流程                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   logs/daily/2026-03-17.jsonl                                   │
│   │                                                              │
│   │  {"timestamp": "...", "query": "...", "result": "failure",  │
│   │   "error": "列名不存在: 授信类型"}                            │
│   │                                                              │
│   └───────────┬─────────────────────────────────────────────────┤
│               │                                                  │
│               ▼                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              错误分类统计                                 │   │
│   │                                                          │   │
│   │  列名不存在: 授信类型    → 5 次                          │   │
│   │  类型错误: 合同金额      → 3 次                          │   │
│   │  语法错误                → 2 次                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│               │                                                  │
│               ▼                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              触发检查                                     │   │
│   │                                                          │   │
│   │  "列名不存在" 出现 5 次 ≥ 3 次 → 触发修复                │   │
│   └─────────────────────────────────────────────────────────┘   │
│               │                                                  │
│               ▼                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              生成修复                                     │   │
│   │                                                          │   │
│   │  建议：添加列名检查，提示用户可用列名                     │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 第五步：知识关联

### 进化引擎与其他概念的关系

```
┌─────────────────────────────────────────────────────────────────┐
│                      进化引擎                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   数据来源 ─────────────────────────────────────────────────────│
│   │                                                              │
│   │  logs/daily/        → 每日交互数据                          │
│   │  logs/corrections/  → 用户纠正记录                          │
│   │  working_memory     → ReAct 的反思                          │
│   │                                                              │
│   └───────────┬─────────────────────────────────────────────────┤
│               │                                                  │
│               ▼                                                  │
│   分析处理 ─────────────────────────────────────────────────────│
│   │                                                              │
│   │  错误模式识别 → 触发自动修复                                │
│   │  高频问题发现 → 生成新 Skill                                │
│   │  用户偏好分析 → 更新默认配置                                │
│   │                                                              │
│   └───────────┬─────────────────────────────────────────────────┤
│               │                                                  │
│               ▼                                                  │
│   输出结果 ─────────────────────────────────────────────────────│
│   │                                                              │
│   │  skills/generated/  → 自动生成的 Skills                     │
│   │  logs/evolution/    → 进化报告                              │
│   │  通知决策者         → 月度报告                              │
│   │                                                              │
│   └─────────────────────────────────────────────────────────────┘
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 第六步：练习思考

### 思考题

1. **为什么不即时应用所有改进？**
   - 答：避免引入新问题，需要分级处理

2. **进化引擎如何与 ReAct 配合？**
   - 答：ReAct 的反思存入日志，进化引擎分析日志

3. **如何判断一个改进是低风险还是高风险？**
   - 答：根据影响范围和可逆性判断

### 练习题

1. 修改触发阈值，观察进化行为变化
2. 添加一个新的错误分类规则
3. 实现一个邮件通知决策者的功能

---

## 📚 延伸阅读

- [Reflexion 论文](https://arxiv.org/abs/2303.11366)
- [Chain of Hindsight](https://arxiv.org/abs/2304.05318)

---

## 下一步

理解了进化引擎后，让我们学习 [05. Hooks 机制](./05-hooks-mechanism.md)，看看如何扩展 Agent 的行为。