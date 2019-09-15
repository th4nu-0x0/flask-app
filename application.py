import os

from flask import Flask, session, render_template, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker 
import requests
from passlib.hash import pbkdf2_sha256
#from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("/index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():

    session.clear()

    if request.method == "GET": 
        return render_template("/register.html")
    if request.method == "POST":
        user = request.form.get("username")
        pass1 = request.form.get("password")
        pass2 = request.form.get("cpassword")

    if pass1 != pass2 or pass1 is None or pass2 is None:
        return render_template("/error.html", message="Passwords do not match!")

    hashpass = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
    db.execute("INSERT INTO users (username, password) VALUES (:name, :pass)",
                {"name": user, "pass": hashpass})
    db.commit()
    return redirect('/login')
        
        #check wheather username alredy exsists
        #usercheck = db.execute("SELECT * FROM users WHERE username = :username", {"username":user})
        #user_exsist = usercheck.first()
        #if not user_exsist:
        


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("/login.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                         {"username": username})
        
        result = rows.fetchone()



        if result == None or not check_password_hash(result[1], request.form.get("password")):
            return render_template("error.html", message="looks like you have entered a wrong password")
        
        session["user_name"] = result[0]
        return redirect("/home")



    #else:
    #    return render_template("login.html")

@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("/home.html")

@app.route("/logout")
def logout():
    session.clear()
    
    return redirect("/")