from dash import html
from dash import Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash.exceptions import PreventUpdate
from flask_login import logout_user, current_user
from user_database import Database_Users
import pdb

from components.modais import modal_nova_od, modal_admin, modal_ver_asp
from app import app


url_theme1 = dbc.themes.LUX
url_theme2 = dbc.themes.DARKLY

# ======= Layout =======
layout_sidebar = dbc.Container([
    modal_nova_od.layout,
    modal_admin.layout,
    modal_ver_asp.layout,
    modal_admin.layout_new_user,
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1('ESCOLA', style={'color': 'white'})
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.H3('NAVAL', style={'color': 'white'}),
                html.Img(src=app.get_asset_url('logo_en.png'), width='80vw')
            ])
        ]),
    ], style={'padding-top': '50px', 'margin-bottom': '30px'}, className='text-center'),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    ThemeSwitchAIO(aio_id='theme', themes=[url_theme1, url_theme2])
                ], style={'padding-left': '15px'})
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Nav([
                        dbc.NavItem(dbc.NavLink([html.I(className='fa fa-plus-circle dbc'), '\tADICIONAR OD'], id='nova_od_button', active=True, style={'text-align': 'left', 'font-size':'13px'}, disabled=True)),
                        html.Br(),
                        dbc.NavItem(dbc.NavLink([html.I(className='fa fa-cogs dbc'), '\tREINICIAR ANO'], id='admin_button', active=True, style={'text-align': 'left', 'font-size': '13px'})),
                        html.Br(),
                        dbc.NavItem(dbc.NavLink([html.I(className='fa fa-window-close-o'), '\tLOGOUT'], id='logout_button', active=True, style={'text-align': 'left', 'font-size': '14px'})),
                        html.Br()
                    ], vertical=True, pills=True, fill=True, style={'margin-right': '0px', 'margin-left': '5px'} ),
                    html.Div(id='feedback_div', className='dbc')
                ])
            ]),
            #
        ])
    ])
], fluid=True, style={'height': '100vh', 'padding': '0px', 'position':'sticky', 'top': 0, 'background-color': '#232423', 'margin': '0px'})



x = ThemeSwitchAIO.ids.store('theme')

# ======== Callbacks ========
@app.callback(
    Output('data-url', 'pathname'),
    Input('logout_button', 'n_clicks')
)
def successfull(n_clicks):
    if n_clicks == None:
        raise PreventUpdate
    
    if current_user.is_authenticated:
        logout_user()
        return '/login'
    else:
        return '/login'
    
# Abrir Modais
@app.callback(
    Output('modal_nova_od', 'is_open'),
    Input('nova_od_button', 'n_clicks'),
    Input('voltar_adicionar_od_button', 'n_clicks'),
    Input('adicionar_od_button', 'n_clicks'),
    State('modal_nova_od', 'is_open')
)
def toggle_modal(n, n2, n3, is_open):
    if n or n2 or n3:
        return not is_open
    return is_open

@app.callback(
    Output('modal_admin', 'is_open', allow_duplicate=True),
    Input('admin_button', 'n_clicks'),
    Input('admin_voltar_button', 'n_clicks'),
    Input('atualizar_button', 'n_clicks'),
    State('modal_admin', 'is_open'),
    prevent_initial_call = True
)
def toggle_modal(n, n2, n3, is_open):
    if n or n2 or n3:
        return not is_open
    return is_open

@app.callback(
    Output('nova_od_button', 'disabled'),
    Input("base-url", "pathname"),
    State('num_interno', 'data')
)
def disabled_or_not(url, user):
    if Database_Users().editor_de_od(user):
        print('sim')
        return False
    else:
        return True
    
