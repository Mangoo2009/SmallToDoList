import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

engine = create_engine(
    os.getenv('DB_URL'),
    echo=True
)

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class ToDoList(Base):
    __tablename__ = 'ToDoList'
    id: Mapped[int] = mapped_column(primary_key=True)
    Zametka: Mapped[str]
    Status: Mapped[bool]

Base.metadata.create_all(engine)