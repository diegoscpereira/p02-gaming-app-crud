from backend.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, datetime


class Library(Base):
    __tablename__ = "library"
    id: Mapped[int] = mapped_column(primary_key=True)
    rawg_id: Mapped[int]
    slug: Mapped[str]
    name: Mapped[str]
    released: Mapped[date | None]
    background_image: Mapped[str | None]
    metacritic: Mapped[int | None]
    rating: Mapped[float]
    ratings_count: Mapped[int]
    updated: Mapped[datetime]
    platforms: Mapped[str | None]
    genres: Mapped[str | None]
    status: Mapped[str | None]
    user_rating: Mapped[int | None]
    comment: Mapped[str | None]
    date_added: Mapped[date] = mapped_column(default=date.today)
