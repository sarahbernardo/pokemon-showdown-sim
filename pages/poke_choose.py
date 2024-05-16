from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import base64
from pokemon import Pokemon
from driver import pokemons


layout = html.Div([
		html.Div([
			html.Div([
				html.H1("Welcome to Pokemon Showdown", style={'margin': '30px 35px', 'fontFamily': 'Pokemon Solid',
															  'color': '#f5a7a2', 'WebkitTextStrokeWidth': '2px',
															  'WebkitTextStrokeColor': '#f06f67'})
			], style={'width': '90vw', 'height': '8vh', 'margin': '25px 35px'}),
			html.Div([
				html.Div([
					html.Div([
						html.Img(src='https://art.pixilart.com/189628eed95a95b.png',
								 style={'width': '35vw', 'height': '35vh', 'opacity': '0.6',
										'borderRadius': '20px 20px 0 0'}),
						html.Img(src='', id='select-img',
								 style={'position': 'absolute', 'left': '3vw', 'top': '5vh', 'height': '25vh'})
					], style={'width': '35vw', 'height': '35vh', 'position': 'absolute',
							  'left': '2.5vw', 'top': '5vh', 'border': '2px solid #def7ff',
							  'borderRadius': '20px 20px 0 0', 'overflow': 'hidden'}),
					html.Div([
						html.Div([
							html.P('Types:', id='poke-types', style={'fontWeight': 'bold', 'marginLeft': '15%'}),
							html.P('hP:', id='poke-hp', style={'fontWeight': 'bold', 'marginLeft': '15%'}),
							html.P('Speed:', id='poke-speed', style={'fontWeight': 'bold', 'marginLeft': '15%'})
						], style={'float': 'left', 'width': '50%', 'marginTop': '2%'}),

						html.Div([
							html.P('Attack:', id='poke-attack', style={'fontWeight': 'bold', 'marginLeft': '15%'}),
							html.P('Defense:', id='poke-defense', style={'fontWeight': 'bold', 'marginLeft': '15%'}),
							html.P('Special Attack:', id='poke-spattack',
								   style={'fontWeight': 'bold', 'marginLeft': '15%'}),
							html.P('Special Defense:', id='poke-spdefense',
								   style={'fontWeight': 'bold', 'marginLeft': '15%'})
						], style={'float': 'left', 'marginTop': '2%', 'width': '40%'})

					], id='select-page-stats', style={'width': '35vw', 'height': '25vh', 'position': 'absolute',
							  						  'left': '2.5vw', 'top': '41vh', 'backgroundColor': '#fcfcfc',
							  						  'border': '2px solid #def7ff', 'borderRadius': '0 0 20px 20px'})

				], style={'width': '40vw', 'height': '73vh', 'backgroundColor': '#f0fbff',
						  'border': '2px solid #def7ff', 'position': 'relative', 'left': '3vw',
						  'top': '0vh', 'borderRadius': '20px'}),
				html.Div([
					html.H4('Choose Your Pokemon', style={'margin': '25px'})
				], style={'width': '25vw', 'height': '8vh', 'backgroundColor': '#f0fbff',
						  'position': 'absolute', 'left': '45vw', 'top': '22vh',
						  'borderRadius': '20px 20px 0 0', 'border': '2px solid #def7ff', 'borderBottom': 'none'}),
				html.Div([
					dcc.RadioItems(id='pokemon-options',
								   options=[{'label': [html.Img(src=pokemon.picture, style={'height': '70px'}),
													   html.Span(name)],
											 'value': name} for name, pokemon in pokemons.items()],
								   style={'margin': '20px'}, inputStyle={'margin': '15px'})
				], id='pokemon-select', style={'width': '25vw', 'height': '65vh', 'backgroundColor': '#f0fbff',
											   'position': 'absolute', 'left': '45vw', 'overflow': 'scroll',
											   'top': '30vh', 'borderRadius': '0 0 20px 20px',
											   'border': '2px solid #def7ff', 'borderTop': 'none'}),

				html.Div([
					html.H4('Choose Your Moves', style={'marginTop': '25px', 'marginLeft': '25px', 'float': 'left'}),
					html.P('(up to four)', style={'fontStyle': 'italic', 'marginTop': '28px',
												  'marginLeft': '5px', 'float': 'left'}),
					html.Div([
						dbc.Checklist(options=[], id='move-options', style={'margin': '15px', 'marginLeft': '30px'})
					], id='move-select', style={'width': '25vw', 'height': '60vh', 'overflow': 'scroll'})
				], style={'width': '25vw', 'height': '73vh', 'backgroundColor': '#f0fbff',
						  'position': 'absolute', 'left': '72vw', 'top': '22vh', 'borderRadius': '20px',
						  'border': '2px solid #def7ff'}),

			])
		])
	])
