import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np
import json
import plotly.graph_objects as go
import pandas as pd

from dash import dcc, html, callback
from dash.dependencies import Input, Output

from typing import TypedDict

# current_working_directory = os.getcwd()
# module_path = os.path.abspath(current_working_directory)
# sys.path.append(module_path)

# from training_scripts.vae_torch import VAE

latent_dim = 8

with open(
    "data/decoded_results_from_env_truth.json",
    "r",
    encoding="utf-8",
) as f:
    data = json.load(f)

df = pd.DataFrame(data)
# Extracting ls_mean values for the scatter plot
ls_mean_values = df["ls_mean"].apply(pd.Series)
ls_mean_values.columns = ["ls_mean_x", "ls_mean_y"]

scatter_trace = go.Scatter(
    x=ls_mean_values["ls_mean_x"],
    y=ls_mean_values["ls_mean_y"],
    mode="markers",
    name="From truth",
)

fig = go.Figure(data=[scatter_trace])
# Set axes properties
fig.update_xaxes(range=[-3, 3])
fig.update_yaxes(range=[-3, 3])


fig.add_shape(
    type="circle",
    xref="x",
    yref="y",
    fillcolor="white",
    x0=-0.1,
    y0=-0.1,
    x1=0.1,
    y1=0.1,
    line_color="black",
)

# # Set figure size
fig.update_layout(width=900, height=900)
graph = dcc.Graph(
    id="basic-interactions",
    className="six columns",
    figure=fig,
    config={
        "editable": True,
        "edits": {
            "shapePosition": True,
            "axisTitleText": False,
            "legendText": False,
            "annotationText": False,
        },
    },
)
# # Load the trained VAE model
# MODEL = "models/sim1_ls2.pth"
# latent_dim = int(MODEL.replace("models/sim1_ls", "").split(".")[0])
# vae = VAE(latent_dim)
# vae.load_state_dict(torch.load(MODEL))
# vae.eval()


# # Function to generate an image from a latent vector
# def generate_image(latent_vector):
#     with torch.no_grad():
#         generated_image = vae.decoder(latent_vector)
#         return generated_image


def slider(i: int) -> dcc.Slider:
    return dcc.Slider(
        id=f"slider-{i}",
        min=-3,
        max=3,
        step=0.1,
        value=0,
        marks={i: str(i) for i in range(-3, 4)},
    )


sliders = html.Div(
    [html.Div([html.Label(f"Latent Dimension {i}"), slider(i), html.Br()]) for i in range(latent_dim)],
    className="d-flex flex-column gap-1" if latent_dim > 2 else "d-none",
    style={"width": "30vw"},
)

final_layout = html.Div(
    [
        html.H1("VAE Color Image Generator"),
        html.Div(
            [
                sliders,
                graph,
                html.Div(id="output-image"),
            ],
            className="d-flex flex-row justify-content-center align-items-center",
            style={"height": "80vh"},
        ),
    ]
)


@callback(
    Output("output-image", "children"),
    [Input(f"slider-{i}", "value") for i in range(latent_dim)],
)
def update_image(*latent_values):
    generated_image = np.arange(15**2).reshape((15, 15))
    fig = px.imshow(generated_image)
    fig.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
    )

    return dcc.Graph(
        figure=fig,
        style={"width": "100%", "height": "100%"},
    )
