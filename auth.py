from flask import Blueprint, render_template , request , flash, Flask, session, redirect
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from . import db
from os import path
from flask_misaka import Misaka

auth = Blueprint('auth', __name__)

@auth.route('/login',methods=['GET','POST'])
def login( ):
    if request.method == 'POST':
            # Get the user's credentials from the request
            email = request.form['email']
            password = request.form['password']
            # check if the user exists
            with open("user.txt", "r") as file:
                for line in file:
                    user_data = line.strip().split(',')
                    print(user_data[0])
                    if email == user_data[0]:
                        # check if the password match
                        if check_password_hash(password, user_data[2]):
                            session['email'] = email
                            flash('You are logged in')
                            return render_template('creer_modifier.html')
                        else:
                            flash('Invalid password')
                            return render_template('login.html')
                flash('Invalid email')
                return render_template('login.html')
    return render_template('login.html')
    

@auth.route('/logout')
def logout( ):
    return "<p>logout</p>"


@auth.route('/sign_up',methods=['GET','POST'])
def sign_up( ):
    if request.method== 'POST' :
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')        
        password2 = request.form.get('password2')
        status = request.form['status']
        user=[email,first_name,password1,status]
        if len(email) < 4:
            flash('email trop court',category='error')
        elif password1!=password2:
            flash('vos mot de passe sont differents',category='error')
        elif len(password1)<8:
            flash('mot de passe doit faire au moins 8 caractere', category='error')
        else :
            #user=User(email,first_name,generate_password_hash(password1,method='sha256'),status)
            #db.session.add(user)
            #db.session.commit()
            with open("user.txt",'a') as file:
                user=str(user)+"\n"
                file.write(user)

            flash('Account created',category='succes')
    return render_template("sign_up.html")


@auth.route('/save_text_to_file', methods=['GET','POST'])
def save_text_to_file():

    content = ''
    if 'email' in session:
        if request.method == 'POST':
            print(request.form)
            # store the text the user entered in a variable
            input_text = request.form['input_text']
            # name the file with the the text entered by the user
            file_name = request.form['file_name'] + ".txt"
            # check if the file already exists
            editname = request.form['file_name']
            if path.isfile(file_name) and file_name!="user.txt":
                if request.form['1'] == "Save/modify":
                        print('test')
                        with open(file_name, 'r') as file:
                                content = file.read()

                                print(content) 
                                print(file_name) 
                                return render_template("creer_modifier.html",name=editname, text=content)      
                if request.form['1'] == "edit":
                        print("dans le edit")
                        # open the file for writing
                        file = open(file_name, 'w')
                        # write the text to the file
                        file.write(input_text)
                        # close the file
                        file.close()
                        mkd_text =  input_text
                        #return render_template("mark.html",mkd_text=mkd_text)
                        return render_template("mark.html",mkd_text=mkd_text)
                    
            else:
                if file_name!= "user.txt":
                    # create the file
                    file = open(file_name, 'w')
                    # close the file
                    file.close()
    else :
        flash('you are not logged in')
        

    return render_template("creer_modifier.html", text=content)