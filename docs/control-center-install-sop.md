# Control Center 安装标准作业程序 (SOP)

**版本**: 1.0  
**创建时间**: 2026-03-16  
**触发事件**: Control Center 安装问题复盘

---

## 📋 启动前检查清单

### 1️⃣ 环境确认 (必做)

```bash
# 确认当前用户
whoami

# 确认用户权限
id

# 检查是否有旧进程
ps aux | grep -E "tsx|node.*control" | grep -v grep
```

**预期输出**:
- `whoami` → `admin` (或其他非 root 用户)
- `ps aux` → 无相关进程 (或记录 PID 准备清理)

---

### 2️⃣ Git 权限检查 (必做)

```bash
# 检查仓库所有者
ls -la /home/admin/.openclaw/workspace/apps/openclaw-control-center/ | head -3

# 如果不匹配，执行
git config --global --add safe.directory /home/admin/.openclaw/workspace/apps/openclaw-control-center

# 验证
git config --global --list | grep safe.directory
```

**预期输出**:
- 所有者匹配当前用户
- `safe.directory` 已配置

---

### 3️⃣ 配置验证 (必做)

```bash
# 检查 Gateway 配置
cat /home/admin/.openclaw/workspace/apps/openclaw-control-center/.env | grep GATEWAY_URL

# 检查实际监听端口
netstat -tlnp | grep openclaw-gat | grep 127.0.0.1

# 对比两者是否匹配
```

**预期输出**:
- `.env`: `GATEWAY_URL=ws://127.0.0.1:15846`
- `netstat`: `127.0.0.1:15846`
- **两者必须匹配！**

---

### 4️⃣ 启动服务

```bash
cd /home/admin/.openclaw/workspace/apps/openclaw-control-center

# 使用 pm2 启动 (推荐)
pm2 start npm --name "control-center" -- run dev:ui

# 或使用 PATH 增强版本
PATH=/home/admin/.local/share/pnpm:$PATH pm2 start npm --name "control-center" -- run dev:ui
```

**预期输出**:
```
[PM2] Starting /usr/bin/npm in fork_mode (1 instance)
[PM2] Done.
┌────┬───────────────────┬...
│ id │ name              │...│ status │...
├────┼───────────────────┼...┼────────┼...
│ 0  │ control-center    │...│ online │...
└────┴───────────────────┴...
```

---

### 5️⃣ 验证启动 (必做 - 全部通过才算成功)

```bash
# 等待 15 秒
sleep 15

# 1. 检查 pm2 状态
pm2 status

# 2. 检查端口监听
netstat -tlnp | grep 4310

# 3. 本地访问测试
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:4310/?section=overview&lang=zh

# 4. 公网访问测试
curl -s -o /dev/null -w "%{http_code}" http://121.196.165.176:4310/?section=overview&lang=zh

# 5. 检查错误日志
pm2 logs control-center --lines 50 --nostream | grep -E "error|Error"
```

**预期输出**:
| 检查项 | 预期结果 |
|--------|----------|
| pm2 status | `online` |
| 端口监听 | `0.0.0.0:4310 LISTEN` |
| 本地访问 | `200` 或 `302` |
| 公网访问 | `200` 或 `302` |
| 错误日志 | 无 error 输出 |

---

### 6️⃣ 持久化 (可选)

```bash
# 保存 pm2 进程列表
pm2 save

# 配置开机自启
pm2 startup
pm2 save
```

---

## 🚨 故障排查

### 问题 1: Git safe.directory 报错

**症状**:
```
fatal: detected dubious ownership in repository
```

**解决**:
```bash
git config --global --add safe.directory /path/to/repo
```

---

### 问题 2: Gateway 端口不匹配

**症状**:
- `.env` 配置与实际监听端口不一致

**解决**:
```bash
# 修正 .env
sed -i 's/15746/15846/' .env

# 重启服务
pm2 restart control-center
```

---

### 问题 3: 端口冲突 EADDRINUSE

**症状**:
```
Error: listen EADDRINUSE: address already in use 0.0.0.0:4310
```

**解决**:
```bash
# 删除 pm2 进程
pm2 delete control-center

# 清理旧进程
pkill -f "tsx.*index"

# 等待端口释放
sleep 2

# 重新启动
pm2 start npm --name "control-center" -- run dev:ui
```

---

### 问题 4: pm2 进程反复重启

**症状**:
- `pm2 status` 显示 `↺` 重启次数 > 0

**解决**:
```bash
# 查看详细日志
pm2 logs control-center --lines 100 --nostream

# 根据错误信息排查
# 常见原因：端口冲突、配置错误、依赖缺失
```

---

## 📊 验证清单

启动后必须全部通过：

- [ ] `pm2 status` → `online`
- [ ] `netstat -tlnp | grep 4310` → 有监听
- [ ] `curl http://127.0.0.1:4310` → 返回 200/302
- [ ] `curl http://PUBLIC_IP:4310` → 返回 200/302
- [ ] `pm2 logs` → 无 error
- [ ] 界面访问正常

---

## 🔗 相关文档

- [错误日志](../.learnings/ERRORS.md)
- [学习日志](../.learnings/LEARNINGS.md)
- [自我修复技能](../skills/self-repair/SKILL.md)

---

_最后更新：2026-03-16_
