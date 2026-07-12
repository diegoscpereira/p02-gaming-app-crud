"""
NiceGUI frontend for the Game Library app.

Talks to the FastAPI backend over HTTP (httpx) — never touches the
database directly. Two pages:
  /         -> Explore: search RAWG, save a game to your library
  /library  -> Library: view/edit/delete your saved games
"""

import httpx
from nicegui import ui

API_URL = "http://localhost:8000"


# ---------------------------------------------------------------------------
# Explore page — search RAWG, save results to the library
# ---------------------------------------------------------------------------

@ui.page("/")
def explore_page():
    ui.label("Explore Games").classes("text-2xl font-bold")

    with ui.row().classes("w-full items-center"):
        search_input = ui.input(label="Search for a game").classes("w-80")
        search_button = ui.button("Search")

    results_container = ui.column().classes("w-full gap-2")

    async def do_search():
        query = search_input.value
        if not query:
            ui.notify("Type something to search for.", type="warning")
            return

        results_container.clear()
        search_button.props("loading")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/explore/", params={"query": query})
                response.raise_for_status()
                games = response.json()
        except httpx.HTTPError:
            ui.notify("Could not reach the backend. Is it running?", type="negative")
            return
        finally:
            search_button.props(remove="loading")

        if not games:
            with results_container:
                ui.label("No games found.")
            return

        with results_container:
            for game in games:
                render_game_card(game)

    def render_game_card(game: dict):
        with ui.card().classes("w-full"):
            with ui.row().classes("w-full items-center justify-between"):
                with ui.row().classes("items-center gap-4"):
                    if game.get("background_image"):
                        ui.image(game["background_image"]).classes("w-24 h-16 object-cover rounded")
                    with ui.column().classes("gap-0"):
                        ui.label(game["name"]).classes("text-lg font-semibold")
                        ui.label(f"Released: {game.get('released') or 'Unknown'}")
                        ui.label(f"Rating: {game.get('rating')} · Metacritic: {game.get('metacritic') or 'N/A'}")
                        ui.label(f"Genres: {game.get('genres') or '—'}")
                ui.button("Save to Library", on_click=lambda g=game: save_game(g))

    async def save_game(game: dict):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"{API_URL}/library/", json=game)
                response.raise_for_status()
                ui.notify(f'"{game["name"]}" saved to your library.', type="positive")
            except httpx.HTTPError:
                ui.notify("Could not save this game.", type="negative")

    search_button.on_click(do_search)
    search_input.on("keydown.enter", do_search)

    ui.link("Go to My Library", "/library").classes("mt-4")


# ---------------------------------------------------------------------------
# Library page — view, edit, delete saved games
# ---------------------------------------------------------------------------

@ui.page("/library")
def library_page():
    ui.label("My Library").classes("text-2xl font-bold")
    ui.link("Back to Explore", "/").classes("mb-4")

    library_container = ui.column().classes("w-full gap-2")

    async def load_library():
        library_container.clear()
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{API_URL}/library/", params={"limit": 100})
                response.raise_for_status()
                games = response.json()
            except httpx.HTTPError:
                ui.notify("Could not reach the backend.", type="negative")
                return

        if not games:
            with library_container:
                ui.label("Your library is empty. Go explore and save a game!")
            return

        with library_container:
            for game in games:
                render_library_row(game)

    def render_library_row(game: dict):
        with ui.card().classes("w-full"):
            with ui.row().classes("w-full items-center justify-between"):
                with ui.row().classes("items-center gap-4"):
                    if game.get("background_image"):
                        ui.image(game["background_image"]).classes("w-20 h-14 object-cover rounded")
                    with ui.column().classes("gap-0"):
                        ui.label(game["name"]).classes("text-lg font-semibold")
                        ui.label(f"Status: {game.get('status') or 'Not set'}")
                        ui.label(f"My rating: {game.get('user_rating') if game.get('user_rating') is not None else '—'} / 10")
                        ui.label(f"Added: {game.get('date_added')}")

                with ui.row().classes("gap-2"):
                    ui.button("Edit", on_click=lambda g=game: open_edit_dialog(g))
                    ui.button("Delete", color="red", on_click=lambda g=game: delete_game(g))

    def open_edit_dialog(game: dict):
        with ui.dialog() as dialog, ui.card():
            ui.label(f'Editing "{game["name"]}"').classes("text-lg font-semibold")
            status_input = ui.select(
                ["want to play", "playing", "beaten", "dropped"],
                label="Status",
                value=game.get("status"),
            ).classes("w-64")
            rating_input = ui.number(label="My rating (0-10)", min=0, max=10, value=game.get("user_rating")).classes("w-64")
            comment_input = ui.textarea(label="Comment", value=game.get("comment") or "").classes("w-64")

            async def save_edit():
                payload = {
                    "status": status_input.value,
                    "user_rating": rating_input.value,
                    "comment": comment_input.value or None,
                }
                async with httpx.AsyncClient() as client:
                    try:
                        response = await client.put(f"{API_URL}/library/{game['id']}", json=payload)
                        response.raise_for_status()
                        ui.notify("Updated.", type="positive")
                    except httpx.HTTPError:
                        ui.notify("Could not update this game.", type="negative")
                        return
                dialog.close()
                await load_library()

            with ui.row().classes("mt-2 justify-end w-full"):
                ui.button("Cancel", on_click=dialog.close)
                ui.button("Save", on_click=save_edit)

        dialog.open()

    async def delete_game(game: dict):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(f"{API_URL}/library/{game['id']}")
                response.raise_for_status()
                ui.notify(f'"{game["name"]}" removed from your library.', type="positive")
            except httpx.HTTPError:
                ui.notify("Could not delete this game.", type="negative")
                return
        await load_library()

    ui.timer(0, load_library, once=True)


ui.run(title="Game Library", port=8080)