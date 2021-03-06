from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed #διαφορετικός χειρισμός για πεδίο αρχείου και τον validator του
from wtforms import StringField,SubmitField,TextAreaField,BooleanField
#from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, DataRequired,Email,Length,EqualTo, ValidationError,Optional
from FlaskBlogApp.models import User #για να κάνουμε έλεγχο στη βάση με query
from flask_login import current_user

#εξωτερικό validator για να χρησιμοποιηθεί σε διάφορες φόρμες δεν απευθύνεται μόνο σε μια φόρμα 
# άρα διαφορετική από validate_email
def maxImageSize(max_size=2):
    max_bytes=max_size*1024*1024
    def _check_file_size(form,field): #εσωτερικη συνήθως δηλώνεται _name
        if len(field.data.read())>max_bytes: #The read() method returns the specified number of bytes from the file
            raise ValidationError(f'Το μέγεθος υπερβαίνει τα 2Mb')
    return _check_file_size


def validate_email(form,email):   #όχι self αλλά form
        user=User.query.filter_by(email=email.data).first()
        if user: raise ValidationError('Το email υπάρχει ήδη') # μπορεί να μπει εντός της κλάσης όπως στο username η εκτός

class SignupForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])

    email = StringField(label="email",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), 
                                       Email(message="Παρακαλώ εισάγετε ένα σωστό email"),validate_email])

    password = StringField(label="password",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])
    
    password2 = StringField(label="Επιβεβαίωση password",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες"),
                                       EqualTo('password', message='Τα δύο πεδία password πρέπει να είναι τα ίδια')])
    submit = SubmitField('Εγγραφή')

    def validate_username(self,username):   #όταν θέλουμε να κάνουμε ένα custom validator,
                                            #   δεν χρειάζεται να το βάλουμε στους validators του username
        user=User.query.filter_by(username=username.data).first()
        if user: raise ValidationError('Το username υπάρχει ήδη')


class LoginForm(FlaskForm):
    email = StringField(label="email",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), 
                                       Email(message="Παρακαλώ εισάγετε ένα σωστό email")])

    password = StringField(label="password",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό.")])
    remember_me=BooleanField(label="Remember me")
    submit = SubmitField('Είσοδος')

class ArticleForm(FlaskForm):
    article_title = StringField(label="Τίτλος Άρθρου",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=50, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες")])

    article_body = TextAreaField(label="Κείμενο Άρθρου",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), 
                                       Length(min=5, message="Αυτό το πεδίο πρέπει να έχει τουλάχιστον 5 χαρακτήρες")])
    article_image=FileField(label="Εικόνα Προφίλ",validators=[Optional(strip_whitespace=True),FileAllowed(['jpg','jpeg','png']),maxImageSize(max_size=2)])
    
    submit = SubmitField('Αποστολή')

class AccountUpdateForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                       Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])

    email = StringField(label="email",
                           validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."), 
                                       Email(message="Παρακαλώ εισάγετε ένα σωστό email")])

    profile_image=FileField(label="Εικόνα Προφίλ",validators=[Optional(strip_whitespace=True),FileAllowed(['jpg','jpeg','png']),maxImageSize(max_size=2)])
    #Optional επιτρέπεται κενή εισαγωγή και το strip_whitespace γίνονται διαγραφή Ο "Optional" όμως φροντίζει να αποκλείσει κάθε άλλο validation που ακολουθεί στο πεδίο, κι έτσι
    #  στην περίπτωση που το πεδίο αυτό είναι κενό, ο "maxImageSize" δε θα τρέξει και κατά συνέπεια δε θα δώσει το σφάλμα που θα έδινε προσπαθώντας να διαβάσει ένα κενό πεδίο.
    submit = SubmitField('Αποστολή')

    def validate_username(self,username):
        if username.data !=current_user.username: # κάνε validation αν εχει αλλάξει από αυτό που είχε
            user=User.query.filter_by(username=username.data).first()
            if user: raise ValidationError('Το username υπάρχει ήδη')
    
    def validate_email(self,email):   
        if email.data !=current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user: raise ValidationError('Το email υπάρχει ήδη')