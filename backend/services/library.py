from sqlalchemy.orm import Session
import backend.models as m
import backend.schemas as s

def create_library_games(db: Session, game: s.SaveGameLibrary) -> s.ShowLibrary:
    """
    Function to CREATE a new game record in the user's library (INSERT).
    """
    db_game = m.Library(**game.model_dump())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game