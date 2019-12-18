from sqlalchemy import Column, Integer, String

from image_upload.database import Base


class Images(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    bucket_link = Column(String)
