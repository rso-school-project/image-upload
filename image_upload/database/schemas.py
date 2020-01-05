from pydantic import BaseModel


class ImageBase(BaseModel):
    user_id: int


class ImageCreate(ImageBase):
    file: dict


class Image(ImageBase):
    id: int
    file_hash: str
    file_name: str
    tags: str

    class Config:
        orm_mode = True
