import uvicorn
from fastapi import FastAPI, HTTPException, Request, status

from config import get_settings
from database import SessionLocal, engine
from models import WaterConsumption
from worker import periodic_task

settings = get_settings()
app = FastAPI()
db = SessionLocal()


@app.post("/api/energy/collect-data", status_code=status.HTTP_201_CREATED)
async def collect_data(request: Request):
    user_id = request.headers.get("request-user-id")
    data = periodic_task(user_id)
    return data


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


@app.delete("/api/water/{water_consumption_id}", status_code=status.HTTP_200_OK)
async def delete_water_measurement(water_consumption_id: int):
    measurement = (
        db.query(WaterConsumption)
        .filter(WaterConsumption.id == water_consumption_id)
        .first()
    )
    if not measurement:
        raise HTTPException(
            detail="Measurement not found", status_code=status.HTTP_404_NOT_FOUND
        )
    db.delete(measurement)
    db.commit()
    return {"message": "Measurement deleted"}


if __name__ == "__main__":
    WaterConsumption.metadata.create_all(bind=engine)
    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
