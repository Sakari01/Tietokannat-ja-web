from app import app
from db import db
from flask import render_template, request, redirect, session, abort
from sqlalchemy.sql import text
import messages, users, boards, zones
import favorites
import secrets

@app.route("/")
def home():
    zone_list = zones.get_zones()
    favorites_list = []

    if users.is_user():
        favorites_list = favorites.get_favorites(users.user_id())

    return render_template("home.html", zones=zone_list, favorites=favorites_list)

    
@app.route("/zone/<int:zone_id>")
def view_zone(zone_id):
    board_list = boards.get_boards(zone_id)
    return render_template("index.html", boards=board_list, zid=zone_id)
    
@app.route("/zone/new")
def new_zone():
    allow = False
    if users.is_admin():
        allow = True

    if not allow:
        return render_template("error.html", message="Ei admin-oikeuksia")

    return render_template("new_zone.html")

    
@app.route("/zone/create", methods=["POST"])
def create_zone():
    name = request.form["name"]
    if zones.create_zone(name):
        return redirect("/")
    else:
        return render_template("error.html", message="aluetta ei voitu luoda")
        
@app.route("/zone/del")
def zone_del():
    allow = False
    if users.is_admin():
        allow = True

    if not allow:
        return render_template("error.html", message="Ei admin-oikeuksia")
        
    zone_list = zones.get_zones()    
    return render_template("zone_del.html", zones=zone_list)
    
@app.route("/zone/delete", methods=["POST"])
def zone_delete():
    allow = False
    if users.is_admin():
        allow = True

    if not allow:
        return render_template("error.html", message="Ei admin-oikeuksia")

    zone_id = request.form["zone_id"]
    if zones.delete_zone(zone_id):
        return redirect("/")
    else:
        return render_template("error.html", message="Aluetta ei voitu poistaa")



@app.route("/board/<int:board_id>")
def view_board(board_id):
    board_name, message_list = boards.get_board_messages(board_id)
    is_favorite = False
    is_user = users.is_user()

    if is_user:
        user_id = users.user_id()
        is_favorite = db.session.execute(
            text("SELECT 1 FROM favorites WHERE user_id = :user_id AND board_id = :board_id"),
            {"user_id": user_id, "board_id": board_id}
        ).fetchone() is not None

    return render_template(
        "board.html",
        board_name=board_name,
        messages=message_list,
        board_id=board_id,
        is_favorite=is_favorite,
        is_user=is_user
    )

@app.route("/zone/<int:zone_id>/board/new")
def new_board(zone_id):
    return render_template("new_board.html", zid=zone_id)

@app.route("/zone/<int:zone_id>/board/create", methods=["POST"])
def create_board(zone_id):
    name = request.form["name"]
    print(f"Attempting to create board: name={name}, zone_id={zone_id}")
    correct = boards.create_board(name, zone_id)
    print(f"Board creation status: {correct}")
    if correct:
        return redirect(f"/zone/{zone_id}")
    else:
        return render_template("error.html", message="Aluetta ei voitu luoda")


@app.route("/send/<int:board_id>", methods=["POST"])
def send(board_id):

    content = request.form["content"]
    if messages.send(content, board_id):
        return redirect(f"/board/{board_id}")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")
        
        
        
@app.route("/board/<int:board_id>/favorite", methods=["POST"])
def add_favorite(board_id):
    if not users.is_user():
        return render_template("error.html", message="Sinun täytyy kirjautua sisään")

    user_id = users.user_id()
    if favorites.add_favorite(user_id, board_id):
        return redirect(f"/board/{board_id}")
    else:
        return render_template("error.html", message="Lisäystä ei voitu suorittaa, yritä uudelleen")

@app.route("/board/<int:board_id>/unfavorite", methods=["POST"])
def remove_favorite(board_id):
    if not users.is_user():
        return render_template("error.html", message="Sinun täytyy kirjautua sisään")

    user_id = users.user_id()
    if favorites.remove_favorite(user_id, board_id):
        return redirect(f"/board/{board_id}")
    else:
        return render_template("error.html", message="Poistamista ei voitu suorittaa, yritä uudelleen")        

        
    

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
        is_admin = request.form.get("is_admin") == "true"
        
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1, is_admin):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
            
