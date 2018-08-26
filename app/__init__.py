from flask import Flask
from config import Config

app_inst = Flask(__name__)
app_inst.config.from_object(Config)

from app import routes
