"""
配置文件
"""
import os
from dotenv import load_dotenv

load_dotenv()

# 高德地图配置
AMAP_API_KEY = os.getenv("AMAP_API_KEY", "")
AMAP_BASE_URL = "https://restapi.amap.com/v3"

# 搜索配置
DEFAULT_RADIUS = int(os.getenv("DEFAULT_RADIUS", 3000))  # 默认搜索半径(米)
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "杭州")

# POI 类型编码
POI_TYPES = {
    "parking": "150900",        # 停车场
    "roadside": "150901",       # 路边停车场
    "underground": "150902",    # 地下停车场
    "ground": "150903",         # 地面停车场
}

# 可能表示免费的关键词
FREE_KEYWORDS = ["免费", "路边", "路面", "公共"]

# 路边停车 POI 类型
ROADSIDE_TYPES = ["路边停车场", "路面停车场"]