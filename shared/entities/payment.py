from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, Field

@dataclass(frozen=True)
class Payment(BaseModel):
    transaction_id: uuid4
    user_id: uuid4
    date: datetime
    nb_of_items: int = Field(gt=0)
    total_amount: Decimal = Field(ge=0.01, decimal_places=2)