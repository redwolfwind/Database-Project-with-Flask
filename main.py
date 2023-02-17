from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
#app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#db = SQLAlchemy(app)



app.run("LOCALHOST",8080)
