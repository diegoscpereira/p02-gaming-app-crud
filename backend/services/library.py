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

def get_library_game(db: Session, game_id: int) -> s.ShowLibrary:
    """
    Function to GET a game record from the library (SELECT).
    """
    return db.query(m.Library).filter(m.Library.id == game_id).first()

def get_library_games(db: Session, skip: int = 0, limit: int = 10) -> list[s.ShowLibrary]:
    """
    Function to GET a sample of games from the library (SELECT). [First 10 games by default]
    """
    return db.query(m.Library).offset(skip).limit(limit).all()

def delete_library_game(db: Session, game_id: int) -> s.ShowLibrary | None:
    """
    Function to DELETE a game record from the library (DELETE).
    """
    db_game = get_library_game(db, game_id)
    if db_game is None:
        return None
    db.delete(db_game)
    db.commit()
    return db_game

def update_library_game(db: Session, game_id: int, games: s.EditGameLibrary) -> s.ShowLibrary | None:
    """
    Function to UPDATE a game record in the library (UPDATE).
    """
    db_game = get_library_game(db, game_id)
    if db_game is None:
        return None
    for field, value in games.model_dump(exclude_unset=True).items():
        setattr(db_game, field, value)
    db.commit()
    db.refresh(db_game)
    return db_game