import os
from pathlib import Path

from starlette.middleware.sessions import SessionMiddleware
from nicegui import app, ui

from src.main_page import MainPage
from src import user

from dotenv import load_dotenv
load_dotenv()

app.add_middleware(SessionMiddleware, secret_key=os.environ.get('NICEGUI_SECRET_KEY', ''))
app.add_static_files('/fonts', str(Path(__file__).parent / 'src' / 'fonts'))
app.add_static_files('/static', str(Path(__file__).parent / 'src' / 'static'))


@user.login_page
def login():
    user.login_form().on('success', lambda: ui.navigate.to('/'))

@user.page('/')
async def home():
    await MainPage.create()

@user.page('/results')
async def results():
    pass


ui.run(dark=True, storage_secret=os.getenv('NICEGUI_SECRET_KEY'))
