# 杭州免费停车位查询

> 基于高德地图 API，查找杭州市附近的免费停车位

---

## 🎯 项目目标

用户打开一个位置点，查找附近免费停车位。

---

## 📋 你需要做的

### 第一步：注册高德开发者账号

1. 访问：https://lbs.amap.com/
2. 点击右上角「注册」
3. 选择「个人开发者」认证

### 第二步：创建应用获取 Key

1. 进入控制台：https://console.amap.com/dev/key/app
2. 点击「创建新应用」
3. 填写应用名称：`杭州免费停车位查询`
4. 添加 Key：
   - 服务平台：选择「Web 服务」
   - 提交后获取 Key

### 第三步：免费额度

| 认证类型 | 每日配额 | 并发数 |
|---------|---------|--------|
| 个人开发者 | 5,000 次/天 | 10 次/秒 |
| 企业开发者 | 30,000 次/天 | 50 次/秒 |

**个人认证完全够测试使用！**

---

## 🔧 技术方案

### 高德地图 API

**使用「周边搜索」API**：

```
GET https://restapi.amap.com/v3/place/around
```

**关键参数**：

| 参数 | 说明 | 示例 |
|------|------|------|
| `key` | 你的 API Key | `your-api-key` |
| `location` | 中心点坐标 | `120.1551,30.2741` |
| `keywords` | 搜索关键词 | `停车场` |
| `radius` | 搜索半径(米) | `3000` |
| `types` | POI 类型 | `150900` (停车场) |
| `extensions` | 返回详细信息 | `all` |

### POI 类型编码

停车场相关：
- `150900` - 停车场
- `150901` - 路边停车场
- `150902` - 地下停车场
- `150903` - 地面停车场

---

## 📂 项目结构

```
hz-free-parking/
├── README.md           # 项目说明
├── .env.example        # 环境变量示例
├── config.py           # 配置
├── api/
│   ├── __init__.py
│   └── amap.py         # 高德 API 封装
├── services/
│   ├── __init__.py
│   └── parking.py      # 停车位服务
├── app.py              # Web 应用
└── requirements.txt    # 依赖
```

---

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API Key
cp .env.example .env
# 编辑 .env，填入你的高德 API Key

# 3. 运行
python app.py
```

---

## 💡 核心功能

### 1. 搜索附近停车场

```python
# 输入：用户位置坐标
location = "120.1551,30.2741"  # 杭州市中心

# 输出：附近停车场列表
[
    {
        "name": "西湖文化广场停车场",
        "address": "西湖文化广场地下",
        "distance": 500,  # 距离(米)
        "parking_type": "地下",
        "location": "120.1623,30.2801",
        "is_free": True   # 是否免费(需要判断)
    }
]
```

### 2. 判断是否免费

高德 API 不直接返回「是否免费」，需要通过：
- 名称关键词：`免费`、`路边`
- 费用字段：`biz_ext.cost`（部分 POI 有）

---

## 📊 API 示例

### 请求

```bash
curl "https://restapi.amap.com/v3/place/around?key=YOUR_KEY&location=120.1551,30.2741&keywords=停车场&radius=3000&extensions=all"
```

### 响应

```json
{
  "status": "1",
  "pois": [
    {
      "id": "B0FFFAB6J2",
      "name": "西湖文化广场停车场",
      "type": "交通设施服务;停车场;地下停车场",
      "address": "西湖文化广场",
      "location": "120.162345,30.280123",
      "distance": "520",
      "parking_type": "地下"
    }
  ]
}
```

---

## ⚠️ 注意事项

1. **免费停车场判断**：高德不直接标注免费/收费，需要通过名称、类型推断
2. **API 限制**：个人开发者每天 5,000 次调用
3. **坐标系统**：高德使用 GCJ-02 坐标系，GPS 坐标需要转换

---

## 🔗 相关链接

- 高德开放平台：https://lbs.amap.com/
- Web 服务 API 文档：https://lbs.amap.com/api/webservice/summary
- 控制台：https://console.amap.com/

---

_📅 创建日期：2026-03-23_