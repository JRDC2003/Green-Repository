from pydantic import BaseModel
from typing import Optional


class DeviceIn(BaseModel):
    name: str
    ip: str


class DeviceOut(BaseModel):
    id: int
    name: str
    ip: str
    online: bool
    last_seen: Optional[str]
