"""
停车位服务
"""
from typing import List, Dict, Any, Optional
from api.amap import AMapAPI, AMapAPISync
from config import FREE_KEYWORDS, DEFAULT_RADIUS, ROADSIDE_TYPES, POI_TYPES


class ParkingService:
    """停车位查询服务"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api = AMapAPI(api_key) if api_key else AMapAPI()
    
    async def find_nearby_parking(
        self,
        location: str,
        radius: int = DEFAULT_RADIUS,
        filter_free: bool = False
    ) -> List[Dict[str, Any]]:
        """查找附近停车场"""
        result = await self.api.search_parking(location, radius)
        
        if result.get("status") != "1":
            return []
        
        pois = result.get("pois", [])
        parking_list = []
        
        for poi in pois:
            parking_info = self._parse_parking(poi)
            if filter_free and not parking_info.get("is_likely_free"):
                continue
            parking_list.append(parking_info)
        
        parking_list.sort(key=lambda x: int(x.get("distance", 999999)))
        return parking_list
    
    async def find_roadside_parking(self, location: str, radius: int = DEFAULT_RADIUS) -> List[Dict[str, Any]]:
        """查找路边停车位"""
        result = await self.api.search_around(
            location=location,
            keywords="路边停车",
            types=POI_TYPES["roadside"],
            radius=radius
        )
        
        if result.get("status") != "1":
            return []
        
        pois = result.get("pois", [])
        parking_list = []
        
        for poi in pois:
            parking_info = self._parse_parking(poi)
            parking_info["is_likely_free"] = True
            parking_info["free_reason"] = "路边停车位（杭州夜间/节假日可能免费）"
            parking_list.append(parking_info)
        
        parking_list.sort(key=lambda x: int(x.get("distance", 999999)))
        return parking_list
    
    def _parse_parking(self, poi: Dict[str, Any]) -> Dict[str, Any]:
        """解析停车场信息"""
        name = poi.get("name", "")
        is_likely_free = self._check_if_free(name, poi)
        
        return {
            "id": poi.get("id"),
            "name": name,
            "address": poi.get("address", ""),
            "location": poi.get("location", ""),
            "distance": int(poi.get("distance", 0)),
            "type": poi.get("type", ""),
            "parking_type": poi.get("parking_type", "") or "",
            "tel": poi.get("tel", "") if isinstance(poi.get("tel"), str) else "",
            "is_likely_free": is_likely_free,
            "free_reason": self._get_free_reason(name, poi) if is_likely_free else None,
        }
    
    def _check_if_free(self, name: str, poi: Dict[str, Any]) -> bool:
        """判断是否可能是免费停车场"""
        for keyword in FREE_KEYWORDS:
            if keyword in name:
                return True
        
        parking_type = poi.get("parking_type", "")
        if parking_type in ROADSIDE_TYPES:
            return True
        
        poi_type = poi.get("type", "")
        if "路边" in poi_type:
            return True
        
        return False
    
    def _get_free_reason(self, name: str, poi: Dict[str, Any]) -> str:
        """获取判断为免费的原因"""
        for keyword in FREE_KEYWORDS:
            if keyword in name:
                return f"名称包含「{keyword}」"
        
        parking_type = poi.get("parking_type", "")
        if parking_type in ROADSIDE_TYPES:
            return "路边停车场"
        
        return "类型判断"
    
    async def close(self):
        """关闭 API 客户端"""
        await self.api.close()


# 同步版本
class ParkingServiceSync:
    """停车位查询服务（同步版本）"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api = AMapAPISync(api_key) if api_key else AMapAPISync()
    
    def find_nearby_parking(self, location: str, radius: int = DEFAULT_RADIUS, filter_free: bool = False) -> List[Dict[str, Any]]:
        """查找附近停车场（同步版本）"""
        result = self.api.search_parking(location, radius)
        
        if result.get("status") != "1":
            return []
        
        pois = result.get("pois", [])
        parking_list = []
        
        for poi in pois:
            parking_info = self._parse_parking(poi)
            if filter_free and not parking_info.get("is_likely_free"):
                continue
            parking_list.append(parking_info)
        
        parking_list.sort(key=lambda x: int(x.get("distance", 999999)))
        return parking_list
    
    def find_roadside_parking(self, location: str, radius: int = DEFAULT_RADIUS) -> List[Dict[str, Any]]:
        """查找路边停车位（同步版本）"""
        result = self.api.search_around(
            location=location,
            keywords="路边停车",
            types=POI_TYPES["roadside"],
            radius=radius
        )
        
        if result.get("status") != "1":
            return []
        
        pois = result.get("pois", [])
        parking_list = []
        
        for poi in pois:
            parking_info = self._parse_parking(poi)
            parking_info["is_likely_free"] = True
            parking_info["free_reason"] = "路边停车位"
            parking_list.append(parking_info)
        
        parking_list.sort(key=lambda x: int(x.get("distance", 999999)))
        return parking_list
    
    def _parse_parking(self, poi: Dict[str, Any]) -> Dict[str, Any]:
        """解析停车场信息"""
        name = poi.get("name", "")
        is_likely_free = self._check_if_free(name, poi)
        
        return {
            "id": poi.get("id"),
            "name": name,
            "address": poi.get("address", ""),
            "location": poi.get("location", ""),
            "distance": int(poi.get("distance", 0)),
            "type": poi.get("type", ""),
            "parking_type": poi.get("parking_type", ""),
            "tel": poi.get("tel", ""),
            "is_likely_free": is_likely_free,
        }
    
    def _check_if_free(self, name: str, poi: Dict[str, Any]) -> bool:
        """判断是否可能是免费停车场"""
        for keyword in FREE_KEYWORDS:
            if keyword in name:
                return True
        
        parking_type = poi.get("parking_type", "")
        if parking_type in ROADSIDE_TYPES:
            return True
        
        return False