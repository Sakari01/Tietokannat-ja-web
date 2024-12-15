from db import db
from sqlalchemy.sql import text

def add_favorite(user_id, board_id):
    sql = text("INSERT INTO favorites (user_id, board_id) VALUES (:user_id, :board_id)")
    db.session.execute(sql, {"user_id": user_id, "board_id": board_id})
    db.session.commit()
    return True

def remove_favorite(user_id, board_id):
    sql = text("DELETE FROM favorites WHERE user_id = :user_id AND board_id = :board_id")
    db.session.execute(sql, {"user_id": user_id, "board_id": board_id})
    db.session.commit()
    return True

def get_favorites(user_id):
    sql = text("""
        SELECT boards.id, boards.name 
        FROM favorites 
        JOIN boards ON favorites.board_id = boards.id 
        WHERE favorites.user_id = :user_id
    """)
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()
