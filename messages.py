from db import db
from sqlalchemy.sql import text
import users

def get_list(board_id):
    sql = text("""
        SELECT M.content, U.username, M.sent_at
        FROM messages M
        JOIN users U ON M.user_id = U.id
        WHERE M.board_id = :board_id
        ORDER BY M.id
    """)
    result = db.session.execute(sql, {"board_id": board_id})
    return result.fetchall()

def send(content, board_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("""
        INSERT INTO messages (content, user_id, board_id, sent_at)
        VALUES (:content, :user_id, :board_id, NOW())
    """)
    db.session.execute(sql, {"content": content, "user_id": user_id, "board_id": board_id})
    db.session.commit()
    return True
