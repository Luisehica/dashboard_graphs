import plotly.express as px
import plotly.graph_objects as go
from itertools import cycle
import pandas as pd

class DashPlotting:
    
    
    ptp_palette = ['#36D7DC', '#FAF3DD', '#AED9E0']
    template    = "plotly_white"
    
    def __init__(self):
            self.range_selector_slider = dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )

    @staticmethod
    def empty_fig(text):
        figure = {
            "layout": {
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": text,
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28
                        }   
                    }
                ]
            }
        }
        return figure

    def time_series(self, data, x_data=None, y_data=None, title=None, selector_slider=False):
        """ Creates a time series plot

        Args:
            data (pandas.dataframe): [description]
            x_data ('str', optional): [description]. Defaults to None.
            title ('str', optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        figure = px.line(data,
                         x=x_data,
                         y=y_data,
                         template = DashPlotting.template,
                         title=title)
        
        if selector_slider==True:   
            figure.update_layout({
            'xaxis': self.range_selector_slider
            })

        return figure

    

