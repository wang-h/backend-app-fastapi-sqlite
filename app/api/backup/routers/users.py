from models.user.models import User
from schema.user import Token
from core.config import settings
from core.db import get_session
from jwt import PyJWTError
import jwt
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import status, Response
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from jieba import Tokenizer
import jieba
from fastapi import APIRouter, Depends
from typing import Optional, List
from collections import defaultdict
from ..sql import crud
from ..sql import models
from ..sql import schemas
from ..sql.database import engine

from ..database import get_db
models.Base.metadata.create_all(bind=engine)
##########################################
login_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/")

# Dependency


@login_router.get("/create/")
def create_user(response: Response, name: str, email: str, password: str,  db: Session = Depends(get_db)):
    #
    db_user = crud.get_user_by_email(db, email=email)

    if db_user:
        response.status_code = status.HTTP_200_OK
        detail = "邮件/用户名已经存在"
    else:
        user = schemas.UserCreate(name=name, email=email, password=password)
        db_user = crud.create_user(db=db, user=user)
        response.status_code = status.HTTP_201_CREATED
        detail = "注册成功"
    data = {
        "name": db_user.name,
        "detail": detail}
    return data

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


SESSION_KEY = ""


def authenticate_user(username: str, password: str):
    """
    登陆认证
    """
    user = get_user(username)
    if not user:
        return None
    if not user.check_password(password):
        return None
    return user


def create_access_token(*, data: dict):
    """
    生成JWT token
    """
    to_encode = data.copy()
    # 设置token过期时间
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY)
    return encoded_jwt


def get_user(username):
    """
    查询用户
    """
    db = get_session()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    获取当前登陆用户
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    校验用户是否被激活
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="用户未激活")
    return current_user


@login_router.post("/login/", response_model=Token, name="用户登陆")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    获取token
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        settings.logger.error("账号密码错误!!!")
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="帐号或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        settings.logger.error(f"{user.username}未激活")
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="用户未激活!!!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return JSONResponse({"access_token": access_token.decode(), "token_type": "bearer"})


@login_router.post("/logout", name="用户登出")
def logout():
    return {"message": "已登出"}
