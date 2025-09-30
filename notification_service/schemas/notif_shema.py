
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum




class NotificationKind(str, Enum):
    BROADCAST = "broadcast"
    LIST = "list"
    PERSONAL = "personal"

# for receiving from other services
class ReceiveNotifySchema(BaseModel):

    sender_id: Optional[int] = None
    receiver_ids: Optional[List[int]] = None
    message: str
    kind: NotificationKind

# for sending to clients
class SendNotifySchema(BaseModel):
    id: int
    sender_id: Optional[int] = None # ممکن است فرستنده سیستم باشد
    receiver_id: int
    message: str
    is_read: bool
    is_received: bool
    created_at: int

    # این کلاس برای هماهنگی با SQLAlchemy/SQLModel لازم است
    class Config:
        orm_mode = True