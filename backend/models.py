from backend.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

class Library(Base):
    __tablename__ = "library"
    id: Mapped[int] = mapped_column(primary_key=True)
    rawg_id: Mapped[int]
    slug: Mapped[str]
    name: Mapped[str]
    game_description: Mapped[str]
    released: Mapped[date]
    background_image: Mapped[str] | None
    metacritic: Mapped[int] | None
    rating: Mapped[float] | None
    ratings_count: Mapped[int] | None
    updated: Mapped[date]
    platforms: Mapped[str]
    genres: Mapped[str]
    developers: Mapped[str]
    status: Mapped[str] | None
    my_rating: Mapped[int] | None
    comment: Mapped[str] | None
    added_at: Mapped[date] = mapped_column(default=date.today)
