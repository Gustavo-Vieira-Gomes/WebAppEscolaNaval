from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from app import *
from dash.exceptions import PreventUpdate
from flask_login import login_user
from user_database import Database_Users
import pdb


card_style = {
    'width': '300px',
    'min-height': '300px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
}


# ======== Layout =========
def render_layout(message):
    message = "Ocorreu algum erro durante o login." if message == "error" else message
    layout = dbc.Card([
                html.Legend("Login", className='dbc'),
                dbc.Input(id="user_login", placeholder="Número Interno", type="text", class_name='dbc', style={'margin-top': '5px', 'margin-bottom': '5px'}),
                dbc.Input(id="pwd_login", placeholder="Senha", type="password", class_name='dbc', style={'margin-top': '5px', 'margin-bottom': '5px'}),
                dbc.Button("Login", id="login_button", class_name='dbc', style={'margin-bottom': '5px', 'margin-top': '5px'}),
                html.Span(message, style={"text-align": "center"}),
                
                html.Div([
                    html.Label("Ou", style={"margin-right": "5px"}),
                    dcc.Link("Registre-se", href="/register"),
                ], style={"padding": "20px", "justify-content": "center", "display": "flex"})

            ], style=card_style, className="align-self-center") 
    return layout


# ========= Callbacks =========
@app.callback(
    Output('login-state', 'data'),
    Input('login_button', 'n_clicks'),
    State('user_login', 'value'),
    State('pwd_login', 'value')
)
def successful(n_clicks, num_int, pwd):
    if n_clicks == None:
        raise PreventUpdate
    
    if num_int and pwd is not None:
        try:
            Database_Users().verificar_senha_de_login(num_int, pwd)
            return 'success'
        except Exception as E:
            print('verificar...',E)
            return 'error'
    else:
        return 'error'