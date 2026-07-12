from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import backend.services.library as l
import backend.schemas as sc
from backend.database import get_db

router = APIRouter(prefix="/library")

@router.post("/", response_model=sc.ShowLibrary, status_code=201)
def post_library_games(game: sc.SaveGameLibrary, db: Session = Depends(get_db)):
    """
    API route to CREATE a new game record in the user's library (POST).
    """
    return l.create_library_games(db=db, game=game)

@router.get("/", response_model=list[sc.ShowLibrary])
def get_library_games(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    API route to SELECT a games sample from the user's library (GET) - 10 first records by default.
    """
    return l.select_library_games(db=db, skip=skip, limit=limit)

@router.get("/{game_id}", response_model=sc.ShowLibrary)
def get_library_game(game_id: int, db: Session = Depends(get_db)):
    """
    API route to SELECT a specific game record from the user's library (GET).
    """
    db_games = l.select_library_game(db=db, game_id=game_id)
    if db_games is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_games

@router.delete("/{game_id}", response_model=sc.ShowLibrary, status_code=200)
def delete_library_game(game_id: int, db: Session = Depends(get_db)):
    """
    API route to DELETE a specific game record from the user's library (DELETE).
    """
    db_games = l.delete_game(db=db, game_id=game_id)
    if db_games is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_games

@router.put("/{game_id}", response_model=sc.ShowLibrary)
def update_library_game(game_id: int, games: sc.EditGameLibrary, db: Session = Depends(get_db)):
    """
    API route to UPDATE a specific game record from the user's library (PUT).
    """
    db_games = l.edit_library_game(db=db, game_id=game_id, games=games)
    if db_games is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_games