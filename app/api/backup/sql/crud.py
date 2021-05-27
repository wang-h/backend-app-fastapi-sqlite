from sqlalchemy.orm import Session
from .models import User
# from .models import Item
from .models import Drug
from .models import Disease
from .models import Admin
from .schemas import DiseaseCreate
from .schemas import AdminCreate
from .schemas import ItemUpdate
from .schemas import ItemCreate
from .schemas import UserCreate
from .models import MedicalDepartment


# def get_user(db: Session, user_id: int):
#     return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_admin_by_email(db: Session, email: str):
    return db.query(Admin).filter(Admin.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(User).offset(skip).limit(limit).all()

# # 用户表操作


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(name=user.name,
                   email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_admin(db: Session, Admin: AdminCreate):
    fake_hashed_password = Admin.password + "notreallyhashed"
    db_Admin = Admin(email=Admin.email, hashed_password=fake_hashed_password)
    db.add(db_Admin)
    db.commit()
    db.refresh(db_Admin)
    return db_Admin
# def update_user(db: Session, user_id: int, update_user: User):
#     db_user = db.query(User).filter(User.id == user_id).first()
#     if db_user:
#         update_dict = update_user.dict(exclude_unset=True)
#         for k, v in update_dict.items():
#             setattr(db_user, k, v)
#         db.commit()
#         db.flush()
#         db.refresh(db_user)
#         return db_user


# def delete_user(db: Session, user_id: int):
#     db_user = db.query(User).filter(User.id == user_id).first()
#     if db_user:
#         db.delete(db_user)
#         db.commit()
#         db.flush()
#         return db_user

# 疾病表操作


def create_disease(db: Session, disease: DiseaseCreate):
    db_disease = Disease(disease)
    db.add(db_disease)
    db.commit()
    db.refresh(db_disease)
    return db_disease


def get_disease_by_given_medical_department(db: Session, name: str):
    db_disease = db.query(Disease).filter(Disease.category == name).all()
    return db_disease


def get_disease_by_given_name(db: Session, name: str):
    db_disease = db.query(Disease).filter(Disease.name == name).first()
    return db_disease
# 医学科表操作


def get_medical_departments(db: Session):
    return db.query(MedicalDepartment).all()


def relate_user_item(db: Session, user_id: int, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db_item.owner_id = user_id
        db.commit()
        db.flush()
        return db.query(User).filter(User.id == user_id).first()


def get_drugs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Drug).offset(skip).limit(limit).all()


def get_drugs_given_name(db: Session, name: str, skip: int = 0, limit: int = 100):
    return db.query(Drug).filter(Drug.name == name).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: ItemCreate, user_id: int):
#     db_item = Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item


# def relate_user_item(db: Session, user_id: int, item_id: int):
#     db_item = db.query(Item).filter(Item.id == item_id).first()
#     if db_item:
#         db_item.owner_id = user_id
#         db.commit()
#         db.flush()
#         return db.query(User).filter(User.id == user_id).first()


# def update_item(db: Session, item_id: int, update_item: ItemUpdate):
#     db_item = db.query(Item).filter(Item.id == item_id).first()
#     if db_item:
#         update_dict = update_item.dict(exclude_unset=True)
#         for k, v in update_dict.items():
#             setattr(db_item, k, v)
#         db.commit()
#         db.flush()
#         db.refresh(db_item)
#         return db_item


# def delete_item(db: Session, item_id: int):
#     db_item = db.query(Item).filter(Item.id == item_id).first()
#     if db_item:
#         db.delete(db_item)
#         db.commit()
#         db.flush()
#         return db_item


# DRUG 药品表
