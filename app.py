from flask import Flask, render_template, request,redirect,url_for,make_response, session
from flask_bootstrap import Bootstrap

# from config import config
#from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2
from dotenv import load_dotenv
currentUserId = None
load_dotenv()
currentId = "-1"

err = 0
error = 0
url = os.environ.get("DATABASE_URL")
def createApp():
    global app
    app = Flask(__name__)
    Bootstrap(app)
    return app
createApp()
allUsers = """SELECT * FROM users"""

connection = psycopg2.connect(url)
#app.config.from_object(os.environ["APP_SETTINGS"])
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#db = SQLAlchemy(app)
@app.get("/getProfileInfo/<id>")
def profileInfo(id):
    with connection:
        with connection.cursor() as cursor:
                userId = """SELECT * FROM users WHERE id = {}""".format(id)
                cursor.execute(userId)
                
                data = cursor.fetchall()
    info = {"id": data[0][0], "name": data[0][1],"age": data[0][2],"password": data[0][3]}
    return info
@app.route("/profile/<id>", methods = ["POST","GET"])
def profile(id):
    global currentId
    with connection:
        with connection.cursor() as cursor:
            userId = """SELECT * FROM users WHERE id = {}""".format(id)
            cursor.execute(userId)
            print(request.cookies.get("id") == None)
            data = cursor.fetchall()
            info = {"id": data[0][0], "name": data[0][1],"age": data[0][2], "password": data[0][3]}
            if request.cookies.get("id") == None:
                response = make_response(render_template("profile.html",info = info,currentId = -1))
                response.set_cookie("id","-1")
                return response
            currentId = int(request.cookies.get("id"))
    return render_template("profile.html",info = info,currentId = currentId)
@app.route("/signout", methods = ["POST","GET"])
def signout():
    response = make_response(redirect(url_for("home")))
    response.set_cookie("id","-1")
    return response
            
# need to make new forms to update and Delete

     # params = config()
@app.route("/newUserPage")
def newUserPage():
    return render_template("newUser.html")
@app.route("/", methods = ["POST","GET"])
def home():
    isSignedIn = False
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(allUsers)
            data = cursor.fetchall()
            if request.cookies.get("id") != None and request.cookies.get("id") != "-1":
                   isSignedIn = True
    return render_template("index.html", data = data, isSignedIn = isSignedIn)
    
    
    
    
@app.route("/updateUser/<userId>", methods = ["POST","GET"])
def updateUser(userId):
    age = request.form["age"]
    name = request.form["name"]
    update = """UPDATE users SET name = %s, age = %s  WHERE id = %s"""
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(update,(name,int(age),userId))
    return redirect(url_for("home"))
    #Error in Update User!
@app.route("/deleteUser", methods = ["POST","GET"])
def deleteUser():
    userId = request.form["id"]
    delete = """DELETE FROM users WHERE id = %s """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(delete,(userId))
    return redirect(url_for("home"))


@app.route("/newUser", methods = ["POST","GET"])
def newUser():
    global currentId,err
    if request.method == "POST":
        age = request.form["Age"]
        name = request.form["Username"]
        password = request.form["pass"]
        passwordcheck = request.form["passcheck"]
        AllUser = """SELECT * FROM users """
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(AllUser)
                users = cursor.fetchall()
#        for user in users:
#            if name == user
        
        if password == passwordcheck:
            new = """INSERT INTO users (name,age,password) VALUES (%s,%s,%s) RETURNING id; """
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(new,(name,int(age),password))
            return redirect(url_for("home"))
        else:
            
            err = 1
            
        return render_template("newUser.html", err = err)
    
   
    
    
@app.route("/signIn", methods = ["POST","GET"])
def signIn():
    if request.method == "POST":
        name = request.form["Username"]
        password = request.form["Pass"]
        passwo = """SELECT * FROM users WHERE password = %s"""
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(passwo,(password,))
                dat = cursor.fetchall()
                
                
        try:
            if name == data[0][1]:
                form = request.form
                response = make_response(redirect(url_for("home")))
                response.set_cookie("pass",str(data[0][3]))
                print("work")
                return response
        except:
                   err = 2
                    
    
        username = """SELECT * FROM users WHERE name = %s"""
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(username,(name,))
                data = cursor.fetchall()
                print(data)
        
#        if data[0][1] == name:
#            print("work")
#            return redirect(url_for("signIn"))
#        else:
            try:
                if dat[0][3] == data[0][3]:
                    form = request.form
                    response = make_response(redirect(url_for("home")))
                    response.set_cookie("id",str(data[0][0]))
                    print("work")
                    return response
            except:
                error = 2
            
            return render_template("signIn.html", error = error)
    
    
    return render_template("signIn.html")
    

    
app.run("LOCALHOST",8080)
