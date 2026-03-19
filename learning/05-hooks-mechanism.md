# 05. Hooks 机制

> 让 Agent 的行为可扩展

---

## 🎯 学习目标

理解 Hooks 的三个核心概念：
- **扩展点** - 在哪里可以拦截
- **拦截器** - 如何拦截和处理
- **执行链** - 如何组织多个 Hook

---

## 第一步：概念解释

### Hooks 是什么？

**Hooks = 钩子 = 扩展点**

想象你在餐厅点餐：
1. 📝 点餐前 - 服务员问"要不要加辣？"
2. 🍳 烹饪中 - 厨师按你的要求调整
3. 🍽️ 上菜后 - 服务员问"还要什么吗？"

这就是 Hooks！在关键节点插入自定义行为。

### 为什么需要 Hooks？

**没有 Hooks：**
```python
def execute_skill(skill_name, params):
    result = skill.execute(params)  # 无法扩展
    return result
```

**有 Hooks：**
```python
def execute_skill(skill_name, params):
    # 操作前 Hook
    params = pre_execute(params)  # 可以修改参数
    
    result = skill.execute(params)
    
    # 操作后 Hook
    result = post_execute(result)  # 可以修改结果
    
    return result
```

---

## 第二步：类比理解

### 类比 1：Spring AOP

| Agent Hooks | Spring AOP | 说明 |
|-------------|------------|------|
| 操作前拦截 | @Before | 方法执行前 |
| 操作后拦截 | @After | 方法执行后 |
| 环绕拦截 | @Around | 完全控制执行 |

### 类比 2：Servlet Filter

```java
// Servlet Filter 类比
public class LoggingFilter implements Filter {
    
    @Override
    public void doFilter(Request request, Response response, FilterChain chain) {
        // 操作前：记录请求
        log.info("Request: " + request.getPath());
        
        // 执行下一个 Filter 或 Servlet
        chain.doFilter(request, response);
        
        // 操作后：记录响应
        log.info("Response: " + response.getStatus());
    }
}
```

---

## 第三步：代码实现

### Hooks 机制设计

```python
# agent/hooks.py（待实现）

class HookType:
    """Hook 类型"""
    PRE_EXECUTE = "pre_execute"    # 执行前
    POST_EXECUTE = "post_execute"  # 执行后
    ON_ERROR = "on_error"          # 错误时
    ON_SUCCESS = "on_success"      # 成功时


class HookManager:
    """Hooks 管理器"""
    
    def __init__(self):
        self.hooks = {
            HookType.PRE_EXECUTE: [],
            HookType.POST_EXECUTE: [],
            HookType.ON_ERROR: [],
            HookType.ON_SUCCESS: [],
        }
    
    def register_hook(self, hook_type: str, hook_func):
        """注册 Hook"""
        self.hooks[hook_type].append(hook_func)
    
    def execute_hooks(self, hook_type: str, context: Dict) -> Dict:
        """执行指定类型的所有 Hooks"""
        for hook in self.hooks[hook_type]:
            context = hook(context)
        return context


# 使用示例
hook_manager = HookManager()

# 注册操作前 Hook
@hook_manager.register_hook(HookType.PRE_EXECUTE)
def validate_parameters(context):
    """验证参数"""
    params = context.get("parameters", {})
    if not params.get("group_by"):
        raise ValueError("缺少 group_by 参数")
    return context

# 注册操作后 Hook
@hook_manager.register_hook(HookType.POST_EXECUTE)
def format_result(context):
    """格式化结果"""
    result = context.get("result")
    if isinstance(result, pd.DataFrame):
        result = result.round(2)  # 保留2位小数
    context["result"] = result
    return context
```

### Java 程序员的理解

```java
// Java 伪代码类比

@Component
public class HookManager {
    
    private Map<HookType, List<Hook>> hooks = new HashMap<>();
    
    /**
     * 注册 Hook
     * 类似 Spring 的 @Order 注解控制顺序
     */
    public void registerHook(HookType type, Hook hook) {
        hooks.computeIfAbsent(type, k -> new ArrayList<>()).add(hook);
    }
    
    /**
     * 执行 Hooks
     * 类似 FilterChain.doFilter()
     */
    public Context executeHooks(HookType type, Context context) {
        for (Hook hook : hooks.get(type)) {
            context = hook.execute(context);
        }
        return context;
    }
}

// 定义 Hook
@FunctionalInterface
public interface Hook {
    Context execute(Context context);
}

// 使用示例
@Component
public class ValidationHook implements Hook {
    @Override
    public Context execute(Context context) {
        Map<String, Object> params = context.getParameters();
        if (params.get("group_by") == null) {
            throw new ValidationException("缺少 group_by 参数");
        }
        return context;
    }
}
```

---

## 第四步：详细解析

### 1. Hook 扩展点设计

```
┌─────────────────────────────────────────────────────────────────┐
│                      Hook 扩展点                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   用户请求                                                       │
│       │                                                          │
│       ▼                                                          │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ PRE_EXECUTE Hook                                         │   │
│   │ • 参数验证                                               │   │
│   │ • 权限检查                                               │   │
│   │ • 参数转换                                               │   │
│   └─────────────────────────────────────────────────────────┘   │
│       │                                                          │
│       ▼                                                          │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ 执行 Skill 或 代码                                        │   │
│   └─────────────────────────────────────────────────────────┘   │
│       │                                                          │
│       ├──────────────┬──────────────┐                            │
│       │              │              │                            │
│       ▼              ▼              ▼                            │
│   成功           失败           完成                              │
│       │              │              │                            │
│       ▼              ▼              ▼                            │
│   ON_SUCCESS     ON_ERROR      POST_EXECUTE                     │
│   Hook           Hook           Hook                            │
│   • 记录成功     • 记录错误     • 格式化结果                     │
│   • 发送通知     • 重试逻辑     • 缓存结果                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Hook 执行顺序

```python
class HookChain:
    """Hook 执行链 - 类似 Servlet FilterChain"""
    
    def __init__(self, hooks: List):
        self.hooks = hooks
        self.index = 0
    
    def next(self, context: Dict) -> Dict:
        """执行下一个 Hook"""
        if self.index < len(self.hooks):
            hook = self.hooks[self.index]
            self.index += 1
            return hook(context, self)
        return context


# Hook 定义
def logging_hook(context: Dict, chain: HookChain) -> Dict:
    """日志 Hook"""
    print(f"[PRE] 执行参数: {context.get('parameters')}")
    result = chain.next(context)  # 执行下一个
    print(f"[POST] 执行结果: {result.get('result')}")
    return result


def validation_hook(context: Dict, chain: HookChain) -> Dict:
    """验证 Hook"""
    params = context.get("parameters", {})
    if not params.get("group_by"):
        raise ValueError("缺少 group_by 参数")
    return chain.next(context)  # 继续执行
```

### 3. 内置 Hooks 示例

```python
# 内置 Hooks

def parameter_validation_hook(context: Dict) -> Dict:
    """参数验证 Hook"""
    params = context.get("parameters", {})
    
    # 检查必填参数
    required = context.get("required_params", [])
    for param in required:
        if param not in params:
            raise ValueError(f"缺少必填参数: {param}")
    
    return context


def result_formatting_hook(context: Dict) -> Dict:
    """结果格式化 Hook"""
    result = context.get("result")
    preferences = context.get("user_preferences", {})
    
    # 根据用户偏好格式化
    decimal_places = preferences.get("decimal_places", 2)
    
    if isinstance(result, pd.DataFrame):
        # 格式化数值列
        for col in result.select_dtypes(include=['number']).columns:
            result[col] = result[col].round(decimal_places)
    
    context["result"] = result
    return context


def error_logging_hook(context: Dict) -> Dict:
    """错误日志 Hook"""
    error = context.get("error")
    
    if error:
        # 记录错误日志
        activity_logger.log_interaction(
            user_id=context.get("user_id"),
            query=context.get("query"),
            result="failure",
            error=str(error)
        )
    
    return context
```

---

## 第五步：知识关联

### Hooks 与其他概念的关系

```
┌─────────────────────────────────────────────────────────────────┐
│                      Hooks 机制                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   被拦截的操作 ─────────────────────────────────────────────────│
│   │                                                              │
│   │  • ReAct Action (执行 Skill 或代码)                         │
│   │  • Skill 执行                                                │
│   │  • 结果返回                                                  │
│   │                                                              │
│   └───────────┬─────────────────────────────────────────────────┤
│               │                                                  │
│               ▼                                                  │
│   Hook 类型 ───────────────────────────────────────────────────│
│   │                                                              │
│   │  PRE_EXECUTE   → 操作前（验证、转换）                        │
│   │  POST_EXECUTE  → 操作后（格式化、缓存）                      │
│   │  ON_SUCCESS    → 成功时（记录、通知）                        │
│   │  ON_ERROR      → 失败时（日志、重试）                        │
│   │                                                              │
│   └───────────┬─────────────────────────────────────────────────┤
│               │                                                  │
│               ▼                                                  │
│   常见用途 ─────────────────────────────────────────────────────│
│   │                                                              │
│   │  • 参数验证 → 防止无效输入                                   │
│   │  • 结果格式化 → 按用户偏好展示                               │
│   │  • 日志记录 → 供进化引擎分析                                 │
│   │  • 性能监控 → 统计执行时间                                   │
│   │  • 权限检查 → 控制访问                                       │
│   │                                                              │
│   └─────────────────────────────────────────────────────────────┘
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 第六步：练习思考

### 思考题

1. **Hooks 和 AOP 的区别？**
   - 答：本质相同，都是切面编程的思想

2. **如何控制多个 Hook 的执行顺序？**
   - 答：通过 priority 或 order 属性

3. **Hook 中能做什么、不能做什么？**
   - 能：修改参数、修改结果、记录日志
   - 不能：阻塞执行（除非抛异常）

### 练习题

1. 实现一个性能监控 Hook，记录 Skill 执行时间
2. 实现一个缓存 Hook，缓存重复查询的结果
3. 实现一个权限 Hook，检查用户是否有权限执行某个 Skill

---

## 📚 延伸阅读

- [Claude Code Hooks](https://code.claude.com/docs/en/hooks)
- [Spring AOP](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#aop)

---

## 下一步

理解了所有概念后，让我们看 [06. 知识体系总结](./06-knowledge-map.md)，建立完整的知识网络。