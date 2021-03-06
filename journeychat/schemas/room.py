from typing import Sequence

from pydantic import BaseModel, HttpUrl


class RoomBase(BaseModel):
    name: str
    is_private: bool


class RoomCreate(RoomBase):
    ...


class RoomUpdate(RoomBase):
    ...


# Properties shared by models stored in DB
class RoomInDBBase(RoomBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Room(RoomInDBBase):
    pass


# Properties properties stored in DB
class RoomInDB(RoomInDBBase):
    pass


class RoomSearchResults(BaseModel):
    results: Sequence[Room]
