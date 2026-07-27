from pydantic import BaseModel, ConfigDict


class URLCreate(BaseModel):

    original_url: str

#---------------------------------

class URLResponse(BaseModel):

    id: int
    original_url: str
    short_code: str
    clicks: int

    model_config = ConfigDict(
        from_attributes=True
    )