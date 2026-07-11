from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import backend.services.library as l
import backend.schemas as sc
from backend.database import get_db

router = APIRouter(prefix="/library")

@router.post("/", response_model=sc.ShowLibrary, status_code=201)
def post_library_games(game: sc.SaveGameLibrary, db: Session = Depends(get_db)):
    return l.create_library_games(db, game)