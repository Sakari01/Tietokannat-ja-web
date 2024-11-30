from db import db
from sqlalchemy.sql import text

def get_zones():
    sql = text("SELECT id, name FROM zones ORDER BY id")
    result = db.session.execute(sql)
    return result.fetchall()


def create_zone(name):
    try:
        sql = text("INSERT INTO zones (name) VALUES (:name)")
        db.session.execute(sql, {"name": name})
        db.session.commit()
        return True
    except Exception as e:
        print("Error creating zone:", e)
        return False
