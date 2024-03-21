<<<<<<< HEAD
import httpx

from src import elements as el
from src.style import title
from src.query import BuildTracklist, SpotifyPlaylistCreator
from src.header import add_head_html
from nicegui import context, ui


class MainPage:
    @classmethod
    async def create(cls):
        """Asynchronously create and display the MainPage content."""
        instance = cls()
        await instance._build()
        return instance

    async def _build(self) -> None:
        """Create the content of the main page."""
        ui.colors(primary="#1DB954")
        context.get_client().content.classes('p-0 gap-0')
        add_head_html()

        with el.Row():
            with el.Column():
                title('*Memo*Mixtape')
                
                input_phrase = ui.input(placeholder='Type a phrase').classes('w-1/2 mt-2').props('flat color=white outlined rounded')
                with el.Row():
                    self.generate_button = ui.button(text='Generate', on_click=lambda e: self._on_generate_click(e, input_phrase.value,minimize_track_count.value)).classes('flex mt-2').props('color=primary')
                    minimize_track_count = ui.checkbox("Minimize Track Count", value=False)
                    

    
    async def _on_generate_click(self, e, input_phrase, minimize_track_count) -> None:
        """Handle the generation button click event."""
        self.builder = BuildTracklist(input_phrase, minimize_track_count)

        self.spinner = el.Spinner()
        self.spinner.visible = True
        self.generate_button.disable()

        result = await self.builder.get_tracks_for_phrase()

        if result['is_success']:
            await self._display_positive_result(result)
            self.spinner.visible = False
            self.generate_button.enable()

        if not result['is_success']:
            await self._display_negative_result(result, input_phrase, minimize_track_count)
            self.spinner.visible = False
            self.generate_button.enable()


    async def _display_positive_result(self, result):
        with ui.dialog() as dialog, ui.card():
            with el.Body(height="fit", width="fit"):
                with el.Column():
                    with ui.card():
                        async with httpx.AsyncClient() as client:
                            playlist_creator = SpotifyPlaylistCreator(tracks=result['result_tracks'])
                            playlist_url = await playlist_creator.create_playlist()
                            oembed_endpoint = f"https://open.spotify.com/oembed?url={playlist_url}"
                            response = await client.get(oembed_endpoint)
                            oembed_html = response.json()['html']
                            ui.html(oembed_html)
                            ui.button('Close', on_click=dialog.close).classes('flex justify-center mt-2').props('color=primary')
        await dialog


    async def _display_negative_result(self, result, input_phrase: str, minimize_track_count: bool):
        with ui.dialog() as dialog, ui.card():
            with el.Body(height="fit", width="fit"):
                with el.Column():
                    with ui.card():
                        suggestions = self.builder._generate_suggestions(result['checked_tracks'], input_phrase, result['checked_tracks'])
                        if suggestions:
                            ui.label('Exact match not found. Please select from the suggested phrases:')
                            ui.select(options=suggestions, on_change=lambda e: on_suggestion_select(e, minimize_track_count))
                        else:
                            ui.label('No suggestions available. Please try a different phrase.')
                        ui.button('Close', on_click=lambda: dialog.close()).classes('flex justify-center mt-2').props('color=primary')
        await dialog
                
                        
        async def on_suggestion_select(e, minimize_track_count: bool):
                selected_suggestion = e.value  
                
                self.builder = BuildTracklist(selected_suggestion, minimize_track_count)
                new_result = await self.builder.get_tracks_for_phrase()
                if new_result['is_success']:
                    await self._display_positive_result(new_result)
                else:
                    ui.notify('Unable to create a playlist from the selected suggestion.', level='error')
=======
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





    
    

    









>>>>>>> 239bbce (first commit)
