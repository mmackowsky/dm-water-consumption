from sqlalchemy import Column, Integer, String

from database import Base


class WaterConsumption(Base):
    __tablename__ = "water_consumption"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, nullable=False)
    user = Column(Integer, nullable=False)
    measurement_date = Column(String, nullable=False)
    water_consumption = Column(Integer, nullable=False)

    def __repr__(self):
        return (
            f"{self.id}, {self.user}, {self.measurement_date}, {self.water_consumption}"
        )
