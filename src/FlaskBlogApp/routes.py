from flask import render_template,json,redirect,url_for,request,flash

from FlaskBlogApp.forms import SignupForm, LoginForm, ArticleForm
from FlaskBlogApp import app,db,bcrypt
from FlaskBlogApp.models import User,Article

import os,secrets

#my_path = os.path.abspath(os.path.dirname(__file__))
#my_path=my_path+ "\mybooks.json"
#print("======================>")
#print (my_path)
#print("<======================")
#os.chdir('/src')
#p=os.getcwd()
 
@app.route("/")
@app.route("/index/")
def root():
    articles=Article.query.all()
    return render_template("index.html",articles=articles)

@app.route("/signup/", methods=["GET", "POST"]) #default χρησιμοποιεί το GET αν χρησιμοποιηθεί POST πρέπει να το δηλώσουμε αλλιώς θα βγάλει λάθος
def signup(): 
    form=SignupForm()
    if request.method == "POST" and form.validate_on_submit():
        username=form.username.data
        email=form.email.data
        password=form.password.data
        password2=form.password2.data
        encrypted_password=bcrypt.generate_password_hash(password).decode('UTF-8')
        user=User(username=username, email=email, password=encrypted_password)
        db.session.add(user)
        db.session.commit()
        flash(f"O λογαριασμός για τον χρήστη <b>{username}</b> δημιουργήθηκε με επιτυχία", "success")
        return redirect(url_for('login')) # μέσα βάζουμε το όνομα της μεθόδου
    #ΠΑΛΙΑ ΜΕΘΟΔΟΣ request.form -> επιστρέφει dictionary πχ request.form["username"]
    # if request.method == 'POST': 
    #     username=request.form["username"]
    #     email=request.form["email"]
    #     password=request.form["password"]
    #     password2=request.form["password2"]
    return render_template("signup.html", form=form)

@app.route("/login/", methods=["GET", "POST"])
def login():
    form=LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        bc=Bcrypt()
        bc.generate_password_hash(password).decode('utf-8')
        flash(f"Eπιτυχές login {email}", "success")
    return render_template("login.html", form=form)

@app.route("/logout/")
def logout():
    return redirect(url_for("root")) #στο url_for δηλώνουμεόπως είναι το όνομα της μεθόδου

@app.route("/new_article/", methods=["GET", "POST"])
def new_article():
    form=ArticleForm()
    if request.method == "POST" and form.validate_on_submit():
        title=form.article_title.data
        body=form.article_body.data
        flash(f"Eπιτυχής καταχώρηση άρθρου", "success")
    return render_template("new_article.html", form=form)


@app.route("/books")
def books():
    with open("mybooks.json") as json_file:
        jdict=json.load(json_file)
        print(jdict)
    return render_template("books.html",jdict=jdict)
