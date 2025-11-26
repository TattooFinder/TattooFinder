from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies
from werkzeug.security import check_password_hash
from app.db import fetch_one

main_bp = Blueprint(
    "main",
    __name__,
    url_prefix="/",
    template_folder="../../frontEnd",
    static_folder="../../frontEnd",
)


@main_bp.route("/")
def root():
    return render_template("index.html")


@main_bp.route("/login")
def login():
    return render_template("auth.html")


@main_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@main_bp.route("/user")
def user_page():
    return render_template("user.html")


@main_bp.route("/search")
def search_page():
    return render_template("search.html")


@main_bp.route("/tattooer")
def tattooer_page():
    return render_template("tattooer.html")


@main_bp.route("/sobre-contato")
def about_page():
    return render_template("sobreContato.html")