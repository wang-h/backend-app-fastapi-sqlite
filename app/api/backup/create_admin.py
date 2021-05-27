from fastapi import APIRouter, Depends
from pydantic import main
from .sql import crud
from .sql import models
from .sql import schemas
from .sql.database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import status, Response

models.Base.metadata.create_all(bind=engine)
##########################################


# Dependency


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def create_admin(email: str, password: str,  db: Session = Depends(get_db)):
    #
    admin = schemas.AdminCreate(email=email, password=password)
    db_admin = crud.create_admin(db=db, admin=admin)

    return {"data": db_admin}


# if __name__ == "__main__":
#     create_admin(email="alveinwang@163.com", password="alveinwang")
