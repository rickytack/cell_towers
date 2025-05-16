from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from typing import Optional, List
from datetime import datetime

from .enum import RadioType


class GeoPointBase(BaseModel):
    lon: float = Field(..., ge=-180, le=180)
    lat: float = Field(..., ge=-90, le=90)

# CellTower
class CellTowerBase(GeoPointBase):
    radio: RadioType
    mcc: int = Field(..., gt=0, le=999)
    mnc: int = Field(..., gt=0, le=999)
    lac: int = Field(..., ge=0)
    cellid: int = Field(..., ge=0)

class CellTowerCreate(CellTowerBase):
    range: Optional[int] = Field(None, ge=0)
    samples: Optional[int] = Field(None, ge=0)
    changeable: int = Field(1, ge=0, le=1)
    average_signal: int = Field(0, ge=-120, le=-30)

class CellTowerRead(CellTowerBase):
    id: int
    unused: int
    range: Optional[int]
    samples: Optional[int]
    changeable: int
    created: datetime
    updated: datetime
    average_signal: int

    @field_validator('created', 'updated', mode='before')
    def convert_timestamp(value):  # No cls parameter needed
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        return value

    model_config = ConfigDict(from_attributes=True)

class CellTowerList(BaseModel):
    towers: List[CellTowerRead]
    count: int

class AreaCoordinates(BaseModel):
    bottom_left_lat: float = Field(..., ge=-90, le=90)
    bottom_left_lon: float = Field(..., ge=-180, le=180)
    top_right_lat: float = Field(..., ge=-90, le=90)
    top_right_lon: float = Field(..., ge=-180, le=180)

    @model_validator(mode='after')
    def validate_rectangle_bounds(self):
        if not (self.bottom_left_lat < self.top_right_lat):
            raise ValueError("Latitude values must form valid range (bottom < top)")
        if not (self.bottom_left_lon < self.top_right_lon):
            raise ValueError("Longitude values must form valid range (left < right)")
        return self

class TriangleRead(BaseModel):
    points: List[GeoPointBase]
    area: float

class TriangleList(BaseModel):
    triangles: List[TriangleRead]
    count: int
