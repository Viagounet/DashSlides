from copy import copy


from dash_slides.presentation import Presentation, PresentationApp
from dash_slides.slides import MarkdownSlide, TitleSlide, OutroductionSlide, LongParagraphSlide, MarkdownSlide, SplitSlide, AutoFillSlide, ListSlide, ImageSlide, CustomDashSlide
from dash import html
import dash_bootstrap_components as dbc

coding = MarkdownSlide(
    markdown_text="""```python
# This allows you to use Orange's private Azure instances.
# You'll need to export AZURE_ENDPOINT as an environnement variable.
from doc_llm.engines.azure import AzureEngine

engine = AzureEngine(
    "dai-semafor-nlp-gpt-35-turbo-model-fr", save_folder="./my_log_folder"
)
answer = engine.query(
    "What is the meaning of life?",
    max_tokens=256,
    temperature=0,
    tags=["for_tutorial"],
    api_version="2023-05-15",
    json_output=False,
    as_cache=False,
)
print(answer.content)
```
""",
    footer="Appel à GPT-3.5 sur l'instance Azure de SemaforNLP",
)
presentation = Presentation()
presentation.add_slide(
    TitleSlide(
        title="DocLLM",
        subtitle="Bibliothèque Python pour l'utilisation de LLMs & l'analyse des documents",
        authors=["Ismaël Rousseau"],
    )
)
presentation.add_slide(
    TitleSlide(
        title="DocLLM",
        subtitle="Bibliothèque Python pour l'utilisation de LLMs & l'analyse des documents",
        authors=["Ismaël Rousseau"],
    )
)

presentation.add_slide(
    SplitSlide(
        SplitSlide(
            TitleSlide(title="Pourquoi DocLLM ?"),
            coding,
            mode="row",
            has_separator=True,
        ),
        CustomDashSlide(
            html.Div(
                [
                    dbc.Textarea(placeholder="Write your text here", style={"height": "5vw"}),
                    dbc.Button("Submit"),
                ],
                className="d-flex flex-row gap-1",
            )
        ),
        mode="column",
    )
)

app = PresentationApp(presentation)
app.start()
