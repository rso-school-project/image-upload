from sqlalchemy import Column, Integer, String

from image_upload.database import Base


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    file_hash = Column(String)
    file_name = Column(String)
