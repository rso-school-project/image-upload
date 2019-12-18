from pydantic import BaseModel


class ImageBase(BaseModel):
    user_id: int
    bucket_link: str


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: int

    class Config:
        orm_mode = True
