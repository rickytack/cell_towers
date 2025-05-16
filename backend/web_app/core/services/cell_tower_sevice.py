from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.pydantic import AreaCoordinates, CellTowerRead, CellTowerList
from models.models import CellTower

class CellTowerService:
    @staticmethod
    async def get_towers_in_area(
        db: AsyncSession,
        coords: AreaCoordinates,
        limit: int = 3000
    ) -> list[CellTower]:
        """Get cell towers within specified geographical bounds"""
        query = (
            select(CellTower)
            .where(
                CellTower.lat.between(coords.bottom_left_lat, coords.top_right_lat),
                CellTower.lon.between(coords.bottom_left_lon, coords.top_right_lon)
            )
            .order_by(CellTower.id)
            .limit(limit)
        )

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    def convert_from_orm_list(db_towers: List[CellTower]):
        return CellTowerList(
            towers=[CellTowerRead.model_validate(tower) for tower in db_towers],
            count=len(db_towers))
