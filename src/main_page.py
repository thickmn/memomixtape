from src.style import title
from src.query import BuildTracklist, SpotifyPlaylistCreator

from nicegui import context, ui


async def create() -> None:
    """Create the content of the main page."""
    ui.colors(primary="#1DB954")
    context.get_client().content.classes('p-0 gap-0')

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

            with ui.column() \
                .classes('flex justify-center items-center no-wrap into-section'):

                title('Your*Playlist*')

                # Create a Spotify playlist with the generated tracklist
                playlist_creator = SpotifyPlaylistCreator(tracks=result['result_tracks'])
                playlist_url = await playlist_creator.create_playlist()

                ui.link(f"{playlist_url}", target=playlist_url, new_tab=True)

                ui.button('Close', on_click=dialog.close) \
                        .classes('flex justify-center mt-2').props('color=primary')


    else:
        spinner.visible = False
        ui.notification('Failed to create Spotify playlist.')

    await dialog
    
            

# async def on_generate_click(e, input_phrase: str, minimize: bool):
#     """Handle the generation button click event."""

#     spinner = ui.spinner(size="sm")
#     builder = BuildTracklist(phrase=input_phrase, minimize_track_count=minimize)

    
#     with ui.dialog(value=True).props("persistent maximized") as dialog, ui.card().classes("bg-transparent"):
#         spinner.visible = True
        
#         # Generate the tracklist
#         result = await builder.get_tracks_for_phrase()
        
#     if result['is_success']:
#         spinner.visible = False
#         dialog.close()
#         # Here, you might want to update the UI with the generated tracklist
#         print(f"Successfully created a playlist of {len(result['result_tracks'])} tracks.")
#         for track in result['result_tracks']:
#             print(f"{track['name']} by {track['artists']}")
#     else:
#         spinner.visible = False
#         dialog.close()
#         print("Failed to generate playlist.")





    
    

    









