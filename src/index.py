# Import dash 
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

# Import plotly
import plotly.graph_objects as go

# Import dependencies for callbacks
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table

# Connect to main app.py file, apps pages and backend
from app import app, create_layout
from apps import main, help, backend
from apps.visual_backend import DashPlotting

from datetime import timedelta

### Instance objects
Plots = DashPlotting()



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

@app.callback(
    [
        Output('users_subscribed','children'),
        Output('users_subscribed_perc','children'),
        Output('growth_subscribed','children'),
        Output('growth_perc_subscribed','children'),
        Output('end_time_subscribed_plot_1','children'),
        Output('end_time_subscribed_plot_2','children'),
        Output('start_time_subscribed_plot_3','children'),
        Output('end_time_subscribed_plot_4','children'),
        Output('start_time_subscribed_plot_5','children')
    ],
    [
        Input('users_subscribed_plot','relayoutData'),
        Input('users_subscribed_plot','figure'),
    ], prevent_initial_call=True
)
def get_data_from_selectors_users_subscribed(relayout, figure):

    if list(relayout.keys())[0]=='xaxis.range':
        start_date = relayout['xaxis.range'][0].split(" ")[0]
        end_date = relayout['xaxis.range'][1].split(" ")[0]
    elif list(relayout.keys())[0]=='xaxis.range[0]':
        start_date = relayout['xaxis.range[0]'].split(" ")[0]
        end_date = relayout['xaxis.range[1]'].split(" ")[0]
    else:
        start_date = figure['data'][0]['x'][0]
        end_date = figure['data'][0]['x'][-1]

    # Filter dataframes between dates 
    between_mask_subscribed = (backend.df_users_subscribed['date'] > start_date) & (backend.df_users_subscribed['date'] < end_date)
    between_mask_users =  (backend.df_users['date'] > start_date) & (backend.df_users['date'] < end_date)

    df_users_subscribed = backend.df_users_subscribed[between_mask_subscribed]
    df_users = backend.df_users[between_mask_users]

    # Calcule KPI's
    min_users_subscribed = df_users_subscribed['cumm_users'].min()
    max_users_subscribed = df_users_subscribed['cumm_users'].max()

    users_subscribed = '{:,.0f}'.format(max_users_subscribed) 

    users = df_users['cumm_users'].max()
    perc_users_subscribed = '% {:.1f}'.format(max_users_subscribed/users * 100) 
    
    new_users_subscribed = max_users_subscribed - min_users_subscribed
    new_users_subscribed_format = '+ {:,.0f}'.format(max_users_subscribed - min_users_subscribed)

    perc_new_users = new_users_subscribed/min_users_subscribed * 100

    growth_new_users = '% {:,.0f}'.format(perc_new_users)

    end_time_subscribed_plot_1 = end_date.split('T')[0]
    end_time_subscribed_plot_2 = end_date.split('T')[0]
    start_time_subscribed_plot_3 = start_date.split('T')[0]
    end_time_subscribed_plot_4 = end_date.split('T')[0]
    start_time_subscribed_plot_5 = start_date.split('T')[0]

    return  users_subscribed, perc_users_subscribed, new_users_subscribed_format, growth_new_users, end_time_subscribed_plot_1, end_time_subscribed_plot_2, start_time_subscribed_plot_3, end_time_subscribed_plot_4, start_time_subscribed_plot_5
    
@app.callback(
    [
        Output('users_active','children'),
        Output('users_active_perc','children'),
        Output('growth_active','children'),
        Output('growth_perc_active','children'),
        Output('end_time_active_plot_1','children'),
    ],
    [
        Input('users_active_plot','relayoutData'),
        Input('users_active_plot','figure'),
    ], prevent_initial_call=True
)
def get_data_from_selectors_users_active(relayout, figure):
    #print(relayout)
    if list(relayout.keys())[0]=='xaxis.range':
        start_date = relayout['xaxis.range'][0].split(" ")[0]
        end_date = relayout['xaxis.range'][1].split(" ")[0]
    elif list(relayout.keys())[0]=='xaxis.range[0]':
        start_date = relayout['xaxis.range[0]'].split(" ")[0]
        end_date = relayout['xaxis.range[1]'].split(" ")[0]
    else:
        start_date = figure['data'][0]['x'][0]
        end_date = figure['data'][0]['x'][-1]
    #print(start_date)
    # Filter dataframes between dates 
    between_mask_active = (backend.df_active_users['current_date_'] >= start_date) & (backend.df_active_users['current_date_'] <= end_date)

    #print(between_mask_active)
    df_active_users = backend.df_active_users[between_mask_active]

    # re calcule start and end week dates 
    start_date_week = df_active_users['current_date_'].min()
    end_date_week = df_active_users['current_date_'].max()   

    # Calcule KPI's
    print(type(end_date_week))
    df_active_users_now = df_active_users[(df_active_users['current_date_']==end_date_week)][['active_users', 'total_users']]
    df_active_users_previous_week = df_active_users[(df_active_users['current_date_']==(end_date_week-timedelta(days=7)))][['active_users', 'total_users']]

    active_users_now = df_active_users_now['active_users'].values[0]
    perc_active_users_now = df_active_users_now['active_users'].values[0]/df_active_users_now['total_users'].values[0]*100

    active_users_previous_week = df_active_users_previous_week['active_users'].values[0]
    diff_active_users = active_users_now - active_users_previous_week

    increase_active_users = diff_active_users/active_users_previous_week*100

    # Format
    users_active = '{:,.0f}'.format(active_users_now) 

    perc_users_active = '% {:.1f}'.format(perc_active_users_now) 
    
    new_users_active_format = '{:,.0f}'.format(diff_active_users)

    growth_new_users = '% {:,.1f}'.format(increase_active_users)

    end_time_active_plot_1 = end_date.split('T')[0]
    end_time_active_plot_2 = end_date.split('T')[0]
    start_time_active_plot_3 = start_date.split('T')[0]
    end_time_active_plot_4 = end_date.split('T')[0]
    start_time_active_plot_5 = start_date.split('T')[0]

    print(end_time_active_plot_1,
        end_time_active_plot_2,
        start_time_active_plot_3,
        end_time_active_plot_4,
        start_time_active_plot_5)

    return  users_active, perc_users_active, new_users_active_format, growth_new_users, end_time_active_plot_1



if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080)
