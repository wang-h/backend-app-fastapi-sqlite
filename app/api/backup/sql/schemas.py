from typing import List, Optional

from pydantic import BaseModel

# 处理pydantic请求与响应的接口函数


class ItemBase(BaseModel):
    name: str
    description: str = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class Drug(BaseModel):
    id:                 int
    approval_number:    str
    name:               str
    dosage:             str
    specification:      str
    mah:                Optional[str]
    producer:           Optional[str]
    code:               int
    description:        str = None

    class Config:
        orm_mode = True


class DiseaseCreate(BaseModel):
    id:             int
    name:           str
    alias:          Optional[str]
    overview:       Optional[str]
    epidemiology:   Optional[str]
    etiology:       Optional[str]
    diagnostic_points: Optional[str]
    treatment:      Optional[str]
    prevention:     Optional[str]

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name:   str
    email:  str
    password: str

    class Config:
        orm_mode = True


class AdminCreate(BaseModel):
    email:  str
    password: str

    class Config:
        orm_mode = True

    # class UserCreate(UserBase):
    #     password: str

    # class UserUpdate(UserBase):
    #     is_active: bool

    # class User(UserBase):
    #     class Config:
    #         orm_mode = True
