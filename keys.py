from dash import Dash, html, Input, Output, State
from dash_extensions import Keyboard

app = Dash(__name__)

app.layout = html.Div([html.Div(id="output"), Keyboard(id="keyboard")])


@app.callback(
    Output("output", "children"),
    Input("keyboard", "n_keydowns"),
    State("keyboard", "keydown"),
)
def update_output(n_keydowns, keydown):
    if n_keydowns is None:
        return "Press a key"

    if keydown is None:
        return "No key information available"

    key = keydown["key"]
    if key == "ArrowLeft":
        return "Left arrow pressed"
    elif key == "ArrowRight":
        return "Right arrow pressed"
    else:
        return f"Key pressed: {key}"


if __name__ == "__main__":
    app.run_server(debug=True)
