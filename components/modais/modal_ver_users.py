from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from app_database import CorpoAspirantes, OperacoesObservacoes
from user_database import Database_Users
import pandas as pd
from dash import dash_table
from dash.dash_table.Format import Group
from app import *
from dash.exceptions import PreventUpdate
import pdb
import datetime

layout = dbc.Modal(children=[
    dbc.ModalHeader(dbc.ModalTitle(id='ver_user_title', children=['Listagem de Usuários Ativos'])),
    dbc.ModalBody([
        dbc.Row([
            dbc.Col([
                html.Div(id='table_users', className='dbc')
            ])
        ])
    ]),
    dbc.ModalFooter([
        dbc.Button('Voltar', style={'text-align': 'right'}, id='voltar_ver_user', n_clicks=None)
    ])
], id='modal_apresentar_users', size='lg')


# =============== Callbacks ====================

@app.callback(
        Output('table_users', 'children'),
        Input('ver_users_button', 'n_clicks'),
        prevent_initial_call=True
)
def table(n1):    
    usuarios = Database_Users().pegar_tabela()
    df = pd.DataFrame(data=usuarios, columns=['Usuário', 'Editor de OD'])
    df.replace({True:'Sim', False:'Não'}, inplace=True)
    table = dash_table.DataTable(
        id='datatable',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action='native',
        sort_action='native',
        sort_mode='single',
        page_size=10,
        page_current=0
    )

    return table