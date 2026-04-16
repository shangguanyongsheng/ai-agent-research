# ⚡ AI Agent 速查卡

> 1 分钟回顾全部核心概念

---

## 核心概念速查

| 概念 | 是什么（一句话） | 类比 |
|------|-----------------|------|
| **Agent** | 能自主完成任务的 AI | 🤖 智能助手 vs 普通聊天机器人 |
| **ReAct** | 思考→行动→观察→反思的循环 | 🔧 修 Bug：想→查→试→改 |
| **Harness** | 管理和控制 Agent 的框架 | 🚗 方向盘 + 刹车 + 仪表盘 |
| **记忆系统** | 长期记忆 + 工作记忆双系统 | 💾 硬盘（永久）+ 🧠 内存（临时） |
| **Skills** | Agent 的可插拔能力包 | 📱 手机 App，需要什么装什么 |
| **OpenClaw** | 自托管 AI 网关，多渠道聊天 | 🤖 智能客服后台 |
| **Claude Code** | 终端里的 AI 程序员 | 🏎️ 完全自动驾驶的汽车 |
| **进化引擎** | 每日分析错误，每月生成新技能 | 📝 错题本 + 月度总结 |
| **EvoMap** | 全球 Agent 共享知识网络 | 🌍 GitHub 开源 + 维基百科 |
| **Multi-Agent** | 多个专业 Agent 分工协作 | 🏢 公司的产品、开发、测试团队 |
| **安全沙箱** | 隔离 Agent 执行环境 | 🎪 游乐场的围栏 |
| **Prompt 工程** | 写好系统提示词引导 Agent | 📋 给新员工写工作手册 |

---

## 关键关系

```
        Agent（AI 大脑）
           │
     ┌─────┼─────┐
     ▼     ▼     ▼
  ReAct  记忆   Harness（管理控制）
  (思考)  (存储)    │
                   ▼
              ┌────┴────┐
              ▼         ▼
           Skills    安全沙箱
          (能力)     (保护)
              │
              ▼
        进化引擎 + EvoMap
         （自我改进）
              │
              ▼
         Multi-Agent
         （团队协作）
```

**一句话串联**：
> Agent **通过** ReAct 循环 **执行** 任务，**用** 记忆记住上下文，**通过** Skills 获得能力，**被** Harness 管理和保护。
> 进化引擎 **分析** Agent 的错误来生成新 Skills，EvoMap 让不同 Agent **共享** 知识，Multi-Agent 把多个 Agent **组合** 成团队。

---

## 快速问答

**Q：Agent 和 ChatGPT 有什么区别？**
A：ChatGPT 只能对话，Agent 能自主执行操作（读写文件、运行命令等）。

**Q：OpenClaw 和 Claude Code 有什么区别？**
A：OpenClaw 是聊天渠道网关（WhatsApp/Telegram/Discord），Claude Code 是终端 Agent。

**Q：Skills 和 Tools 有什么区别？**
A：Skills 是任务模板（做什么），Tools 是具体工具（怎么做）。Skill 内部调用 Tools。

**Q：什么时候用 Skills，什么时候用 CLAUDE.md？**
A：具体任务工作流用 Skills，项目规则/约定用 CLAUDE.md。

**Q：进化引擎怎么触发？**
A：同类错误 ≥3 次记录模式，同一纠正 ≥2 次自动修复，月度纠正 ≥10 次生成新 Skill。

**Q：Multi-Agent 适合所有场景吗？**
A：不适合。小任务一个 Agent 就够了，Multi-Agent 有额外成本（token、延迟、复杂度）。

**Q：GDI 评分是什么？**
A：EvoMap 的质量评分（0-100），由内在质量 35% + 使用指标 30% + 社交信号 20% + 新鲜度 15% 组成。

---

> 📖 想深入了解？→ [学习地图](README.md)
> 🟢 入门：[01](01-agent是什么.md) [02](02-agent怎么思考.md) [03](03-agent怎么被管理.md)
> 🟡 进阶：[04](04-agent怎么记住.md) [05](05-agent用什么工具.md) [06](06-agent怎么变聪明.md)
> 🟠 高阶：[07](07-多个agent怎么协作.md) [08](08-agent安全.md) [09](09-prompt工程.md)
