from pathlib import Path
from typing import Optional

from nicegui import app, ui


HEADER_HTML = (Path(__file__).parent / 'static' / 'header.html').read_text()
STYLE_CSS = (Path(__file__).parent / 'static' / 'style.css').read_text()


def add_head_html() -> None:
    """Add the code from header.html and reference style.css."""
    ui.add_head_html(HEADER_HTML + f'<style>{STYLE_CSS}</style>')


def add_header(menu: Optional[ui.left_drawer] = None) -> None:
    """Create the page header."""
    menu_items = {
        'Installation': '/#installation',
        'Features': '/#features',
        'Demos': '/#demos',
        'Documentation': '/documentation',
        'Examples': '/#examples',
        'Why?': '/#why',
    }
   
    with ui.header() \
            .classes('items-center duration-200 p-0 px-4 no-wrap') \
            .style('box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)'):
        if menu:
            ui.button(on_click=menu.toggle, icon='menu').props('flat color=black round').classes('lg:hidden')
        # with ui.link(target='/').classes('row gap-4 items-center no-wrap mr-auto'):
            # svg.face().classes('w-8 stroke-white stroke-2 max-[610px]:hidden')
            # svg.word().classes('w-24')

        with ui.row().classes('max-[1050px]:hidden'):
            for title_, target in menu_items.items():
                ui.link(title_, target).classes(replace='text-lg text-black')


        with ui.row().classes('min-[1051px]:hidden'):
            with ui.button(icon='more_vert').props('flat color=black round'):
                with ui.menu().classes('bg-primary text-black text-lg'):
                    for title_, target in menu_items.items():
                        ui.menu_item(title_, on_click=lambda target=target: ui.navigate.to(target))