from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_qrcode import QRcode
from flask_mysqldb import MySQL
import yaml, os

app = Flask(__name__)
db = yaml.safe_load(open("db.yaml")) 
app.config["MYSQL_HOST"] = db["mysql_host"]
app.config["MYSQL_USER"] = db["mysql_user"]
app.config["MYSQL_PASSWORD"] = db["mysql_password"]
app.config["MYSQL_DB"] = db["mysql_db"]
QRcode(app)

app.secret_key = os.urandom(16)
mysql = MySQL(app)

def get_cursor():
    return mysql.connection.cursor()

from corona_archive import routes