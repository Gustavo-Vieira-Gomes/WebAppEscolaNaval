from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from app_database import CorpoAspirantes, OperacoesObservacoes
import pandas as pd
from dash import dash_table
from dash.dash_table.Format import Group
from app import *
from dash.exceptions import PreventUpdate
import pdb
import datetime

layout = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle(id='ver_asp_title')),
    dbc.ModalBody([
        dbc.Row([
            dbc.Col([
                html.Div(id='table_asp', className='dbc')
            ])
        ])
    ]),
    dbc.ModalFooter([
        dbc.Button('Voltar', style={'text-align': 'right'}, id='voltar_ver_asp', n_clicks=None)
    ])
], id='modal_apresentar_ods', size='xl')


# ======= Callbacks ========
@app.callback(
    Output('modal_apresentar_ods', 'is_open', allow_duplicate=True),
    Input('olhar_destaque_positivo', 'n_clicks'),
    Input('olhar_destaque_negativo', 'n_clicks'),
    Input('voltar_ver_asp', 'n_clicks'),
    State('modal_apresentar_ods', 'is_open'),
    prevent_initial_call=True
)
def toggle_modal(n1, n2, n3, is_open):
    if n1 is None and n2 is None and n3 is None:
        raise PreventUpdate
    
    ctx = dash.callback_context
    if ctx.triggered:
        trigg_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigg_id == 'olhar_destaque_positivo':
        if n1 != None:
            return not is_open
    elif trigg_id == 'olhar_destaque_negativo':
        if n2 != None:
            return not is_open
    else:
        if is_open:
            return not is_open


@app.callback(
    Output('modal_apresentar_ods', 'is_open', allow_duplicate=True),
    Input('abrir_ods_searched_asp', 'n_clicks'),
    Input('voltar_ver_asp', 'n_clicks'),
    State('modal_apresentar_ods', 'is_open'),
    prevent_initial_call=True,
)
def toggle_modal2(n1, n2, is_open):
    #if n1 is None and n2 is None:
    #    raise PreventUpdate
    
    ctx = dash.callback_context
    if ctx.triggered:
        trigg_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if trigg_id == 'abrir_ods_searched_asp':
        if n1 != None:
            return not is_open
    elif trigg_id == 'voltar_ver_asp':
        if is_open:
            return not is_open
    


@app.callback(
    Output('table_asp', 'children', allow_duplicate=True),
    Output('ver_asp_title', 'children', allow_duplicate=True),
    Input('olhar_destaque_positivo', 'n_clicks'),
    Input('olhar_destaque_negativo', 'n_clicks'),
    State('nome_aspirante_pos', 'children'),
    State('nome_aspirante_neg', 'children'),
    prevent_initial_call=True
)
def table(n1, n2, asp_pos, asp_neg):
    if n1 is None and n2 is None:
        raise PreventUpdate
    
    pdb.set_trace()
    ctx = dash.callback_context
    if ctx.triggered:
        trigg_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigg_id == 'olhar_destaque_positivo':
        nome = ' '.join(asp_pos.split(' ')[2:])
        numero = asp_pos.split(' ')[1]
        df = OperacoesObservacoes().buscar_ods_aspirante(nome, numero)
    elif trigg_id == 'olhar_destaque_negativo':
        nome = ' '.join(asp_neg.split(' ')[2:])
        numero = asp_neg.split(' ')[1]
        df = OperacoesObservacoes().buscar_ods_aspirante(nome, numero)

    df['Data'] = df['Data'].apply(lambda x: x.strftime('%d/%m/%Y'))
    df['Tipo de OD'] = df['Tipo de OD'].map({1: 'Negativa', 2: 'Positiva'})
    df['Repreensao?'] = df['Repreensao?'].map({False: 'Não', True: 'Sim'})


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

    return table, f'ASPIRANTE {numero} {nome}'


@app.callback(
    Output('table_asp', 'children', allow_duplicate=True),
    Output('ver_asp_title', 'children', allow_duplicate=True),
    Input('abrir_ods_searched_asp', 'n_clicks'),
    State('searched_asp_store', 'data'),
    prevent_initial_call=True
)
def table_(n1, searched_data):
    if n1 is None:
        raise PreventUpdate
    
    ctx = dash.callback_context
    if ctx.triggered:
        trigg_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigg_id == 'abrir_ods_searched_asp':
        df = OperacoesObservacoes().buscar_ods_aspirante(searched_data['nome'], searched_data['numero'])
        if df.empty:
            return dbc.Container([dbc.Row([dbc.Col([dbc.Label('Esse Aspirante não possui nenhuma anotação')])])], fluid=True), f"ASPIRANTE {searched_data['numero']} {searched_data['nome']}"
        if searched_data['tipo_filter'] == 1:
            df = df[df['Tipo de OD'] == 1]
            pdb.set_trace()
            df = df[(df['Data'] <= searched_data['final_date']) & (df['Data'] >= searched_data['initial_date'])]
        elif searched_data['tipo_filter'] == 2:
            pdb.set_trace()
            df = df[df['Tipo de OD'] == 1]
            df = df[(df['Data'] <= searched_data['final_date']) & (df['Data'] >= searched_data['initial_date'])]
 
        df['Data'] = df['Data'].apply(lambda x: x.strftime('%d/%m/%Y'))
        df['Tipo de OD'] = df['Tipo de OD'].map({1: 'Negativa', 2: 'Positiva'})
        df['Repreensao?'] = df['Repreensao?'].map({False: 'Não', True: 'Sim'})


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

    return table, f"ASPIRANTE {searched_data['numero']} {searched_data['nome']}"
