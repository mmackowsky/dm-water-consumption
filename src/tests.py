import unittest
from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app
from src.models import WaterConsumption

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
db = TestingSessionLocal()
energy = WaterConsumption(
    id=1,
    user=1,
    measurement_date=datetime.now().strftime("%Y-%m-%d"),
    water_consumption=100,
)
db.add(energy)
db.commit()
db.refresh(energy)


print(db.query(WaterConsumption).all())


class TestEnergyAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_water_consumption(self):
        response = self.client.get("/api/water")
        print(response.json())
        print(response.text)
        print(response.status_code)


if __name__ == "__main__":
    unittest.main()
