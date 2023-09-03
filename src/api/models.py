from sqlalchemy import Column, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..database import Base
from sqlalchemy import MetaData

metadata = MetaData()


class Landmark(Base):
    __tablename__ = "landmarks"
    
    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    rating: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    reviews: Mapped = Column(JSON, nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False, unique=True)
    time: Mapped[str] = mapped_column(nullable=False)
    img: Mapped[str] = mapped_column(nullable=False, unique=True)
    

    
