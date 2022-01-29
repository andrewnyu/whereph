from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db, login
from flask import flash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    compute_credits = db.Column(db.Integer)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    download_link = db.Column(db.String(256))

    uploaded = db.Column(db.DateTime)





#Utilities that interact with data models

def create_user(username, password, compute_credits):
    user = User.query.filter_by(username=username)
    if user is not None:
        flash ("user already exists")
    
    else:
        u = User(username=username, compute_credits=compute_credits)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()


def update_credits(user_id, credits):
    user = load_user(user_id)
    user.compute_credits += credits
    db.session.commit()

def add_transaction(user_id, cost, download_link):
    update_credits(user_id, -cost)
    transaction = Transaction(uploaded = db.func.now(), user=user_id, cost=cost, download_link=download_link)
    db.session.add(transaction)
    db.session.commit()
