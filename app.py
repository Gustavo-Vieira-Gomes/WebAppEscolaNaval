import dash
import dash_bootstrap_components as dbc
import os
from user_database import *
from sqlalchemy.sql import select
from flask_login import UserMixin, LoginManager
import os

estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", dbc.themes.LUX]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=estilos + [dbc_css])
server = app.server

server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:apptolda@localhost:5432/postgres',
    SQLALCHEMY_TRACK_MODIFICATIONS=False)


db.init_app(server)
