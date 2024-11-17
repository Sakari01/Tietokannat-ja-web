from app import app
from flask import render_template, request, redirect
import messages, users, boards

@app.route("/")
def index():
    board_list = boards.get_boards()
    return render_template("index.html", boards=board_list)

@app.route("/board/<int:board_id>")
def view_board(board_id):
    board_name, message_list = boards.get_board_messages(board_id)
    return render_template("board.html", board_name=board_name, messages=message_list, board_id=board_id)

@app.route("/board/new")
def new_board():
    return render_template("new_board.html")

@app.route("/board/create", methods=["POST"])
def create_board():
    name = request.form["name"]
    if boards.create_board(name):
        return redirect("/")
    else:
        return render_template("error.html", message="Lautaa ei voitu luoda")

@app.route("/send/<int:board_id>", methods=["POST"])
def send(board_id):
    content = request.form["content"]
    if messages.send(content, board_id):
        return redirect(f"/board/{board_id}")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

