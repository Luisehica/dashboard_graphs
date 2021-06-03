import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from apps.visual_backend import DashPlotting
from datetime import date
from apps.backend import df_users_subscribed, df_active_users

# initialice visual backend
Plot = DashPlotting()

def content(app):
    layout = dbc.Container(
        [   
            html.Br(),
            
            #
            big_box_kpi(app, 'Users Subscribed',
                'users_subscribed_plot', 
                Plot.time_series(df_users_subscribed, x_data='date', y_data='cumm_users',
                    selector_slider=True),
                [
                    'users_subscribed',
                    'users_subscribed_perc',
                    'growth_subscribed',
                    'growth_perc_subscribed'
                ],
                [
                    'Users Subscribed until ',
                    'of our users are subscribed until ',
                    ' from ',
                    " 'till ",
                    ' of Growth since ',
                ], 
                [
                    'end_time_subscribed_plot_1',
                    'end_time_subscribed_plot_2',
                    'start_time_subscribed_plot_3',
                    'end_time_subscribed_plot_4',
                    'start_time_subscribed_plot_5',

                ]
            ),
            html.Br(),
            big_box_kpi(app, 'Active Users',
                'users_active_plot',
                Plot.time_series(df_active_users, x_data='current_date_',
                y_data='active_users', title='Active Users', 
                selector_slider=True),
                [
                    'users_active',
                    'users_active_perc',
                    'growth_active',
                    'growth_perc_active'
                ],
                [
                    'Users Active ',
                    'of our users are weekly active ',
                    'last week',
                    '',
                    'last week',
                ], 
                [
                    'end_time_active_plot_1',
                    'end_time_active_plot_2',
                    'start_time_active_plot_3',
                    'end_time_active_plot_4',
                    'start_time_active_plot_5',
                ]
            )
        ]
    )
    return layout


def big_box_kpi(app, title, plot_id, plot, values_id, text_list, time_window_id_list):
    """Creates the big box for each KPI.

    Args:
        app (dash.Dash): Dash object
        plot_id (str): plot id
        values_id (list): list of 4 ids.
        text_list (list):  list of two strings.
        time_window_id_list (list): list of 3 ids

    Returns:
        dbc.Row: Big box
    """
    card = dbc.Row(
        [
            dbc.Col( #Left Column
                plot_core(app, plot_id, plot),
                className="box_plot",
                sm=12,
                lg=7
            ),
            dbc.Col( #right Column
                 right_card(app, title, values_id, text_list, time_window_id_list),
                 align='center',
                 className="rigth_card"
            )
        ]
    )
    return card

def right_card(app, title,values_id_list, text_list, time_window_id_list):
    """ Creates the right card.

    Args:
        app (dash.Dash): Dash object
        values_id_list (list): list of 4 ids.
        text_list (list):  list of two strings.
        time_window_id_list (list): list of 2 ids

    Returns:
        html.Div: Card
    """
    card = html.Div(
        [
            html.H1(title, className='title_card'),
            box_2_lines(app, values_id_list[0], text_list[0], time_window_id_list[0]),
            box_2_lines(app, values_id_list[1], text_list[1], time_window_id_list[1]),
            html.Div(id="h-line"),
            box_1_line(app, values_id_list[2], text_list[2], time_window_id_list[2], text_list[3], time_window_id_list[3]),
            box_1_line(app, values_id_list[3], text_list[4], time_window_id_list[4])
        ]
    )
    return card
   
def box_2_lines(app, value_id, text, time_window_id):
    """ Creates a box with two rows

    Args:
        app (dash.Dash): Dash object
        values_id (list): id for the value.
        text (list):  text for two row.
        time_window_id (list): id of the time window

    Returns:
        html.Div: Box
    """
    box = html.Div(
            [
            html.Span('__value__', id=value_id, className='KPI_Value'),
            html.P(
                [
                    html.Span(text, className='KPI_Text'),
                    html.Span("", id=time_window_id, className='KPI_Text')
                ]
            )
        ]
        , className='box-2-lines'
    )
    return box

def box_1_line(app, left_id, text, center_id, text2=None, right_id='right_id_box_1_line'):
    """ Create 1 line Box.

    Args:
        app (dash.Dash): Dash Object
        left_id (str): id of the value in the left
        right_id (str): id of the value in the left

    Returns:
        html.Div: Box
    """
    box=html.Div(
        [
            html.Span("+ 200", id=left_id, className='KPI_Value_2'),
            html.P(
                [
                    text,
                    html.Span(id=center_id, className='KPI_Text_2'),
                    text2,
                    html.Span(id=right_id, className='KPI_Text_2'),
                ]
            ),
            

        ],
        className='box-1-line'
    )
    return box

def plot_core(app, plot_id, fig_plot):
    """Empty plot just with text

    Args:
        app (dash.Dash): Dash Object
        plot_id (str): id of the plot

    Returns:
        html.Div: plot
    """
    plot = dcc.Graph(
        id=plot_id,
        figure = fig_plot
    )
    return plot


def cohort(app):
    #https://medium.com/analytics-vidhya/cohort-analysis-95a794b4e58c

    pass