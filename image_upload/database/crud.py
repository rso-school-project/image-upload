from sqlalchemy.orm import Session

from . import models
from . import schemas

#
# def create_image_record(db: Session, item: schemas.ImageCreate, user_id: int):
#     db_item = models.Images(**item.dict(), user_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
