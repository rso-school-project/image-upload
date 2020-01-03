import time
from PIL import Image
import hashlib
import numbers


from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from starlette.requests import Request
from func_timeout import func_set_timeout
from sqlalchemy.orm import Session
from google.cloud import storage


from image_upload import settings
from image_upload.utils import fallback
from image_upload.database import crud, models, schemas, get_db, engine

try:
    models.Base.metadata.create_all(bind=engine, checkfirst=True)
except:
    pass

router = APIRouter()


# Instantiates a client
storage_client = storage.Client()
bucket_name = "super_skrivni_bozickov_zaklad"
bucket = storage_client.bucket(bucket_name)



@router.post('/images/', response_model=schemas.Image)
def upload(*, user_id: int = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        Image.open(file.file)
    except:
        raise HTTPException(status_code=400, detail='Uploaded file is not an image.')

    if not isinstance(user_id, numbers.Number):
        raise HTTPException(status_code=400, detail='user_id is not a number.')

    # Get hash.
    file_hash = hashlib.sha1(file.filename.encode('utf-8')).hexdigest() + "." + file.filename.split(".")[-1]

    # Save to DB.
    new_image = crud.create_image(db=db, file_name=file.filename, file_hash=file_hash, user_id=user_id)
    iid = new_image.id

    # Upload to GC, append file ID to hash.
    file.file.seek(0)
    try:
        blob = bucket.blob(str(iid) + file_hash)
        blob.upload_from_file(file.file)
    except:
        crud.delete_image(db=db, image_id=iid)
        raise HTTPException(status_code=400, detail='Upload to gCloud failed.')

    return new_image


@router.delete('/images/{image_id}', response_model=schemas.Image)
def delete_image(image_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_image(db=db, image_id=image_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@router.get('/settings')
async def test_configs(request: Request):
    return {"Config for X:": f"{settings.config_x}", "Config for Y:": f"{settings.config_y}"}
