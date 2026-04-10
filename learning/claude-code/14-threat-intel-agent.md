# 威胁情报 Agent 实战案例

> 来源：Claude Cookbook - Threat Intelligence Enrichment Agent

---

## 场景说明

构建一个自主调查 IOC（Indicators of Compromise）的 Agent：
- 查询多个威胁情报源
- 交叉验证发现
- 映射到 MITRE ATT&CK
- 生成结构化报告供 SIEM/SOAR 集成

---

## 第一步：概念解释

**IOC 是什么？**

IOC = 入侵指标，是攻击者留下的"痕迹"：
- IP 地址（恶意服务器）
- 文件哈希（恶意软件）
- 域名（钓鱼网站）

**威胁情报 Agent 做什么？**

输入一个 IOC → Agent 自动：
1. 查 IP 信誉（AbuseIPDB、GreyNoise、Shodan）
2. 查文件哈希（VirusTotal、MalwareBazaar）
3. 查域名（URLhaus、DomainTools）
4. 映射到 MITRE ATT&CK 战术/技术
5. 生成结构化报告

---

## 第二步：类比理解

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   传统方式 = 侦探手动查档案                                  │
│   → 去这个局查 → 去那个局查 → 手动比对 → 写报告              │
│   → 慢、容易漏                                              │
│                                                             │
│   Agent 方式 = AI 侦探助手                                  │
│   → "查这个 IP" → 自动查所有情报库                          │
│   → 自动交叉验证 → 自动生成报告                              │
│   → 快、全面、结构化                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 第三步：核心工具定义

### IP 信誉查询

```python
def lookup_ip_reputation(ip_address: str) -> dict:
    """
    查询 IP 信誉。

    生产环境：调用 AbuseIPDB、GreyNoise、Shodan API
    """
    # 返回示例数据结构
    return {
        "ip": "203.0.113.42",
        "country": "Russia",
        "abuse_confidence_score": 87,
        "total_reports": 1243,
        "threat_types": ["botnet_c2", "malware_distribution"],
        "known_malware_associations": ["Emotet", "Trickbot"],
        "open_ports": [443, 8080, 4444],
        "is_tor_exit_node": False,
        "tags": ["banking-trojan-c2", "spam-source"],
    }
```

### 文件哈希查询

```python
def lookup_file_hash(file_hash: str, hash_type: str) -> dict:
    """
    查询文件信誉。

    生产环境：调用 VirusTotal、MalwareBazaar API
    """
    return {
        "hash": "d131dd02c5e6eec4693d9a0698aff95c",
        "hash_type": "md5",
        "detections": 58,
        "total_engines": 72,
        "detection_rate": "80.6%",
        "malware_family": "Emotet",
        "malware_type": "banking_trojan",
        "severity": "critical",
        "behavior_summary": "通过 regsvr32 投放载荷，建立持久化...",
        "contacted_ips": ["203.0.113.42"],
        "contacted_domains": ["update-service-cdn.ru"],
    }
```

### 域名查询

```python
def lookup_domain(domain: str) -> dict:
    """
    查询域名信誉。

    生产环境：调用 URLhaus、DomainTools、WHOIS API
    """
    return {
        "domain": "secure-bankofamerica-login.com",
        "reputation_score": 98,
        "category": "phishing",
        "subcategory": "credential_harvesting",
        "targeted_brand": "Bank of America",
        "hosting_provider": "BulletProof Hosting Ltd",
        "ssl_issuer": "Let's Encrypt",
        "tags": ["phishing-kit", "credential-harvest"],
    }
```

### MITRE ATT&CK 映射

```python
def get_mitre_techniques(query: str) -> dict:
    """
    将行为映射到 MITRE ATT&CK 战术/技术。

    生产环境：查询 ATT&CK STIX/TAXII 或本地数据库
    """
    return {
        "techniques": [
            {"id": "T1071.001", "name": "Web Protocols", "tactic": "Command and Control"},
            {"id": "T1573.002", "name": "Asymmetric Cryptography", "tactic": "Command and Control"},
        ],
        "associated_groups": ["APT28", "Wizard Spider"],
        "detection_suggestions": [
            "监控非标准端口 HTTPS 出站",
            "检查自签名 TLS 证书",
        ],
    }
```

---

## 第四步：Agent 工作流

```
输入 IOC
    │
    ▼
┌─────────────────┐
│  分析 IOC 类型   │  ← IP / Hash / Domain
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  查询威胁情报源  │  ← 调用对应工具
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  交叉验证       │  ← 比对多个源的结果
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  MITRE 映射     │  ← 关联到攻击战术
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  生成结构化报告  │  ← SIEM/SOAR 可集成
└─────────────────┘
```

---

## 第五步：实际应用场景

### 场景 1：发现可疑 IP

```
输入：203.0.113.42

Agent 输出：
┌─────────────────────────────────────────────────────────────┐
│ 威胁情报报告                                                │
│                                                             │
│ IP: 203.0.113.42                                           │
│ 威胁等级: 高 (Abuse Score: 87)                              │
│                                                             │
│ 关联恶意软件:                                               │
│   - Emotet (银行木马)                                       │
│   - Trickbot (模块化木马)                                   │
│                                                             │
│ 威胁类型:                                                   │
│   - 僵尸网络 C2                                             │
│   - 恶软件分发                                              │
│   - 暴力破解                                                │
│                                                             │
│ MITRE ATT&CK:                                              │
│   - T1071.001 Web Protocols (C2)                           │
│   - T1008 Fallback Channels                                │
│                                                             │
│ 建议:                                                       │
│   - 立即封禁该 IP                                          │
│   - 检查是否有内网与其通信                                  │
│   - 审查相关账户凭证                                        │
└─────────────────────────────────────────────────────────────┘
```

### 场景 2：发现钓鱼域名

```
输入：secure-bankofamerica-login.com

Agent 输出：
┌─────────────────────────────────────────────────────────────┐
│ 威胁情报报告                                                │
│                                                             │
│ 域名: secure-bankofamerica-login.com                       │
│ 类别: 钓鱼网站                                              │
│ 目标品牌: Bank of America                                  │
│                                                             │
│ 威胁评分: 98/100                                            │
│                                                             │
│ 注册信息:                                                   │
│   - 注册商: NameSilo LLC                                   │
│   - 注册国: Panama                                         │
│   - 托商: BulletProof Hosting (Moldova)                    │
│                                                             │
│ MITRE ATT&CK:                                              │
│   - T1566.002 Spearphishing Link                           │
│   - T1598.003 Spearphishing for Information                │
│                                                             │
│ 建议:                                                       │
│   - 加入 DNS 黑名单                                        │
│   - 通知目标品牌                                           │
│   - 检查员工是否收到相关钓鱼邮件                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 第六步：集成到安全运营

### SIEM 集成

报告格式支持 JSON 导出，可直接导入 Splunk、ELK 等平台：

```json
{
  "ioc_type": "ip",
  "ioc_value": "203.0.113.42",
  "threat_level": "high",
  "confidence": 87,
  "malware_associations": ["Emotet", "Trickbot"],
  "mitre_techniques": ["T1071.001", "T1008"],
  "recommended_actions": ["block_ip", "investigate_connections"],
  "generated_at": "2026-04-10T12:00:00Z"
}
```

### SOAR 集成

可触发自动响应：
- 高威胁 IOC → 自动封禁
- 钓鱼域名 → 自动 DNS 黑名单
- 恶意软件哈希 → 自动隔离

---

## 知识关联

- **Agent Patterns** → 见 [12-agent-patterns.md](12-agent-patterns.md)
- **MCP 工具** → 见 [03-mcp-tools.md](03-mcp-tools.md)
- **工具设计** → 见 [13-effective-agents.md](13-effective-agents.md)

---

## 原文链接

- [Threat Intelligence Enrichment Agent](https://platform.claude.com/cookbook/tool-use-threat-intel-enrichment-agent)