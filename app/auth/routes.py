from app.auth import bp
from flask_login import current_user, login_user
from app.models import User
from flask import url_for, redirect, flash, render_template, request
from app.auth.forms import LoginForm
from app import db

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.api'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        
        login_user(user)        
        return redirect(url_for("main.api"))
    
    return render_template('auth/login.html', form=form)