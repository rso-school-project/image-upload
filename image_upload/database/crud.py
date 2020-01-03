from sqlalchemy.orm import Session

from . import models, schemas



def create_image(db: Session, file_name: str, file_hash: str, user_id: int):
    db_image = models.Image(file_name=file_name, file_hash=file_hash, user_id=user_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def delete_image(db: Session, image_id: int):
    db_image = db.query(models.Image).filter(models.Image.id == image_id).first()
    db.delete(db_image)
    db.commit()
    return db_image