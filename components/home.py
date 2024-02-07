from dash import html, dcc, callback_context, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
from app_database import CorpoAspirantes, OperacoesObservacoes
from dash.exceptions import PreventUpdate
from app import app
from components.sidebar import layout_sidebar
import pdb

# ========== Styles ===========
card_style = {'height': '100%', 'margin-bottom': '12px'}

# Função para gerar os cards


# ======== Layout =========
layout_home = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Location(id='data-url'),
            html.H3('SISTEMA DE OBSERVAÇÃO DINÂMICA', style={'text-align': 'center'})
        ], className='text-center'),
    ], style={'margin-top': '20px'}, className='g-2 my-auto'),
    html.Hr(style={'margin-top': '0px'}),
    dbc.Row([
        # Filtros
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            dbc.Row([
                                dbc.Col([
                                    html.H3('Buscar Aspirante', style={'text-align': 'center', 'justify-content': 'center'})
                                ])
                            ]),
                        ]),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.H6('Nome do'),
                                    html.H6('Aspirante')
                                ], md=4),
                                dbc.Col([
                                    dbc.Input(id='nome_aspirante')
                                ], md=8)
                            ], style={'margin-bottom': '15px'}),
                            dbc.Row([
                                dbc.Col([
                                    html.H6('Número'),
                                    html.H6('Interno')
                                ], md=4),
                                dbc.Col([
                                    dbc.Input(id='numero_interno_aspirante')
                                ], md=8)
                            ], style={'margin-top': '15px', 'margin-bottom': '15px'}),
                            dbc.Row([
                                dbc.Col([
                                    dcc.DatePickerRange(min_date_allowed=datetime.date(year=datetime.datetime.today().year, month=1, day=1),
                                                        max_date_allowed=datetime.date(year=datetime.datetime.today().year, month=12, day=31),
                                                        start_date=datetime.date(year=datetime.datetime.today().year, month=1, day=1),
                                                        end_date=datetime.date.today(),
                                                        initial_visible_month=datetime.date.today(),
                                                        style={'margin-left': 'auto', 'margin-right': 'auto'}, className='dbc', id='date_range')
                                ]),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dcc.RadioItems(id='tipo_filter', options=[{'label': ' ODs Positivas', 'value': 2}, {'label': ' ODs Negativas', 'value': 1}, {'label': ' Todas as ODs', 'value': 0}], value=0, style={'font-size': '15px', 'margin-top': '15px'})
                                ]),
                                dbc.Col([
                                    dbc.Button('Buscar', style={'vertical-alignment': 'center', 'margin-top': '25px'}, id='buscar_asp_buttom')
                                ])
                            ])
                        ])
                    ])
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Container(id='aspirante_buscado', fluid=True)
                ])
            ], class_name='g-2 my-auto')
        ], md=5),
    # Destaques
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            dbc.Row([
                                dbc.Col([
                                    html.H6('Destaque Positivo:', style={'margin-top': '10px', 'text-align': 'center'})
                                ]),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.H6(' Aspirante com maior numero de Observações Positivas', style={'text-align': 'center'})
                                ])
                            ])
                        ]),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(id='ods_destaque_positivo')
                                ])
                            ]),
                        ])
                    ])
                ])
            ], className='g-2 my-auto'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                             dbc.Row([
                                    dbc.Col([
                                        html.H6('Destaque Negativo:', style={'margin-top': '10px', 'text-align': 'center'})
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.H6(' Aspirante com maior numero de Observações Negativas', style={'text-align': 'center'})
                                    ])
                                ])
                        ]),
                        dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        html.Div(id='ods_destaque_negativo')
                                    ])
                                ]),
                            ])
                    ])
                ])
            ], className='g-2 my-auto'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div(id='feedback_div', className='dbc', style={'margin': '0px', 'padding': '0px', 'text-align': 'center'})                          
                        ])
                    ])
                ])
            ], className='g-2 my-auto')
        ], md=7)
    ], className='g-2 my-auto')
], fluid=True, style={'margin': '0px', 'padding': '0px'})

layout = dbc.Container([
    dbc.Row([
            dbc.Col([
                layout_sidebar,
            ], md=2, style={'padding': '0px', 'margin': '0px'}),
            dbc.Col([
                layout_home,
                html.Div(id='div_fantasma_admin', hidden=True)
            ], md=10, style={'padding-left': '5px'})
        ], style={'margin': '0px', 'padding': '0px'})
], fluid=True, style={'padding':'0px'})


# Gerar card Aspirante Buscado
def searched_asp(num_int, nome):        
    card_asp_buscado = dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col([
                    dbc.Label(f'ASPIRANTE {num_int} {nome}', style={'text-align': 'center', 'justify-content': 'center'})
                ], style={'text-align': 'center', 'justify-content': 'center'})
            ])
        ]),
        dbc.CardBody([
            dbc.Row([
                
                dbc.Col([
                    dbc.Button('Abrir', size='md', id='abrir_ods_searched_asp')
                ], style={'text-align': 'center', 'margin-right': '20px', 'margin-left': '20px'})
            ])
        ])
    ])
    return card_asp_buscado

# Gerar Card Destaque positivo
def gerar_destaque_positivo():
    asp = OperacoesObservacoes().contar_odd('positiva')
    if asp == 'Sem ODs Inseridas no Banco de Dados Até Agora':
        card = dbc.Row([
            dbc.Col([
                dbc.Label('Sem Nenhuma Observação Dinâmica no Banco de Dados', id='nome_aspirante_pos')
            ]),
            dbc.Col([
                dbc.Button('Abrir', id='olhar_destaque_positivo', style={'height': '60px', 'width': '180px'}, n_clicks=None, disabled=True)
            ])
        ])
    elif asp == 'Sem ODs positivas no Banco de dados' or asp == 'Sem ODs negativas no banco de dados':
        card = dbc.Row([
            dbc.Col([
                dbc.Label(asp, id='nome_aspirante_pos')
            ]),
            dbc.Col([
                dbc.Button('Abrir', id='olhar_destaque_positivo', style={'height': '60px', 'width': '180px'}, n_clicks=None, disabled=True)
            ])
        ])
    else:
        nome = CorpoAspirantes().buscar_aspirante('Num_interno', asp[0]).Nome
        df_negativo = OperacoesObservacoes().buscar_ods_aspirante(None, asp[0])
        df_aspirante_negativo = df_negativo[df_negativo['Tipo de OD'] == 1].groupby(by=['Numero Interno'])[['Tipo de OD']].sum()
        if asp[0] in df_aspirante_negativo.index:
            numero_anots_negativo = df_aspirante_negativo.loc[asp[0]][0]
        else: numero_anots_negativo = 0
    
        card = dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Label(f'ASPIRANTE {asp[0]} {nome}', id='nome_aspirante_pos')
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label(f'{int(asp[1])} Observações Positivas'),
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label(f'{numero_anots_negativo} Observações Negativas')
                            ])
                        ])
                    ])
                ])
            ]),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Button('Abrir', id='olhar_destaque_positivo', style={'height': '60px', 'width': '180px'}, n_clicks=None)
                    ], style={'text-align': 'center', 'justify-content': 'center'})
                ])
            ])
        ])

    return card
        
            

# Gerar Card Aluno Negativo
def gerar_card_negativo():
    asp = OperacoesObservacoes().contar_odd('negativo')
    if asp == 'Sem ODs Inseridas no Banco de Dados Até Agora':
        card = dbc.Row([
            dbc.Col([
                dbc.Label('Sem Nenhuma Observação Dinâmica no Banco de Dados', id='nome_aspirante_neg')
            ]),
            dbc.Col([
                dbc.Button('Abrir', id='olhar_destaque_negativo', style={'height': '60px', 'width': '180px'}, n_clicks=None, disabled=True)
            ])
        ])
    elif asp == 'Sem ODs Positivas no Banco de dados' or asp == 'Sem ODs negativas no banco de dados':
        card = dbc.Row([
            dbc.Col([
                dbc.Label(asp, id='nome_aspirante_neg')
            ]),
            dbc.Col([
                dbc.Button('Abrir', id='olhar_destaque_negativo', style={'height': '60px', 'width': '180px'}, n_clicks=None, disabled=True)
            ])
        ])
        
    else:
        nome = CorpoAspirantes().buscar_aspirante('Num_interno', asp[0]).Nome
        df_positivo = OperacoesObservacoes().buscar_ods_aspirante(None, asp[0])
        df_aspirante_positivo = df_positivo[df_positivo['Tipo de OD'] == 2].groupby(by=['Numero Interno'])[['Tipo de OD']].sum()
        if asp[0] in df_aspirante_positivo.index:
            numero_anots_positivo = df_aspirante_positivo.loc[asp[0]][0] / 2
        else: numero_anots_positivo = 0
    
        card = dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Label(f'ASPIRANTE {asp[0]} {nome}', id='nome_aspirante_neg')
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label(f'{int(numero_anots_positivo)} Observações Positivas'),
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label(f'{asp[1]} Observações Negativas')
                            ])
                        ])
                    ])
                ])
            ]),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Button('Abrir', id='olhar_destaque_negativo', style={'height': '60px', 'width': '180px'}, n_clicks=None)
                    ], style={'text-align': 'center', 'justify-content': 'center'})
                ])
            ])
        ])

    return card


# Tentar encontrar uma solução para os problemas de não conseguir acessar um item que ainda não foi lançado.

# ======= Callbacks ========
@app.callback(
    Output('aspirante_buscado', 'children'),
    Output('searched_asp_store', 'data'),
    Output('nome_aspirante', 'value'),
    Output('numero_interno_aspirante', 'value'),
    Input('buscar_asp_buttom', 'n_clicks'),
    State('nome_aspirante', 'value'),
    State('numero_interno_aspirante', 'value'),
    State('date_range', 'start_date'),
    State('date_range', 'end_date'),
    State('tipo_filter', 'value')
)
def renderizar_searched_card(n_clicks, nome, numero, initial_date, final_date, tipo_filter):
    if n_clicks is None:
        raise PreventUpdate

    if nome is None or nome == '':
        nome = CorpoAspirantes().buscar_aspirante('Num_interno', numero).Nome
    if numero is None or numero == '':
        numero = CorpoAspirantes().buscar_aspirante('Nome', nome.upper()).Numero
    
    store_dict = {'nome': nome.upper(), 'numero': numero, 'initial_date': initial_date, 'final_date': final_date, 'tipo_filter': tipo_filter}

    card = searched_asp(numero, nome.upper())

    return card, store_dict, None, None


@app.callback(
    Output('ods_destaque_positivo', 'children'),
    Input('adicionar_od_button', 'n_clicks'),
    Input('base-url', 'pathname')
)
def destaque_positivo(n_clicks, pathname):
    if pathname == '/home':
        layout = gerar_destaque_positivo()
        return layout
    

@app.callback(
    Output('ods_destaque_negativo', 'children'),
    Input('adicionar_od_button', 'n_clicks'),
    Input('base-url', 'pathname')
)
def destaque_negativo(n_clicks, pathname):
    if pathname == '/home':
        layout = gerar_card_negativo()
        return layout
    