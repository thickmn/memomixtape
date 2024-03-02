from src.style import title
from src.header import add_head_html
from src.query import BuildTracklist, SpotifyPlaylistCreator

from nicegui import context, ui


async def create() -> None:
    """Create the content of the main page."""
    ui.colors(primary="#1DB954")
    context.get_client().content.classes('p-0 gap-0')
    add_head_html()

    with ui.row() \
        .classes('w-full h-screen flex justify-center items-center no-wrap into-section'):

        with ui.column():
            title('*Memo*Mixtape')

            with ui.row():
                user_input = ui.input(placeholder='Type a phrase') \
                    .classes('w-full mt-2').props('flat color=white outlined')
                minimize_track_count = ui.checkbox("Minimize Track Count", value=False)

            ui.button('Generate', on_click=lambda e: on_generate_click(e, user_input.value, minimize_track_count.value)) \
                .classes('flex justify-center mt-2').props('color=primary')
            

async def on_generate_click(e, input_phrase: str, minimize: bool):
    """Handle the generation button click event."""
    builder = BuildTracklist(phrase=input_phrase, minimize_track_count=minimize)
    spinner = ui.spinner(size="sm")
    spinner.visible = True
    result = await builder.get_tracks_for_phrase()

    if result['is_success']:
        ui.notification('Playlist successfully created!')
        spinner.visible = False
        with ui.dialog() as dialog, ui.card():
            with ui.column().classes('flex justify-center items-center no-wrap into-section'):
                # Create a Spotify playlist with the generated tracklist
                playlist_creator = SpotifyPlaylistCreator(tracks=result['result_tracks'])
                playlist_url = await playlist_creator.create_playlist()
                oembed_endpoint = f"https://open.spotify.com/oembed?url={playlist_url}"
                response = requests.get(oembed_endpoint)
                oembed_html = response.json()['html']
                ui.html(oembed_html)
                ui.button('Close', on_click=dialog.close).classes('flex justify-center mt-2').props('color=primary')
    else:
        spinner.visible = False
        ui.notification('Failed to create Spotify playlist.')

    await dialog
    
