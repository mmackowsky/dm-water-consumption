from sqlalchemy import Column, Integer, String

from database import Base


class WaterConsumption(Base):
    __tablename__ = "water_consumption"

    id = Column(Integer, primary_key=True, nullable=False)
    user = Column(Integer, nullable=False)
    measurement_date = Column(String, nullable=False)
    water_consumption = Column(Integer, nullable=False)
