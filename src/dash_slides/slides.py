from copy import copy
from typing import Optional
from dash_slides.slide import Slide
from dash import html, dcc
from dash_slides.utils import MAIN_TITLE_SIZE, MAIN_TITLE_WEIGHT, SUB_TITLE_SZE, center, border
from dash.development.base_component import Component
import dash_bootstrap_components as dbc

def set_style_if_none(render: html.Div):
    if not hasattr(render, "style"):
        render.style = {}
    return render

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
                "text-align": "center",
            },
        )
        subtitle_div = html.Div(
            self.subtitle,
            style={
                "font-size": SUB_TITLE_SZE,
                "display": "solid" if self.subtitle else "none",
                "text-align": "center",
            },
        )

        authors_div = html.Div()
        if self.authors:
            authors_div = html.Div(
                ", ".join(self.authors),
                style={
                    "font-size": "1rem",
                    "font-weight": "400",
                    "text-align": "center",
                },
            )
        return html.Div(
            children=[title_div, subtitle_div, authors_div],
            className=f"d-flex flex-column gap-1 {center}",
        )
    
class OutroductionSlide(Slide):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text
        self.set_background(
            "linear-gradient(0deg, rgba(255,255,255,1) 0%, rgba(255,160,0,1) 100%)"
        )

    @property
    def _render(self) -> html.Div:
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
    def _render(self) -> html.Div:
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
    def _render(self) -> html.Div:
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


class SplitSlide(Slide):
    def __init__(
        self,
        first_slide: Slide,
        second_slide: Slide,
        mode: str = "row",
        has_separator: bool = False,
    ) -> None:
        super().__init__()
        self.first_slide = first_slide
        self.second_slide = second_slide
        self.has_separator = has_separator
        if mode not in ["row", "column"]:
            raise ValueError(
                "SplitSlide `mode` parameter must be either 'row' or 'column'"
            )
        self.mode = mode

    @property
    def _render(self) -> html.Div:
        first_slide_render = set_style_if_none(self.first_slide._render)
        second_slide_render = set_style_if_none(self.second_slide._render)

        filler_div = html.Div(style={"display": "none"})
        style = {"width": "auto", "height": "100%"}
        if self.mode == "column":
            style = {"width": "100%", "height": "auto"}
            if self.has_separator:
                filler_div = html.Hr(style={"width": "100%"})
        else:
            first_slide_render.style["width"] = "100%"
            second_slide_render.style["width"] = "100%"
        return html.Div(
            [first_slide_render, filler_div, second_slide_render],
            className=f"d-flex flex-{self.mode} justify-content-start gap-2",
            style=style,
        )


class AutoFillSlide(Slide):
    def __init__(self, slides: list[Slide]) -> None:
        super().__init__()
        self.slides = slides
        self.copied_renders: list[html.Div] = []
        for slide in self.slides:
            copied_slide = copy(slide)
            copied_render = copied_slide._render
            if not hasattr(copied_render, "style"):
                copied_render.style = {}

            percent_size = (2 * 100 / len(self.slides)) - 5
            copied_render.style["flex"] = f"1 1 {percent_size}%"
            self.copied_renders.append(copied_render)

    @property
    def _render(self) -> html.Div:
        return html.Div(
            [render for render in self.copied_renders],
            className=f"d-flex flex-wrap gap-2 {center}",
        )


class ListSlide(Slide):
    def __init__(self, items: list[str]) -> None:
        super().__init__()
        self.items = items

    @property
    def _render(self) -> html.Div:
        return html.Div(
            dbc.ListGroup(
                [dbc.ListGroupItem(item) for item in self.items],
                numbered=True,
            ),
            className=f"d-flex {center} fs-2",
        )


class ImageSlide(Slide):
    def __init__(self, img_path: str, border_thickness: float = 0) -> None:
        super().__init__()
        self.img_path = img_path
        self.border_thickness = border_thickness

    @property
    def _render(self) -> html.Div:
        return html.Div(
            html.Img(
                src=self.img_path,
                style={
                    "width": "100%",  # Make the image width 100% of its container
                    "height": "100%",  # Make the image height 100% of its container
                    "border": f"solid black {self.border_thickness}rem",
                    "object-fit": "contain",  # Ensures the image scales to fit its container without overflow
                },
            ),
            style={
                "width": "100%",
                "height": "100%",
                "overflow": "hidden",  # Prevents the image from overflowing the parent div
            },
            className=f"p-2 d-flex {center}",
        )


class CustomDashSlide(Slide):
    def __init__(self, dash_component: Component) -> None:
        super().__init__()
        self.dash_component = dash_component

    @property
    def _render(self) -> html.Div:
        return self.dash_component