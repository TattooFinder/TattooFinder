from flask import Blueprint, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity

main_bp = Blueprint("main", __name__)

@main_bp.route("/dashboard")
@jwt_required()
def dashboard():
    return render_template("index.html")

@main_bp.route("/")
def root():
    return render_template("account.html")

@main_bp.route("/login")
@jwt_required(optional=True)
def login():
    current_user = get_jwt_identity()
    if current_user:
        return redirect(url_for("main.dashboard"))
    return render_template("account.html")
