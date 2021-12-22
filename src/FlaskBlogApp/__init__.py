from flask import Flask

app = Flask(__name__) 
app.config["SECRET_KEY"]="c3038989c4224e910fa7c8a878e2407e"
app.config["WTF_CSRF_SECRET_KEY"]="c34234303SDAF89c4224e234234910fa7234234c8a878e2407e" #αν δεν υπάρχει παίρνει ίδια τιμή με το SECRET KEY
from FlaskBlogApp import routes # στο αρχείο routes καλούμε την app. Αν μπει στην αρχή δεν τη βλέπει!!
