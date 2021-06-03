import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

"""
In this script, it is the main objects and components in POO
"""

def Header(app):
    return html.Div(
        [
            get_header_navbar(app)
        ]
    )

def get_header_navbar(app):
    beek_logo = html.Img(
        src=app.get_asset_url("Beek_logo.png")
        , style={'width': '100px'}
    )

    navbar = dbc.Navbar(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(beek_logo),
                            dbc.Col(dbc.NavbarBrand("Dashboard - Data Challenge", className="title_header")),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    href="/main",
                ),
                dbc.NavbarToggler(id="navbar-toggler"),
                dbc.Collapse(head_menu(app),
                    id ="navbar-collapse", navbar=True
                )
                      
            ],
        )
    return navbar
    
def head_menu(app):
    nav_list = [
        dbc.Col(dbc.NavLink('Help', href='/help',
            className='link-control'),
            lg={'size':1,'offset': 6},
            md={'size':1, 'offset': 6}
        ),
        dbc.Col(dbc.NavLink('GitHub', href='https://github.com/Luisehica/Beak_Data_Challenge',
            className='link-control'),
            lg={'size':2},
            md={'size':2}
        ),
        dbc.Col(dbc.NavLink('Notion', href='https://www.notion.so/luisehica/Beak-Data-Challenge-ed5404842b214f9395c3c0894ccb0e3f',
            className='link-control'),
            lg={'size':1},
            md={'size':1}
        ),
    ]
    return nav_list

