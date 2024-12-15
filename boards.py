from db import db
from sqlalchemy.sql import text

def get_boards(zone_id=None):
    if zone_id:
        sql = text("""
            SELECT B.id, B.name, 
                   COUNT(M.id) AS message_count, 
                   MAX(M.sent_at) AS last_post
            FROM boards B
            LEFT JOIN messages M ON B.id = M.board_id
            WHERE B.zone_id = :zone_id
            GROUP BY B.id
            ORDER BY B.id
        """)
        result = db.session.execute(sql, {"zone_id": zone_id})
    else:
        sql = text("""
            SELECT B.id, B.name, 
                   COUNT(M.id) AS message_count, 
                   MAX(M.sent_at) AS last_post
            FROM boards B
            LEFT JOIN messages M ON B.id = M.board_id
            GROUP BY B.id
            ORDER BY B.id
        """)
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

def create_board(name, zone_id):
    sql = text("INSERT INTO boards (name, zone_id) VALUES (:name, :zone_id)")
    db.session.execute(sql, {"name": name, "zone_id": zone_id})
    db.session.commit()
    return True
