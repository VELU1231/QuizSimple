from flask import Blueprint, jsonify
from app.services.auth_service import get_current_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/me")
def me():
    """Placeholder: returns null user until auth is implemented."""
    user = get_current_user()
    return jsonify({"user": user, "auth_enabled": False})
