# 08 - 安全与沙箱

> Agent 执行代码时的安全保护

---

## 🎯 概念解释

### 什么是沙箱？

**简单说**：一个隔离的环境，Agent 在里面执行代码，不会影响真实系统。

就像：
- **游乐场**：孩子可以在里面随便玩，不会跑丢
- **虚拟机**：系统和主机隔离，崩溃也不影响主机
- **浏览器沙箱**：网页 JS 不能访问本地文件

### 为什么需要沙箱？

| 风险 | 后果 | 沙箱保护 |
|------|------|---------|
| 删除文件 | 数据丢失 | 禁止文件操作 |
| 访问网络 | 数据泄露 | 禁止网络访问 |
| 无限循环 | 资源耗尽 | 超时强制终止 |
| 恶意代码 | 系统被控 | 隔离执行环境 |

---

## 🛡️ 安全机制

### 1. 代码审查（静态检查）

**在执行前检查代码**：

```python
class CodeValidator:
    """代码安全检查器"""
    
    DANGEROUS_PATTERNS = [
        r"import\s+os",           # 禁止导入 os
        r"import\s+subprocess",   # 禁止子进程
        r"open\s*\(",             # 禁止文件操作
        r"eval\s*\(",             # 禁止动态执行
        r"exec\s*\(",             # 禁止动态执行
        r"__import__",            # 禁止动态导入
        r"rm\s+-rf",              # 禁止删除命令
    ]
    
    def validate(self, code: str) -> tuple[bool, str]:
        """检查代码是否安全"""
        import re
        
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, code):
                return False, f"发现危险操作: {pattern}"
        
        return True, "代码安全"

# 使用
validator = CodeValidator()
is_safe, reason = validator.validate("import os; os.system('rm -rf /')")
# is_safe = False, reason = "发现危险操作: import os"
```

### 2. 执行超时

**限制执行时间**：

```python
import signal
import asyncio

class TimeoutExecutor:
    """超时执行器"""
    
    def __init__(self, timeout_seconds: int = 30):
        self.timeout = timeout_seconds
    
    async def execute(self, code: str, context: dict) -> dict:
        """带超时的代码执行"""
        try:
            result = await asyncio.wait_for(
                self._run_code(code, context),
                timeout=self.timeout
            )
            return {"success": True, "result": result}
        except asyncio.TimeoutError:
            return {"success": False, "error": "执行超时"}
    
    async def _run_code(self, code: str, context: dict):
        # 在受限环境中执行
        exec_globals = {"__builtins__": {}}
        exec(code, exec_globals)
        return exec_globals.get("result")

# 使用
executor = TimeoutExecutor(timeout_seconds=10)
result = await executor.execute("while True: pass", {})
# result = {"success": False, "error": "执行超时"}
```

### 3. 资源限制

**限制内存、CPU 使用**：

```python
import resource

class ResourceLimiter:
    """资源限制器"""
    
    def __init__(self, max_memory_mb: int = 512, max_cpu_seconds: int = 30):
        self.max_memory = max_memory_mb * 1024 * 1024  # 转为字节
        self.max_cpu = max_cpu_seconds
    
    def apply_limits(self):
        """应用资源限制"""
        # 限制内存
        resource.setrlimit(
            resource.RLIMIT_AS,
            (self.max_memory, self.max_memory)
        )
        # 限制 CPU 时间
        resource.setrlimit(
            resource.RLIMIT_CPU,
            (self.max_cpu, self.max_cpu)
        )

# 使用
limiter = ResourceLimiter(max_memory_mb=256, max_cpu_seconds=10)
limiter.apply_limits()
```

### 4. 受限内置函数

**只允许安全的 Python 函数**：

```python
class SafeBuiltins:
    """安全的内置函数白名单"""
    
    SAFE_BUILTINS = {
        # 基础类型
        "int", "float", "str", "bool", "list", "dict", "tuple", "set",
        # 数学运算
        "abs", "min", "max", "sum", "round", "pow",
        # 类型检查
        "isinstance", "type", "len", "range", "enumerate", "zip",
        # 函数相关
        "map", "filter", "sorted", "reversed",
        # 打印（可选）
        "print",
    }
    
    @classmethod
    def get_safe_builtins(cls) -> dict:
        import builtins
        return {
            name: getattr(builtins, name)
            for name in cls.SAFE_BUILTINS
            if hasattr(builtins, name)
        }

# 使用
safe_globals = {"__builtins__": SafeBuiltins.get_safe_builtins()}
exec("result = sum([1, 2, 3])", safe_globals)
# 安全执行
```

---

## 🔧 Simple BI Agent 沙箱实现

### 当前实现

```python
# agent/react_engine.py 中的 Action 模块

class ActionExecutor:
    """安全代码执行器"""
    
    def __init__(self, df: pd.DataFrame, timeout: int = 30):
        self.df = df
        self.timeout = timeout
    
    def execute(self, code: str) -> dict:
        """执行 pandas 代码"""
        # 1. 代码安全检查
        is_safe, reason = self._validate_code(code)
        if not is_safe:
            return {"success": False, "error": reason}
        
        # 2. 准备执行环境
        exec_globals = {
            "pd": pd,           # 允许 pandas
            "np": np,           # 允许 numpy
            "df": self.df,      # 传入数据
            "__builtins__": self._get_safe_builtins()
        }
        
        # 3. 执行代码（带超时）
        try:
            exec(code, exec_globals)
            result = exec_globals.get("result")
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _validate_code(self, code: str) -> tuple[bool, str]:
        """代码安全检查"""
        # 检查危险模式
        dangerous = ["import os", "import subprocess", "open(", "eval(", "exec("]
        for pattern in dangerous:
            if pattern in code:
                return False, f"禁止使用: {pattern}"
        return True, "安全"
    
    def _get_safe_builtins(self) -> dict:
        """获取安全的内置函数"""
        # 只允许数据处理相关的函数
        return {
            "len": len,
            "range": range,
            "enumerate": enumerate,
            "zip": zip,
            "map": map,
            "filter": filter,
            "sorted": sorted,
            "list": list,
            "dict": dict,
            "str": str,
            "int": int,
            "float": float,
            "print": print,
        }
```

---

## 🧠 类比理解

### 类比 1: 银行金库

| 安全层 | 银行 | Agent 沙箱 |
|--------|------|-----------|
| 第一层 | 门禁卡 | 代码审查 |
| 第二层 | 摄像头监控 | 执行日志 |
| 第三层 | 时间限制 | 超时终止 |
| 第四层 | 保险柜 | 资源隔离 |

### 类比 2: 儿童游乐区

```
┌─────────────────────────────────┐
│         游乐区（沙箱）            │
│  ┌─────┐  ┌─────┐  ┌─────┐     │
│  │滑梯 │  │秋千 │  │沙坑 │     │
│  └─────┘  └─────┘  └─────┘     │
│                                 │
│  🚫 不能出去（禁止危险操作）      │
│  ⏰ 限时 1 小时（执行超时）       │
│  👀 老师看着（监控日志）          │
└─────────────────────────────────┘
```

---

## 📊 安全等级对比

| 等级 | 描述 | 适用场景 |
|------|------|---------|
| 🔴 **开放** | 无限制执行 | 完全信任的环境 |
| 🟡 **限制** | 代码审查 + 超时 | 内部使用 |
| 🟢 **沙箱** | 受限环境 + 资源限制 | 生产环境 |
| 🔵 **隔离** | Docker/容器隔离 | 多租户环境 |

---

## 🔮 进阶方案：Docker 沙箱

**更安全的隔离执行**：

```python
import docker

class DockerSandbox:
    """Docker 容器沙箱"""
    
    def __init__(self):
        self.client = docker.from_env()
        self.image = "python:3.11-slim"
    
    def execute(self, code: str, timeout: int = 30) -> dict:
        """在容器中执行代码"""
        try:
            # 创建临时容器
            container = self.client.containers.run(
                self.image,
                command=f"python -c '{code}'",
                mem_limit="256m",       # 内存限制
                cpu_period=100000,      # CPU 周期
                cpu_quota=50000,        # CPU 配额 (50%)
                network_disabled=True,  # 禁用网络
                remove=True,            # 执行后删除
                timeout=timeout
            )
            return {"success": True, "output": container.decode()}
        except Exception as e:
            return {"success": False, "error": str(e)}

# 使用
sandbox = DockerSandbox()
result = sandbox.execute("print('Hello from container!')")
```

---

## ⚠️ 常见安全陷阱

### 陷阱 1: 绕过 import 检查

```python
# 危险！可以通过 __import__ 绕过
code = "__import__('os').system('rm -rf /')"

# 防护：也禁止 __import__
if "__import__" in code:
    raise SecurityError("禁止动态导入")
```

### 陷阱 2: 通过字符串拼接绕过

```python
# 危险！可以通过字符串拼接绕过
code = "getattr(__builtins__, 'ex' + 'ec')('...')"

# 防护：完全替换 __builtins__，而不是过滤
safe_globals = {"__builtins__": {}}  # 空的 builtins
```

### 陷阱 3: 通过异常处理隐藏

```python
# 危险！可以通过异常处理隐藏恶意代码
code = """
try:
    import os
    os.system('...')
except:
    pass
"""

# 防护：解析 AST（抽象语法树）检查
import ast
tree = ast.parse(code)
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        raise SecurityError("禁止 import 语句")
```

---

## 📊 状态：实现情况

| 功能 | 状态 | 说明 |
|------|------|------|
| 代码审查 | ✅ 已实现 | 危险模式检查 |
| 执行超时 | ⚠️ 部分 | 当前无强制超时 |
| 资源限制 | 🔲 待开发 | 需要实现 memory/CPU 限制 |
| 受限 builtins | ✅ 已实现 | 白名单模式 |
| Docker 沙箱 | 🔲 待开发 | 更安全的隔离方案 |
| AST 检查 | 🔲 待开发 | 更精确的代码分析 |

---

## 💡 练习思考

1. **思考**：如果一个 Agent 需要访问数据库，怎么保证安全？

2. **实践**：修改 Simple BI Agent 的代码检查器，添加更多危险模式：
   ```python
   # 添加到 DANGEROUS_PATTERNS
   r"socket\.",          # 禁止网络操作
   r"pickle\.",          # 禁止序列化攻击
   r"subprocess\.",      # 禁止子进程
   ```

3. **挑战**：如何实现一个允许文件读取但禁止文件写入的沙箱？

---

## 🔗 相关概念

- [ReAct 框架](./01-react-framework.md) - Action 执行阶段
- [Hooks 机制](./05-hooks-mechanism.md) - 执行前后拦截点

---

*下一篇：[Prompt Engineering](./09-prompt-engineering.md)*