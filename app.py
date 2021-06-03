
import os
from random import randint

import dash
import dash_cytoscape as cyto
import dash_html_components as html

import flask


server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '400px'},
        elements=[
            {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 75, 'y': 75}},
            {'data': {'id': 'two', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
            {'data': {'source': 'one', 'target': 'two'}}
        ]
    )
])

if __name__ == '__main__':
    app.run_server()
