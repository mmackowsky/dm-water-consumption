import unittest
from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from config import get_settings
from database import Base, get_db
from main import app
from src.models import WaterConsumption

settings = get_settings()

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
        print(response.status_code)

    def test_get_water_consumptions(self):
        response = self.client.get("/api/water")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")

    def test_get_water_consumption_by_id(self):
        response = self.client.get("/api/water/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")

    def test_delete_water_measurement(self):
        response = self.client.delete("/api/water/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers["content-type"], "application/json")

    def test_delete_nonexistent_energy_measurement(self):
        response = self.client.delete("/api/energy/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()