from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Base schema with shared attributes
class StatementBase(BaseModel):
    transaction_type: str
    description: str
    amount: float
    sender_name: Optional[str] = None
    receiver_name: Optional[str] = None
    status: str

# Schema for creating a new statement
class StatementCreate(StatementBase):
    pass

# Schema for returning statement data
class StatementResponse(StatementBase):
    id: int
    date: datetime
    user_id: int

    class Config:
        from_attributes = True

# Schema for paginated statements
class StatementPage(BaseModel):
    items: List[StatementResponse]
    total: int
    skip: int
    limit: int