from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AccountCreate(BaseModel):
    handle: str
    email: EmailStr
    secret: str

class SessionCreate(BaseModel):
    handle: str
    secret: str

class AccountOut(BaseModel):
    id: int
    handle: str
    email: str
    created: datetime

class EntryCreate(BaseModel):
    mood: int
    comment: Optional[str] = None
    sleep_hours: Optional[float] = None
    appetite: Optional[int] = None
    concentration: Optional[int] = None

class EntryOut(BaseModel):
    id: int
    account_id: int
    handle: str
    mood: int
    comment: Optional[str]
    sleep_hours: Optional[float]
    appetite: Optional[int]
    concentration: Optional[int]
    created: datetime
