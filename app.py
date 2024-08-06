import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from typing import Any, Optional
from dash_extensions import Keyboard


app = dash.Dash(external_stylesheets=["assets/preset1/style.css", dbc.themes.COSMO])

ACTIVE_SIZE_PADDING = "10%"
MAIN_TITLE_SIZE = "5rem"
MAIN_TITLE_WEIGHT = "500"

SUB_TITLE_SZE = "3rem"
SCREEN_PADDING = 2

center = "justify-content-center align-items-center"
border = "border border-solid"


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

    def _render(self):
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
        )
        if self._background:
            wrapper.style["background"] = self._background

        return wrapper

    def set_background(self, background: str) -> None:
        self._background = background


class TitleSlide(Slide):
    def __init__(
        self,
        title: str,
        subtitle: Optional[str] = None,
        authors: Optional[list[str]] = None,
    ) -> None:
        super().__init__()
        self.title = title
        self.subtitle = subtitle
        self.authors = authors

    @property
    def _render(self) -> html.Div:
        title_div = html.Div(
            self.title,
            style={
                "font-size": MAIN_TITLE_SIZE,
                "font-weight": MAIN_TITLE_WEIGHT,
                "display": "solid" if self.title else "none",
            },
        )
        subtitle_div = html.Div(
            self.subtitle,
            style={
                "font-size": SUB_TITLE_SZE,
                "display": "solid" if self.subtitle else "none",
            },
        )

        authors_div = html.Div()
        if self.authors:
            authors_div = html.Div(
                ", ".join(self.authors),
                style={"font-size": "1rem", "font-weight": "400"},
            )
        return html.Div(
            children=[title_div, subtitle_div, authors_div],
            className=f"d-flex flex-column gap-1 {center}",
        )


class GoodbyeSlide(Slide):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text
        self.set_background(
            "linear-gradient(0deg, rgba(255,255,255,1) 0%, rgba(255,160,0,1) 100%)"
        )

    @property
    def _render(self):
        return html.Div(
            self.text,
            style={
                "font-size": MAIN_TITLE_SIZE,
                "color": "white",
            },
            className="d-flex {center}",
        )


class LongParagraphSlide(Slide):
    def __init__(self, text: str, paragraph_title: Optional[str] = None) -> None:
        super().__init__()
        self.text = text
        self.paragraph_title = paragraph_title

    @property
    def _render(self):
        paragraph_divs = []
        for paragraph in self.text.split("\n"):
            paragraph_divs.append(html.Div(paragraph))

        title_div = html.Div()
        if self.paragraph_title:
            title_div = html.Div(self.paragraph_title, className="fs-4")
        full_paragraph = html.Div(
            paragraph_divs,
            style={"width": "80%", "height": "80%", "overflow-y": "scroll"},
            className=f"d-flex flex-column gap-1 p-3 {border} border-3 rounded",
        )
        return html.Div(
            children=[title_div, full_paragraph],
            className=f"d-flex flex-column gap-2 {center}",
        )


class MarkdownSlide(Slide):
    def __init__(self, markdown_text: str, footer: Optional[str] = None) -> None:
        super().__init__()
        self.markdown_text = markdown_text
        self.footer = footer

    @property
    def _render(self):
        footer_div = html.Div()
        if self.footer:
            footer_div = html.Div(
                self.footer,
                style={"max-width": "100%", "font-weight": "300"},
                className=f"d-flex {center}",
            )
        return html.Div(
            [
                dcc.Markdown(
                    self.markdown_text,
                    style={
                        "max-width": "80%",
                        "max-height": "80%",
                        "overflow-y": "scroll",
                    },
                    className=f"d-flex {center} {border} border-2 border-black",
                ),
                footer_div,
            ],
            className=f"d-flex flex-column gap-2 {center} p-1",
        )


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


title_slide = TitleSlide(
    title="Projet de fin d'études :",
    subtitle="Simplification d'énoncé dans l'optique de produire un résumé de conversation",
    authors=["Ismaël Rousseau"],
)
title_slide_2 = TitleSlide(
    title="Projet de fin d'études 2 :",
    subtitle="Simplification d'énoncé dans l'optique de produire un résumé de conversation",
)

text = (
    "This is quite the long text that will be repeated\nAnd it has multiple paragraphs too!!\n\n"
    * 100
)
paragraph = LongParagraphSlide(text=text, paragraph_title="Louis XIV")
goodbye = GoodbyeSlide(text="Thanks!")
coding = MarkdownSlide(
    markdown_text="""```python
def factorial(n):
    \"""
    This function returns the factorial of a given number using recursion.
    
    :param n: Integer, the number to calculate the factorial of
    :return: Integer, the factorial of the number
    \"""
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

# Example usage:
number = 5
print(f"The factorial of {number} is {factorial(number)}")
```
""",
    footer="Le code python d'une fonction factorielle",
)
presentation = Presentation()
presentation.add_slide(title_slide)
presentation.add_slide(title_slide_2)
presentation.add_slide(paragraph)
presentation.add_slide(coding)
presentation.add_slide(goodbye)

app.layout = html.Div(
    children=[
        html.Div(
            children=[presentation.render()],
            style={"width": "100%", "height": "100%"},
            className=f"d-flex {center}",
            id="active",
        ),
        Keyboard(id="keyboard"),
    ],
    style={"width": "100vw", "height": "100vh", "padding": f"{SCREEN_PADDING}%"},
    className=f"d-flex {center} {border} border-3 border-orange",
    id="background-div",
)


@app.callback(
    Output("active", "children"),
    Input("keyboard", "n_keydowns"),
    State("keyboard", "keydown"),
    State("active", "children"),
    prevent_initial_call=True,
)
def update_output(n_keydowns, keydown, current_active_slide):
    key = keydown["key"]
    if key == "ArrowLeft":
        presentation.previous()
    elif key == "ArrowRight":
        presentation.next()
    else:
        pass
    return presentation.render()


if __name__ == "__main__":
    app.run_server(debug=False)
