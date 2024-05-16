from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc


layout = html.Div([
    # col 1 - left side game interface
    html.Div([
        # row a - battle screen
        html.Div([

            # win box
            html.Div([
                html.Div([
                    html.P(id='win-text', style={'justify': 'center'})
                ], id='win-text-box')
            ], style={'position': 'absolute', 'height': '50vh', 'width': '55vw'}),
            
            # opponent
            html.Div([
                
                    # stats box
                    html.Div([

                        html.H3('Pokemon Name', id='opponent-name',
                                style={'position': 'absolute', 'marginTop': '1vh', 'marginLeft': '1vw',
                                       'fontSize': '25px', 'fontFamily': 'impact',
                                       'WebkitTextStrokeWidth': '.5px', 'WebkitTextStrokeColor': '#e4e4e4'}),

                        # hp box
                        html.Div([
                            html.H4('HP', style={'margin': '1px 3px', 'fontSize': '2vh'}),
                            html.Div([
                                html.Div([], id='opp-hp-bar', style={'width': '100%', 'height': '100%',
                                                                     'backgroundColor': 'green',
                                                                     'position': 'absolute'})
                            ], style={'width': '80%', 'height': '60%', 'backgroundColor': 'white',
                                      'position': 'absolute', 'top': '20%', 'left': '18%',
                                      'border': '1px solid #919191', 'borderTop': '1px solid #E4E4E4',
                                      'borderLeft': '1px solid #E4E4E4'})

                        ], style={'width': '60%', 'height': '30%', 'marginTop': '5vh', 'marginLeft': '6.7vw',
                                  'backgroundColor': '#C2C2C2', 'position': 'relative',
                                  'border': '1.5px solid #919191', 'borderTop': '1px solid #E4E4E4',
                                  'borderLeft': '1px solid #E4E4E4'})

                    ], style={'width': '35%', 'height': '35%', 'backgroundColor': '#96c23c', 'float': 'left',
                              'left': '0%', 'top': '20%', 'position': 'absolute', 'borderRadius': '0 3px 3px 0'}),

                    html.Img(src='',
                             id='opponent-sprite', style={'height': '90%', 'position': 'absolute', 'right': '10%',
                                                          'top': '15%', 'float': 'left'})

            ], style={'height': '50%', 'position': 'relative'}),

            # player
            html.Div([
                    html.Img(src='',
                             id='player-sprite', style={'height': '90%', 'left': '10%', 'bottom': '10%',
                                                        'float': 'left', 'position': 'absolute'}),

                    # stats box
                    html.Div([
                        html.H3('Pokemon Name', id='player-name',
                                style={'position': 'absolute', 'marginTop': '1vh', 'marginLeft': '1vw',
                                       'fontSize': '25px', 'fontFamily': 'impact',
                                       'WebkitTextStrokeWidth': '.5px', 'WebkitTextStrokeColor': '#e4e4e4'}),

                        # hp box
                        html.Div([
                            html.H4('HP', style={'margin': '1px 3px', 'fontSize': '2vh'}),
                            html.Div([
                                html.Div([], id='player-hp-bar', style={'width': '100%', 'height': '100%',
                                                                    'backgroundColor': 'green',
                                                                    'borderRadius': '3px'})
                            ], style={'width': '80%', 'height': '60%', 'backgroundColor': 'white',
                                      'position': 'absolute', 'top': '20%', 'left': '18%',
                                      'border': '1px solid #919191', 'borderTop': '1px solid #E4E4E4',
                                      'borderLeft': '1px solid #E4E4E4', 'borderRadius': '3px'})

                        ], style={'width': '60%', 'height': '30%', 'marginTop': '5vh', 'marginLeft': '6.7vw',
                                  'backgroundColor': '#C2C2C2', 'position': 'relative',
                                  'border': '1.5px solid #919191', 'borderTop': '1px solid #E4E4E4',
                                  'borderLeft': '1px solid #E4E4E4', 'borderRadius': '3px'})

                    ], style={'width': '35%', 'height': '35%', 'backgroundColor': '#96c23c', 'float': 'left',
                              'right': '0%', 'top': '30%', 'position': 'absolute', 'borderRadius': '3px 0 0 3px'})
            ], style={'height': '50%', 'position': 'relative'})
        ], style={'height': '50vh', 'backgroundColor': 'olivedrab', 'border': '2px solid green',
                  'borderTop': '2px solid yellowgreen', 'borderLeft': '2px solid yellowgreen', 'margin': '10px'}),

        html.Div([
            html.P("What will your pokemon do?", id="move-header",
                   style={'height': '2.5vh', 'margin': '2%', 'fontSize': '20px'}),

            # row b - move select
            html.Div([

                # move buttons
                html.Div([
                    html.Button('move 1', id='move-1', n_clicks=0, n_clicks_timestamp=0, title='',
                                style={'width': '95%', 'height': '13vh', 'marginLeft': '3.5%', 'marginTop': '0',
                                       'backgroundColor': 'pink', 'cursor': 'pointer'}),
                    html.Button('move 2', id='move-2', n_clicks=0, n_clicks_timestamp=0, title='',
                                style={'width': '95%', 'height': '13vh', 'marginLeft': '3.5%', 'marginTop': '2.5%',
                                       'backgroundColor': 'yellowgreen', 'cursor': 'pointer'})
                ], style={'width': '50%', 'float': 'left', 'margin': '0 auto'}),
                html.Div([
                    html.Button('move 3', id='move-3', n_clicks=0, n_clicks_timestamp=0, title='',
                                style={'width': '95%', 'height': '13vh', 'marginLeft': '1.5%', 'marginTop': '0',
                                       'backgroundColor': 'goldenrod', 'cursor': 'pointer'}),
                    html.Button('move 4', id='move-4', n_clicks=0, n_clicks_timestamp=0, title='',
                                style={'width': '95%', 'height': '13vh', 'marginLeft': '1.5%', 'marginTop': '2.5%',
                                       'backgroundColor': 'lightblue', 'cursor': 'pointer'})
                ], style={'width': '50%', 'float': 'left'})
            ], style={'height': '30vh', 'justifyContent': 'center'})
        ], style={'backgroundColor': '#EEEEEE', 'border': '2px solid #E4E4E4', 'borderLeft': '2px solid #C2C2C2',
                  'borderTop': '2px solid #C2C2C2', 'margin': '10px'})
    ], style={'width': '55vw', 'height': '98vh', 'float': 'left'}),

    # col 2 - right side descriptions
    html.Div([

        # game history
        html.Div([


        ], id='game-log', style={'overflow': 'scroll', 'width': '95%', 'height': '30%',
                                 'backgroundColor': '#FCFCFC', 'margin': '2.5%', 'padding': '20px'}),

        # row a - pokemon describe
        html.Div([
            html.H1('Pokemon Description',
                    style={'textIndent': '15px', 'fontWeight': 'bold'})
        ]),

        html.Div([
            html.Div([
                html.H3('POKEMON', id='player-describe',
                       style={'fontWeight': 'bold'}),
                html.P('Types', id='player-types', style={'fontWeight': 'bold', 'fontSize': '16px',
                                                          'fontStyle': 'italic'}),
            ], style={'width': '95%', 'height': '20%', 'position': 'relative', 'margin': '5%'}),

            html.Div([
                html.P('hP:', id='player-hp', style={'fontWeight': 'bold', 'marginTop': '5%'}),
                html.P('Status Condition:', id='player-status', style={'fontWeight': 'bold', 'marginTop': '5%'}),
                html.P('Speed:', id='player-speed', style={'fontWeight': 'bold', 'marginTop': '5%'}),
                html.P('Attack:', id='player-attack', style={'fontWeight': 'bold', 'marginTop': '5%'}),
                html.P('Defense:', id='player-defense', style={'fontWeight': 'bold', 'marginTop': '5%'}),
                html.P('Special Attack:', id='player-spattack', style={'fontWeight': 'bold', 'marginTop': '5%'}),
                html.P('Special Defense:', id='player-spdefense', style={'fontWeight': 'bold', 'marginTop': '5%'})

            ], style={'width': '95%', 'height': '30%', 'textAlign': 'left', 'position': 'relative',
                      'margin': '2.5% 5%', 'color': '#414141'})

        ], style={'height': '55%', 'width': '45%', 'backgroundColor': '#FCFCFC',
                  'margin': '2.5%', 'position': 'relative', 'float': 'left'}),

        html.Div([
            html.Div([
               html.H3('POKEMON', id='opp-describe',
                        style={'fontWeight': 'bold'}),
                html.P('Types', id='opp-types', style={'fontWeight': 'bold', 'fontSize': '16px',
                                                       'fontStyle': 'italic'}),
            ], style={'width': '95%', 'height': '20%', 'position': 'relative', 'margin': '5%'}),

            html.Div([
                html.P('hP:', id='opp-hp', style={'fontWeight': 'bold', 'marginTop': '5%'}),
                html.P('Status Condition:', id='opp-status', style={'fontWeight': 'bold', 'marginTop': '5%'}),
                html.P('Speed:', id='opp-speed', style={'fontWeight': 'bold', 'marginTop': '5%'}),
                html.P('Attack:', id='opp-attack', style={'fontWeight': 'bold', 'marginTop': '5%'}),
                html.P('Defense:', id='opp-defense', style={'fontWeight': 'bold', 'marginTop': '5%'}),
                html.P('Special Attack:', id='opp-spattack', style={'fontWeight': 'bold', 'marginTop': '5%'}),
                html.P('Special Defense:', id='opp-spdefense', style={'fontWeight': 'bold', 'marginTop': '5%'})
            ], style={'width': '95%', 'height': '30%', 'textAlign': 'left', 'position': 'relative',
                      'margin': '2.5% 5%', 'color': '#414141'})

        ], style={'height': '55%', 'width': '45%', 'backgroundColor': '#FCFCFC', 'margin': '2.5%',
                  'position': 'relative', 'float': 'left'}),

    ], style={'width': '40vw', 'height': '88vh', 'float': 'left', 'backgroundColor': '#EEEEEE',
              'margin': '10px', 'border': '2px solid #E4E4E4', 'borderLeft': '2px solid #C2C2C2',
              'borderTop': '2px solid #C2C2C2'})
], style={'backgroundColor': '#FCFCFC', 'color': '#313131'})
