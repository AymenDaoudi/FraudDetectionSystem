from dataclasses import dataclass
from decimal import Decimal
from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel, Field

@dataclass(frozen=True)
class Payment(BaseModel):
    operation_id: uuid4
    user_id: uuid4
    date: datetime
    price: Decimal = Field(ge=0.01, decimal_places=2)