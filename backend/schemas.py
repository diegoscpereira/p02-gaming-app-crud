from pydantic import BaseModel, ConfigDict
from datetime import date


class RawgBase(BaseModel):
    rawg_id: int
    slug: str
    name: str
    released: date
    background_image: str | None
    metacritic: int | None
    rating: float | None
    ratings_count: int | None
    updated: date
    platforms: str | None
    genres: str | None

class SaveGameLibrary(RawgBase):
    status: str | None = None
    user_rating: int | None = None
    comment: str | None = None

class EditGameLibrary(BaseModel):
    status: str | None = None
    user_rating: int | None = None
    comment: str | None = None

class ShowLibrary(SaveGameLibrary):
    id: int
    date_added: date
    model_config = ConfigDict(from_attributes=True)
