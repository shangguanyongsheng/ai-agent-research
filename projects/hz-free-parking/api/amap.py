"""
高德地图 API 封装
"""
import httpx
from typing import Optional, List, Dict, Any
from config import AMAP_API_KEY, AMAP_BASE_URL, POI_TYPES


class AMapAPI:
    """高德地图 Web 服务 API 封装"""
    
    def __init__(self, api_key: str = AMAP_API_KEY):
        self.api_key = api_key
        self.base_url = AMAP_BASE_URL
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def search_around(
        self,
        location: str,
        keywords: Optional[str] = None,
        types: Optional[str] = None,
        radius: int = 3000,
        offset: int = 25,
        page: int = 1,
        extensions: str = "all"
    ) -> Dict[str, Any]:
        """
        周边搜索 API
        
        Args:
            location: 中心点坐标，格式：经度,纬度
            keywords: 搜索关键词
            types: POI 类型编码
            radius: 搜索半径(米)，最大 50000
            offset: 每页记录数，最大 25
            page: 当前页码
            extensions: 返回数据控制，base/all
        
        Returns:
            API 响应数据
        """
        url = f"{self.base_url}/place/around"
        params = {
            "key": self.api_key,
            "location": location,
            "radius": radius,
            "offset": offset,
            "page": page,
            "extensions": extensions,
        }
        
        if keywords:
            params["keywords"] = keywords
        if types:
            params["types"] = types
        
        response = await self.client.get(url, params=params)
        return response.json()
    
    async def search_parking(
        self,
        location: str,
        radius: int = 3000,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        搜索附近停车场
        
        Args:
            location: 中心点坐标
            radius: 搜索半径(米)
            page: 页码
        
        Returns:
            停车场列表
        """
        return await self.search_around(
            location=location,
            keywords="停车场",
            types=POI_TYPES["parking"],
            radius=radius,
            page=page
        )
    
    async def geocode(
        self,
        address: str,
        city: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        地址转坐标
        
        Args:
            address: 地址字符串
            city: 城市名称
        
        Returns:
            坐标信息
        """
        url = f"{self.base_url}/geocode/geo"
        params = {
            "key": self.api_key,
            "address": address,
        }
        if city:
            params["city"] = city
        
        response = await self.client.get(url, params=params)
        return response.json()
    
    async def regeocode(
        self,
        location: str,
        extensions: str = "base"
    ) -> Dict[str, Any]:
        """
        坐标转地址（逆地理编码）
        
        Args:
            location: 坐标，格式：经度,纬度
            extensions: 返回数据控制
        
        Returns:
            地址信息
        """
        url = f"{self.base_url}/geocode/regeo"
        params = {
            "key": self.api_key,
            "location": location,
            "extensions": extensions,
        }
        
        response = await self.client.get(url, params=params)
        return response.json()
    
    async def close(self):
        """关闭 HTTP 客户端"""
        await self.client.aclose()


# 同步版本（用于简单测试）
class AMapAPISync:
    """高德地图 API 同步版本"""
    
    def __init__(self, api_key: str = AMAP_API_KEY):
        self.api_key = api_key
        self.base_url = AMAP_BASE_URL
    
    def search_around(
        self,
        location: str,
        keywords: Optional[str] = None,
        types: Optional[str] = None,
        radius: int = 3000,
        extensions: str = "all"
    ) -> Dict[str, Any]:
        """周边搜索（同步版本）"""
        import requests
        
        url = f"{self.base_url}/place/around"
        params = {
            "key": self.api_key,
            "location": location,
            "radius": radius,
            "extensions": extensions,
        }
        
        if keywords:
            params["keywords"] = keywords
        if types:
            params["types"] = types
        
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    
    def search_parking(self, location: str, radius: int = 3000) -> Dict[str, Any]:
        """搜索附近停车场（同步版本）"""
        return self.search_around(
            location=location,
            keywords="停车场",
            types=POI_TYPES["parking"],
            radius=radius
        )