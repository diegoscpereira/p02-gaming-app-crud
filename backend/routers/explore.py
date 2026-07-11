from fastapi import APIRouter, HTTPException
from backend.services.explore import explore_games
from backend.schemas import RawgBase

router = APIRouter(prefix="/explore")

@router.get("/", response_model=list[RawgBase])
def search_rawg_games(query: str):
    """
    Function to call the explore_games back-end function after receiving a request from the front-end.
    """
    return explore_games(query)