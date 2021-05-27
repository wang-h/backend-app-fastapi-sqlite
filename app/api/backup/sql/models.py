from enum import auto
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import false, true
from .database import Base

# 处理数据库的接口函数，定义各种数据对象的数据库中字段代理


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    is_active = Column(Boolean, default=True)
    name = Column(String, index=True, nullable=True)
    email = Column(String, index=True, nullable=True)
    hashed_password = Column(String, nullable=True)

    # items = relationship("Item", back_populates="owner")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Admin(Base):
    __tablename__ = "Admins"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    is_active = Column(Boolean, default=True)
    name = Column(String, index=True, nullable=True)
    email = Column(String, index=True, nullable=True)
    hashed_password = Column(String, nullable=True)

    # items = relationship("Item", back_populates="owner")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Disease(Base):
    __tablename__ = "disease"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, nullable=True)  # 【医学科】
    alias = Column(String, nullable=True)  # 【别名】
    overview = Column(Text, nullable=True)  # 【概述】
    epidemiology = Column(Text, nullable=True)  # 【流行病学】
    etiology = Column(Text, nullable=True)  # 【病因与发病机制】
    diagnostic_points = Column(Text, nullable=True)  # 【诊断要点】
    treatment = Column(Text, nullable=True)  # 【治疗概述】
    prevention = Column(Text, nullable=True)  # 【预防】

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class MedicalDepartment(Base):
    __tablename__ = "medical_department"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)  # 【医学科】
    description = Column(Text, nullable=True)  # 【描述】

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")

#     def to_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Drug(Base):
    __tablename__ = "domestic_drugs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    approval_number = Column(String)
    dosage = Column(String, nullable=True)
    specification = Column(String, nullable=True)
    mah = Column(String,  nullable=True)
    producer = Column(String,  nullable=True)
    code = Column(Text,  nullable=True)
    description = Column(Text,  nullable=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
