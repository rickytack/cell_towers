import csv
from sqlalchemy import Column, Integer, Index, Float, BigInteger, Enum, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from typing import Optional, List

from db.session import AsyncSessionLocal
from .enum import RadioType

Base = declarative_base()


class CellTower(Base):
    __tablename__ = 'cell_tower'

    id = Column(Integer, primary_key=True)
    radio = Column(Enum(RadioType, name="radio_types"), nullable=False)
    mcc = Column(Integer, nullable=False, index=True)
    mnc = Column(Integer, nullable=False, index=True)
    lac = Column(Integer, nullable=False)
    cellid = Column(Integer, nullable=False)
    unused = Column(Integer, default=0)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    range = Column(Integer)                    # in meters
    samples = Column(Integer)
    changeable = Column(Integer, default=1)
    created = Column(BigInteger)
    updated = Column(BigInteger)
    average_signal = Column(Integer, default=0)

    __table_args__ = (
        Index('ix_coordinates', 'lat', 'lon'),
    )

    def created_datetime(self):
        return datetime.datetime.fromtimestamp(self.created)

    def updated_datetime(self):
        return datetime.datetime.fromtimestamp(self.updated)

    def __repr__(self):
        return (f"<CellTower({self.radio.value} {self.mcc}-{self.mnc}, "
                f"LAC:{self.lac}, Cell:{self.cellid}, "
                f"at {self.lat:.4f}°N {self.lon:.4f}°E)>")

    @classmethod
    async def create_simple(cls, **kwargs):
        async with AsyncSessionLocal() as session:
            new_tower = cls(**kwargs)
            session.add(new_tower)
            await session.commit()
            return new_tower

    @classmethod
    async def _commit_batch(cls, towers: List):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                try:
                    session.add_all(towers)
                    print(f"Committed {len(towers)} towers")
                except Exception as e:
                    print(f"Batch failed: {e}")
                    raise

    @classmethod
    async def import_opencellid_towers(cls, csv_path: str, batch_size: int = 1000):
        batch: List[cls] = []

        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    tower = cls(
                        radio=RadioType[row[0]],
                        mcc=int(row[1]),
                        mnc=int(row[2]),
                        lac=int(row[3]),
                        cellid=int(row[4]),
                        unused=int(row[5]),
                        lon=float(row[6]),
                        lat=float(row[7]),
                        range=int(row[8]) if row[8] else None,
                        samples=int(row[9]) if row[9] else None,
                        changeable=int(row[10]),
                        created=int(row[11]),
                        updated=int(row[12]),
                        average_signal=int(row[13])
                    )
                    batch.append(tower)

                    if len(batch) >= batch_size:
                        await cls._commit_batch(batch)
                        batch = []

                except Exception as e:
                    print(f"Skipped row {row}: {e}")
                    continue

            if batch:
                await cls._commit_batch(batch)
