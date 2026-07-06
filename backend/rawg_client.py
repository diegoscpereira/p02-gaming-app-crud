from backend.config import settings
import requests

RAWG_URL = 'https://api.rawg.io/api/games/'

def search_rawg_games(game_name: str) -> dict:
    """
    Function to connect with RAWG's API, returning a result on a python dict format.
    """
    try:
        rawg_response = requests.get(RAWG_URL, params={"key": settings.rawg_api_key, "search": game_name})
        rawg_response.raise_for_status()
        rawg_response_output = rawg_response.json()
        return rawg_response_output
    except requests.exceptions.RequestException:
        raise