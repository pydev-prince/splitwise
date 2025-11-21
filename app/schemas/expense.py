from pydantic import BaseModel
from typing import List

class SplitInput(BaseModel):
    user_id: int
    amount: float

class ExpenseCreate(BaseModel):
    group_id : int
    amount : float
    description : str | None = None
    splits: List[SplitInput]

class ExpenseOut(BaseModel):
    id: int
    group_id: int
    amount: float
    description: str | None = None
    paid_by: int
    splits : List[SplitInput]

    class Config:
        from_attributes = True
