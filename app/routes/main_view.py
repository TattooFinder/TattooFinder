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