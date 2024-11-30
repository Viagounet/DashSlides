
from copy import copy
from typing import Any, Optional
from dash_extensions import Keyboard
from dash.development.base_component import Component
from dash import html

class SlideObject:
    def __init__(self, width: float, height: float) -> None:
        self.width = 100
        self.height = 100

    @property
    def style(self):
        return {"width": f"{self.width}vw", "height": f"{self.height}vh"}


class Slide:
    def __init__(self) -> None:
        pass
        self._background: Optional[str] = None
        self.style_modifier: dict[str, str] = {}

    @property
    def _render(self) -> html.Div:
        return html.Div()

    def render(self, slide_number: int) -> html.Div:
        render_div: html.Div = self._render
        if not hasattr(render_div, "style"):
            render_div.style = {}

        render_div.style["height"] = "100%"
        render_div.style["width"] = "100%"

        wrapper = html.Div(
            [
                render_div,
                html.Div(
                    slide_number,
                    style={
                        "position": "absolute",
                        "top": "97vh",
                        "left": "3vh",
                        "font-size": "large",
                    },
                ),
            ],
            style={"padding": "0px", "width": "100%", "height": "100%"},
            id={"type": "wrapper", "slide_number": slide_number},
        )
        if self._background:
            wrapper.style["background"] = self._background

        return wrapper

    def set_background(self, background: str) -> None:
        self._background = background