# Imports
from dash import html, dcc, Input, Output, State
import pandas as pd
from flask_login import current_user

# import from folders
from app import *
from user_database import Users
from components import home
from components.login import login, register

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


# Ajustar conteúdo para stores

app._favicon = 'favico.ico'
app.title = 'SODEN 1.1'

# ========== Layout ============
app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            dcc.Location(id="base-url", refresh=False), 
            dcc.Store(id="login-state", data=""),
            dcc.Store(id="register-state", data=""),
            dcc.Store(id='searched_asp_store', data=''),
            dcc.Store(id='num_interno', data=''),

            html.Div(id='page-content', style={'height': '100vh', 'display': 'flex', 'justify-content': 'center', 'margin': '0px', 'padding-left': '0px', 'padding-right': '0px'})
        ], style={'margin': '0px', 'padding': '0px'}, width=True)
    ], style={'margin': '0px', 'padding': '0px'}, className='g-2 my-auto')
    # Stores e Location

    # Layout
], fluid=True, style={'padding': '0px', 'margin': '0px'})


# ======= Callbacks ==========
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@app.callback(
    Output('base-url', 'pathname'),
    Input("login-state", "data"),
    Input("register-state", "data")
)
def render_page_content(login_state, register_state):
    ctx = dash.callback_context
    if ctx.triggered:
        trigg_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if trigg_id == 'login-state' and login_state == "success":
            return '/home'
        if trigg_id == 'login-state' and login_state == "error":
            return '/login'
        

        elif trigg_id == 'register-state':
            if register_state == "":
                return '/login'
            else:
                return '/register'
    else:
        return '/'
    

@app.callback(Output("page-content", "children"), 
            Input("base-url", "pathname"),
            [State("login-state", "data"), State("register-state", "data")])
def render_page_content(pathname, login_state, register_state):
    if (pathname == "/login" or pathname == "/"):
        return login.render_layout(login_state)

    if pathname == "/register":
        return register.render_layout(register_state)

    if pathname == "/home":
        if current_user.is_authenticated:
            return home.layout
        else:
            return login.render_layout(register_state)


# Run
if __name__ == '__main__':
    #app.run(debug=False, port=80, host='10.128.0.2')
    app.run(debug=False, port=443, host='10.128.0.2', ssl_context=('/etc/letsencrypt/live/soden.pyserver.com.br/cert.pem', '/etc/letsencrypt/live/soden.pyserver.com.br/privkey.pem'))
