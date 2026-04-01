from pydantic import BaseModel
import datetime as dt


class RecordCreate(BaseModel):
    amount: float
    type: str  # income / expense
    category: str
    date: dt.date
    notes: str | None = None


class RecordUpdate(BaseModel):
    amount: float | None = None
    type: str | None = None
    category: str | None = None
    date: dt.date | None= None
    notes: str | None = None


class RecordResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: dt.date
    notes: str | None

    class Config:
        from_attributes = True