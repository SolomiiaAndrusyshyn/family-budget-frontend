from sqlalchemy.orm import Session
import models
import schemas


# ---------- USERS ----------

def get_users(db: Session):
    return db.query(models.User).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        password=user.password,
        role=user.role,
        personal_balance=0.0
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, data: schemas.UserCreate):
    user = get_user(db, user_id)
    if not user:
        return None
    user.username = data.username
    user.password = data.password
    user.role = data.role
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user


# ---------- CATEGORIES ----------

def get_categories(db: Session):
    return db.query(models.Category).all()


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(
        name=category.name,
        type=category.type
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id)
    if not category:
        return None
    db.delete(category)
    db.commit()
    return category


# ---------- FAMILY BUDGET ----------

def get_family_budget(db: Session):
    budget = db.query(models.FamilyBudget).first()
    if not budget:
        budget = models.FamilyBudget(balance=0.0)
        db.add(budget)
        db.commit()
        db.refresh(budget)
    return budget


def deposit_to_family(db: Session, tx: schemas.TransactionCreate):
    budget = get_family_budget(db)
    budget.balance += tx.amount

    transaction = models.Transaction(
        user_id=tx.user_id,
        category_id=tx.category_id,
        amount=tx.amount,
        type="deposit",
        description=tx.description,
        date=tx.date
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def withdraw_from_family(db: Session, tx: schemas.TransactionCreate):
    budget = get_family_budget(db)

    if budget.balance < tx.amount:
        return None

    budget.balance -= tx.amount

    user = get_user(db, tx.user_id)
    user.personal_balance += tx.amount

    transaction = models.Transaction(
        user_id=tx.user_id,
        category_id=tx.category_id,
        amount=tx.amount,
        type="withdraw",
        description=tx.description,
        date=tx.date
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


# ---------- TRANSACTIONS ----------

def get_all_transactions(db: Session):
    return db.query(models.Transaction).all()


def get_user_transactions(db: Session, user_id: int):
    return db.query(models.Transaction).filter(
        models.Transaction.user_id == user_id
    ).all()