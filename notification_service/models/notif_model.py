from sqlmodel import SQLModel, Field
import time
from typing import Optional

class NotificationModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sender_id: Optional[int] = Field(default=None)
    receiver_id: int
    message: str
    created_at: int = Field(default_factory=lambda: int(time.time()))
    is_received: bool = Field(default=False, nullable=False)
    is_read: bool = Field(default=False, nullable=False)



