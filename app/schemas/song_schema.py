from pydantic import BaseModel

class Song(BaseModel):
    path: str
