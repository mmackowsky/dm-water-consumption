import uvicorn
from fastapi import FastAPI, HTTPException, Request, status

from config import get_settings
from database import SessionLocal, engine
from models import WaterConsumption

settings = get_settings()
app = FastAPI()
db = SessionLocal()


@app.get("/app/water", status_code=status.HTTP_200_OK)
async def get_water_consumptions(request: Request):
    return db.query(WaterConsumption).all()


@app.get("/app/water/{water_consumption_id}", status_code=status.HTTP_200_OK)
async def get_water_consumption_by_id(request: Request, water_consumption_id: int):
    return (
        db.query(WaterConsumption)
        .filter(WaterConsumption.id == water_consumption_id)
        .first()
    )


if __name__ == "__main__":
    WaterConsumption.metadata.create_all(bind=engine)
    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
