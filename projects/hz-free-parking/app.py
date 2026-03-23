"""
杭州免费停车位查询 - Web 应用
"""
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from services.parking import ParkingService, ParkingServiceSync
from config import DEFAULT_RADIUS, DEFAULT_CITY

app = FastAPI(
    title="杭州免费停车位查询",
    description="基于高德地图 API，查找杭州市附近的停车位",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 响应模型
class ParkingInfo(BaseModel):
    """停车场信息"""
    id: str
    name: str
    address: str
    location: str
    distance: int
    type: str
    parking_type: str
    tel: str = ""
    is_likely_free: bool
    free_reason: Optional[str] = None


class ParkingResponse(BaseModel):
    """停车位查询响应"""
    status: str
    count: int
    location: str
    radius: int
    parkings: List[ParkingInfo]


@app.get("/", response_class=HTMLResponse)
async def root():
    """API 首页"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>杭州免费停车位查询</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            code { background: #e0e0e0; padding: 2px 6px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🅿️ 杭州免费停车位查询</h1>
        <p>基于高德地图 API，查找附近停车位</p>
        
        <h2>API 接口</h2>
        
        <div class="endpoint">
            <h3>1. 查找附近所有停车场</h3>
            <code>GET /parking/nearby?location=经度,纬度&radius=半径</code>
            <p>示例：<a href="/parking/nearby?location=120.162345,30.280123">/parking/nearby?location=120.162345,30.280123</a></p>
        </div>
        
        <div class="endpoint">
            <h3>2. 只查找可能免费的停车场</h3>
            <code>GET /parking/free?location=经度,纬度</code>
            <p>示例：<a href="/parking/free?location=120.162345,30.280123">/parking/free?location=120.162345,30.280123</a></p>
        </div>
        
        <div class="endpoint">
            <h3>3. 查找路边停车位</h3>
            <code>GET /parking/roadside?location=经度,纬度</code>
            <p>杭州路边停车有免费时段（夜间、节假日）</p>
        </div>
        
        <hr>
        <p>📖 <a href="/docs">API 文档</a></p>
    </body>
    </html>
    """


@app.get("/parking/nearby", response_model=ParkingResponse)
async def find_nearby_parking(
    location: str = Query(..., description="中心点坐标，格式：经度,纬度，如 120.1551,30.2741"),
    radius: int = Query(DEFAULT_RADIUS, description="搜索半径(米)，最大 50000", ge=100, le=50000),
    filter_free: bool = Query(False, description="是否只返回可能免费的停车场")
):
    """查找附近停车场"""
    service = ParkingService()
    try:
        parkings = await service.find_nearby_parking(location, radius, filter_free)
        
        return ParkingResponse(
            status="success",
            count=len(parkings),
            location=location,
            radius=radius,
            parkings=parkings
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await service.close()


@app.get("/parking/free", response_model=ParkingResponse)
async def find_free_parking(
    location: str = Query(..., description="中心点坐标"),
    radius: int = Query(DEFAULT_RADIUS, description="搜索半径(米)", ge=100, le=50000)
):
    """只查找可能免费的停车场"""
    return await find_nearby_parking(location, radius, filter_free=True)


@app.get("/parking/roadside", response_model=ParkingResponse)
async def find_roadside_parking(
    location: str = Query(..., description="中心点坐标"),
    radius: int = Query(DEFAULT_RADIUS, description="搜索半径(米)", ge=100, le=50000)
):
    """查找路边停车位（杭州路边停车有免费时段）"""
    service = ParkingService()
    try:
        parkings = await service.find_roadside_parking(location, radius)
        
        return ParkingResponse(
            status="success",
            count=len(parkings),
            location=location,
            radius=radius,
            parkings=parkings
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await service.close()


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok"}


# 测试入口
def test_search():
    """测试搜索功能"""
    print("=" * 60)
    print("🅿️  杭州免费停车位查询 - 测试")
    print("=" * 60)
    
    # 测试坐标
    test_locations = [
        ("西湖文化广场", "120.162345,30.280123"),
        ("杭州火车站", "120.183589,30.243420"),
        ("武林广场", "120.161324,30.279186"),
    ]
    
    service = ParkingServiceSync()
    
    for name, location in test_locations:
        print(f"\n📍 {name} ({location})")
        print("-" * 50)
        
        # 查找所有停车场
        parkings = service.find_nearby_parking(location, 1000)
        print(f"   附近停车场: {len(parkings)} 个")
        
        # 显示前 5 个
        for i, p in enumerate(parkings[:5], 1):
            free_mark = "🆓" if p.get("is_likely_free") else "💰"
            print(f"   {i}. {free_mark} {p['name']}")
            print(f"      📍 {p['address']}")
            print(f"      📏 {p['distance']} 米 | {p['parking_type'] or '未知类型'}")
            if p.get("free_reason"):
                print(f"      ℹ️  {p['free_reason']}")
        
 # 统计免费停车场
        free_count = sum(1 for p in parkings if p.get("is_likely_free"))
        print(f"\n   📊 可能免费: {free_count} / {len(parkings)}")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成！")
    print("\n💡 提示: 启动 Web 服务运行 python app.py")
    print("📖 API 文档: http://localhost:8000/docs")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_search()
    else:
        print("🚀 启动服务: http://localhost:8000")
        print("📖 API 文档: http://localhost:8000/docs")
        uvicorn.run(app, host="0.0.0.0", port=8000)