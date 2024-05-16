from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

# Define the navbar structure
def Navbar():
    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Create Your Own", href="/create", id="create-button")),
                dbc.NavItem(dbc.NavLink("New Game", href="/", id="new-game-button")),
                dbc.NavItem(dbc.NavLink("Start Game", href="/battle", id="start-game-button", disabled=True)),
            ],
            brand="Pokemon Showdown",
            brand_href="/",
            color="#e4e4e4",
            light=True,
            brand_style={'color': '#414141'},
            style={'fontFamily': 'impact'}
        ),
    ])

    return layout
