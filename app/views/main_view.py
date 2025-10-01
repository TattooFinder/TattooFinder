from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/login")
def login():
    return render_template("conta/login.html")

@main_bp.route("/registro")
def registro():
    return render_template("conta/registro.html")
