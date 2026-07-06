from backend.rawg_client import search_rawg_games
from backend.schemas import RawgBase

def explore_games(query: str) -> list[RawgBase]:
    """
    Function used to orchestrate RAWG's API call and to run data quality checks, displaying the response as structured text.
    """
    raw_response = search_rawg_games(query)
    results = raw_response["results"]
    games = [RawgBase.model_validate(game) for game in results]
    return games