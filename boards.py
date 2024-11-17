from db import db
from sqlalchemy.sql import text

def get_boards():
    sql = text("SELECT id, name FROM boards ORDER BY id")
    result = db.session.execute(sql)
    return result.fetchall()

def get_board_messages(board_id):
    sql_board = text("SELECT name FROM boards WHERE id=:board_id")
    board_result = db.session.execute(sql_board, {"board_id": board_id})
    board_name = board_result.fetchone()

    if not board_name:
        return None, []

    sql_messages = text("""
        SELECT M.content, U.username, M.sent_at
        FROM messages M
        JOIN users U ON M.user_id = U.id
        WHERE M.board_id = :board_id
        ORDER BY M.sent_at
    """)
    messages_result = db.session.execute(sql_messages, {"board_id": board_id})
    return board_name[0], messages_result.fetchall()

def create_board(name):
    try:
        sql = text("INSERT INTO boards (name) VALUES (:name)")
        db.session.execute(sql, {"name": name})
        db.session.commit()
        return True
    except Exception as e:
        print("Error creating board:", e)
        return False
