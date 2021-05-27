from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from jieba import Tokenizer
import jieba
from fastapi import APIRouter, Depends
from ..sql import crud
from ..sql import models
from ..sql import schemas
from ..sql.database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import status, Response
from ..database import get_db
models.Base.metadata.create_all(bind=engine)
##########################################
router = APIRouter()


# @router.post("/")
# def read_admin(response: Response, email: str, password: str,  db: Session = Depends(get_db)):
#     #
#     db_admin = crud.get_admin_by_email(db, email=email)

#     if db_admin:
#         response.status_code = status.HTTP_200_OK
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="邮件/密码错误")

#     return db_admin.id


@router.post("/")
def create_admin(response: Response, email: str, password: str,  db: Session = Depends(get_db)):
    db_admin = crud.get_admin_by_email(db, email=email)

    if db_admin:
        response.status_code = status.HTTP_200_OK
    admin = schemas.AdminCreate(email=email, password=password)
    db_admin = crud.create_admin(db=db, admin=admin)

    return {"data": db_admin}

    #     response.status_code = status.HTTP_200_OK
    #     db_user = crud.create_user(db=db, user=user)
    #     data = {
    #         "user": db_user}
    #     return data
    # def create_user(response: Response, user: schemas.User, db: Session = Depends(get_db)):
    #     db_user = crud.get_user_by_email(db, email=user.email)
    #     if db_user:
    #         raise HTTPException(status_code=400, detail="Email already registered")


# @router.get("/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @router.get("/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @router.delete('/{user_id}', response_model=schemas.User)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.delete_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @router.put("/{user_id}", response_model=schemas.User)
# def update_user(user_id: int, update_user: schemas.User, db: Session = Depends(get_db)):
#     updated_user = crud.update_user(db, user_id, update_user)
#     if updated_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return updated_user
