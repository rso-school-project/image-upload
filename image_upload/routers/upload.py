import time

from typing import List
from fastapi import APIRouter, Depends
from starlette.requests import Request
from func_timeout import func_set_timeout
from sqlalchemy.orm import Session


from image_upload import settings
from image_upload.utils import fallback
from image_upload.database import crud, models, schemas, get_db, engine

try:
    models.Base.metadata.create_all(bind=engine, checkfirst=True)
except:
    pass

router = APIRouter()


@router.post('/upload/')
def read_users(request: Request):
    return {}


@router.get('/settings')
async def test_configs(request: Request):
    return {"Config for X:": f"{settings.config_x}", "Config for Y:": f"{settings.config_y}"}
