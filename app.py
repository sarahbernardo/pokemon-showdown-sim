# Actual app

from dash import html, Dash
import dash_bootstrap_components as dbc

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP, "https://fonts.cdnfonts.com/css/pokemon-solid?styles=24573"],
           meta_tags=[{"name": "viewport", "content": "width=device-width"}], suppress_callback_exceptions=True)

