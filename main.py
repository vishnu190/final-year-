from flask import Flask, render_template, request
from flask import redirect, session
import os
import mysql.connector as c
##### creating flask instance ############
app=Flask(__name__)

# Creating secret key########
app.secret_key=os.urandom(24) # 24 character long 1:.8:00

### making a connection object ###########
conn = c.connect(host="ec2-44-194-113-156.compute-1.amazonaws.com",
                             user="ggbqhuevmlwnrr",
                             passwd ="0ced3e9d0c6b967a3b1a747bb4cfad1ca561c6abee91a4448378da4eb31add3c",
                             database ="d9r44556mhfpsv")
######## establish communication with server ##############
cursor = conn.cursor()

@app.route('/') # DECORATOR  for creating URLs
def login():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        redirect('/')

@app.route('/login_validation',methods=['POST']) #concept at43:00
def login_validation():
    email=request.form.get('email')
    password= request.form.get('password')


    #######  call the function > execute and then pass a query ########
    cursor.execute("""SELECT * FROM `final_project` WHERE `email` LIKE '{}' AND `password` LIKE '{}' """
                   .format(email, password))
    users=cursor.fetchall()

    if len(users) > 0:
        session['user_id'] = users[0][0] # 1st item of tuple
        return redirect('/home')
    else:
        return redirect('/')

@app.route('/add_users',methods=['POST'])
def add_users():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    cursor.execute("""INSERT INTO `final_project` (`user_id`, `name`, `email`,`password`)
    VALUES ('','{}','{}','{}') """.format(name, email, password))
    conn.commit() # commit for relational database during transactions

    cursor.execute(""" SELECT * FROM `final_project` WHERE `email` LIKE '{}'""". format(email))
    myuser = cursor.fetchall()
    session['user_id'] = myuser[0][0]


    return redirect('/home')

    print(users)

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')




    #return " The email is {} and the password is {} ".format(email,password)

if __name__ == "__main__":
    app.run(debug=True)