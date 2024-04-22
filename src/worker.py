import random
import time
from datetime import datetime, timedelta

from celery import Celery, shared_task

from config import get_settings
from database import SessionLocal
from models import WaterConsumption

settings = get_settings()
db = SessionLocal()

app = Celery("src")
app.conf.result_backend = settings.CELERY_RESULT_BACKEND
app.conf.update(
    broker_url=settings.CELERY_BROKER_URL,
    broker_connection_retry_on_startup=True,
)

app.autodiscover_tasks()
