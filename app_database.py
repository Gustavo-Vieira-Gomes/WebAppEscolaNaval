from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas as pd
import datetime
import pdb

Base = declarative_base()

class CorpoAspirantes(Base):
    __tablename__ = 'corpo_de_aspirantes'
    index = Column(Integer, primary_key=True)
    Numero = Column(String)
    Nome = Column(String)

    def __init__(self):
        self.engine = create_engine('postgresql://postgres:anaeivan10@10.128.0.2:5432/postgres')
        self.session = sessionmaker(bind=self.engine)()

    def inserir_corpo_de_aspirantes(self, df_):
        df = pd.DataFrame(df_)
        df.loc[:, ('Numero', 'Nome')]
        df.to_sql('corpo_de_aspirantes', con=self.engine, if_exists='replace', )

    def excluir_corpo_de_aspirantes(self):
        Base.metadata.drop_all(self.engine)

    def buscar_aspirante(self, key, value):
        match key:
            case 'Num_interno':    
                searched_item = self.session.query(CorpoAspirantes).filter_by(Numero=value).first()
            case 'Nome':
                searched_item = self.session.query(CorpoAspirantes).filter_by(Nome=value).first()
        return searched_item

Base2 = declarative_base()


class ObservacoesDinamicas(Base2):
    __tablename__ = 'observções_dinâmicas'
    id = Column(Integer, primary_key=True)
    Num_interno = Column(String)
    Nome = Column(String)
    Responsavel = Column(String)
    Data = Column(Date)
    TipoDeOD = Column(Integer)
    Descricao = Column(String)


class OperacoesObservacoes:
    def __init__(self):
        self.engine = create_engine('postgresql://postgres:anaeivan10@localhost:5432/postgres')
        self.session = sessionmaker(bind=self.engine)()

    def criar_table(self):
        Base2.metadata.create_all(self.engine)

    def adicionar_od(self, num_int, nome, responsavel, data, tipo, descricao):
        if (nome is None  or nome == '') and (num_int is not None and num_int != ''):
            nome = CorpoAspirantes().buscar_aspirante('Num_interno', num_int).Nome
        elif (num_int is None or num_int == '') and (nome is not None and nome != ''):
            num_int = CorpoAspirantes().buscar_aspirante('Nome', nome.upper()).Numero
        responsavel = '' if responsavel is None else responsavel
        descricao = '' if descricao is None else descricao
        nova_od = ObservacoesDinamicas(Num_interno=num_int, Nome=nome.upper(), Responsavel=responsavel, Data=data, TipoDeOD=tipo,Descricao=descricao)
        self.session.add(nova_od)
        self.session.commit()
        self.session.close()

    def buscar_ods_aspirante(self, nome, num_int):
        df = pd.DataFrame(columns=['Numero Interno', 'Nome', 'Responsavel', 'Data','Tipo de OD', 'Descricao'])
        if (nome is None  or nome == '') and (num_int is not None and num_int != ''):
            nome = CorpoAspirantes().buscar_aspirante('Num_interno', num_int).Nome
        elif (num_int is None or num_int == '') and (nome is not None and nome != ''):
            num_int = CorpoAspirantes().buscar_aspirante('Nome', nome.upper()).Numero
        query = self.session.query(ObservacoesDinamicas).filter_by(Nome=nome, Num_interno=num_int).all()
        for od in query:
            df_ = pd.DataFrame({'Numero Interno': od.Num_interno, 'Nome': od.Nome, 'Responsavel': od.Responsavel, 'Data': od.Data, 'Tipo de OD': od.TipoDeOD, 'Descricao': od.Descricao}, index=[od.id])
            df = pd.concat([df, df_], axis=0)

        return df

    def excluir_ods(self):
        Base2.metadata.drop_all(self.engine)

    def contar_odd(self, tipo_de_od):
        df = pd.DataFrame(columns=['Numero Interno', 'Nome', 'Responsavel', 'Data', 'Tipo de OD', 'Descricao'])
        tipo_de_od = 2 if tipo_de_od == 'positiva' else 1
        query = self.session.query(ObservacoesDinamicas).all()
        for od in query:
            df_ = pd.DataFrame({'Numero Interno': od.Num_interno, 'Nome': od.Nome, 'Responsavel': od.Responsavel, 'Data': od.Data, 'Tipo de OD': od.TipoDeOD, 'Descricao': od.Descricao}, index=[od.id])
            df = pd.concat([df, df_], axis=0)
        
        if df.empty:
            return 'Sem ODs Inseridas no Banco de Dados Até Agora'
        else:
            partial_df = df[df['Tipo de OD'] == tipo_de_od]
            if partial_df.empty:
                response = 'Sem ODs positivas no Banco de dados' if tipo_de_od == 2 else 'Sem ODs negativas no banco de dados'
                return response
            
            filtered_df = partial_df.groupby(by=['Numero Interno'])[['Tipo de OD']].sum()
            filtered_df.reset_index(inplace=True)
            filtered_df['Tipo de OD'] = filtered_df['Tipo de OD'].astype('int32')
            filtered_df.set_index('Numero Interno', inplace=True)
            asp_destaque = filtered_df.idxmax()[0]
            if tipo_de_od == 2:  numero_de_anots = filtered_df.loc[asp_destaque][0] / 2
            else: 
                numero_de_anots = filtered_df.loc[asp_destaque][0]

            return asp_destaque, numero_de_anots
 

    def obter_todas_ods(self):
        df = pd.DataFrame(columns=['Numero Interno', 'Nome', 'Responsavel', 'Data', 'Tipo de OD', 'Descricao'])
        query = self.session.query(ObservacoesDinamicas).all()
        
        for od in query:
            df_ = pd.DataFrame({'Numero Interno': od.Num_interno, 'Nome': od.Nome, 'Responsavel': od.Responsavel, 'Data': od.Data, 'Tipo de OD': od.TipoDeOD, 'Descricao': od.Descricao}, index=[od.id])
            df = pd.concat([df, df_], axis=0)
        
        df.loc[:, 'Tipo de OD'] = df.loc[:, 'Tipo de OD'].replace(2, 'positiva').replace(1, 'negativa')
        df.loc[:, 'Data'] = df.loc[:, 'Data'].apply(lambda x: datetime.datetime.strftime(x, '%d/%m/%Y'))
        
        return df
