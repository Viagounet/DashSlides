from typing import Any
from dash import html

import dash
import dash_bootstrap_components as dbc

from dash import html, Input, Output, State
from dash_extensions import Keyboard
from networkx import center

from dash_slides.utils import SCREEN_PADDING

class Presentation:
    def __init__(self) -> None:
        self.slides: list = []
        self.active_slide = 0

    def add_slide(self, slide: Any):
        self.slides.append(slide)

    def previous(self):
        self.active_slide -= 1

    def next(self):
        self.active_slide += 1

    def render(self) -> html.Div:
        div_elements: list[html.Div] = []
        for i, slide in enumerate(self.slides):
            slide_div_render = slide.render(slide_number=i)
            slide_div_render.style["display"] = "block"
            if i is not self.active_slide % len(self.slides):
                slide_div_render.style["display"] = "none"

            slide_div_render.id = str(i)
            div_elements.append(slide_div_render)

        return html.Div(
            children=div_elements,
            className="d-flex flex-row",
            style={"width": "100%", "height": "100%"},
        )


class PresentationApp:
    def __init__(self, presentation: Presentation):
        self.presentation = presentation
        self.app = dash.Dash(external_stylesheets=[dbc.themes.COSMO])

        # Define the layout
        self.app.layout = html.Div(
            children=[
                html.Div(
                    children=[self.presentation.render()],
                    style={"width": "100%", "height": "100%"},
                    className=f"d-flex {center}",
                    id="active",
                ),
                Keyboard(id="keyboard"),
            ],
            style={
                "width": "100vw",
                "height": "100vh",
                "padding": f"{SCREEN_PADDING}%",
                "border": "solid #ff7900 0.5rem",
            },
            className=f"d-flex {center}",
            id="background-div",
        )

        # Add the callback
        self.add_callbacks()

    def add_callbacks(self):
        @self.app.callback(
            Output("active", "children"),
            Input("keyboard", "n_keydowns"),
            State("keyboard", "keydown"),
            prevent_initial_call=True,
        )
        def update_output(n_keydowns, keydown):
            key = keydown["key"]
            if key == "ArrowLeft":
                self.presentation.previous()
            elif key == "ArrowRight":
                self.presentation.next()
            return self.presentation.render()

    def start(self, debug: bool = True):
        self.app.run_server(debug=debug)
