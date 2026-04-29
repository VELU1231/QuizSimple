from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from app.services.auth_service import get_current_user, login_admin, logout_admin

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET"])
def login_page():
    if get_current_user():
        return redirect(url_for("main.admin_panel"))
    error = request.args.get("error")
    next_url = request.args.get("next", "/admin")
    return render_template("admin_login.html", error=error, next_url=next_url)


@auth_bp.route("/login", methods=["POST"])
def login_action():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    next_url = request.form.get("next", "/admin")

    if login_admin(username, password):
        return redirect(next_url or "/admin")

    return redirect(url_for("auth.login_page", error="Invalid credentials", next=next_url))


@auth_bp.route("/logout", methods=["POST"])
def logout_action():
    logout_admin()
    return redirect(url_for("auth.login_page"))


@auth_bp.route("/me")
def me():
    user = get_current_user()
    return jsonify({"user": user, "auth_enabled": True})
