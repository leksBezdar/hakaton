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
    address: Mapped[str] = mapped_column(nullable=False)
    time: Mapped[str] = mapped_column(nullable=False)
    img: Mapped[str] = mapped_column(nullable=False)
    coordinates: Mapped[int] = mapped_column(nullable=False)
    categories: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    

class Review(Base):
    __tablename__ = "reviews"

    stars: Mapped[float] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    description: Mapped[str] = mapped_column(nullable=False)
    

class PublishedLandmark(Base):
    __tablename__ = "published_landmarks"

    id = mapped_column(primary_key=True, index=True)
    user_id = mapped_column(ForeignKey("users.id"))
    landmark_id = mapped_column(ForeignKey("landmarks.id"))

    user = relationship("User", back_populates="published_landmarks")

class FavoriteLandmark(Base):
    __tablename__ = "favorite_landmarks"

    id = mapped_column(primary_key=True, index=True)
    user_id = mapped_column(ForeignKey("users.id"))
    landmark_id = mapped_column(ForeignKey("landmarks.id"))

    user = relationship("User", back_populates="favorite_landmarks")

