from db import db
from sqlalchemy.sql import text

def get_zones():
    sql = text("SELECT id, name FROM zones ORDER BY id")
    result = db.session.execute(sql)
    return result.fetchall()


def create_zone(name):
    sql = text("INSERT INTO zones (name) VALUES (:name)")
    db.session.execute(sql, {"name": name})
    db.session.commit()
    return True
        

def delete_zone(zone_id):
    sql = text("DELETE FROM zones WHERE id = :id")
    db.session.execute(sql, {"id": zone_id})
    db.session.commit()
    return True
