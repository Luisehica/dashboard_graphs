import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import flask
from utils import Header

### Setup dash plotly
external_stylesheets = [dbc.themes.BOOTSTRAP]
#server = flask.Flask(__name__)


app = dash.Dash(__name__, 
    suppress_callback_exceptions=True,
    external_stylesheets=external_stylesheets,
    meta_tags=[{'name': 'viewport',
        'content': 'width=device-width'}] #, initial-scale=1.0'}]
    )
    
server = app.server
app.title = 'Beek Dashboard Data Challenge'

### Create Layout
def create_layout(app, page):
    layout = html.Div(
        [
            Header(app),
            dbc.Container(
                [
                    page.content(app)
                ]
            )
        ]
    )
    return layout