import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def content(app):
    layout = dbc.Container(
        [
            html.Br(),
            html.H1("Hello World!")
        ]
    )
    return layout