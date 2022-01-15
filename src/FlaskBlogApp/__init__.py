from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import timedelta

app = Flask(__name__) 

app.config["SECRET_KEY"]="c3038989c4224e910fa7c8a878e2407e"
app.config["WTF_CSRF_SECRET_KEY"]="c34234303SDAF89c4224e234234910fa7234234c8a878e2407e" #αν δεν υπάρχει παίρνει ίδια τιμή με το SECRET KEY

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///flask_database.db" #sqlite:/// standard
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["REMEMBER_COOKIE_DURATION"]=timedelta(minutes=15)
db=SQLAlchemy(app)
bcrypt = Bcrypt(app) #δενουμε το αpp με το bcrypt

login_manager=LoginManager(app)
login_manager.login_view="login"
login_manager.login_message_category="warning"
login_manager.login_message="Παρακαλώ κάνετε login"


from FlaskBlogApp import routes,models # στο αρχείο routes καλούμε την app. Αν μπει στην αρχή δεν τη βλέπει!! 
                                        #το models προσωρινά μετά θα πάει στο routes

