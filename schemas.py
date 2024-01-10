from pydantic import BaseModel

class EventBase(BaseModel):
    name: str


class EventCreate(EventBase):
    description: str  


class Event(EventBase):
    id: int
    is_active: bool
    description: str