from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False

def logout():
    del session["user_id"]

def register(username, password, is_admin=False):
    hash_value = generate_password_hash(password)
    
    sql = text("INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :is_admin)")
    db.session.execute(sql, {"username": username, "password": hash_value, "is_admin": is_admin})
    db.session.commit()
    
    return login(username, password)


def user_id():
    return session.get("user_id", 0)
    
def is_user():
    return "user_id" in session

def is_admin():
    user_id = session.get("user_id")
    if not user_id:
        return False

    sql = text("SELECT is_admin FROM users WHERE id = :id")
    result = db.session.execute(sql, {"id": user_id}).fetchone()
    return result and result.is_admin

