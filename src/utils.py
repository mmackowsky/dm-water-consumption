from sqlalchemy import desc

from config import get_settings
from database import SessionLocal
from models import WaterConsumption

settings = get_settings()


def set_new_id(db: SessionLocal):
    last_object_id = (
        db.query(WaterConsumption).order_by(desc(WaterConsumption.id)).first()
    )
    next_id = (last_object_id.id + 1) if last_object_id.id else 1
    return next_id
