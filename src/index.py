# Import dash 
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

# Import plotly
import plotly.graph_objects as go

# Import dependencies for callbacks
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


# Connect to main app.py file, apps pages and backend
from app import app, create_layout
from apps import main


from datetime import timedelta



# Describe the layout/UI of the app
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content")
    ]
)



### Callback for page salection
@app.callback(Output(component_id='page-content', component_property='children'),
    Input(component_id='url', component_property='pathname'))
def display_page(pathname):
    if pathname == '/help':
        return create_layout(app, help)
    else:
        return create_layout(app, main)




if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True ,port=8080)
