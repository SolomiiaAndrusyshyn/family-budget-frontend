from datetime import date
from typing import Literal
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=4, max_length=50)
    role: Literal["admin", "regular"]


class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    personal_balance: float

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    type: Literal["income", "expense"]


class CategoryResponse(CategoryCreate):
    id: int

    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    user_id: int = Field(gt=0)
    category_id: int | None = None
    amount: float = Field(gt=0)
    type: Literal["deposit", "withdraw"]
    description: str | None = Field(default=None, max_length=200)
    date: date


class TransactionResponse(TransactionCreate):
    id: int

    class Config:
        from_attributes = True


class FamilyBudgetResponse(BaseModel):
    balance: float

    class Config:
        from_attributes = True