from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import date, datetime


class RawgBase(BaseModel):
    rawg_id: int = Field(alias="id")
    slug: str
    name: str
    released: date | None
    background_image: str | None
    metacritic: int | None
    rating: float
    ratings_count: int
    updated: datetime
    platforms: str | None
    genres: str | None

    @field_validator("platforms", mode="before")
    @classmethod
    def flatten_platforms(cls, value):
        if not value:
            return None
        return ", ".join(p["platform"]["name"] for p in value)

    @field_validator("genres", mode="before")
    @classmethod
    def flatten_genres(cls, value):
        if not value:
            return None
        return ", ".join(g["name"] for g in value)


class SaveGameLibrary(BaseModel):
    rawg_id: int = Field(alias="id")
    slug: str
    name: str
    released: date | None
    background_image: str | None
    metacritic: int | None
    rating: float
    ratings_count: int
    updated: datetime
    platforms: str | None
    genres: str | None
    status: str | None = None
    user_rating: int | None = Field(ge=0, le=10, default=None)
    comment: str | None = None


class EditGameLibrary(BaseModel):
    status: str | None = None
    user_rating: int | None = Field(ge=0, le=10, default=None)
    comment: str | None = None


class ShowLibrary(SaveGameLibrary):
    id: int
    date_added: date
    model_config = ConfigDict(from_attributes=True)
