from FlaskBlogApp import db,login_manager
from datetime import datetime
from flask_login import UserMixin #κλάσεις που προσθέτουν πολλαπλή κληρονομικότητα

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(36), nullable=False)
    profile_image = db.Column(db.String(30),default='default_profile_image.jpg')
    articles = db.relationship('Article', backref='author', lazy=True)
    #column περιγραφής συσχέτισης , author = backreference πως θα αναφερόμαστε από τον article στον user,
    # lazy=True-> την στιγμή που φορτώνουμε το χρήστη ανεβάζουμε όλα τα άρθρα του
    #καλώντας Article.author μας φαίρνει το αντικείμενο user

    def __repr__(self):
        return f"{self.username}:{self.email}"

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_title = db.Column(db.String(50), unique=True, nullable=False)
    article_body = db.Column(db.Text(), nullable=False)
    article_image = db.Column(db.String(30), default='default_article_image.jpg')
    date_created = db.Column(db.DateTime, default=datetime.utcnow) #χωρίς παρενθέσεις στη default τιμη δίνουμε τρόπο υπολογισμού utcnow (σταθερή ώρα)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False ) #user.id αφορά τον πίνακα user

    def __repr__(self):
        return f"{self.date_created}:{self.article_title}"