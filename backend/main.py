from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import engine, get_db

app = FastAPI(title="Family Budget API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Family Budget API is running"}


# ---------- AUTH ----------

@app.post("/auth/login")
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password != data.password:
        raise HTTPException(status_code=401, detail="Wrong password")
    return {
        "message": "Login successful",
        "id": user.id,
        "username": user.username,
        "role": user.role
    }


# ---------- USERS ----------

@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.create_user(db, user)


@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}


# ---------- CATEGORIES ----------

@app.get("/categories", response_model=list[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


@app.post("/categories", response_model=schemas.CategoryResponse)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)


@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.delete_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted"}


# ---------- FAMILY BUDGET ----------

@app.get("/family/budget", response_model=schemas.FamilyBudgetResponse)
def get_family_budget(db: Session = Depends(get_db)):
    return crud.get_family_budget(db)


@app.post("/family/deposit", response_model=schemas.TransactionResponse)
def deposit(tx: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.deposit_to_family(db, tx)


@app.post("/family/withdraw", response_model=schemas.TransactionResponse)
def withdraw(tx: schemas.TransactionCreate, db: Session = Depends(get_db)):
    result = crud.withdraw_from_family(db, tx)
    if not result:
        raise HTTPException(status_code=400, detail="Not enough funds in family budget")
    return result


# ---------- HISTORY ----------

@app.get("/family/history", response_model=list[schemas.TransactionResponse])
def family_history(db: Session = Depends(get_db)):
    return crud.get_all_transactions(db)


@app.get("/users/{user_id}/history", response_model=list[schemas.TransactionResponse])
def user_history(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_transactions(db, user_id)