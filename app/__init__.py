from flask import Flask

app = Flask(__name__)

from app import config
from app import routes
from app import login
from app import api
from app import dashboard
from app import admin
from app import depositHandler
from app import order