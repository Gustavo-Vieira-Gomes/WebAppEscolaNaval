from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from user_database import Database_Users

from app import *

card_style = {
    'width': '350px',
    'min-height': '300px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px'
}


# ========= Layout ========== #

def render_layout(message):
    message = 'ocorreu um erro durante o registro.' if message else message

    layout = dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Legend('Alterar senha'),
                    dbc.Input(id='numero_interno_register', placeholder='Número Interno', type='text', style={'margin-top': '5px', 'margin-bottom': '5px'}),
                    dbc.Input(id='pwd_padrao', placeholder='Senha atual', type='password', style={'margin-top': '5px', 'margin-bottom': '5px'}),
                    dbc.Input(id='pwd_usuario', placeholder='Nova senha', type='password', style={'margin-top': '5px', 'margin-bottom': '5px'}),
                    dbc.Button('Registrar', id='register-button'),
                    html.Span(message, style={'text-align': 'center'}),
                ], style={'text-align': 'center'})
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                    html.Label('Ou ', style={'margin-right': '5px'}),
                    dcc.Link('faça login', href='/login')
                    ], style={'padding': '20px', 'justify-content': 'center', 'display': 'flex'})
                ])
            ]),
    ])
    ], style=card_style, class_name='align-self-center')

    return layout



# ======= Callbacks =========
@app.callback(
    Output('register-state', 'data'),
    Input('register-button', 'n_clicks'),
    State('numero_interno_register', 'value'),
    State('pwd_padrao', 'value'),
    State('pwd_usuario', 'value')
)
def successful(n_clicks, num_int, old_pwd, new_pwd):
    if n_clicks == None:
        raise PreventUpdate
    
    if num_int is not None and old_pwd is not None and new_pwd is not None:
        try:
            Database_Users().registrar_user(num_int, old_pwd, new_pwd)
            return ''
        except:
            return 'error'
    else:
        return 'error'        
