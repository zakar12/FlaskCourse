from flask import render_template,json,redirect,url_for,request,flash,abort
#abort λειτουργεί όπως η first_or_404
from FlaskBlogApp.forms import SignupForm, LoginForm, ArticleForm,AccountUpdateForm
from FlaskBlogApp import app,db,bcrypt
from FlaskBlogApp.models import User,Article
from flask_login import login_user,current_user,logout_user,login_required
import os,secrets #κωδικοποίηση ονομάτων images για να μην υπάρχει conflict
from PIL import Image #βιβλιοθήκη επεξεργασίας εικόνων

#my_path = os.path.abspath(os.path.dirname(__file__))
#my_path=my_path+ "\mybooks.json"
#print("======================>")
#print (my_path)
#print("<======================")
#os.chdir('/src')
#p=os.getcwd()
 
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/404.html'), 404 # επιστρέφει και το status code 404 

@app.errorhandler(415)
def unsupported_media_type(e):
    # note that we set the 415 status explicitly
    return render_template('errors/415.html'), 415


def image_save(image, where, size): #where και για τα articles ή στα profile
    # το size είναι ένα tuple της μορφής πχ 640,480
    random_filename=secrets.token_hex(12)
    print(random_filename)
    _,file_extension=os.path.splitext(image.filename) #_ όνομα μεταβλητής που δεν χρησιμοποιείται. επιστρέφει tuple
    image_filename=random_filename+file_extension
    print(image_filename)
    #my_path=app.root_path+'/static/images/' + where + image_filename ή
    image_path=os.path.join(app.root_path,'static\images' + where, image_filename) 
    print(image_path)
    img=Image.open(image)
    print(img)
    img.thumbnail(size) #ή resize
    img.save(image_path)
    return image_filename

@app.route("/")
@app.route("/index/")
def root():
    page=request.args.get("page",1,type=int) #default=1 και μπορούμε να πουμε τον τύπο
    # αν δώσω page=hello θα το μετατρέψει αυτόματα σε None
    articles=Article.query.order_by(Article.date_created.desc()).paginate(per_page=3,page=page)
    return render_template("index.html",articles=articles)
    
@app.route("/articles_by_author/<int:author_id>")
def articles_by_author(author_id):
    user=User.query.get_or_404(author_id)
    page=request.args.get("page",1,type=int)
    articles=Article.query.filter_by(author=user).order_by(Article.date_created.desc()).paginate(per_page=1,page=page)
    print ('aaa ',articles.pages)    
    return render_template("articles_by_author.html",articles=articles,author=user) #,200 προαιρετικό


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
    if current_user.is_authenticated:
        return redirect(url_for('root'))
    form=LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        user=User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            flash(f"Eπιτυχές login {email}", "success")
            login_user(user,remember=form.remember_me.data) # η μέθοδος παίρνει παράμετρο remember
            next_link=request.args.get("next")
            return redirect(next_link) if next_link else redirect(url_for('root'))
        else:
            flash(f"Aνεπιτυχής είσοδος χρήστη", "warning")
    return render_template("login.html", form=form)

@app.route("/logout/")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash(f"Aποσύνδεση χρήση", "success")
    return redirect(url_for("root")) #στο url_for δηλώνουμεόπως είναι το όνομα της μεθόδου

@app.route("/new_article/", methods=["GET", "POST"])
@login_required
def new_article():
    form=ArticleForm()

    if request.method == "POST" and form.validate_on_submit():
        article_title=form.article_title.data
        article_body=form.article_body.data
        if form.article_image.data:
            #try:
            image_file=image_save(form.article_image.data,'\\articles_images',(640,360))
            #except:
            #    abort(415) #unsupported media type

            # extra λειτουργία που πρέπει να προστεθεί ->να διαγραφεί το παλιό αρχείο img από το δίσκο.
            #image_file το όνομα του αρχείου
            article=Article(article_title=article_title,article_body=article_body,author=current_user,article_image=image_file)
        else:
            article=Article(article_title=article_title,article_body=article_body,author=current_user)

        db.session.add(article)
        db.session.commit()
        flash(f"Eπιτυχής καταχώρηση άρθρου με τίτλο {article.article_title}", "success")
        return redirect (url_for('root'))
        
    return render_template("new_article.html", form=form, page_title="Εισαγωγή")


@app.route("/account/", methods=["GET", "POST"])
@login_required
def account():
    form=AccountUpdateForm(username=current_user.username, email=current_user.email)
     #προσυμπληρωμένα τα υφιστάμενα
    if request.method=="POST" and form.validate_on_submit():
        current_user.username=form.username.data # καταλαβαίνει το alchemy και κάνει αλλαγή στη βάση
        current_user.email=form.email.data
        # image_save (image,where,size)
        if form.profile_image.data:
            try:
                image_file=image_save(form.profile_image.data,'\profiles_images',( 150,150))
            except:
                abort(415) #unsupported media type

            # extra λειτουργία που πρέπει να προστεθεί ->να διαγραφεί το παλιό αρχείο img από το δίσκο.
            #image_file το όνομα του αρχείου
            current_user.profile_image=image_file
        db.session.commit() # δεν χρειάζεται να δηλώσουμε add
        flash(f"Eπιτυχής ενημέρωση χρήστη", "success")
        return redirect(url_for("root"))

    return render_template("account_update.html",form=form)


@app.route("/edit_article/<int:article_id>", methods=["GET", "POST"])
@login_required
def edit_article(article_id):#<> το βάζουμε και ως παράμετρο
    
    #article=Article.query.get(article_id)
    # if article:
    #     if article.author!=current_user:
    #         abort(403) #import από flask δεν μπορεί να αλλάξει αρθρο άλλου χρήστη
    # εναλλακτικά πιο εύκολα:
    
    article = Article.query.filter_by(id=article_id, author=current_user).first_or_404()
    # βρες αρθρο με id που περνάμε ως article_id και author τον current user. Aν δεν υπάρχει ->not found
    form=ArticleForm(article_title=article.article_title,article_body=article.article_body)

    if request.method == "POST" and form.validate_on_submit():
        article.article_title=form.article_title.data
        article.article_body=form.article_body.data

        if form.article_image.data:
            try:
                image_file=image_save(form.article_image.data,'\\articles_images',( 640,360)) #LATHOS LATHOS ????????????????????
            except:
                abort(415)  
            article.article_image=image_file
            
        db.session.commit()
        
        flash(f"Eπιτυχής ενημέρωση άρθρου <b>{article.article_title}<b>", "success")

        return redirect (url_for('root'))
        
    return render_template("new_article.html", form=form, page_title="Επεξεργασία")

@app.route("/full_article/<int:article_id>", methods=["GET"])
def full_article(article_id):
    article=Article.query.get_or_404(article_id)
    return render_template("full_article.html", article=article)


@app.route("/delete_article/<int:article_id>", methods=["GET","POST"])
@login_required
def delete_article(article_id):
    article = Article.query.filter_by(id=article_id, author=current_user).first_or_404()    
    if article:
        db.session.delete(article)
        db.session.commit()
        flash(f"Eπιτυχής διαγραφή άρθρου", "success")
        return redirect (url_for('root'))
    flash(f"To άρθρο δεν βρέθηκε", "warning") # από τη στιγμή που βάζουμε or404 δεν έχει νόημα η συγκεκριμένη σειρά
    return redirect (url_for('root'))



# @app.route("/books")
# def books():
#     with open("mybooks.json") as json_file:
#         jdict=json.load(json_file)
#         print(jdict)
#     return render_template("books.html",jdict=jdict)


