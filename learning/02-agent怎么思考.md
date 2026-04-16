# 🟢 02 — Agent 怎么思考？（ReAct 循环）

> 💡 一句话：**思考 → 行动 → 观察 → 反思，循环直到搞定。**

---

## 一个故事：程序员修 Bug

你修 Bug 的过程就是这样：

```
🤔 Thought："这个报错可能是空指针，得看看日志"
🔧 Action：打开日志文件，搜索错误关键字
👀 Observation：日志显示 NullPointerException at line 42
🔄 Reflection："果然是空指针。等等，为什么 line 42 会是 null？"

🤔 Thought："上游的 getUser() 可能返回了 null"
🔧 Action：打开 UserDAO.java，查看 getUser 方法
👀 Observation：getUser 在用户不存在时返回 null
🔄 Reflection："找到了！应该加个判断"

🤔 Thought："用 Optional 更优雅"
🔧 Action：重写 getUser，返回 Optional<User>
👀 Observation：编译通过，测试通过！
✅ 搞定！
```

**这就是 ReAct 循环。Agent 就是这样思考的。**

---

## ReAct 四步

| 步骤 | 做什么 | 类比 |
|------|--------|------|
| **Thought** 🤔 | 想下一步该做什么 | 做题前先想思路 |
| **Action** 🔧 | 执行操作 | 写下答案 |
| **Observation** 👀 | 看结果对不对 | 检查答案 |
| **Reflection** 🔄 | 错了就想为什么 | 分析错因 |

## 真实 Agent 例子

任务："帮我修复这个 Python 脚本的 bug"

```
1. 🤔 Thought："先看看代码"
2. 🔧 Action：read_file("script.py")
3. 👀 Observation：第 15 行有语法错误（缩进不对）
4. 🔄 Reflection："缩进问题，直接修复"
5. 🔧 Action：patch("script.py", old="    x=1", new="x = 1")
6. 👀 Observation：语法检查通过！
7. 🤔 Thought："再跑一下测试确认"
8. 🔧 Action：python script.py
9. 👀 Observation：运行成功 ✅
10. 告诉用户已修复
```

## 为什么 Reflection 最重要？

**没有 Reflection 的 Agent：**
```
试了方法 A → 失败 → 又试方法 A → 又失败 → 无限循环 💀
```

**有 Reflection 的 Agent：**
```
试了方法 A → 失败 → 反思"为什么失败" → 换方法 B → 成功 ✅
```

> Reflection 让 Agent **从失败中学习**，而不是原地打转。

## 总结

> ReAct = 先想再做，做完检查，错了反思。就像你修 Bug 的过程一样自然。
>
> 下一篇 → [Agent 怎么被管理？](03-agent怎么被管理.md)
