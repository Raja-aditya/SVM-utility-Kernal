import numpy as np
from flask import Flask,request,jsonify,render_template
import joblib
import sqlite3
import pandas as pd
#import cv2



app = Flask(__name__)




@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route("/signup")
def signup():

    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
    con.commit()
    con.close()
    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("index.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("signup.html")


@app.route('/index')
def index():
	return render_template('index.html')



@app.route('/predict',methods=['POST'])
def predict():

    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]

    #final_features = np.array([val1,val2,val3,val4,val5,val6,val7,val8,val9,val10,val11,val12,val13,val14,val15,val16,val17,val18]).reshape(1,-1)
    model = joblib.load('model.sav')
    predict = model.predict(final4)
    if predict == 1:
        output = 'The Patient is not diagnosis with Breast Cancer based on Features given!'
    elif predict == 0:
        output = 'The Patient is diagnosis with Breast Cancer based on Features given!'
 
    return render_template('result.html',output=output)


@app.route('/notebook1')
def notebook1():
	return render_template('Survival Prediction Models at 5-Year Survival.html')


@app.route('/notebook2')
def notebook2():
	return render_template('Survival Prediction Models at 6-Year Survival.html')


@app.route('/notebook3')
def notebook3():
	return render_template('Survival Prediction Models at 7-Year Survival.html')


@app.route('/notebook4')
def notebook4():
	return render_template('Survival Prediction Models at 8-Year Survival.html')


@app.route('/notebook5')
def notebook5():
	return render_template('Survival Prediction Models at 9-Year Survival.html')


@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == "__main__":
    app.run()
