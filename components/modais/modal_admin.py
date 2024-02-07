from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from app import *
import base64
import io
import pandas as pd
from app_database import *
from user_database import Database_Users
from dash.exceptions import PreventUpdate
from werkzeug.security import check_password_hash, generate_password_hash


layout_new_user = dbc.Modal([
    dbc.ModalHeader([
        dbc.Label(id='modify_user_title')
    ]),
    dbc.ModalBody([
        dbc.Row([
            dbc.Col([
                dbc.Input(id='modify_user', style={'margin-bottom': '10px'}),
                dbc.Checkbox(id='administrador', label='Este novo usuário poderá acessar os recursos de administrador?', value=False)
            ]),
            dbc.Col([
                dbc.Input(id='required_password', type='password', placeholder='Nova senha do Usuário', style={'margin-bottom': '10px'}),
                dbc.Checkbox(id='editor', label='Este novo usuário poderá adicionar novas ODs?', value=False)
            ]),
            dcc.Store(id='operation_user', data='')
        ])
    ]),
    dbc.ModalFooter([
        dbc.Button(id='new_user_button', n_clicks=None),
        dbc.Button('Voltar', id='voltar_modify_user_button', n_clicks=None)
    ])
], id='modify_user_modal', size='lg')

layout = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle('Manutenção do Sistema', style={'text-align': 'center'})),
    dbc.ModalBody([
        dbc.Row([
            dbc.Col([
                dbc.Checkbox(id='excluir_ods', label='Excluir todas as ODs anteriores?', value=False),
                html.Hr(),
                dbc.Checkbox(id='atualizar_corpo_de_aspirantes', label='Deseja Atualizar o Corpo de Aspirantes?', value=False),
                html.Hr(),
                dbc.Row([
                    dbc.Col([
                        dcc.Upload(
                            children=html.Div([
                                'Selecione um arquivo com o roll do corpo de aspirantes.',
                                html.A('Clique aqui para selecionar arquivo.')
                            ]),
                            id='novo_CA', 
                            className='dbc'),
                        html.Hr(),
                    ]),
                ]),
                dbc.Row([    
                    dbc.Col([
                        dbc.Button('Adicionar Usuário', id='adc_user', n_clicks=None, style={'margin-bottom': '15px'}),
                    ]),
                    dbc.Col([
                        dbc.Button('Remover Usuário', id='remove_user', n_clicks=None)
                    ])
                ])
            ])
        ]),
    ]),
    dbc.ModalFooter([
        dbc.Row([
            dbc.Col([
                dbc.Button('Atualizar', id='atualizar_button', style={'margin-bottom': '15px', 'margin-left': '10px'}),
            ], md=6),
            dbc.Col([
                dbc.Button('Voltar', id='admin_voltar_button', style={'margin-left': '10px'})
            ], md=6)
        ])
       
    ])
], id='modal_admin')


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded), sheet_name='CA', header=1, usecols=['Numero','Nome', 'Acesso'])
    except Exception as e:
        print(e)
        return pd.DataFrame()
    return df


# ======= Callbacks ========
@app.callback(
        Output('excluir_ods', 'value'),
        Output('atualizar_corpo_de_aspirantes', 'value'),
        Input('atualizar_corpo_de_aspirantes', 'value'),
        Input("excluir_ods", 'value'),
        prevent_initial_call = True
)
def ativar_excluir_ods(value_atualizar, value_excluir):
    ctx = dash.callback_context
    if ctx.triggered:
        trigg_id = ctx.triggered[0]['prop_id'].split('.')[0]
    #pdb.set_trace()
    if trigg_id == 'atualizar_corpo_de_aspirantes':
        if value_atualizar == True:
            return value_atualizar, True
        else:
            return value_excluir, value_atualizar
    else:
        if value_excluir == False:
            return False, False
        else:
            return value_excluir, value_atualizar



@app.callback(
    Output('feedback_div', 'children'),
    Input('atualizar_button', 'n_clicks'),
    State('excluir_ods', 'value'),
    State('atualizar_corpo_de_aspirantes', 'value'),
    State('novo_CA', 'contents'),
    State('novo_CA', 'filename'),
    prevent_initial_call = True
)
def reiniciar_ano(n_clicks, excluir_ods, atualizar_CA, conteudo, filename):
    print('aqui 1')
    if n_clicks is None:
        PreventUpdate
    response = ''
    #pdb.set_trace()
    if excluir_ods == True:
        print('aqui 2')
        try:
            OperacoesObservacoes().excluir_ods()
            print('AQUI 3')
            OperacoesObservacoes().criar_table()
            print('aqui 4')
            response += 'ODs excluidas com sucesso! '
        except:
            print('Erro excluindo as ODs')
            response += 'Erro ao excluir as ODs! '
    
    if atualizar_CA == True:
        if conteudo is not None:
            print('aqui1')
            df = parse_contents(conteudo, filename)
            # pdb.set_trace()
            if df.empty:
                print('erro fazendo upload')
                response += 'Erro ao fazer Upload. Não consegui ler o arquivo ou o arquivo está vazio! '
            else:
                try:
                    print('aqui2')
                # pdb.set_trace()
                    CorpoAspirantes().excluir_corpo_de_aspirantes()
                    CorpoAspirantes().inserir_corpo_de_aspirantes(df)
                    Database_Users().cadastrar_users(df)
                    print('upload bem sucedido')
                    response += 'Banco de dados atualizado com sucesso! '
                except:
                    response += 'Não foi possível inserir sua planilha no banco de dados! '

    return dbc.Label(response)
            
            
@app.callback(
    Output('modify_user_modal', 'is_open'),
    Output('modify_user_title', 'children'),
    Output('modify_user', 'placeholder'),
    Output('required_password', 'disabled'),
    Output('modal_admin', 'is_open', allow_duplicate=True),
    Output('operation_user', 'data'),
    Output('new_user_button', 'children'),
    Output('editor', 'disabled'),
    Output('administrador', 'disabled'),
    Input('adc_user', 'n_clicks'),
    Input('remove_user', 'n_clicks'),
    Input('voltar_modify_user_button', 'n_clicks'),
    Input('new_user_button', 'n_clicks'),
    State('modify_user_modal', 'is_open'),
    prevent_initial_call = True
)
def abrir_e_fechar_modificar_users(n1, n2, n3, n4, is_open):
    ctx = dash.callback_context
    if ctx.triggered:
        trigg_id = ctx.triggered[0]['prop_id'].split('.')[0]
    #pdb.set_trace()
    if trigg_id == 'adc_user':
        if n1 != None:
            return True, 'Adicionar Usuário', 'Novo Usuário', False, False, 'adicionar', 'Adicionar Usuário', False, False
    elif trigg_id == 'remove_user':
        if n2 != None:
            return True, 'Remover Usuário', 'Usuário a ser removido', True, False, 'remover', 'Remover Usuário', True, True
    elif trigg_id == 'new_user_button':
        if n4 != None:
            return False, '', '', False, False, '', '', False, False
    else:
        if n3 != None:
            return False, '', '', False, False, '', '', False, False
        
@app.callback(
    Output('modify_user', 'value'),
    Output('required_password', 'value'),
    Output('feedback_div', 'children', allow_duplicate=True),
    Input('new_user_button', 'n_clicks'),
    State('operation_user', 'data'),
    State('modify_user', 'value'),
    State('required_password', 'value'),
    State('editor', 'value'),
    State('admnistrador', 'value'),
    prevent_initial_call=True
)
def modificar_users(n_clicks, operacao, user, new_user_password, editor, administrador):
    if n_clicks != None:
        if operacao == 'adicionar':
            if administrador:
                situacao = 2
            elif editor:
                situacao = 1
            else:
                situacao = 0
            try:
                Database_Users().adicionar_usuario(user, situacao, generate_password_hash(new_user_password))
                return None, None, dbc.Label('Usuário Adicionado!')
            except:
                return None, None, dbc.Label('Erro ao adicionar o Usuário!')
        elif operacao == 'remover':
            try:
                Database_Users().remover_usuario(user)
                return None, None, dbc.Label('Usuário removido com sucesso!')
            except:
                return None, None, dbc.Label('Erro ao remover o usuário!')
        
