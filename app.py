from flask import Flask, render_template, jsonify, request, flash, redirect, url_for, session, abort, make_response, Response
from fastapi import Response
import os
import stripe
import sqlite3
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import UserMixin, login_user,LoginManager, login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import dbmanager
import random
import string
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date
import time
from datetime import datetime
import array
from fuzzywuzzy import fuzz
from difflib import SequenceMatcher
#from cryptography.fernet import Fernet

app = Flask(__name__)
db = SQLAlchemy(app) 
bcrypt=Bcrypt(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db?check_same_thread=False' #Connect to DB
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_COOKIE_SAMESITE'] = "Lax"
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") 
ImageFolder = os.path.join('static', 'Images')
app.config['UPLOAD_FOLDER'] = ImageFolder
app.static_folder = 'static'
Session(app) #Initiliase session for payments

DOMAIN = 'http://127.0.0.1:5000'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

"""DATABASE STUFF"""
'''
Base = declarative_base()
engine = create_engine("sqlite:///people.db")
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

class Person(Base):
    __tablename__ = 'people'

    id = Column("id", String, primary_key=True)
    email = Column("Email", String)
    parentname = Column("ParentName", String)
    childname = Column("ChildName", String)
    registeredlesson = Column("RegisteredLesson", String)

    def __init__(self,id, email, parentname, childname, registeredlesson):
        self.id = id
        self.email = email
        self.parentname = parentname
        self.childname = childname
        self.registeredlesson = registeredlesson

    def __repr__(self):
        return f"{self.id}, {self.email}, {self.parentname}, {self.childname}, {self.registeredlesson})"

def addPerson(email,parentName,childName,lessonName):

    generatedID = (''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=40)))
    person = Person(generatedID, email,parentName,childName,lessonName)
    session.add(person)
    session.commit()

    results = session.query(Person).all()
    print(results)
'''
#c.execute("SELECT * FROM people WHERE first='Stellan'")
#print(c.fetchone())

#User Registration Process
'''
hashed_password = bcrypt.generate_password_hash('v;&0x7*-k@*?wi0AG^VsW(^wVMvgCk')
new_user = User(username='XSsdTdNRGf', password=hashed_password)
db.session.add(new_user)
db.session.commit()
print("User Created")'''

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder": "username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder": "password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filterby(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username is already taken, pick another one"
            )
        
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder": "username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4,max=30)], render_kw={"placeholder": "password"})
    submit = SubmitField("Login")

    '''def validate_username(self, username):
        existing_user_username = User.query.filterby(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username is already taken, pick another one"
            )'''

#payment key
stripe.api_key = os.getenv("STRIPE_PRIVATE_KEY")

#Data for each Lesson
lessonData = {
    #Template
    #Name : [Price,age group, Term Duration,Hourly Duration, description]
    "Court Kangaroos": ['120 per Term','2-4 years','1 Term','Half Hour','Motor skill development and refinement for infants.  Children are progressed through both fine and gross motor activities, building their confidence and coordination.'],
    "Little Smash": ['130 per Term', '4-7 years','1 Term','Half Hour','An introductory program for 4-7 year olds that encourages a love for the sport and introduces the swing patterns for future development.'],
    "Young Beginners": ['180 per Term','7-10 years','1 Term','45 min','Tennis coaching for 7-10 year olds which encourages the child to learn the technical and physical skills required to play the game in a fun atmosphere'],
    "Beginner/Intermediate":['180 per Term','9-16','1 Term','1 Hour', 'A more progressive program for 9-16 year olds that encourages the child to further develop their technical and physical skill level and begin to become more tactically aware.'],
    "Advanced": ['180 per Term','9-16','1 Term', '1 Hour', 'Allows experienced players to further develop their skills in a more challenging environment. The use of spin and power are incorporated and game styles are discovered.'],
    "Competitive Squad": ['220 per Term','8-12', '1 Term', '1 Hour','	The most advanced level of the Junior Development program. This allows students, who compete in Pennant and competition, access to the most up to date high performance aids.'],
    "Private Lessons": ['80 per hour','3+','','As Requested','	A more personalised service that focuses on the needs of more competitive players. Usually one player per coach, but can be up to three.']
}

#Add a dictionary/list for timetable as well
lesssonTimes = {
    #Name: M T W T F S S | M T W T F SS
    "Court Kangaroos": ['','','','','','','',
                        '','','10:00am','','','','',],
    "Little Smash": ['3:30pm','','3:30pm','','3:30pm','11:00am','',
                    '','','3:30pm','3:45pm','3:30pm','','',],
    "Young Beginners": ['4:00pm','3:45pm','','3:45pm','4:00pm','9:00am','',
                        '','','4:00pm','4:15pm','4:00pm','','',],
    "Beginner/Intermediate": ['5:00pm','4:30pm','','4:30pm','5:00pm','10:00am','',
                            '','','5:00pm','5:00pm','4:45pm','','',],
    "Advanced": ['5:00pm','','','','5:00pm','','',
                '','','','','','','',],
    "Competitive Squad": ['','','4:00pm','','','','',
                        '','','','','','','',]
}

#Add Pricing
lessonPrices = {
    "Court Kangaroos": os.getenv("Court_Kangaroos"),
    "Little Smash": os.getenv("Little_Smash"),
    "Young Beginners": os.getenv("Young_Beginners"),
    "Beginner/Intermediate":os.getenv("Beginner_Intermediate"),
    "Advanced": os.getenv("Advanced"),
    "Competitive Squad": os.getenv("Competitive_Squad"),
    "Private Lessons":''
}

@app.route('/')
def home():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    TennisCoaching = os.path.join(app.config['UPLOAD_FOLDER'], 'tennis_coaching.jpg')
    return render_template("index.html", logo=logo, TennisCoaching=TennisCoaching)

@app.route('/select')
def select():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    TennisCoaching = os.path.join(app.config['UPLOAD_FOLDER'], 'tennis_coaching.jpg')
    return render_template("select.html", logo=logo, TennisCoaching=TennisCoaching, lessonData=lessonData)

@app.route('/payment')
def payment():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    ClayCourt = os.path.join(app.config['UPLOAD_FOLDER'], 'Clay_Court_Tennis_1200x1200.webp')
    return render_template("lessonpayment.html", logo=logo, ClayCourt=ClayCourt)

#All Lessons
@app.route('/CourtKangaroos')
def CourtKangaroos():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    ClayCourt = os.path.join(app.config['UPLOAD_FOLDER'], 'Clay_Court_Tennis_1200x1200.webp')
    lessonName = "Court Kangaroos"
    return render_template("lessondetails.html", ClayCourt=ClayCourt, logo=logo, lessonData=lessonData, name=lessonName,times=lesssonTimes, lessonPrices=lessonPrices)

@app.route('/LittleSmash')
def LittleSmash():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    ClayCourt = os.path.join(app.config['UPLOAD_FOLDER'], 'Clay_Court_Tennis_1200x1200.webp')
    lessonName = "Little Smash"
    return render_template("lessondetails.html", ClayCourt=ClayCourt, logo=logo, lessonData=lessonData, name=lessonName,times=lesssonTimes, lessonPrices=lessonPrices)

@app.route('/YoungBeginners')
def YoungBeginners():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    ClayCourt = os.path.join(app.config['UPLOAD_FOLDER'], 'Clay_Court_Tennis_1200x1200.webp')
    lessonName = "Young Beginners"
    return render_template("lessondetails.html", ClayCourt=ClayCourt, logo=logo, lessonData=lessonData, name=lessonName,times=lesssonTimes, lessonPrices=lessonPrices)

@app.route('/BeginnerIntermediate')
def BeginnerIntermediate():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    ClayCourt = os.path.join(app.config['UPLOAD_FOLDER'], 'Clay_Court_Tennis_1200x1200.webp')
    lessonName = "Beginner/Intermediate"
    return render_template("lessondetails.html", ClayCourt=ClayCourt, logo=logo, lessonData=lessonData, name=lessonName,times=lesssonTimes, lessonPrices=lessonPrices)

@app.route('/Advanced')
def Advanced():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    ClayCourt = os.path.join(app.config['UPLOAD_FOLDER'], 'Clay_Court_Tennis_1200x1200.webp')
    lessonName = "Advanced"
    return render_template("lessondetails.html", ClayCourt=ClayCourt, logo=logo, lessonData=lessonData, name=lessonName,times=lesssonTimes, lessonPrices=lessonPrices)

@app.route('/CompetitiveSquad')
def CompetitiveSquad():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    ClayCourt = os.path.join(app.config['UPLOAD_FOLDER'], 'Clay_Court_Tennis_1200x1200.webp')
    lessonName = "Competitive Squad"
    return render_template("lessondetails.html", ClayCourt=ClayCourt, logo=logo, lessonData=lessonData, name=lessonName,times=lesssonTimes, lessonPrices=lessonPrices)

@app.route('/PrivateLessons')
def PrivateLessons():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    ClayCourt = os.path.join(app.config['UPLOAD_FOLDER'], 'Clay_Court_Tennis_1200x1200.webp')
    lessonName = "Private Lessons"
    return render_template("lessondetails.html", ClayCourt=ClayCourt, logo=logo, lessonData=lessonData, name=lessonName,times=lesssonTimes, lessonPrices=lessonPrices)

@app.route('/success')
def success():
    return render_template("success.html")


@app.route('/tmpdashboard', methods=['GET','POST'])
@login_required
def tmpdashboard():
    # Get date
    parentNames = []
    childNames = []
    searchResults = []
    query = dbmanager.queryPeople()
    for object in query:
        childNames.append(object.childname)
        parentNames.append(object.parentname)
        
    # print(parentNames)
    # print(childNames)

    if request.method == "GET":
        print("get detected")
        
        # Search for users
        if(request.args.get('search-input') and request.args.get('search-input') != ""): #Incase get request is empty
            for person in query:
                # Check similarity for search
                s = SequenceMatcher(None, request.args.get('search-input'), person.parentname)
                if(s.ratio() >= 0.7):
                    searchResults.append(person)
            
            # print(searchResults)
            query=searchResults
        else:
            print("passed")
            # print(request.args.get('money'))


        # Filter Users
        lesson = request.args.get('lessonSelect')
        if(lesson != None and lesson != ""): #Check if user input something
            for user in query:
                if user.lessonname != lesson:
                    query.remove(user)

    #Obtain date
    date = datetime.today().strftime('%d/%m/%Y')

    #Use date to calculate monetisation this month
    totalThisMonth = 0
    paymentsToday = 0
    earliestDay = 0

    month = int(date.split("/")[1])
    print("Month:",month)
    
    for user in query:
        usermonth = int(date.split("/")[1])
        if usermonth == month:
            totalThisMonth += user.amount

        if user.date == date:
            paymentsToday += 1

    #Reverse list for highest recency
    query.reverse()
    # print("Reached Dashboard")
    return render_template("dashboard2.html", date=date, people=query, paymentsToday = paymentsToday, totalPayments=len(query), totalThisMonth = totalThisMonth)

@app.route('/customerdashboard', methods=['GET','POST'])
@login_required
def customersdashboard():
    # Get date
    parentNames = []
    childNames = []
    searchResults = []
    query = dbmanager.queryPeople()
    for object in query:
        childNames.append(object.childname)
        parentNames.append(object.parentname)
        
    # print(parentNames)
    # print(childNames)

    if request.method == "GET":
        print("get detected")
        if(request.args.get('search-input') and request.args.get('search-input') != ""): #Incase get request is empty
            for person in query:
                # Check similarity for search
                s = SequenceMatcher(None, request.args.get('search-input'), person.parentname)
                if(s.ratio() >= 0.7):
                    searchResults.append(person)
            
            # print(searchResults)
            query=searchResults
        else:
            print("passed")
            # print(request.args.get('money'))
        
        # Filter Users
        lesson = request.args.get('lessonSelect')
        newQuery = []
        if(lesson == "Any" or lesson == None or lesson ==""):
            pass
        else:
            print("got here somehow...")
            for user in query:
                if user.registeredlesson == lesson:
                    # print(user.parentname)
                    newQuery.append(user)

            query = newQuery

    date = datetime.today().strftime('%d/%m/%Y')
    
    #Reverse list for highest recency
    query.reverse()

    return render_template("paymentview.html", date=date, people=query, paymentToday = "0")

@app.route('/cancel')
def cancel():
    return render_template("cancel.html")

@app.route('/admin', methods=['GET','POST'])
def admin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('tmpdashboard'))
            
    return render_template("admin.html", form=form)

# @app.route("/dashboard", methods=['GET','POST'])
# @login_required
# def dashboard():
#     # Get date
#     parentNames = []
#     childNames = []
#     searchResults = []
#     query = dbmanager.queryPeople()
#     for object in query:
#         childNames.append(object.childname)
#         parentNames.append(object.parentname)
        
#     # print(parentNames)
#     # print(childNames)

#     if request.method == "GET":
#         print("get detected")
#         if(request.args.get('search-input') and request.args.get('search-input') != ""): #Incase get request is empty
#             for person in query:
#                 # Check similarity for search
#                 s = SequenceMatcher(None, request.args.get('search-input'), person.parentname)
#                 # print("the string is:", request.args.get('search-input'))
#                 # levenshtein_distance = fuzz.ratio(
#                 #     request.args.get('search-input'), person.parentname
#                 #     )
#                 if(s.ratio() >= 0.7):
#                     searchResults.append(person)
            
#             # print(searchResults)
#             query=searchResults
#         else:
#             print("passed")
#             # print(request.args.get('money'))
        

    
#     date = datetime.today().strftime('%d/%m/%Y')
#     # print("Reached Dashboard")
#     return render_template("dashboard.html", date=date, people=query, paymentToday = "")

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin'))

@app.route('/create-checkout-session', methods=['POST','GET'])
def create_checkout_session():
    #Retrieve User Data
    if request.method == 'POST':
        priceIDname = request.form.get('price_id')
        priceID = lessonPrices.get(priceIDname)
        
        #Attempt to create payment sesssion
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # add the name here
                        # ex:
                        'price': priceID,
                        'quantity': 1,
                    },
                ],
                custom_fields=[
                    {
                        "key": "ParentalName",
                        "label": {"type": "custom", "custom": "Parents Name"},
                        "type": "text",
                    },
                                        {
                        "key": "ChildName",
                        "label": {"type": "custom", "custom": "Child's Name"},
                        "type": "text",
                    }
                ],
                mode='payment',
                success_url= DOMAIN + '/success',
                cancel_url= DOMAIN + '/cancel',
            )
        except Exception as e:
            return str(e)
            
        return redirect(checkout_session.url, code=303)

    if request.method == 'GET':
        return "Invalid Request"

@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('Webhook called')

    if request.content_length > 1024 * 1024: #1mb
        print('REQUEST TOO BIG')
        abort(400)

    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = os.environ.get('ENDPOINT_SECRET')
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )

    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        payment_intent = event.data.object 

        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        print("Payment was succesful!")

        #line_items = stripe.checkout.Session.list_line_items(session['id'],limit=5)
        line_items = stripe.checkout.Session.list(limit=1)
        tmp = stripe.checkout.Session.list_line_items(line_items['data'][0]['id'], limit=1)
        
        product_id = tmp['data'][0]['price']['id']

        #iterate through, find relevant ID and set that
        lesson = "Unkown";
        for key in lessonPrices:
            if(lessonPrices[key] == product_id):
                lesson = key

        print("ID:", lesson)
        parent = line_items['data'][0]['custom_fields'][0]['text']['value']
        child = line_items['data'][0]['custom_fields'][1]['text']['value']
        email = line_items['data'][0]['customer_details']['email']
        amount = line_items['data'][0]['amount_total']
        amount = int(amount) / 100
        #print(line_items)
        print("---------------------")
        print("Parent is", parent)
        print("Child is", child)
        print("Email is", email)
        print("Amount paid was", amount)
        today = date.today()
        dt = today.strftime("%d/%m/%Y")
        # print("d1 =", dt)
        # print(line_items)
        dbmanager.addPerson(email, parent, child, lesson, dt, amount)
        print(parent,"was added to the database")

        #Create Person object
        #Upload Person object to database
        #Setup the view

    return {}

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == "__main__":
    app.run(debug=True)