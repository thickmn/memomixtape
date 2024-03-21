import os
from pathlib import Path

from starlette.middleware.sessions import SessionMiddleware
<<<<<<< HEAD
from nicegui import app, ui

from src.main_page import MainPage
from src import user

from dotenv import load_dotenv
load_dotenv()

app.add_middleware(SessionMiddleware, secret_key=os.environ.get('NICEGUI_SECRET_KEY', ''))
=======
from fastapi.responses import HTMLResponse
from fastapi import FastAPI

from nicegui import app, ui
from src import main_page
from src import user
from dotenv import load_dotenv

load_dotenv()

fastapi_app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=os.environ.get('NICEGUI_SECRET_KEY', ''))

>>>>>>> 239bbce (first commit)
app.add_static_files('/fonts', str(Path(__file__).parent / 'src' / 'fonts'))
app.add_static_files('/static', str(Path(__file__).parent / 'src' / 'static'))


@user.login_page
def login():
    user.login_form().on('success', lambda: ui.navigate.to('/'))

<<<<<<< HEAD
@user.page('/')
async def home():
    await MainPage.create()

@user.page('/results')
async def results():
    pass


ui.run(dark=True, storage_secret=os.getenv('NICEGUI_SECRET_KEY'))
=======

@user.page('/')
async def home():
    await main_page.create()


ui.run(reload=False, dark=True, storage_secret=os.getenv('NICEGUI_SECRET_KEY'))
>>>>>>> 239bbce (first commit)
