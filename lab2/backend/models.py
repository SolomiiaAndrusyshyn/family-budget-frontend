from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    personal_balance = Column(Float, default=0.0)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    type = Column(String, nullable=False)  # income або expense


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # deposit, withdraw
    description = Column(String, nullable=True)
    date = Column(Date, nullable=False)


class FamilyBudget(Base):
    __tablename__ = "family_budget"

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float, default=0.0)