# -*- encoding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from api.config import get_config


# 创建对象的基类:
Base = declarative_base()

# 初始化数据库连接:
engine = create_engine(get_config().SQLALCHEMY_DATABASE_URI)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = sessionmaker(bind=engine)
# Dependency


async def get_db_local():
    return SessionLocal()


async def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
