from flask import Blueprint,render_template,flash,request,redirect,url_for
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.functions import user
from . import db
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user,current_user

auths=Blueprint('auth',__name__)

@auths.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form .get('email')
        password = request.form.get('password')

        user =User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("logged in",category="logged in")
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Invalid password,try again",category="invalid password try again ")
        else:
            flash('email does not exist')
            
    return render_template('login.html')

@auths.route('/logout')
@login_required
def logout():
    return redirect(url_for('auth.login'))

@auths.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password = request.form.get('password')
        password1=request.form.get('password1')
        user = User.query.filter_by(email=email).first()
        if user:
            flash("email already exists",category='error')
        elif len(email)<4:
            flash('email must be greater than 4 characters',category='email must be greater than 4 characters')
        elif password!=password1:
            flash('password does not match',category='password doesnt match')
        elif len(password)<7:
            flash('password must be greater than 7 characters',category='password be greater than 7 characters')
        else:
            new_user =User(email=email,first_name=first_name,password=generate_password_hash(password,method='sha256'))
            db.session.add(new_user)
            db.session.commit()


            flash('account created',category='success')
            login_user(user,remember=True)
            return redirect(url_for('views.home'))


         
    return render_template('signup.html')