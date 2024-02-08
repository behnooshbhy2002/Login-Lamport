from cyber import app, db, bcrypt
from flask import Flask, render_template, redirect, url_for, flash
from cyber.forms import RegisterForm, LoginForm, ResetForm
from cyber.modules import User
from hashlib import sha256 
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("home.html", index=True )

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()


        if user and user.get_password(password):
            if user.number_n == user.login_counter:
                flash(f"you have been logged in {user.number_n} times please set new **N**", "danger")
                return redirect("/resetpass")
            else:
                login_user(user, remember=form.remember_me.data)
                user.login_counter += 1
                user.password = password
                db.session.commit()
                flash(f"{user.full_name}, you are successfully logged in!", "success")
                return redirect("/index")
        else:
            flash("Email or Password is wrong","danger")
        if user.number_n == user.login_counter:
                flash(f"you have been logged in {user.number_n} times please set new **N**", "danger")
                return redirect("/resetpass")


    return render_template("login.html", title="Login", form=form, login=True )


@app.route("/register",methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        hash_pass = form.password.data
        for i in range(form.number_n.data):
            hash_pass = (sha256(hash_pass.encode('utf-8')).hexdigest())
        
        user = User(username=form.username.data, email=form.email.data, full_name=form.full_name.data, password=hash_pass, login_counter=0, number_n=form.number_n.data)
        db.session.add(user)
        db.session.commit()
        flash('you registered successfully', 'success')
        return redirect(url_for('index'))
        
    return render_template("register.html", title="Register", form=form, register=True)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out successfully', 'success')
    return redirect('/index')

@app.route('/resetpass', methods=['GET','POST'])
def reset():
    form = ResetForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        number_n = form.number_n.data
        user = User.query.filter_by(email=email).first()
        if user and password==user.password:
            user.login_counter = 0
            hash_pass = password
            for i in range(number_n):
                hash_pass = (sha256(hash_pass.encode('utf-8')).hexdigest())
            user.password = hash_pass
            user.number_n = number_n
            db.session.commit()
            flash(f"{user.full_name}, you are successfully changed **N**!", "success")
            return redirect("/index")
        else:
            flash("Email or Password is wrong","danger")

    return render_template("reset.html", title="Reset Password", form=form)