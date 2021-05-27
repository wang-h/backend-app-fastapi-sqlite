from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically

    # 强制将表名小写
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
