from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
    session,
)
import os
import config
from datetime import datetime
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config["MYSQL_USER"] = config.MYSQL_USER
app.config["MYSQL_DB"] = config.MYSQL_DB
app.config["MYSQL_PASSWORD"] = config.MYSQL_PASSWORD
app.config["SECRET_KEY"] = config.HEX_SEC_KEY  # Configurar la clave secreta
mysql = MySQL(app)
