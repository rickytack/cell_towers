from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# noinspection PyUnresolvedReferences
from web_app.grpc_client.generated.task_worker_pb2 import TaskType, TaskResponse
from web_app.core.services.cell_tower_sevice import CellTowerService
from models.pydantic import CellTowerList, AreaCoordinates, GeoPointBase, TriangleRead, TriangleList
from models.models import CellTower
from db.session import get_db

from web_app.grpc_client.grpc_client import task_worker_client

router = APIRouter()


@router.get("/towers", response_model=CellTowerList)
async def get_towers(
        db: AsyncSession = Depends(get_db),
        limit: int = Query(2000, ge=1, le=2000)
) -> CellTowerList:
    result = await db.execute(
        select(CellTower).order_by(CellTower.id).limit(limit)
    )
    towers: list[CellTower] = list(result.scalars().all())  # Explicit conversion

    return CellTowerService.convert_from_orm_list(towers)


@router.get("/towers/area", response_model=CellTowerList)
async def get_towers_in_rectangle(
        coords: AreaCoordinates = Depends(),
        db: AsyncSession = Depends(get_db),
        limit: int = Query(2000, ge=1, le=2000)
) -> CellTowerList:
    """
    Get cell towers within a geographic rectangle.

    Uses AreaCoordinates model for input validation.
    """
    towers: list[CellTower] = await CellTowerService.get_towers_in_area(db, coords, limit)
    return CellTowerService.convert_from_orm_list(towers)


@router.get("/towers/triangles", response_model=TriangleList)
async def get_towers_triangles(
        coords: AreaCoordinates = Depends(),
        db: AsyncSession = Depends(get_db)
) -> TriangleList:

    towers: list[CellTower] = await CellTowerService.get_towers_in_area(db, coords)

    task_response: TaskResponse = await task_worker_client.process_task(towers, TaskType.TRIANGULATION)
    #print("!!! qRPC res: ", task_response.polygons)

    triangles = []
    for polygon in task_response.polygons.polygons:
        #print("!!! polygon: ", polygon)

        # for vertice in polygon.vertices:
        #     print("!!! vertice: ", vertice)

        triangle = TriangleRead(points=[GeoPointBase(lat=geo_point.lat, lon=geo_point.lng)
                                        for geo_point in polygon.vertices], area=0)
        triangles.append(triangle)

    return TriangleList(triangles=triangles, count=len(task_response.polygons.polygons))
