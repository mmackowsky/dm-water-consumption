import unittest
from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from config import get_settings
from database import get_db  # Base out
from main import app
from models import WaterConsumption

settings = get_settings()

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)

Base = declarative_base()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


WaterConsumption.metadata.create_all(bind=engine)
# print("Created:")
# print(TestingSessionLocal().query(WaterConsumption).all())


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


class TestEnergyAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        app.dependency_overrides[get_db] = override_get_db

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=engine)

    def setUp(self):
        self.client = TestClient(app)
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
        db.close()

    def tearDown(self):
        db = TestingSessionLocal()
        db.query(WaterConsumption).delete()
        db.commit()
        db.close()

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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")

    def test_delete_nonexistent_energy_measurement(self):
        response = self.client.delete("/api/energy/999")
        self.assertEqual(response.status_code, 404)


# WaterConsumption.metadata.drop_all(bind=engine)


if __name__ == "__main__":
    unittest.main()
