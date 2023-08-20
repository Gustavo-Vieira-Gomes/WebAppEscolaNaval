from sqlalchemy import Table, create_engine, String, Column
from sqlalchemy.orm import sessionmaker, declarative_base
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from app import *
import pandas as pd
from flask_login import login_user
from flask_login import UserMixin, LoginManager
from user_database import *
from datetime import timedelta
import pdb

db = SQLAlchemy()

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Num_interno = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(100), nullable=False)

Users_tbl = Table('users', Users.metadata)

class Database_Users:
    def __init__(self) -> None:
        self.engine = create_engine('postgresql://postgres:anaeivan10@localhost:5432/postgres')
        self.Session = sessionmaker(self.engine)
        self.session = self.Session()
        

    def _create_users_table(self):
        Users.metadata.create_all(self.engine)

    def registrar_user(self, num_int, old_password, password):
        pdb.set_trace()
        if check_password_hash(Users.query.filter_by(Num_interno=num_int).first().password, old_password):
            hashed_password = generate_password_hash(password, method='sha256')
            pdb.set_trace()
            upd = Users_tbl.update().where(Users_tbl.c.Num_interno==num_int).values(password=hashed_password)
            conn = self.engine.connect()
            try:
                pdb.set_trace()
                conn.execute(upd)
                conn.commit()
                conn.close()
            except Exception as E:
                print(E)
        else:
            raise ConnectionRefusedError

    def _apagar_users(self):
        delete = Users_tbl.drop(self.engine)
        conn = self.engine.connect()
        conn.execute(delete)
        conn.close()

    def cadastrar_users(self, df):
        df['Numero'] = df['Numero'].astype('str')
        df_quarto_ano = df[(df['Numero'].apply(lambda x: x[0]) == '4') | (df['Numero'].apply(lambda x: x[0]) == 'F') | (df['Numero'].apply(lambda x: x[0]) == 'I')]
        df_quarto_ano.loc[:, ('password')] = df_quarto_ano.loc[:, ('Nome')].apply(lambda x: generate_password_hash(x))
        df_quarto_ano.rename(columns={'Numero': 'Num_interno'}, inplace=True)
        df_quarto_ano.rename_axis(index='id', inplace=True)
        df_quarto_ano.drop('Nome', inplace=True, axis=1)
        try:
            df_quarto_ano.to_sql('users', con=self.engine, if_exists='replace', index_label='id')
        except Exception as E:
            print('não foi possível jogar a tabela para o banco', E)

    def adicionar_usuario(self, user, password):
        id = len(Users.query.all())
        usuario = Users(id=id, Num_interno=user, password=password)    
        try:
            #pdb.set_trace()
            self.session.add(usuario)
            self.session.commit()
            self.session.close()
            print('Novo usuario adicionado com sucesso!')
        except Exception as E:
            print('Erro ao adicionar novo usuario!', E)

    def remover_usuario(self, user):
        usuario = Users.query.filter_by(Num_interno=user).first()

        if usuario:
            try:
                session = self.session.object_session(usuario)
                session.delete(usuario)
                session.commit()
                session.close()
                print('Usuário removido com sucesso')
            except Exception as E:
                print('Erro removendo o usuario', E)

    
    def verificar_senha_de_login(self, num_int, password):
        user = Users.query.filter_by(Num_interno=num_int).first()
        if check_password_hash(user.password, password):
            try:
                login_user(user, duration=timedelta(hours=12), remember=True, force=True)
            except Exception as E:
                print('login_user', E)
        else:
            raise ConnectionRefusedError
        
Base = declarative_base()

class AdminPassword(Base):
    __tablename__ = 'admin_password'
    admin_password = Column(String, primary_key=True)

class AdminPasswordOperation:
    def __init__(self):
        self.engine = create_engine('postgresql://postgres:anaeivan10@localhost:5432/postgres')
        self.session = sessionmaker(bind=self.engine)()
    
    def criar_database(self):
        Base.metadata.create_all(self.engine)

    def inserir_senha(self, password):
        hashed_password = generate_password_hash(password)
        instance = AdminPassword(admin_password=hashed_password)
        self.session.add(instance)
        self.session.commit()
        self.session.close()

    def apagar_senha(self):
        Base.metadata.drop_all(self.engine)

    def pegar_senha(self):
        query = self.session.query(AdminPassword).all()
        for passwords in query:
            senha = passwords.admin_password
        return senha
