from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
import datetime
from app import app
from app_database import CorpoAspirantes, OperacoesObservacoes
from dash.exceptions import PreventUpdate
import pdb

layout = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle('Adicione uma nova OD', style={'text-align': 'center'})),
    dbc.ModalBody([
        dbc.Row([
            dbc.Col([
                dbc.Label('Número Interno'),
                dbc.Input(id='num_int', placeholder='Apenas o número, sem letras.', type='text')
            ], sm=12, md=6),
            dbc.Col([
                dbc.Label('Nome'),
                dbc.Input(id='nome_de_guerra', placeholder='Insira o Nome de Guerra', type='text')
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Responsável pela OD')
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Nome do Responsavel da OD'),
                        dbc.Input(id='nome_responsavel_od', placeholder='Ex:4001/FN-401/IM-401')
                    ])
                ])
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.RadioItems(options=[{'label': 'Positiva', 'value': 2}, {'label': 'Negativa', 'value': 1}], value='Negativa', inline=True, className='dbc', id='positivity'),
                dbc.Checkbox(id='repreensao_po', label='É repreensão de PO?', style={'margin-top': '10px'}, value=False)
            ]),
            dbc.Col([
                dbc.Label('Data da Observação', style={'text-align': 'center', 'margin-top': '10px', 'margin-bottom': '5px'}),
                dcc.DatePickerSingle(date=datetime.date.today(), min_date_allowed=datetime.date(datetime.datetime.today().year, 1, 1),
                                     max_date_allowed=datetime.date(datetime.date.today().year, 12, 31), initial_visible_month=datetime.date.today(),
                                     className='dbc', id='data_da_od', style={'margin-top': '5px', 'text-align': 'center'})
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label('Descrição do Ocorrido:', style={'text-align': 'center'}),
                dbc.Input(id='descricao_od', required=True, html_size='300', style={'height': '40px'})
            ])
        ])
    ]),
    dbc.ModalFooter([
        dbc.Button('Adicionar', id='adicionar_od_button'),
        dbc.Button('Voltar', id='voltar_adicionar_od_button')
    ])
], id='modal_nova_od')


# ======== Modal Callbacks ==========
@app.callback(
    Output('num_int', 'value'),
    Output('nome_de_guerra', 'value'),
    Output('nome_responsavel_od', 'value'),
    Output('descricao_od', 'value'),
    Input('adicionar_od_button', 'n_clicks'),
    State('num_int', 'value'),
    State('nome_de_guerra', 'value'),
    State('nome_responsavel_od', 'value'),
    State('positivity', 'value'),
    State('repreensao_po', 'value'),
    State('data_da_od', 'date'),
    State('descricao_od', 'value')
)
def adicionar_od_no_bd(n_clicks, num_int, nome_de_guerra, nome_responsavel, sinal, repreensao, data, descricao):
    if n_clicks is None:
        raise PreventUpdate
    
    try:
        OperacoesObservacoes().adicionar_od(num_int=num_int, nome= nome_de_guerra, responsavel=nome_responsavel, data=data, tipo=sinal, repreensao=repreensao, descricao=descricao)
        #print('Feito')
        return None, None, None, None
    except Exception as E:
        print(E)
        return None, None, None, None